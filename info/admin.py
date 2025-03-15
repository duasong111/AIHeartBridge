from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from .models import userInfo,Language, Project
@admin.register(userInfo)
class userInfoShow(admin.ModelAdmin):
    ordering = ('id',)
    fieldsets = (
        ("个人信息", {'fields': ['Name','Account','Age','Country', 'Email','Sex','Address' ]}),
        ("状态信息", {'fields': ['WorkingCondition','HealthGrade','PhoneNumber','LastLoginTime']}),
    )
    list_display = ('id', 'Name', 'Account', 'Country', 'Sex', 'HealthGrade','LastLoginTime')


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
