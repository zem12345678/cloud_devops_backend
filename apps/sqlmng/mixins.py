#coding=utf8
from rest_framework.exceptions import ParseError
from utils.tasks import send_mail
from utils.basemixins import AppellationMixins
from utils.dbcrypt import prpcrypt
from utils import inception
from .models import *
import copy,os,re,json
import time,datetime
import subprocess
import configparser
from django.conf import settings
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from guardian.models import UserObjectPermission, GroupObjectPermission
from utils.basemixins import HttpMixin, AppellationMixin, PromptMixin
from utils.basecomponent import DateEncoder
from utils.baseviews import ReturnFormatMixin as res
from utils.sqltools import Inception, SqlQuery, AutoQuery
from utils.exceptions import NotValid
from utils.lock import RedisLock
from utils.wrappers import timer
from .data import inception_conn
from django.db.models import Count,Q


class ActionMxins(AppellationMixins, object):

    action_desc_map = {
        'execute': '代执行',
        'reject': '代放弃',
        'rollback': '代回滚'
    }

    def get_db_addr(self, user, password, host, port, actiontype):
        pc = prpcrypt()
        password = pc.decrypt(password)
        dbaddr = '--user={}; --password={}; --host={}; --port={}; {};'.format(user, password, host, port, actiontype)
        return dbaddr

    def mail(self, sqlobj, mailtype):
        if sqlobj.env == self.env_prd:  # 线上环境，发邮件提醒
            username = self.request.user.username
            treater = sqlobj.treater  # 执行人
            commiter = sqlobj.commiter  # 提交人
            mailto_users = [treater, commiter]
            mailto_users = list(set(mailto_users))  # 去重（避免提交人和执行人是同一人，每次收2封邮件的bug）
            mailto_list = [u.email for u in UserProfile.objects.filter(username__in = mailto_users)]
            # 发送邮件，并判断结果
            send_mail.delay(mailto_list, username, sqlobj.id, sqlobj.remark, mailtype, sqlobj.sql_content, sqlobj.db.name)

    def replace_remark(self, sqlobj):
        username = self.request.user.username
        uri = self.request.META['PATH_INFO'].split('/')[-2]
        if username != sqlobj.treater:  # 如果是dba或总监代执行的
            sqlobj.remark +=  '   [' + username + self.action_desc_map.get(uri) + ']'
        sqlobj.save()

    def check_execute_sql(self, db_id, sql_content):
        dbobj = DbConf.objects.get(id = db_id)
        db_addr = self.get_db_addr(dbobj.user, dbobj.password, dbobj.host, dbobj.port, self.action_type)  # 根据数据库名 匹配其地址信息，"--check=1;" 只审核
        sql_review = inception.table_structure(db_addr, dbobj.name, sql_content)  # 审核
        result, status = sql_review.get('result'), sql_review.get('status')
        # 判断检测错误，有则返回
        if status == -1 or len(result) == 1:  # 兼容2种版本的抛错
            raise ParseError({self.connect_error: result})
        success_sqls = []
        exception_sqls = []
        for sql_result in result:
            error_message = sql_result[4]
            if error_message == 'None' or re.findall('Warning', error_message):
                success_sqls.append(sql_result)
            else:
                exception_sqls.append(error_message)
        if exception_sqls and self.action_type == '--enable-check':
            raise ParseError({self.exception_sqls: exception_sqls})
        return (success_sqls, exception_sqls)

class GuardianPermission(object):

    permission_models = [UserObjectPermission, GroupObjectPermission]

    def get_related_status(self, instance):
        for model in self.permission_models:
            if model.objects.filter(object_pk=instance.id):
                return 1
        return 0

    def delete_relation(self, instance):
        for model in self.permission_models:
            queryset_permission = model.objects.filter(object_pk=instance.id)
            queryset_permission.delete()

class FixedDataMixin(object):

    def get_queryset(self):
        model = self.serializer_class.Meta.model
        objects = model.objects
        queryset = objects.all()
        if queryset.count() != len(self.source_data):
            queryset.delete()
            data = [model(**row) for row in self.source_data]
            objects.bulk_create(data)
            queryset = objects.all()
        return queryset

