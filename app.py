import streamlit as st
import random

# -----------------------------------------------------------------------------
# 1. 页面基本配置与样式
# -----------------------------------------------------------------------------
st.set_page_config(page_title="浪花男子心动日常", page_icon="💖", layout="centered")

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
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 2. 基础数据源
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

ROLES = ["经纪人", "青梅竹马", "在日学生or打工人"]
MAX_ACT = 10

# -----------------------------------------------------------------------------
# 3. 10幕完整剧情生成器 (包含早晚时间流逝与几天几夜的真实陪伴感)
# -----------------------------------------------------------------------------
def get_10_act_story(member, role, act):
    stories = {
        1: {
            "title": f"🎬 {member} × {role} · 第 1 幕：后台初遇 (第 1 天·早晨)",
            "choices": [
                ("耐心微笑着纠正他的发音与台词", f"『有你这么细心地指导，我感觉今天的状态好极了！』", 10),
                ("递上一份热腾腾的早餐和资料", f"『哇，太贴心了吧！一早能看到你，今天工作绝对动力满满。』", 10),
                ("公事公办地催促：『快点对完台词，要开工了。』", f"『遵命大总管！不过……能不能多给我一个鼓励的眼神嘛？』", 5)
            ]
        },
        2: {
            "title": f"🎬 {member} × {role} · 第 2 幕：异国茶歇 (第 1 天·下午)",
            "choices": [
                ("分享自己带的家乡点心", f"『真的超级好吃！谢谢你特意留给我，心里暖洋洋的。』", 10),
                ("调侃他刚才采访时吃螺丝的可爱样子", f"『喂！那纯属意外啦！不准笑话我，要补偿我一个笑脸！』", 8),
                ("安静地在一旁陪着他休息，递上纸巾", f"『每次累了只要看到你在，我就觉得特别安心。』", 10)
            ]
        },
        3: {
            "title": f"🎬 {member} × {role} · 第 3 幕：电车站台 (第 1 天·深夜)",
            "choices": [
                ("买两罐热饮，把其中一罐贴在他冰凉的脸颊上", f"『好冰……不过，你的手心比饮料还要暖和呢。』", 10),
                ("默默并肩站着，看着末班车缓缓驶来", f"『真希望这条路没有尽头，能一直和你这样安静地走下去。』", 10),
                ("催促他快上车：『明天还要早起，快回去休息吧。』", f"『好吧……那明天一睁眼，你可要第一个给我发信息哦！』", 7)
            ]
        },
        4: {
            "title": f"🎬 {member} × {role} · 第 4 幕：晨起突发 (第 2 天·早晨)",
            "choices": [
                ("发现他有些着凉，关切地递上感冒药", f"『这点小感冒没事的……不过能让你这么关心我，突然觉得生病也挺赚的。』", 10),
                ("笑话他昨晚踢被子：『大明星也会着凉呀？』", f"『才没有踢被子！……好啦，谢谢你特意来看我。』", 7),
                ("默默帮他调整房间空调温度", f"『有你在身边照顾，我感觉自己快要被你宠坏了。』", 10)
            ]
        },
        5: {
            "title": f"🎬 {member} × {role} · 第 5 幕：手作便当 (第 2 天·中午)",
            "choices": [
                ("惊喜地尝了一口他亲手做的便当", f"『怎么样？虽然卖相一般，但这可是我满满的心意哦！』", 10),
                ("不好意思地推辞：『这怎么好意思让你破费呢。』", f"『别客气嘛，快尝尝看合不合你的胃口！』", 7),
                ("开玩笑：『味道一般般，罚你明天再做一次！』", f"『遵命！只要你想吃，我天天做给你吃都行！』", 10)
            ]
        },
        6: {
            "title": f"🎬 {member} × {role} · 第 6 幕：空旷排练室 (第 2 天·傍晚)",
            "choices": [
                ("帮他关掉练习室的大灯，只留一盏小夜灯", f"『灯光暗下来之后，我满眼就只剩下你的身影了……』", 10),
                ("认真陪他复盘今天的舞蹈动作", f"『有你这个最棒的专属监督在，我绝对能拿满分！』", 10),
                ("催促他赶紧收工去吃大餐", f"『走吧！今天必须得去吃顿好的，好好犒劳一下我们自己！』", 8)
            ]
        },
        7: {
            "title": f"🎬 {member} × {role} · 第 7 幕：雨中屋檐 (第 3 天·下午)",
            "choices": [
                ("两人挤在同一把小伞下，肩膀紧紧相贴", f"『伞有点小呢……不过没关系，这样离你更近了。』", 10),
                ("把伞全部倾斜到他那边：『别淋湿了。』", f"『笨蛋，那你自己呢？快过来一点，别着凉了！』", 10),
                ("提议一起踩水花跑向便利店", f"『哈哈，难得看你这么幼稚，那我就奉陪到底啦！』", 8)
            ]
        },
        8: {
            "title": f"🎬 {member} × {role} · 第 8 幕：深夜走心长谈 (第 3 天·深夜)",
            "choices": [
                ("坚定地握住他的手：『别怕，不管未来多远我都陪着你。』", f"『有你这句话，我心里所有的迷茫和不安瞬间就消失了。』", 10),
                ("拍拍他肩膀：『累了就靠在我肩膀上休息。』", f"『那我不客气了……你的肩膀，真的让人很有安全感。』", 10),
                ("默默听他倾诉，递上一杯热牛奶", f"『谢谢你愿意听我倒苦水，你总是这么懂我。』", 8)
            ]
        },
        9: {
            "title": f"🎬 {member} × {role} · 第 9 幕：离别倒计时 (第 4 天·傍晚)",
            "choices": [
                ("郑重地与他许下未来的约定", f"『一言为定！不管以后走到哪，我们的心永远在一起。』", 10),
                ("把准备好的离别小礼物塞进他口袋", f"『这是……太惊喜了！我会一辈子好好珍藏它的。』", 10),
                ("笑着掩饰眼角的泪水：『以后要常联系哦。』", f"『不许哭！我会经常去找你的，绝对不会让你孤单。』", 8)
            ]
        },
        10: {
            "title": f"🎬 {member} × {role} · 第 10 幕：终章抉择 (最终结算)",
            "choices": [] # 最后一幕展示结算结局
        }
    }
    return stories.get(act, stories[1])

