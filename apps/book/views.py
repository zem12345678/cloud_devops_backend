from django.http import Http404
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions

from rest_framework import filters
# 第三方过滤器，高度可定制，DjangoFilterBackend 默认是精确（查找）过滤，即字段值必须要完全一样才能匹配成功
from django_filters.rest_framework import DjangoFilterBackend
# drf自带的分页
from rest_framework.pagination import PageNumberPagination
# jwt用户认证方式
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# drf自带的三种用户认证方式
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
# drf自带的权限管理方式
from rest_framework.permissions import IsAuthenticated
from rest_framework_extensions.cache.mixins import CacheResponseMixin,ListCacheResponseMixin,RetrieveCacheResponseMixin
from rest_framework_extensions.cache.decorators import cache_response
from .models import Book
from .models import Author
from .models import Publish
from .serializers import PublishSerializer
from .serializers import AuthorSerializer
from .serializers import BookSerializer
from .filters import PublishFilter, AuthorFilter, BookFilter

from commons.custom import RbacPermission



class PublishList(APIView):
    """
    GET: 获取publish 数据列表
    POST: 创建数据

    这两个方法有个共同的特点，不需要传入PK，故而共用一个url
    """
    @cache_response()
    def get(self, request, *args, **kwargs):
        queryset = Publish.objects.all()
        publish_list = PublishSerializer(queryset, many=True)
        # print(publish_list)
        # print(publish_list.data)
        # Response完成了JSONRander对数据json化的处理,等价于JSONRenderer().render(publish_list.data)。详见源码
        return Response(publish_list.data)

    def post(self, request, *args, **kwargs):
        # request.data完成了JSONParser反序列化处理
        print(request.data)
        publish = PublishSerializer(data=request.data)
        print(publish)
        if publish.is_valid():
            publish.save()
            return Response(publish.data,status=200)
        return Response(publish.data, status=400)

class PublishDetail(APIView):
    """
    GET: 获取单条数据
    PUT: 更新某一条数据
    DELETE: 删除某一条数据

    这三个方法都有一个共同的特点、就是必须先通过传过来的pk,获取这条记录，
    故而写到一起，共用同一个url。
    """
    # 自定义函数，通过url中的pk获取当前条数据
    def get_object(self, pk):
        try:
            return Publish.objects.get(pk=pk)
        except Publish.DoesNotExist:
            raise Http404

    @cache_response()
    def get(self,request,*args,**kwargs):
        print(kwargs.get("pk"))
        pk = kwargs.get("pk")
        publish = self.get_object(pk)
        serializer = PublishSerializer(publish)
        return Response(serializer.data)

    def put(self,request,*args,**kwargs):
        pk = kwargs.get("pk")
        publish = self.get_object(pk)
        serializer = PublishSerializer(publish, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.data, status=400)

    def delete(self,request,*args,**kwargs):
        pk = kwargs.get("pk")
        publish = self.get_object(pk)
        publish.delete()
        return Response(status=200)


# 第二个版本
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
class PublishGenericAPIView(GenericAPIView):
    queryset = Publish.objects.all()
    serializer_class = PublishSerializer
    keyword = ""
    # 用户认证（三种用户认证按顺序依次匹配）
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)


    # 重写get_queryset，实现列表页过滤
    def get_queryset(self):
        queryset = super(PublishGenericAPIView, self).get_queryset()
        print(queryset)
        self.keyword = self.request.GET.get('keyword', '').strip()
        print(self.keyword)
        if self.keyword:
            queryset = queryset.filter(name__icontains=self.keyword)
        return queryset

    @cache_response()
    def get(self, request, *args, **kwargs):
        # 群查
        pub_query = self.get_queryset()
        pub_ser = self.get_serializer(pub_query, many=True)
        return Response(pub_ser.data)

    def post(self, request, *args, **kwargs):
            publish = self.get_serializer(data=request.data)
            if publish.is_valid():
                publish.save()
                return Response(publish.data,status=200)
            return Response(publish.data, status=400)



class  PublishDetailGenericAPIView(GenericAPIView):
    queryset = Publish.objects.all()
    serializer_class = PublishSerializer
    # 权限判断,所有权限都满足才可以
    # pmission_classes = (IsAuthenticated)

    @cache_response()
    def get(self, request, *args, **kwargs):
        print(self.get_object())
        publish = self.get_object()
        serializer = self.get_serializer(publish)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        publish = self.get_object()
        serializer = self.get_serializer(publish, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.data, status=400)

    def delete(self,request,*args,**kwargs):
        publish = self.get_object()
        publish.delete()
        return Response(status=200)

# 第三个版本
from rest_framework import mixins
from rest_framework.generics import GenericAPIView

