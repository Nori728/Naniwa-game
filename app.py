import streamlit as st
import random

# -----------------------------------------------------------------------------
# 1. 页面基本配置与样式 (定制化浪漫背景与卡片阴影)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="偶像专属心动企划", page_icon="💖", layout="centered")

st.markdown(
    """
    <style>
    /* 全局浪漫背景渐变 */
    .stApp {
        background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 50%, #fce7f3 100%);
    }
    .main-header {
        font-size: 2.2rem;
        color: #e11d48;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
    }
    .sub-header {
        text-align: center;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .card-box {
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 8px 16px rgba(225, 29, 72, 0.08);
        margin-bottom: 20px;
        border: 1px solid #fbcfe8;
    }
    .gacha-box {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #fde68a;
        margin-bottom: 15px;
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
MAX_ACT = 4  # 幕数

# -----------------------------------------------------------------------------
# 3. Session State 初始化
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
    st.session_state.total_score = 30
if "dialogue_history" not in st.session_state:
    st.session_state.dialogue_history = []
if "inventory" not in st.session_state:
    st.session_state.inventory = []  # 道具与卡片背包
if "daily_gacha_result" not in st.session_state:
    st.session_state.daily_gacha_result = None

# -----------------------------------------------------------------------------
# 4. 智能动态剧情生成器
# -----------------------------------------------------------------------------
def get_scene_data(role, member, act):
    auto_titles = {
        1: f"🎬 第一幕：初次相遇与心动试探",
        2: f"🎬 第二幕：私下里的单独相处",
        3: f"🎬 第三幕：心跳加速的近距离对峙",
        4: f"🎬 第四幕：浪漫的终极告白契约",
    }
    title = auto_titles.get(act, f"🎬 第 {act} 幕：心动日常进展中")
    
    choices = [
        ("微笑着向他靠近一步，认真注视他的眼睛", f"『怎么突然靠这么近……不过，我一点也不讨厌。』", 20),
        ("调侃他今天的表情很有趣，开个小玩笑", f"『好啊你，居然敢笑话我！看我怎么“惩罚”你～』", 15),
        ("安静地陪伴在他身旁，递上一杯温水", f"『只要有你陪着，哪怕什么都不做也是最幸福的时光。』", 25)
    ]
    return {"title": title, "choices": choices}

# -----------------------------------------------------------------------------
# 5. 页面核心渲染
# -----------------------------------------------------------------------------
st.markdown('<p class="main-header">💖 浪花男子心动日常</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">✨ 每日运势抽卡 ＋ 道具增益 ＋ 沉浸互动剧情 (共 {MAX_ACT} 幕)</p>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 模块 A：每日运势与道具抽卡区 (仿照你截图中的灵动设计)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="gacha-box">
        <h3 style="margin-top:0; color:#b45309; font-size: 1.2rem;">🎲 每日运势与道具扭蛋机</h3>
        <p style="font-size: 0.9rem; color: #78350f; margin-bottom: 10px;">测测今天的心动成员，抽取专属恋爱道具为你增加剧情好感buff！</p>
    </div>
    """,
    unsafe_allow_html=True
)

col_g1, col_g2 = st.columns(2)
with col_g1:
    if st.button("✨ 测测今天大势心动成员", use_container_width=True):
        lucky_name, lucky_data = random.choice(list(MEMBERS.items()))
        st.session_state.daily_gacha_result = (lucky_name, lucky_data)

with col_g2:
    if st.button("🎁 抽取心动道具 (消耗10积分)", use_container_width=True):
        if st.session_state.total_score >= 10:
            st.session_state.total_score -= 10
            items_pool = [
                ("🍬 恋爱加倍糖果", "下一次选择获得双倍好感积分！"),
                ("🎧 读心耳机", "能精准洞察他内心的真实羞涩台词。"),
                ("📸 SSR限定拍立得", "增加全盘浪漫氛围与结局甜度。"),
                ("🥤 冰爽解暑饮料", "恢复元气，解锁隐藏温柔互动。")
            ]
            item_name, item_desc = random.choice(items_pool)
            st.session_state.inventory.append(item_name)
            st.success(f"抽中道具：{item_name}！({item_desc})")
        else:
            st.warning("心动积分不足 10 分，快去下方剧情里累积吧！")

# 如果抽出了今日大势成员，展示其写真与运势卡片
if st.session_state.daily_gacha_result:
    lname, ldata = st.session_state.daily_gacha_result
    st.markdown(
        f"""
        <div class="card-box" style="text-align: center;">
            <p style="color: #e11d48; font-weight: bold; font-size: 1.1rem;">🌟 今日运势爆棚中：{lname} ({ldata['trait']})</p>
            <img src="{ldata['img']}" width="100%" style="border-radius: 12px; max-height: 250px; object-fit: cover; margin-top: 5px;">
        </div>
        """,
        unsafe_allow_html=True
    )

