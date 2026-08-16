# -*- coding: utf-8 -*-
import streamlit as st
import random
import os

# -----------------------------------------------------------------------------
# 1. 页面基本配置
# -----------------------------------------------------------------------------
st.set_page_config(page_title="浪花男子心动日常·七人独立博弈篇", page_icon="💖", layout="centered")

# -----------------------------------------------------------------------------
# 2. 七位成员独立人设与个性化标签配置
# -----------------------------------------------------------------------------
MEMBERS = {
    "丈君": {"nick": "丈君", "trait": "搞笑又可靠、自带关西方言语调的大哥哥", "color": "💙 蓝色"},
    "大酱": {"nick": "大酱", "trait": "热情如火、随时散发C位光芒的太阳", "color": "🔴 红色"},
    "布丁": {"nick": "布丁", "trait": "温柔体贴、偶尔带点小腹黑的队长", "color": "💚 绿色"},
    "高恭": {"nick": "高恭", "trait": "嘴硬心软、自带反差萌的傲娇帅哥", "color": "💜 紫色"},
    "流星": {"nick": "流星", "trait": "眼神会放电、让人捉摸不透的小恶魔", "color": "🧡 橙色"},
    "米七": {"nick": "米七", "trait": "高挑温柔、拥有让人沦陷眼神的长腿王子", "color": "💖 粉色"},
    "谦杜": {"nick": "谦杜", "trait": "时尚敏锐、喜欢出其不意的小恶魔末子", "color": "💛 黄色"},
}

ROLES = ["经纪人", "粉丝/地下恋", "青梅竹马", "在日留学生or打工人"]

# -----------------------------------------------------------------------------
# 3. Session State 状态初始化
# -----------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "role" not in st.session_state:
    st.session_state.role = None
if "target" not in st.session_state:
    st.session_state.target = None
if "act" not in st.session_state:
    st.session_state.act = 1
