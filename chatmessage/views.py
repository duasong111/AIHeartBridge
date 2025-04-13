import base64
import json
import os
from datetime import datetime

import librosa
import requests
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import soundfile as sf
from django.http import HttpResponse
from API.AIMod2 import get_spark_response, trim_history  # 导入封装好的函数
# from staticData import AINoticeWordAnalyse
from .models import AiWithUserChatingInformation,summaryAnswerStorage
from API.DeepSeek import analyze_messages_with_deepseek
from API.convert2 import text_to_speech
from API.Convert1 import speech_to_text

class AIWithUserChatView(APIView):
    authentication_classes = []  # 无需认证
    '''此处是进行与AI大模型进行沟通对话的内容，已经进行了上下文效果不是很理想，期待后续开发中进行进一步的完善'''

    def post(self, request, *args, **kwargs):
        input_text = request.data.get('input_text', None)
        user_id = request.data.get('user_id', 'default_user')
        topic_name = request.data.get('topic_name', '默认话题')  # 前端传入话题名称，默认值为“默认话题”

        if not input_text:
            return Response({
                "code": 400,
                "message": "请提供输入消息",
                "error": "input_text is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 获取当前话题的对话历史
            history_records = AiWithUserChatingInformation.objects.filter(
                UserId=user_id,
                TopicName=topic_name
            ).order_by('TopicStartTime')

            # 将数据库记录转为 Spark 需要的格式
            history = [
                {"role": record.Role, "content": record.Content}
                for record in history_records
            ]

            # 添加当前用户输入到历史
            history.append({"role": "user", "content": input_text})

            # 调用 Spark 大模型，传入完整历史
            ai_response = get_spark_response(trim_history(history))

            # 保存用户输入到数据库
            AiWithUserChatingInformation.objects.create(
                UserId=user_id,
                Role="user",
                Content=input_text,
                TopicName=topic_name,
                TopicStartTime=datetime.now(),
                TopicEndTime=datetime.now(),  # 暂时设为当前时间，可根据需要调整
                KeyMan="未知",  # 可根据业务逻辑动态填充
                TopicSummary="未总结",  # 可后续通过其他逻辑生成
                HealthScore="未知",
                TopicSensitiveLevel=1,  # 默认值，可根据内容分析调整
                PredictivePsychology=3,  # 默认“一般”
                Memo="无"
            )

            # 保存 AI 回复到数据库
            AiWithUserChatingInformation.objects.create(
                UserId=user_id,
                Role="assistant",
                Content=ai_response,
                TopicName=topic_name,
                TopicStartTime=timezone.now(),
                TopicEndTime=timezone.now(),
                KeyMan="未知",
                TopicSummary="未总结",
                HealthScore="未知",
                TopicSensitiveLevel=1,
                PredictivePsychology=3,
                Memo="无"
            )

            return Response({
                "code": 200,
                "message": "返回成功",
                "response": ai_response
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "code": 400,
                "message": "返回失败",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AIDealChatMessageView(APIView):
    authentication_classes = []  # 无需认证
    '''该接口是能够将用户与星火大模型之间的聊天之间进行一个汇总，并将汇总内容以列表的形式去传输给DeepSeek
    再由deepseek去进行一个汇总，并将汇总数据进行存储'''
    def post(self, request, *args, **kwargs):
        try:
            # 解码字节数据为 UTF-8 字符串
            data = json.loads(request.body.decode('utf-8'))
            if "messageList" not in data or not isinstance(data["messageList"], list):
                return Response(
                    {"error": "Request must contain a 'messageList' key with a list of messages"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            messages = data["messageList"][:10]
            for msg in messages:
                if not all(key in msg for key in ["content", "sender", "timestamp"]):
                    return Response(
                        {"error": "Each message must have 'content', 'sender', and 'timestamp'"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            analysis_result = analyze_messages_with_deepseek(messages)

            summaryAnswerStorage.objects.create(
                UserId='00001',
                Content=data,
                ReturnTime=timezone.now(),
                TopicSummary=analysis_result,
                HealthScore='None',
                Memo='None'
            )
            # 部分数据先暂时mock，到时候根据用户来去确定
            return Response({
                "code": 200,
                "message": "返回成功",
                "response": analysis_result
            }, status=status.HTTP_200_OK)

        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)
        except UnicodeDecodeError:
            return Response({"error": "Data encoding error, please use UTF-8"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AudioPlay(APIView):
    authentication_classes = []  # 无需认证
    def post(self, request):
        """
        接收前端传来的文本并调用文字转语音接口，返回 Base64 编码的音频数据
        """
        # 获取前端传来的文本
        text = request.data.get('text')
        # 调用文字转语音函数（假设返回的是二进制音频数据）
        audio_data = text_to_speech(text)
        if audio_data:
            # 将二进制音频数据编码为 Base64
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            # 返回 JSON 响应，包含 Base64 编码的音频数据
            return JsonResponse({
                'status': 'success',
                'audio_data': audio_base64,
                'format': 'mp3'  # 可选，告诉前端音频格式
            })
        else:
            # 如果转换失败，返回错误信息
            return JsonResponse({'status': 'error', 'message': '语音转换失败'}, status=500)


class SpeechToText(APIView):
    authentication_classes = []  # 无需认证

    def post(self, request, *args, **kwargs):
        """
        接收微信小程序上传的音频文件，调用百度API转为文字并返回结果。
        """
        if "audio" not in request.FILES:
            return Response(
                {"error": "未上传音频文件"},
                status=status.HTTP_400_BAD_REQUEST
            )
        audio_file = request.FILES["audio"]
        try:
            audio_data = audio_file.read()
            print(f"收到音频文件: {audio_file.name}, 大小: {len(audio_data)} 字节")
        except Exception as e:
            return Response(
                {"error": f"读取音频文件失败: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 保存上传文件（调试用，保持与文件扩展名一致）
        file_ext = os.path.splitext(audio_file.name)[1].lower().lstrip(".")
        debug_path = f"debug_uploaded.{file_ext}"
        with open(debug_path, "wb") as f:
            f.write(audio_data)
        print(f"已保存上传文件到: {debug_path}")

        if file_ext not in ["wav", "pcm"]:
            return Response(
                {"error": "仅支持wav或pcm格式"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 直接调用 speech_to_text（WAV 无需转换）
        result = speech_to_text(
            audio_data=audio_data,
            audio_format=file_ext,
            sample_rate=16000
        )
        print(f"百度API返回: {result}")
        if result.get("error"):
            return Response(
                {"error": result["error"]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            {"text": result["text"]},
            status=status.HTTP_200_OK
        )