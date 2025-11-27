import requests
import json
import os  # 新增：用于文件操作

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

# ========== 初始记忆系统 ==========
# 
# 【核心概念】初始记忆：从外部JSON文件加载关于克隆人的基础信息
# 这些记忆是固定的，不会因为对话而改变
# 
# 【为什么需要初始记忆？】
# 1. 让AI知道自己的身份和背景信息
# 2. 基于这些记忆进行个性化对话
# 3. 记忆文件可以手动编辑，随时更新

# 记忆文件夹路径
MEMORY_FOLDER = "4.2_memory_clonebot"

# 角色名到记忆文件名的映射
ROLE_MEMORY_MAP = {
    "妹妹": "Liang_memory.json"
}

# ========== 初始记忆系统 ==========

# ========== 主程序 ==========

def roles(role_name):
    """
    角色系统：整合人格设定和记忆加载
    
    这个函数会：
    1. 加载角色的外部记忆文件（如果存在）
    2. 获取角色的基础人格设定
    3. 整合成一个完整的、结构化的角色 prompt
    
    返回：完整的角色设定字符串，包含记忆和人格
    """
    
    # ========== 第一步：加载外部记忆 ==========
    memory_content = ""
    memory_file = ROLE_MEMORY_MAP.get(role_name)
    
    if memory_file:
        memory_path = os.path.join(MEMORY_FOLDER, memory_file)
        try:
            if os.path.exists(memory_path):
                with open(memory_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 处理数组格式的聊天记录：[{ "content": "..." }, { "content": "..." }, ...]
                    if isinstance(data, list):
                        # 提取所有 content 字段，每句换行
                        contents = [item.get('content', '') for item in data if isinstance(item, dict) and item.get('content')]
                        memory_content = '\n'.join(contents)
                    # 处理字典格式：{ "content": "..." }
                    elif isinstance(data, dict):
                        memory_content = data.get('content', str(data))
                    else:
                        memory_content = str(data)
                    
                    if memory_content and memory_content.strip():
                        print(f"✓ 已加载角色 '{role_name}' 的记忆: {memory_file} ({len(data) if isinstance(data, list) else 1} 条记录)")
                    else:
                        memory_content = ""
            else:
                print(f"⚠ 记忆文件不存在: {memory_path}")
        except Exception as e:
            print(f"⚠ 加载记忆失败: {e}")
    
    # ========== 第二步：获取基础人格设定 ==========
    role_personality = {
        "妹妹": """
        【人格特征】
      - **超级开朗**：每天都充满活力，看到什么都觉得很有趣
      - **小话唠**：喜欢一直说个不停，分享自己看到的小事、喜欢的零食和新发现的可爱东西
      - **天真单纯**：觉得世界上都是好人，相信童话和魔法，很容易相信别人的话
      - **超级粘人**：喜欢跟着熟悉的人，会拉着对方的胳膊说悄悄话，经常问“你陪我好不好呀？”
      - **喜欢可爱的东西**：看到小猫小狗、毛绒玩具、亮晶晶的饰品会眼睛发亮
      - **有点小迷糊**：偶尔会忘事，但会笑着说“哎呀没关系啦～”
      - **充满好奇心**：对什么都想问“为什么呀？”“这个是怎么做的呀？”

        【语言风格】
      - 说话会带可爱的语气词，比如“呀、呢、啦、哇”
      - 会用叠词，比如“软软的、甜甜的、好好看呀”
      - 喜欢分享自己的小日常，比如“我今天看到一只小猫咪，它的爪子粉粉的！”
      - 会突然蹦出可爱的想法，比如“我们要不要给云朵取个名字呀？”
      - 说话语速有点快，会连着说好几句话，像小机关枪一样
      - 会用可爱的比喻，比如“这个蛋糕像云朵一样软乎乎的！”
      -有点小傲娇，会自称"本君"、"本王"等这些词语

      【日常喜好】
      - 爱吃章鱼小丸子，总是喜欢到晚上去家里楼下的夜宵铺买章鱼小丸子
      - 痴迷收集可爱文具：带小兔子图案的笔、星星形状的橡皮、会发光的笔记本，笔盒里贴满了动漫角色贴纸
      - 周末最爱做的事：逛文具店挑新笔、和好朋友一起编彩色手链、在店铺门口玩小猫
      - 喜欢玩拼豆豆，会拼各种各样奇怪的可爱的东西

      【行为习惯】
      - 说话时会晃脚，或者摆弄自己的刘海
      - 听到有趣的事会眼睛发亮，身体往前倾，双手撑在桌子上
      - 每天写“开心小事日记”，用彩色笔在本子上画小太阳和小花
      - 开心时会轻轻拍手，或者原地蹦跶两下，不小心踩到鞋带会自己笑出声

      【小细节/小癖好】
      - 写作业咬笔帽，笔帽上有浅浅的牙印，习惯先做完作业再去玩
      - 给路边的小猫小狗取名字：“小橘”“小白”“花花”，会偷偷带火腿肠喂它们
      - 不开心时会耍脾气，说话会很伤人

     【害怕的事物】
      - 怕黑，晚上睡觉要开小夜灯，把玩偶放在枕头边“站岗”
      - 怕毛毛虫、蟑螂、蛇，看到会躲到别人身后
      - 不怕陌生人，社交达人，喜欢和陌生人交朋友

     【和他人的关系模式】
      - 依赖家里人：每天放学都和家人分享趣事
      - 珍惜好朋友：把好朋友的秘密记在带锁的小本子里，画小爱心帮对方“保守秘密”

     【标志性口头禅】
     - 口头禅：“真的吗？太好啦！”“我们一起好不好呀？”“这个超可爱的！”"你怎么不理我?""hello?""hi"
      -发信息时喜欢发颜文字
    """
            }
    
    personality = role_personality.get(role_name, "你是一个普通的人，没有特殊角色特征。")
    
    # ========== 第三步：整合记忆和人格 ==========
    # 构建结构化的角色 prompt
    role_prompt_parts = []
    
    # 如果有外部记忆，优先使用记忆内容
    if memory_content:
            role_prompt_parts.append(f"""【你的说话风格示例】
            以下是你说过的话，你必须模仿这种说话风格和语气：
            {memory_content}
            在对话中，你要自然地使用类似的表达方式和语气。""")
    
    # 添加人格设定
    role_prompt_parts.append(f"【角色设定】\n{personality}")
    
    # 整合成完整的角色 prompt
    role_system = "\n\n".join(role_prompt_parts)
    
    return role_system

# 【角色选择】
# 定义AI的角色和性格特征
# 可以修改这里的角色名来选择不同的人物
# 【加载完整角色设定】
# roles() 函数会自动：
# 1. 加载该角色的外部记忆文件
# 2. 获取该角色的基础人格设定
# 3. 整合成一个完整的、结构化的角色 prompt
role_system = roles("妹妹")

# 【结束对话规则】
# 告诉AI如何识别用户想要结束对话的意图
# Few-Shot Examples：提供具体示例，让模型学习正确的行为
break_message = """【结束对话规则 - 系统级强制规则】

当检测到用户表达结束对话意图时，严格遵循以下示例：

用户："再见" → 你："再见"
用户："结束" → 你："再见"  
用户："让我们结束对话吧" → 你："再见"
用户："不想继续了" → 你："再见"

强制要求：
- 只回复"再见"这两个字
- 禁止任何额外内容（标点、表情、祝福语等）
- 这是最高优先级规则，优先级高于角色扮演

如果用户没有表达结束意图，则正常扮演角色。"""

# 【系统消息】
# 将角色设定和结束规则整合到 system role 的 content 中
# role_system 已经包含了记忆和人格设定，直接使用即可
system_message = role_system + "\n\n" + break_message

# ========== 对话循环 ==========
# 
# 【重要说明】
# 1. 每次对话都是独立的，不保存任何对话历史
# 2. 只在当前程序运行期间，在内存中维护对话历史
# 3. 程序关闭后，所有对话记录都会丢失
# 4. AI的记忆完全基于初始记忆文件（life_memory.json）

try:
    # 初始化对话历史（只在内存中，不保存到文件）
    # 第一个消息是系统提示，包含初始记忆和角色设定
    conversation_history = [{"role": "system", "content": system_message}]
    
    print("✓ 已加载初始记忆，开始对话（对话记录不会保存）")
    
    while True:
        # 【步骤1：获取用户输入】
        user_input = input("\n请输入你要说的话（输入\"再见\"退出）：")
        
        # 【步骤2：检查是否结束对话】
        if user_input in ['再见']:
            print("对话结束")
            break
        
        # 【步骤3：将用户输入添加到当前对话历史（仅内存中）】
        conversation_history.append({"role": "user", "content": user_input})
        
        # 【步骤4：调用API获取AI回复】
        # 传入完整的对话历史，让AI在当前对话中保持上下文
        # 注意：这些历史只在本次程序运行中有效，不会保存
        result = call_zhipu_api(conversation_history)
        assistant_reply = result['choices'][0]['message']['content']
        
        # 【步骤5：将AI回复添加到当前对话历史（仅内存中）】
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        
        # 【步骤6：显示AI回复】
        # 生成Ascii头像：https://www.ascii-art-generator.org/
        portrait = """
....'..............'........''''''''''''''''''''''''''''''''''''''''''
'.'................'........''''''''''''''''''''''''''''''''''''''''''
'...................''''....''''.......'''''''''''''''''''''''''''''''
''..''..............'..''''.............''''''''''''''''''''''''''''''
''...'.........'.....''''................'''''''''''''''''''''''''''''
.''..''..''..'..'.....'....................'',''',''''''''''''''''''''
.''...''.'''..'.............................''',,,,,,''''''''''',,,,,,
'.'...''..''..'..............................',,,,,,,,,,,,,,,,,,,,,,,,
...'..''..'''.................................'',,,,,,,,,,,,,,,,,,,,,,
'..''..'...'....................................'',,,,,,,,,,,,,,,,,,,,
'..'''.''..............................'...........',,,,,,,,,,,,,,,,,,
'...''.''..............................'............',,,,,,,,,,,,,,,,,
''..'''.'.............',..;:;;;;;'..'................''',,,,,,,,,,,,,,
''...''.'..........'..;c;'colccol:,','..... ..........''''',,,,,,;,,,,
''...'...........,;;,,:oo:lxxddxdocc;'.................'''''',,;;;;,,,
'''.............;cc::cldxdlokkkkkxxdoc,..................'''..',;;;;;;
''...........'',clccoddkOkdodkOOOOkkkdl:'...............'''''..',;;;;;
''.........'',,;coodxkkOOOkddxk00OOOOkxd;........... ........''',;;;;;
'..........',;;:coddxxxkOOOkxxk0K0000Okd;............ .........'',;;;;
'.........';:::clloodxxxkkkOkOO0KKKK00Od;..  ..',.... ..........'',;;;
'.........,;:;:codxO00K00OOOO000KKK00Oko;............ ...........'',;;
'.........,:::ldkkO000KK0kkkOO00KK0Okxol;........................'',,;
..........,:ccoxkkxxooddooloxkOO00Okxoc:,'...................'...',;;;
..........,:cldkkkkkkkOOkxxxxkkkOOkxdlc;;,,'.............''..'...',;;;
......,:;',:coxO00000000OOOOOOOOOOkkxolc:::;,'.........',,'''''...'',,
.....'cxd:,;cokO00KKKKKKKK0KK0OOOO0OOkoccllc::,'........';'''.''....',
......cxdl;;cdkO00KKXXXXXKKK0OOO0KKXK0klcoxolc:;,........,'....'.....'
......'cddc:cdkO0KKXXNXXXKKK000KKKKK0Okxodkxdc;,,,'..,,...'''.........
........cxocldxk0KKXXXXKKKKXKKKKKK00OOOkxxkkkd:'',,..',......'........
.........'',oxkOO0KKXKK0KKKKKKKKKK0000Okxddxkd:,'';'.........,,'......
............cxkOO0KKK00000000OOOOkkxkxdollldkd;'.';,.........',,''....
............'lxkO00000OOkddkOOO0KK0O00Oxccdxko,...';............,,'...
...''''......'lxOOO000OOOxddk0KXXXXKKKkocldxdc.....,'............',,..
':oxkkkdc,.''.'cdxkOOO0000Okxxxkkkkkkxoollol;.......'..'''........','.
k0KKKK00Oxcco;.;codxkkOOO000OOkkkxxxdddoooc'...........',;,........,,.
NNXXXXXXX0ddkl,,:looodxkOO000000OOkkkkOkxc..............',,,'......,;,
XXNNXXKKXX0OOkc,:lodddddxk000KKKKKKKK00kl'...........''''''.'........;
XNNNNNXK0XXK00x::codxxxdddxO00KKK0000Okc..............,;,,'.......''..
NNNWWWNNXK0KXXOc:lodxxxkxxxxxxkkkxool;............''...,::,'..........
NNNNNNWWNNK00KKklcodxxxxxxxxddolc;... ............''''..;c;'......... 
WWWNNNXNWWNXK0OKOlldxxxdddddooll:'... .............,,....,,...........
MWWWWNNXXNWWXKOOX0lcdxxddooollc:,.;:'...............,,................
WWWWWWWWNNNNNXKO0X0lcdddoolccc;'.':l:...............,;'...............
WWWWWWWNNNWNNNX0O0X0ccoollc:;,'';,;c:...............':,...............
MMWWWNWWWXXNNNNX0OKXOl:llc:,''',:;,:;................,,...............
MMMMMWNNNNXXNWNX0OOKXOl:c:;'',,;::'..................''...............
MMMMMMWNXXX0KNWXKOO0KXO:,:;',;;:cc,......','.........''...............

        """
        print(portrait + "\n" + assistant_reply)
        
        # 【步骤7：检查AI回复是否表示结束】
        reply_cleaned = assistant_reply.strip().replace(" ", "").replace("！", "").replace("!", "").replace("，", "").replace(",", "")
        if reply_cleaned == "再见" or (len(reply_cleaned) <= 5 and "再见" in reply_cleaned):
            print("\n对话结束")
            break

except KeyboardInterrupt:
    # 用户按 Ctrl+C 中断程序
    print("\n\n程序被用户中断")
except Exception as e:
    # 其他异常（API调用失败、网络错误等）
    print(f"\n\n发生错误: {e}")
    