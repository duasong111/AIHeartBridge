from datetime import datetime

from django.shortcuts import render
import uuid
import json
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from info import models
from staticData import HealthLevelData,AINoticeWordAnalyse
from .models import Language, Project,QuickAssessment,QuickAssessmentSelected,userInfo
from chatmessage.models import  summaryAnswerStorage
from rest_framework import status
from rest_framework import exceptions
from API.DeepSeek import  analyze_messages_with_deepseek

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
        # 获取当前日期
        current_date = datetime.now().date()
        # 如果是第一次登录，初始化 LastLoginTime
        if not instance.LastLoginTime:
            instance.LastLoginTime = current_date
        # 生成新的 token
        token = str(uuid.uuid4())
        instance.Token = token
        instance.save()
        # 在下次登录时更新 LastLoginTime（这里只是展示逻辑）
        # 实际需要额外的机制，比如在用户退出时更新
        return Response({
            "code": 200,
            "message": "登录成功",
            "token": token,
            "last_login_date": str(instance.LastLoginTime) if instance.LastLoginTime else None,
            "current_login_date": str(current_date)
        })

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


    # 进行心理测评的展示信息
class GetPsychometricsView(APIView):
    authentication_classes = []
    def get(self, request, *args, **kwargs):
        data = summaryAnswerStorage.objects.all()
        serializer = PsychometricDetailSerializer(data, many=True)
        return Response({"code": 200, "message": "获取数据成功", "data": serializer.data})

# 得到所有的数据的序列化
class GetTestQuestionsSerializer(serializers.ModelSerializer):
    testTime = serializers.DateTimeField(format="%Y-%m-%d")
    class Meta:
        model = QuickAssessment
        fields = ['userId','user','testTitile','testTime','index','score','testType']

 # 获取测评的随机20条数据进行返回
class GetTestQuestions(APIView):
    authentication_classes = []
    def post(self,request,*args, **kwargs):
        test_type = request.data.get('type')
        if test_type is not None:
            data = QuickAssessment.objects.filter(testType=test_type).order_by('?')[:20]
        else: # 有检索类型返回检索类型，没有检索类型就按照全部的去进行返回
            data = QuickAssessment.objects.order_by('?')[:20]
        serializer = GetTestQuestionsSerializer(data, many=True)
        return Response({"code": 200, "message": "获取数据成功", "data": serializer.data})

# 对用户进行选择的数据进行一个归纳
class QuickAssessmentsummarize(APIView):
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        # 将用户选择的20条数据进行归纳 -- QuickAssessmentSelected
        try:
            # 提取数据
            user = request.data.get('user')
            random_questions = request.data.get('randomQuestions', [])
            selected = request.data.get('selected', [])
            latest_score = request.data.get('latestScore')
            test_time = request.data.get('testTime')
            # 处理 selected，将 None 替换为 0
            if not isinstance(selected, list):
                selected = []
            processed_selected = [0 if item is None else item for item in selected]
            # 处理 randomQuestions，转换为目标格式
            if not isinstance(random_questions, list):
                random_questions = []
            grouped_data = {}
            for item in random_questions:
                user_key = (item['user'], item['userId'])  # 用 (user, userId) 作为唯一键
                if user_key not in grouped_data:
                    grouped_data[user_key] = {
                        "user": item['user'],
                        "userId": item['userId'],
                        "testData": [],
                        "testTime": item['testTime']  # 使用第一条记录的时间
                    }
                grouped_data[user_key]["testData"].append({
                    "score": item['score'],
                    "testTitile": item['testTitile']
                })
            processed_random_questions = list(grouped_data.values())

            # 处理 latestScore
            if latest_score is not None:
                latest_score = int(latest_score)

            # 处理 testTime，移除时区信息
            if test_time:
                dt = datetime.fromisoformat(test_time.replace('Z', '+00:00'))
                test_time = dt.replace(tzinfo=None)

            # 创建并保存到数据库
            assessment = QuickAssessmentSelected(
                user=user,
                randomQuestions=processed_random_questions,  # 保存转换后的数据
                selected=processed_selected,
                latestScore=latest_score,
                testTime=test_time
            )
            assessment.save()

            # 调用 DeepSeek API 进行分析
            # 将 randomQuestions 转换为 DeepSeek 需要的消息格式
            messages_for_ai = []
            for group in processed_random_questions:
                for test in group["testData"]:
                    messages_for_ai.append({
                        "content": f"Score: {test['score']} for {test['testTitile']}",
                        "sender": group["user"],
                        "timestamp": group["testTime"]
                    })


            # 调用 DeepSeek 分析
            ai_analysis = analyze_messages_with_deepseek(messages_for_ai,AINoticeWordAnalyse)
            '''需要改进的地方就是给AI一些特定的返回格式，以及前端需要去等一会，需要去等一小段时间，在
            等的过程中显示Ai正在分析的页面'''
            # 返回响应，包含 AI
            return Response({
                "message": "数据保存成功并完成AI分析",
                "id": str(assessment.userId),
                "saved_randomQuestions": assessment.randomQuestions,
                "saved_selected": assessment.selected,
                "ai_analysis": ai_analysis  # 添加 AI 分析结果
            }, status=200)



        except ValueError as e:
            return Response({"error": f"数据格式错误: {str(e)}"}, status=400)
        except Exception as e:
            return Response({"error": f"保存失败: {str(e)}"}, status=500)

# 发送所有的测评数据(是一个小的接口)
class GetTestDatas(APIView):
    authentication_classes = []
    def get(self,request,*args, **kwargs):
        result_data ={
            "code":200,
            "message:":"获取数据成功",
            "data":HealthLevelData
        }
        return Response(result_data)

#返回用户的所有的信息
class ReturnUserInform(APIView):
    authentication_classes = []
    def post(self,request,*args,**kwargs):
        try:
            account = request.data.get('account')
            if not account:
                return Response({"error": "账户名不能为空"}, status=400)
            user_records = userInfo.objects.filter(Account=account)
            data = [
                {
                    "user": record.Name,
                    "Account":record.Account,
                    "email": record.Email,
                    "signature":record.signature,
                    "Country":record.Country,
                    "LastLoginTime":record.LastLoginTime,
                    "Address":record.Address

                }
                for record in user_records
            ]
            # 返回响应
            return Response({
                "message": "查询成功",
                "data": data
            }, status=200)
        except ValueError as e:
            return Response({"error": f"数据格式错误: {str(e)}"}, status=400)
        except Exception as e:
            return Response({"error": f"保存失败: {str(e)}"}, status=500)