if "tension" not in st.session_state:
    st.session_state.tension = 0
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------------------------------------------------------
# 4. 七人独立性格匹配的动态剧情生成引擎
# -----------------------------------------------------------------------------
def get_act_data(role, target, act):
    t = target
    
    # -------- 示例：针对不同成员在不同幕和身份下的“独立性格定制” --------
    # 你可以在这里为 7 个人分别定制完全不一样的台词和反应！
    
    # 【藤原丈一郎 (丈君) 的独立剧情范例】
    if target == "丈君":
        if role == "经纪人":
            if act == 1:
                return {
                    "title": "🎬 第一幕：后台的关西腔吐槽",
                    "desc": f"离上台还有 10 分钟，丈君正拿着台本碎碎念，看到你走过来，立刻露出了标志性的搞怪笑容。",
                    "choices": [
                        {"label": "🅰️ 拍拍他的肩：『别紧张，大不了讲个冷笑话热场。』", "dialogue": f"『喂喂！我可是认真的偶像好不好！不过……被你这么一说，紧张感全飞光了啦。』", "tension": 15},
                        {"label": "🅱️ 严肃检查行程：『笑什么笑，台本背熟了吗？』", "dialogue": f"『嗨嗨，经纪人大人最严格了……放心吧，绝对完美过关！』", "tension": 5},
                        {"label": "🆎 假装无视：『那我去找别人对流程了。』", "dialogue": f"『诶！别走啊！好歹多看我一眼嘛！』(急忙伸手拉住你的衣角)", "tension": 10}
                    ]
                }
            elif act == 2:
                return {
                    "title": "🎬 第二幕：突发舞台事故的默契",
                    "desc": f"直播中麦克风突然没声音，全场一瞬间安静，丈君却精准地用眼神向你求助。",
                    "choices": [
                        {"label": "🅰️ 迅速切备用麦，并在台下做了一个大大的‘OK’手势。", "dialogue": f"在台上看到你的手势后瞬间安心，完美控场并冲着镜头方向露出了只有你懂的灿烂笑容。", "tension": 20},
                        {"label": "🅱️ 赶紧指挥其他工作人员进行切换。", "dialogue": f"顺利救场后下台，擦着汗松了口气：『刚才真是吓死我了，还好有你在！』", "tension": 10},
                        {"label": "🆎 紧张得呆在原地不知所措。", "dialogue": f"虽然凭借经验圆了过去，但下台后忍不住吐槽你：『关键时刻怎么比我还慌啊？』", "tension": -5}
                    ]
                }
            elif act == 3:
                return {
                    "title": "🎬 第三幕：深夜保姆车的真心话",
                    "desc": f"深夜收工的车里，丈君疲惫地靠着窗，突然转过头认真地看着你。",
                    "choices": [
                        {"label": "🅰️ 递过热罐装咖啡：『今天辛苦了，大明星。』", "dialogue": f"『有你在身边，再累也值了……呐，以后收工后也陪我多走一会儿吧？』", "tension": 25},
                        {"label": "🅱️ 看着窗外：『快闭眼休息吧，还有通告呢。』", "dialogue": f"『真是个铁石心肠的经纪人……偶尔也多关心关心我嘛。』", "tension": 10},
                        {"label": "🆎 转头笑问：『怎么，想加工资了？』", "dialogue": f"『钱可买不到我想对你说的话……笨蛋。』(小声嘟囔)", "tension": 15}
                    ]
                }
        # 如果是其他身份，可继续拓展……

    # 【默认/其他成员的独立张力框架（当匹配到其他成员时自动加载对应风格）】
    # 你可以依葫芦画瓢，为“大酱、布丁、高恭、流星、米七、谦杜”写出他们各自性格的专属对白！
    
    # 作为一个健壮的通用兜底，确保任意角色都有高质量的互动：
    return {
        "title": f"🎬 第 {act} 幕：与 {t} 的心动博弈",
        "desc": f"在灯光与视线的交错中，{t} 正在等待你的回应，空气中弥漫着微妙的张力。",
        "choices": [
            {"label": "🅰️ 迎上他的目光，主动打破沉默。", "dialogue": f"『（微微一愣，随即勾起嘴角）你总是能轻易扰乱我的节奏……』", "tension": 20},
            {"label": "🅱️ 保持安全距离，公事公办地微笑。", "dialogue": f"『（眼神中闪过一丝失落）又用这招来敷衍我吗……』", "tension": 10},
            {"label": "🆎 调侃一句，试图掩饰内心的波澜。", "dialogue": f"『（无奈地笑出声）拿你真是一点办法也没有。』", "tension": 15}
        ]
    }

# -----------------------------------------------------------------------------
# 5. 主页面逻辑渲染
# -----------------------------------------------------------------------------
if st.session_state.page == "home":
    st.title("💖 浪花男子心动日常·七人独立博弈篇 💖")
    st.write("选择你的心动目标与身份，体验七位成员完全不同的专属互动剧情与情感张力！")
    
    st.subheader("1. 选择你的心动男主角")
    cols = st.columns(4)
    target_names = list(MEMBERS.keys())
    for idx, name in enumerate(target_names):
        col = cols[idx % 4]
        with col:
            m = MEMBERS[name]
            st.markdown(f"**{m['nick']}**")
            st.caption(m['color'])
            if st.button(f"选择 {name}", key=f"btn_{name}"):
                st.session_state.target = name
                st.rerun()

    if st.session_state.target:
        st.success(f"已选择心动目标：**{st.session_state.target}** ({MEMBERS[st.session_state.target]['trait']})")

    st.markdown("---")
    st.subheader("2. 选择你在故事中的身份")
    selected_role = st.selectbox("请下拉选择身份：", ROLES)
    st.session_state.role = selected_role

    st.markdown("---")
    if st.button("🚀 开启独立心动博弈", type="primary", use_column_width=True):
        if not st.session_state.target:
            st.warning("请先选择一位心动男主角哦！")
        else:
            st.session_state.page = "story"
            st.session_state.act = 1
            st.session_state.tension = 0
            st.session_state.history = []
            st.rerun()

