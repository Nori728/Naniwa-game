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
    "布丁": {"trait": "温柔体贴又吃得超开心的队长", "color": "绿色", "img": "https://img-mdpr.freetls.fastly.net/article/H0CW/nm/H0CW_-CrOagXoRlSyQPOD6_zSqLjGNjyrfLRLWlqECw.jpg?width=750"},
    "高恭": {"trait": "自恋又帅气的八嘎", "color": "紫色", "img": "https://img-mdpr.freetls.fastly.net/article/d4sb/nm/d4sbe7H-P8R6sUQpAshcntVT8-h0ZPcuMe3icV8aOm4.jpg?width=750"},
    "流星": {"trait": "眼睛会闪光的小恶魔", "color": "橙色", "img": "https://oggi.jp/wp-content/uploads/2023/03/DMA-DSC00151_2-2.jpg"},
    "米七": {"trait": "高挑的长腿王子", "color": "粉色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvYWZ1rSHkldisNtmwbvxSYNjR8FWjj4_wdyKxw84_h0SabJN81yYpsGXL&s=10"},
    "谦杜": {"trait": "时尚又有主见的末子", "color": "黄色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRs8ILDomyP9A6WZPtgig1e6IyPPmSpxS8HSYiRImU0uSqXicpvyNrHV8A&s=10"},
}

ROLES = ["经纪人", "粉丝/地下恋", "青梅竹马", "在日留学生or打工人"]

# 经典剧情分支库
STORIES = {
    "经纪人": {
        "title": "🎬 后台的斗嘴日常",
        "desc": "离上台还有 10 分钟，成员正坐在化妆镜前调侃。",
        "choices": [
            ("A. 顺着他的话打趣", "哼，就知道拆我的台！不过……今天表现得不错嘛。"),
            ("B. 递上手卡正色道", "好啦好啦，听你的还不行吗？工作时认真认真的样子，其实挺吸引人的。"),
            ("C. 假装严肃：『再不认真我要扣鸡腿了！』", "别介介！经纪人大人手下留情，我马上进入状态还不行吗！")
        ]
    },
    "粉丝/地下恋": {
        "title": "🎬 深夜的私密连线",
        "desc": "结束了闪耀的巨蛋演出，深夜手机屏幕亮起，是他打来的视频电话。",
        "choices": [
            ("A. 假装生气：『这么晚还不睡，明天有黑眼圈怎么办！』", "因为见不到你，想你想得睡不着嘛……只能听听你的声音了。"),
            ("B. 柔声撒娇：『欢迎回家，今天在台下我有一直看着你哦。』", "真的吗？我在台上一眼就看到你了……那一刻，聚光灯好像都没你耀眼。"),
            ("C. 无奈叹气默默听他碎碎念", "喂，别叹气呀！能听到你的声音，我今天所有的疲惫都消失了。")
        ]
    },
    "青梅竹马": {
        "title": "🎬 放学后的旧琴房",
        "desc": "夕阳透过琴房的玻璃窗，他正百无聊赖地拨弄着吉他弦。",
        "choices": [
            ("A. 直接恶作剧蒙住他的眼睛：『猜猜我是谁？』", "这股香气……笨蛋，除了你还能有谁。快松手，我有东西要给你看。"),
            ("B. 递上一罐冰可乐：『弹这么久不累吗？』", "哇，还是你最懂我！冰可乐和你的关心，我全部收下啦。"),
            ("C. 安静地坐在旁边听他弹奏", "……干嘛一直盯着我看？我会不好意思专心弹吉他的。")
        ]
    },
    "在日留学生or打工人": {
        "title": "🎬 后台兼职偶遇",
        "desc": "你在后台兼职翻译，正好碰到他在练习中文台词。",
        "choices": [
            ("A. 耐心纠正发音：『发音很棒，加油哦！』", "真的吗？中文发音像是在吃的东西吗？谢谢你耐心的指导！"),
            ("B. 递上资料：『这是今天的台词对照表。』", "太感谢了！如果没有你，我今天肯定要出大丑了。"),
            ("C. 鞠躬低头：『那个……请问有什么需要我做的吗？』", "不用这么客气啦！快抬起头来，我想多看看你。")
        ]
    }
}

# -----------------------------------------------------------------------------
# Session State 初始化
# -----------------------------------------------------------------------------
if "gacha" not in st.session_state:
    st.session_state.gacha = None
