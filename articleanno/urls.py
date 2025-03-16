from django.urls import path
from django.contrib import admin
from . import views



urlpatterns = [
    #进行自定义新闻列表
    path('art-news/', views.GetNews.as_view(), name='get-news'),
    #进行首页面常见进行展示
    path('art-notice/', views.GetNoticeView.as_view(), name='get-notice'),
    #进行该系统页面的整个一键播报功能
    path('art-about/', views.GetAboutView.as_view(), name='get-about'),
]


