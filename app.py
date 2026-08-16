# -*- coding: utf-8 -*-
import streamlit as st
import random

# -----------------------------------------------------------------------------
# 1. 页面基本配置
# -----------------------------------------------------------------------------
st.set_page_config(page_title="浪花男子心动日常", page_icon="💖", layout="centered")

# -----------------------------------------------------------------------------
# 2. 七位成员与身份配置
# -----------------------------------------------------------------------------
MEMBERS = {
    "丈君": {"trait": "搞笑又可靠的大哥哥", "color": "蓝色", "img": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400"},
    "大酱": {"trait": "热情又散发C位光芒的太阳", "color": "红色", "img": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"},
    "布丁": {"trait": "温柔体贴又吃得超香的队长", "color": "绿色", "img": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400"},
    "高恭": {"trait": "嘴硬心软的傲娇帅哥", "color": "紫色", "img": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400"},
    "流星": {"trait": "眼神会放电的小恶魔", "color": "橙色", "img": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=400"},
    "米七": {"trait": "温柔长腿王子", "color": "粉色", "img": "https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?w=400"},
    "谦杜": {"trait": "时尚敏锐的小恶魔末子", "color": "黄色", "img": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400"},
}

ROLES = ["经纪人", "粉丝/地下恋", "青梅竹马", "在日留学生or打工人"]

# -----------------------------------------------------------------------------
# 3. Session State 初始化
# -----------------------------------------------------------------------------
if "gacha_target" not in st.session_state:
    st.session_state.gacha_target = None
if "story_started" not in st.session_state:
    st.session_state.story_started = False
if "act" not in st.session_state:
    st.session_state.act = 1
if "score" not in st.session_state:
    st.session_state.score = 0
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------------------------------------------------------
# 4. 主界面：标题与每日运势抽卡
# -----------------------------------------------------------------------------
st.title("💖 浪花男子心动日常")
st.markdown("---")

st.subheader("🎲 每日运势抽卡")
if st.button("✨ 测测今天心动的成员"):
    st.session_state.gacha_target = random.choice(list(MEMBERS.keys()))

if st.session_state.gacha_target:
    t = st.session_state.gacha_target
    m_info = MEMBERS[t]
    st.success(f"🎉 恭喜你抽中了今天心动的成员：**{t}**！")
    st.image(m_info["img"], width=300, caption=f"✨ {t}")

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. 互动剧情模块
# -----------------------------------------------------------------------------
st.subheader("📖 开启心动互动剧情")

# 选择身份
selected_role = st.selectbox("1️⃣ 请选择你的身份：", ROLES, key="role_select")

# 选择攻略成员
selected_target = st.selectbox("2️⃣ 请选择你想攻略的成员：", list(MEMBERS.keys()), key="target_select")

# 展示当前选中成员的背景与特征
current_member_data = MEMBERS[selected_target]
st.markdown(f"> ✨ **成员特征**：{current_member_data['trait']} | **专属颜色**：{current_member_data['color']}")

st.markdown("---")

# 剧情开始按钮
if st.button("🌟 进入多分手剧情", type="primary"):
    st.session_state.story_started = True
    st.session_state.act = 1
    st.session_state.score = 0
    st.session_state.history = []
    st.rerun()

# -----------------------------------------------------------------------------
# 6. 分幕剧情逻辑
# -----------------------------------------------------------------------------
if st.session_state.story_started:
    st.markdown(f"## 【{selected_role}】 🎬 第 {st.session_state.act} 幕")
    
    # 定义简单的剧情模拟数据
    act = st.session_state.act
    
    if act == 1:
        st.write(f"【第一幕：初遇与后台】你在后台准备时，意外遇到了正在准备登台的 {selected_target}。")
        choice = st.radio("请做出你的回应选择：", [
            "🅰️ 耐心纠正对方：『发音很棒，加油哦！』",
            "🅱️ 递上资料：『这是今天的大纲对照表。』",
            "🆎 调侃语气：『那个……请问有什么需要我做的吗？』"
        ], key="c1")
        
        if st.button("确认选择并进入第二幕"):
            st.session_state.score += 20
            st.session_state.history.append(("第一幕选择", choice))
            st.session_state.act = 2
            st.rerun()

    elif act == 2:
        st.write(f"【第二幕：异国文化交流】休息时间，{selected_target} 好奇地问起你在日本的打工生活。")
        choice = st.radio("请做出你的回应选择：", [
            "🅰️ 分享家乡美食，聊起异国趣事。",
            "🅱️ 聊起打工：『虽然有点累，但挺充实的。』",
            "🆎 倒苦水：『日语不通，真想回国了。』"
        ], key="c2")
        
        if st.button("确认选择并进入第三幕"):
            st.session_state.score += 30
            st.session_state.history.append(("第二幕选择", choice))
            st.session_state.act = 3
            st.rerun()

    elif act == 3:
        st.write(f"【第三幕：深夜车站】深夜打工结束，你们在微凉的电车站台并肩等车。")
        choice = st.radio("请做出你的回应选择：", [
            "🅰️ 汉堡摊偶遇，碰到了彼此的手指。",
            "🅱️ 看着电车：『今天工作很充实，电车来了。』",
            "🆎 戴上耳机不说话。"
        ], key="c3")
        
        if st.button("查看结算结果"):
            st.session_state.score += 30
            st.session_state.history.append(("第三幕选择", choice))
            st.session_state.act = 4
            st.rerun()

    elif act >= 4:
        # 结算页面
        st.markdown("---")
        st.header("✨ 结算页面 ✨")
        st.image(current_member_data["img"], width=300, caption=f"✨ {selected_target} ({current_member_data['trait']})")
        
        final_score = st.session_state.score
        st.write(f"在【{selected_role}】的故事中，你与 **{selected_target}** 的最终心动指数为：**{final_score} 分**（满分 80 分）。")
        
        st.markdown("### 💖 【HE 甜蜜告白结局】")
        st.write(f"『不管易在人群中找到了你……这次再也不想松开你的手了！无论别人怎么看，你才是我最重要的选择！』")
        st.write(f"—— {selected_target} 在灯光下的角落里，紧紧牵住了你的手，开启了属于你们的甜蜜恋情。")
        
        if st.button("🔄 返回首页 / 重新体验"):
            st.session_state.story_started = False
            st.session_state.act = 1
            st.session_state.score = 0
            st.session_state.gacha_target = None
            st.rerun()