if "story_reply" not in st.session_state:
    st.session_state.story_reply = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------------------------------------------------------
# 页面标题
# -----------------------------------------------------------------------------
st.markdown('<p class="main-header">💖 浪花男子 · 专属心动企划</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">抽卡写真 ＋ 剧情分支 ＋ 自由畅聊</p>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 模块一：每日运势抽卡
# -----------------------------------------------------------------------------
st.markdown("### 🎰 1. 每日心动运势抽卡")
if st.button("✨ 测测今天最心动的成员", type="primary", use_container_width=True):
    st.session_state.gacha = random.choice(list(MEMBERS.keys()))

if st.session_state.gacha:
    m_name = st.session_state.gacha
    m_info = MEMBERS[m_name]
    st.success(f"🎉 抽卡成功！你今天的命定心动对象是：{m_name}")
    st.markdown(
        f"""
        <div class="card-box" style="text-align: center;">
            <img src="{m_info['img']}" width="100%" style="border-radius: 12px; max-height: 320px; object-fit: cover;">
            <p style="margin-top: 10px; font-weight: bold; color: #e11d48;">✨ {m_name} ({m_info['trait']})</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# -----------------------------------------------------------------------------
# 模块二：沉浸式剧情分支
# -----------------------------------------------------------------------------
st.markdown("### 📖 2. 经典剧情分支模式")
col1, col2 = st.columns(2)
with col1:
    sel_role = st.selectbox("选择你的身份", ROLES)
with col2:
    sel_member = st.selectbox("选择攻略对象", list(MEMBERS.keys()))

story = STORIES[sel_role]
member_data = MEMBERS[sel_member]

st.markdown(f"#### {story['title']}")
st.markdown(f"> **{story['desc']}**")

# 展示成员图片
st.markdown(
    f"""
    <div style="text-align: center; margin-bottom: 10px;">
        <img src="{member_data['img']}" width="100%" style="border-radius: 10px; max-height: 220px; object-fit: cover;">
    </div>
    """,
    unsafe_allow_html=True
)

if st.session_state.story_reply:
    st.markdown(
        f"""
        <div style="background: white; padding: 12px; border-radius: 8px; border-left: 4px solid #e11d48; margin-bottom: 10px;">
            💬 <b>{sel_member} 的回应：</b><br>
            <p style="color: #334155; margin-top: 4px;">「{st.session_state.story_reply}」</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("💖 **【HE 甜蜜告白结局达成】**：*『好不容易在人群中找到了你……这次我再也不会松开你的手了！』*")

st.write("👉 **请选择你的回应：**")
for idx, (label, reply_text) in enumerate(story["choices"]):
    if st.button(label, key=f"choice_{idx}", use_container_width=True):
        st.session_state.story_reply = reply_text
        st.rerun()

if st.button("🔄 重置剧情选择", use_container_width=True):
    st.session_state.story_reply = ""
    st.rerun()

st.divider()

# -----------------------------------------------------------------------------
# 模块三：自由畅聊模式 (想说什么就说什么)
# -----------------------------------------------------------------------------
st.markdown("### 💬 3. 自由畅聊模式 (随心所欲聊天)")
chat_member = st.selectbox("选择聊天对象", list(MEMBERS.keys()), key="chat_m")
chat_role = st.selectbox("选择当前身份", ROLES, key="chat_r")

c_info = MEMBERS[chat_member]

# 初始化对话
if not st.session_state.chat_history:
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": f"（看着走过来的你，{chat_member} 笑了笑）喂，今天找我有事吗？"
    })

# 显示聊天框
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="🌸"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant", avatar="💙"):
            st.write(msg["content"])

# 用户打字输入
if user_input := st.chat_input(f"对 {chat_member} 说点什么……"):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🌸"):
        st.write(user_input)
        
    with st.chat_message("assistant", avatar="💙"):
        with st.spinner("思考中..."):
            time.sleep(0.6)
            replies = [
                f"（耳朵微微泛红）你突然对我说这种话……犯规啦！",
                f"（轻笑了一声）真拿你没办法，听你的还不行吗？",
                f"（认真地看着你）记住你今天说的话哦，不许反悔！",
                f"（顺势靠近你身边）既然你都这么讲了，那接下来要好好陪我才行~"
            ]
            reply = random.choice(replies)
            st.write(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

if st.button("🧹 清空聊天记录"):
    st.session_state.chat_history = []
    st.rerun()
