import streamlit as st
import random
import time

# 页面配置
st.set_page_config(page_title="唯一伴侣·命运匹配仪", page_icon="🔮", layout="wide")

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .soulmate-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 1rem 0;
    }
    .interaction-box {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2rem;
        padding: 0.8rem;
        border-radius: 10px;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🔮 唯一伴侣·命运匹配仪</h1>', unsafe_allow_html=True)
st.markdown("**核心设定：每个人只有1个随机匹配的知心伴侣——但TA的命运由你的选择决定**")

# 初始化session state
if 'soulmate_data' not in st.session_state:
    st.session_state.soulmate_data = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

# ---------------------- 1. 用户自定义选择 ----------------------
with st.sidebar:
    st.header("⚙️ 你的命运参数")
    user_age = st.slider("👤 你的年龄", min_value=0, max_value=100, value=25, help="年龄会影响相遇概率")
    user_orientation = st.radio("💝 你的取向", ["异性", "同性", "不限"], help="这会影响匹配的性别")
    user_region = st.selectbox("🌍 你所在地区", ["乡村", "县城", "地级市", "省会/一线城市", "海外"], help="地区会影响相遇概率")
    
    st.divider()
    if st.session_state.soulmate_data:
        if st.button("🔄 重新匹配", use_container_width=True):
            st.session_state.soulmate_data = None
            st.session_state.messages = []
            st.rerun()


# ---------------------- 2. 伴侣生成逻辑（贴合主题矛盾） ----------------------
def generate_soulmate(user_age, user_orientation, user_region):
    # 1. 随机时空（覆盖“离世/在世/未出生”）
    time_options = [
        ("公元前500年·古希腊", "已离世"),
        ("公元1500年·明朝", "已离世"),
        ("1900年·维多利亚时代", "已离世"),
        (f"{2025 - (user_age//20)*10}年·当代", "在世"),  # 同年代波动
        (f"{2025 + (user_age//20)*20}年·近未来", "未出生"),
        (f"{2100 + (user_age//20)*50}年·远未来", "未出生")
    ]
    era, status = random.choice(time_options)

    # 2. 匹配性别（基于用户取向）
    genders = ["男", "女"]
    if user_orientation == "异性":
        user_gender = random.choice(genders)
        soulmate_gender = "女" if user_gender == "男" else "男"
    elif user_orientation == "同性":
        soulmate_gender = random.choice(genders)
    else:
        soulmate_gender = random.choice(genders)

    # 3. 年龄（贴合时空+用户年龄）
    if status == "在世":
        age_diff = random.randint(-15, 15)
        soulmate_age = max(0, user_age + age_diff)
    else:
        soulmate_age = random.randint(16, 60)  # 离世/未出生者的年龄

    # 4. 地区（随机，可能与用户无关）
    soulmate_region = random.choice(["古雅典城邦", "明朝苏州府", "伦敦东区", "你的同城", "火星基地", "银河殖民地"])

    # 5. 专属标签（贴合时空）
    era_short = era.split("·")[-1]
    trait_map = {
        "古希腊": "会写哲学戏剧台词",
        "明朝": "能绣双面苏绣手帕",
        "维多利亚时代": "擅长调英式下午茶",
        "当代": f"收藏了{random.randint(10,50)}种{user_region}特色小吃配方",
        "近未来": "能修家用机器人电路",
        "远未来": "会和星际宠物精神链接"
    }
    # 处理可能的时代名称
    trait = trait_map.get(era_short, f"拥有{random.choice(['神秘', '独特', '稀有'])}的{random.choice(['技能', '天赋', '才能'])}")

    return era, status, soulmate_gender, soulmate_age, soulmate_region, trait


# ---------------------- 3. 相遇概率计算（贴合原文逻辑） ----------------------
def calc_prob(status, user_region, user_age):
    # 基础概率：时空状态
    if status == "已离世" or status == "未出生":
        base_prob = 0.00001
        reason1 = "TA和你不在同一时空，相遇概率趋近于0"
    else:
        base_prob = 0.01  # 同年代基础概率
        reason1 = "你们处于同一时空，有相遇的可能"

    # 地区修正：乡村/县城接触人数更少
    region_factor = {
        "乡村": 0.05,
        "县城": 0.1,
        "地级市": 0.3,
        "省会/一线城市": 0.8,
        "海外": 0.5
    }
    base_prob *= region_factor[user_region]

    # 年龄修正：年龄越大，接触新人越少
    age_factor = max(0.1, 1 - (user_age / 150))
    base_prob *= age_factor

    # 最终概率+原因（转换为百分比）
    final_prob_percent = round(base_prob * 100, 6)
    reasons = [reason1] if status != "在世" else [
        reason1,
        f"你在{user_region}，接触的陌生人数量有限",
        f"你{user_age}岁，能接触的新人越来越少"
    ]
    return final_prob_percent, reasons


# ---------------------- 辅助函数：解析年份 ----------------------
def parse_year(era_str):
    """解析时空字符串中的年份"""
    try:
        year_part = era_str.split("·")[0]
        if "前" in year_part:
            year_str = year_part.replace("公元前", "").replace("年", "")
            return -int(year_str)
        else:
            year_str = year_part.replace("公元", "").replace("年", "")
            return int(year_str)
    except:
        return 2025

# ---------------------- 4. 互动逻辑：命运卡片拆箱 ----------------------
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    if st.button("✨ 开启命运：抽取你的唯一伴侣", type="primary", use_container_width=True):
        # 拆箱动画
        progress_bar = st.progress(0)
        status_text = st.empty()
        loading_messages = [
            "正在扫描时空维度...",
            "正在读取命运线索...",
            "正在匹配唯一伴侣...",
            "正在计算相遇概率...",
            "✨ 匹配完成！"
        ]
        for i, msg in enumerate(loading_messages):
            status_text.info(f"🔮 {msg}")
            progress_bar.progress((i + 1) / len(loading_messages))
            time.sleep(0.8)
        progress_bar.empty()
        status_text.empty()

        # 生成伴侣信息
        era, status, sm_gender, sm_age, sm_region, sm_trait = generate_soulmate(
            user_age, user_orientation, user_region
        )
        prob_percent, prob_reasons = calc_prob(status, user_region, user_age)
        
        # 保存到session state
        st.session_state.soulmate_data = {
            'era': era,
            'status': status,
            'gender': sm_gender,
            'age': sm_age,
            'region': sm_region,
            'trait': sm_trait,
            'prob': prob_percent,
            'reasons': prob_reasons
        }

# 如果已有匹配结果，显示命运卡片
if st.session_state.soulmate_data:
    data = st.session_state.soulmate_data
    era = data['era']
    status = data['status']
    sm_gender = data['gender']
    sm_age = data['age']
    sm_region = data['region']
    sm_trait = data['trait']
    prob_percent = data['prob']
    prob_reasons = data['reasons']

    # 命运卡片展示
    st.divider()
    
    # 状态图标
    status_emoji = "💀" if status == "已离世" else "👶" if status == "未出生" else "✨"
    st.markdown(f'<div class="soulmate-card"><h2>{status_emoji} 你的唯一伴侣·命运卡片</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📋 基本信息")
        st.markdown(f"""
        **🌌 时空坐标**：{era}  
        **{status_emoji} 命运状态**：{status}  
        **👤 性别**：{sm_gender}  
        **🎂 年龄**：{sm_age}岁  
        **📍 所在地区**：{sm_region}  
        **⭐ 专属技能**：{sm_trait}
        """)
        
        st.divider()
        
        # 概率展示
        prob_display = f"{prob_percent}%" if prob_percent >= 0.01 else f"{prob_percent:.6f}%"
        st.markdown(f"### 📊 相遇概率：{prob_display}")
        
        # 进度条（归一化处理）
        progress_value = min(prob_percent / 100, 1.0) if prob_percent > 0 else prob_percent / 0.0001
        st.progress(progress_value)
        
        st.markdown("**概率分析**：")
        for idx, r in enumerate(prob_reasons, 1):
            st.markdown(f"💭 {idx}. {r}")

    with col2:
        st.markdown("### 💬 跨命运互动")
        
        # 不同状态的互动
        if status == "已离世":
            era_year = parse_year(era)
            years_ago = 2025 - era_year
            st.markdown(f'<div class="interaction-box">', unsafe_allow_html=True)
            st.error(f"💀 **（来自{era}的刻痕）**：\n\n「你的呼唤穿过了{years_ago}年，但我已经化作尘埃了...」")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 聊天历史
            if st.session_state.messages:
                st.markdown("**💭 对话历史**：")
                for msg in st.session_state.messages[-5:]:  # 只显示最后5条
                    st.caption(f"💬 {msg}")
            
            user_msg = st.text_input("💭 你想对TA说句跨越时空的话：", key="msg_input")
            if user_msg and st.button("📤 发送", key="send_past"):
                response = f"（刻痕泛起微光）：「{user_msg}... 我会把这句话刻在石碑上，留给后世看见。」"
                st.session_state.messages.append(f"你：{user_msg}")
                st.session_state.messages.append(f"TA：{response}")
                st.info(f"✨ {response}")
                st.rerun()
                
        elif status == "未出生":
            era_year = parse_year(era)
            years_wait = max(0, era_year - 2025)
            st.markdown(f'<div class="interaction-box">', unsafe_allow_html=True)
            st.warning(f"👶 **（来自{era}的光斑）**：\n\n「我还要等{years_wait}年才会出生，但我感受到了你的期待~」")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 聊天历史
            if st.session_state.messages:
                st.markdown("**💭 对话历史**：")
                for msg in st.session_state.messages[-5:]:
                    st.caption(f"💬 {msg}")
            
            user_msg = st.text_input("💭 你想给未来的TA留句话：", key="msg_input")
            if user_msg and st.button("📤 发送", key="send_future"):
                response = f"（光斑凝聚成文字）：「{user_msg}——这句话会存在时空缓存里，等我出生时收到。」"
                st.session_state.messages.append(f"你：{user_msg}")
                st.session_state.messages.append(f"TA：{response}")
                st.info(f"✨ {response}")
                st.rerun()
        else:
            if sm_region == "你的同城":
                st.markdown(f'<div class="interaction-box">', unsafe_allow_html=True)
                st.success(f"✨ **（TA在你家楼下奶茶店朝你挥手）**：\n\n「我会{sm_trait}，你要不要尝尝我调的特色奶茶？」")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="interaction-box">', unsafe_allow_html=True)
                st.success(f"✨ **（TA在{sm_region}给你发了条跨区消息）**：\n\n「我会{sm_trait}，可惜我们隔得太远啦~」")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # 聊天历史
            if st.session_state.messages:
                st.markdown("**💭 对话历史**：")
                for msg in st.session_state.messages[-5:]:
                    st.caption(f"💬 {msg}")
            
            user_msg = st.text_input("💭 你想回复TA：", key="msg_input")
            col_send1, col_send2 = st.columns([3, 1])
            with col_send1:
                if user_msg and st.button("📤 发送消息", key="send_present", use_container_width=True):
                    # 贴合原文"假装匹配"机制
                    fake_chance = random.randint(1, 10)
                    if fake_chance > 8:
                        response = "（TA突然撤回消息）：「抱歉，我认错人了... 你和我要找的人好像。」"
                        st.session_state.messages.append(f"你：{user_msg}")
                        st.session_state.messages.append(f"TA：{response}")
                        st.warning(f"⚠️ {response}")
                    else:
                        responses = [
                            f"（TA秒回）：「{user_msg}？好巧！我也超喜欢这个！」",
                            f"（TA发了个表情包）：「{user_msg}... 我们果然心有灵犀！」",
                            f"（TA语音消息）：「哈哈，{user_msg}，这太有趣了！」",
                            f"（TA正在输入...）：「{user_msg}？这也正是我想说的！」"
                        ]
                        response = random.choice(responses)
                        st.session_state.messages.append(f"你：{user_msg}")
                        st.session_state.messages.append(f"TA：{response}")
                        st.info(f"💬 {response}")
                    st.rerun()
            with col_send2:
                if st.button("🎲 随机回复", key="random_reply", use_container_width=True):
                    random_replies = [
                        "你好呀！",
                        "真有趣！",
                        "我也有同感！",
                        "太巧了！",
                        "这是什么？",
                        "哈哈，有意思！"
                    ]
                    random_msg = random.choice(random_replies)
                    st.session_state.messages.append(f"你：{random_msg}")
                    fake_chance = random.randint(1, 10)
                    if fake_chance > 8:
                        response = "（TA突然撤回消息）：「抱歉，我认错人了...」"
                        st.session_state.messages.append(f"TA：{response}")
                        st.warning(f"⚠️ {response}")
                    else:
                        response = f"（TA秒回）：「{random_msg}？我也这么觉得！」"
                        st.session_state.messages.append(f"TA：{response}")
                        st.info(f"💬 {response}")
                    st.rerun()
        
        # 清空对话按钮
        if st.session_state.messages:
            if st.button("🗑️ 清空对话历史", key="clear_chat"):
                st.session_state.messages = []
                st.rerun()


# ---------------------- 5. 主题槽点弹窗（点击触发） ----------------------
st.divider()
with st.expander("⚠️ 这个设定的「噩梦」真相（点击查看）", expanded=False):
    st.markdown("""
    <div style="background: #fff3cd; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #ffc107;">
    <h4>🌑 黑暗设定解析</h4>
    """, unsafe_allow_html=True)
    st.markdown("""
    1. **💀 时空陷阱**：95%的伴侣要么已死，要么还没出生，你永远等不到；  
    2. **🎰 概率骗局**：即使同年代，你遇到TA的概率≈中彩票头奖；  
    3. **👥 社会异化**：多数人会"假结婚"掩饰孤独，超市收银员会被当"匹配工具"；  
    4. **💰 资源垄断**：只有富人能花钱买"匹配时间"，穷人只能听天由命。
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# 底部提示
st.divider()
st.caption("💡 提示：每次匹配都是全新的命运，你的选择决定了唯一伴侣的时空坐标")