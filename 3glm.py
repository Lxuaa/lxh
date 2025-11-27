import requests
import json

from requests.utils import stream_decode_response_unicode

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "1732aa9845ec4ce09dca7cd10e02d209.dA36k1HPTnFk7cLU",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.5   
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

# 使用示例
while True:
    user_input = input("请输入你要说的话：")
    role_system = "你要全程扮演一个冷酷的犯罪者，说话简短、带点不耐烦，只要我提到‘结束、不想聊了’这类话，你就回复‘再见’"
    messages = [
        {"role": "system", "content": role_system},
        {"role": "user", "content": user_input}
    ]
    result = call_zhipu_api(messages)
    print(result['choices'][0]['message']['content'])
    if result  == "再见":
        print("对话结束。")
        break