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
        background: rgba(255, 255, 255, 0.95);
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
# 2. 基础数据源 (7人全员数据)
# -----------------------------------------------------------------------------
MEMBERS = {
    "丈君": {"trait": "搞笑又可靠的大哥哥", "color": "蓝色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRxeLPXR2kAxnf8Z0uNFWIH7j_vjPcrr8Eg1qWtaTSoPKTvTMcZtXXX6Kn&s=10"},
    "大酱": {"trait": "热情太阳般的 C 位", "color": "红色", "img": "https://gingerweb.jp/wp-content/uploads/2023/06/nishihatadaigo.jpg"},
    "布丁": {"trait": "温柔体贴又元气的队长", "color": "绿色", "img": "https://img-mdpr.freetls.fastly.net/article/H0CW/nm/H0CW_-CrOagXoRlSyQPOD6_zSqLjGNjyrfLRLWlqECw.jpg?width=750"},
    "高恭": {"trait": "自恋又帅气的傲娇少年", "color": "紫色", "img": "https://img-mdpr.freetls.fastly.net/article/d4sb/nm/d4sbe7H-P8R6sUQpAshcntVT8-h0ZPcuMe3icV8aOm4.jpg?width=750"},
    "流星": {"trait": "眼睛会闪光的小恶魔", "color": "橙色", "img": "https://oggi.jp/wp-content/uploads/2023/03/DMA-DSC00151_2-2.jpg"},
    "米七": {"trait": "高挑清纯的长腿王子", "color": "粉色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvYWZ1rSHkldisNtmwbvxSYNjR8FWjj4_wdyKxw84_h0SabJN81yYpsGXL&s=10"},
    "谦杜": {"trait": "时尚又有主见的末子", "color": "黄色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRs8ILDomyP9A6WZPtgig1e6IyPPmSpxS8HSYiRImU0uSqXicpvyNrHV8A&s=10"},
}

ROLES = ["经纪人", "青梅竹马", "在日留学生or打工人"]
MAX_ACT = 4

# -----------------------------------------------------------------------------
# 3. 剧情库
# -----------------------------------------------------------------------------
STORIES = {
    1: {
        "title": "🎬 第一幕：后台初遇与心动试探",
        "choices": [
            ("微笑着向他靠近一步，认真注视他的眼睛", "『怎么突然靠这么近……不过，我一点也不讨厌。』", 20),
            ("调侃他今天的表情很有趣，开个小玩笑", "『好啊你，居然敢笑话我！看我怎么“惩罚”你～』", 15),
            ("安静地陪伴在他身旁，递上一杯温水", "『只要有你陪着，哪怕什么都不做也是最幸福的时光。』", 25)
        ]
    },
    2: {
        "title": "🎬 第二幕：私下里的单独相处",
        "choices": [
            ("顺着他的话轻声安慰，拍拍他的肩膀", "『有你在身边听我倾诉，真的好安心。』", 20),
            ("假装生气地双手叉腰：『不许这么没自信！』", "『好好好听你的！只要你一瞪眼我就投降行了吧～』", 15),
            ("默默递上一张纸巾和一颗糖果", "『甜甜的糖果和你一样，能治愈我所有的疲惫。』", 25)
        ]
    },
    3: {
        "title": "🎬 第三幕：心跳加速的近距离对峙",
        "choices": [
            ("直视他的目光，毫不退缩地反问", "『被你这样盯着，我的心跳快得连台词都快忘光了……』", 25),
            ("害羞地低下头避开视线，耳根通红", "『别用这种犯规的眼神看我嘛，我会忍不住想把你藏起来。』", 20),
            ("故意转移话题调侃他：『好啦，快去准备下一个通告！』", "『就知道转移话题！不过……私下里我只想把所有的温柔都留给你。』", 15)
        ]
    },
    4: {
        "title": "🎬 第四幕：浪漫的终极告白契约",
        "choices": [
            ("主动伸出手与他十指相扣：『我愿意。』", "『太好了……这一次，我绝对不会再放开你的手。』", 30),
            ("眼眶微热，笑着点头答应", "『不许哭哦，从今以后，我的未来里全部都是你。』", 25),
            ("深情地靠进他的怀里", "『嗯，以后的每一个日日夜夜，我们都要永远在一起。』", 35)
        ]
    }
}

# -----------------------------------------------------------------------------
# 4. Session State 初始化
# -----------------------------------------------------------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "menu"  # menu, story, result
if "player_role" not in st.session_state:
    st.session_state.player_role = ROLES[0]
if "target_member" not in st.session_state:
    st.session_state.target_member = "大酱"
if "current_act" not in st.session_state:
    st.session_state.current_act = 1
if "total_score" not in st.session_state:
    st.session_state.total_score = 30
if "dialogue_history" not in st.session_state:
    st.session_state.dialogue_history = []
if "inventory" not in st.session_state:
    st.session_state.inventory = []  # 存储道具名称列表
if "active_buff" not in st.session_state:
    st.session_state.active_buff = None  # 当前生效的道具效果
if "daily_gacha_result" not in st.session_state:
    st.session_state.daily_gacha_result = None