# -----------------------------------------------------------------------------
# 4. Session State 初始化
# -----------------------------------------------------------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "menu"
if "player_role" not in st.session_state:
    st.session_state.player_role = ROLES[0]
if "target_member" not in st.session_state:
    st.session_state.target_member = "大酱"
if "current_act" not in st.session_state:
    st.session_state.current_act = 1
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "dialogue_history" not in st.session_state:
    st.session_state.dialogue_history = []

# -----------------------------------------------------------------------------
# 5. 页面核心渲染
# -----------------------------------------------------------------------------
st.markdown('<p class="main-header">💖 浪花男子心动日常</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">✨ 7人全员 × 10幕沉浸式日常 (几天几夜、早晚时间流逝与多重结局)</p>', unsafe_allow_html=True)

# 菜单阶段
if st.session_state.stage == "menu":
    st.subheader("📖 开启 10 幕沉浸式恋爱剧情")
    
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
    
    if st.button("✨ 开始 10 幕沉浸式恋爱旅程 ➔", type="primary", use_container_width=True):
        st.session_state.player_role = selected_role
        st.session_state.target_member = selected_member
        st.session_state.current_act = 1
        st.session_state.total_score = 0
        st.session_state.dialogue_history = []
        st.session_state.stage = "story"
        st.rerun()

# 剧情互动阶段 (第 1 到 9 幕)
elif st.session_state.stage == "story" and st.session_state.current_act < MAX_ACT:
    role = st.session_state.player_role
    member = st.session_state.target_member
    act = st.session_state.current_act
    m_info = MEMBERS[member]
    
    scene_data = get_10_act_story(member, role, act)
    
    st.markdown(f"### 💖 【{role}】 × **{member}** (第 {act}/{MAX_ACT} 幕)")
    st.info(f"💓 当前累计心动指数：**{st.session_state.total_score} 分**")
    
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
            st.session_state.dialogue_history.append({
                "choice_text": c_text,
                "reply_text": r_text
            })
            st.session_state.total_score += score_val
            st.session_state.current_act += 1
            if st.session_state.current_act >= MAX_ACT:
                st.session_state.stage = "result"
            st.rerun()
            
    st.markdown("---")
    if st.button("🏠 返回主菜单"):
        st.session_state.stage = "menu"
        st.rerun()

# 结算阶段 (第 10 幕 - 多重结局判定)
elif st.session_state.stage == "result" or (st.session_state.stage == "story" and st.session_state.current_act >= MAX_ACT):
    role = st.session_st
