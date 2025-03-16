from django.urls import path
from django.contrib import admin
from . import views



urlpatterns = [
    path('art-notice/', views.GetNoticeView.as_view(), name='get-notice'),
    path('art-news/', views.GetNews.as_view(), name='get-news'),
    path('art-about/', views.GetAboutView.as_view(), name='get-about'),
]


