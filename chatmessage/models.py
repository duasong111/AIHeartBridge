from django.db import models
import django.utils.timezone as timezone
from django.db import models
from django.utils.encoding import smart_str

"""获取AI与人之间聊天的内容并进行存储"""
class AiWithUserChatingInformation(models.Model):
    UserId = models.CharField(max_length=100, default="default_user")
    Role = models.CharField(max_length=10, choices=[("user", "User"), ("assistant", "Assistant")])
    Content = models.TextField()
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
        return True
class traditionalAnsweringMode(models.Model):
    content = models.CharField(
        max_length=200,
        verbose_name="题目内容"
    )
    index = models.IntegerField(
        verbose_name="题目序号",
        default=0
    )
    score = models.IntegerField(
        verbose_name="分数",
        default=0,
    )
    created_at = models.DateTimeField(
        verbose_name="创建时间",
        default=timezone.now
    )

    class Meta:
        verbose_name = "传统答题模式"
        verbose_name_plural = "传统答题模式"
        ordering = ['index']  # 默认按序号排序

    def __str__(self):
        return f"{self.content[:20]} (index: {self.index})"

class QuestionHistory(models.Model):
    user = models.ForeignKey(
        'info.userInfo',
        on_delete=models.CASCADE,
        verbose_name="用户",
        related_name="question_histories"
    )
    question = models.CharField(
        max_length=200,
        verbose_name="题目"
    )
    choices = models.CharField(
        max_length=200,
        verbose_name="选项"
    )
    score = models.IntegerField(
        verbose_name="分数",
        default=0
    )
    experience = models.TextField(
        max_length=500,
        verbose_name="心得体会",
        blank=True,  # 允许为空
        null=True
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="创建时间"
    )

    class Meta:
        verbose_name = "问题历史记录"
        verbose_name_plural = "问题历史记录"
        ordering = ['-created_at']  # 默认按创建时间倒序

    def __str__(self):
        return f"{self.user} - {self.question[:20]}"
