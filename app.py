import streamlit as st
import random
import os

# -----------------------------------------------------------------------------
# 1. 页面基本配置与安全加载
# -----------------------------------------------------------------------------
st.set_page_config(page_title="浪花男子心动日常", page_icon="💖", layout="centered")

def safe_image(img_path, caption=None):
    if not img_path:
        return
    if str(img_path).startswith("http"):
        st.image(img_path, caption=caption, use_container_width=True)
    elif os.path.exists(img_path):
        st.image(img_path, caption=caption, use_container_width=True)
    else:
        st.warning(f"图片路径或网址无法加载: {img_path}")

def safe_audio(audio_path):
    if audio_path and os.path.exists(audio_path):
        try:
            st.audio(audio_path, loop=True, autoplay=True)
        except Exception:
            pass

# -----------------------------------------------------------------------------
# 2. 成员与身份数据配置 (已完美填入你的专属网络图片)
# -----------------------------------------------------------------------------
BG_IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEiQYHWo7za_O6O-FerVkj5mA2s49UBL3hj_Tfmu-npd2yfIz1OJSCHD8n&s=10"

MEMBERS = {
    "丈君": {
        "nick": "丈君", 
        "trait": "搞笑又可靠的大哥哥", 
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRxeLPXR2kAxnf8Z0uNFWIH7j_vjPcrr8Eg1qWtaTSoPKTvTMcZtXXX6Kn&s=10", 
        "color": "💙 蓝色"
    },
    "大酱": {
        "nick": "大酱", 
        "trait": "热情太阳般的 C 位", 
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEiQYHWo7za_O6O-FerVkj5mA2s49UBL3hj_Tfmu-npd2yfIz1OJSCHD8n&s=10", 
        "color": "🔴 红色"
    },
    "布丁": {
        "nick": "布丁", 
        "trait": "温柔体贴又吃得超香的队长", 
        "img": "https://img-mdpr.freetls.fastly.net/article/H0CW/nm/H0CW_-CrOagXoRlSyQPOD6_zSqLjGNjyrfLRLWlqECw.jpg?width=750&disable=upscale&auto=webp&quality=80", 
        "color": "💚 绿色"
    },
    "高恭": {
        "nick": "高恭", 
        "trait": "自恋又亚撒西的八嘎帅哥，实则运动超强", 
        "img": "https://img-mdpr.freetls.fastly.net/article/d4sb/nm/d4sbe7H-P8R6sUQpAshcntVT8-h0ZPcuMe3icV8aOm4.jpg?width=750&disable=upscale&auto=webp&quality=80", 
        "color": "💜 紫色"
    },
    "流星": {
        "nick": "流星", 
        "trait": "眼睛会闪光的小恶魔", 
        "img": "https://oggi.jp/wp-content/uploads/2023/03/DMA-DSC00151_2-2.jpg", 
        "color": "🧡 橙色"
    },
    "米七": {
        "nick": "米七", 
        "trait": "高挑帅气的长腿王子", 
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvYWZ1rSHkldisNtmwbvxSYNjR8FWjj4_wdyKxw84_h0SabJN81yYpsGXL&s=10", 
        "color": "💖 粉色"
    },
    "谦杜": {
        "nick": "谦杜", 
        "trait": "时尚又有主见的小恶魔末子", 
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRs8ILDomyP9A6WZPtgig1e6IyPPmSpxS8HSYiRImU0uSqXicpvyNrHV8A&s=10", 
        "color": "💛 黄色"
    },
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
if "score" not in st.session_state:
    st.session_state.score = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "fortune_result" not in st.session_state:
    st.session_state.fortune_result = None

# -----------------------------------------------------------------------------
# 4. 动态多分支剧情数据生成（场景图自动使用背景图网址）
# -----------------------------------------------------------------------------
def get_act_data(role, target, act):
    t = target
    if role == "经纪人":
        if act == 1:
            return {
                "title": "🎬 第一幕：后台迎面的压力",
                "desc": f"离上台还有 10 分钟，{t} 一个人站在休息室门口发呆，看起来有些紧张。",
                "img": BG_IMAGE_URL,
                "bgm": "audio/act1_bgm.mp3",
                "choices": [
                    {"label": f"🅰️ 递上热茶温柔鼓励：『别担心，{t} 排练很完美，相信自己！』", "dialogue": f"『听到你这么说，我心里一下子踏实了！等会儿看我表现吧！』", "score": 20},
                    {"label": f"🅱️ 敲敲表格提醒：『{t}，还有 10 分钟，记得检查麦克风。』", "dialogue": f"『好的，我知道了，这就去准备。』", "score": 10},
                    {"label": f"🆎 严厉督促：『怎么还在发呆？大家都在等你呢！』", "dialogue": f"『……抱歉，我只是有点头晕，马上来。』（眼神有些黯淡）", "score": -10}
                ]
            }
        elif act == 2:
            return {
                "title": "🎬 第二幕：突发危机",
                "desc": f"中场换装时间仅剩 1 分钟，{t} 的服装拉链突然卡住了！",
                "img": BG_IMAGE_URL,
                "bgm": "audio/act2_bgm.mp3",
                "choices": [
                    {"label": f"🅰️ 眼神坚定迅速上手帮忙拉开，顺手擦掉他额头的汗：『有我在，别慌。』", "dialogue": f"『你靠得好近……心跳都要漏拍了，不过多亏有你！』", "score": 20},
                    {"label": f"🅱️ 叫旁边服装师：『老师快来帮 {t} 看看！』", "dialogue": f"『呼……险些赶不上，谢谢你叫人帮忙！』", "score": 10},
                    {"label": f"🆎 抱怨吐槽：『怎么关键时刻掉链子啊，快点！』", "dialogue": f"『对不起……我下次会注意的。』（显得有些沮丧）", "score": -10}
                ]
            }
        elif act == 3:
            return {
                "title": "🎬 第三幕：深夜保姆车",
                "desc": f"演出完美结束，在回程的车上，{t} 累得靠在座椅上昏昏欲睡。",
                "img": BG_IMAGE_URL,
                "bgm": "audio/act3_bgm.mp3",
                "choices": [
                    {"label": "🅰️ 调低空调，轻轻将他的头靠在自己肩膀上。", "dialogue": f"『（微笑着没睁眼）你的肩膀好暖和……别动，让我靠一会儿。』", "score": 20},
                    {"label": "🅱️ 拿出一瓶水放在他手边：『累坏了吧，喝点水。』", "dialogue": f"『嗯，今天辛苦你陪我跑一整天了。』", "score": 10},
                    {"label": "🆎 拿出行程表敲醒他：『别睡啦，明早还有通告！』", "dialogue": f"『……好吧，让我再叹一口气。』（疲惫地揉揉眼）", "score": -10}
                ]
            }

    elif role == "粉丝/地下恋":
        if act == 1:
            return {
                "title": "🎬 第一幕：后台通道的秘密碰面",
                "desc": f"在无人注意的后台角落，你和 {t} 只有短短 1 分钟的碰面时间。",
                "img": BG_IMAGE_URL,
                "bgm": "audio/act1_bgm.mp3",
                "choices": [
                    {"label": "🅰️ 悄悄递上手写信和小零食，拉拉他的手。", "dialogue": f"『只有你还记得我最爱吃这个！真想不管不顾抱抱你……』", "score": 20},
                    {"label": "🅱️ 保持距离比心：『今天台上超级帅哦！』", "dialogue": f"『嘿嘿，能得到你的夸奖，比拿大奖还开心！』", "score": 10},
                    {"label": "🆎 慌张后退：『被人看到就完蛋了，我先走了！』", "dialogue": f"『诶……就这么不想跟我多待一秒吗？』（有些失落）", "score": -10}
                ]
            }
        elif act == 2:
            return {
                "title": "🎬 第二幕：台下观众席的暗号",
                "desc": f"演唱会高潮，{t} 巡场时眼神扫过了你所在的区域。",
                "img": BG_IMAGE_URL,
                "bgm": "audio/act2_bgm.mp3",
                "choices": [
                    {"label": "🅰️ 举起只有你俩懂的专属手幅，甜甜一笑。", "dialogue": f"在台上精准捕捉到了你的眼神，对着你的方向做了一个专属于你的飞吻！", "score": 20},
                    {"label": "🅱️ 跟着大家一起挥舞应援棒欢呼。", "dialogue": f"{t} 向你所在的方向大力挥了挥手，笑容灿烂。", "score": 10},
                    {"label": "🆎 害怕被发现，连忙低头遮住脸。", "dialogue": f"{t} 在台上的眼神一愣，失落地移开了视线……", "score": -10}
                ]
            }
        elif act == 3:
            return {
                "title": "🎬 第三幕：深夜公寓约会",
                "desc": f"{t} 风尘仆仆赶到你的住处，解下口罩深深叹了口气。",
                "img": BG_IMAGE_URL,
                "bgm": "audio/act3_bgm.mp3",
                "choices": [
                    {"label": "🅰️ 主动上前抱住他的腰：『今天辛苦啦。』", "dialogue": f"『在你面前，我只想做那个深深爱着你的普通男人。』", "score": 20},
                    {"label": "🅱️ 递上一杯温牛奶：『快进来，外面冷。』", "dialogue": f"『只要能回到有你的房间，再累都烟消云散了。』", "score": 10},
                    {"label": "🆎 警惕地张望：『后面没记者狗仔跟着吧？』", "dialogue": f"『放心吧……我们之间除了防备狗仔，就没有别的话想说了吗？』", "score": -10}
                ]
            }

    elif role == "青梅竹马":
        if act == 1:
            return {
                "title": "🎬 第一幕：家常便当盒",
                "desc": f"你带了便当去看 {t}，他正坐在休息室擦汗。",
                "img": BG_IMAGE_URL,
                "bgm": "audio/act1_bgm.mp3",
                "choices": [
                    {"label": "🅰️ 递上便当帮他整理乱发：『还记得你最爱吃这个。』", "dialogue": f"『一点都没变！从小到大，还是你最懂我的口味！』", "score": 20},
                    {"label": "🅱️ 放在桌上：『阿姨让我带给你的，快吃吧。』", "dialogue": f"『太好了！正好肚子饿得咕咕叫呢！』", "score": 10},
                    {"label": "🆎 拿旧照调侃：『你小时候流鼻涕的照片我可还留着呢！』", "dialogue": f"『快收起来！万一被团员看到，我形象就全毁啦！』", "score": -10}
                ]
            }
        elif act == 2:
            return {
                "title": "🎬 第二幕：童年回忆",
                "desc": f"两人并排坐在沙发上，聊起了小时候在公园打闹的日子。",
                "img": BG_IMAGE_URL,
                "bgm": "audio/act2_bgm.mp3",
                "choices": [
                    {"label": "🅰️ 感慨：『没想到当年那个小不点，现在真成了大明星。』", "dialogue": f"『无论我走多远，在你面前我永远是那个少年。』", "score": 20},
                    {"label": "🅱️ 分享零食：『诺，小时候我们俩总抢这个吃。』", "dialogue": f"『这次我不跟你抢了，全都留给你吃！』", "score": 10},
                    {"label": "🆎 催促：『你现在是大忙人了，我就不打扰你了。』", "dialogue": f"『别走啊……在你心里我现在就只剩下“大忙人”了吗？』", "score": -10}
                ]
            }
        elif act == 3:
            return {
                "title": "🎬 第三幕：晚风漫步",
                "desc": "深夜工作结束，两人走在回家熟悉的小路上。",
                "img": BG_IMAGE_URL,
                "bgm": "audio/act3_bgm.mp3",
                "choices": [
                    {"label": "🅰️ 侧头看他：『这条路我们从小走到大呢。』", "dialogue": f"『唯一不同的是，现在的我……想牵着你的手继续走下去。』", "score": 20},
                    {"label": "🅱️ 买热烤红薯：『分你一半！』", "dialogue": f"『好香！还是跟你在一起时吃东西最开心！』", "score": 10},
                    {"label": "🆎 往前小跑：『快点走啦，明天还要早起！』", "dialogue": f"『等等我啊……你就不能慢下来陪我多走一会儿吗？』", "score": -10}
                ]
            }

    else:
        if act == 1:
            return {
                "title": "🎬 第一幕：后台兼职偶遇",
                "desc": f"你在后台当兼职翻译，正好碰到 {t} 在练习中文台词。",
                "img": BG_IMAGE_URL,
                "bgm": "audio/act1_bgm.mp3",
                "choices": [
                    {"label": "🅰️ 耐心纠正发音：『发音很棒，加油哦！』", "dialogue": f"『真的吗？为了你，我一定会好好练习中文的！』", "score": 20},
                    {"label": "🅱️ 递上资料：『这是今天的台词对照表。』", "dialogue": f"『太清晰了！有你在后台沟通顺畅多了，谢谢你！』", "score": 10},
                    {"label": "🆎 拘谨低头：『那个……请问有什么需要我做的吗？』", "dialogue": f"『不用这么拘谨啦，把我当成普通朋友就好了嘛。』", "score": -10}
                ]
            }
        elif act == 2:
            return {
                "title": "🎬 第二幕：异国文化交流",
                "desc": f"休息时间，{t} 好奇地问起你在日本的打工生活。",
                "img": BG_IMAGE_URL,
                "bgm": "audio/act2_bgm.mp3",
                "choices": [
                    {"label": "🅰️ 分享家乡零食，聊起异国趣事。", "dialogue": f"『真好吃！以后有机会，你一定要当我的导游带 me 去你的家乡！』", "score": 20},
                    {"label": "🅱️ 聊起打工：『虽然有点累，但很充实。』", "dialogue": f"『一个人在异国打拼真不简单，有困难随时找我！』", "score": 10},
                    {"label": "🆎 倒苦水：『语言不通，真想回国了。』", "dialogue": f"『别气馁啊……如果你走了，我会非常舍不得你的。』", "score": -10}
                ]
            }
        elif act == 3:
            return {
                "title": "🎬 第三幕：电车站台",
                "desc": "深夜打工结束，你们在微凉的电车站台并排等车。",
                "img": BG_IMAGE_URL,
                "bgm": "audio/act3_bgm.mp3",
                "choices": [
                    {"label": "🅰️ 买两罐热可可，碰到了彼此的手指。", "dialogue": f"『握着热可可……感觉整个冬天都不冷了，手贴在一起更暖和。』", "score": 20},
                    {"label": "🅱️ 看着电车：『今天工作很充实，电车来啦。』", "dialogue": f"『真希望这趟电车永远不要来，能多陪你一会儿。』", "score": 10},
                    {"label": "🆎 戴上耳机不说话。", "dialogue": f"『（小声嘀咕）……是我太无聊了吗，你怎么不理我了。』", "score": -10}
                ]
            }

# -----------------------------------------------------------------------------
# 5. 界面绘制
# -----------------------------------------------------------------------------
st.title("💖 浪花男子心动日常")

if st.session_state.page == "home":
    safe_audio("audio/bgm_home.mp3")
    
    st.header("🎲 每日运势抽卡")
    
    if st.button("✨ 测测今天最心动的成员", use_container_width=True):
        st.session_state.fortune_result = random.choice(list(MEMBERS.keys()))
        
    if st.session_state.fortune_result:
        m = st.session_state.fortune_result
        st.success(f"🎉 恭喜你抽中了今天最心动的成员：**{m}** ！")
        safe_image(MEMBERS[m]["img"], caption=f"✨ {m}")
        
        if st.button("🔄 返回首页"):
            st.session_state.fortune_result = None
            st.rerun()

    st.write("---")
    st.header("📖 开启心动互动剧情")
    
    st.subheader("1️⃣ 请选择你的身份：")
    role_choice = st.selectbox("身份列表", ROLES)
    
    st.subheader("2️⃣ 请选择你想攻略的成员：")
    target_choice = st.selectbox("成员列表", list(MEMBERS.keys()))
    
    m_info = MEMBERS[target_choice]
    st.caption(f"✨ 成员特征：{m_info['trait']} | 专属颜色：{m_info['color']}")
    
    if st.button("🌟 进入多分支剧情 🌟", use_container_width=True):
        st.session_state.role = role_choice
        st.session_state.target = target_choice
        st.session_state.act = 1
        st.session_state.score = 0
        st.session_state.history = []
        st.session_state.page = "story"
        st.rerun()

elif st.session_state.page == "story" and st.session_state.act <= 3:
    act = st.session_state.act
    role = st.session_state.role
    target = st.session_state.target
    
    act_data = get_act_data(role, target, act)
    
    safe_audio(act_data.get("bgm"))
    
    st.sidebar.metric("当前攻略", target)
    st.sidebar.metric("当前心动指数", st.session_state.score)
    
    st.subheader(f"【{role} 线】{act_data['title']}")
    
    safe_image(act_data.get("img"), caption=act_data["title"])
    
    st.info(act_data["desc"])
    
    if st.session_state.history:
        last = st.session_state.history[-1]
        st.success(f"💬 {target} 的回应：\n\n{last['dialogue']}")
        st.write("---")
        
    st.write("👉 **请做出你的回应选择：**")
    for idx, choice in enumerate(act_data["choices"]):
        if st.button(choice["label"], key=f"act_{act}_btn_{idx}", use_container_width=True):
            st.session_state.score += choice["score"]
            st.session_state.history.append({"choice": choice["label"], "dialogue": choice["dialogue"]})
            st.session_state.act += 1
            st.rerun()

else:
    target = st.session_state.target
    score = st.session_state.score
    role = st.session_state.role
    m_info = MEMBERS[target]
    
    st.header("🏆 最终心动结局结算")
    safe_image(m_info["img"], caption=f"✨ {target} ({m_info['trait']})")
    st.write(f"在【{role}】的故事中，你与 **{target}** 的最终心动指数为：**{score} 分**（满分 60 分）。")
    st.write("---")
    
    if score >= 45:
        st.balloons()
        st.subheader("💖 【HE 甜蜜告白结局】")
        st.success(f"『好不容易在人群中找到了你……这次我再也不想松开你的手了！无论别人怎么看，你才是我最重要的选择！』\n\n—— **{target}** 在灯光暗下的角落里，紧紧牵住了你的手，开启了只属于你们的甜蜜恋情。")
    elif score >= 20:
        st.subheader("🤝 【TE 默契搭档结局】")
        st.info(f"『今天真的多亏有你在……每次看到你，我都觉得心里很踏实。以后也请一直在身边支持我，好吗？』\n\n—— 你与 **{target}** 建立了极其深厚的信任与默契，成为了彼此生命中最不可或缺的灵魂陪伴。")
    else:
        st.subheader("💔 【BE 遗憾错失结局】")
        st.error(f"『今天辛苦你了……我待会儿还有通告，就先走一步了。』\n\n—— **{target}** 对你客套地微笑了笑，便转身跟随人群离开。两人的距离似乎在不知不觉中渐行渐远……")
        
    st.write("---")
    if st.button("🔄 返回首页 / 重新体验", use_container_width=True):
        st.session_state.page = "home"
        st.session_state.role = None
        st.session_state.target = None
        st.session_state.act = 1
        st.session_state.score = 0
        st.session_state.history = []
        st.rerun()