class ChangeSpecialCharacterMixin(object):
    special_character_list = ['*']
    transference_character = '\\'

    def convert(self, forbidden_words):
        forbidden_words_list = forbidden_words.split('/')
        forbidden_list = []
        for word in forbidden_words_list:
            if word:
                if word in self.special_character_list:
                    word = '{}{}'.format(self.transference_character, word)
                forbidden_list.append(word)
        return forbidden_list

    def reverse(self, forbidden_list):
        fb_words = []
        for word in forbidden_list:
            if self.transference_character in word:
                word = word.replace(self.transference_character, '')
            fb_words.append(word)
        if len(fb_words) == 1:
            return fb_words[0]
        return fb_words

class InceptionConn(object):
    error_tag = 'error'
    model = InceptionConnection

    def get_cmd(self, sub_cmd):
        conn = self.get_inception_conn()
        return '{} -e "{}" '.format(conn, sub_cmd)

    def get_inception_conn(self):
        instance = self.model.objects.first()
        obj = instance or self.model.objects.get_or_create(**inception_conn[0])[0]
        return 'mysql -h{} -P{}'.format(obj.host, obj.port)

class CheckConn(InceptionConn, AutoQuery):
    conf = configparser.ConfigParser()
    file_path = settings.INCEPTION_SETTINGS.get('file_path')

    def get_target_databases(self, request):
        databases = self.get_databases(request.data)
        return [db[0] for db in databases]

    def get_alive_databases(self, cluster, env, host):
        queryset = DbConf.objects.filter(env=env, host=host)
        if cluster:
            queryset = queryset.filter(cluster_id=cluster)
        return [db.name for db in queryset]

    def get_db_list(self, request):
        ret = res.get_ret()
        cluster = request.data.pop('cluster')
        env = request.data.pop('env')
        host = request.data.get('host')
        target_databases = self.get_target_databases(request)
        alive_databases = self.get_alive_databases(cluster, env, host)
        databases = set(target_databases) - set(alive_databases)
        ret['data'] = databases
        return ret

    def inception_conn(self, *args):
        ret = res.get_ret()
        sub_cmd = "inception get variables"
        cmd = self.get_cmd(sub_cmd)
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines = result.stdout.readlines()
        last_item = lines[-1].decode('gbk') if len(lines) > 0 else ''
        if self.error_tag in last_item.lower():
            ret['status'] = -1
            ret['data'] = last_item
        return ret

    def inception_backup(self, request):
        self.conf.read(self.file_path)
        password = self.conf.get('inception', 'inception_remote_system_password')
        params = request.data
        params['password'] = password
        params['db'] = 'inception'
        self.conn_database(params)
        return res.get_ret()

    def update_target_db(self, request):
        pk = request.data.get('id')
        instance = DbConf.objects.get(pk=pk)
        params = {
            'db': instance.name,
            'host': instance.host,
            'port': instance.port,
            'user': instance.user,
            'password': prpcrypt.decrypt(instance.password)
        }
        self.conn_database(params)
        return res.get_ret()

class HandleInceptionSettingsMixin(InceptionConn):
    backup_variables = [
        'inception_remote_backup_host',
        'inception_remote_backup_port',
        'inception_remote_system_user',
        'inception_remote_system_password'
    ]

    def get_inception_backup(self):
        return {variable:self.get_status(variable) for variable in self.backup_variables}

    def get_status(self, variable_name):
        filter_words = [variable_name, '\t', '\n']
        sub_cmd = "inception get variables '{}'".format(variable_name)
        cmd = self.get_cmd(sub_cmd)
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines = result.stdout.readlines()
        if not lines:
            return None
        ret = lines[-1].decode('gbk')
        if self.error_tag in ret.lower():
            return None
        for word in filter_words:
            ret = ret.replace(word, '')
        return ret

    def set_variable(self, request):
        request_data = request.data
        variable_name = request_data.get('variable_name')
        variable_value = request_data.get('variable_value')
        sub_cmd = "inception set {}={}".format(variable_name, variable_value)
        cmd = self.get_cmd(sub_cmd)
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def get_osc_data(self, request):
        sha = request.GET.get('sha')
        sub_cmd = "inception get osc_percent '{}'".format(sha)
        cmd = self.get_cmd(sub_cmd)
        data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return data.stdout.readlines()