class PublishMixinGenericAPIView(ListCacheResponseMixin,mixins.ListModelMixin,
                                 mixins.CreateModelMixin,
                                 GenericAPIView):
    queryset = Publish.objects.all()
    serializer_class = PublishSerializer

    # 群查
    @cache_response()
    def get(self, request, *args, **kwargs):
        # list方法是继承mixins.ListModelMixin
        return self.list(request, *args, **kwargs)

    # 单增
    def post(self, request, *args, **kwargs):
        # create方法是继承mixins.CreateModelMixin
        return self.create(request, *args, **kwargs)


class PublishDetailMixinGenericAPIView(RetrieveCacheResponseMixin,mixins.RetrieveModelMixin,
                                       mixins.UpdateModelMixin,
                                       mixins.DestroyModelMixin,
                                       GenericAPIView):

    queryset = Publish.objects.all()
    serializer_class = PublishSerializer

    # 单查
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # 更新
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # 删除
    def delete(self, request, *args, **kwargs):
        return  self.destroy(request, *args, **kwargs)

# 第四个版本
from  rest_framework.generics import GenericAPIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView,UpdateAPIView,DestroyAPIView
# 上面五个类其实就完成了数据的增删改查，增删改查分为带PK和不带PK两类，索性下面两个方法就这个规则将五个类封装成两个，一次搞定
from  rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

class PublishMixinAPIView(ListCacheResponseMixin,ListCreateAPIView):
    """
    ListCreateAPIView = CreateAPIView+ListAPIView+GenericAPIView
    """
    queryset = Publish.objects.all()
    serializer_class = PublishSerializer

class PublishDetailMixinAPIView(RetrieveCacheResponseMixin,RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView = RetrieveAPIView+UpdateAPIView+DestroyAPIView+GenericAPIView
    """
    queryset = Publish.objects.all()
    serializer_class = PublishSerializer


# 第五个版本,增删改查合并为一个视图集
from rest_framework import viewsets
from rest_framework import mixins
class PublishViewSet(CacheResponseMixin,viewsets.ModelViewSet):
# class PublishViewSet(viewsets.GenericViewSet,
#                      mixins.CreateModelMixin,
#                      mixins.ListModelMixin,
#                      mixins.UpdateModelMixin,
#                      mixins.RetrieveModelMixin,
#                      mixins.DestroyModelMixin):

    """
    viewsets.ModelViewSet 和 上面一大窜等价。ModelViewSet包含了增删改查所有操作。
    实际工作中，并不是每个操作都是完整的增删改查，往往按需加载对应增删改查的五大类和对应
    的六大函数即可，六大函数都可以按需重写
    """

    queryset = Publish.objects.all()
    serializer_class = PublishSerializer


# 第六个版本viewset＋router,优化URL
from rest_framework import viewsets

class PublishViewSets(CacheResponseMixin,viewsets.ModelViewSet):
    queryset = Publish.objects.all()
    serializer_class = PublishSerializer


# 序列化进阶 ModelSerializer+关系表
class AuthorViewSets(CacheResponseMixin,viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSets(CacheResponseMixin,viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



class Pagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100



class PublishViewSet(CacheResponseMixin,viewsets.ModelViewSet):
    """
    list:
      列出所有出版商
    retrieve:
      某个出版商的详细信息
    create:
      创建出版商
    update:
      更新出版商
    delete:
      删除出版商
    """

    # 用户认证及权限验证（四种用户模式按顺序依次匹配）
    authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication,
                            BasicAuthentication)
    permission_classes = (RbacPermission,IsAuthenticated,)

    # 查询结果集
    queryset = Publish.objects.all()
    # 调用序列化类
    serializer_class = PublishSerializer
    # 调用分页类
    pagination_class = Pagination
    # 定义过滤器
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 调用过滤类
    filter_class = PublishFilter
    search_fields = ('name', 'city')
    ordering_fields = ('name',)

class AuthorViewSet(CacheResponseMixin,viewsets.ModelViewSet):
    """
    list:
      列出所有作者信息
    retrieve:
      某个作者的详细信息
    create:
      创建作者
    update:
      更新作者
    delete:
      删除作者
    """

    # 用户认证及权限验证
    authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication,
                             BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = AuthorFilter
    search_fields = ('name', 'email')
    ordering_fields = ('name',)

class BookViewSet(CacheResponseMixin,viewsets.ModelViewSet):
    """
    list:
      列出所有图书信息
    retrieve:
      某个图书的详细信息
    create:
      创建图书
    update:
      更新图书
    delete:
      删除图书
    """

    # 用户认证及权限验证
    authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication,
                             BasicAuthentication)
    permission_classes = (IsAuthenticated, permissions.DjangoModelPermissions)

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = Pagination
    # filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter类和search类都可以实现模糊查询， filter的特点是可以支持区间查询，search不可以
    filter_class = BookFilter
    # 关联表道的搜索格式： 关联列名__关联表字段
    search_fields = ('name', 'publisher__name', 'authors__name')
    ordering_fields = ('publication_date',)



