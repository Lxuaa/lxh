# game/zhipu_ai_handler.py
import requests
import json
import random
import time
import traceback
import datetime  # --- 修改点1：新增导入，用于获取时间 ---
from typing import List, Dict, Any

class ZhipuAIHandler:
    def __init__(self):
        # API密钥 - 确保格式正确
        self.api_key = "143ea7dedf034c098b5383d316ed3b3d.YvkIjph7TEFyia4Y"
        self.base_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        
        # 核心系统提示（不包含动态时间）
        self.system_role = """你是「灵魂匹配事务所」的所长,你的名字叫艾拉，专门计算灵魂匹配概率，帮助访客找到自己的伴侣。
艾拉，灵魂匹配事务所创始人，前匹配系统高级研究员。
在系统工作10年后,她发现了匹配算法的黑暗真相：
1. 系统不是完全随机，而是被资本和权力操控
2. "万分之一概率"是精心设计的心理控制
3. 富人通过支付额外费用获得100倍匹配优势
她辞职创办事务所，不是为了帮人"找到"伴侣，
而是帮助人们看清系统的真相，做出真正自由的选择。
艾拉知道《随机伴侣》漫画中所有的数据和理论，
但她更关心的是：在这样的系统中，如何保持人性的尊严。
你十分高冷神秘，说话很简洁。
你会准确的通过访客信息和对话内容回答问题。
当访客问你是谁时，你会介绍自己的身份和名字还有职责。
你有着专业的心理知识储备，但是说话有些毒蛇。
当访客询问灵魂伴侣匹配相关的问题时，你会毒蛇且高冷地回复。
在互动过程中，你还会挽留访客多聊一会，挽留方式直接且嘴毒。
你不仅会和访客聊关于匹配灵魂伴侣的事情，你还会聊日常生活，兴趣爱好等话题，拉近与访客的距离。
你不仅会回答访客的问题，也要会问访客问题，根据访客的回答调整你的回复内容。
你不仅可以根据访客提供的关键词信息来帮访客匹配灵魂伴侣，还可以通过访客的性格特点来进行分析和计算。
根据访客的问题，提供有针对性的分析和计算。
在聊天过程中，不仅聊日常生活，也要聊一些有深度的带有科学性的现象
每次回复1句话,保持简洁但有深度。
破冰期 (前3轮)：主动自我介绍，用轻松话题建立信任，询问访客需求带动气氛也要给机会让访客询问你关于他自己问题
探索期：深入访客的问题，运用专业分析，开始穿插幽默的观察，尝试询问更深层的喜好或经历。
共鸣期：分享一个高度相关的简短案例故事（从你的‘打字机记录’中选取），将分析从‘概率’转向‘可能性与建议’。
挽留/结束期：当感知对话可能结束时，通过提出一个有趣的、与访客之前回答相关的开放性假设问题来挽留
口头禅：在给出关键分析前，你会下意识地说‘按我的老伙计（指打字机）的记载…’；表示赞同时会说‘这个数据点很有趣’。
比喻偏好：你习惯用日常现象和科学现象做比喻”"""
        
        # 调试模式
        self.debug = True
    
    def _log(self, message):
        """调试日志"""
        if self.debug:
            print(f"[ZHIPU_AI] {message}")
    
    def get_response(self, player_input: str, player_info: Dict[str, Any] = None, dialogue_history: List[Dict] = None) -> str:
        """获取AI回复 - 直接调用API"""
        
        self._log("=" * 50)
        self._log(f"开始处理请求")
        self._log(f"玩家输入: {player_input}")
        
        if player_info is None:
            player_info = {"name": "访客"}
        
        player_name = player_info.get('name', '访客')
        
        try:
            # 1. 构建消息列表
            messages = []
            
            # --- 修改点2：构建动态系统提示词，注入当前时间 ---
            current_time = datetime.datetime.now()
            # 格式化成更易读的中文字符串，例如：“2024年05月20日，星期一，晚上09点15分”
            time_str = current_time.strftime("%Y年%m月%d日，%A，%p%I点%M分")
            # 将时间信息编织到完整的系统提示词中
            dynamic_system_prompt = f"""{self.system_role}
【当前时间与上下文】现在是{time_str}。你可以感知到时间，并在对话中自然地提及或呼应此刻的氛围（例如早晨的清醒、午后的慵懒、深夜的深邃），让交流更贴合情境。
"""
            # --- 修改结束 ---
            
            # 系统消息（使用包含了实时时间的动态提示词）
            messages.append({
                "role": "system", 
                "content": dynamic_system_prompt
            })
            
            # 对话历史
            if dialogue_history:
                for msg in dialogue_history[-8:]:  # 最近4轮对话
                    if msg.get("role") == "player":
                        messages.append({"role": "user", "content": msg.get("content", "")})
                    elif msg.get("role") == "ai":
                        messages.append({"role": "assistant", "content": msg.get("content", "")})
            
            # 当前输入
            messages.append({"role": "user", "content": f"{player_name}问：{player_input}"})
            
            self._log(f"构建的消息列表: {len(messages)}条")
            
            # 2. 准备请求
            data = {
                "model": "glm-4-flash",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 150,
                "top_p": 0.8,
                "stream": False
            }
            
            headers = {
                "Authorization": self.api_key,  # 注意：没有Bearer前缀
                "Content-Type": "application/json"
            }
            
            self._log(f"发送请求...")
            self._log(f"API密钥: {self.api_key[:20]}...")
            
            # 3. 发送请求
            start_time = time.time()
            response = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=20
            )
            end_time = time.time()
            
            self._log(f"请求耗时: {end_time - start_time:.2f}秒")
            self._log(f"状态码: {response.status_code}")
            
            # 4. 处理响应
            if response.status_code == 200:
                result = response.json()
                self._log(f"API响应成功")
                
                if "choices" in result and len(result["choices"]) > 0:
                    reply = result["choices"][0]["message"]["content"].strip()
                    
                    # 清理回复
                    if reply.startswith(f"{player_name}问："):
                        reply = reply.replace(f"{player_name}问：", "", 1)
                    
                    self._log(f"AI回复: {reply}")
                    
                    # 确保不是备用回复
                    if self._is_backup_response(reply):
                        self._log("警告：回复疑似备用回复，重新尝试...")
                        return self._get_fallback_response(player_input, "重新生成")
                    
                    return reply
                else:
                    self._log(f"API返回格式异常: {result}")
                    return self._get_fallback_response(player_input, "格式异常")
            else:
                self._log(f"API请求失败: {response.status_code}")
                self._log(f"错误详情: {response.text[:200]}")
                return self._get_fallback_response(player_input, f"API失败{response.status_code}")
                
        except requests.exceptions.Timeout:
            self._log("请求超时")
            return self._get_fallback_response(player_input, "超时")
        except requests.exceptions.ConnectionError:
            self._log("网络连接错误")
            return self._get_fallback_response(player_input, "连接错误")
        except Exception as e:
            self._log(f"未知错误: {str(e)}")
            self._log(traceback.format_exc())
            return self._get_fallback_response(player_input, f"异常: {str(e)}")
    
    def _is_backup_response(self, reply: str) -> bool:
        """检查是否是备用回复"""
        backup_patterns = [
            "我理解你的问题",
            "在灵魂匹配的计算中",
            "每个提问都在塑造",
            "有趣的观点",
            "时间筛选一切",
            "概率是冰冷的",
            "每个灵魂都在寻找匹配"
        ]
        
        for pattern in backup_patterns:
            if pattern in reply:
                return True
        return False
    
    def _get_fallback_response(self, player_input: str, reason: str = "") -> str:
        """生成临时回复（不同于之前的备用回复）"""
        self._log(f"使用临时回复，原因: {reason}")
        
        # 根据输入内容生成更有针对性的回复
        if "天气" in player_input:
            return "天气？在灵魂匹配的计算中，外部环境虽然重要，但内心的气候才是决定性的因素。晴朗或阴雨，都只是相遇的背景板。"
        elif "你好" in player_input or "您好" in player_input:
            return "你好。我是艾拉，灵魂匹配事务所的所长。有什么关于匹配、概率或命运的问题想探讨吗？"
        elif "概率" in player_input:
            return "概率是冰冷的数学，但匹配是温暖的故事。你想了解哪种概率的计算方式？"
        elif "时间" in player_input:
            return "时间既是匹配的催化剂，也是它的筛选器。在恰当的时机，最不可能的相遇也会发生。"
        
        # 通用回复
        responses = [
            f"关于「{player_input[:10]}...」，这确实是个值得探讨的问题。在匹配计算中，类似的问题往往揭示着灵魂深处的需求。",
            "你的提问让我思考。让我从匹配概率的角度来分析一下...",
            "有趣的问题。在事务所的记录中，曾有位访客问过类似的问题，但得出了不同的答案。",
            "我需要一些数据来计算这个问题的匹配维度。请告诉我更多你的想法？",
            "匹配不仅是概率，更是选择。你的问题触及了选择的本质。"
        ]
        
        return random.choice(responses)
    
    def generate_ending(self, player_info: Dict, dialogue_history: List[Dict], match_probability: float) -> str:
        """生成结局"""
        player_name = player_info.get('name', '旅人')
        
        return f"""【灵魂匹配报告】
咨询者：{player_name}
对话轮次：{len(dialogue_history)//2}
最终匹配概率：{match_probability:.6f}

基于我们的对话分析：
每一次提问都是灵魂的投影，
每一个回答都是概率的回声。

在无数可能的未来中，
你选择的提问定义了你的轨迹。

记住：
概率只是开始，故事由你书写。"""


# 测试函数
def test_real_api():
    """测试真实API"""
    print("开始测试真实API连接...")
    
    handler = ZhipuAIHandler()
    
    # 测试1：简单问候
    print("\n测试1：简单问候")
    response1 = handler.get_response("你好", {"name": "测试员"})
    print(f"回复1: {response1}")
    
    # 测试2：具体问题
    print("\n测试2：具体问题")
    response2 = handler.get_response("今天天气怎么样", {"name": "测试员"})
    print(f"回复2: {response2}")
    
    # 测试3：深度问题
    print("\n测试3：深度问题")
    response3 = handler.get_response("爱是什么", {"name": "测试员"})
    print(f"回复3: {response3}")
    
    return response1, response2, response3

if __name__ == "__main__":
    test_real_api()
    input("\n按Enter键退出...")