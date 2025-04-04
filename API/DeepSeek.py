# deepseek_api.py
from openai import OpenAI
import requests  # 添加 requests 异常处理支持

# 初始化 DeepSeek 客户端
client = OpenAI(api_key="sk-f0a368779df94a55a05371e138f7ce43", base_url="https://api.deepseek.com/v1")

def analyze_messages_with_deepseek(messages, prompt_template=None):
    """
    使用 DeepSeek 分析消息列表，支持自定义提示词模板
    :param messages: 包含 content、sender、timestamp 的消息列表
    :param prompt_template: 可选的自定义提示词模板，需包含 {formatted_messages} 占位符
    :return: AI 的分析结果
    """
    # 将消息格式化为字符串，便于大模型分析
    formatted_messages = "\n".join(
        [f"[{msg['timestamp']} - {msg['sender']}]: {msg['content']}" for msg in messages]
    )

    # 构造提示词逻辑
    try:
        if prompt_template:  # 使用自定义模板
            prompt = prompt_template.format(formatted_messages=formatted_messages)
        else:  # 默认模板
            prompt = (
                f"以下是一段对话记录，请分析其内容并提供简短的总结或建议：\n\n"
                f"{formatted_messages}\n\n"
                "总结或建议："
            )
    except KeyError:  # 捕获占位符缺失错误
        prompt = (  # 自动回退到默认模板
            f"⚠️ 自定义模板缺少 {{formatted_messages}} 占位符，已使用默认模板\n\n"
            f"以下是一段对话记录，请分析其内容并提供简短的总结或建议：\n\n"
            f"{formatted_messages}\n\n"
            "总结或建议："
        )
    except Exception as e:  # 其他模板错误
        return f"Error: 提示词模板解析失败 - {str(e)}"

    try:
        # 调用 DeepSeek API
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled in analyzing conversations."},
                {"role": "user", "content": prompt}
            ],
            stream=False,
            timeout=30
        )
        return response.choices[0].message.content

    except requests.exceptions.ConnectionError as conn_err:
        return f"Error: 连接失败 - {str(conn_err)}"
    except requests.exceptions.Timeout as timeout_err:
        return f"Error: 请求超时 - {str(timeout_err)}"
    except requests.exceptions.RequestException as req_err:
        return f"Error: API 请求失败 - {str(req_err)}"
    except Exception as e:
        return f"Error: 未知错误 - {str(e)}"