class CheckStatusMixin(HttpMixin, AppellationMixin, PromptMixin):

    @property
    def init(self):
        status_map = \
        {
            self.urn_execute: {
                'status_list': [-1, 3],
                'warning': self.action_status_warning_execute
            },
            self.urn_reject: {
                'status_list': [-2, -1, 3, 4, 6],
                'warning': self.action_status_warning_reject
            },
            self.urn_approve: {
                'status_list': [-1],
                'warning': self.action_status_warning_approve
            },
            self.urn_disapprove: {
                'status_list': [-1],
                'warning': self.action_status_warning_approve
            },
            self.urn_rollback: {
                'status_list': [0],
                'warning': self.action_status_warning_rollback
            },
            self.urn_cron: {
                'status_list': [-1, 3, 5],
                'warning': self.action_status_warning_cron
            },
            self.urn_database_order_approve: {
                'status_list': [0],
                'warning': self.action_status_warning_database_order_manage
            },
            self.urn_database_order_disapprove: {
                'status_list': [0],
                'warning': self.action_status_warning_database_order_manage
            },
            self.urn_database_order_reject: {
                'status_list': [0, 1, 2],
                'warning': self.action_status_warning_database_order_reject
            }

        }
        return status_map

    def check_status(self, instance):
        action = self.get_urls_action(self.request)
        status_list = self.init[action]['status_list']
        warning = self.init[action]['warning']
        if instance.status not in status_list:
            raise ParseError(warning)

class ActionMixin(HttpMixin, AppellationMixin, PromptMixin):

    type_select_tag = 'select'
    action_type_execute = '--enable-execute'
    action_type_check = '--enable-check'
    success_tag = 'Execute Successfully\nBackup successfully'

    def get_reject_step(self, instance):
        user = self.request.user
        if self.has_flow(instance):
            if user.is_superuser:
                return 1 if instance.commiter == user.username else 2
            else:
                return self.reject_steps.get(user.role)

    @staticmethod
    def get_current_step(instance):
        steps = instance.work_order.step_set.all()
        current = 0
        for step in steps:
            if step.status not in [-1, 0]:
                current += 1
        return current

    @property
    def is_manual_review(self):
        instance = Strategy.objects.first()
        if not instance:
            instance = Strategy.objects.create()
        return instance.is_manual_review

    def handle_workflow(self, call_type, status, step_number, instance=None):
        instance = instance or self.get_object()
        if self.has_flow(instance):
            if call_type == 1:
                if status == 1:
                    self.save_instance(instance.work_order, True)
            step_instance = instance.work_order.step_set.order_by('id')[step_number]
            self.save_instance(step_instance, status)
            if call_type == 3:
                steps = instance.work_order.step_set.all()
                steps_behind = steps.filter(id__gt=step_instance.id)
                for step in steps_behind:
                    self.save_instance(step, -1)

    def get_db_conf(self, user, password, host, port, actiontype):
        password = prpcrypt.decrypt(password)
        return '--user={}; --password={}; --host={}; --port={}; {};'.format(user, password, host, port, actiontype)

    def has_flow(self, instance):
        return instance.is_manual_review is True and instance.env == self.env_prd

    @classmethod
    def save_instance(cls, instance, status=None):
        if status is not None:
            instance.status = status
        instance.save()

    def check_lock(self, instance):
        if not RedisLock.locked(instance.id):
            raise ParseError(self.task_locked.format(instance.id))

    def filter_select_type(self, instance):
        if instance.type == self.type_select_tag:
            raise ParseError(self.type_warning)

    def check_valid_date(self, cron_time):
        date_format = settings.CELERY_BUSINESS_PARAMS.get('date_format')
        try:
            time.mktime(time.strptime(cron_time, date_format))
        except Exception:
            raise ParseError(self.invalid_date_warning.format(cron_time))

    def filter_date(self, queryset):
        date_range = self.request.GET.get('daterange')
        if queryset and date_range:
            return queryset.filter(createtime__range=date_range.split(','))
        return queryset

    def check_rollback_able(self, instance):
        if not instance.rollback_able:
            raise ParseError(self.not_rollback_able)

    def check_execute_sql(self, db_id, sql_content, action_type):
        db_instance = DbConf.objects.get(id=db_id)
        db_conf = self.get_db_conf(db_instance.user, db_instance.password, db_instance.host, db_instance.port, action_type)
        sql_review = Inception(sql_content, db_instance.name).inception_handle(db_conf)
        result, status = sql_review.get('result'), sql_review.get('status')
        if status == -1 or len(result) == 1:
            raise ParseError({self.connect_error: result})
        success_sql_list = []
        exception_sql_list = []
        for sql_result in result:
            error_message = sql_result[4]
            if error_message == 'None':
                success_sql_list.append(sql_result)
            else:
                exception_sql_list.append(error_message)
        if exception_sql_list and action_type == self.action_type_check:
            raise NotValid(exception_sql_list)
        return success_sql_list, exception_sql_list, json.dumps(result)

    def replace_remark(self, instance, action=None, user=None):
        user = user or self.request.user
        username = user.username
        action = action or self.get_urls_action(self.request)
        if username != instance.treater:
            instance.remark +=  '   [' + username + self.action_desc_map.get(action) + ']'
        if instance.work_order.status is True:
            steps = instance.work_order.step_set.all()
            step_obj_second = steps[1]
            if user and not (user == step_obj_second.user and action == 'reject'):
                step_obj = steps[0]
                step_obj.user = user
                self.save_instance(step_obj)

