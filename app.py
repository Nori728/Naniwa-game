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
    "大酱": {"trait": "热情太阳般的 C 位", "color": "红色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEiQYHWo7za_O6O-FerVkj5mA2s49UBL3hj_Tfmu-npd2yfIz1OJSCHD8n&s=10"},
    "布丁": {"trait": "温柔体贴又元气的队长", "color": "绿色", "img": "https://img-mdpr.freetls.fastly.net/article/H0CW/nm/H0CW_-CrOagXoRlSyQPOD6_zSqLjGNjyrfLRLWlqECw.jpg?width=750"},
    "高恭": {"trait": "自恋又帅气的傲娇少年", "color": "紫色", "img": "https://img-mdpr.freetls.fastly.net/article/d4sb/nm/d4sbe7H-P8R6sUQpAshcntVT8-h0ZPcuMe3icV8aOm4.jpg?width=750"},
    "流星": {"trait": "眼睛会闪光的小恶魔", "color": "橙色", "img": "https://oggi.jp/wp-content/uploads/2023/03/DMA-DSC00151_2-2.jpg"},
    "米七": {"trait": "高挑清纯的长腿王子", "color": "粉色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvYWZ1rSHkldisNtmwbvxSYNjR8FWjj4_wdyKxw84_h0SabJN81yYpsGXL&s=10"},
    "谦杜": {"trait": "时尚又有主见的末子", "color": "黄色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRs8ILDomyP9A6WZPtgig1e6IyPPmSpxS8HSYiRImU0uSqXicpvyNrHV8A&s=10"},
}

ROLES = ["经纪人", "青梅竹马", "在日留学生or打工人"]
MAX_ACT = 4

# -----------------------------------------------------------------------------
# 3. 完整独立剧情库 (确保任何成员在任何幕都有内容，绝不报错)
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
            ("害羞地低下头避
