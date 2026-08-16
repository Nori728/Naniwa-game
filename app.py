import random
import streamlit as st

# 1. 初始化 Session State 状态
if "current_char" not in st.session_state:
    st.session_state.current_char = "藤原丈一郎"
if "story_stage" not in st.session_state:
    st.session_state.story_stage = 1
if "scores" not in st.session_state:
    st.session_state.scores = {"heart": 0, "trust": 0}
if "gacha_buff" not in st.session_state:
    st.session_state.gacha_buff = None  # 抽奖获得的运势/道具加成

# 2. 浪花男子全员数据与专属剧情库
CHAR_DATA = {
    "藤原丈一郎": {
        "avatar": "images/jo.jpg",
        "desc": "浪花男子的副队长，看似傲娇爱吐槽，实则极具责任感。",
        "bg_color": "#E6F3FF"
    },
    "道枝駿佑": {
        "avatar": "images/micchi.jpg",
        "desc": "清澈纯粹的少年，对待感情细腻又有些害羞。",
        "bg_color": "#FFEFF2"
    },
    "大桥和也": {
        "avatar": "images/kazu.jpg",
        "desc": "元气满满的队长，总能用笑容和美食治愈人心。",
        "bg_color": "#E8F8F5"
    }
}

# 侧边栏：角色切换与抽奖区域
st.sidebar.title("🎭 互动控制台")

# 【功能一：角色选择】
selected = st.sidebar.selectbox("选择互动成员", list(CHAR_DATA.keys()))
if selected != st.session_state.current_char:
    st.session_state.current_char = selected
    st.session_state.story_stage = 1
    st.session_state.scores = {"heart": 0, "trust": 0}
    st.session_state.gacha_buff = None
    st.rerun()

st.sidebar.divider()

# 【功能二：今日运势/道具抽奖】
st.sidebar.subheader("🎲 每日心动抽奖")
if st.sidebar.button("点击抽奖/抽取今日运势"):
    cards = [
        ("🌸 樱花御守", "心动值增加时额外 +1"),
        ("☕ 冰美式咖啡", "可以解锁吐槽向剧情的隐藏对话"),
        ("⚾ 限量棒球门票", "直接触发特殊随机事件"),
        ("🌧️ 骤雨卡", "剧情遭遇波折，但可能塞翁失马")
    ]
    drawn = random.choice(cards)
    st.session_state.gacha_buff = drawn
    st.sidebar.success(f"抽中：**{drawn[0]}**\n\n_{drawn[1]}_")

if st.session_state.gacha_buff:
    st.sidebar.info(f"当前生效加成：{st.session_state.gacha_buff[0]}")

# 主界面显示
char = CHAR_DATA[st.session_state.current_char]
st.title("💖 浪花男子心动日常")
st.caption(f"当前互动：{st.session_state.current_char} | {char['desc']}")

# 【功能三：分阶段随机剧情（非固定 HE/BE 路线）】
st.divider()

# 剧情节点 1
if st.session_state.story_stage == 1:
    st.subheader("第一章：突然掉落的休息日")
    st.write("难得有一天的拍摄早早结束，走廊里只有你们两个人。他看起来有些疲惫，但眼神里又透着一丝不知道去哪里的空虚。")

    # 选项设计：没有绝对的“好与坏”，取决于隐藏性格与随机波长
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("A. 递上一杯冷饮，并顺势吐槽今天的行程太满"):
            # 引入随机判定：根据性格+随机数决定反馈，打破固定走向
            luck = random.randint(1, 10)
            if luck > 4 or (st.session_state.gacha_buff and "咖啡" in st.session_state.gacha_buff[0]):
                st.session_state.scores["trust"] += 2
                st.write("＞ **意外的共鸣**：他笑了起来，接过饮料顺着你的话接下去，两人之间的气氛轻松了不少。")
            else:
                st.session_state.scores["heart"] += 1
                st.write("＞ **微妙的沉默**：他喝了一口，叹了口气：“是啊……不过工作多也是好事啦。”")
            st.session_state.story_stage = 2

    with col2:
        if st.button("B. 保持安静，默默在他旁边坐下陪他刷手机"):
            luck = random.randint(1, 10)
            if luck > 5:
                st.session_state.scores["heart"] += 2
                st.write("＞ **无声的默契**：他把肩窝往你这边靠了靠，把手机屏幕往你这边偏了偏，分享他正在看搞笑视频。")
            else:
                st.session_state.scores["trust"] += 1
                st.write("＞ **自然而然的舒适**：虽然没说话，但空气并不尴尬，两个人享受了一会儿难得的平静。")
            st.session_state.story_stage = 2

# 剧情节点 2
elif st.session_state.story_stage == 2:
    st.subheader("第二章：晚风与岔路")
    st.write("准备离开电视台时，天空突然下起了小雨。门前的台阶上积了浅浅的水洼。")

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("A. 提议“不如稍微等雨小一点再走”"):
            st.session_state.scores["heart"] += 1
            st.session_state.scores["trust"] += 1
            st.write("＞ 你们站在檐下听雨声，他突然侧过脸看了你一眼。")
            st.session_state.story_stage = 3

    with col2:
        if st.button("B. 拿出包里唯一的折叠伞：“一起撑到车站吧”"):
            # 道具/抽奖加成对剧情的影响
            if st.session_state.gacha_buff and "御守" in st.session_state.gacha_buff[0]:
                st.session_state.scores["heart"] += 3
                st.write("＞ 伞下空间不大，他的肩膀靠得很紧，雨水打湿了他的后背，他却一直把伞往你这边倾斜。")
            else:
                st.session_state.scores["trust"] += 2
                st.write("＞ 一路上为了避开水洼，你们打打闹闹地跑到了车站。")
            st.session_state.story_stage = 3

# 结局结算：多维度积分判定，而非简单 A=HE/B=BE
elif st.session_state.story_stage == 3:
    st.subheader("📖 本日片段收录")
    
    heart = st.session_state.scores["heart"]
    trust = st.session_state.scores["trust"]
    
    # 根据组合数值（非单一选项）生成不同关系结局
    if heart >= 3 and trust >= 3:
        st.success("✨ **【心动共鸣】**：不仅是无话不谈的伙伴，眼神交汇时还多了一份说不清的暧昧情绪。")
    elif heart > trust:
        st.info("💓 **【心跳超载】**：关系突飞猛进，他开始频频对你展露从未在镜头前出现过的慌张与害羞。")
    elif trust >= heart:
        st.warning("🤝 **【灵魂羁绊】**：比起浪漫，你们建立起了无可替代的信任感，在他眼里你已经是特别的存在。")
    else:
        st.write("🍃 **【平淡如水】**：平稳度过了日常的一天，关系在细水长流中悄悄萌芽。")

    if st.button("重新开始/开启新一天"):
        st.session_state.story_stage = 1
        st.session_state.scores = {"heart": 0, "trust": 0}
        st.rerun()
