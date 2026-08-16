import streamlit as st
import random
import time

# -----------------------------------------------------------------------------
# 1. 页面基本配置
# -----------------------------------------------------------------------------
st.set_page_config(page_title="浪花男子 · 专属心动企划", page_icon="💖", layout="centered")

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
# 2. 基础数据源 (成员信息、头像与特征)
# -----------------------------------------------------------------------------
MEMBERS = {
    "丈君": {"trait": "搞笑又可靠的大哥哥", "color": "蓝色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRxeLPXR2kAxnf8Z0uNFWIH7j_vjPcrr8Eg1qWtaTSoPKTvTMcZtXXX6Kn&s=10"},
    "大酱": {"trait": "热情太阳般的 C 位", "color": "红色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEiQYHWo7za_O6O-FerVkj5mA2s49UBL3hj_Tfmu-npd2yfIz1OJSCHD8n&s=10"},
    "布丁": {"trait": "温柔体贴又吃得超看的队长", "color": "绿色", "img": "https://img-mdpr.freetls.fastly.net/article/H0CW/nm/H0CW_-CrOagXoRlSyQPOD6_zSqLjGNjyrfLRLWlqECw.jpg?width=750"},
    "高恭": {"trait": "自恋又帅气的八嘎", "color": "紫色", "img": "https://img-mdpr.freetls.fastly.net/article/d4sb/nm/d4sbe7H-P8R6sUQpAshcntVT8-h0ZPcuMe3icV8aOm4.jpg?width=750"},
    "流星": {"trait": "眼睛会闪光的小恶魔", "color": "橙色", "img": "https://oggi.jp/wp-content/uploads/2023/03/DMA-DSC00151_2-2.jpg"},
    "米七": {"trait": "高挑的长腿王子", "color": "粉色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvYWZ1rSHkldisNtmwbvxSYNjR8FWjj4_wdyKxw84_h0SabJN81yYpsGXL&s=10"},
    "谦杜": {"trait": "时尚又有主见的末子", "color": "黄色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRs8ILDomyP9A6WZPtgig1e6IyPPmSpxS8HSYiRImU0uSqXicpvyNrHV8A&s=10"},
}

ROLES = ["经纪人", "粉丝/地下恋", "青梅竹马", "在日留学生or打工人"]

# 经典多幕剧本库 (带选项)
STORIES = {
    "经纪人": {
        "title": "🎬 第一幕：后台的斗嘴日常",
        "desc": "离上台还有 10 分钟，成员正坐在化妆镜前调侃。",
        "choices": [
            {"label": "A. 顺着他的话打趣", "score": 20, "reply": "哼，就知道拆我的台！不过……今天表现得不错嘛。"},
            {"label": "B. 递上手卡正色道", "score": 15, "reply": "好啦好啦，听你的还不行吗？工作时认真认真的样子，其实挺吸引人的。"},
            {"label": "C. 假装严肃：『再不认真我要扣鸡腿了！』", "score": 10, "reply": "别介介！经纪人大人手下留情，我马上进入状态还不行吗！"}
        ]
    },
    "粉丝/地下恋": {
        "title": "🎬 第一幕：深夜的私密连线",
        "desc": "结束了闪耀的巨蛋演出，深夜手机屏幕亮起，是他打来的视频电话。",
        "choices": [
            {"label": "A. 假装生气：『这么晚还不睡，明天有黑眼圈怎么办！』", "score": 20, "reply": "因为见不到你，想你想得睡不着嘛……只能听听你的声音了。"},
            {"label": "B. 柔声撒娇：『欢迎回家，今天在台下我有一直看着你哦。』", "score": 25, "reply": "真的吗？我在台上一眼就看到你了……那一刻，聚光灯好像都没你耀眼。"},
            {"label": "C. 无奈叹气默默听他碎碎念", "score": 10, "reply": "喂，别叹气呀！能听到你的声音，我今天所有的疲惫都消失了。"}
        ]
    },
    "青梅竹马": {
        "title": "🎬 第一幕：放学后的旧琴房",
        "desc": "夕阳透过琴房的玻璃窗，他正百无聊赖地拨弄着吉他弦。",
        "choices": [
            {"label": "A. 直接恶作剧蒙住他的眼睛：『猜猜我是谁？』", "score": 25, "reply": "这股香气……笨蛋，除了你还能有谁。快松手，我有东西要给你看。"},
            {"label": "B. 递上一罐冰可乐：『弹这么久不累吗？』", "score": 20, "reply": "哇，还是你最懂我！冰可乐和你的关心，我全部收下啦。"},
            {"label": "C. 安静地坐在旁边听他弹奏", "score": 15, "reply": "……干嘛一直盯着我看？我会不好意思专心弹吉他的。"}
        ]
    },
    "在日留学生or打工人": {
        "title": "🎬 第一幕：后台兼职偶遇",
        "desc": "你在后台兼职翻译，正好碰到他在练习中文台词。",
        "choices": [
            {"label": "A. 耐心纠正发音：『发音很棒，加油哦！』", "score": 20, "reply": "真的吗？中文发音像是在吃的东西吗？谢谢你耐心的指导！"},
            {"label": "B. 递上资料：『这是今天的台词对照表。』", "score": 15, "reply": "太感谢了！如果没有你，我今天肯定要出大丑了。"},
            {"label": "C. 鞠躬低头：『那个……请问有什么需要我做的吗？』", "score": 10, "reply": "不用这么客气啦！快抬起头来，我想多看看你。"}
        ]
    }
}

