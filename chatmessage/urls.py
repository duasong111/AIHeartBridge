from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    # AI与用户进行聊天的心理进行存储
    path('ai-chat/', views.AIWithUserChatView.as_view(), name='chat'),
    # 用户与AI进行聊天的内容，每十次进行一个数据更新处理
    path('ai-messagedel/', views.AIDealChatMessageView.as_view(), name='deal-message'),
    # 实现文字转语音的说明
    path('audio-play/', views.AudioPlay.as_view(), name='audio-play'),
    # 实现语言转文字的说明
    path('speech-to-text/', views.SpeechToText.as_view(), name='speech-to-text'),

]
