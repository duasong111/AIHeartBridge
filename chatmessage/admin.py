from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from .models import AiWithUserChatingInformation,traditionalAnsweringMode,QuestionHistory



@admin.register(AiWithUserChatingInformation)
class AiWithUserChatingShow(admin.ModelAdmin):
    ordering = ('id',)
    fieldsets = (
        ("话题", {'fields': ['TopicName','TopicStartTime','TopicEndTime', 'KeyMan']}),
        ("其他", {'fields': ['TopicSummary','HealthScore','TopicSensitiveLevel','PredictivePsychology']}),
        ("备注", {'fields': ['Memo']}),
    )
    list_display = ('id', 'TopicName', 'TopicStartTime', 'TopicEndTime', 'TopicSensitiveLevel')

#展示其他数据库的内容
@admin.register(traditionalAnsweringMode)
class TraditionalAnsweringModeShow(admin.ModelAdmin):
    fieldsets = (
        ("话题", {'fields': ['content',  'score']}),
        ("创建时间", {'fields': ['created_at','index']}),
    )
    list_display = ('id', 'content', 'index', 'score', 'created_at')

# 展示历史记录的数据库
@admin.register(QuestionHistory)
class QuestionHistoryShow(admin.ModelAdmin):
    fieldsets = (
        ("用户", {'fields': ['user', 'choices','score']}),
        ("细节性的内容", {'fields': ['question', 'created_at']}),
        ("用户感想", {'fields': ['experience']}),
    )
    list_display = ('id', 'user', 'score', 'question', 'created_at')

