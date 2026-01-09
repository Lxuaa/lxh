define g = "fonts/gete.ttf"
define x = "fonts/xiangsu.ttf"

# 自定义主菜单
screen main_menu():
    add "images/background.png" zoom 1.1
    text "灵魂匹配事务所" xcenter 0.3 ypos 60:
        size 100
        color "#ffffff"
        bold False
        font x
        
    text "Soul Matching Office" xcenter 0.3 ypos 170:
        size 70
        color "#f9ebff"
        bold False
        font x

    # 开始游戏按钮
    button xcenter 0.2 ypos 300 action Start():
        background "#351c60"
        hover_background "#05002f"
        padding (40, 15)
        text "开启匹配伴侣":
            size 40
            color "#ffffff"
            hover_color "#ffffff"
            font x

    # 读取存档按钮
    button xcenter 0.2 ypos 400 action ShowMenu("load"):
        background "#351c60"
        hover_background "#05002f"
        padding (40, 15)
        text "读取过往契约":
            size 40
            color "#ffffff"
            hover_color "#ffffff"
            font x

    # 设置按钮
    button xcenter 0.185 ypos 500 action ShowMenu("preferences"):
        background "#351c60"
        hover_background "#05002f"
        padding (40, 15)
        text "事务所设置":
            size 40
            color "#ffffff"
            hover_color "#ffffff"
            font x

    # 退出按钮
    button xcenter 0.185 ypos 600 action Quit(confirm=False):
        background "#351c60"
        hover_background "#05002f"
        padding (40, 15)
        text "离开事务所":
            size 40
            color "#ffffff"
            hover_color "#ffffff"
            font x

image office:
    "images/office.png"
    zoom 0.5

# 所长立绘
image ai_character:
    "images/Person1.PNG"
    zoom 0.35
    xanchor 0.4
    yanchor 1
    yoffset 100 
    xoffset 70

image bg_broken_clock:
    "images/broken_clock.png"
    zoom 0.24
image bg_ghost_love:
    "images/ghost_love.png"
    zoom 0.24
image bg_graveyard:
    "images/graveyard.png"
    zoom 0.24
image bg_money_timeline:
    "images/money_timeline.png"
    zoom 0.24
image bg_future_city:
    "images/future_city.png"
    zoom 0.24
image bg_golden_match:
    "images/golden_match.png"
    zoom 0.24
image bg_times_square_police:
    "images/times_square_police.png"
    zoom 0.24
image bg_supermarket_miracle:
    "images/supermarket_miracle.png"
    zoom 0.24
image bg_burning_system:
    "images/burning_system.png"
    zoom 0.24
image bg_empty_universe:
    "images/empty_universe.png"
    zoom 0.24
image bg_exhausted_police:
    "images/exhausted_police.png"
    zoom 0.24
image bg_poor_despair:
    "images/poor_despair.png"
    zoom 0.24
image bg_perfect_mask:
    "images/perfect_mask.png"
    zoom 0.24
image bg_endless_road:
    "images/endless_road.png"
    zoom 0.24
image bg_dream_butterfly:
    "images/dream_butterfly.png"
    zoom 0.24
image bg_quantum_entanglement:
    "images/quantum_entanglement.png"
    zoom 0.24

image workingroom:
    "images/working room.jpeg"
    zoom 0.5

image way:
    "images/ways.jpeg"
    zoom 0.5

image peopleindoor:
    "images/people in door.jpeg"
    zoom 0.5

image opendoor:
    "images/open door.jpeg"
    zoom 0.5

image opendoor:
    "images/open door.jpeg"
    zoom 0.5

image ai:
    "images/AI in room.jpeg"
    zoom 0.5

image taking:
    "images/taking.jpeg"
    zoom 0.5

image withpeople:
    "images/with people.jpeg"
    zoom 0.5

image table:
    "images/working table.jpeg"
    zoom 0.5

image touch:
    "images/touch.jpeg"
    zoom 0.5

image light:
    "images/light.jpeg"
    zoom 0.5

image morepeople:
    "images/more people.jpeg"
    zoom 0.5
# ====================== 全局变量 ======================
default player_name = "亚当"
default player_age = "20"
default player_gender = "男"
default player_orientation = "双向"
default player_age_gap = "5"
default input_error = ""

# AI对话相关变量
default dialogue_history = []
default current_input = ""
default dialogue_round = 0
default match_probability = 0.0001
default show_story = False
default story_text = ""
default ai_ready = False

# 新增变量
default min_dialogue_rounds = 5
default dialogue_count = 0
default keywords_triggered = {}

default soulmate_status = "unknown"  # 灵魂伴侣状态：unknown, dead, unborn, alive, found
default meeting_chance = 0.0001      # 相遇概率，从0.0001开始
default years_searching = 0           # 寻找年数
default search_method = "passive"    # 寻找方法：passive, active, career, network, tech
default social_class = "middle"      # 社会阶级：poor, middle, rich
default philosophical_view = "realist" # 哲学观点：realist, romantic, nihilist, rebel
default unique_phrases_used = []      # 使用的独特短语
default special_trigger = None        # 特殊触发条件

