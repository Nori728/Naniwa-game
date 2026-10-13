import random
import time
import streamlit as st

# 1. 页面基础配置
st.set_page_config(
    page_title="偶像培养计划：星途甄选",
    page_icon="🌟",
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

# 3. 极简高颜值 UI 设计（全萌系粉紫渐变）
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #fce4ec 0%, #f3e5f5 100%);
    }
    .top-dashboard {
        background: #ffffff;
        padding: 12px 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 2px solid #ff80ab;
        font-weight: bold;
        color: #4a148c;
        text-align: center;
    }
    .event-card {
        background: #2d1b4e;
        color: #ffffff;
        padding: 24px;
        border-radius: 18px;
        border: 3px solid #ff80ab;
        box-shadow: 0px 10px 25px rgba(255, 128, 171, 0.3);
        margin: 20px 0;
        font-size: 16px;
        line-height: 1.7;
    }
    .event-title {
        font-size: 20px;
        font-weight: 800;
        color: #ff80ab;
        margin-bottom: 12px;
    }
    .cute-info {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 18px;
        border: 2px dashed #ff4081;
        color: #4a148c;
        font-weight: 600;
        margin-bottom: 15px;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label {
        background-color: #ffffff;
        padding: 12px 18px;
        border-radius: 15px;
        margin-bottom: 8px;
        border: 2px solid #ea80fc;
        transition: all 0.2s ease;
        color: #4a148c;
        font-weight: 600;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background-color: #f3e5f5;
        border-color: #ff4081;
    }
    .stButton > button {
        background: linear-gradient(45deg, #ff4081, #ab47bc) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 12px 30px !important;
        box-shadow: 0 6px 15px rgba(255, 64, 129, 0.4) !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# 4. 初始化游戏数据
def init_game():
  st.session_state.game_started = False
  st.session_state.stage = 1
  st.session_state.group = ""
  st.session_state.member = ""
  st.session_state.lucky_item = ""

  # 隐藏的内部数值
  st.session_state.dance = random.randint(15, 25)
  st.session_state.vocal = random.randint(15, 25)
  st.session_state.variety = random.randint(15, 25)
  st.session_state.fans = 100
  st.session_state.trust = 40
  st.session_state.logs = []


if "game_started" not in st.session_state:
  init_game()


# 隐藏属性更新函数
def update_hidden_stats(dance=0, vocal=0, variety=0, fans=0, trust=0, log_msg=""):
  # 如果抽到了对应的幸运物，给予额外加成
  if st.session_state.lucky_item == "🍀 前辈送的开光御守":
    trust += 3
  elif st.session_state.lucky_item == "👟 加厚防滑特制舞鞋":
    dance += 3
  elif st.session_state.lucky_item == "🍲 深夜暖心关东煮":
    variety += 3

  st.session_state.dance += dance
  st.session_state.vocal += vocal
  st.session_state.variety += variety
  st.session_state.fans += fans
  st.session_state.trust += trust

  # 内部限制范围
  st.session_state.trust = max(0, min(100, st.session_state.trust))
  st.session_state.fans = max(0, st.session_state.fans)
  st.session_state.dance = max(0, st.session_state.dance)
  st.session_state.vocal = max(0, st.session_state.vocal)
  st.session_state.variety = max(0, st.session_state.variety)

  if log_msg:
    st.session_state.logs.append(log_msg)


# 主标题
st.title("💖 偶像培养计划：星途甄选 4.0")

# 游戏开始后，顶部只显示身份和幸运物，绝不显示分数！
if st.session_state.game_started:
  st.markdown(
      f'<div class="top-dashboard">👑 当前研修生：<b>{st.session_state.member}</b>（所属：{st.session_state.group}） | 🎒 随身幸运物：{st.session_state.lucky_item}</div>',
      unsafe_allow_html=True,
  )

# -------------------------------------------------------------------
# STAGE 0: 选角与开局幸运物盲盒抽取
# -------------------------------------------------------------------
if not st.session_state.game_started:
  st.markdown(
      '<div class="cute-info">✨ 欢迎来到 STARTO 偶像养成营！在踏入练习室之前，请先抽取属于你的开局【幸运物盲盒】，并选择你的出道身份。</div>',
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
  st.subheader("🎁 抽取你的入所幸运物盲盒")

  if "temp_lucky" not in st.session_state:
    st.session_state.temp_lucky = ""

  if st.button("🎲 点击盲盒抽签"):
    lucky_pool = [
        "🍀 前辈送的开光御守",
        "👟 加厚防滑特制舞鞋",
        "🍲 深夜暖心关东煮",
        "📖 记满心得的旧笔记本",
    ]
    st.session_state.temp_lucky = random.choice(lucky_pool)

  if st.session_state.temp_lucky:
    st.success(f"✨ 你抽中了：**{st.session_state.temp_lucky}**！它将在暗中庇佑你的星途。")
  else:
    st.info("请点击上方按钮抽取属于你的开局幸运物。")

  st.markdown("---")
  if st.button("🚀 带着祝福，正式开启练习生生涯！", use_container_width=True):
    if not st.session_state.temp_lucky:
      st.session_state.temp_lucky = "📖 记满心得的旧笔记本"
    st.session_state.group = selected_group
    st.session_state.member = selected_member
    st.session_state.lucky_item = st.session_state.temp_lucky
    st.session_state.game_started = True
    st.rerun()

# -------------------------------------------------------------------
# STAGE 1: 日常练习室 — 挥汗如雨的基础课
# -------------------------------------------------------------------
elif st.session_state.game_started and st.session_state.stage == 1:
  st.subheader("🎵 Stage 1：练习室的汗水与抉择")

  st.markdown("""
    <div class="event-card">
        <div class="event-title">📌 【日常：基础体能与舞蹈课】</div>
        窗外的东京正下着小雨。练习室里镜子前满是雾气，今天的舞蹈老师对动作要求极其严苛，训练结束后大家都累得瘫坐在地板上。
    </div>
    """, unsafe_allow_html=True)

  choice = st.radio(
      "看着镜子里的自己，你决定：",
      [
          "1. 留下来独自对着镜子把刚才卡壳的动作反复练习到深夜。",
          "2. 笑着把毛巾分给旁边气喘吁吁的同期伙伴，大家一起结伴去买冰麦茶。",
          "3. 觉得差不多就行了，保存体力，回宿舍连线打游戏放松一下。",
      ],
      key="s1",
  )

  if st.button("进入下一阶段 ➔"):
    if "1." in choice:
      update_hidden_stats(
          dance=15,
          trust=5,
          log_msg="【Stage 1】深夜独自加练的背影被舞蹈老师默默记在了心里。",
      )
    elif "2." in choice:
      update_hidden_stats(
          variety=12,
          fans=300,
          trust=10,
          log_msg="【Stage 1】温柔体贴的性格让伙伴们倍感温暖，结下了深厚友谊。",
      )
    else:
      update_hidden_stats(
          variety=5,
          fans=100,
          log_msg="【Stage 1】得到了充分的休息，保持了轻松愉快的心态。",
      )

    st.session_state.stage = 2
    st.rerun()

# -------------------------------------------------------------------
# STAGE 2: 前辈休息室 — 礼仪与前辈相处
# -------------------------------------------------------------------
elif st.session_state.game_started and st.session_state.stage == 2:
  st.subheader("☕ Stage 2：前辈休息室的下午茶")

  st.markdown("""
    <div class="event-card">
        <div class="event-title">📌 【日常：向前辈请教】</div>
        事务所的前辈组合今天在隔壁录音，你带着伴手礼去前辈休息室敲门问候。前辈正坐着休息，顺口问了你一句最近的练习情况。
    </div>
    """, unsafe_allow_html=True)

  choice = st.radio(
      "面对前辈的关心，你打算如何回答？",
      [
          "1. 恭恭敬敬地请教对方关于舞台上如何控制表情和眼神的技巧。",
          "2. 顺势讲了个幽默的小段子，把休息室的所有人都逗得哈哈大笑。",
          "3. 有点拘谨地鞠躬道谢，简单回答“一切都好，正在努力”。",
      ],
      key="s2",
  )

  if st.button("进入下一阶段 ➔"):
    if "1." in choice:
      update_hidden_stats(
          vocal=12,
          trust=12,
          log_msg="【Stage 2】前辈对你的虚心好学赞赏有加，传授了许多宝贵的舞台经验。",
      )
    elif "2." in choice:
      update_hidden_stats(
          variety=18,
          trust=8,
          log_msg="【Stage 2】幽默感给前辈留下了深刻印象，夸奖你很有综艺潜力。",
      )
    else:
      update_hidden_stats(
          trust=5, log_msg="【Stage 2】虽然有些拘谨，但礼仪周到，表现合格。"
      )

    st.session_state.stage = 3
    st.rerun()

# -------------------------------------------------------------------
# STAGE 3: 杂志采访日常 — 表达与个性
# -------------------------------------------------------------------
elif st.session_state.game_started and st.session_state.stage == 3:
  st.subheader("📖 Stage 3：《Myojo》杂志小长篇采访")

  st.markdown("""
    <div class="event-card">
        <div class="event-title">📌 【日常：私下兴趣与性格访谈】</div>
        杂志社来给 Jr. 做日常专访。摄影师让你摆出一个最能代表你当下心情的姿势，并问你最近私底下最大的爱好是什么。
    </div>
    """, unsafe_allow_html=True)

  choice = st.radio(
      "你的回答是：",
      [
          "1. “最近一直在研究编曲和吉他，希望能早日写出属于自己的歌。”",
          "2. “喜欢收集各种奇怪的复古玩具，房间里到处都是。”",
          "3. “每天最大的爱好就是和成员们一起去吃烤肉，聊到深夜。”",
      ],
      key="s3",
  )

  if st.button("进入下一阶段 ➔"):
    if "1." in choice:
      update_hidden_stats(
          vocal=15,
          fans=600,
          log_msg="【Stage 3】才华横溢的音乐爱好吸引了大批注重实力的粉丝。",
      )
    elif "2." in choice:
      update_hidden_stats(
          variety=15,
          fans=500,
          log_msg="【Stage 3】独特的搞怪收藏癖让读者觉得你十分有趣、充满反差萌。",
      )
    else:
      update_hidden_stats(
          variety=10,
          fans=400,
          log_msg="【Stage 3】真诚的团队羁绊发言让粉丝直呼太好嗑了。",
      )

    st.session_state.stage = 4
    st.rerun()

# -------------------------------------------------------------------
# STAGE 4: 团体内部的温馨时刻
# -------------------------------------------------------------------
elif st.session_state.game_started and st.session_state.stage == 4:
  st.subheader("🍖 Stage 4：深夜的烤肉店聚会")

  st.markdown("""
    <div class="event-card">
        <div class="event-title">📌 【日常：伙伴间的倾诉与交心】</div>
        结束了一整天的密集排练，大家聚在一家街角的小烤肉店。滋滋作响的烤肉香气中，大家开始畅谈各自对未来的迷茫与憧憬。
    </div>
    """, unsafe_allow_html=True)

  choice = st.radio(
      "大家举杯时，你对伙伴们说：",
      [
          "1. “不管未来有多难，我们一定要一起以这个组合的身份站上巨蛋！”",
          "2. 默默烤好了一整盘肉，分给身边的每一个人，“快吃吧，辛苦啦。”",
          "3. “如果以后我红了，绝对不会忘记大家当年分着吃一份炒面的情谊！”",
      ],
      key="s4",
  )

  if st.button("进入下一阶段 ➔"):
    if "1." in choice:
      update_hidden_stats(
          trust=15,
          fans=800,
          log_msg="【Stage 4】充满热血与羁绊的发言让全员凝聚力达到了顶峰。",
      )
    elif "2." in choice:
      update_hidden_stats(
          trust=20,
          variety=5,
          log_msg="【Stage 4】体贴入微的举动让队友们在私底下对你充满信赖。",
      )
    else:
      update_hidden_stats(
          variety=15,
          fans=400,
          log_msg="【Stage 4】幽默的调侃让沉重的气氛瞬间轻松了起来。",
      )

    st.session_state.stage = 5
    st.rerun()

# -------------------------------------------------------------------
# STAGE 5: 小型 Showcase 舞台呈现
# -------------------------------------------------------------------
elif st.session_state.game_started and st.session_state.stage == 5:
  st.subheader("🎤 Stage 5：事务所内部 Showcase 表演")

  st.markdown("""
    <div class="event-card">
        <div class="event-title">📌 【考核：小型成果汇报舞台】</div>
        这是在事务所内部剧场举办的小型 Showcase，台下坐着各部门的制作人和高层。灯光亮起，轮到你进行个人 Solo 展示了。
    </div>
    """, unsafe_allow_html=True)

  choice = st.radio(
      "在聚光灯下，你选择展现：",
      [
          "1. 节奏感拉满、卡点精准的高难度燃炸舞蹈 Solo。",
          "2. 安静深情、直击人心的清澈主唱 Solo。",
          "3. 带动全场观众一起互动拍手的欢快曲目。",
      ],
      key="s5",
  )

  if st.button("进入下一阶段 ➔"):
    if "1." in choice:
      update_hidden_stats(
          dance=20,
          fans=1000,
          log_msg="【Stage 5】利落的舞姿赢得了台下制作人的一致点头认可。",
      )
    elif "2." in choice:
      update_hidden_stats(
          vocal=20,
          fans=1000,
          log_msg="【Stage 5】清澈动人的歌声让后台安静了下来，余音绕梁。",
      )
    else:
      update_hidden_stats(
          variety=20,
          fans=1200,
          log_msg="【Stage 5】极具感染力的现场氛围把全场带成了一片欢乐的海洋。",
      )

    st.session_state.stage = 6
    st.rerun()

# -------------------------------------------------------------------
# STAGE 6: 帝国剧场最终大决选 (揭晓全部评分与结局)
# -------------------------------------------------------------------
elif st.session_state.game_started and st.session_state.stage == 6:
  st.subheader("🏆 Final Stage：帝国剧场 CD 出道大决选")

  st.markdown("""
    <div class="event-card">
        <div class="event-title">✨ 【命运的终章】</div>
        帝国剧场金碧辉煌的大厅内聚集了上百家媒体。社长站在话筒前，即将宣读今年正式获得 CD 出道资格的最终名单。<br><br>
        这段时间的练习、日常与欢笑在脑海中闪过，揭晓答案的时刻到了！
    </div>
    """, unsafe_allow_html=True)

  if st.button("🌟 揭晓最终出道结果与个人档案 🌟", use_container_width=True):
    st.markdown("---")

    total_ability = (
        st.session_state.dance
        + st.session_state.vocal
        + st.session_state.variety
    )
    trust = st.session_state.trust
    fans = st.session_state.fans

    # 结局判定逻辑
    if trust < 25:
      st.error("💀 【最终结局：遗憾离场 / 另谋出路】")
      st.write(
          f"很遗憾，{st.session_state.member}。"
          f"由于在各项考察中未能建立足够的信任，你与组合在出道前夕擦肩而过，选择走向了不同的道路。"
      )
    elif fans >= 4500 and total_ability >= 90 and trust >= 50:
      st.balloons()
      st.success("🎉 【最终结局：闪耀万丈 - CD 华丽出道！】")
      st.markdown(
          f"### 👑 恭喜 {st.session_state.group} 的 **{st.session_state.member}**！\n"
          f"携带幸运物【{st.session_state.lucky_item}】的你，在长期的汗水与伙伴的羁绊中脱颖而出！"
          "社长在发布会上亲手递出了出道 CD 的契约函，全场掌声雷动，你正式登上了主流娱乐圈的顶峰！"
      )
    else:
      st.warning("⚠️ 【最终结局：稳扎稳打 - 剧场与舞台核心骨干】")
      st.write(
          f"很可惜，{st.session_state.member}。"
          "虽然你拥有非常温暖的日常和不错的伙伴基础，但综合爆发力距离正式 CD 出道还有一小步。"
          "社长决定让你继续作为组合的中坚力量深耕舞台，未来可期！"
      )

    # 完整档案大公开
    st.markdown("---")
    st.markdown("### 📊 你的星途终极能力档案")
    st.write(
        f"- 💃 舞蹈实力：**{st.session_state.dance} pt** | 🎤 歌唱实力：**{st.session_state.vocal} pt** | 🤡 综艺表现：**{st.session_state.variety} pt**"
    )
    st.write(f"- 🤝 社长信任度：**{trust} / 100**")
    st.write(f"- 💖 累积粉丝总数：**{fans:,} 人**")
    st.write(f"- 🎒 开局幸运物：**{st.session_state.lucky_item}**")

    st.markdown("#### 📖 你的青春历程手记：")
    for log in st.session_state.logs:
      st.caption(f"• {log}")

    st.write("")
    if st.button("🎮 开启新的偶像人生"):
      init_game()
      st.rerun()
