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
        box-shadow: 0 8px 20px rgba(255, 64, 129, 0.6) !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# 4. 初始化游戏数据（增加防死机保护）
def init_game():
  st.session_state.game_started = False
  st.session_state.stage = 1
  st.session_state.group = ""
  st.session_state.member = ""
  st.session_state.avatar = None

  # 地狱开局低数值
  st.session_state.dance = random.randint(15, 25)
  st.session_state.vocal = random.randint(15, 25)
  st.session_state.variety = random.randint(15, 25)
  st.session_state.fans = 100
  st.session_state.trust = 40
  st.session_state.logs = []


# 极其严密的状态安全检查
if "avatar" not in st.session_state or "game_started" not in st.session_state:
  init_game()


# 属性更新隐蔽辅助函数
def update_stats(dance=0, vocal=0, variety=0, fans=0, trust=0, log_msg=""):
  st.session_state.dance += dance
  st.session_state.vocal += vocal
  st.session_state.variety += variety
  st.session_state.fans += fans
  st.session_state.trust += trust

  st.session_state.trust = max(0, min(100, st.session_state.trust))
  st.session_state.fans = max(0, st.session_state.fans)
  st.session_state.dance = max(0, st.session_state.dance)
  st.session_state.vocal = max(0, st.session_state.vocal)
  st.session_state.variety = max(0, st.session_state.variety)

  if log_msg:
    st.session_state.logs.append(log_msg)


# 主标题
st.title("💖 偶像培养计划：星途甄选 2.0")

# 侧边栏：状态面板与头像
if st.session_state.game_started:
  st.sidebar.markdown("### 👑 当前训练生")

  # 使用 safe get 语法，防止 KeyError
  avatar_file = st.session_state.get("avatar", None)
  if avatar_file is not None:
    st.sidebar.image(
        avatar_file,
        caption=f"{st.session_state.group} - {st.session_state.member}",
        use_container_width=True,
    )
  else:
    st.sidebar.markdown(
        f"**{st.session_state.group}**\n# 🌟 {st.session_state.member}"
    )

  st.sidebar.markdown("---")
  st.sidebar.markdown("### 📊 个人实力属性")

  c1, c2 = st.sidebar.columns(2)
  with c1:
    st.metric("💃 舞蹈", f"{st.session_state.dance} pt")
    st.metric("🤡 综艺感", f"{st.session_state.variety} pt")
  with c2:
    st.metric("🎤 歌唱", f"{st.session_state.vocal} pt")
    st.metric("🤝 社长信任", f"{st.session_state.trust} / 100")

  st.sidebar.metric("💖 粉丝数量", f"{st.session_state.fans:,} 人")

  st.sidebar.markdown("---")
  if st.sidebar.button("🔄 放弃并重新开始"):
    init_game()
    st.rerun()

# -------------------------------------------------------------------
# STAGE 0: 选角与准备
# -------------------------------------------------------------------
if not st.session_state.game_started:
  st.markdown(
      '<div class="cute-info">✨ 欢迎来到 STARTO 偶像训练营！请选择你的身份并开启地狱级的甄选之路吧！</div>',
      unsafe_allow_html=True,
  )

  col_a, col_b = st.columns(2)
  with col_a:
    selected_group = st.selectbox(
        "选择心仪的偶像组合：", list(IDOL_GROUPS.keys())
    )
  with col_b:
    selected_member = st.selectbox(
        "选择你要扮演的成员：", IDOL_GROUPS[selected_group]
    )

  st.markdown("---")
  st.markdown("#### 📷 自定义你的偶像头像（可选）")
  uploaded_file = st.file_uploader(
      "支持上传 JPG / PNG 格式照片，让体验更具代入感！", type=["jpg", "png", "jpeg"]
  )

  if st.button("🚀 签订研修契约，开启星途！", use_container_width=True):
    st.session_state.group = selected_group
    st.session_state.member = selected_member
    st.session_state.avatar = uploaded_file
    st.session_state.game_started = True
    st.rerun()