# ====================== 对话分析函数 ======================
init python:
    def analyze_dialogue_for_ending():
        """分析对话内容，为结局触发做准备"""
        global search_method, philosophical_view, social_class, unique_phrases_used, years_searching
        
        # 分析所有玩家对话
        all_player_text = " ".join([msg["content"] for msg in dialogue_history if msg["role"] == "player"])
        
        # 分析寻找方法
        if any(word in all_player_text for word in ["科技", "系统", "轮盘", "传送带", "算法"]):
            search_method = "tech"
        elif any(word in all_player_text for word in ["工作", "职业", "警察", "收银", "导游"]):
            search_method = "career"
        elif any(word in all_player_text for word in ["主动", "寻找", "搜索", "努力"]):
            search_method = "active"
        elif any(word in all_player_text for word in ["朋友", "介绍", "社交", "网络"]):
            search_method = "network"
        
        # 分析哲学观点
        if any(word in all_player_text for word in ["反抗", "推翻", "不公平", "革命"]):
            philosophical_view = "rebel"
        elif any(word in all_player_text for word in ["浪漫", "真爱", "命运", "注定"]):
            philosophical_view = "romantic"
        elif any(word in all_player_text for word in ["无意义", "虚无", "化学", "幻觉"]):
            philosophical_view = "nihilist"
        elif any(word in all_player_text for word in ["现实", "妥协", "接受", "差不多"]):
            philosophical_view = "realist"
        
        # 分析社会阶级暗示
        if any(word in all_player_text for word in ["富人", "有钱", "VIP", "特权", "昂贵"]):
            social_class = "rich"
        elif any(word in all_player_text for word in ["穷人", "贫困", "底层", "没钱", "廉价"]):
            social_class = "poor"
        
        # 分析独特短语（彩蛋触发）
        special_phrases = {
            "银河系漫游指南": "hitchhiker_egg",
            "庄周梦蝶": "dream_egg",
            "薛定谔": "quantum_egg"
        }
        
        for phrase, egg_type in special_phrases.items():
            if phrase in all_player_text and egg_type not in unique_phrases_used:
                unique_phrases_used.append(egg_type)
        
        # 估算寻找年数（基于对话轮次）
        years_searching = dialogue_count // 5
        
        # 计算相遇概率（基于漫画逻辑）
        global meeting_chance
        base_chance = 0.0001
        
        # 方法加成
        method_multiplier = {
            "passive": 0.5,
            "active": 2,
            "network": 3,
            "career": 5,
            "tech": 8
        }.get(search_method, 1)
        
        # 阶级加成
        class_multiplier = {
            "poor": 0.3,
            "middle": 1,
            "rich": 3
        }.get(social_class, 1)
        
        # 时间加成
        time_multiplier = min(1 + (years_searching / 20), 5)
        
        meeting_chance = base_chance * method_multiplier * class_multiplier * time_multiplier
        meeting_chance = min(meeting_chance, 0.01)  # 最大1%，符合漫画
    
    def determine_ending_type():
        """确定触发哪个结局"""
        global soulmate_status, special_trigger
        
        # 1. 先检查彩蛋触发
        if len(unique_phrases_used) >= 2:
            special_trigger = "double_egg"
            return "double_egg"
        elif "hitchhiker_egg" in unique_phrases_used:
            special_trigger = "hitchhiker_egg"
            return "hitchhiker_ending"
        elif "dream_egg" in unique_phrases_used:
            special_trigger = "dream_egg"
            return "dream_ending"
        elif "quantum_egg" in unique_phrases_used:
            special_trigger = "quantum_egg"
            return "quantum_ending"
        elif "math_egg" in unique_phrases_used:
            special_trigger = "math_egg"
            return "math_ending"
        
        # 2. 确定灵魂伴侣状态（基于漫画数据）
        import random
        rand = random.random()
        
        if rand < 0.93:  # 93%已去世
            soulmate_status = "dead"
        elif rand < 0.96:  # 3%未出生
            soulmate_status = "unborn"
        else:  # 4%活着
            soulmate_status = "alive"
        
        # 3. 如果伴侣活着，检查是否找到
        if soulmate_status == "alive":
            if random.random() < meeting_chance:
                soulmate_status = "found"
        
        # 4. 基于状态和玩家特征确定具体结局
        if soulmate_status == "dead":
            if philosophical_view == "rebel":
                return "time_rebel_ending"
            elif philosophical_view == "romantic":
                return "ghost_love_ending"
            else:
                return "soulmate_dead_ending"
        
        elif soulmate_status == "unborn":
            if philosophical_view == "nihilist":
                return "paradox_acceptance_ending"
            elif social_class == "rich":
                return "future_investor_ending"
            else:
                return "soulmate_unborn_ending"
        
        elif soulmate_status == "found":
            if social_class == "rich":
                return "rich_success_ending"
            elif search_method == "career":
                return "career_success_ending"
            else:
                return "miracle_found_ending"
        
        else:  # alive but not found
            if philosophical_view == "rebel":
                return "system_rebel_ending"
            elif philosophical_view == "nihilist":
                return "nihilist_acceptance_ending"
            elif search_method == "career":
                return "career_tragedy_ending"
            elif social_class == "poor":
                return "poor_desperation_ending"
            elif philosophical_view == "realist":
                return "realistic_compromise_ending"
            else:
                return "eternal_search_ending"
# ====================== 关键词回复字典 ======================
init python:
    # 定义关键词回复
    keyword_responses = {
        "概率": [
            "概率是灵魂相遇的数学表达。每个数字背后，都藏着无数可能的故事。",
            "在我们事务所，概率从不撒谎。它只是诚实地展示现实的残酷与美好。",
            "你问概率？有趣。大多数人害怕知道真相。"
        ],
        "时间": [
            "时间是最公正的筛选者。它会让错误的匹配消散，让正确的相遇沉淀。",
            "在时间的长河中，五年只是一瞬。但对于匹配来说，可能是永恒的距离。",
            "过早或过晚，都是时间的玩笑。"
        ],
        "孤独": [
            "孤独不是缺陷，而是灵魂的留白，等待被另一个灵魂填满。",
            "我见过太多人在孤独中迷失，又在匹配中找到自己。",
            "孤独与匹配，是一枚硬币的两面。"
        ],
        "命运": [
            "命运不是写好的剧本，而是无数选择交织成的网。",
            "相信命运的人，往往更愿意接受匹配的结果。",
            "命运让我们相遇，但选择让我们停留。"
        ],
        "爱": [
            "爱是匹配的最高形式，但也最难以计算。",
            "有人用一生寻找爱，有人在一瞬间找到。概率从不关心这些。",
            "爱让概率失去意义，却又让匹配成为必然。"
        ],
        "未来": [
            "未来是未书写的匹配记录。每一次选择都在改变它的轨迹。",
            "人们总是害怕未来的不确定性，却忘了不确定性正是希望所在。",
            "你的未来，由今天的提问开始塑造。"
        ]
    }

# ====================== AI初始化 ======================
init python:
    import json
    import random
    import sys
    import os
    
    print("=" * 50)
    print("初始化AI处理器...")
    
    # 尝试导入AI处理器
    ai_handler = None
    
    try:
        # 尝试导入zhipu_ai_handler
        from zhipu_ai_handler import ZhipuAIHandler
        
        print("✅ 成功导入 ZhipuAIHandler")
        
        # 创建处理器实例
        ai_handler = ZhipuAIHandler()
        print("✅ AI处理器实例创建成功")
        
        # 立即测试API
        print("立即测试API连接...")
        test_reply = ai_handler.get_response("测试连接", {"name": "系统测试"})
        print(f"✅ API测试回复: {test_reply[:50]}...")
        
        # 确认不是备用回复
        if "测试连接" in test_reply or len(test_reply) < 10:
            print("⚠️ 回复可能来自备用库，但API连接成功")
        else:
            print("✅ 确认使用真实AI回复")
            
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("尝试添加路径...")
        
        # 尝试添加当前目录到路径
        game_dir = os.path.join(config.basedir, "game")
        if game_dir not in sys.path:
            sys.path.append(game_dir)
        
        try:
            from zhipu_ai_handler import ZhipuAIHandler
            ai_handler = ZhipuAIHandler()
            print("✅ 通过路径修复成功导入")
        except ImportError as e2:
            print(f"❌ 路径修复后仍然导入失败: {e2}")
            print("⚠️ 使用模拟处理器")
            
            class MockAIHandler:
                def __init__(self):
                    print("创建模拟AI处理器")
                    self.count = 0
                
                def get_response(self, player_input, player_info, dialogue_history=None):
                    self.count += 1
                    return f"[模拟AI第{self.count}次回复] 关于「{player_input}」，这个问题需要真实的AI来回答。"
                
                def generate_ending(self, *args, **kwargs):
                    return "【模拟结局】AI连接失败，请检查API设置"
            
            ai_handler = MockAIHandler()
    except Exception as e:
        print(f"❌ 初始化AI处理器时出错: {e}")
        import traceback
        traceback.print_exc()
        
        # 紧急备用
        class EmergencyAIHandler:
            def get_response(self, player_input, *args, **kwargs):
                return f"[紧急回复] AI系统初始化失败，请检查设置"
            def generate_ending(self, *args, **kwargs):
                return "【紧急结局】系统错误"
        
        ai_handler = EmergencyAIHandler()
    
    print(f"✅ AI处理器最终状态: {type(ai_handler).__name__}")
    print("=" * 50)
