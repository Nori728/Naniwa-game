import streamlit as st
import random
import os

# -----------------------------------------------------------------------------
# 1. 页面配置与绝对路径安全加载
# -----------------------------------------------------------------------------
st.set_page_config(page_title="浪花男子心动日常", page_icon="💖", layout="centered")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def safe_image(img_path, caption=None):
    if img_path:
        full_path = os.path.join(BASE_DIR, img_path) if not img_path.startswith("http") else img_path
        if img_path.startswith("http"):
            st.image(img_path, caption=caption, use_container_width=True)
        elif os.path.exists(full_path):
            st.image(full_path, caption=caption, use_container_width=True)
        else:
            st.warning(f"⚠️ 未找到图片：{img_path}，请检查文件名与路径。")

def safe_audio(audio_path):
    if audio_path:
        full_path = os.path.join(BASE_DIR, audio_path) if not audio_path.startswith("http") else audio_path
        if audio_path.startswith("http") or os.path.exists(full_path):
            try:
                st.audio(full_path, loop=True, autoplay=True)
            except Exception:
                pass

# -----------------------------------------------------------------------------
# 2. 浪花男子人物设定与角色配置
# -----------------------------------------------------------------------------
MEMBERS = {
    "丈君": {
        "nick": "丈君",
        "trait": "搞笑又可靠的大哥哥",
        "img": "images/zhang_jun.gif",
        "color": "💙 蓝色"
    },
    "大西": {
        "nick": "大西",
        "trait": "热情太阳般的 C 位",
        "img": "images/da_jiang.gif",
        "color": "🔴 红色"
    },
    "布丁": {
        "nick": "布丁",
        "trait": "温柔体贴又吃得超香的队长",
        "img": "images/bu_ding.gif",
        "color": "💚 绿色"
    },
    "高恭": {
        "nick": "高恭",
        "trait": "自恋又亚撒西的八嘎帅哥，实则运动超强",
        "img": "images/gao_gong.gif",
        "color": "💜 紫色"
    },
    "流星": {
        "nick": "流星",
        "trait": "眼睛会闪光的小恶魔",
        "img": "images/liu_xing.gif",
        "color": "🧡 橙色"
    },
    "道枝": {
        "nick": "道枝",
        "trait": "高挑帅气的长腿王子",
        "img": "images/mi_qi.gif",
        "color": "💖 粉色"
    },
    "谦杜": {
        "nick": "谦杜",
        "trait": "时尚又有主见的小恶魔末子",
        "img": "images/qian_du.gif",
        "color": "💛 黄色"
    }
}

USER_ROLES = ["初入职场的助理妹子", "粉丝", "青梅竹马", "在日留学生or打工人"]

# -----------------------------------------------------------------------------
# 3. Session State 状态初始化
# -----------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user_name" not in st.session_state:
    st.session_state.user_name = "小浪花"
if "user_role" not in st.session_state:
    st.session_state.user_role = USER_ROLES[0]
if "selected_member" not in st.session_state:
    st.session_state.selected_member = None
if "current_act" not in st.session_state:
    st.session_state.current_act = 1
if "favorability" not in st.session_state:
    st.session_state.favorability = 50
if "story_history" not in st.session_state:
    st.session_state.story_history = []

# -----------------------------------------------------------------------------
# 4. 3幕分段剧情定义
# -----------------------------------------------------------------------------
def get_act_data(member, act, role):
    if act == 1:
        return {
            "title": "Act 1: 幕后的紧张时刻",
            "img": "images/act1_backstage.jpg",
            "bgm": "audio/bgm_gentle.mp3",
            "text": f"离上台还有 10 分钟，{member} 一个人站在休息室门口发呆，看起来有些紧张。",
            "choices": [
                {"text": f"递上热茶温柔鼓励：『别担心，{member} 排练得很完美，相信自己！』", "favor": 15, "reply": f"{member} 愣了一下，接过热茶笑了出来：『谢谢你，{role}，听到你这么说我安心多了！』"},
                {"text": f"敲敲表格提醒：『{member}，还有 10 分钟，记得检查麦克风。』", "favor": 5, "reply": f"{member} 点了点头：『好的，收到了，我这就去准备。』"},
                {"text": "严厉督促：『怎么还在发呆？大家都在等你呢！』", "favor": -10, "reply": f"{member} 显得有些沮丧，低声道：『抱歉，我这就过去……』"}
            ]
        }
    elif act == 2:
        return {
            "title": "Act 2: 突发状况与默契",
            "img": "images/act2_stage.jpg",
            "bgm": "audio/bgm_upbeat.mp3",
            "text": f"演出途中道具出了点小状况，{member} 灵巧地化解后走下舞台，擦着汗对你微微一笑。",
            "choices": [
                {"text": "立刻递上毛巾和水：『刚才应变太棒了！完全没看出破绽！』", "favor": 15, "reply": f"{member} 眼睛一亮：『多亏你在台下给我打气，不然我也悬着一口气！』"},
                {"text": "比出大拇指赞许：『表现完美，继续保持！』", "favor": 10, "reply": f"{member} 露出自信的笑容：『那是当然，我们可是最棒的！』"},
                {"text": "冷淡地核对下半场流程：『下半场别再出岔子了。』", "favor": -5, "reply": f"{member} 轻声叹了口气，没再说什么。"}
            ]
        }
    else:
        return {
            "title": "Act 3: 属于两人的特别感谢",
            "img": "images/act3_sunset.jpg",
            "bgm": "audio/bgm_sweet.mp3",
            "text": f"演唱会圆满落幕，夕阳下，{member} 单独走过来叫住了你。",
            "choices": [
                {"text": f"『今天大家都辛苦了，{member} 今天特别闪耀哦！』", "favor": 20, "reply": f"{member} 脸微红，看着你的眼睛：『比起舞台上的闪耀，我更希望能在你心里一直闪耀……』"},
                {"text": "『收拾得差不多了，准备回去了吗？』", "favor": 5, "reply": f"{member} 笑了笑：『嗯，今天很充实，辛苦啦。』"},
                {"text": "『我也要下班了，再见。』", "favor": 0, "reply": f"{member} 挥了挥手：『拜拜，路上小心。』"}
            ]
        }

