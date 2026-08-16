import streamlit as st
import random
import time
import os

# -----------------------------------------------------------------------------
# 1. 页面基本配置与样式 (浪漫风格)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="浪花男子 · 专属心动企划", page_icon="💖", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    }
    .main-header {
        font-size: 2.5rem;
        color: #ff758c;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0;
    }
    .sub-header {
        text-align: center;
        color: #888;
        margin-bottom: 2rem;
    }
    .ur-card { color: #ff007f; font-weight: bold; text-shadow: 0 0 5px #ffb6c1; }
    .ssr-card { color: #ffa500; font-weight: bold; }
    .sr-card { color: #800080; font-weight: bold; }
    .r-card { color: #4169e1; }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 2. 基础数据源定义 (浪花男子)
# -----------------------------------------------------------------------------
MEMBERS = {
    "丈君 (Fujiwara Joichiro)": {"color": "💙", "trait": "搞笑又可靠的大哥哥", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRxeLPXR2kAxnf8Z0uNFWIH7j_vjPcrr8Eg1qWtaTSoPKTvTMcZtXXX6Kn&s=10"},
    "大酱 (Nishihata Daigo)": {"color": "🔴", "trait": "热情太阳般的 C 位", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEiQYHWo7za_O6O-FerVkj5mA2s49UBL3hj_Tfmu-npd2yfIz1OJSCHD8n&s=10"},
    "布丁 (Ohashi Kazuya)": {"color": "💚", "trait": "温柔体贴的队长", "img": "https://img-mdpr.freetls.fastly.net/article/H0CW/nm/H0CW_-CrOagXoRlSyQPOD6_zSqLjGNjyrfLRLWlqECw.jpg?width=750"},
    "高恭 (Takahashi Kyohei)": {"color": "💜", "trait": "自恋又帅气的八嘎", "img": "https://img-mdpr.freetls.fastly.net/article/d4sb/nm/d4sbe7H-P8R6sUQpAshcntVT8-h0ZPcuMe3icV8aOm4.jpg?width=750"},
    "流星 (Onishi Ryusei)": {"color": "🧡", "trait": "眼睛会闪光的小恶魔", "img": "https://oggi.jp/wp-content/uploads/2023/03/DMA-DSC00151_2-2.jpg"},
    "米七 (Michieda Shunsuke)": {"color": "💖", "trait": "高挑的长腿王子", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvYWZ1rSHkldisNtmwbvxSYNjR8FWjj4_wdyKxw84_h0SabJN81yYpsGXL&s=10"},
    "谦杜 (Nagao Kento)": {"color": "💛", "trait": "时尚又有主见的末子", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRs8ILDomyP9A6WZPtgig1e6IyPPmSpxS8HSYiRImU0uSqXicpvyNrHV8A&s=10"},
}

ROLES = ["经纪人", "粉丝 / 地下恋", "青梅竹马", "在日留学生 / 打工人", "✨ 自定义身份..."]

# -----------------------------------------------------------------------------
# 3. Session State 初始化 (用于保存抽卡背包和聊天记录)
# -----------------------------------------------------------------------------
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "scenario_set" not in st.session_state:
    st.session_state.scenario_set = False

# -----------------------------------------------------------------------------
# 页面头部
# -----------------------------------------------------------------------------
st.markdown('<p class="main-header">✨ 浪花男子 · 专属心动企划 ✨</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">抽卡收集羁绊 × 自由设定属于你们的故事</p>', unsafe_allow_html=True)

# 使用 Tabs 将【抽卡系统】和【自由剧情系统】分开
tab1, tab2 = st.tabs(["🎰 心动羁绊抽卡", "📖 自由剧情 / 互动聊天"])

# =============================================================================
# TAB 1: 抽卡 / 抽奖代码 (原汁原味的抽卡系统)
# =============================================================================
with tab1:
    st.subheader("💌 抽取你的专属羁绊卡片")
    st.write("概率公示：UR(2%) | SSR(8%) | SR(30%) | R(60%)")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    def do_gacha(times):
        results = []
        has_ur_ssr = False
        for _ in range(times):
            rand = random.random()
            if rand <= 0.02:
                rarity = "UR"
                has_ur_ssr = True
            elif rand <= 0.10:
                rarity = "SSR"
                has_ur_ssr = True
            elif rand <= 0.40:
                rarity = "SR"
            else:
                rarity = "R"
            
            member = random.choice(list(MEMBERS.keys()))
            card = {"member": member, "rarity": rarity, "time": time.strftime("%H:%M:%S")}
            results.append(card)
            st.session_state.inventory.append(card)
            
        if has_ur_ssr:
            st.balloons() # 抽到高级卡放气球
            
        return results

    # 抽卡按钮
    with col1:
        if st.button("✨ 单次抽取 (1连)", use_container_width=True):
            with st.spinner("抽卡中..."):
                time.sleep(0.5)
                pulls = do_gacha(1)
                st.success(f"获得了: **{pulls[0]['rarity']}** - {pulls[0]['member']}")
    
    with col2:
        if st.button("🌟 奇迹祈愿 (10连)", type="primary", use_container_width=True):
            with st.spinner("光芒汇聚中..."):
                time.sleep(1)
                pulls = do_gacha(10)
                st.write("### 十连结果：")
                for p in pulls:
                    if p['rarity'] == "UR":
                        st.markdown(f"<span class='ur-card'>✨ UR ✨ | {p['member']} (专属心动瞬间)</span>", unsafe_allow_html=True)
                    elif p['rarity'] == "SSR":
                        st.markdown(f"<span class='ssr-card'>⭐ SSR ⭐ | {p['member']} (舞台闪耀时刻)</span>", unsafe_allow_html=True)
                    elif p['rarity'] == "SR":
                        st.markdown(f"<span class='sr-card'>🌙 SR | {p['member']} (日常相伴)</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span class='r-card'>☁️ R | {p['member']} (一个微笑)</span>", unsafe_allow_html=True)
                        
    with col3:
        if st.button("🎒 清空背包", use_container_width=True):
            st.session_state.inventory = []
            st.rerun()

    st.divider()
    st.write(f"**我的羁绊背包** (已收集 {len(st.session_state.inventory)} 张卡片):")
    # 统计展示背包
    if st.session_state.inventory:
        ur_count = sum(1 for c in st.session_state.inventory if c['rarity'] == 'UR')
        ssr_count = sum(1 for c in st.session_state.inventory if c['rarity'] == 'SSR')
        st.write(f"🏆 UR: `{ur_count}` 张 | ⭐ SSR: `{ssr_count}` 张")
        with st.expander("查看所有卡片"):
            for idx, c in enumerate(reversed(st.session_state.inventory)):
                st.write(f"{idx+1}. [{c['time']}] {c['rarity']} - {c['member']}")
    else:
        st.info("背包空空如也，快去抽卡吧！")


# =============================================================================
# TAB 2: 自由设定 + 动态聊天系统
# =============================================================================
with tab2:
    if not st.session_state.scenario_set:
        st.subheader("🛠️ 设定属于你们的背景与身份")
        
        # 1. 选对象
        target_member = st.selectbox("💖 攻略对象：", list(MEMBERS.keys()))
        
        # 2. 选身份
        selected_role = st.selectbox("🎭 你的身份设定：", ROLES)
        if selected_role == "✨ 自定义身份...":
            user_role = st.text_input("请输入你的自定义身份（比如：新来的化妆师助理、失忆的青梅竹马...）")
        else:
            user_role = selected_role
            
        # 3. 选背景
        story_bg = st.text_area(
            "🎬 故事背景设定（写得越详细越有代入感）：", 
            placeholder="例如：\n昨晚刚结束东蛋演唱会，庆功宴上大家都喝了点酒。此刻深夜两点，只有我们两个人在酒店顶楼的阳台上吹风……",
            height=100
        )
        
        if st.button("🚀 生成世界观，开始互动！", type="primary"):
            if not user_role or not story_bg:
                st.warning("请填写完整的身份和背景故事哦！")
            else:
                st.session_state.scenario_set = True
                st.session_state.current_member = target_member
                st.session_state.current_role = user_role
                st.session_state.story_bg = story_bg
                
                # 初始化第一句开场白
                m_info = MEMBERS[target_member]
                intro_msg = f"*(背景音：{story_bg})*\n\n*(你现在的身份是：{user_role}。{target_member.split(' ')[0]} 看了看你，主动开口了：)*\n\n「喂……你在这里发什么呆呢？」"
                st.session_state.chat_history = [{"role": "assistant", "content": intro_msg}]
                st.rerun()

    else:
        # 进入聊天互动界面
        m_name = st.session_state.current_member.split(' ')[0]
        st.subheader(f"💬 正在与 {m_name} 互动中...")
        st.caption(f"📍 **背景**: {st.session_state.story_bg} | 🎭 **你的身份**: {st.session_state.current_role}")
        
        if st.button("↩️ 重新设定故事背景"):
            st.session_state.scenario_set = False
            st.session_state.chat_history = []
            st.rerun()
            
        st.divider()
        
        # 显示聊天记录
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                with st.chat_message("user", avatar="🌸"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant", avatar=MEMBERS[st.session_state.current_member]["color"]):
                    st.write(message["content"])
                    
        # 聊天输入框
        if prompt := st.chat_input(f"对 {m_name} 说点什么... (按回车发送)"):
            # 1. 记录用户的发言
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            with st.chat_message("user", avatar="🌸"):
                st.write(prompt)
                
            # 2. 生成对象的回复 (这里使用了一个简单的本地动态回复逻辑，你后续也可以接入大模型API)
            with st.chat_message("assistant", avatar=MEMBERS[st.session_state.current_member]["color"]):
                with st.spinner(f"{m_name} 正在输入..."):
                    time.sleep(1) # 模拟思考时间
                    
                    # 简单的回复生成器：根据成员特征和你的话进行互动
                    trait = MEMBERS[st.session_state.current_member]["trait"]
                    responses = [
                        f"（耳朵微微发红，看着你）……你突然说这个，犯规了吧。",
                        f"（轻笑了一声，顺势靠近你）既然你是我的 {st.session_state.current_role}，那我现在可以提一点任性的要求吗？",
                        f"（认真地盯着你的眼睛）其实刚才我就想说了，你这样看着我……我会误会的哦。",
                        f"（愣了一下，随后笑得眉眼弯弯）笨蛋，我知道啦。接下来交给我吧！",
                        f"（伸手轻轻揉了揉你的头发）别多想，有我在呢。"
                    ]
                    reply = random.choice(responses)
                    
                    st.write(reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