# ====================== 对话处理函数 ======================
# 在 script.rpy 中找到 init python: 部分，修改为以下内容：

init python:
    import json
    import random
    
    # 尝试导入AI处理器
    ai_handler = None
    
    try:
        # 尝试导入zhipu_ai_handler
        from zhipu_ai_handler import ZhipuAIHandler
        ai_handler = ZhipuAIHandler()
        print("✅ 成功加载 ZhipuAIHandler - 使用真实AI")
        
        # 测试API连接
        test_result = ai_handler.get_response("测试连接", {"name": "测试"})
        print(f"✅ API连接测试成功: {test_result[:50]}...")
    except ImportError as e:
        print(f"❌ 导入 ZhipuAIHandler 失败: {e}")
        print("⚠️ 将使用模拟处理器")
        
        # 创建一个简单的模拟处理器作为后备
        class SimpleMockAIHandler:
            def __init__(self):
                self.responses = [
                    "我理解你的问题。在灵魂匹配的计算中，每个提问都在塑造未来的轨迹。",
                    "有趣的观点。让我思考一下如何回应这个问题。",
                    "时间筛选一切，但也给真正的匹配留下空间。",
                    "概率是冰冷的，但你的选择可以赋予它温度。",
                    "每个灵魂都在寻找匹配，但方式各不相同。",
                ]
            
            def get_response(self, player_input, player_info, dialogue_history=None):
                return random.choice(self.responses)
            
            def generate_ending(self, player_info, dialogue_history, match_probability):
                player_name = player_info.get('name', '旅人')
                return f"""【匹配报告】
咨询者：{player_name}
最终概率：{match_probability:.6f}
结论：匹配需要时间、勇气和一点运气。"""
        
        ai_handler = SimpleMockAIHandler()
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        print("⚠️ 使用备用处理器")
        # 同样的备用处理器代码...


init python:
    def process_dialogue_input():
        """处理对话输入 - 使用真实AI生成回复"""
        global dialogue_history, dialogue_count, match_probability, current_input
        
        player_text = current_input.strip()
        if not player_text:
            return
        
        print(f"\n" + "=" * 50)
        print(f"📝 处理玩家输入")
        print(f"📋 输入内容: {player_text}")
        print(f"🔄 当前对话轮次: {dialogue_count}")
        print(f"🤖 AI处理器类型: {type(ai_handler).__name__}")
        
        # 记录玩家输入
        dialogue_history.append({"role": "player", "content": player_text})
        dialogue_count += 1
        
        # 检查是否要结束对话
        end_keywords = ["结束", "再见", "够了", "谢谢", "完成", "停止"]
        if any(keyword in player_text for keyword in end_keywords):
            if dialogue_count >= min_dialogue_rounds:
                print(f"🎯 满足结束条件，跳转到结局")
                renpy.jump("generate_ending")
                return
            else:
                needed = min_dialogue_rounds - dialogue_count
                dialogue_history.append({
                    "role": "ai", 
                    "content": f"我们至少还需要{needed}轮对话才能获得准确结果。请继续提问。"
                })
                current_input = ""
                renpy.restart_interaction()
                return
        
        # 准备玩家信息
        player_info = {
            "name": player_name,
            "gender": player_gender,
            "orientation": player_orientation,
            "dialogue_count": dialogue_count
        }
        
        # 获取AI回复
        print("🤖 正在获取AI回复...")
        try:
            # 调用AI处理器
            ai_reply = ai_handler.get_response(player_text, player_info, dialogue_history)
            print(f"✅ AI回复成功")
            print(f"💬 回复内容: {ai_reply[:200]}")
            
            # 检查是否为真实AI回复
            if "[模拟AI" in ai_reply or "[紧急回复" in ai_reply or "[测试回复" in ai_reply:
                print("⚠️ 警告：使用模拟回复，AI可能未正确连接")
        except Exception as e:
            print(f"❌ 获取AI回复时出错: {e}")
            import traceback
            traceback.print_exc()
            
            # 紧急备用回复
            ai_reply = f"关于「{player_text}」，系统正在处理中。换个问题试试？"
        
        # 记录AI回复
        dialogue_history.append({"role": "ai", "content": ai_reply})
        
        # 更新匹配概率
        update_match_probability(ai_reply, player_text)
        
        # 清空输入框
        current_input = ""
        
        # 强制界面更新
        renpy.restart_interaction()
    
    def update_match_probability(ai_reply, player_text):
        """更新匹配概率"""
        global match_probability
        
        # 基于回复长度和内容的质量调整概率
        reply_length = len(ai_reply)
        
        # 基础调整
        base_adjustment = random.uniform(-0.000002, 0.000003)
        
        # 长度加成（较长的回复通常质量更高）
        length_bonus = min(reply_length / 500.0 * 0.000001, 0.000001)
        
        # 相关性加成（检查是否回应了关键词）
        relevance_bonus = 0.0
        keywords = ["概率", "时间", "孤独", "命运", "爱", "未来"]
        for keyword in keywords:
            if keyword in player_text and keyword in ai_reply:
                relevance_bonus += 0.0000005
        
        # 总调整
        total_adjustment = base_adjustment + length_bonus + relevance_bonus
        
        # 应用调整
        match_probability += total_adjustment
        
        # 确保概率在合理范围内
        match_probability = max(0.000001, min(0.001, match_probability))
        
        print(f"概率更新: {total_adjustment:.9f}, 新概率: {match_probability:.6f}")
    
    def validate_inputs():
        """验证用户输入信息"""
        global input_error
        
        # 清空之前的错误提示
        input_error = ""
        
        # 1. 校验姓名（不能为空）
        if not player_name.strip():
            input_error = "姓名不能为空！"
            return False
        
        # 所有校验通过
        return True

