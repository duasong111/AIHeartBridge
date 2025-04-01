from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from .models import userInfo,Language, Project,QuickAssessment,QuickAssessmentSelected
@admin.register(userInfo)
class userInfoShow(admin.ModelAdmin):
    ordering = ('id',)
    fieldsets = (
        ("个人信息", {'fields': ['Name','Account','Age','Country','signature' ,'Email','Sex','Address' ]}),
        ("状态信息", {'fields': ['WorkingCondition','HealthGrade','PhoneNumber','LastLoginTime']}),
    )
    list_display = ('id', 'Name', 'Account', 'Country','signature' ,'Sex', 'HealthGrade','LastLoginTime')

@register(Language)
class Language(admin.ModelAdmin):

    list_display = ('id','Name',)
@register(Project)
class AboutAdmin(admin.ModelAdmin):
    fieldsets = (
        ("人物", {'fields': ['Name',  'Edit']}),
        ("其他", {'fields': ['News','Time','Description','Memo']}),
    )
    list_display = ('id','Name','Edit','News' ,'Description','Memo', 'Time',)

@register(QuickAssessment)
class QuickAssessment(admin.ModelAdmin):
    fieldsets = (
        ("有关", {'fields': ['user',  'testTitile','testTime']}),
    )
    list_display = ('userId','user','testTitile','index','score','testTime' )

@register(QuickAssessmentSelected)
class QuickAssessmentSelected(admin.ModelAdmin):
    fieldsets = (
        ("人物", {'fields': ['user',  'latestScore']}),
        ("其他", {'fields': ['testTime','selected','randomQuestions']}),
    )
    list_display = ('id','user','latestScore','testTime','selected' ,'randomQuestions' )
