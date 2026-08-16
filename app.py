import streamlit as st
import random

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
# 2. 基础数据源 (7人详细档案与写真)
# -----------------------------------------------------------------------------
CHARACTERS = {
    "丈君 (Fujiwara Joichiro)": {"color": "💙", "trait": "搞笑又可靠的大哥哥", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRxeLPXR2kAxnf8Z0uNFWIH7j_vjPcrr8Eg1qWtaTSoPKTvTMcZtXXX6Kn&s=10"},
    "大酱 (Nishihata Daigo)": {"color": "🔴", "trait": "热情太阳般的 C 位", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEiQYHWo7za_O6O-FerVkj5mA2s49UBL3hj_Tfmu-npd2yfIz1OJSCHD8n&s=10"},
    "布丁 (Ohashi Kazuya)": {"color": "💚", "trait": "温柔体贴的元气队长", "img": "https://img-mdpr.freetls.fastly.net/article/H0CW/nm/H0CW_-CrOagXoRlSyQPOD6_zSqLjGNjyrfLRLWlqECw.jpg?width=750"},
    "高恭 (Takahashi Kyohei)": {"color": "💜", "trait": "自恋又帅气的傲娇少年", "img": "https://img-mdpr.freetls.fastly.net/article/d4sb/nm/d4sbe7H-P8R6sUQpAshcntVT8-h0ZPcuMe3icV8aOm4.jpg?width=750"},
    "流星 (Onishi Ryusei)": {"color": "🧡", "trait": "眼睛会闪光的小恶魔", "img": "https://oggi.jp/wp-content/uploads/2023/03/DMA-DSC00151_2-2.jpg"},
    "米七 (Michieda Shunsuke)": {"color": "💖", "trait": "高挑清纯的长腿王子", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvYWZ1rSHkldisNtmwbvxSYNjR8FWjj4_wdyKxw84_h0SabJN81yYpsGXL&s=10"},
    "谦杜 (Nagao Kento)": {"color": "💛", "trait": "时尚又有主见的末子", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRs8ILDomyP9A6WZPtgig1e6IyPPmSpxS8HSYiRImU0uSqXicpvyNrHV8A&s=10"},
}

ROLES = ["经纪人", "粉丝/地下恋", "青梅竹马", "在日留学生or打工人"]

# -----------------------------------------------------------------------------
# 3. 多幕剧情与个性化台词大数据库 (针对不同身份、不同人物拥有独特剧情)
# -----------------------------------------------------------------------------
CHARACTER_SCRIPTS = {
    "经纪人": {
        "丈君 (Fujiwara Joichiro)": {
            1: {
                "title": "🎬 第一幕：通告间隙的吐槽",
                "desc": "刚结束搞笑番组的录制，丈君拿着毛巾一边擦汗一边凑过来。",
                "choices": [
                    {"label": "A. 递上一瓶冰麦茶：『今天表现不错哦，辛苦啦。』", "next": 2, "score": 20, "reply": "哇，还是你最懂我！不过刚才那个整蛊企划吓死我了，得你安慰一下才行。"},
                    {"label": "B. 假装严肃：『刚才有个梗你接慢了半拍哦！』", "next": 2, "score": 15, "reply": "诶——？那是因为我在后台分心看你了嘛！好啦，饶了我这一次吧。"}
                ]
            },
            2: {
                "title": "🎬 第二幕：深夜的保姆车后座",
                "desc": "深夜收工的保姆车上，经纪人席位只剩下你和他，车厢里一片安静。",
                "choices": [
                    {"label": "A. 靠在车窗边假装闭目养神", "next": "HE", "score": 25, "reply": "（悄悄把肩膀挪过来让你靠着）累了就靠一会儿吧……有我在，安心睡吧。"},
                    {"label": "B. 翻看接下来的行程表提醒他早点休息", "next": "HE", "score": 20, "reply": "好啦，工作狂经纪人小姐，现在是私人时间，不许再看文件了，看我一眼嘛。"}
                ]
            }
        },
        "米七 (Michieda Shunsuke)": {
            1: {
                "title": "🎬 第一幕：杂志拍摄后台",
                "desc": "米七刚换好一身纯白西装，走到你面前低头整理领带。",
                "choices": [
                    {"label": "A. 帮他仔细整理领口：『这样就完美啦。』", "next": 2, "score": 25, "reply": "（低头看着你，耳根微微泛红）每次你这样帮我……我都觉得心跳好快。"},
                    {"label": "B. 调侃道：『不愧是国宝级帅哥，今天也闪闪发光。』", "next": 2, "score": 15, "reply": "别笑话我了……你在旁边看着我的时候，我才没办法专心拍照呢。"}
                ]
            },
            2: {
                "title": "🎬 第二幕：收工后的私下对剧本",
                "desc": "休息室里只剩你们两人，他突然合上剧本，认真地看着你。",
                "choices": [
                    {"label": "A. 疑惑回望：『怎么了？台词有什么不懂的吗？』", "next": "HE", "score": 25, "reply": "台词我都懂……我只是在想，什么时候才能让你只做我一个人的专属经纪人。"},
                    {"label": "B. 拍拍他的肩膀：『快把最后一段对完收工啦！』", "next": "HE", "score": 20, "reply": "好吧……既然你这么急着收工，那今晚收工后必须陪我一起去吃拉面作为惩罚！"}
                ]
            }
        }
    },
    "粉丝/地下恋": {
        "大酱 (Nishihata Daigo)": {
            1: {
                "title": "🎬 第一幕：巨蛋演唱会后的深夜连线",
                "desc": "万粉欢呼的巨蛋演唱会刚刚落幕，手机屏幕上亮起了他的视频通话。",
                "choices": [
                    {"label": "A. 刚接通就笑着说：『今天在台下我有一直看着你哦！』", "next": 2, "score": 25, "reply": "真的吗？我在台上一眼就找到你了……那一刻，聚光灯好像都没有你耀眼。"},
                    {"label": "B. 假装傲娇：『大明星今天表现不错，特此表扬。』", "next": 2, "score": 15, "reply": "什么嘛，明明最想听你夸我的人就是我！快多说两句好听的哄哄我。"}
                ]
            },
            2: {
                "title": "🎬 第二幕：无人小巷的秘密拥抱",
                "desc": "通过层层伪装，你们终于在约好的公园长椅旁见到了彼此。",
                "choices": [
                    {"label": "A. 紧张地环顾四周：『会被狗仔拍到的！快回去吧……』", "next": "HE", "score": 20, "reply": "（一把将你拉进怀里）不怕……好不容易见到你，让我抱一会儿就好，就一会儿。"},
                    {"label": "B. 笑着递上亲手做的便当", "next": "HE", "score": 25, "reply": "呜哇……每次吃到你做的饭，我就觉得所有的辛苦都值了。有你真好。"}
                ]
            }
        },
        "布丁 (Ohashi Kazuya)": {
            1: {
                "title": "🎬 第一幕：深夜广播节目结束后",
                "desc": "他结束了深夜生放送广播，带着温柔的笑意给你发来语音电话。",
                "choices": [
                    {"label": "A. 声音带着困意：『欢迎回家，今天辛苦啦队长。』", "next": 2, "score": 20, "reply": "听到你的声音，我一天的疲惫就全飞走啦！好想现在就飞到你身边吃你做的布丁。"},
                    {"label": "B. 吐槽他今天广播里吃螺丝：『刚才直播吃螺丝了吧你！』", "next": 2, "score": 15, "reply": "诶——？这都被你听出来了！不许笑话我，我要亲亲才能好！"}
                ]
            },
            2: {
                "title": "🎬 第二幕：秘密约会的料理时光",
                "desc": "在安全的小屋里，他系着围裙，笑意盈盈地看着你切菜。",
                "choices": [
                    {"label": "A. 小心翼翼躲开他的视线：『专心切你的菜啦！』", "next": "HE", "score": 20, "reply": "因为你比菜好看嘛~ 呐，张嘴，尝尝我刚刚做好的汤够不够甜。"},
                    {"label": "B. 喂他吃一口切好的水果", "next": "HE", "score": 25, "reply": "唔……好甜！不过没有你对我笑的时候甜。最喜欢你了！"}
                ]
            }
        }
    }
}

# 默认通用剧本（当选中其他未单独罗列组合时使用，确保每一个人都可以玩）
DEFAULT_SCRIPT = {
    1: {
        "title": "🎬 第一幕：命运的邂逅日常",
        "desc": "阳光正好，你们在约好的地点相遇，他带着标志性的微笑向你走来。",
        "choices": [
            {"label": "A. 主动挥手打招呼：『这里这里！』", "next": 2, "score": 20, "reply": "看到你笑得这么开心，我今天一整天的心情都变好了呢。"},
            {"label": "B. 假装高冷双手抱胸：『你迟到了三分钟哦。』", "next": 2, "score": 15, "reply": "好啦好啦是我不对！为了赔罪，今天你想吃什么我都请客！"}
        ]
    },
    2: {
        "title": "🎬 第二幕：心跳加速的独处时光",
        "desc": "周围的人渐渐散去，只剩下彼此的心跳声和微风吹过的声音。",
        "choices": [
            {"label": "A. 脸颊微红地别过头去", "next": "HE", "score": 25, "reply": "（轻轻握住你的手）……别把脸转过去，我想一直这样看着你。"},
            {"label": "B. 认真地向他倾诉心意", "next": "HE", "score": 25, "reply": "（眼神变得无比温柔）傻瓜，其实我的心意，早就只为你一个人停留了。"}
        ]
    }
}

# -----------------------------------------------------------------------------
# Session State 初始化
# -----------------------------------------------------------------------------
if "gacha_res" not in st.session_state:
    st.session_state.gacha_res = None
if "story_stage" not in st.session_state:
    st.session_state.story_stage = 1
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "history_replies" not in st.session_state:
    st.session_state.history_replies = []
if "current_script_key" not in st.session_state:
    st.session_state.current_script_key = ""

# -----------------------------------------------------------------------------
# 页面顶部标题
# -----------------------------------------------------------------------------
st.markdown('<p class="main-header">💖 浪花男子 · 专属心动企划</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">抽卡写真 ＋ 7人专属多幕剧情分支 ＋ 纯净沉浸式体验</p>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 模块一：每日运势抽卡
# -----------------------------------------------------------------------------
st.markdown("### 🎰 1. 每日心动运势抽卡")
if st.button("✨ 抽取今日命定心动对象", type="primary", use_container_width=True):
    st.session_state.gacha_res = random.choice(list(CHARACTERS.keys()))

if st.session_state.gacha_res:
    c_name = st.session_state.gacha_res
    c_info = CHARACTERS[c_name]
    st.success(f"🎉 抽卡成功！你今天的命定心动对象是：{c_name}")
    st.markdown(
        f"""
        <div class="card-box" style="text-align: center;">
            <img src="{c_info['img']}" width="100%" style="border-radius: 12px; max-height: 320px; object-fit: cover;">
            <p style="margin-top: 10px; font-weight: bold; color: #e11d48;">✨ {c_name} ({c_info['trait']})</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# -----------------------------------------------------------------------------
# 模块二：多幕剧情分支系统（无自由发言，专注精细剧情）
# -----------------------------------------------------------------------------
st.markdown("### 📖 2. 7人专属多幕剧情模式")

col1, col2 = st.columns(2)
with col1:
    sel_role = st.selectbox("选择你的身份", ROLES, key="role_sel")
with col2:
    sel_member = st.selectbox("选择攻略对象", list(CHARACTERS.keys()), key="member_sel")

# 切换身份或人物时，重置剧情进度
script_key = f"{sel_role}_{sel_member}"
if st.session_state.current_script_key != script_key:
    st.session_state.current_script_key = script_key
    st.session_state.story_stage = 1
    st.session_state.total_score = 0
    st.session_state.history_replies = []

# 获取对应的剧本 (如果没有独立写明，则调用默认精美剧本)
role_dict = CHARACTER_SCRIPTS.get(sel_role, {})
member_script = role_dict.get(sel_member, DEFAULT_SCRIPT)

member_data = CHARACTERS[sel_member]
stage = st.session_state.story_stage

st.markdown(
    f"""
    <div style="text-align: center; margin-bottom: 15px;">
        <img src="{member_data['img']}" width="100%" style="border-radius: 10px; max-height: 200px; object-fit: cover;">
        <p style="color: #64748b; font-size: 0.9rem; margin-top: 5px;">当前攻略：<b>{sel_member}</b> | 身份：<b>{sel_role}</b></p>
    </div>
    """,
    unsafe_allow_html=True
)

# 回放之前的对话记录
for h in st.session_state.history_replies:
    st.markdown(
        f"""
        <div style="background: white; padding: 10px; border-radius: 8px; border-left: 3px solid #e11d48; margin-bottom: 8px; font-size: 0.95rem;">
            💬 <b>{sel_member}：</b> 「{h}」
        </div>
        """,
        unsafe_allow_html=True
    )

# 判断是否通关 (HE 结局)
if stage == "HE":
    st.markdown("---")
    st.markdown("### 🏆 【HE 甜蜜告白结局达成】")
    st.markdown(
        f"""
        <div class="card-box" style="text-align: center;">
            <p style="color: #e11d48; font-weight: bold; font-size: 1.1rem;">✨ 最终心动指数：{st.session_state.total_score} 分 (完美满分！)</p>
            <p style="margin-top: 10px; line-height: 1.6;">
                <i>『好不容易在人山人海中认出了彼此……这次我再也不会松开你的手了！无论外界怎么看，你永远是我唯一的偏爱与选择。』</i><br>
                —— <b>{sel_member}</b> 在灯光暗下的后台角落里，紧紧将你拥入怀中，开启了只属于你们的浪漫恋爱。
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("🔄 重新体验本段剧情", use_container_width=True):
        st.session_state.story_stage = 1
        st.session_state.total_score = 0
        st.session_state.history_replies = []
        st.rerun()

else:
    # 渲染当前幕的剧情与选项
    current_scene = member_script.get(stage, DEFAULT_SCRIPT[1])
    
    st.markdown(f"#### {current_scene['title']}")
    st.markdown(f"> **{current_scene['desc']}**")
    
    st.markdown("👉 **请做出你的抉择：**")
    for idx, choice in enumerate(current_scene["choices"]):
        if st.button(choice["label"], key=f"choice_btn_{stage}_{idx}", use_container_width=True):
            st.session_state.history_replies.append(choice["reply"])
            st.session_state.total_score += choice["score"]
            st.session_state.story_stage = choice["next"]
            st.rerun()

if st.button("🧹 重置当前进度", use_container_width=True):
    st.session_state.story_stage = 1
    st.session_state.total_score = 0
    st.session_state.history_replies = []
    st.rerun()