# -------------------------------------------------------------------
# STAGE 1: 入校试镜与自主练习
# -------------------------------------------------------------------
elif st.session_state.stage == 1:
  st.subheader("🚩 Stage 1：研修生入所试镜")

  st.markdown("""
    <div class="event-card">
        <div class="event-title">📌 【考核事件：分班考核试镜】</div>
        你刚刚作为 Jr. 进入练习室。社长坐在台下，要求每位新人即兴展示一段才艺。周遭都是实力强劲的练习生，你打算怎么展现自己？
    </div>
    """, unsafe_allow_html=True)

  choice = st.radio(
      "请做出你的决定：",
      [
          "1. 挑战超高难度的特技空翻展示极致舞蹈！",
          "2. 唱一首前辈的经典抒情歌曲，展示温柔的真假音转换。",
          "3. 展现独特的搞笑天赋，准备一段单口相声（Talk）！",
      ],
      key="s1",
  )

  if st.button("提交决定 ➔"):
    if "1." in choice:
      if random.random() < 0.65:
        update_stats(
            dance=18,
            fans=300,
            trust=10,
            log_msg="【Stage 1】完美完成空翻！社长惊叹连连，获得了高评分！",
        )
      else:
        update_stats(
            dance=5,
            trust=-10,
            log_msg="【Stage 1】空翻落地失误，让社长担心你的身体状况。",
        )
    elif "2." in choice:
      update_stats(
          vocal=15,
          trust=10,
          fans=200,
          log_msg="【Stage 1】沉稳的歌声打动了考官，被分入了歌唱组练习。",
      )
    else:
      update_stats(
          variety=20,
          fans=500,
          trust=5,
          log_msg="【Stage 1】全场被你逗得大笑，成为了练习室里的人气王！",
      )

    st.session_state.stage = 2
    st.rerun()

# -------------------------------------------------------------------
# STAGE 2: 前辈 Concert Back 伴舞危机
# -------------------------------------------------------------------
elif st.session_state.stage == 2:
  st.subheader("🚩 Stage 2：大型演唱会 - 前辈 Back 伴舞")

  st.markdown("""
    <div class="event-card">
        <div class="event-title">📌 【考核事件：搬梯子与走位危机】</div>
        你获得了为前辈巨蛋演唱会伴舞的珍贵机会！但在开场前 5 分钟，舞蹈总监临时变更了走位，并且舞台道具梯子突然无人搬运！
    </div>
    """, unsafe_allow_html=True)

  choice = st.radio(
      "你会怎么做？",
      [
          "1. 主动承担起搬运梯子的脏活累活，同时凭借记忆硬记新走位。",
          "2. 不管道具，专注死记硬背自己的舞蹈走位，确保自己绝对不出错。",
          "3. 趁着灯光昏暗，在后排做出超大动作吸引观众席视线！",
      ],
      key="s2",
  )

  if st.button("提交决定 ➔"):
    if "1." in choice:
      update_stats(
          dance=10,
          trust=20,
          fans=400,
          log_msg="【Stage 2】默默奉献的精神被前辈和社长看在眼里，信任度大增！",
      )
    elif "2." in choice:
      update_stats(
          dance=15,
          trust=5,
          log_msg="【Stage 2】虽然没有特别亮眼，但展现了扎实的舞蹈基本功。",
      )
    else:
      if random.random() < 0.4:
        update_stats(
            fans=2500,
            trust=-15,
            log_msg="【Stage 2】抢镜成功！引起了热议，但社长认为你不守规矩。",
        )
      else:
        update_stats(
            fans=-500,
            trust=-20,
            log_msg="【Stage 2】抢镜导致整体失调，被舞蹈总监严厉批评！",
        )

    st.session_state.stage = 3
    st.rerun()

