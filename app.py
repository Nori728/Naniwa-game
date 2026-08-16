import streamlit as st
import random
import os

# --- 新增的图片加载逻辑 (不影响页面布局) ---
def safe_image(img_path, caption=None):
    if img_path.startswith("http"):
        st.image(img_path, caption=caption, use_container_width=True)
    elif os.path.exists(img_path):
        st.image(img_path, caption=caption, use_container_width=True)
    else:
        st.warning(f"⚠️ 图片路径不存在: {img_path}")

# --- 原有的人物数据 ---
MEMBERS = {
    "丈君": {"nick": "丈君", "trait": "搞笑又可靠的大哥哥", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRxeLPXR2kAxnf8Z0uNFWIH7j_vjPcrr8Eg1qWtaTSoPKTvTMcZtXXX6Kn&s=10", "color": "💙 蓝色"},
    "大西": {"nick": "大西", "trait": "热情太阳般的 C 位", "img": "images/da_jiang.gif", "color": "🔴 红色"},
    "布丁": {"nick": "布丁", "trait": "温柔体贴又吃得超香的队长", "img": "images/bu_ding.gif", "color": "💚 绿色"},
    "高恭": {"nick": "高恭", "trait": "自恋又亚撒西的八嘎帅哥，实则运动超强", "img": "images/gao_gong.gif", "color": "💜 紫色"},
    "流星": {"nick": "流星", "trait": "眼睛会闪光的小恶魔", "img": "images/liu_xing.gif", "color": "🧡 橙色"},
    "道枝": {"nick": "道枝", "trait": "高挑帅气的长腿王子", "img": "images/mi_qi.gif", "color": "💖 粉色"},
    "谦杜": {"nick": "谦杜", "trait": "时尚又有主见的小恶魔末子", "img": "images/qian_du.gif", "color": "💛 黄色"}
}

USER_ROLES = ["初入职场的助理妹子", "粉丝", "青梅竹马", "在日留学生or打工人"]

# --- 原有的初始化逻辑 ---
if "page" not in st.session_state: st.session_state.page = "home"
if "user_name" not in st.session_state: st.session_state.user_name = "小浪花"
if "user_role" not in st.session_state: st.session_state.user_role = USER_ROLES[0]
if "selected_member" not in st.session_state: st.session_state.selected_member = None
if "current_act" not in st.session_state: st.session_state.current_act = 1
if "favorability" not in st.session_state: st.session_state.favorability = 50
if "story_history" not in st.session_state: st.session_state.story_history = []

# --- 原有的剧情逻辑 ---
def get_act_data(member, act, role):
    if act == 1:
        return {
            "title": "Act 1: 幕后的紧张时刻",
            "img": "images/act1_backstage.jpg",
            "text": f"离上台还有 10 分钟，{member} 一个人站在休息室门口发呆。",
            "choices": [
                {"text": "温柔鼓励", "favor": 15, "reply": "谢谢你，我安心多了！"},
                {"text": "督促检查", "favor": 5, "reply": "好的，我去准备。"},
                {"text": "严厉批评", "favor": -10, "reply": "抱歉，我这就过去……"}
            ]
        }
    return {"title": "结局", "img": "images/end.jpg", "text": "故事结束", "choices": []}

# --- 原有的页面渲染 (保持界面结构完全不变) ---
if st.session_state.page == "home":
    st.title("💖 浪花男子心动日常")
    st.write("欢迎来到与浪花男子的互动世界！请设置你的角色并抽取今天的男主角吧！")
    st.session_state.user_name = st.text_input("输入你的昵称：", value=st.session_state.user_name)
    st.session_state.user_role = st.selectbox("选择你的身份：", USER_ROLES)
    
    if st.button("🎰 开启心动抽卡！"):
        st.session_state.selected_member = random.choice(list(MEMBERS.keys()))
        st.rerun()

    if st.session_state.selected_member:
        m = MEMBERS[st.session_state.selected_member]
        st.success(f"抽中：{st.session_state.selected_member}")
        safe_image(m["img"]) # 这里使用了新功能
        if st.button("🚀 开始故事"):
            st.session_state.page = "story"
            st.rerun()

elif st.session_state.page == "story":
    act_data = get_act_data(st.session_state.selected_member, st.session_state.current_act, st.session_state.user_role)
    st.title(act_data["title"])
    safe_image(act_data["img"]) # 这里使用了新功能
    st.write(act_data["text"])
    for choice in act_data["choices"]:
        if st.button(choice["text"]):
            st.session_state.favorability += choice["favor"]
            st.session_state.current_act += 1
            st.rerun()