class MailMixin(AppellationMixin):

    def get_extend_mail_list(self, user):
        mail_list_extend = user.mail_list_extend
        return mail_list_extend.split() if mail_list_extend else []

    def get_username(self, user):
        if not isinstance(user, str):
            user = user.username
        return user

    def get_mail_list(self, instance):
        commiter = self.get_username(instance.commiter)
        treater = self.get_username(instance.treater)
        user = UserProfile.objects.get(username=commiter)
        admin_mail = user.admin_mail.username if user.admin_mail else None
        mail_users = [commiter, treater, admin_mail]
        mail_list_extend = self.get_extend_mail_list(user)
        mail_list = [u.email for u in UserProfile.objects.filter(username__in=mail_users)]
        mail_list.extend(mail_list_extend)
        mail_list = list(set(mail_list))
        return mail_list

    def mail(self, instance, mail_type, personnel, source_app):
        try:
            mail_action = MailActions.objects.get(name=mail_type)
            mail_func = getattr(self, source_app)
            mail_func(instance, mail_action, personnel, source_app)
        except Exception as e:
            return e

    def mail_inception(self, instance, mail_action, personnel, source_app):
        if (instance.env == self.env_prd) and mail_action.value:
            mail_list = self.get_mail_list(instance)
            send_mail.delay(
                mail_list=mail_list,
                personnel=personnel.username,
                instance_id=instance.id,
                remark=instance.remark,
                sql_content=instance.sql_content,
                db_name=instance.db.name,
                status=instance.status,
                source_app=source_app,
                desc_cn=mail_action.desc_cn
            )

    def mail_db_order(self, instance, mail_action, personnel, source_app):
        mail_list = self.get_mail_list(instance)
        data_dict = copy.deepcopy(instance.__dict__)
        for field in ['_state', 'createtime', 'updatetime']:
            data_dict.pop(field)
        send_mail.delay(
            mail_list=mail_list,
            personnel=personnel.username,
            instance_id=instance.id,
            remark=instance.remark,
            status=instance.status,
            data_dict=data_dict,
            source_app=source_app,
            desc_cn=mail_action.desc_cn
        )

