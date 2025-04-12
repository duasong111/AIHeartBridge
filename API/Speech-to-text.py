import requests
import json

API_KEY = "0YZOURxbxIDUsHFvd9vK1TXe"
SECRET_KEY = "EtmFTdPGzFsEBK9TMXKZvfL55zonRxQv"


def main():
    # 读取音频文件（static/test.mp3）
    audio_file_path = "../test.mp3"
    with open(audio_file_path, 'rb') as f:
        audio_data = f.read()

    # 获取百度API的access token
    access_token = get_access_token()

    # 请求URL
    url = "https://vop.baidu.com/server_api"

    # 请求体参数
    payload = {
        "format": "mp3",  # 确保这里的格式与音频文件一致
        "rate": 16000,
        "channel": 1,
        "cuid": "WKrotlaPdTQ0j8cPz8I6udmKIiqQS8Mx",
        "token": access_token
    }

    # 上传文件和参数
    files = {
        'audio': ('test.mp3', audio_data)
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # 发送POST请求
    response = requests.post(url, headers=headers, data=json.dumps(payload).encode("utf-8"), files=files)

    # 打印返回的结果
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Error:", response.text)


def get_access_token():
    """
    使用 API_KEY 和 SECRET_KEY 获取 Access Token
    :return: access_token，或 None（如果获取失败）
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    response = requests.post(url, params=params)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Failed to get access token:", response.text)
        return None


if __name__ == '__main__':
    main()
