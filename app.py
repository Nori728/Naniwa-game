import streamlit as st
import random

# --- 1. 修正后的专属配色配置 ---
# 丈君-蓝, 大酱-红, 布丁-绿, 高恭-紫, 流星-橙, 米七-粉, 谦杜-黄
CHARACTERS = {
    "丈君": {"color": "#0068C9"}, 
    "大酱": {"color": "#FF4B4B"}, 
    "布丁": {"color": "#28a745"}, 
    "高恭": {"color": "#6f42c1"}, 
    "流星": {"color": "#fd7e14"}, 
    "米七": {"color": "#ff69b4"}, 
    "谦杜": {"color": "#FFD700"}
}

# --- 2. 初始化 ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'stage' not in st.session_state: st.session_state.stage = 1
if 'name' not in st.session_state: st.session_state.name = "丈君"

# --- 3. 动态 CSS 注入 (颜色锁定) ---
def apply_style(name):
    color = CHARACTERS.get(name, {"color": "#000000"})["color"]
    st.markdown(f"""
        <style>
            h1 {{ color: {color}; }}
            .stButton>button {{ border: 2px solid {color}; }}
            .highlight {{ color: {color}; font-weight: bold; }}
        </style>
    """, unsafe_allow_html=True)

apply_style(st.session_state.name)

# --- 4. 主界面渲染 ---
st.title(f"💖 与 {st.session_state.name} 的故事")

# 假设这里是你原本的图片显示逻辑，不需要我改动
# 如果你的图片变量存在，直接使用即可
st.image(f"你的图片路径/{st.session_state.name}.jpg", caption=f"{st.session_state.name}")

# 显示好感度 (使用你指定的配色)
st.markdown(f"当前好感度: <span class='highlight'>{st.session_state.score}</span>", unsafe_allow_html=True)

# --- 5. 核心逻辑 ---
# 随机事件与道具逻辑保持不变，但会遵循你设定的颜色
def trigger_random_event():
    if random.random() < 0.15:
        st.warning("⚡ 随机事件发生！")
        st.session_state.score += 5

trigger_random_event()

# 剧情渲染 (5幕框架)
st.write(f"第 {st.session_state.stage} 幕进行中...")
# 在这里放入你的剧情选项代码即可
