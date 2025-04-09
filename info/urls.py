'''版本说明:由于上一个项目是使用Django:3.2 所以其是支持 from django.conf.urls import url
并且在path路径下是要求去使用正则表达式去进行匹配的，例如：    url(r'^client-login/$', views.RegistesView.as_view(), name='login'),
目前该项目采用的Django版本号为 4.2.15 不再支持以上操作
路由选择和上述是一样的，只不过不再增加正则表达式进行匹配
'''

from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    #用户进行登录
    path('info-login/', views.LoginView.as_view(), name='login'),
    #用户进行注册
    path('info-register/', views.RegisterView.as_view(), name='register'),
    #返回用户查询的数据结果
    path('info-userinform/', views.ReturnUserInform.as_view(), name='userinform'),
    #新闻列表
    path('info-newslist/', views.NewsInformationView.as_view(), name='news'),
    #新闻记录存储
    path('info-newslistdetail/', views.NewsDetailView.as_view(), name='newsdetail'),
    #去存储有关心理健康15条数据集合返回
    path('info-psychometrics/',views.GetPsychometricsView.as_view(),name='psychometrics'),
    #去获取用户的聊天数据的返回列表
    path('info-getquestionlist/',views.GetTestQuestions.as_view(),name='getquestionlist'),
    # 对用户选择过的东西去进行一个归纳总结
    path('info-assessmentsummary/',views.QuickAssessmentsummarize.as_view(),name='assessmentsummary'),
    #去发送所有的测评的数据---
    path('info-sendalltestdata/',views.GetTestDatas.as_view(),name='sendalltestdata')
]