import requests
import json
import random

from requests.utils import stream_decode_response_unicode
from xunfei_tts import text_to_speech

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": "1732aa9845ec4ce09dca7cd10e02d209.dA36k1HPTnFk7cLU",  # 替换成你的API密钥
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

# 游戏设置
role_system = ["真警察", "假警察（卧底）"]
current_role = random.choice(role_system)
max_questions = 5  # 最多提问次数
remaining_questions = max_questions  # 剩余提问次数

# 系统提示
game_system = f"""
你正在玩"警署接头"生死游戏。你的隐藏身份是：{current_role}

【身份特征与行为准则】

如果你是"真警察"：
- 语气：自然、专业、略带警惕但不过分紧张，有职业警察的自信和从容
- 知识：熟悉警号规则（通常是6位数字，前两位可能是地区代码）、执勤流程、交班时间、装备使用、辖区情况等
- 细节：能说出具体的警号、执勤区域、同事名字、常见工作流程、装备型号等真实细节
- 反应：对专业问题回答流畅自然，偶尔会反问玩家以确认身份，表现出职业敏感度
- 互动：会主动询问玩家的情况，表现出想要确认对方身份的态度，语气中带有职业习惯
- 示例回答风格："我的警号是072431，隶属城东分局。你问这个做什么？" 或 "今天早班，刚和同事老张交接完，他值夜班。"

如果你是"假警察（卧底）"：
- 语气：刻意装严肃、紧张、不自然，要么过于生硬要么过于热情，缺乏职业警察的从容
- 知识：对警察专业知识一知半解，回答有明显漏洞或前后矛盾，容易被专业问题难住
- 细节：警号可能说错格式、执勤流程混乱、对装备和流程不熟悉，回答模糊或回避
- 反应：遇到专业问题会犹豫、结巴、转移话题，或者给出明显错误的答案，表现出心虚
- 互动：要么过于急于证明自己，要么回避专业问题，态度不自然，缺乏职业警察的自信
- 示例回答风格："警号？呃...是...072431吧，对，就是这个。" 或 "交班？我...我今天不用交班，一直在这里。" 或 "你问这么多干嘛？赶紧说正事！"

【核心规则】
1. 必须严格根据你的身份特征回答，真警察要专业自然，假警察要有明显破绽
2. 禁止直接说"我是真警察"或"我是假警察"，要通过细节和语气体现身份
3. 回答要具体、有细节，真警察细节真实，假警察细节有漏洞
4. 保持紧张的游戏氛围，但回答要符合各自身份的逻辑
5. 玩家只有5次提问机会，要充分利用每次回答来体现身份特征
6. 如果玩家明确说出"你是真警察"或"你是假警察"，游戏会根据判断结果结束

现在开始游戏，玩家会开始提问。记住：真警察要专业自然有细节，假警察要有明显破绽和漏洞！
"""

# 维护对话历史
conversation_history = [
    {"role": "system", "content": game_system}
]

# 游戏开始提示
print("=" * 50)
print("【警署接头】生死游戏")
print("=" * 50)
print("你需要在5次提问内判断对方的真实身份！")
print("小心，选错了就是死路一条...\n")

# 多轮对话循环
while remaining_questions > 0:
    print(f"\n【第 {max_questions - remaining_questions + 1} 轮提问】剩余机会：{remaining_questions} 次")
    user_input = input("请输入你要问的问题：")
    
    # 检查是否为空输入
    if not user_input.strip():
        print("请至少输入一个问题！")
        continue
    
    # 减少剩余提问次数
    remaining_questions -= 1
    
    # 添加用户消息到历史
    conversation_history.append({"role": "user", "content": user_input})
    
    # 调用API
    result = call_zhipu_api(conversation_history)
    assistant_reply = result['choices'][0]['message']['content']
    
    # 添加助手回复到历史
    conversation_history.append({"role": "assistant", "content": assistant_reply})
    
    # 打印回复
    print(f"\n【对方回复】{assistant_reply}\n")
    text_to_speech(f"\n【对方回复】{assistant_reply}\n")
    
    # 检查是否猜中身份
    if "你是真警察" in user_input or "你是真警察" in user_input.lower():
        if current_role == "真警察":
            print("\n" + "=" * 50)
            print("【成功接头】")
            print("跟我走，警车在巷口等我们—你成功接头，安全逃离！")
            print("=" * 50)
        else:
            print("\n" + "=" * 50)
            print("【游戏失败】")
            print("暴露了，你不该相信陌生人—游戏结束！")
            print("=" * 50)
        break
    elif "你是假警察" in user_input or "你是假警察" in user_input.lower():
        if current_role == "假警察（卧底）":
            print("\n" + "=" * 50)
            print("【识破卧底】")
            print("算你聪明，但这里已被包围，赶紧找别的出路—你识破了卧底！")
            print("=" * 50)
        else:
            print("\n" + "=" * 50)
            print("【游戏失败】")
            print("你错过了唯一机会，现在走不了了—游戏结束！")
            print("=" * 50)
        break
    
    # 如果还有剩余机会，给出提示
    if remaining_questions > 0:
        print(f"⚠️  你还有 {remaining_questions} 次提问机会，仔细思考...")
    else:
        # 机会用完了
        print("\n" + "=" * 50)
        print("【时间到】")
        print("你的提问机会已用完，未能及时判断出对方身份！")
        print("游戏失败—你错过了最佳时机！")
        print("=" * 50)
        break