class Handle(ActionMixin):

    @timer
    def select(self, instance):
        sql_query = SqlQuery(instance.db)
        status, data = sql_query.get_select_result(instance.sql_content)
        instance.handle_result_execute = json.dumps([str(row) for row in data], cls=DateEncoder)
        instance.status = status
        return instance, len(data)

    @timer
    def execute(self, instance):
        affected_rows = 0
        opid_list = []
        instance.status = 0
        success_sql_num = 0
        success_sql_list, exception_sql_list, handle_result_execute = self.check_execute_sql(instance.db.id, instance.sql_content, self.action_type_execute)
        for success_sql in success_sql_list:
            affected_rows += success_sql[6]
            if re.findall(self.success_tag, success_sql[3]):
                success_sql_num += 1
                opid_list.append(success_sql[7].replace("'", ""))
        rollback_able = True if success_sql_num == len(success_sql_list) - 1 else False
        if exception_sql_list:
            instance.status = 2
            instance.execute_errors = exception_sql_list
        instance.rollback_db = success_sql[8]
        instance.rollback_opid = opid_list
        instance.rollback_able = rollback_able
        instance.handle_result_execute = handle_result_execute
        return instance, affected_rows

    @timer
    def rollback(self, instance):
        self.filter_select_type(instance)
        self.check_rollback_able(instance)
        db_instance = instance.db
        rollback_opid_list = instance.rollback_opid
        rollback_db = instance.rollback_db
        back_sql_list = ''
        for opid in eval(rollback_opid_list):
            back_source = 'select tablename from $_$Inception_backup_information$_$ where opid_time = "{}" '.format(opid)
            back_table = Inception(back_source, rollback_db).get_back_table()
            statement_sql = 'select rollback_statement from {} where opid_time = "{}" '.format(back_table, opid)
            rollback_statement = Inception(statement_sql, rollback_db).get_back_sql()
            if not rollback_statement:
                instance.status = 2
                instance.handle_result_rollback = json.dumps([self.get_rollback_fail])
                return instance, instance.affected_rows
            back_sql_list += rollback_statement
        db_conf = self.get_db_conf(db_instance.user, db_instance.password, db_instance.host, db_instance.port, self.action_type_execute)
        execute_results = Inception(back_sql_list, db_instance.name).inception_handle(db_conf).get('result')
        status = -3
        for result in execute_results:
            if result[4] != 'None':
                status = 2
                break
        instance.status = status
        instance.handle_result_rollback = json.dumps(execute_results)
        return instance, instance.affected_rows

class PermissionDatabases(object):

    def get_permission_databases(self, user):
        group = user.groups.first()
        user_perms = user.userobjectpermission_set.all()
        group_perms = group.groupobjectpermission_set.all() if group else []
        user_perms_set = set([perm.object_pk for perm in user_perms])
        group_perms_set = set([perm.object_pk for perm in group_perms])
        return user_perms_set | group_perms_set

    def filter_databases(self, db_list, user=None):
        user = user or self.request.user
        perm_dbs = self.get_permission_databases(user)
        return db_list.filter(pk__in=[int(pk) for pk in perm_dbs])

class OSC(object):

    @classmethod
    def get_osc_status(cls, handle_result_check):
        handle_result_check = json.loads(handle_result_check)
        status = False
        for i in handle_result_check:
            sha = i[-1]
            if sha:
                status = True
                break
        return status

    @classmethod
    def get_osc_sha(cls, instance):
        handle_result_check = json.loads(instance.handle_result_check)
        data = [{'sql':i[5], 'sha':i[-1]} for i in handle_result_check if i[-1]]
        return data


###dashbord