elif st.session_state.page == "story":
    target = st.session_state.target
    role = st.session_state.role
    act = st.session_state.act
    
    st.title(f"💖 {target} × {role} (第 {act} 幕)")
    st.markdown(f"当前情感张力 (Tension): **{st.session_state.tension}**")
    st.markdown("---")
    
    current_data = get_act_data(role, target, act)
    
    st.subheader(current_data["title"])
    st.write(current_data["desc"])
    st.markdown("---")
    
    choice_labels = [c["label"] for c in current_data["choices"]]
    selected_choice = st.radio("请做出你的选择：", choice_labels, key=f"act_{act}_choice")
    
    if st.button("确认选择", type="primary"):
        chosen_dict = next(c for c in current_data["choices"] if c["label"] == selected_choice)
        
        st.session_state.tension += chosen_dict["tension"]
        st.session_state.history.append({
            "act": act,
            "title": current_data["title"],
            "choice": selected_choice,
            "dialogue": chosen_dict["dialogue"]
        })
        
        st.info(f"**{target} 的反应：**\n\n{chosen_dict['dialogue']}")
        
        if act < 3:
            if st.button("进入下一幕 ➡️", key=f"next_{act}"):
                st.session_state.act += 1
                st.rerun()
        else:
            if st.button("揭晓最终走向 ✨", key="to_result"):
                st.session_state.page = "result"
                st.rerun()

elif st.session_state.page == "result":
    st.title("✨ 情感博弈·最终走向 ✨")
    target = st.session_state.target
    role = st.session_state.role
    tension = st.session_state.tension
    
    st.markdown(f"### 🎯 目标：{target} | 身份：{role}")
    st.markdown(f"### ⚡ 最终情感张力指数：**{tension}**")
    st.markdown("---")
    
    if tension >= 60:
        st.markdown("🔥 **【极限拉扯·危险同谋】**")
        st.write(f"你们的每一次交锋都像是在刀尖上跳舞，满溢的占有欲与克制将空气烧得滚烫。在聚光灯照不到的阴影里，{target} 贴在你的耳边，用沙哑的声音宣告：『既然你敢把火点起来，就别想轻易抽身。从今以后，我们只能绑死在一起。』")
    elif tension >= 30:
        st.markdown("🌙 **【暧昧试探·无声对峙】**")
        st.write(f"你们维持着一种微妙而危险的平衡。谁也没有彻底捅破那层窗户纸，但在无数个眼神交汇的瞬间，汹涌的情感早已心照不宣。{target} 常常在深夜看着你的方向，轻轻勾起嘴角：『真狡猾啊你……明明把我的心搅得一团乱，却还装作什么都没发生。』")
    elif tension >= 0:
        st.markdown("🌫️ **【平行交错·未完待续】**")
        st.write(f"因为彼此的克制与防备，你们的关系始终隔着一层薄雾。看着 {target} 渐行渐远的背影，空气中只留下一句悬而未决的低语：『如果当时再多踏出一步，结局会不会不一样？』")
    else:
        st.markdown("❄️ **【冰层之下的暗涌】**")
        st.write(f"过度的试探与疏离让气氛降至冰点。{target} 在转头时，眼底闪过一丝倔强与不甘：『你就这么想跟我划清界限吗？……好，那就走着瞧。』")
        
    st.markdown("---")
    st.subheader("📜 你的博弈轨迹回顾：")
    for h in st.session_state.history:
        st.markdown(f"**{h['title']}**")
        st.markdown(f"- 你的选择：{h['choice']}")
        st.markdown(f"- 他的反应：{h['dialogue']}")
        st.markdown("---")
        
    if st.button("🔄 重新开启新博弈", type="primary"):
        st.session_state.page = "home"
        st.session_state.act = 1
        st.session_state.tension = 0
        st.session_state.history = []
        st.session_state.target = None
        st.rerun()