init python:
    # 主引导系统类
    class GuidanceSystem:
        def __init__(self):
            self.guidance_log = []  # 记录所有引导性提问
            self.player_responses_to_guidance = {}  # 玩家对引导的回应质量
            
        def should_offer_guidance(self, dialogue_count, player_text, ai_response_length):
            """判断是否应该提供引导"""
            
            conditions = []
            
            # 条件1：对话轮次是3的倍数（但不包括第一轮）
            if dialogue_count > 1 and dialogue_count % 3 == 0:
                conditions.append("regular_interval")
            
            # 条件2：玩家回应很简短（少于10字）
            if len(player_text.strip()) < 10:
                conditions.append("short_response")
            
            # 条件3：AI的回应很长（超过200字），需要确认理解
            if ai_response_length > 200:
                conditions.append("need_confirmation")
            
            # 条件4：话题需要深化（检测到关键词但未深入）
            if self.needs_deepening(player_text):
                conditions.append("needs_deepening")
            
            # 条件5：对话出现重复模式
            if self.has_repetitive_pattern():
                conditions.append("repetitive_pattern")
            
            # 如果有任何条件满足，且距离上次引导至少2轮
            last_guidance_round = self.get_last_guidance_round()
            if conditions and (dialogue_count - last_guidance_round >= 2):
                return True, conditions
            
            return False, []
        
        def needs_deepening(self, player_text):
            """检查话题是否需要深化"""
            surface_keywords = ["概率", "时间", "孤独", "命运", "爱", "未来"]
            deep_keywords = ["存在主义", "决定论", "社会结构", "系统批判", "本体论"]
            
            # 如果提到了表面关键词但未涉及深层思考
            has_surface = any(keyword in player_text for keyword in surface_keywords)
            has_deep = any(keyword in player_text for keyword in deep_keywords)
            
            return has_surface and not has_deep
        
        def has_repetitive_pattern(self):
            """检查对话是否有重复模式"""
            if len(dialogue_history) < 4:
                return False
            
            last_4_player = [msg["content"] for msg in dialogue_history[-4:] if msg["role"] == "player"]
            
            # 检查是否都是简短回应
            if all(len(text) < 15 for text in last_4_player):
                return True
            
            # 检查是否重复相同类型的问题
            return False
        
        def get_last_guidance_round(self):
            """获取上次提供引导的对话轮次"""
            if not self.guidance_log:
                return 0
            
            return self.guidance_log[-1]["dialogue_count"]
        
        def generate_guidance(self, conditions, player_traits, dialogue_context):
            """生成引导性提问"""
            
            # 根据条件类型选择引导策略
            if "short_response" in conditions:
                return self._generate_reengagement_question(player_traits)
            elif "need_confirmation" in conditions:
                return self._generate_clarification_question(dialogue_context)
            elif "needs_deepening" in conditions:
                return self._generate_deepening_question(dialogue_context)
            elif "repetitive_pattern" in conditions:
                return self._generate_diversion_question(player_traits)
            else:  # regular_interval
                return self._generate_progression_question(dialogue_context)
        
        def _generate_reengagement_question(self, player_traits):
            """重新吸引玩家参与的问题"""
            questions = [
                "我注意到你的回应很简短。是这个话题让你感到不适，还是有其他原因？",
                "有时候简单的词句背后有复杂的感受。你想多分享一些吗？",
                "如果这个问题太难回答，我们可以换个角度。你对匹配最困惑的是什么？"
            ]
            
            # 根据玩家特征调整
            if player_traits.get("philosophical_view") == "rebel":
                questions.append("沉默也是一种反抗。你是在用沉默对抗系统的荒谬吗？")
            elif player_traits.get("philosophical_view") == "romantic":
                questions.append("爱情的话题有时让人词穷。是美好得难以形容，还是复杂得无从说起？")
            
            return random.choice(questions)
        
        def _generate_clarification_question(self, dialogue_context):
            """确认理解的引导问题"""
            # 总结最近的AI观点，让玩家确认或反驳
            last_ai_msg = None
            for msg in reversed(dialogue_context):
                if msg["role"] == "ai":
                    last_ai_msg = msg["content"]
                    break
            
            if last_ai_msg:
                # 提取关键观点
                key_points = self._extract_key_points(last_ai_msg)
                if key_points:
                    point = random.choice(key_points)
                    return f"我刚才提到'{point}'，你对这个观点有什么看法？"
            
            return "我刚才的解释清楚吗？你有什么疑问或不同看法？"
        
        def _generate_deepening_question(self, dialogue_context):
            """深化话题的引导问题"""
            # 分析最近的话题关键词
            recent_text = " ".join([msg["content"] for msg in dialogue_context[-3:]])
            
            topic_questions = {
                "概率": "当我们谈论概率时，是在讨论数学现实，还是在讨论希望与绝望的边界？",
                "时间": "时间对你来说，是爱情的敌人，还是爱情的考验？",
                "孤独": "这种孤独是来自外部世界的缺失，还是内心某种更深层的渴望？",
                "命运": "你相信的命运，是写好的剧本，还是无数选择的累积效应？",
                "爱": "你说的爱，是生物本能、社会建构，还是超越理解的连接？",
                "未来": "你想象的未来，是概率决定的终点，还是自由意志创造的画布？"
            }
            
            for topic, question in topic_questions.items():
                if topic in recent_text:
                    return question
            
            return "这个话题似乎有很多层面。你想从哪个角度深入探讨？"
        
        def _generate_diversion_question(self, player_traits):
            """转移话题的引导问题"""
            # 引入新但相关的维度
            new_dimensions = [
                "我们一直在谈个人层面。如果从社会角度看匹配系统，会有什么不同？",
                "换个角度：如果匹配不是找'另一半'，而是找'完整的自己'，会怎样？",
                "让我们想想哲学层面：匹配的本质是填补空缺，还是创造新的整体？"
            ]
            
            return random.choice(new_dimensions)
        
        def _generate_progression_question(self, dialogue_context):
            """推进对话的引导问题"""
            # 基于对话历史自然推进
            recent_topics = self._analyze_recent_topics(dialogue_context[-5:])
            
            progression_map = {
                "个人经历": "你的个人经历如何影响你对匹配的看法？",
                "社会观察": "你观察到的社会现象如何验证或挑战我们的讨论？", 
                "哲学思考": "这些思考如何改变你对生命意义的理解？",
                "情感体验": "这些概念与你的实际情感体验有什么关联？"
            }
            
            for topic, question in progression_map.items():
                if topic in recent_topics:
                    return question
            
            return "基于我们的对话，你想探索什么新方向？"
        
        def _extract_key_points(self, text):
            """从文本中提取关键观点"""
            # 简单实现：找包含观点性的句子
            import re
            point_indicators = ["我认为", "我相信", "实际上", "本质上", "关键在于"]
            sentences = re.split(r'[。！？]', text)
            
            points = []
            for sentence in sentences:
                if any(indicator in sentence for indicator in point_indicators):
                    # 清理句子
                    clean_sentence = sentence.strip()
                    if len(clean_sentence) > 10 and len(clean_sentence) < 100:
                        points.append(clean_sentence)
            
            return points[:3]  # 最多返回3个关键点
        
        def _analyze_recent_topics(self, recent_messages):
            """分析最近消息的话题"""
            all_text = " ".join([msg["content"] for msg in recent_messages])
            
            topics = []
            topic_keywords = {
                "个人经历": ["我", "我的", "自己", "经历", "体验", "感受"],
                "社会观察": ["社会", "人们", "大家", "普遍", "常见", "现象"],
                "哲学思考": ["意义", "存在", "本质", "真理", "哲学", "思考"],
                "情感体验": ["感觉", "情感", "心情", "情绪", "爱", "孤独"]
            }
            
            for topic, keywords in topic_keywords.items():
                if any(keyword in all_text for keyword in keywords):
                    topics.append(topic)
            
            return topics
        
        def integrate_guidance(self, ai_response, guidance_question, guidance_style="natural"):
            """将引导性提问整合到AI回应中"""
            
            styles = {
                "natural": f"\n\n说到这里，我不禁想问：{guidance_question}",
                "direct": f"\n\n【我想引导你思考】{guidance_question}",
                "subtle": f"\n\n（这让我想到：{guidance_question}）",
                "challenge": f"\n\n**挑战性问题：**{guidance_question}",
                "reflective": f"\n\n**值得反思的是：**{guidance_question}"
            }
            
            style = guidance_style
            if not guidance_style or guidance_style not in styles:
                # 根据玩家特征选择风格
                player_traits = player_traits_cache
                if player_traits.get("philosophical_view") == "rebel":
                    style = "challenge"
                elif player_traits.get("philosophical_view") == "romantic":
                    style = "reflective"
                elif player_traits.get("emotional_tendency", 0) < -2:
                    style = "subtle"  # 情绪低落时用更温和的方式
                else:
                    style = "natural"
            
            integrated_response = ai_response + styles[style]
            
            # 记录这次引导
            self.guidance_log.append({
                "dialogue_count": dialogue_count,
                "question": guidance_question,
                "style": style,
                "conditions": conditions if 'conditions' in locals() else []
            })
            
            return integrated_response