# -----------------------------------------------------------------------------
# 5. 页面核心渲染
# -----------------------------------------------------------------------------
st.markdown('<p class="main-header">💖 浪花男子心动日常</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">✨ 每日运势抽卡 ＋ 自主道具背包 ＋ 沉浸互动剧情 (共 {MAX_ACT} 幕)</p>', unsafe_allow_html=True)

# 抽卡与扭蛋区域
st.markdown(
    """
    <div class="gacha-box">
        <h3 style="margin-top:0; color:#b45309; font-size: 1.2rem;">🎲 每日运势与道具扭蛋机</h3>
        <p style="font-size: 0.9rem; color: #78350f; margin-bottom: 10px;">测测今天的心动成员，消耗10积分抽取恋爱道具，并在背包中手动点击使用！</p>
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
            st.success(f"成功获得：{item_name}！(已存入下方背包)")
        else:
            st.warning("心动积分不足 10 分，快去下方剧情里累积吧！")

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

# -----------------------------------------------------------------------------
# 🎒 可交互的自主道具背包区域
# -----------------------------------------------------------------------------
if st.session_state.inventory:
    st.markdown("### 🎒 我的道具背包（点击按钮手动使用）")
    
    # 显示当前生效中的 Buff
    if st.session_state.active_buff:
        st.info(f"✨ **当前生效中的道具Buff**：`{st.session_state.active_buff}` —— 将在你的下一次选择中触发！")
    
    # 遍历背包里的每一个道具，为每个道具生成一个“使用”按钮
    for i, item in enumerate(list(st.session_state.inventory)):
        col_item1, col_item2 = st.columns([3, 1])
        with col_item1:
            st.markdown(f"**{item}**")
        with col_item2:
            if st.button(f"✨ 使用", key=f"use_item_{i}_{item}"):
                # 把该道具设为当前生效的Buff，并从背包中移除
                st.session_state.active_buff = item
                st.session_state.inventory.remove(item)
                st.success(f"已成功使用【{item}】！请在下方剧情中做出回应吧。")
                st.rerun()
    st.markdown("---")

# -----------------------------------------------------------------------------
# 菜单阶段：选择身份与攻略对象
# -----------------------------------------------------------------------------
if st.session_state.stage == "menu":
    st.subheader("📖 开启心动互动剧情")
    
    selected_role = st.selectbox("1️⃣ 请选择你的身份：", ROLES)
    selected_member = st.selectbox("2️⃣ 请选择你想攻略的成员：", list(MEMBERS.keys()))
    
    m_info = MEMBERS[selected_member]
    st.markdown(
        f"""
        <div class="card-box" style="text-align: center;">
            <img src="{m_info['img']}" width="100%" style="border-radius: 12px; max-height: 280px; object-fit: cover;">
            <p style="margin-top: 10px; font-weight: bold; font-size: 1.1rem; color: #e11d48;">✨ {selected_member} (特征：{m_info['trait']} | 专属色：{m_info['color']})</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if st.button("✨ 确认并进入多幕专属剧情 ➔", type="primary", use_container_width=True):
        st.session_state.player_role = selected_role
        st.session_state.target_member = selected_member
        st.session_state.current_act = 1
        st.session_state.dialogue_history = []
        st.session_state.stage = "story"
        st.rerun()

# -----------------------------------------------------------------------------
# 剧情互动阶段
# -----------------------------------------------------------------------------
elif st.session_state.stage == "story":
    role = st.session_state.player_role
    member = st.session_state.target_member
    act = st.session_state.current_act
    m_info = MEMBERS[member]
    
    scene_data = STORIES.get(act, STORIES[1])
    
    st.markdown(f"### 💖 【{role}】 × **{member}** (第 {act}/{MAX_ACT} 幕)")
    st.info(f"💡 当前心动指数（积分）：**{st.session_state.total_score} 分**")
    
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
            # 检查玩家是否手动使用了“恋爱加倍糖果”
            if st.session_state.active_buff == "🍬 恋爱加倍糖果":
                score_val *= 2
                st.toast("🍬 成功触发加倍糖果！本次好感度积分翻倍！", icon="✨")
                st.session_state.active_buff = None  # 消耗掉Buff
            elif st.session_state.active_buff:
                st.toast(f"✨ 成功触发【{st.session_state.active_buff}】的浪漫氛围加成！", icon="💖")
                score_val += 10  # 其他道具额外加10分
                st.session_state.active_buff = None
            
            st.session_state.dialogue_history.append({
                "choice_text": c_text,
                "reply_text": r_text
            })
            st.session_state.total_score += score_val
            
            if act < MAX_ACT:
                st.session_state.current_act += 1
            else:
                st.session_state.stage = "result"
            st.rerun()
            
    st.markdown("---")
    if st.button("🏠 放弃当前进度，返回主菜单"):
        st.session_state.stage = "menu"
        st.rerun()

# -----------------------------------------------------------------------------
# 结算阶段
# -----------------------------------------------------------------------------
elif st.session_state.stage == "result":
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
            st.session_state.stage = "story"
            st.rerun()
    with col_r2:
        if st.button("🏠 返回主菜单/更换角色", use_container_width=True):
            st.session_state.stage = "menu"
            st.session_state.current_act = 1
            st.session_state.total_score = 30
            st.session_state.dialogue_history = []
            st.session_state.inventory = []
            st.session_state.active_buff = None
            st.session_state.daily_gacha_result = None
            st.rerun()
