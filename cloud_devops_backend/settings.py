"""
Django settings for cloud_devops_backend project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys
import datetime
from past.builtins import execfile
from mongoengine import connect
import djcelery
from celery import platforms
from celery.schedules import crontab
from kombu import Queue
from kombu import Exchange
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(1, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!ck-4t*50y+yz=b(xew^ubsh=m-&s*n=3m2=19!kw4j4wk4th='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DOMAIN = "zhangenmin888@gmail.com"

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'django_apscheduler',
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',
    'djcelery',
    'import_export',
    'simple_history',
    'haystack',
    'channels',
    'graphene_django',
    'rest_framework_swagger',
    'social_django',
    'raven.contrib.django.raven_compat',
    'xadmin',
    'crispy_forms',
    'reversion',
    'DjangoUeditor',
    'rbac',
    'cmdb',
    'deployment',
    'book',
    'workorder',
    'sqlmng',
    'resources',
    'zabbix',
    'clouds',
    'salt',
    'release',
    'servicetree',
    'task',
    'autotask',
    'workflow'
]

GRAPHENE = {
    'SCHEMA': 'cloud_devops_backend.schema.schema'
}


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',#跨域
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware', #操作记录

]

# CORS跨域设置
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = (           #白名单
    'http://localhost:5000',
    'http://localhost:8000',
    'http://localhost:8080',
)

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

ROOT_URLCONF = 'cloud_devops_backend.urls'

APPEND_SLASH = False

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cloud_devops_backend.wsgi.application'
# 配置ASGI
ASGI_APPLICATION = "cloud_devops_backend.routing.application"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cloud_devops',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': '123456',
        'PORT': '3307',
        'OPTIONS': { 'init_command': 'SET default_storage_engine=INNODB;' }
    },
    "zabbix": {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zabbix',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3307',
        'OPTIONS': {
            'init_command': "SET default_storage_engine=INNODB;SET sql_mode='STRICT_TRANS_TABLES'"
        }
    },
    'container': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'container',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3307',
        'OPTIONS': {
            'init_command': "SET default_storage_engine=INNODB;SET sql_mode='STRICT_TRANS_TABLES'"
        },
    'test': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    },
    # 'container': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'container',
    #     'USER': 'root',
    #     'PASSWORD': '123456',
    #     'HOST': '127.0.0.1',
    #     'PORT': '5432',
    #     'ATOMIC_REQUESTS': True,
    # },

}

DATABASE_ROUTERS = ['cloud_devops_backend.database_router.DatabaseAppsRouter']
DATABASE_APPS_MAPPING = {
    # 'default': 'default',
    'admin':'default',
    'xadmin':'default',
    'sessions':'default',
    'contenttypes':'default',
    'django_apscheduler':'default',
    'otp_static':'default',
    'otp_totp':'default',
    'two_factor':'default',
    'djcelery':'default',
    'social_django':'default',
    'auth':'default',
    'book':'default',
    'rbac':'default',
    'cmdb':'default',
    'clouds':'default',
    'deployment':'default',
    'resources':'default',
    'workorder':'default',
    'sqlmng':'default',
    'release':'default',
    'autotask':'default',
    'salt':'default',
    'servicetree':'default',
    'task':'default',
    'zabbix':'zabbix',
    'k8s':'container',
    'workflow':'default',
    'test':'test'

}


connect('elk', host='127.0.0.1', port=21017, username='root',password='VgOK8WctTOEtM2')

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ("django_filters.rest_framework.DjangoFilterBackend",),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',#
        'rest_framework.authentication.SessionAuthentication',#
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    # 自定义异常处理
    'EXCEPTION_HANDLER': 'commons.custom.ops_exception_handler',
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '100/day',
    #     'user': '10000/day'
    # },

}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "VgOK8WctTOEtM2"
        },
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "VgOK8WctTOEtM2"
        }
    },
    "scheduler": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/10",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "VgOK8WctTOEtM2"
        }
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

ACCCESSKEYID = os.environ.get("ACCCESSKEYID", '')
ACCESSSECRET = os.environ.get("ACCESSSECRET", '')

# redis 设置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 8
REDIS_PASSWORD = 'VgOK8WctTOEtM2'

# zabbix 设置
ZABBIX_API = "http://192.168.1.132/zabbix/"
ZABBIX_ADMIN_USER = "Admin"
ZABBIX_ADMIN_PASS = "zabbix"
ZABBIX_DEFAULT_HOSTGROUP = "2"

# salt_api 设置
SALT_URL = 'https://192.168.222.132:8100'
SALT_USER = 'saltapi'
SALT_PASSWORD = 'saltapi'

# 需要过滤掉的网卡设备名
FILTER_NETWORK_DEVICE = ["docker", "veth", "tun", "sit", "br"]

# django-channels配置
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": ["redis://:{}@{}:{}/{}".format(REDIS_PASSWORD,REDIS_HOST,REDIS_PORT,REDIS_DB)],
        },
    },
}

# 配置Haystack搜索引擎后端
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        # 端口号固定为9200
        'URL': 'http://127.0.0.1:9200/',
        # 指定elasticsearch建立的索引库的名称
        'INDEX_NAME': 'cloud_devops',
        'TIME_OUT':60,
    },
}
# 当添加、修改、删除数据时，自动生成索引  es自动重建索引
# 保证了在Django运行起来后，有新的数据产生时，haystack仍然可以让Elasticsearch实时生成新数据的索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

AUTH_USER_MODEL = 'rbac.UserProfile'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# swagger login/out
LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'

#yml配置文件存放的目录
YML_CONF_DIR = os.path.join(BASE_DIR, 'conf')

# 部署管理工作区地址
WORKSPACE = '/tmp/workspace/'

## 钉钉 报警机器人 地址  调用地方为 system.tasks.ding_ding_to_info
web_hook_url = ""

# 手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"

# 缓存过期时间
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 15
}

djcelery.setup_loader()
BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672/my_vhost'
CELERY_RESULT_BACKEND = 'redis://:{}@127.0.0.1:6379/1'.format(REDIS_PASSWORD) # BACKEND配置，这里使用redis
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler' # 定时任务
CELERYCELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERYD_CONCURRENCY = 8                                          # 并发worker数
CELERY_TIMEZONE = TIME_ZONE
CELERYD_FORCE_EXECV = True                                       # 非常重要,有些情况下可以防止死锁
CELERYD_MAX_TASKS_PER_CHILD = 100    # 每个worker最多执行100个任务就会被销毁，可防止内存泄露
CELERY_DISABLE_RATE_LIMITS = True    # 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行
CELERYD_TASK_TIME_LIMIT = 15 * 60 # 任务超时时间
CELERY_ACKS_LATE = True
# 设置默认不存结果
# CELERY_IGNORE_RESULT = True
CELERY_CREATE_MISSING_QUEUES = True
CELERYD_TASK_SOFT_TIME_LIMIT = 900
CELERY_TASK_RESULT_EXPIRES = 86400
CELERY_ENABLE_UTC = True
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_QUEUES = (
    Queue('low', Exchange('low', type='direct')),
    Queue('high', Exchange('high', type='direct')),
)

class MyRouter(object):
    def route_for_task(self, task, args=None, kwargs=None):

        if task.startswith('deploy'):
            return {
                'queue': 'high',
            }
        else:
            return {'queue': 'low'}


CELERY_ROUTES = (MyRouter(),)

# 定时任务
CELERYBEAT_SCHEDULE = {
    'minion_status_task': {
        'task': 'salt.tasks.minion_status',
        # 'schedule': crontab(minute=u'40', hour=u'17',),
        'schedule': timedelta(seconds=60),
        'args': (),
        'options': {
            'queue': 'low',  # 指定要使用的队列
        }
    }
}


## K8S
Token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLTVreHZoIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiJmN2I0NWI3Zi03ZGFhLTQ0YjktYTgwMi1iMTRjMzFjODRlYzAiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZXJuZXRlcy1kYXNoYm9hcmQ6YWRtaW4tdXNlciJ9.mEOC6RqNyriOnnrt2D7aePzvDXkUj0SqlneHVJe8fss_VD06t9bm7Z9kSkoPXulOIzXetfRl6hhlplZDxkleyha1Gw1X1HIP3gDmOX6paOhgQfK5o6uEYsk3i42sIyRAWCdpIRnkdXCLJgv13IyLQgYF_eRgjznNpPr-IKDKAM8dc53vMh1L6r0Mf-rVschuSP71fwaczMVLHN09LZpjCja836aSYqgsG6Xp9uwxtgM78-BbiGt2fKEVqPqb3oDHCrV-jxi70r4b-kYJE5zq_2VT832u-E4vSTeb89ciuqxcCVza6CfdTN-dN8u3ZN1yFXuvmgIEklh_hcSuPquYXQ"
APISERVER = 'https://192.168.222.128:6443'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.exmail.qq.com"
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = "1586346727@qq.com"
EMAIL_HOST_PASSWORD = "zem@12345678"
EMAIL_FROM = "标题<1586346727@qq.com>"


GITLAB_HTTP_URI = "http://127.0.0.1/"
GITLAB_TOKEN = "G_kTyBbvWmWMBnsyE-9J"

JENKINS_URL = "http://127.0.0.1:8088/"
JENINS_TOKEN = "4dfcb7e9423a1c8733cddd595ddd9142"
JENKINS_USERNAME = 'admin'
JENKINS_PASSWORD = 'zem@12345678'


# 支付宝相关的key路径
private_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/private_2048.txt')
ali_pub_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/alipay_key_2048.txt')

# 第三方登录相关
SOCIAL_AUTH_WEIBO_KEY = 'foobar'
SOCIAL_AUTH_WEIBO_SECRET = 'bazqux'

SOCIAL_AUTH_QQ_KEY = 'foobar'
SOCIAL_AUTH_QQ_SECRET = 'bazqux'

SOCIAL_AUTH_WEIXIN_KEY = 'foobar'
SOCIAL_AUTH_WEIXIN_SECRET = 'bazqux'

# sentry设置
# import os
# import raven
#
# RAVEN_CONFIG = {
#     'dsn': 'https://<key>:<secret>@sentry.io/<project>',
# }
# X_FRAME_OPTIONS = 'sameorigin'
# REMOTE_DEBUG = False
# PROJECT_ROOT = os.path.join(BASE_DIR, 'cloud_devops_backend')
# if DEBUG and REMOTE_DEBUG:
#     try:
#         execfile(os.path.join(PROJECT_ROOT, 'dev_settings.py'))
#     except IOError:
#         pass
# elif DEBUG:
#     try:
#         execfile(os.path.join(PROJECT_ROOT, 'local_settings.py'))
#     except IOError:
#         pass
# else:
#     try:
#         execfile(os.path.join(PROJECT_ROOT, 'dev_settings.py'))
#     except IOError:
#         pass

#jwt setting
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=3),
    'JWT_AUTH_HEADER_PREFIX': 'jwt',
    # 'JWT_ENCODE_HANDLER':
    #     'rest_framework_jwt.utils.jwt_encode_handler',
    #
    # 'JWT_DECODE_HANDLER':
    #     'rest_framework_jwt.utils.jwt_decode_handler',
    #
    # 'JWT_PAYLOAD_HANDLER':
    #     'rest_framework_jwt.utils.jwt_payload_handler',
    #
    # 'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    #     'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
    #
    # 'JWT_RESPONSE_PAYLOAD_HANDLER':
    #     'rest_framework_jwt.utils.jwt_response_payload_handler',
    #
    # 'JWT_SECRET_KEY': settings.SECRET_KEY,
    # 'JWT_PUBLIC_KEY': None,
    # 'JWT_PRIVATE_KEY': None,
    # 'JWT_ALGORITHM': 'HS256',
    # 'JWT_VERIFY': True,
    # 'JWT_VERIFY_EXPIRATION': True,
    # 'JWT_LEEWAY': 0,
    # 'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
    # 'JWT_AUDIENCE': None,
    # 'JWT_ISSUER': None,
    #
    # 'JWT_ALLOW_REFRESH': True,
    # 'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    # 'JWT_AUTH_HEADER_PREFIX': 'JWT',
}


SWAGGER_SETTINGS = {
    # 基础样式
    # 'SECURITY_DEFINITIONS': {
    #     "basic": {
    #         'type': 'basic'
    #     }
    # },
    'USE_SESSION_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'authorization'
        }
    },
    # 如果需要登录才能够查看接口文档, 登录的链接使用restframework自带的.
    # 'LOGIN_URL': '/api/v1/login/',
    # 'LOGOUT_URL': 'rest_framework:logout',
    # 'DOC_EXPANSION': None,
    # 'SHOW_REQUEST_HEADERS':True,
    # 'USE_SESSION_AUTH': True,
    # 'DOC_EXPANSION': 'list',
    # 接口文档中方法列表以首字母升序排列
    'APIS_SORTER': 'alpha',
    # 如果支持json提交, 则接口文档中包含json输入框
    'JSON_EDITOR': True,
    # 方法列表字母排序
    'OPERATIONS_SORTER': 'alpha',
    'VALIDATOR_URL': None,
}

# 日志
BASE_LOG_DIR = os.path.join(BASE_DIR, 'logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s][%(levelname)s]''[%(filename)s:%(lineno)d][%(message)s]'
        },
        'simple': {
            'format': '[%(levelname)s][%(asctime)s]%(message)s'
        },

    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_LOG_DIR, "info_xops.log"),
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 3,
            'formatter': 'simple',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_LOG_DIR, "err_xops.log"),
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        }

    },
        'loggers': {
            'info': {
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': True,
            },
            'warn':{
                'handlers': ['default'],
                'level': 'WARNING',
                'propagate': True,
            },
            'error': {
                'handlers': ['error'],
                'level': 'ERROR',
            }
    }

}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {'format': '%(asctime)s %(levelname)s %(message)s'},
#         'simple': {'format': '%(levelname)s %(message)s'},
#         'default': {
#             'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s] - %(message)s',
#             'datefmt': '%Y-%m-%d %H:%M:%S'
#         }
#     },
#     'handlers': {
#         'null': {
#             'level':'DEBUG',
#             'class':'logging.NullHandler',
#         },
#         'sentry': {
#             'level': 'ERROR',
#             'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
#             'tags': {'custom-tag': 'x'},
#         },
#         'console':{
#             'level':'DEBUG',
#             'class':'logging.StreamHandler',
#             'formatter': 'default'
#         },
#         'django':{
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
#             'formatter': 'default'
#
#         },
#         'root_handler': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'formatter': 'default',
#             'filename': os.path.join(BASE_DIR, 'logs', 'server.log'),
#             'when': 'D',
#             'interval': 1,
#             'encoding': 'utf8',
#         },
#         'django_request_handler':{
#             'level': 'DEBUG',
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'formatter': 'default',
#             'filename': os.path.join(BASE_DIR, 'logs', 'request.log'),
#             'when': 'D',
#             'interval': 7,
#             'encoding': 'utf8',
#         },
#         'django_db_backends_handler':{
#             'level': 'DEBUG',
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'formatter': 'verbose',
#             'filename': os.path.join(BASE_DIR, 'logs', 'db_backends.log'),
#             'when': 'D',
#             'interval': 7,
#         }
#     },
#     'loggers' : {
#         'django': {
#             'level': 'DEBUG',
#             'handlers': ['django'],
#             'propagate': False
#         },
#         'django.request': {
#             'handlers': ['django_request_handler'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#         'django.db.backends':{
#             'handlers': ['django_db_backends_handler'],
#             'level': 'DEBUG',
#             'propagate': False,
#         }
#     },
#     'root':{
#         'level': 'DEBUG',
#         'handlers': ['root_handler']
#     }
# }

SIMPLEUI_HOME_TITLE = '百度一下你就知道'