# 全局引导系统实例
default guidance_system = GuidanceSystem()

# ====================== 信息输入界面 ======================
screen player_info_input():
    # modal True  # 移除 modal 以允许 input 聚焦
    add "table"  # 背景图
    
    # 输入容器
    frame:
        xalign 0.5
        yalign 0.5
        background "#00000080"  # 半透明黑
        padding (40, 40)
        
        vbox spacing 20:
            # 标题
            label "请填写你的信息" style "input_label_style"
            
            # 错误提示（红色显示）
            if input_error:
                text input_error size 26 color "#ff4444" xalign 0.5
            
            # --- 姓名输入 ---
            hbox spacing 15:
                label "姓名：" style "input_label_style"
                input value VariableInputValue("player_name") style "input_style"
            
            # --- 性别选择  ---
            hbox spacing 15:
                label "性别：" style "input_label_style"
                textbutton "男" action SetVariable("player_gender", "男") style "choice_button_style"
                textbutton "女" action SetVariable("player_gender", "女") style "choice_button_style"
            
            # --- 性取向选择 ---
            hbox spacing 15:
                label "取向：" style "input_label_style"
                textbutton "偏向男性" action SetVariable("player_orientation", "偏向男性") style "choice_button_style"
                textbutton "偏向女性" action SetVariable("player_orientation", "偏向女性") style "choice_button_style"
                textbutton "双向" action SetVariable("player_orientation", "双向") style "choice_button_style"
            
            # 确认按钮（点击先校验，通过再返回）
            textbutton "确认信息" action [Function(validate_inputs), If(validate_inputs(), Return())] style "confirm_button_style"

# ====================== 重新设计的对话界面 ======================
screen dialogue_interface():
    modal True   # <--- 新增这行代码，这是关键！
    
    add "taking"
    
    # 左侧显示所长立绘
    add "ai_character":
        xpos 50
        ypos 200
        zoom 0.7
    
    # 右侧区域：对话内容
    frame:
        xpos 300
        ypos 50
        xsize 900
        ysize 550
        background "#00000080"
        
        # 状态栏
        hbox:
            xpos 20
            ypos 20
            spacing 50
            
            vbox:
                text "匹配概率":
                    size 20
                    color "#cccccc"
                    font x
                text "[match_probability:.6f]":
                    size 26
                    color "#f9c74f"
                    font x
            
            vbox:
                text "对话轮次":
                    size 20
                    color "#cccccc"
                    font x
                text "[dialogue_count] 轮":
                    size 26
                    color "#4cc9f0"
                    font x
            
            vbox:
                text "咨询对象":
                    size 20
                    color "#cccccc"
                    font x
                text "艾拉所长":
                    size 26
                    color "#f72585"
                    font x
        
        # 对话历史区域
        frame:
            xpos 20
            ypos 80
            xsize 860
            ysize 400
            background "#1a1a2a80"
            
            viewport:
                id "dialogue_viewport"
                scrollbars "vertical"
                mousewheel True
                draggable True
                yinitial 1.0
                
                vbox:
                    spacing 15
                    xsize 830
                    
                    # 欢迎语
                    if len(dialogue_history) == 0:
                        frame:
                            background "#2a1b3d80"
                            padding (15, 15)
                            xmaximum 700
                            
                            text "【艾拉所长】你好，[player_name]。我是灵魂匹配事务所的所长艾拉。" +\
                                "你可以问我任何关于匹配、概率、命运的问题。" +\
                                "我们的对话需要至少5轮才能获得准确的分析结果。" +\
                                "试试问这些问题：概率、时间、孤独、命运、爱、未来":
                                size 22
                                color "#f9c74f"
                                font x
                    
                    # 对话历史
                    for msg in dialogue_history:
                        if msg["role"] == "player":
                            frame:
                                background "#351c6080"
                                padding (15, 15)
                                xmaximum 600
                                xalign 1.0
                                
                                text "【你】" + msg["content"]:
                                    size 22
                                    color "#ffffff"
                                    font x
                        else:
                            frame:
                                background "#2a1b3d80"
                                padding (15, 15)
                                xmaximum 600
                                xalign 0.0
                                
                                text "【艾拉】" + msg["content"]:
                                    size 22
                                    color "#f9c74f"
                                    font x
    
    # 底部输入区域
    frame:
        xpos 300
        ypos 620
        xsize 900
        background "#1a1a2a"
        padding (20, 20)
        yoffset -65
        
        vbox:
            spacing 10
            
            # 输入提示
            text "输入你想问艾拉的问题..." size 20 color "#888888" font x
            
            # 输入框和发送按钮
            hbox:
                spacing 15
                xfill True
                
                input:
                    id "player_input"
                    value VariableInputValue("current_input")
                    length 100
                    size 24
                    color "#ffffff"
                    xfill True
                    font x
                    yoffset -35
                
                textbutton "发送":
                    action Function(process_dialogue_input)
                    background "#7209b7"
                    text_color "#ffffff"
                    padding (20, 10)
                    xminimum 100
                    hover_background "#9d4edd"
                    text_size 22
                    text_font x
                    yoffset -35
                    xoffset 100
            
            # 关键词快捷按钮
            hbox:
                spacing 10
                xalign 0.5
                
                for keyword in ["概率", "时间", "孤独", "命运", "爱", "未来"]:
                    textbutton keyword:
                        action [SetVariable("current_input", keyword), Function(process_dialogue_input)]
                        background "#444444"
                        text_color "#ffffff"
                        padding (10, 5)
                        hover_background "#666666"
                        text_size 18
                        text_font x
                        yoffset -10
                        xoffset 5
    
    # 结束咨询按钮
    if dialogue_count >= min_dialogue_rounds:
        textbutton "结束咨询":
            action Jump("generate_ending")
            xpos 1150
            ypos 80
            background "#f72585"
            text_color "#ffffff"
            padding (20, 15)
            hover_background "#ff4da6"
            text_size 24
            text_font x
            text_bold True

