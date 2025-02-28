from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from .models import userInfo
@admin.register(userInfo)
class userInfoShow(admin.ModelAdmin):
    ordering = ('id',)
    fieldsets = (
        ("个人信息", {'fields': ['Name','Account','Age','Country', 'Email','Sex','Address' ]}),
        ("状态信息", {'fields': ['WorkingCondition','HealthGrade','PhoneNumber','LastLoginTime']}),
    )
    list_display = ('id', 'Name', 'Account', 'Country', 'Sex', 'HealthGrade','LastLoginTime')
