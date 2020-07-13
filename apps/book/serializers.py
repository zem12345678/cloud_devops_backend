from rest_framework.renderers import JSONRenderer
from rest_framework import serializers
from .models import Publish, Author, Book


# class PublishSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=30, required=True, help_text="出版商名")
#     city = serializers.CharField(max_length=60, required=False, help_text="出版商城市")
#     address = serializers.CharField(max_length=60,required=True, help_text="出版商地址")
#
#     # 接受POST请求的数据，验证之后入库
#     def create(self, validated_data):
#         print(validated_data)
#         print("2222")
#         return Publish.objects.create(**validated_data)
#
#     # 接受PUT请求的数据，验证之后入库
#     def update(self, instance, validated_data):
#         print("2222")
#         print(instance)
#         print(validated_data)
#         instance.name = validated_data["name"]
#         instance.city = validated_data["city"]
#         instance.address = validated_data["address"]
#         instance.save()
#         return instance


class PublishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publish
        fields = "__all__"


    # # 接受POST请求的数据，验证之后入库
    # def create(self, validated_data):
    #     print(validated_data)
    #     print("2222")
    #     return self.Meta.model.objects.create(**validated_data)

    # # 接受PUT请求的数据，验证之后入库
    # def update(self, instance, validated_data):
    #     print("2222")
    #     print(instance)
    #     print(validated_data)
    #     instance.name = validated_data["name"]
    #     instance.city = validated_data["city"]
    #     instance.address = validated_data["address"]
    #     instance.save()
    #     return instance



# 引入ModelSerializer
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


# 版本一： Serializer序列化反序列化嵌套关系表
# class BookSerializer(serializers.Serializer):
#     publisher = PublishSerializer(many=False)         # 一对多，默认显示PublishSerializer定义的所有列
#     authors = AuthorSerializer(many=True)   # 多对多，默认显示AuthorSerializer定义所有的列
#     publication_date = serializers.DateField(format="%Y-%m-%d")   # 后端格式化序列化输出的日期
#
#     name = serializers.CharField(max_length=100, required=True, help_text="书名")
#     # 作者和书是多对多的关系
#     authors = authors
#     # 一本书只能被一家出版，出版商可以出版多本书
#     publisher = publisher
#     publication_date = publication_date
#     # publication_date = serializers.DateField(required=False, help_text="出版日前")
#
#     def create(self, validated_data):
#         print(validated_data)
#         print("2222")
#         #return Book.objects.create(**validated_data)
#
#         # 管理数据需要一个个拉出来处理
#         author_list = validated_data.pop('authors', [])
#         publisher = validated_data.pop('publisher',"")
#         print(publisher)
#         print(dict(publisher))
#         p = Publish.objects.get(name=dict(publisher)['name'])
#         print(p)
#         validated_data['publisher']=p
#         print(validated_data)
#         instance = Book.objects.create(**validated_data)
#         print("222")
#         print(author_list)
#         authors = []
#         for author in author_list:
#             print(dict(author))
#             author = Author.objects.get(name=dict(author)['name'])
#             authors.append(author)
#         # author和book是多对多关系，添加数据时需要单独处理
#         print(authors)
#         instance.authors.add(*authors)
#         return instance
#
#     def update(self, instance, validated_data):
#         print(validated_data)
#         author_list = validated_data.pop('authors', [])
#         publisher = validated_data.pop('publisher', "")
#         p = Publish.objects.get(name=dict(publisher)['name'])
#         validated_data['publisher'] = p
#         Book.objects.filter(id=instance.id).update(**validated_data)
#         authors = []
#         for author in author_list:
#             author = Author.objects.get(name=dict(author)['name'])
#             authors.append(author)
#         # 多对多添加的两种写法,add是追加，set是覆盖重置
#         instance.authors.set(authors)
#         return instance