# -------------------------------------------------------------------
# STAGE 3：电视直播舞台故障
# -------------------------------------------------------------------
elif st.session_state.stage == 3:
  st.subheader("🚩 Stage 3：电视直播 LIVE 舞台危机")

  st.markdown("""
    <div class="event-card">
        <div class="event-title">📌 【突发事件：麦克风掉落 & 断音】</div>
        你在录制独唱特写段落时，手里的麦克风突然滑落掉在了地上！现场观众和镜头都在注视着你！
    </div>
    """, unsafe_allow_html=True)

  choice = st.radio(
      "电光火石之间，你的反应是：",
      [
          "1. 顺势将捡麦克风做成一个超帅气的舞蹈动作，并顺畅接上清唱！",
          "2. 保持镇定，对镜头抛个媚眼，微笑着用口型唱完后半段。",
          "3. 慌张地捡起麦克风，手忙脚乱地跟上伴奏节奏。",
      ],
      key="s3",
  )

  if st.button("提交决定 ➔"):
    if "1." in choice:
      if st.session_state.dance + st.session_state.vocal >= 50:
        update_stats(
            dance=15,
            vocal=15,
            fans=3500,
            trust=15,
            log_msg="【Stage 3】神级现场应变！这一幕成为了名场面！",
        )
      else:
        update_stats(
            fans=1000,
            trust=-5,
            log_msg="【Stage 3】有创意，但由于唱功不够导致声音发颤。",
        )
    elif "2." in choice:
      update_stats(
          variety=20,
          fans=2500,
          trust=10,
          log_msg="【Stage 3】强大的心理素质和爱豆魅力征服了全场！",
      )
    else:
      update_stats(
          fans=-800,
          trust=-10,
          log_msg="【Stage 3】表现过于慌乱，失去了难得的镜头展示机会。",
      )

    st.session_state.stage = 4
    st.rerun()

# -------------------------------------------------------------------
# STAGE 4：杂志访谈与综艺危机
# -------------------------------------------------------------------
elif st.session_state.stage == 4:
  st.subheader("🚩 Stage 4：偶像杂志专访 & 应对")

  st.markdown("""
    <div class="event-card">
        <div class="event-title">📌 【考核事件：犀利记者提问】</div>
        在专访中，记者抛出了刁钻问题：“你觉得你在组合里是不可替代的吗？其他人会不会拖你后腿？”
    </div>
    """, unsafe_allow_html=True)

  choice = st.radio(
      "你的回答策略：",
      [
          "1. 高情商回复：“我们每个人都是拼图的一块，缺了谁这幅画都不完整！”",
          "2. 霸气回复：“我会用实力成为队伍里绝对的核心（Center）！”",
          "3. 搞笑调侃：“他们确实常拖我后腿，比如经常抢我的便当吃！”",
      ],
      key="s4",
  )

  if st.button("提交决定 ➔"):
    if "1." in choice:
      update_stats(
          trust=20,
          fans=2000,
          log_msg="【Stage 4】展现了极佳的团魂，高层和粉丝非常满意！",
      )
    elif "2." in choice:
      update_stats(
          dance=10,
          vocal=10,
          fans=3000,
          trust=-10,
          log_msg="【Stage 4】野心满满吸了一波唯粉，但也引发了部分争议。",
      )
    else:
      update_stats(
          variety=25,
          fans=2500,
          trust=10,
          log_msg="【Stage 4】爆笑金句登上了热搜，综艺感大受好评！",
      )

    st.session_state.stage = 5
    st.rerun()