# ====================== 游戏流程 ======================
label start:
    play music "audio/opening_theme.mp3"
    # 全黑开场
    scene black with Dissolve(2.0)

# 开篇独白（配合打字机效果）
    show text "{color=#cccccc}在这个城市，每个人都有一个匹配数字。{/color}" at truecenter with dissolve
    $ renpy.pause(2.0)
    hide text with dissolve

    show text "{color=#cccccc}它决定了你与灵魂伴侣相遇的概率。{/color}" at truecenter with dissolve
    $ renpy.pause(2.0)
    hide text with dissolve

    show text "{color=#cccccc}从0.000001%到0.01%不等。{/color}" at truecenter with dissolve
    $ renpy.pause(2.0)
    hide text with dissolve

    show text "{color=#cccccc}有人穷尽一生，只为验证这个数字的真实性。{/color}" at truecenter with dissolve
    $ renpy.pause(2.0)
    hide text with dissolve

    show text "{color=#cccccc}欢迎来到...{/color}" at truecenter with dissolve
    $ renpy.pause(1.5)
    hide text with dissolve

    show text "{font=[x]}{color=#f9ebff}{size=80}灵魂匹配事务所{/size}{/color}{/font}" at truecenter with dissolve
    # 实际使用时取消注释下一行
    # play sound "audio/glitch_effect.wav"
    $ renpy.pause(3.0)
    hide text with dissolve
    stop music fadeout 1.0

    play music "audio/medium_theme.mp3" fadein 1.0
    scene way
    play sound "audio/rain.MP3" 
    "雨夜。霓虹灯在潮湿的街道上拖出长长的倒影。"
    "这座城市从不睡眠，就像匹配系统从不停止计算。"
    scene office
    "你站在一栋不起眼的建筑前。"
    "门口的招牌在雨中闪烁：{font=[x]}{color=#f9ebff}灵魂匹配事务所{/color}{/font}"
    scene peopleindoor
    "玻璃门映出你的面容。"
    scene opendoor
    play sound "audio/bell.MP3"
    play sound "audio/door.MP3"
    "推开门的瞬间，风铃轻响。"
    stop sound fadeout 0.5
    scene ai
    play sound "audio/typewriter.MP3"
    play sound "audio/paper.MP3"
    "光线柔和。空气中弥漫着旧纸张和电子设备混合的气息。"
    "办公桌后，一个身影抬起头。"
    scene workingroom
    show ai_character at left with dissolve
    "艾拉所长" "请坐。我是艾拉，这间事务所的所长。"
    "艾拉所长" "我知道你为什么来。每个人都为同一个原因而来。"


    # 关键问题
    show expression Text("你想知道真相吗？", size=40, color="#f9c74f", font=x) as truth_text:
        xcenter 0.5
        ycenter 0.3
    with dissolve
    # 实际使用时取消注释下一行
    # play sound "audio/glitch_effect2.wav"
    $ renpy.pause(1.5)
    hide truth_text with dissolve

    # 解释匹配系统
    "艾拉所长" "让我先解释规则。这很重要。"

    "艾拉所长" "灵魂匹配概率由『三重算法』决定："
    scene light
    show ai_character at left with dissolve
    "艾拉所长" "1. {color=#4cc9f0}时间坐标{/color} - 你们是否存在于同一个时代"
    scene touch
    show ai_character at left with dissolve
    "艾拉所长" "2. {color=#f72585}空间频率{/color} - 生活轨迹的交集可能性" 
    scene morepeople
    show ai_character at left with dissolve
    "艾拉所长" "3. {color=#38b000}社会共振{/color} - 阶级、职业、社交圈的匹配度" 
    scene withpeople
    show ai_character at left with dissolve
    "艾拉所长" "我的工作，就是计算你的数字。"
    "艾拉所长" "然后...告诉你最后会匹配到的结果。"

    # 停顿，增加紧张感
    $ renpy.pause(1.0)
    # 实际使用时取消注释下一行
    # play sound "audio/paper_rustle.wav"

    "艾拉所长" "但在此之前，我需要了解你。"
    "艾拉所长" "真正的你。{w=0.8}不仅仅是名字和年龄。"
    "艾拉所长" "而是你的渴望。{w=0.6}你的恐惧。{w=0.6}你对爱的定义。"

# 展示统计数据
    show expression Text("统计数据：", size=35, color="#cccccc", font=x) as stats_title:
        xcenter 0.5
        ycenter 0.2
    with dissolve

    show expression Text("· 93% 的灵魂伴侣已去世", size=28, color="#ff5555", font=x) as stat1:
        xcenter 0.5
        ycenter 0.3
    with dissolve

    show expression Text("· 3% 的灵魂伴侣尚未出生", size=28, color="#4cc9f0", font=x) as stat2:
        xcenter 0.5
        ycenter 0.4
    with dissolve

    show expression Text("· 4% 的灵魂伴侣与你同时代", size=28, color="#38b000", font=x) as stat3:
        xcenter 0.5
        ycenter 0.5
    with dissolve

    show expression Text("在这4%中，只有0.01%的概率会相遇", size=28, color="#f9c74f", font=x) as stat4:
        xcenter 0.5
        ycenter 0.6
    with dissolve

    $ renpy.pause(3.0)
    hide stats_title
    hide stat1
    hide stat2
    hide stat3
    hide stat4
    with dissolve

    "艾拉所长" "这些数字可能让你感到...冰冷。"
    "艾拉所长" "但每一次咨询，都是一次对命运的计算。"
    "艾拉所长" "而计算的结果，可能会改变你对孤独的理解。"

    # 引导玩家提问
    "艾拉所长" "现在，轮到你了。"
    "艾拉所长" "你可以问我任何问题。关于概率，关于时间，关于孤独..."
    "艾拉所长" "关于那个你一直想知道答案的问题。"

    # 强调对话重要性
    # 实际使用时取消注释下一行
    #play sound "audio/typewriter.wav"
    show expression Text("每一次提问，都会改变你的匹配概率", size=30, color="#f9c74f", font=x) as tip_text:
        xcenter 0.5
        ycenter 0.8
    with dissolve
    $ renpy.pause(2.5)
    hide tip_text with dissolve

    "艾拉所长" "我们至少需要5轮对话。"
    "艾拉所长" "让我更了解你。{w=0.5}也让系统更精确。"

    # 准备开始信息收集
    "艾拉所长" "那么，先让来登记一下你的基础信息吧。"
    
    # 信息收集 - 重置错误信息
    $ input_error = ""
    call screen player_info_input
    
    "✅ 信息已记录！"
    scene taking
    "艾拉所长" "嗯，请跟随我移步到房间内。"
    "艾拉所长" "现在，让我们开始对话吧。"
    stop music fadeout 1.0
    play music "audio/consultation_theme.mp3" fadein 1.0
    # 初始化对话
    $ dialogue_count = 0
    $ dialogue_history = []
    $ match_probability = 0.0001
    
    # 进入对话界面
    show screen dialogue_interface
    window hide
    pause

