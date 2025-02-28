from django.db import models
from django.utils.encoding import smart_str
# Create your models here.
class userInfo(models.Model):
    Name = models.CharField(verbose_name="姓名", max_length=32)
    Account=models.CharField(verbose_name="账户",max_length=32,)
    PassWord=models.CharField(verbose_name="密码",max_length=32,)
    Email = models.CharField(verbose_name="邮箱", max_length=36)
    Sex = models.IntegerField(verbose_name="性别", choices=((1, "男"), (2, "女")), default=1)
    Age = models.IntegerField(verbose_name="年龄")
    # Education = models.IntegerField(verbose_name="教育", choices=((1, "小学"), (2, "初中"),
    # (3, "高中（职高，高技）"), (4, "中专"),(5, "大专(高职)"), (6, "本科"),(7, "硕士研究生"), (8, "博士研究生")), default=6),

    WorkingCondition=models.IntegerField(verbose_name="工作状态", choices=((1, "未曾工作"), (2, "工作中"), (3, "待就业")), default=1)
    HealthGrade= models.IntegerField(verbose_name="健康等级", choices=((1, "优秀"), (2, "良好"),(3, "一般"), (4, "较差"), (5, "差")), default=3)
    Country = models.CharField(verbose_name="国家", max_length=32, )
    Token = models.CharField(verbose_name="TOKEN", max_length=64, null=True, blank=True)
    PhoneNumber = models.CharField(verbose_name="手机号",max_length=32, )
    Address = models.CharField(verbose_name="地址", max_length=40)
    LastLoginTime = models.DateField(verbose_name="上次登录时间")
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
