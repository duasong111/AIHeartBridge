from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from .models import AiWithUserChatingInformation



@admin.register(AiWithUserChatingInformation)
class AiWithUserChatingShow(admin.ModelAdmin):
    ordering = ('id',)
    fieldsets = (
        ("话题", {'fields': ['TopicName','TopicStartTime','TopicEndTime', 'KeyMan']}),
        ("其他", {'fields': ['TopicSummary','HealthScore','TopicSensitiveLevel','PredictivePsychology']}),
        ("备注", {'fields': ['Memo']}),
    )
    list_display = ('id', 'TopicName', 'TopicStartTime', 'TopicEndTime', 'TopicSensitiveLevel')
