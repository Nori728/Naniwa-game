import streamlit as st
import random

# -----------------------------------------------------------------------------
# 1. 页面基本配置与样式
# -----------------------------------------------------------------------------
st.set_page_config(page_title="偶像专属心动企划", page_icon="💖", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%);
    }
    .main-header {
        font-size: 2.2rem;
        color: #e11d48;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0;
    }
    .sub-header {
        text-align: center;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .card-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 2. 7人全员基础数据源与写真
# -----------------------------------------------------------------------------
MEMBERS = {
    "丈君": {"trait": "搞笑又可靠的大哥哥", "color": "蓝色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRxeLPXR2kAxnf8Z0uNFWIH7j_vjPcrr8Eg1qWtaTSoPKTvTMcZtXXX6Kn&s=10"},
    "大酱": {"trait": "热情太阳般的 C 位", "color": "红色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEiQYHWo7za_O6O-FerVkj5mA2s49UBL3hj_Tfmu-npd2yfIz1OJSCHD8n&s=10"},
    "布丁": {"trait": "温柔体贴又元气的队长", "color": "绿色", "img": "https://img-mdpr.freetls.fastly.net/article/H0CW/nm/H0CW_-CrOagXoRlSyQPOD6_zSqLjGNjyrfLRLWlqECw.jpg?width=750"},
    "高恭": {"trait": "自恋又帅气的傲娇少年", "color": "紫色", "img": "https://img-mdpr.freetls.fastly.net/article/d4sb/nm/d4sbe7H-P8R6sUQpAshcntVT8-h0ZPcuMe3icV8aOm4.jpg?width=750"},
    "流星": {"trait": "眼睛会闪光的小恶魔", "color": "橙色", "img": "https://oggi.jp/wp-content/uploads/2023/03/DMA-DSC00151_2-2.jpg"},
    "米七": {"trait": "高挑清纯的长腿王子", "color": "粉色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvYWZ1rSHkldisNtmwbvxSYNjR8FWjj4_wdyKxw84_h0SabJN81yYpsGXL&s=10"},
    "谦杜": {"trait": "时尚又有主见的末子", "color": "黄色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRs8ILDomyP9A6WZPtgig1e6IyPPmSpxS8HSYiRImU0uSqXicpvyNrHV8A&s=10"},
}

ROLES = ["经纪人", "青梅竹马", "在日留学生or打工人"]

# 🌟 在这里自由修改总幕数（例如改成 5 代表五个晚上的长线剧情！）
MAX_ACT = 5

# -----------------------------------------------------------------------------
# 3. 核心剧情数据库 (支持前几幕精细定制，后续幕数自动智能扩展)
# -----------------------------------------------------------------------------
DETAILED_STORIES = {
    "经纪人": {
        "丈君": {
            1: {
                "title": "🌙 第一夜：后台行程与初次晚归",
                "choices": [
                    ("顺着他的话打趣：『紧张的话，要不要我给你一个爱的鼓励？』", "『呜哇，你别突然这么正经，搞得我心跳比待会录节目还快！』", 20),
                    ("递上提词卡严肃道：『少废话，第三个笑话梗你刚才排练又忘词了！』", "『好啦好啦，金牌经纪人大人饶命！有你在后台盯着，我绝对不会砸场子的！』", 15),
                    ("默默递上一杯冰麦茶不说话", "『还是你最懂我……虽然平时总管着我，但其实最离不开的就是你啦。』", 25)
                ]
            },
            2: {
                "title": "🌙 第二夜：深夜保姆车的后座独处",
                "choices": [
                    ("假装靠在车窗边闭目养神", "（悄悄把肩膀挪过来让你靠着）『累了就靠一会儿吧……有我在，安心睡到终点站。』", 25),
                    ("翻看接下来的行程表轻声提醒他早点休息", "『工作狂经纪人小姐，现在是私人时间，不许再看文件了，快看着我。』", 20),
                    ("小声调侃他今天在节目里的搞笑失误", "『喂！那是个意外！不过……能让你一直笑着，就算出糗也值了。』", 15)
                ]
            },
            3: {
                "title": "🌙 第三夜：通告间隙的秘密天台",
                "choices": [
                    ("迎上他的目光：『怎么了？是有新的通告安排吗？』", "『以后不只是工作上的搭档……我的余生，我也想申请做你专属的唯一伴侣。』", 30),
                    ("有些害羞地别过头去", "『别把脸转过去嘛……我好不容易鼓起勇气对你表白，给点面子笑一笑好不好？』", 25)
                ]
            }
            # 如果 MAX_ACT 设为了 4 或 5，第 4、5 夜没写的话，系统会自动智能延伸生成对应晚上的甜蜜剧情！
        }
    }
}

# -----------------------------------------------------------------------------
# 4. 智能动态剧情生成器（核心：解决幕数变多时不用手动写完所有角色的痛点）
# -----------------------------------------------------------------------------
def get_scene_data(role, member, act):
    # 先尝试从预设里找
    role_stories = DETAILED_STORIES.get(role, {})
    member_story = role_stories.get(member, {})
    if act in member_story:
        return member_story[act]
    
    # 如果没写，根据当前是第几个晚上自动智能扩展生成一段符合氛围的剧情
    auto_titles = {
        2: f"🌙 第二夜：私下里的单独相处",
        3: f"🌙 第三夜：心跳加速的近距离试探",
        4: f"🌙 第四夜：空气中弥漫的暧昧微光",
        5: f"🌙 第五夜：突破防线的命运交织",
    }
    title = auto_titles.get(act, f"🌙 第 {act} 夜：专属两人的浪漫羁绊")
    
    choices = [
        ("微笑着向他靠近一步，听听他的心跳", f"『怎么突然靠这么近……不过，我一点也不讨厌，甚至想让你抱得更紧一点。』", 25),
        ("调侃他最近越来越会说情话了", f"『对别人我可不说，只对你一个人这样……承认吧，你是不是也心动了？』", 20),
        ("安静地看着他，把选择权交给他", f"『别用这种眼神看着我，我会忍不住想把你彻底藏进我的未来里。』", 30)
    ]
    return {"title": title, "choices": choices}

# -----------------------------------------------------------------------------
# 5. Session State 初始化
# -----------------------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0  
if "player_role" not in st.session_state:
    st.session_state.player_role = ""
if "target_member" not in st.session_state:
    st.session_state.target_member = ""
if "current_act" not in st.session_state:
    st.session_state.current_act = 1
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "dialogue_history" not in st.session_state:
    st.session_state.dialogue_history = []
if "gacha_inventory" not in st.session_state:
    st.session_state.gacha_inventory = []

# -----------------------------------------------------------------------------
# 6. 侧边栏：心动抽卡系统
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎁 偶像心动扭蛋机")
    st.write("消耗心动值抽取限定写真与羁绊道具！")
    
    if st.button("✨ 抽一次卡 (消耗 10 积分)", use_container_width=True):
        if st.session_state.total_score >= 10:
            st.session_state.total_score -= 10
            rewards = [
                "【SSR限定】丈君·后台专属对视签名照 📸",
                "【SSR限定】大酱·舞台C位闪耀拍立得 ✨",
                "【SR稀有】布丁·亲手做的爱心铜锣烧 🍪",
                "【SR稀有】高恭·傲娇的后台解暑冰饮 🥤",
                "【SSR限定】流星·眨眼Wink限定小卡 💖",
                "【SSR限定】米七·长腿王子私服私密写真 📘",
                "【SR稀有】谦杜·吉他弹唱手写简谱 🎶"
            ]
            get_card = random.choice(rewards)
            st.session_state.gacha_inventory.append(get_card)
            st.success(f"恭喜抽中：{get_card}")
        else:
            st.warning("当前心动积分不足 10 分，快去剧情里增加好感吧！")
            
    if st.session_state.gacha_inventory:
        st.markdown("---")
        st.markdown(f"**🎒 我的抽卡背包 ({len(st.session_state.gacha_inventory)}张)**")
        for idx, card in enumerate(st.session_state.gacha_inventory):
            st.caption(f"{idx+1}. {card}")

# -----------------------------------------------------------------------------
# 7. 页面核心逻辑与渲染
# -----------------------------------------------------------------------------
st.markdown('<p class="main-header">💖 偶像专属心动企划</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">全员 7 人满配 ＋ 多晚长线剧情引擎 (当前总计设定为：{MAX_ACT} 夜)</p>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 阶段 0：选择身份
# -----------------------------------------------------------------------------
if st.session_state.step == 0:
    st.subheader("🎭 第一步：请选择你在故事中的身份：")
    selected_role = st.radio("你的身份定位：", ROLES)
    
    if st.button("确认身份，挑选心动对象 ➔", type="primary", use_container_width=True):
        st.session_state.player_role = selected_role
        st.session_state.step = 1
        st.rerun()

# -----------------------------------------------------------------------------
# 阶段 1：选择攻略对象
# -----------------------------------------------------------------------------
elif st.session_state.step == 1:
    st.subheader(f"💖 第二步：当前身份【{st.session_state.player_role}】，请从下方 7 位成员中选择你想攻略的对象：")
    
    chosen_member = st.selectbox("选择你的心动男主角：", list(MEMBERS.keys()))
    
    m_info = MEMBERS[chosen_member]
    st.markdown(
        f"""
        <div class="card-box" style="text-align: center;">
            <img src="{m_info['img']}" width="100%" style="border-radius: 12px; max-height: 300px; object-fit: cover;">
            <p style="margin-top: 10px; font-weight: bold; font-size: 1.1rem; color: #e11d48;">✨ {chosen_member} ({m_info['trait']})</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 重新选择身份"):
            st.session_state.step = 0
            st.rerun()
    with col2:
        if st.button("开启专属恋爱长线剧情 ➔", type="primary"):
            st.session_state.target_member = chosen_member
            st.session_state.current_act = 1
            st.session_state.total_score = 30  # 初始赠送积分，方便去抽卡玩
            st.session_state.dialogue_history = []
            st.session_state.step = 2  
            st.rerun()

# -----------------------------------------------------------------------------
# 阶段 2 及以后：动态多晚剧情幕推进
# -----------------------------------------------------------------------------
elif st.session_state.step >= 2 and st.session_state.step < 5:
    role = st.session_state.player_role
    member = st.session_state.target_member
    act = st.session_state.current_act
    
    m_info = MEMBERS[member]
    
    # 调动智能动态剧情生成函数（没写的幕数会自动扩展渲染）
    scene_data = get_scene_data(role, member, act)
    
    st.markdown(f"### 🎭 当前身份：【{role}】 | 攻略对象：**{member}** (第 {act}/{MAX_ACT} 夜)")
    st.info(f"💡 当前心动积分：**{st.session_state.total_score} 分**（快去左侧边栏使用扭蛋机抽卡吧！）")
    
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 15px;">
            <img src="{m_info['img']}" width="100%" style="border-radius: 12px; max-height: 220px; object-fit: cover;">
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.subheader(scene_data["title"])
    
    if st.session_state.dialogue_history:
        st.markdown("---")
        for item in st.session_state.dialogue_history:
            st.markdown(f"💬 **你**：{item['choice_text']}")
            st.success(f"💖 **{member} 的回应**：{item['reply_text']}")
        st.markdown("---")
    
    st.markdown("👉 **请根据他的性格做出你的回应：**")
    for idx, (c_text, r_text, score_val) in enumerate(scene_data["choices"]):
        if st.button(c_text, key=f"choice_btn_{act}_{idx}", use_container_width=True):
            st.session_state.dialogue_history.append({
                "choice_text": c_text,
                "reply_text": r_text
            })
            st.session_state.total_score += score_val
            
            # 判断是否到达最后一幕
            if act < MAX_ACT:
                st.session_state.current_act += 1
            else:
                st.session_state.step = 5  # 达成最终结局结算
            st.rerun()

# -----------------------------------------------------------------------------
# 阶段 5：专属结局结算
# -----------------------------------------------------------------------------
elif st.session_state.step == 5:
    role = st.session_state.player_role
    member = st.session_state.target_member
    score = st.session_state.total_score
    m_info = MEMBERS[member]
    
    st.balloons()
    st.header("🏆 专属心动结局结算")
    st.success(f"在【{role}】身份下，你与 **{member}** 共同度过整整 {MAX_ACT} 个晚上的漫长羁绊，最终得分为：**{score} 分**！")
    
    st.markdown(
        f"""
        <div class="card-box" style="text-align: center;">
            <img src="{m_info['img']}" width="100%" style="border-radius: 12px; max-height: 320px; object-fit: cover;">
            <p style="margin-top: 15px; font-weight: bold; font-size: 1.2rem; color: #e11d48;">✨ 达成长线 HE 终极告白结局：【{member} × {role}】</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    ENDING_QUOTES = {
        "丈君": "『无论是聚光灯下的万人瞩目，还是这连续好几个夜晚的独自陪伴……只要你在我身旁，我就是最闪耀的那个。做我唯一的专属偏爱，好吗？』",
        "大酱": "『这些个日日夜夜谢谢你一直包容我、陪在我身旁。比起那些遥不可及的奖杯，我现在最想拥抱和拥有的，只有你一个。』",
        "布丁": "『好吃的布丁想分你一半，这几个晚上的温柔全部都给你！只要……你愿意把你的余生也分我一半！』",
        "高恭": "『在这漫长的长线相处里，在你面前，我不用扮演那个完美酷炫的大人。未来的路还很长，我想带着最真实的心，牵着你一直走下去。』",
        "流星": "『每一个夜晚的眨眼和微笑，都是只对你一个人的营业。不，不对……我对你的爱才不是营业，是百分之百的真心！』",
        "米七": "『每次累到想放弃的时候，只要看到你，我就能重新充满力量。这几个晚上的相伴让我确信，你就是我余生唯一的避风港。』",
        "谦杜": "『我写了那么多好听的旋律，这几个晚上的心跳就是最完美的灵感。这首为你而写的歌，你想听一辈子吗？』"
    }
    
    quote = ENDING_QUOTES.get(member, f"『能陪你度过这好几个夜晚，是我这辈子最幸运的奇迹。今后的每一天，我的眼里都只有你。』")
    
    st.markdown(
        f"""
        > {quote}
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        if st.button("🔄 重新攻略当前角色", use_container_width=True):
            st.session_state.current_act = 1
            st.session_state.total_score = 30
            st.session_state.dialogue_history = []
            st.session_state.step = 2
            st.rerun()
    with col_r2:
        if st.button("🏠 返回主菜单/更换身份", use_container_width=True):
            st.session_state.step = 0
            st.session_state.player_role = ""
            st.session_state.target_member = ""
            st.session_state.current_act = 1
            st.session_state.total_score = 0
            st.session_state.dialogue_history = []
            st.session_state.gacha_inventory = []
            st.rerun()
