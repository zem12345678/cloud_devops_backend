import django_filters
from .models import Publish, Author, Book             


class PublishFilter(django_filters.rest_framework.FilterSet):
    """
    过滤类
    """
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    city = django_filters.CharFilter(field_name="city", lookup_expr="icontains")

    class Meta:
        model = Publish
        fields = ['name', 'city']


class AuthorFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")

    class Meta:
        model = Author
        fields = ['name', 'email']


# 关联表道的搜索格式： 关联列名__关联表字段
class BookFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    publisher = django_filters.CharFilter(field_name="publisher__name", lookup_expr="icontains")
    authors = django_filters.CharFilter(field_name="authors__name", lookup_expr="icontains")
    start_date = django_filters.DateFilter(field_name="publication_date", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="publication_date", lookup_expr="lte")

    class Meta:
        model = Book
        fields = ['name', 'authors', 'publisher','start_date','end_date']

