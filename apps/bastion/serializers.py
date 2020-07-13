from rest_framework import serializers
from apps.bastion import  models
import requests
import json
from django.conf import settings

class AccountSerializer(serializers.ModelSerializer):

    def create(self,validated_data):
        url = "http://127.0.0.1:8080/account_create"
        username = validated_data.get("username")
        account_json = requests.post(url,json.dumps({"username":username}))
        if account_json.status_code >= 300:
            raise Exception
        return models.Account.objects.get(username=username)


    class Meta:
        model = models.Account
        fields = (
                "id",
                "username"
            )





class GroupsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Groups
        fields = "__all__"



class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Permisssion
        fields = (
                "id",
                "hostname",
                "username",
                "appendgroups"
            )



class AuditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Auditor
        fields = "__all__"