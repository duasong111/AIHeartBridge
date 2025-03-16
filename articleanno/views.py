import base64
from rest_framework.views import APIView
from .models import Notices, About,News
from rest_framework.response import Response
from rest_framework import serializers
# from pytz import timezone
from django.shortcuts import render,redirect,HttpResponse
# cst_tz = timezone('Asia/Shanghai')


# 来对那数据库的内容进行格式化的显示
class GetNoticeViewSerializer(serializers.ModelSerializer):
    # 进行时间的格式化处理
    date = serializers.DateTimeField(format="%Y-%m-%d")
    class Meta:
        model = Notices
        fields = ["id", "title", "content", "is_show","date","inner_web_url"]
class GetNoticeView(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        queryset = Notices.objects.all().order_by('-date')

        serializer = GetNoticeViewSerializer(queryset, many=True)

        return Response({"code": 200, "message": "获取比赛通知成功", "data": serializer.data})

class GetNewsSerializer(serializers.ModelSerializer):
    # 进行时间的格式化处理
    dates = serializers.DateTimeField(format="%Y-%m-%d")
    type = serializers.CharField(source="get_type_display") #将其进行转化出对应的文字
    class Meta:
        model = News
        fields = ["id", "title", "content", "is_show","dates","type"]

class GetNews(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        queryset = News.objects.all().order_by('-dates')

        serializer = GetNewsSerializer(queryset, many=True)

        return Response({"code": 200, "message": "获取新闻成功", "data": serializer.data})


class GetAboutView(APIView):
    # 无需认证
    authentication_classes = []

    def get(self, request, *args, **kwargs):

        return '发送'








