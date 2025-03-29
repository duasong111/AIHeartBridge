from django.contrib.admin import ModelAdmin, register
from .models import Notices, About,News



@register(About)
class AboutAdmin(ModelAdmin):
    ordering = ('id',)
    fieldsets = (
        ("类型", {'fields': ['type','is_show']}),
        ("内容", {'fields': ['title', 'content', 'url','color','dates']}),
    )
    list_display = ('id', 'type', 'title','content','is_show','color','dates')


@register(Notices)
class NoticeAdmin(ModelAdmin):
    ordering = ('-id',)
    fieldsets = (
        ("基本信息", {'fields': ['title', 'is_show', 'is_important', 'date']}),
        ("内容",
         {'fields': ['content', 'inner_web_url', 'addition_action_title', 'addition_action_url',
            ]}),
    )
    list_display = ('id', 'title', 'content', 'is_show', 'is_important', 'date')
    search_fields = ('title', 'is_show', 'is_important', 'date')
    list_per_page = 20

"""关于心理健康的新闻"""
@register(News)
class AboutAdmin(ModelAdmin):
    ordering = ('id',)
    fieldsets = (
        ("必填内容", {'fields': ['title', 'content', ]}),
        ("类型", {'fields': ['type','is_show']}),
        ("选填", {'fields': ['url', 'dates']}),
    )
    list_display = ('id', 'type', 'title','is_show', 'dates')
