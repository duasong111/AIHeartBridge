from django.shortcuts import render
import uuid
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from info import models
from rest_framework import status
from rest_framework import exceptions


# Create your views here.
class RegisterSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = models.userInfo
        fields = ["Name","Account", "PassWord", "confirm_password"]
        extra_kwargs = {
            "id": {"read_only": True},
            "PassWord": {"write_only": True}
        }

    def validate(self, attrs):
        # 在 validate 方法中统一验证
        if attrs["PassWord"] != attrs["confirm_password"]:
            raise exceptions.ValidationError({"confirm_password": "密码和确认密码不一致"})
        # 可选：检查账户是否已存在
        if models.userInfo.objects.filter(Account=attrs["Account"]).exists():
            raise exceptions.ValidationError({"Account": "该账户已存在"})
        if models.userInfo.objects.filter(Name=attrs["Name"]).exists():
            raise exceptions.ValidationError({"Name": "用户名已存在"})
        return attrs

    def create(self, validated_data):
        # 移除 confirm_password 并创建用户
        validated_data.pop("confirm_password")
        return models.userInfo.objects.create(**validated_data)


# 用户注册功能
class RegisterView(APIView):
    def post(self, request):
        print("Request data:", request.data)
        ser = RegisterSerializers(data=request.data)
        if ser.is_valid():
            user = ser.save()  # 调用 save 并获取创建的对象
            return Response({
                "code": 200,
                "message": "注册成功",
                "data": {
                    "Name":user.Name,
                    "Account": user.Account}  # 只返回必要数据
            }, status=status.HTTP_201_CREATED)
        print("Errors:", ser.errors)  # 调试错误
        return Response({
            "code": 1000,
            "message": "注册失败",
            "data": ser.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.userInfo
        fields = ["Account", "PassWord"]        #则要求必须输入的检验数据


class LoginView(APIView):
    def post(self, request):

        ser = LoginSerializers(data=request.data)
        if not ser.is_valid():
            return Response({"code": 1001, "error": "校验失败", "detail": ser.errors})

        instance = models.userInfo.objects.filter(**ser.validated_data).first()
        if not instance:
            return Response({"code": 1001, "error": "用户名或密码错误"})

        token = str(uuid.uuid4())
        instance.Token = token
        instance.save()
        return Response({"code": 200, "message": "登录成功", "token": token})
