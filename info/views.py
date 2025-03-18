from django.shortcuts import render
import uuid
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from info import models
from .models import Language, Project

from chatmessage.models import  summaryAnswerStorage
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


class NewsInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class NewsInformationView(APIView):
    authentication_classes = []
    # 这个是将所有的领域的信息来进行返回
    def get(self, request, *args, **kwargs):
        data = models.Language.objects.all()
        serializer = NewsInformationSerializer(data, many=True)
        return Response({"code": 200, "message": "获取新闻列表成功", "data": serializer.data})


class NewsDetailSerializer(serializers.ModelSerializer):
    LANGUAGE_CHOICES = {
        1:"心理科普",
        2:"婚恋情感",
        3:"家庭关系",
        4:"人际社交",
        5:"自我觉察",
        6:"成长学习",
        7:"心理健康",
        8:"职场技能",
    }
    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, instance):
        navLeftItems = [
            {"id": lang_id, "data": {"title": lang_title}} for lang_id, lang_title in self.LANGUAGE_CHOICES.items()
        ]
        project_data_list = list(Project.objects.all().values())
        navRightItems = self.group_data_by_language(project_data_list)
        result = {
            "navLeftItems": navLeftItems,
            "navRightItems": navRightItems
        }
        return result  # 返回包含 navLeftItems 和 navRightItems 的单个对象

    def group_data_by_language(self, data_list):
        grouped_data = {}
        for data in data_list:
            News = data['News']
            if News in grouped_data:
                grouped_data[News].append(data)
            else:
                grouped_data[News] = [data]
        return list(grouped_data.values())
class NewsDetailView(APIView):
    authentication_classes = []
    # 某个领域内的获奖的状况来进行展示
    def get(self, request, *args, **kwargs):
        data = Project.objects.all()
        serializer = NewsDetailSerializer(data, many=True)
        return Response({"code": 200, "message": "获取数据成功", "data": serializer.data[0]})

class PsychometricDetailSerializer(serializers.ModelSerializer):
    ReturnTime = serializers.DateTimeField(format="%Y-%m-%d")
    class Meta:
        model = summaryAnswerStorage
        fields = ['TopicSummary','HealthScore','ReturnTime','Memo']


class GetPsychometricsView(APIView):
    authentication_classes = []
    # 进行心理测评的展示信息
    def get(self, request, *args, **kwargs):
        data = summaryAnswerStorage.objects.all()
        serializer = PsychometricDetailSerializer(data, many=True)
        return Response({"code": 200, "message": "获取数据成功", "data": serializer.data})

