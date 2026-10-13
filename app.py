import random
import time
import streamlit as st

# 1. 页面基础配置
st.set_page_config(
    page_title="偶像培养计划：星途甄选 2.0",
    page_icon="💖",
    layout="centered",
)

# 2. 杰尼斯 / STARTO 组合与最新成员数据
IDOL_GROUPS = {
    "KEY TO LIT": ["岩崎大昇", "井上瑞稀", "中村岭亚", "猪狩苍弥", "佐佐木大光"],
    "B&ZAI": [
        "桥本凉",
        "矢花黎",
        "今野大辉",
        "菅田琳宁",
        "本高克树",
        "铃木悠仁",
        "川崎星辉",
        "稻叶通阳",
    ],
    "ACEes": ["浮所飞贵", "那须雄登", "作间龙斗", "深田龙生", "佐藤龙我"],
    "Aぇ! group (A少年)": [
        "末泽诚也",
        "正门良规",
        "草间理查德敬太",
        "小岛健",
        "佐野晶哉",
    ],
    "浪花男子 (なにわ男子)": [
        "道枝骏佑",
        "西畑大吾",
        "大西流星",
        "高桥恭平",
        "长尾谦杜",
        "藤原丈一郎",
        "大桥和也",
    ],
    "SUPER EIGHT": ["横山裕", "村上信五", "丸山隆平", "安田章大", "大仓忠义"],
    "Snow Man": [
        "目黑莲",
        "岩本照",
        "深泽辰哉",
        "ラウール",
        "渡边翔太",
        "向井康二",
        "阿部亮平",
        "宫馆凉太",
        "佐久间大介",
    ],
    "SixTONES": [
        "松村北斗",
        "京本大我",
        "田中树",
        "杰西 (Jesse)",
        "高地优吾",
        "森本慎太郎",
    ],
    "King & Prince": ["平野紫耀", "永濑廉", "高桥海人", "岸优太", "神宫寺勇太"],
    "Travis Japan": [
        "宫近海斗",
        "松田元太",
        "七五三挂龙也",
        "中村海人",
        "川岛如惠留",
        "吉泽闲也",
        "松仓海斗",
    ],
}

# 3. 超可爱高颜值 CSS 样式与高对比卡片
st.markdown(
    """
    <style>
    /* 全局背景与字体 */
    .stApp {
        background: linear-gradient(135deg, #fce4ec 0%, #f3e5f5 100%);
    }
    
    /* 考核卡片：高对比深色亮字 */
    .event-card {
        background: #2d1b4e;
        color: #ffffff;
        padding: 22px;
        border-radius: 18px;
        border: 3px solid #ff80ab;
        box-shadow: 0px 10px 25px rgba(255, 128, 171, 0.3);
        margin: 20px 0;
        font-size: 16px;
        line-height: 1.6;
    }
    
    .event-title {
        font-size: 20px;
        font-weight: 800;
        color: #ff80ab;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* 可爱提示框 */
    .cute-info {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 15px;
        border: 2px dashed #ff4081;
        color: #4a148c;
        font-weight: 600;
        margin-bottom: 15px;
    }

    /* Streamlit 单选框样式调整 */
    div[data-testid="stRadio"] > label {
        font-size: 18px !important;
        font-weight: bold !important;
        color: #4a148c !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label {
        background-color: #ffffff;
        padding: 12px 18px;
        border-radius: 15px;
        margin-bottom: 8px;
        border: 2px solid #ea80fc;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background-color: #f3e5f5;
        border-color: #ff4081;
        transform: translateY(-2px);
    }

    /* 可爱按钮外观 */
    .stButton > button {
        background: linear-gradient(45deg, #ff4081, #ab47bc) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 12px 30px !important;
        box-shadow: 0 6px 15px rgba(255, 64, 129, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: scale(1.05) !important;
