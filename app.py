import streamlit as st
import random

# -----------------------------------------------------------------------------
# 1. 页面配置与样式
# -----------------------------------------------------------------------------
st.set_page_config(page_title="浪花男子心动日常", page_icon="💖", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 50%, #fce7f3 100%); }
    .main-header { font-size: 2.2rem; color: #e11d48; text-align: center; font-weight: bold; }
    .card-box { background: rgba(255, 255, 255, 0.95); padding: 20px; border-radius: 16px; border: 1px solid #fbcfe8; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 数据定义 (成员、道具、剧情)
# -----------------------------------------------------------------------------
MEMBERS = {
    "丈君": {"trait": "搞笑又可靠", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRxeLPXR2kAxnf8Z0uNFWIH7j_vjPcrr8Eg1qWtaTSoPKTvTMcZtXXX6Kn&s=10"},
    "大酱": {"trait": "热情太阳", "img": "https://gingerweb.jp/wp-content/uploads/2023/06/nishihatadaigo.jpg"},
    "布丁": {"trait": "温柔队长", "img": "https://img-mdpr.freetls.fastly.net/article/H0CW/nm/H0CW_-CrOagXoRlSyQPOD6_zSqLjGNjyrfLRLWlqECw.jpg?width=750"},
    "高恭": {"trait": "傲娇少年", "img": "https://img-mdpr.freetls.fastly.net/article/d4sb/nm/d4sbe7H-P8R6sUQpAshcntVT8-h0ZPcuMe3icV8aOm4.jpg?width=750"},
    "流星": {"trait": "小恶魔", "img": "https://oggi.jp/wp-content/uploads/2023/03/DMA-DSC00151_2-2.jpg"},
    "米七": {"trait": "长腿王子", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvYWZ1rSHkldisNtmwbvxSYNjR8FWjj4_wdyKxw84_h0SabJN81yYpsGXL&s=10"},
    "谦杜": {"trait": "时尚末子", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRs8ILDomyP9A6WZPtgig1e6IyPPmSpxS8HSYiRImU0uSqXicpvyNrHV8A&s=10"},
}

ITEMS = ["恋爱幸运符", "草莓牛奶", "应援荧光棒"]

# 剧情库 (10幕)
def get_story(member, act):
    scenarios = {
        1: ("后台初遇", "他在练习中文台词，看到你进来……"),
        2: ("异国茶歇", "休息间隙，他递给你一块抹茶饼干。"),
        3: ("深夜电车", "末班车上，你们并排坐在窗边。"),
        4: ("清晨关怀", "你感冒了，他特意为你带了咖啡。"),
        5: ("手作便当", "他拿出亲手做的饭菜，有点害羞。"),
        6: ("排练余温", "练习室只剩你们两人，空气微醺。"),
        7: ("大雨屋檐", "雨太大困在门前，伞只有一把。"),
        8: ("心声长谈", "深夜聊起对未来的不安与期许。"),
        9: ("离别时刻", "最后一天打工，到了要道别的时候。"),
        10: ("最终告白", "无论结果如何，这是最重要的时刻。")
    }
    return scenarios.get(act, ("日常", "平静的一天"))

# -----------------------------------------------------------------------------
# 3. Session State 管理
# -----------------------------------------------------------------------------
if "stage" not in st.session_state: st.session_state.stage = "draw"
if "score" not in st.session_state: st.session_state.score = 0
if "act" not in st.session_state: st.session_state.act = 1
if "member" not in st.session_state: st.session_state.member = None
if "inventory" not in st.session_state: st.session_state.inventory = []

# -----------------------------------------------------------------------------
# 4. 逻辑处理
# -----------------------------------------------------------------------------
st.markdown('<p class="main-header">💖 浪花男子心动日常</p>', unsafe_allow_html=True)

# 抽卡阶段
if st.session_state.stage == "draw":
    if st.button("抽选今日缘分对象"):
        st.session_state.member = random.choice(list(MEMBERS.keys()))
        st.session_state.inventory = [random.choice(ITEMS)]
        st.session_state.stage = "story"
        st.rerun()

# 剧情阶段
elif st.session_state.stage == "story":
    m = st.session_state.member
    act = st.session_state.act
    title, desc = get_story(m, act)
    
    st.image(MEMBERS[m]["img"], width=200)
    st.subheader(f"第 {act} 幕：{title}")
    st.write(desc)
    st.write(f"💼 拥有道具: {', '.join(st.session_state.inventory)}")
    
    # 互动选择
    col1, col2 = st.columns(2)
    with col1:
        if st.button("积极回应 (+10心动)"):
            st.session_state.score += 10
            st.session_state.act += 1
    with col2:
        if st.button("害羞回避 (+5心动)"):
            st.session_state.score += 5
            st.session_state.act += 1
            
    if st.session_state.act > 10:
        st.session_state.stage = "result"
        st.rerun()

# 结算阶段
elif st.session_state.stage == "result":
    st.success(f"最终心动指数：{st.session_state.score}")
    if st.session_state.score >= 80:
        st.write("💖 HE 结局：甜蜜告白！")
    else:
        st.write("🌙 BE 结局：遗憾错过。")
    
    if st.button("重新开始"):
        st.session_state.score = 0
        st.session_state.act = 1
        st.session_state.stage = "draw"
        st.rerun()