# 展示当前背包道具
if st.session_state.inventory:
    st.markdown(f"**🎒 我的道具背包：** " + " | ".join([f"`{i}`" for i in st.session_state.inventory]))

st.markdown("---")

# -----------------------------------------------------------------------------
# 阶段 0：选择身份
# -----------------------------------------------------------------------------
if st.session_state.step == 0:
    st.subheader("📖 开启心动互动剧情")
    st.markdown("### 1️⃣ 请选择你的身份：")
    selected_role = st.selectbox("身份列表", ROLES)
    
    if st.button("确认身份，进入下一步 ➔", type="primary", use_container_width=True):
        st.session_state.player_role = selected_role
        st.session_state.step = 1
        st.rerun()

# -----------------------------------------------------------------------------
# 阶段 1：选择攻略对象
# -----------------------------------------------------------------------------
elif st.session_state.step == 1:
    st.subheader(f"📖 开启心动互动剧情")
    st.markdown(f"当前身份：【**{st.session_state.player_role}**】")
    st.markdown("### 2️⃣ 请选择你想攻略的成员：")
    
    chosen_member = st.selectbox("成员列表", list(MEMBERS.keys()))
    m_info = MEMBERS[chosen_member]
    
    st.markdown(
        f"""
        <div class="card-box" style="text-align: center;">
            <img src="{m_info['img']}" width="100%" style="border-radius: 12px; max-height: 280px; object-fit: cover;">
            <p style="margin-top: 10px; font-weight: bold; font-size: 1.1rem; color: #e11d48;">✨ {chosen_member} (特征：{m_info['trait']} | 专属色：{m_info['color']})</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("⬅️ 重新选择身份"):
            st.session_state.step = 0
            st.rerun()
    with col_b2:
        if st.button("✨ 进入多幕专属剧情 ➔", type="primary"):
            st.session_state.target_member = chosen_member
            st.session_state.current_act = 1
            st.session_state.dialogue_history = []
            st.session_state.step = 2  
            st.rerun()

# -----------------------------------------------------------------------------
# 阶段 2 及以后：动态剧情幕推进
# -----------------------------------------------------------------------------
elif st.session_state.step >= 2 and st.session_state.step < 5:
    role = st.session_state.player_role
    member = st.session_state.target_member
    act = st.session_state.current_act
    m_info = MEMBERS[member]
    
    scene_data = get_scene_data(role, member, act)
    
    st.markdown(f"### 💖 【{role}】 × **{member}** (第 {act}/{MAX_ACT} 幕)")
    st.info(f"💡 当前心动指数：**{st.session_state.total_score} 分** (可去上方抽道具或写真)")
    
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 15px;">
            <img src="{m_info['img']}" width="100%" style="border-radius: 12px; max-height: 200px; object-fit: cover;">
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
    
    st.markdown("👉 **请做出你的回应选择：**")
    for idx, (c_text, r_text, score_val) in enumerate(scene_data["choices"]):
        if st.button(c_text, key=f"choice_btn_{act}_{idx}", use_container_width=True):
            # 道具联动效果：如果背包里有“恋爱加倍糖果”，单次加分翻倍！
            if "🍬 恋爱加倍糖果" in st.session_state.inventory:
                score_val *= 2
                st.toast("🍬 触发加倍糖果效果，好感度翻倍！", icon="✨")
            
            st.session_state.dialogue_history.append({
                "choice_text": c_text,
                "reply_text": r_text
            })
            st.session_state.total_score += score_val
            
            if act < MAX_ACT:
                st.session_state.current_act += 1
            else:
                st.session_state.step = 5  # 结算
            st.rerun()

# -----------------------------------------------------------------------------
# 阶段 5：结算画面
# -----------------------------------------------------------------------------
elif st.session_state.step == 5:
    role = st.session_state.player_role
    member = st.session_state.target_member
    score = st.session_state.total_score
    m_info = MEMBERS[member]
    
    st.balloons()
    st.header("🏆 结算：HE 甜蜜告白结局")
    st.success(f"在【{role}】的故事中，你与 **{member}** 的最终心动指数为：**{score} 分**！")
    
    st.markdown(
        f"""
        <div class="card-box" style="text-align: center;">
            <img src="{m_info['img']}" width="100%" style="border-radius: 12px; max-height: 300px; object-fit: cover;">
            <p style="margin-top: 15px; font-weight: bold; font-size: 1.2rem; color: #e11d48;">✨ 达成 HE 专属告白：【{member} × {role}】</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        > 『不管别人怎么看，你才是我最重要的选择！在灯光下的角落里，紧紧握住你的手，这就是属于我们的甜蜜恋情。』
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        if st.button("🔄 重新体验当前角色", use_container_width=True):
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
            st.session_state.total_score = 30
            st.session_state.dialogue_history = []
            st.session_state.inventory = []
            st.session_state.daily_gacha_result = None
            st.rerun()