# ====================== 结局跳转逻辑 ======================
label generate_ending:
    hide screen dialogue_interface

    # 准备玩家信息
    $ player_info = {
        "name": player_name,
        "gender": player_gender,
        "orientation": player_orientation
    } 
    
    # 分析对话，确定结局
    $ analyze_dialogue_for_ending()
    $ ending_type = determine_ending_type()
    

    
    # 跳转到对应结局
    if ending_type == "time_rebel_ending":
        jump ending_time_rebel
    elif ending_type == "ghost_love_ending":
        jump ending_ghost_love
    elif ending_type == "soulmate_dead_ending":
        jump ending_soulmate_dead
    elif ending_type == "future_investor_ending":
        jump ending_future_investor
    elif ending_type == "soulmate_unborn_ending":
        jump ending_soulmate_unborn
    elif ending_type == "rich_success_ending":
        jump ending_rich_success
    elif ending_type == "career_success_ending":
        jump ending_career_success
    elif ending_type == "miracle_found_ending":
        jump ending_miracle_found
    elif ending_type == "system_rebel_ending":
        jump ending_system_rebel
    elif ending_type == "nihilist_acceptance_ending":
        jump ending_nihilist_acceptance
    elif ending_type == "career_tragedy_ending":
        jump ending_career_tragedy
    elif ending_type == "poor_desperation_ending":
        jump ending_poor_desperation
    elif ending_type == "realistic_compromise_ending":
        jump ending_realistic_compromise
    elif ending_type == "eternal_search_ending":
        jump ending_eternal_search
    elif ending_type == "dream_ending":
        jump ending_dream_egg
    elif ending_type == "quantum_ending":
        jump ending_quantum_egg
    else:
        jump ending_default

# ====================== 结局1: 时间革命者 ======================
label ending_time_rebel:
    # 触发逻辑：伴侣已去世 + 反抗哲学观
    # 海报设计：破碎的时钟环绕着光芒，标题"时间革命者"
    scene bg_broken_clock with dissolve
    play music "audio/time_revolution.mp3"
    pause 3.0
    "你选择了反抗时间的道路。"
    "也许你永远无法见到已故的灵魂伴侣，但你决定用自己的方式改写规则。"
    "艾拉所长看着你离去的背影，轻轻叹了口气。"
    "有些人选择接受，有些人选择改变。"
    "而你，选择成为时间的革命者。"
    jump ending_common_conclusion

# ====================== 结局2: 幽灵恋人 ======================
label ending_ghost_love:
    # 触发逻辑：伴侣已去世 + 浪漫哲学观
    # 海报设计：半透明的幽灵与活人牵手，月光下，标题"幽灵恋人"
    scene bg_ghost_love with dissolve
    play music "audio/ghost_love.mp3"
    pause 3.0
    
    "你的伴侣是那个已故的灵魂。"
    "虽然无法触摸，无法对话，但你知道，在某个平行宇宙中，你们正幸福地生活在一起。"
    "爱情超越了物理定律，成为你心中永恒的光芒。"
    jump ending_common_conclusion

# ====================== 结局3: 已故灵魂伴侣 ======================
label ending_soulmate_dead:
    # 触发逻辑：伴侣已去世 + 其他哲学观
    # 海报设计：墓碑前孤独的身影，年份1965/1988/1990等，标题"时间的玩笑"
    scene bg_graveyard with dissolve
    play music "audio/melancholy.mp3"
    pause 3.0
    
    "你的灵魂伴侣已经去世多年，可能是在1965年的一场意外中。"
    "这是93%%的人都面临的现实：完美的匹配存在于时间之外。"
    

    jump ending_common_conclusion


# ====================== 结局5: 未来投资者 ======================
label ending_future_investor:
    # 触发逻辑：伴侣未出生 + 富人阶级
    # 海报设计：金钱符号与时间线交织，标题"时间的价值"
    scene bg_money_timeline with dissolve
    play music "audio/future_investment.mp3"
    pause 3.0
    
    "你决定投资未来。"
    "设立基金，冷冻精子或卵子，确保在正确的时间与正确的灵魂相遇。"
    "富人可以用金钱购买时间的特权，这是系统的另一种规则。"
    
    jump ending_common_conclusion

# ====================== 结局6: 未出生灵魂伴侣 ======================
label ending_soulmate_unborn:
    # 触发逻辑：伴侣未出生 + 其他条件
    # 海报设计：未来的城市剪影，标题"等待2075"
    scene bg_future_city with dissolve
    play music "audio/waiting_future.mp3"
    pause 3.0
    
    "报告显示，你的灵魂伴侣将在2075年出生。"
    "那时你已经是一位老人，或者可能已经不在人世。"
    "3%%的人面临这样的命运：完美的匹配存在于错误的时代。"
    jump ending_common_conclusion

# ====================== 结局7: 富人成功者 ======================
label ending_rich_success:
    # 触发逻辑：找到伴侣 + 富人阶级
    # 海报设计：金色光芒中的两人，VIP徽章，标题"金质匹配"
    scene bg_golden_match with dissolve
    play music "audio/rich_success.mp3"
    pause 3.0
    
    "恭喜你！系统找到了你的灵魂伴侣。"
    "由于你的社会阶级和资源，匹配系统能够更高效地工作。"
    "富人成功率为0.01%%，而穷人的成功率只有0.0001%%。"
    "这就是现实：金钱可以购买概率。"
    jump ending_common_conclusion

