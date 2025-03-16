from datetime import datetime

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from API.AIMod2 import get_spark_response ,trim_history # 导入封装好的函数
from .models import AiWithUserChatingInformation

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
    '''此处是进行10条输出传输过来，然后使用大模型进行分析'''
    def get(self, request, *args, **kwargs):
        return "还没有写"