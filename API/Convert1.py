import requests
import json
import os
import base64
import librosa
import soundfile as sf
import numpy as np

# 百度API的密钥
API_KEY = ""
SECRET_KEY = ""


def get_access_token():
    """
    使用API_KEY和SECRET_KEY获取百度API的Access Token。
    :return: access_token (str)，失败时返回None。
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        result = response.json()
        access_token = result.get("access_token")
        if not access_token:
            print(f"获取Access Token失败，返回结果: {result}")
        return access_token
    except requests.RequestException as e:
        print(f"获取Access Token失败: {e}")
        return None


def convert_mp3_to_wav(mp3_path):
    """
    将 MP3 文件转换为 WAV 格式（单声道，16000 Hz）。
    :param mp3_path: MP3 文件路径。
    :return: WAV 二进制数据。
    """
    try:
        # 使用 librosa 加载 MP3 文件
        audio, sr = librosa.load(mp3_path, sr=16000, mono=True)

        # 使用 soundfile 保存为 WAV
        temp_wav_path = "temp.wav"
        sf.write(temp_wav_path, audio, sr, format="WAV")

        # 读取 WAV 数据
        with open(temp_wav_path, "rb") as f:
            wav_data = f.read()

        # 清理临时文件
        os.remove(temp_wav_path)

        return wav_data
    except Exception as e:
        print(f"音频转换失败: {e}")
        return None


def speech_to_text(audio_data, audio_format="wav", sample_rate=16000):
    """
    将音频数据转换为文字，使用百度语音转文字API。
    :param audio_data: 音频的二进制数据。
    :param audio_format: 音频格式（如'wav', 'pcm'）。
    :param sample_rate: 音频采样率（如16000）。
    :return: 包含转录结果或错误信息的字典。
    """
    # 检查音频数据是否有效
    if not audio_data:
        return {"text": None, "error": "音频数据为空"}

    # 获取Access Token
    access_token = get_access_token()
    if not access_token:
        return {"text": None, "error": "无法获取Access Token"}

    # 百度语音转文字API地址
    url = "https://vop.baidu.com/server_api"

    # 将音频数据编码为 Base64
    audio_base64 = base64.b64encode(audio_data).decode('utf-8')

    # 请求参数
    payload = {
        "format": audio_format,
        "rate": sample_rate,
        "channel": 1,
        "cuid": "WKrotlaPdTQ0j8cPz8I6udmKIiqQS8Mx",
        "token": access_token,
        "speech": audio_base64,
        "len": len(audio_data)
    }

    try:
        # 发送POST请求
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        if "result" in result and result["result"]:
            return {"text": result["result"][0], "error": None}
        else:
            return {"text": None, "error": result.get("err_msg", "未知错误")}
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return {"text": None, "error": f"请求失败: {e}"}


if __name__ == '__main__':
    # 测试音频文件路径
    audio_file_path = "output.mp3"
    # 检查文件是否存在
    if not os.path.exists(audio_file_path):
        print(f"错误: 音频文件 {audio_file_path} 不存在")
    else:
        try:
            # 转换为 WAV
            wav_data = convert_mp3_to_wav(audio_file_path)
            if not wav_data:
                print("转换 WAV 失败，退出")
            else:
                print(f"成功转换为 WAV，大小: {len(wav_data)} 字节")
                # 调用语音转文字
                result = speech_to_text(wav_data, audio_format="wav", sample_rate=16000)
                print(f"最终结果: {result}")
        except Exception as e:
            print(f"处理音频文件失败: {e}")