# -----------------------------------------------------------------------------
# Session State 初始化
# -----------------------------------------------------------------------------
if "gacha_result" not in st.session_state:
    st.session_state.gacha_result = None
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "last_reply" not in st.session_state:
    st.session_state.last_reply = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------------------------------------------------------
# 页面顶部标题
# -----------------------------------------------------------------------------
st.markdown('<p class="main-header">💖 浪花男子 · 专属心动企划</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">抽卡收集 ＋ 经典剧情分支 ＋ 自由畅聊模式</p>', unsafe_allow_html=True)

# 使用 Tabs 将功能划分清晰
tab_gacha, tab_story, tab_chat = st.tabs(["🎰 每日运势抽卡", "📖 经典剧情分支", "💬 自由畅聊模式"])

# =============================================================================
# TAB 1: 每日运势抽卡
# =============================================================================
with tab_gacha:
    st.subheader("🎲 每日心动运势抽卡")
    st.write("测一测今天哪位成员会带给你好运，并解锁他的专属写真！")
    
    if st.button("✨ 立即抽取今日心动成员", type="primary", use_container_width=True):
        chosen_name = random.choice(list(MEMBERS.keys()))
        st.session_state.gacha_result = chosen_name

    if st.session_state.gacha_result:
        m_name = st.session_state.gacha_result
        m_data = MEMBERS[m_name]
        st.success(f"🎉 恭喜你抽中了今天最心动的成员：{m_name}！")
        
        st.markdown(
            f"""
            <div style="text-align: center;" class="card-box">
                <img src="{m_data['img']}" width="100%" style="border-radius: 12px; max-height: 350px; object-fit: cover;">
                <p style="margin-top: 15px; font-weight: bold; font-size: 1.2rem; color: #e11d48;">✨ {m_name} ({m_data['trait']})</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("🔄 返回重抽"):
            st.session_state.gacha_result = None
            st.rerun()

# =============================================================================
# TAB 2: 经典剧情分支 (带选项与结局结算)
# =============================================================================
with tab_story:
    st.subheader("📖 沉浸式多幕剧情选择")
    
    selected_role = st.selectbox("🎭 1️⃣ 请选择你的身份：", ROLES, key="story_role")
    selected_member = st.selectbox("💖 2️⃣ 请选择你想攻略的成员：", list(MEMBERS.keys()), key="story_member")
    
    m_info = MEMBERS[selected_member]
    script_data = STORIES[selected_role]
    
    st.divider()
    st.markdown(f"### 【{selected_role}】 {script_data['title']}")
    st.markdown(f"> **{script_data['desc']}**")
    
    # 展示头像
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 15px;">
            <img src="{m_info['img']}" width="100%" style="border-radius: 12px; max-height: 250px; object-fit: cover;">
        </div>
        """,
        unsafe_allow_html=True
    )

    # 如果已经选择了某选项，展示回应
    if st.session_state.get("active_role") == selected_role and st.session_state.get("active_member") == selected_member and st.session_state.last_reply:
        st.markdown(
            f"""
            <div style="background-color: #fff; padding: 15px; border-radius: 10px; border-left: 4px solid #e11d48; margin-bottom: 15px;">
                💬 <b>{selected_member} 的回应：</b><br>
                <p style="color: #334155; margin-top: 5px; font-size: 1.05rem;">「{st.session_state.last_reply}」</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("#### 👉 请做出你的回应选择：")
    for idx, choice in enumerate(script_data["choices"]):
        if st.button(choice["label"], key=f"story_choice_{idx}", use_container_width=True):
            st.session_state.last_reply = choice["reply"]
            st.session_state.total_score = choice["score"] + 30
            st.session_state.active_role = selected_role
            st.session_state.active_member = selected_member
            st.rerun()

    # 结算面板
    if st.session_state.get("active_role") == selected_role and st.session_state.get("active_member") == selected_member and st.session_state.last_reply:
        st.divider()
        st.markdown("### 🏆 剧情结算")
        score = st.session_state.total_score
        
        st.markdown(
            f"""
            <div class="card-box" style="text-align: center;">
                <p style="color: #e11d48; font-weight: bold;">✨ {selected_member} ({m_info['trait']})</p>
                <p>在 <b>【{selected_role}】</b> 的故事中，你与 {selected_member} 的最终心动指数为：<b>{score} 分</b> (满分 60 分)。</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("#### 💖 【HE 甜蜜告白结局】")
        st.markdown(
            f"""
            > *『好不容易在人群中找到了你……这次我再也不想松开你的手了！无论别人怎么看，你才是我最重要的选择！』* > —— **{selected_member}** 在灯光暗下的角落里，紧紧牵住了你的手，开启了只属于你们的甜蜜恋情。
            """,
            unsafe_allow_html=True
        )
        
        if st.button("🔄 重新体验本段剧情", use_container_width=True):
            st.session_state.last_reply = ""
            st.session_state.total_score = 0
            if "active_role" in st.session_state:
                del st.session_state.active_role
            st.rerun()

# =============================================================================
# TAB 3: 自由畅聊模式 (玩家自己想说什么就说什么)
# =============================================================================
with tab_chat:
    st.subheader("💬 自由
