import requests
from django.http import HttpResponse
from rest_framework.views import APIView

API_KEY = "0YZOURxbxIDUsHFvd9vK1TXe"
SECRET_KEY = "EtmFTdPGzFsEBK9TMXKZvfL55zonRxQv"


def get_access_token():
    """
    获取百度的 access token
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return requests.post(url, params=params).json().get("access_token")


def text_to_speech(text):
    """
    使用百度的文字转语音接口，将文本转换为音频文件（二进制数据）
    """
    # 获取 access token
    token = get_access_token()

    # 百度语音合成接口 URL
    url = "https://tsn.baidu.com/text2audio"

    # 请求参数
    payload = {
        'tok': token,
        'cuid': 'your_cuid',  # 用户设备唯一标识
        'ctp': 1,  # 客户端类型
        'lan': 'zh',  # 语言类型
        'spd': 5,  # 语速
        'pit': 5,  # 音调
        'vol': 5,  # 音量
        'per': 1,  # 1 表示男性，0 表示女性
        'aue': 3,  # 返回音频格式：3 为 MP3 格式
        'tex': text  # 要转换的文本
    }

    # 发起 POST 请求
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        # 返回音频二进制数据
        return response.content
    else:
        # 请求失败时返回空或自定义错误信息
        return None