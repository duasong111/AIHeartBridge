from django.shortcuts import render
import uuid
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from info import models
from rest_framework import exceptions


# Create your views here.



class RegisterSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = models.userInfo
        fields = ["id", "Name", "PassWord", "confirm_password","Age"]
        extra_kwargs = {
            "id": {"read_only": True},
            "PassWord": {"write_only": True}
        }
    def validate_password(self, value):
        return value

    def validate_confirm_password(self, value):
        password = self.initial_data.get("PassWord")
        if password != value:
            raise exceptions.ValidationError("密码不一样")
        return value


# 用户注册功能
class registerView(APIView):
    def post(self, request):
        ser = RegisterSerializers(data=request.data)
        if ser.is_valid():
            ser.validated_data.pop("confirm_password")
            ser.save()
            return Response({"code": 200, "message": "成功", "data": ser.data})
        else:
            return Response({"code": 1000, "errors": "注册失败", "data": ser.errors})


class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.userInfo
        fields = ["Name", "Account", "PassWord"]


class loginView(APIView):
    def post(self, request):

        ser = LoginSerializers(data=request.data)
        if not ser.is_valid():
            return Response({"code": 1001, "error": "校验失败", "detail": ser.errors})

        instance = models.userInfo.objects.filter(**ser.validated_data).first()
        if not instance:
            return Response({"code": 1001, "error": "用户名或密码错误"})

        token = str(uuid.uuid4())
        instance.token = token
        instance.save()
        return Response({"code": 200, "message": "登录成功", "token": token})