# ====================== 结局8: 职业成功者 ======================
label ending_career_success:
    # 触发逻辑：找到伴侣 + 职业寻找法
    # 海报设计：时代广场警察制服，无数眼睛背景，标题"职业的胜利"
    scene bg_times_square_police with dissolve
    play music "audio/career_victory.mp3"
    pause 3.0
    
    "系统通过你的职业轨迹，锁定了那个最匹配的灵魂。"
    "职业成为了你的优势，让你在概率游戏中占据主动。"
    jump ending_common_conclusion

# ====================== 结局9: 奇迹发现者 ======================
label ending_miracle_found:
    # 触发逻辑：找到伴侣 + 普通条件
    # 海报设计：超市收银台相遇，朴素但温馨，标题"万分之一奇迹"
    scene bg_supermarket_miracle with dissolve
    play music "audio/miracle_found.mp3"
    pause 3.0
    
    "在0.01%的概率中，你成为了那个幸运儿。"
    "系统找到了你的灵魂伴侣，你们生活在同一个时代，同一个城市。"
    "这是统计学上的奇迹，是系统计算出的完美匹配。"
    "请相信，有时候数字会给你惊喜。"
    jump ending_common_conclusion

# ====================== 结局10: 系统革命者 ======================
label ending_system_rebel:
    # 触发逻辑：未找到伴侣 + 反抗哲学观
    # 海报设计：燃烧的匹配系统界面，抗议标语，标题"匹配革命"
    scene bg_burning_system with dissolve
    play music "audio/system_revolution.mp3"
    pause 3.0
    
    "你决定反抗这个系统。"
    "为什么爱情要被概率和算法定义？"
    "你加入了地下抵抗组织，试图推翻这个决定论的匹配系统。"
    "也许真正的爱情，应该超越所有的计算。"
    jump ending_common_conclusion

# ====================== 结局11: 虚无主义接受者 ======================
label ending_nihilist_acceptance:
    # 触发逻辑：未找到伴侣 + 虚无主义哲学观
    # 海报设计：空无一物的宇宙，标题"虚无的宁静"
    scene bg_empty_universe with dissolve
    play music "audio/nothingness.mp3"
    pause 3.0
    
    "你接受了虚无。"
    "如果爱情只是化学物质和社会建构的产物，那么寻找灵魂伴侣又有什么意义？"
    "你找到了另一种平静：在承认无意义之后，自由地活着。"

    jump ending_common_conclusion

# ====================== 结局12: 职业悲剧 ======================
label ending_career_tragedy:
    # 触发逻辑：未找到伴侣 + 职业寻找法
    # 海报设计：疲惫的警察，眼睛布满血丝，标题"职业的代价"
    scene bg_exhausted_police with dissolve
    play music "audio/career_failure.mp3"
    pause 3.0
    
    "二十年的职业生涯，你见过无数人。"
    "但系统从未发出确认信号。"
    "职业成为了你的牢笼，你在无尽的寻找中逐渐疲惫。"
    "有时候，接触越多，孤独越深。"
    jump ending_common_conclusion

# ====================== 结局13: 穷人绝望 ======================
label ending_poor_desperation:
    # 触发逻辑：未找到伴侣 + 穷人阶级
    # 海报设计：破旧房间，价格标签"VIP匹配：10000元/月"，标题"贫穷的诅咒"
    scene bg_poor_despair with dissolve
    play music "audio/poor_desperation.mp3"
    pause 3.0
    
    "贫穷限制了你的可能性。"
    "VIP匹配服务需要每月10000元，而你的收入只有2000元。"
    "富人成功率为0.01%%，穷人只有0.0001%。"
    "阶级成为了无法逾越的鸿沟。"
    jump ending_common_conclusion

# ====================== 结局14: 现实妥协者 ======================
label ending_realistic_compromise:
    # 触发逻辑：未找到伴侣 + 现实主义哲学观
    # 海报设计：微笑面具，完美的社交媒体照片，标题"现实的微笑"
    scene bg_perfect_mask with dissolve
    play music "audio/bitter_sweet.mp3"
    pause 3.0
    
    "你选择了妥协。"
    "既然找不到灵魂伴侣，那就找一个合适的伴侣。"
    "社交媒体上的完美照片，朋友圈的甜蜜更新。"
    "有时候，表演幸福比真正幸福更容易。"
    jump ending_common_conclusion

# ====================== 结局15: 永恒寻找者 ======================
label ending_eternal_search:
    # 触发逻辑：未找到伴侣 + 其他条件
    # 海报设计：无尽的道路，不断行走的身影，标题"无尽的寻找"
    scene bg_endless_road with dissolve
    play music "audio/eternal_search.mp3"
    pause 3.0
    
    "你决定继续寻找。"
    "[years_searching]年过去了，你仍在路上。"
    "也许永远找不到，但寻找本身成为了意义。"
    "在这条无尽的道路上，你学会了与孤独和解。"
    jump ending_common_conclusion

# ====================== 彩蛋结局1: 梦境编织者 ======================
label ending_dream_egg:
    # 触发逻辑：对话中提到"庄周梦蝶"
    # 海报设计：蝴蝶与人影交织，梦境般模糊，标题"庄周梦蝶"
    scene bg_dream_butterfly with dissolve
    #play music "audio/dream_weaving.mp3"
    pause 3.0
    
    "庄周梦蝶，蝶梦庄周。"
    "也许整个匹配系统只是一场集体梦境。"
    "我们是梦中的蝴蝶，还是做梦的庄周？"
    "当你开始怀疑现实本身，匹配的概率就失去了意义。"
    jump ending_common_conclusion

# ====================== 彩蛋结局2: 量子纠缠伴侣 ======================
label ending_quantum_egg:
    # 触发逻辑：对话中提到"薛定谔"或"双缝实验"
    # 海报设计：量子态叠加的两个人，标题"量子纠缠"
    scene bg_quantum_entanglement with dissolve
    #play music "audio/quantum.mp3"
    pause 3.0
    
    "根据量子力学，你的灵魂伴侣处于叠加态。"
    "在你观察之前，TA同时是你的伴侣又不是你的伴侣。"
    "也许，所有的可能性同时存在，只是你的选择让其中一个坍缩为现实。"
    jump ending_common_conclusion
    
label ending_common_conclusion:
    scene workingroom 
    "【匹配分析完成】"
    show ai_character at left with dissolve
    "艾拉" "感谢你来到灵魂匹配事务所。"
    "艾拉" "无论结局如何，希望都在你手中。"
    
    return

# ====================== 样式定义 ======================
style input_label_style:
    size 30
    color "#ffffff"
    font x

style input_style:
    size 30
    color "#ffffff"
    background "#000000"
    padding (10, 5)
    font x

style choice_button_style:
    size 28
    background "#351c60"
    color "#ffffff"
    padding (10, 5)
    hover_background "#05002f"
    font x

style confirm_button_style:
    xalign 0.5
    size 35
    background "#351c60"
    color "#ffffff"
    padding (20, 10)
    hover_background "#05002f"
    font x