# -----------------------------------------------------------------------------
# 5. 页面渲染逻辑
# -----------------------------------------------------------------------------
if st.session_state.page == "home":
    st.title("💖 浪花男子心动日常")
    st.write("欢迎来到与浪花男子的互动世界！请设置你的角色并抽取今天的男主角吧！")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.user_name = st.text_input("输入你的昵称：", value=st.session_state.user_name)
    with col2:
        st.session_state.user_role = st.selectbox("选择你的身份：", USER_ROLES)
    
    st.markdown("---")
    
    if st.button("🎰 开启心动抽卡！", use_container_width=True):
        selected = random.choice(list(MEMBERS.keys()))
        st.session_state.selected_member = selected
        st.session_state.favorability = 50
        st.session_state.current_act = 1
        st.session_state.story_history = []
        st.balloons()

    if st.session_state.selected_member:
        m_info = MEMBERS[st.session_state.selected_member]
        st.success(f"🎉 恭喜你抽中了：**{st.session_state.selected_member}**！")
        
        safe_image(m_info["img"], caption=f"{m_info['nick']} - {m_info['trait']}")
        
        st.write(f"**应援色：** {m_info['color']}")
        st.write(f"**性格特点：** {m_info['trait']}")
        
        if st.button("🚀 开始我们的故事！", use_container_width=True):
            st.session_state.page = "story"
            st.rerun()

elif st.session_state.page == "story":
    member = st.session_state.selected_member
    act = st.session_state.current_act
    role = st.session_state.user_role
    act_data = get_act_data(member, act, role)
    
    st.title(f"📖 {act_data['title']}")
    st.caption(f"当前与 **{member}** 的好感度：{st.session_state.favorability} ❤️")
    
    safe_image(act_data["img"])
    safe_audio(act_data["bgm"])
    
    st.info(act_data["text"])
    
    st.write("👉 请做出你的回应选择：")
    for idx, choice in enumerate(act_data["choices"]):
        if st.button(f"{chr(65+idx)} {choice['text']}", key=f"choice_{act}_{idx}", use_container_width=True):
            st.session_state.favorability += choice["favor"]
            st.session_state.story_history.append({
                "act": act,
                "choice": choice["text"],
                "reply": choice["reply"]
            })
            if act < 3:
                st.session_state.current_act += 1
                st.rerun()
            else:
                st.session_state.page = "result"
                st.rerun()

elif st.session_state.page == "result":
    member = st.session_state.selected_member
    fav = st.session_state.favorability
    
    st.title("🌟 结局时刻")
    st.write(f"与 **{member}** 的最终好感度为：**{fav}** 分！")
    
    if fav >= 80:
        st.balloons()
        st.success(f"✨ **【 Happy Ending 】心有灵犀！**\n\n{member} 轻轻拉住你的手：『以后所有的舞台和日常，我都希望有你在身边。』")
    elif fav >= 50:
        st.info(f"🌸 **【 True Ending 】默契搭档！**\n\n{member} 对你笑着挥手：『今天合作很愉快，下次也要加油哦！』")
    else:
        st.warning(f"🌧️ **【 Bad Ending 】有些疏离……**\n\n{member} 礼貌地告别：『今天辛苦了，早点休息吧。』")
        
    st.markdown("---")
    st.subheader("📝 你们的心动回忆")
    for item in st.session_state.story_history:
        st.write(f"**Act {item['act']} 回应：** {item['choice']}")
        st.write(f"💬 **{member} 的回复：** {item['reply']}")
        st.write("---")
        
    if st.button("🔄 重新开始抽取新成员", use_container_width=True):
        st.session_state.page = "home"
        st.session_state.selected_member = None
        st.rerun()
