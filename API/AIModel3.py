from openai import OpenAI

# 初始化客户端
client = OpenAI(api_key="sk-f0a368779df94a55a05371e138f7ce43", base_url="https://api.deepseek.com/v1")


def chat_with_deepseek():
    print("欢迎使用DeepSeek聊天助手！输入消息开始对话，输入 'exit' 退出。")

    while True:
        # 获取用户输入
        user_input = input("你: ")

        # 检查是否退出
        if user_input.lower() == "exit":
            print("再见！")
            break

        # 调用API
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": user_input},
            ],
            stream=False
        )

        # 输出响应
        print("助手:", response.choices[0].message.content)


if __name__ == "__main__":
    chat_with_deepseek()