# 版本二： ModelSerializer序列化反序列化嵌套关系表
# class BookSerializer(serializers.ModelSerializer):
#     publisher = PublishSerializer(many=False)
#     authors = AuthorSerializer(many=True)
#     publication_date = serializers.DateField(format="%Y-%m-%d")
#
#     class Meta:
#         model = Book
#         #fields = ('name', 'publisher', 'authors','publication_date')
#         fields = "__all__"


    # 默认情况下，嵌套序列化类是只读的。如果要支持对嵌套序列化字段的写操作，
    # 则需要创建 create() 和/或 update() 方法，以明确指定应如何保存子关系。
    # # 本例中创建图书的对应初步商的逻辑：只能选择已经存在的出版商和作者，如果没有则提前单独创建好
    # def create(self, validated_data):
    #     author_list = validated_data.pop('authors', [])
    #     publisher = validated_data.pop('publisher',"")
    #     p = Publish.objects.get(name=dict(publisher)['name'])
    #     validated_data['publisher']=p
    #     instance = Book.objects.create(**validated_data)
    #     authors = []
    #     for author in author_list:
    #         author = Author.objects.get(name=dict(author)['name'])
    #         authors.append(author)
    #     # author和book是多对多关系，添加数据时需要单独处理
    #     instance.authors.add(*authors)
    #     return instance
    #
    # def update(self, instance, validated_data):
    #     author_list = validated_data.pop('authors', [])
    #     publisher = validated_data.pop('publisher', "")
    #     p = Publish.objects.get(name=dict(publisher)['name'])
    #     validated_data['publisher'] = p
    #     Book.objects.filter(id=instance.id).update(**validated_data)
    #     authors = []
    #     for author in author_list:
    #         author = Author.objects.get(name=dict(author)['name'])
    #         authors.append(author)
    #     # 多对多添加的两种写法,add是追加，set是覆盖重置
    #     instance.authors.set(authors)
    #     return instance



# 版本三：ModelSerializer+自定义序列化反序列化嵌套关系表
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    def author(self, author_queryset):
        ret = []
        # 多对多的结果是一个列表对象，需要遍历对象，将需要序列化的内容提出来即可
        for author in author_queryset:
            ret.append({
                'id': author.id,
                'name': author.name,
                'email': author.email
            })
        return ret

    # 重写to_representation方法，定义关系表中要序列化输出的列，默认只输出关系表对应列的ID
    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        将从 Model 取出的数据 parse 给 Api
        """
        # 一对多关系，相当于一对多的正向查询。获取当前书的出版商，SQL：Book.objects.get(pk=1).publisher
        publisher_obj = instance.publisher
        # 对对多，相当于多对多的正向查询。获取当前书的作者，SQL：Book.objects.get(pk=1).authors.all()
        authors_obj = self.author(instance.authors.all())

        # 将书的相关信息序列化，即将Book.objects.all()的querydict结果集合转为JSON
        ret = super(BookSerializer, self).to_representation(instance)
        print(ret)

        # 将关联表需要序列化输出的列处理为json,也加入序列化大字典中。这样就能序列化出当前表和关联表所有想展示的字段了
        ret["publisher"] = {
            "id": publisher_obj.id,
            "name": publisher_obj.name,
            "address": publisher_obj.address
        },
        ret["authors"] = authors_obj
        print("1111")
        print(ret)
        return ret

    # def to_internal_value(self, data):
    #     """
    #     Dict of native values <- Dict of primitive datatypes.
    #     将客户端传来的 json 数据 parse 给 Model,并将数据model化
    #     对于关系型号数据，必须填写期望为主键，即ID,这种场景特别适合前后端分离项目，传入类型如下格式：
    #     {
    #         "name": "python",
    #         "publication_date":  "2019-11-11",
    #         "publisher": 3,
    #         "authors": [2,3]
    #     }
    #
    #     """
    #     print("111")
    #     print(data)        # {'name': 'python', 'publication_date': '2019-11-11', 'publisher': 3, 'authors': [2, 3]}
    #     print(type(data))  # <class 'dict'>
    #     return super(BookSerializer, self).to_internal_value(data)

    # # 重写create方法，源码中已经对单表、一对多、多对多对关系做了处理，此次为了学习调试方便重写
    # def create(self, validated_data):
    #     # {'name': '平凡的世界', 'publication_date': datetime.date(2018, 5, 10),
    #     # 'publisher': <Publish: Publish object>, 'authors': [<Author: Author object>]}
    #     print(validated_data)
    #     print("2222")
    #     author_list = validated_data.pop('authors', [])
    #     print(validated_data)
    #     print(author_list)
    #     instance = self.Meta.model.objects.create(**validated_data)
    #     # author和book是多对多关系，添加数据时需要单独处理
    #     instance.authors.add(*author_list)
    #     return instance
    # #
    # # # 源码中已经对单表、一对多、多对多对关系做了处理，此次为了学习调试方便重写
    # def update(self, instance, validated_data):
    #     print(validated_data)
    #     author_list = validated_data.pop('authors', [])
    #     self.Meta.model.objects.filter(id=instance.id).update(**validated_data)
    #     # 多对多添加的两种写法,add是追加，set是覆盖重置
    #     instance.authors.set(author_list)
    #     instance.authors.add(*author_list)
    #     return instance


