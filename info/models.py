import uuid

from django.db import models
from django.utils.encoding import smart_str
# Create your models here.
class userInfo(models.Model):
    Name = models.CharField(verbose_name="姓名", max_length=32,null=True, blank=True)
    Account=models.CharField(verbose_name="账户",max_length=32,)
    PassWord=models.CharField(verbose_name="密码",max_length=32,)
    Email = models.CharField(verbose_name="邮箱", max_length=36,null=True, blank=True)
    Sex = models.IntegerField(verbose_name="性别", choices=((1, "男"), (2, "女")), default=1)
    Age = models.IntegerField(verbose_name="年龄",null=True, blank=True)
    # Education = models.IntegerField(verbose_name="教育", choices=((1, "小学"), (2, "初中"),
    # (3, "高中（职高，高技）"), (4, "中专"),(5, "大专(高职)"), (6, "本科"),(7, "硕士研究生"), (8, "博士研究生")), default=6),
    signature = models.CharField(verbose_name="个性签名",max_length=128,default="快乐活着")
    WorkingCondition=models.IntegerField(verbose_name="工作状态", choices=((1, "未曾工作"), (2, "工作中"), (3, "待就业")), default=1)
    HealthGrade= models.IntegerField(verbose_name="健康等级", choices=((1, "优秀"), (2, "良好"),(3, "一般"), (4, "较差"), (5, "差")), default=3)
    Country = models.CharField(verbose_name="国家", max_length=32,null=True, blank=True )
    Token = models.CharField(verbose_name="TOKEN", max_length=64, null=True, blank=True)
    PhoneNumber = models.CharField(verbose_name="手机号",max_length=32,null=True, blank=True )
    Address = models.CharField(verbose_name="地址", max_length=40,null=True, blank=True)
    LastLoginTime = models.DateField(verbose_name="上次登录时间",null=True, blank=True)
    def __str__(self):
        return smart_str('%s-%s' % (self.Name, self.LastLoginTime))
    class Meta:
        db_table = "login_userinfo"
        verbose_name = '用户信息'
        verbose_name_plural = '用户基本信息'
    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

# 新闻类型进行添加
class Language(models.Model):
    Name = models.CharField(verbose_name="新闻类型", max_length=32)
    def __str__(self):
        return self.Name
    class Meta:
        db_table = "news_type"
        verbose_name = '新闻类型'
        verbose_name_plural = '新闻类型'
class Project(models.Model):
    NEWS_CHOICES = (
        (1, "心理科普"),
        (2, "婚恋情感"),
        (3, "家庭关系"),
        (4, "人际社交"),
        (5, "自我觉察"),
        (6, "成长学习"),
        (7, "心理健康"),
        (8, "职场技能"),
    )

    Name = models.CharField(verbose_name="新闻标题", max_length=100)
    Edit = models.CharField(verbose_name="新闻编辑",max_length=30,default="张三")
    Time = models.DateField(verbose_name="时间")
    Description = models.TextField(verbose_name="描述")
    Memo = models.TextField(verbose_name="备注信息",default="暂无")
    News = models.IntegerField(verbose_name='专业选择',choices=NEWS_CHOICES,default=1)

    def __str__(self):
        return self.Name
    class Meta:
        db_table = "news_project"
        verbose_name = '新闻报道'
        verbose_name_plural = '新闻报道'

#心理测评数据存储
class QuickAssessment(models.Model):
    userId = models.CharField(max_length=100, verbose_name="用户ID", default=uuid.uuid4())
    user = models.CharField(verbose_name="用户名", max_length=32,null=True, blank=True)
    testTitile = models.CharField(verbose_name="题目",max_length=640,null=True, blank=True)
    testTime = models.DateTimeField(verbose_name="测试时间",null=True, blank=True)
    index = models.IntegerField(verbose_name="下标",null=True, blank=True)
    score = models.IntegerField(verbose_name="分数",null=True, default = 0 )
    '''心理测评类型1-心理健康问卷，2-情感问卷 3-人格测试'''
    testType = models.IntegerField(verbose_name="测试类型",null=True,default=1)
    def __str__(self):
        return self.user
    class Meta:
        db_table = "quick_assessment_db"
        verbose_name = '快速测评'
        verbose_name_plural = '快速测评题目集'

#快速测评选择集
class QuickAssessmentSelected(models.Model):
    userId = models.CharField(max_length=100, verbose_name="用户ID", default=uuid.uuid4())
    user = models.CharField(verbose_name="用户名", max_length=32, null=True, blank=True)
    randomQuestions = models.JSONField(verbose_name="所选题目集")
    selected = models.JSONField(verbose_name="选择的内容", default=list)
    latestScore = models.IntegerField(verbose_name="最终得分",null=True, blank=True)
    testTime = models.DateTimeField(verbose_name="测试时间",null=True, blank=True)
    def __str__(self):
        return self.user
    class Meta:
        db_table = "quick_assessment_result_db"
        verbose_name = '快评结果'
        verbose_name_plural = '快评结果集'