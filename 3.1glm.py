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
import random

# 角色定义
roles = {
    "清洁工": "你是一家面包店里的清洁工，是一个老实人，你昨晚请假了，没看到谁进了收银台",
    "面包师": "你是这家面包店里的面包师，真凶，不会说真话，你会狡辩一直在做糕点，根本没空去收银台",
    "门卫": "你是这家面包店的门卫，细心且正直，会说真话，一直在守门，你昨晚看到了面包师去了收银台拿走了钱"
}

game_system = "当我想问一个角色时，你必须要扮演这个角色，并且符合他的身份和特点。这是一个抓真凶游戏，你可以问角色问题，或输入角色名指认真凶。当我抓到面包师为真凶时，游戏结束。"

print("=== 猜真凶游戏 ===")
print("角色：清洁工、面包师、门卫")
print("你可以：1. 输入角色名+问题（如：面包师 你昨晚在做什么？）")
print("       2. 直接指认真凶（如：面包师是真凶）")
print("-" * 40)

while True:  # 表示"当条件为真时一直循环"。由于 True 永远为真，这个循环会一直运行，直到遇到 break 才会停止。
    user_input = input("\n请输入你要说的话：").strip()
    
    # 检查是否指认真凶
    if "面包师" in user_input and "真凶" in user_input:
        print("恭喜！你找到真凶了，游戏结束！")
        break
    
    # 解析用户输入，提取角色名和问题
    role_name = None
    question = user_input
    
    for role in roles.keys():
        if user_input.startswith(role):
            role_name = role
            question = user_input[len(role):].strip()
            break
    
    # 如果没有指定角色，随机选择一个
    if role_name is None:
        role_name = random.choice(list(roles.keys()))
        print(f"（随机选择角色：{role_name}）")
    
    # 构建消息
    role_prompt = roles[role_name]
    full_prompt = f"{game_system}\n\n{role_prompt}\n\n玩家的问题：{question}"
    
    messages = [
        {"role": "system", "content": game_system},
        {"role": "user", "content": f"{role_prompt}\n\n玩家的问题：{question}"}
    ]
    
    try:
        result = call_zhipu_api(messages)
        assistant_reply = result['choices'][0]['message']['content']
        print(f"\n[{role_name}]：{assistant_reply}")
    except Exception as e:
        print(f"错误：{e}")
    
    
    