# deepseek_api.py
from openai import OpenAI
import requests  # 添加 requests 异常处理支持

# 初始化 DeepSeek 客户端
client = OpenAI(api_key="sk-f0a368779df94a55a05371e138f7ce43", base_url="https://api.deepseek.com/v1")

def analyze_messages_with_deepseek(messages):
    """
    使用 DeepSeek 分析消息列表
    :param messages: 包含 content、sender、timestamp 的消息列表
    :return: AI 的分析结果
    """
    # 将消息格式化为字符串，便于大模型分析
    formatted_messages = "\n".join(
        [f"[{msg['timestamp']} - {msg['sender']}]: {msg['content']}" for msg in messages]
    )

    # 构造提示，要求 AI 分析这组消息
    prompt = (
        f"以下是一段对话记录，请分析其内容并提供简短的总结或建议：\n\n"
        f"{formatted_messages}\n\n"
        "总结或建议："
    )

    try:
        # 调用 DeepSeek API
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled in analyzing conversations."},
                {"role": "user", "content": prompt}
            ],
            stream=False,
            timeout=30  # 设置超时，避免长时间等待
        )
        return response.choices[0].message.content

    except requests.exceptions.ConnectionError as conn_err:
        return f"Error: Connection failed - {str(conn_err)}"
    except requests.exceptions.Timeout as timeout_err:
        return f"Error: Request timed out - {str(timeout_err)}"
    except requests.exceptions.RequestException as req_err:
        return f"Error: API request failed - {str(req_err)}"
    except Exception as e:
        return f"Error: Unexpected error - {str(e)}"