# -------------------------------------------------------------------
# STAGE 5：八卦绯闻风波
# -------------------------------------------------------------------
elif st.session_state.stage == 5:
  st.subheader("🚩 Stage 5：八卦周刊绯闻风波")

  st.markdown("""
    <div class="event-card">
        <div class="event-title">📌 【致命危机：周刊曝光照片】</div>
        八卦周刊拍到了你深夜与朋友在聚会的照片，并撰文暗示你有负面嫌疑！社交媒体瞬间炸锅！
    </div>
    """, unsafe_allow_html=True)

  choice = st.radio(
      "危机公关，你选择怎么做？",
      [
          "1. 连夜向社长诚恳说明原委，并主动配合事务所做出合理解释。",
          "2. 在官方博客上发长文自证清白，安抚粉丝。",
          "3. 选择沉默不作任何回应，冷处理等热度过去。",
      ],
      key="s5",
  )

  if st.button("提交决定 ➔"):
    if "1." in choice:
      update_stats(
          trust=25,
          fans=-500,
          log_msg="【Stage 5】你的坦诚赢得了事务所全力的公关保驾护航，危机解除！",
      )
    elif "2." in choice:
      if random.random() < 0.5:
        update_stats(
            fans=4000,
            trust=-15,
            log_msg="【Stage 5】粉丝被真诚打动，固粉成功！但社长对你的自作主张略有不满。",
        )
      else:
        update_stats(
            fans=-3000,
            trust=-25,
            log_msg="【Stage 5】风波未能平息，反而引发了更多的讨论与脱粉。",
        )
    else:
      update_stats(
          fans=-2000,
          trust=-20,
          log_msg="【Stage 5】冷处理导致脱粉严重，社长对你的态度感到失望。",
      )

    st.session_state.stage = 6
    st.rerun()

# -------------------------------------------------------------------
# STAGE 6: 最终大决选
# -------------------------------------------------------------------
elif st.session_state.stage == 6:
  st.subheader("🏁 Final Stage：出道最终大决选")

  st.markdown("""
    <div class="event-card">
        <div class="event-title">👑 【最后的考核】</div>
        舞台灯光璀璨。社长手里拿着今年最后一份 <b>“CD 出道推荐书”</b>。<br><br>
        这是你近几年来所有汗水、努力与选择的汇总时刻！
    </div>
    """, unsafe_allow_html=True)

  if st.button("🌟 揭晓出道甄选结果 🌟", use_container_width=True):
    st.markdown("---")

    total_ability = (
        st.session_state.dance
        + st.session_state.vocal
        + st.session_state.variety
    )
    trust = st.session_state.trust
    fans = st.session_state.fans

    if trust < 25:
      st.error("💀 【结局：退所 / 解除契约】")
      st.write(
          f"很遗憾，{st.session_state.member}。"
          f"由于社长信任度跌至谷底（{trust}），你未能在事务所立足，最终在出道前夕收到了退所通知。"
      )
    elif fans >= 8000 and total_ability >= 110 and trust >= 65:
      st.balloons()
      st.success("🎉 【结局：百万销量 - 传说级 CD 出道！】")
      st.markdown(
          f"### 👑 恭喜 {st.session_state.group} 的 **{st.session_state.member}**！\n"
          "你凭借无可挑剔的综合实力、极高的社长信任与庞大的粉丝基础，在舞台上正式接过了 CD 出道的金标签！"
          "你的出道单曲首周即破百万销量，成为了新一代顶流！"
      )
    elif fans >= 4500 and trust >= 45:
      st.success("✨ 【结局：顺利 CD 出道！】")
      st.markdown(
          f"### 👏 恭喜 {st.session_state.group} 的 **{st.session_state.member}**！\n"
          "经过多年的默默耕耘，社长终于为你和组合敲定了出道单曲！你正式摆脱了 Jr. 身份，步入主流明星行列！"
      )
    else:
      st.warning("⚠️ 【结局：万年 Jr. 骨干 / 舞台剧专项】")
      st.write(
          f"很可惜，{st.session_state.member}。"
          "虽然你非常努力，但目前的综合实力和粉丝基础尚未达到 CD 出道的门槛。"
          "社长决定让你继续在舞台深耕，等待下一次机会。"
      )

    st.markdown("---")
    st.markdown("### 📜 你的星途档案记录")
    st.write(
        f"- 最终实力总和：**{total_ability} pt**（舞:{st.session_state.dance} / 唱:{st.session_state.vocal} / 综:{st.session_state.variety}）"
    )
    st.write(f"- 最终社长信任：**{trust} / 100**")
    st.write(f"- 最终粉丝总数：**{fans:,} 人**")

    st.markdown("#### 📖 历程事件回顾：")
    for log in st.session_state.logs:
      st.caption(f"• {log}")

    st.write("")
    if st.button("🎮 开启新的偶像人生"):
      init_game()
      st.rerun()
