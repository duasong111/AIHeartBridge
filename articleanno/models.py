import datetime
import django.utils.timezone as timezone
from django.db import models
from django.utils.encoding import smart_str

"""进行信息的通知"""
class About(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
    type = models.IntegerField(verbose_name="类型", choices=((1, "Q&A"), (2, "声明说明"), (3, "捐赠"), (4, "关于")), default=1)
    title = models.CharField(verbose_name="标题", max_length=64)
    content = models.TextField(verbose_name="内容", max_length=512)
    dates = models.DateTimeField(verbose_name="时间", default=timezone.now)
    url = models.TextField(verbose_name="链接", max_length=512, null=True, blank=True, default="")

    def __str__(self):
        return smart_str('%s-%s' % (self.title, self.type))

    class Meta:
        db_table = "everyday_about"
        verbose_name = '通知'
        verbose_name_plural = '信息通告'


"""关于新闻类型信息的通告"""
class Notices(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
    title = models.CharField(verbose_name="标题", max_length=64, null=False)
    content = models.TextField(verbose_name="主体内容", max_length=1024, null=False)
    inner_web_url = models.CharField(verbose_name="比赛官网", max_length=256, blank=True)
    addition_action_title = models.CharField(verbose_name="附加活动标题", max_length=256, blank=True)
    addition_action_url = models.CharField(verbose_name="附加活动地址", max_length=256, blank=True)
    background_color_1 = models.CharField(verbose_name="弹窗背景色1", max_length=24, default='default')
    background_color_2 = models.CharField(verbose_name="弹窗背景色2", max_length=24, default='default')
    background_color_3 = models.CharField(verbose_name="弹窗背景色3", max_length=24, default='default')
    is_show = models.BooleanField(verbose_name="是否展示", default=True, choices=((True, "是"), (False, "否")))
    is_important = models.BooleanField(verbose_name="是否紧急通知", default=False, choices=((True, "是"), (False, "否")))
    date = models.DateTimeField(verbose_name="通知时间", default=timezone.now)

    def __str__(self):
        return smart_str('%s-%s' % (self.id, self.title))

    class Meta:
        db_table = "everyday_notices"
        verbose_name = '信息通知'
        verbose_name_plural = '信息通告'

"""关于心理健康有关的新闻"""
class News(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
    type = models.IntegerField(verbose_name="类型", choices=((1, "获奖通告"), (2, "信息征集"), (3, "成员活动"), (4, "其他")), default=1)
    title = models.CharField(verbose_name="标题", max_length=64)
    content = models.TextField(verbose_name="内容", max_length=512)
    dates = models.DateTimeField(verbose_name="时间", default=timezone.now)
    url = models.TextField(verbose_name="链接", max_length=512, null=True, blank=True, default="")
    is_show = models.BooleanField(verbose_name="是否展示", default=True, choices=((True, "是"), (False, "否")))
    def __str__(self):
        return smart_str('%s-%s' % (self.title, self.type))

    class Meta:
        db_table = "news"
        verbose_name = '新闻发布'
        verbose_name_plural = '心理健康的新闻'