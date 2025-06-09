import requests
import sys

# API 配置
API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/739f8ca9219f7ae877b46759f7fe9eb3/ai/run/"
headers = {"Authorization": ""}

# 模型选择
MODEL = "@cf/meta/llama-3-8b-instruct"


def run_model(messages):
    """调用 Cloudflare AI API"""
    input_data = {"messages": messages}
    try:
        response = requests.post(f"{API_BASE_URL}{MODEL}", headers=headers, json=input_data)
        response.raise_for_status()  # 检查 HTTP 错误
        result = response.json()
        if 'result' in result and 'response' in result['result']:
            return result['result']['response']
        else:
            return "Error: Unexpected response format"
    except requests.exceptions.RequestException as e:
        return f"Error: API request failed - {str(e)}"


def main():
    # 初始化对话历史
    conversation = [
        {
            "role": "system",
            "content": "You are a friendly assistant that helps write stories"
        }
    ]

    print("欢迎使用故事生成助手！输入您的请求开始创作（输入 'quit' 退出）")
    print("例如：'Write a short story about a llama that goes on a journey to find an orange cloud'")

    while True:
        # 获取用户输入
        user_input = input("\n您：").strip()

        if user_input.lower() == 'quit':
            print("感谢使用，再见！")
            break

        if not user_input:
            print("请输入内容哦！")
            continue

        # 将用户输入添加到对话历史
        conversation.append({
            "role": "user",
            "content": user_input
        })

        # 调用 API 获取响应
        print("AI 正在生成...")
        response = run_model(conversation)

        # 输出 AI 响应
        print(f"AI：{response}")

        # 将 AI 响应添加到对话历史，以便保持上下文
        conversation.append({
            "role": "assistant",
            "content": response
        })


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序已中断，感谢使用！")
        sys.exit(0)
