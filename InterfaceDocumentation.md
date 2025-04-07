# 接口文档说明文件

## 1. 获取用户信息
- **URL**: `/info/info-login/`
- **方法**: `POST`
- **参数**:
  - `Account` (int): 用户ID
  - `PassWord`(int): 用户密码
  - 举例说明{ "Account":"1234", "PassWord":"PassWord"}
- **返回值**:
  ```json
   {
    "code": 200,
    "message": "登录成功",
    "token": "6b68a0b6-1074-420e-8956-a2b8204b03f2",
    "last_login_date": "2025-01-08",
    "current_login_date": "2025-04-07"
}
  ```

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
    #去发送所有的测评的数据
    path('info-sendalltestdata/',views.GetTestDatas.as_view(),name='sendalltestdata')