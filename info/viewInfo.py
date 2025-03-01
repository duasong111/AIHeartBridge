from django.shortcuts import render
import  uuid
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from info import models
from rest_framework import exceptions
# Create your views here.


class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.userInfo
        fields = ["Name","Account", "PassWord"]
class LoginView(APIView):
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