from django.db import models
import django.utils.timezone as timezone
from django.db import models
from django.utils.encoding import smart_str

"""获取AI与人之间聊天的内容并进行存储"""
class AiWithUserChatingInformation(models.Model):

    TopicName = models.CharField(verbose_name="话题名称",max_length=40)
    TopicStartTime = models.TimeField(verbose_name="话题开始时间",default=timezone.now)
    TopicEndTime = models.TimeField(verbose_name="话题结束时间", default=timezone.now)
    KeyMan = models.TextField(verbose_name="关键人物",max_length=50)
    TopicSummary = models.TextField(verbose_name="话题总结",max_length=60)
    HealthScore = models.CharField(verbose_name="心理健康打分",max_length=60)
    TopicSensitiveLevel = models.IntegerField(verbose_name="话题敏感度级别",
                                              choices=((1, "一级"), (2, "二级"), (3, "三级"), (4, "四级"), (5, "五级")),
                                              default=1)
    PredictivePsychology = models.IntegerField(verbose_name="健康等级", choices=((1, "优秀"), (2, "良好"),(3, "一般"), (4, "较差"), (5, "差")), default=3)
    Memo = models.TextField(verbose_name="备注信息",null=True,default="无")

    def __str__(self):
        return smart_str('%s-%s' % (self.TopicName, self.TopicStartTime))
    class Meta:
        db_table = "ChattingWithAI"
        verbose_name = 'AI聊天'
        verbose_name_plural = 'AI聊天存储'

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True