class HandleData(object):

    @property
    def get_user_info(self):
        user_instance = self.request.user
        user_info = dict()
        user_group = user_instance.groups.first()
        user_info['username'] = user_instance.username
        user_info['date_joined'] = user_instance.date_joined
        user_info['group'] = user_group.name if user_group else None
        user_info['identity'] = 'superuser' if user_instance.is_superuser else user_instance.role
        return user_info

    @property
    def get_count_data(self):
        count_data = dict()
        count_data['sql_total'] = self.queryset.count()
        count_data['sql_handled'] = self.queryset.filter(~Q(status=-1) & ~Q(status=-2)).count()
        count_data['user_total'] = self.serializer_user.Meta.model.objects.all().count()
        count_data['group_total'] = self.serializer_group.Meta.model.objects.all().count()
        return count_data

    @property
    def get_status_data(self):
        return self.queryset.values('status').annotate(num=Count('status')).order_by()

    @property
    def get_trend_data(self):
        date_range = range(14)
        date_list = []
        times_list = []
        for day in reversed(date_range):
            date_time = datetime.datetime.now() - datetime.timedelta(days=day)
            date = date_time.strftime("%Y-%m-%d")
            times = self.queryset.filter(createtime__startswith=date).count()
            date_list.append(date)
            times_list.append(times)
        return {'date_list':date_list, 'times_list':times_list}

    @property
    def get_today_data(self):
        date_time = datetime.datetime.now() - datetime.timedelta(days=0)
        date = date_time.strftime("%Y-%m-%d")
        qs_today = self.queryset.filter(createtime__startswith=date)
        return self.serializer_class(qs_today, many=True).data

    @property
    def get_type_data(self):
        index_list = Inception('desc inception.statistic').get_index_list()
        index_data = []
        for index in index_list:
            sql = 'SELECT `statistic`.`{}`, COUNT(`statistic`.`{}`) ' \
                  'AS `num` FROM `statistic` WHERE {} > 0 ' \
                  'GROUP BY `statistic`.`{}` ORDER BY NULL;'\
                .format(index, index, index, index)
            records = Inception(sql, 'inception').manual()
            total_execute_counts = 0
            total_execute_times = 0
            if records:
                for record in records:
                    total_execute_counts += record[0] * record[1]
                    total_execute_times += record[1]
            index_data.append(
                {
                    'index':index,
                    'total_execute_counts':total_execute_counts,
                    'total_execute_times':total_execute_times
                })
        return index_data

class RenderFile(object):
    path = settings.MEDIA.get('sql_file_path')

    def create_file(self, params, content):
        pk, sfx = params.get('pk'), params.get('sfx')
        file_name = '{}.{}'.format(pk, sfx)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        path = os.path.join(self.path, file_name)
        with open(path, 'w') as f:
            content_list = json.loads(content)
            length = len(content_list)
            if isinstance(content_list, list):
                for row in content_list:
                    f.write(str(row))
                    if content_list.index(row) < length - 1:
                        f.write('\n')
            else:
                f.write(content)
        return path, file_name

    def file_iterator(self, file_path, chunk_size=512):
        with open(file_path) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

class DownloadBaseView(PromptMixin, RenderFile, APIView):

    def check_content(self):
        content = self.get_content()
        if not content:
            raise ParseError(self.get_content_fail)
        return content

    def get(self, request, *args, **kwargs):
        content = self.check_content()
        file_path, file_name = self.create_file(kwargs, content)
        response = StreamingHttpResponse(self.file_iterator(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response

### media
class RenderFile(object):
    path = settings.MEDIA.get('sql_file_path')

    def create_file(self, params, content):
        pk, sfx = params.get('pk'), params.get('sfx')
        file_name = '{}.{}'.format(pk, sfx)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        path = os.path.join(self.path, file_name)
        with open(path, 'w') as f:
            content_list = json.loads(content)
            length = len(content_list)
            if isinstance(content_list, list):
                for row in content_list:
                    f.write(str(row))
                    if content_list.index(row) < length - 1:
                        f.write('\n')
            else:
                f.write(content)
        return path, file_name

    def file_iterator(self, file_path, chunk_size=512):
        with open(file_path) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

class DownloadBaseView(PromptMixin, RenderFile, APIView):

    def check_content(self):
        content = self.get_content()
        if not content:
            raise ParseError(self.get_content_fail)
        return content

    def get(self, request, *args, **kwargs):
        content = self.check_content()
        file_path, file_name = self.create_file(kwargs, content)
        response = StreamingHttpResponse(self.file_iterator(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
