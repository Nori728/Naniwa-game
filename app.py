import random
import time
import streamlit as st

# 1. 页面基础配置
st.set_page_config(
    page_title="偶像培养计划：星途甄选",
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

# 3. 极简高颜值 UI 设计（无侧边栏，顶部面板）
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #fce4ec 0%, #f3e5f5 100%);
    }
    .top-dashboard {
        background: #ffffff;
        padding: 15px 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 2px solid #ff80ab;
    }
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
    }
    .cute-info {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 15px;
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
  st.session_state.avatar_url = ""
  st.session_state.dance = random.randint(15, 25)
  st.session_state.vocal = random.randint(15, 25)
  st.session_state.variety = random.randint(15, 25)
  st.session_state.fans = 100
  st.session_state.trust = 40
  st.session_state.inventory = []
  st.session_state.logs = []


# 绝对安全的键值检查与初始化（防止任何 KeyError）
if "game_started" not in st.session_state:
  init_game()
else:
  # 确保新增字段在老会话中不会报错
  if "inventory" not in st.session_state:
    st.session_state.inventory = []
  if "avatar_url" not in st.session_state:
    st.session_state.avatar_url = ""
  if "logs" not in st.session_state:
    st.session_state.logs = []


# 辅助属性更新函数
def update_stats(dance=0, vocal=0, variety=0, fans=0, trust=0, log_msg=""):
  multiplier = 1.5 if "金牌训练护符" in st.session_state.inventory else 1.0

  st.session_state.dance += int(dance * multiplier)
  st.session_state.vocal += int(vocal * multiplier)
  st.session_state.variety += int(variety * multiplier)
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
st.title("💖 偶像培养计划：星途甄选 3.0")

# 如果游戏已经开始，在顶部渲染状态仪表盘
if st.session_state.game_started:
  st.markdown('<div class="top-dashboard">', unsafe_allow_html=True)
  col_h1, col_h2, col_h3, col_h4, col_h5, col_h6 = st.columns(6)
  with col_h1:
    st.markdown(
        f"**👑 练习生**<br>{st.session_state.member} ({st.session_state.group})",
        unsafe_allow_html=True,
    )
  with col_h2:
    st.metric("💃 舞蹈", f"{st.session_state.dance} pt")
  with col_h3:
    st.metric("🎤 歌唱", f"{st.session_state.vocal} pt")
  with col_h4:
    st.metric("🤡 综艺感", f"{st.session_state.variety} pt")
  with col_h5:
    st.metric("💖 粉丝数", f"{st.session_state.fans:,}")
  with col_h6:
    st.metric("🤝 社长信任", f"{st.session_state.trust}/100")

  current_inv = st.session_state.get("inventory", [])
  if current_inv:
    st.info(f"🎒 **当前拥有道具背包**：{', '.join(current_inv)}")
  st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# STAGE 0: 选角与准备
# -------------------------------------------------------------------
if not st.session_state.game_started:
  st.markdown(
      '<div class="cute-info">✨ 欢迎来到 STARTO 偶像训练营！请选择你的组合与成员，输入你的专属宣传照网址（选填），开启养成之路！</div>',
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

  avatar_input = st.text_input(
      "📷 输入你的偶像宣传照图片网址 (URL，可选)：",
      placeholder="例如: https://example.com/idol.jpg",
  )

  if st.button("🚀 签订研修契约，开启星途！", use_container_width=True):
    st.session_state.group = selected_group
    st.session_state.member = selected_member
    st.session_state.avatar_url = avatar_input.strip()
    st.session_state.game_started = True
    st.rerun()


# -------------------------------------------------------------------
# 抽奖/道具盲盒小函数
# -------------------------------------------------------------------
def gacha_draw():
  items = [
      "🌟 《Myojo》限定单人封面（粉丝+1500）",
      "🛡️ 防文春护身符（抵消一次负面绯闻）",
      "🎤 录音棚黄金麦克风（歌唱属性暴增+15）",
      "👟 练习室减震舞鞋（舞蹈属性暴增+15）",
  ]
  reward = random.choice(items)
  st.session_state.inventory.append(reward)
  st.success(f"🎁 **恭喜你通过阶段考核，抽中事务所盲盒奖励**：【 {reward} 】！")


# -------------------------------------------------------------------
# STAGE 1: 入校试镜与自主练习
# -------------------------------------------------------------------
if st.session_state.game_started and st.session_state.stage == 1:
  st.subheader("🚩 Stage 1：研修生入所试镜")

  st.markdown("""
    <div class="event-card">
        <div class="event-title">📌 【突发考核：分班即兴考核】</div>
        你刚作为 Jr. 进入练习室。社长突然临时抽查，要求每位新人即兴展示一项绝活。周遭竞争极其惨烈，你决定展示：
    </div>
    """, unsafe_allow_html=True)

  choice = st.radio(
      "请做出你的决定：",
      [
          "1. 挑战超高难度的特技空翻，展现视觉冲击力！",
          "2. 清唱一首高难度的前辈金曲，展露歌喉。",
          "3. 讲一个冷笑话，展现出众的综艺谈话天赋。",
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
            log_msg="【Stage 1】空翻完美落地！社长对你的运动神经表示赞赏。",
        )
      else:
        update_stats(
            dance=5,
            trust=-10,
            log_msg="【Stage 1】空翻时险些摔倒，留下了一个惊险的失误回忆。",
        )
    elif "2." in choice:
      update_stats(
          vocal=15,
          trust=10,
          fans=200,
          log_msg="【Stage 1】温柔稳健的转音打动了台下的音响总监。",
      )
    else:
      update_stats(
          variety=20,
          fans=500,
          trust=5,
          log_msg="【Stage 1】冷笑话逗笑了全场，迅速在练习生中树立了开心果形象。",
      )

    gacha_draw()
    st.session_state.stage = 2
    st.rerun()

# -------------------------------------------------------------------
# STAGE 2: 前辈 Concert Back 伴舞突发事件
# -------------------------------------------------------------------
elif st.session_state.game_started and st.session_state.stage == 2:
  st.subheader("🚩 Stage 2：东京巨蛋 - 前辈演唱会后台")

  st.markdown("""
    <div class="event-card">
        <div class="event-title">📌 【突发状况：搬梯子与走位冲突】</div>
        巨蛋演唱会开场前 10 分钟，前辈的道具梯子因工作人员疏忽堆在通道。同时舞蹈总监临时调整了你们的后排走位！
    </div>
    """, unsafe_allow_html=True)

  choice = st.radio(
      "你该怎么应对？",
      [
          "1. 一个人默默把重型道具梯子搬走，并加急硬记新走位。",
          "2. 专心死磕自己的舞蹈走位，对杂务置之不理。",
          "3. 在后排跳舞时故意加上夸张的可爱动作，争取摄像机多扫一眼。",
      ],
      key="s2",
  )

  if st.button("提交决定 ➔"):
    if "1." in choice:
      update_stats(
          dance=10,
          trust=20,
          fans=400,
          log_msg="【Stage 2】任劳任怨的奉献精神被前辈看在眼里，信任度暴增！",
      )
    elif "2." in choice:
      update_stats(
          dance=15,
          trust=5,
          log_msg="【Stage 2】虽然毫无差错，但也显得中规中矩。",
      )
    else:
      if random.random() < 0.4:
        update_stats(
            fans=2500,
            trust=-15,
            log_msg="【Stage 2】加戏成功！在推特上引起了热议，吸了一波颜粉。",
        )
      else:
        update_stats(
            fans=-500,
            trust=-20,
            log_msg="【Stage 2】因私自抢镜头导致舞蹈队形混乱，遭到严厉训斥！",
        )

    gacha_draw()
    st.session_state.stage = 3
    st.rerun()

# -------------------------------------------------------------------
# STAGE 3：电视直播突发事故
# -------------------------------------------------------------------
elif st.session_state.game_started and st.session_state.stage == 3:
  st.subheader("🚩 Stage 3：音乐打歌节目直播事故")

  st.markdown("""
    <div class="event-card">
        <div class="event-title">📌 【突发危机：耳返没声音 & 走音】</div>
        在黄金档音乐直播节目中，你的耳返突然毫无预兆地断电了，伴奏声听不真切，随时面临大走音的风险！
    </div>
    """, unsafe_allow_html=True)

  choice = st.radio(
      "电光火石之间，你选择：",
      [
          "1. 凭着肌肉记忆和对全场音响的感知硬扛，进行高难度的全开麦演唱！",
          "2. 临危不乱，迅速将耳返摘下挂在耳后，用眼神和队友默契对齐节拍。",
          "3. 慌乱之中有点跟不上节拍，只能靠对口型（半开麦）糊弄过去。",
      ],
      key="s3",
  )

  if st.button("提交决定 ➔"):
    if "1." in choice:
      if st.session_state.vocal >= 40:
        update_stats(
            vocal=20,
            fans=3500,
            trust=15,
            log_msg="【Stage 3】全开麦硬扛成功！高音震撼全网，实力受到业内狂赞！",
        )
      else:
        update_stats(
            fans=-500,
            trust=-5,
            log_msg="【Stage 3】由于唱功基础不够，导致现场有些许走音，引发热议。",
        )
    elif "2." in choice:
      update_stats(
          variety=15,
          fans=2500,
          trust=10,
          log_msg="【Stage 3】冷静沉着的台风圈粉无数，展现了极强的专业素养！",
      )
    else:
      update_stats(
          fans=-1000,
          trust=-15,
          log_msg="【Stage 3】假唱动作被火眼金睛的网友捕捉到，口碑小幅下滑。",
      )

    gacha_draw()
    st.session_state.stage = 4
    st.rerun()

# -------------------------------------------------------------------
# STAGE 4：深夜生配信与粉丝互动突发
# -------------------------------------------------------------------
elif st.session_state.game_started and st.session_state.stage == 4:
  st.subheader("🚩 Stage 4：Jr. 独家深夜生配信")

  st.markdown("""
    <div class="event-card">
        <div class="event-title">📌 【突发互动：直播间连线恶搞】</div>
        你在进行个人的 Johnny's web 深夜直播时，弹幕突然刷屏要求你模仿社长平时的口头禅，并连线另一位组合成员爆料私密糗事！
    </div>
    """, unsafe_allow_html=True)

  choice = st.radio(
      "你会如何掌控这场直播？",
      [
          "1. 高情商巧妙化解，大谈对组合未来的认真规划，走温柔治愈路线。",
          "2. 幽默感拉满，大方模仿社长并爆料队友洗澡不锁门，笑果拔群！",
          "3. 险些说错话泄露了公司还未公开的新专辑企划机密！",
      ],
      key="s4",
  )

  if st.button("提交决定 ➔"):
    if "1." in choice:
      update_stats(
          trust=20,
          fans=2000,
          log_msg="【Stage 4】真诚走心的发言让粉丝和高层倍感欣慰。",
      )
    elif "2." in choice:
      update_stats(
          variety=25,
          fans=4000,
          trust=5,
          log_msg="【Stage 4】直播片段直接冲上推特趋势第一，综艺感封神！",
      )
    else:
      update_stats(
          trust=-25,
          fans=1000,
          log_msg="【Stage 4】险些泄密导致被经纪人当场切断直播，连夜写检讨！",
      )

    gacha_draw()
    st.session_state.stage = 5
    st.rerun()

# -------------------------------------------------------------------
# STAGE 5：文春炮绯闻危机 (道具联动)
# -------------------------------------------------------------------
elif st.session_state.game_started and st.session_state.stage == 5:
  st.subheader("🚩 Stage 5：文春炮突击绯闻危机")

  st.markdown("""
    <div class="event-card">
        <div class="event-title">📌 【致命危机：周刊偷拍风波】</div>
        八卦周刊突然放出风声，称拍到了你深夜与神秘异性出入的照片，要求事务所对质！网络舆论瞬间狂风暴雨！
    </div>
    """, unsafe_allow_html=True)

  has_shield = "🛡️ 防文春护身符" in st.session_state.inventory
  if has_shield:
    st.info(
        "💡 **触发道具生效**：你背包中的【🛡️ 防文春护身符】自动生效，成功化解了一半危机！"
    )

  choice = st.radio(
      "危机公关，你打算采取什么行动？",
      [
          "1. 连夜向社长坦白一切（只是普通聚会），配合公司公关部极速澄清。",
          "2. 独自在博客发长文宣誓“我的爱只属于粉丝”，跟媒体硬刚到底。",
          "3. 采取冷处理闭麦不回应，任由舆论发酵。",
      ],
      key="s5",
  )

  if st.button("提交决定 ➔"):
    if "1." in choice:
      bonus_trust = 30 if has_shield else 20
      update_stats(
          trust=bonus_trust,
          fans=500,
          log_msg="【Stage 5】公关部雷厉风行，完美将负面新闻压制下来！",
      )
      if has_shield:
        st.session_state.inventory.remove("🛡️ 防文春护身符")
    elif "2." in choice:
      if random.random() < 0.6 or has_shield:
        update_stats(
            fans=5000,
            trust=-10,
            log_msg="【Stage 5】热血感发言让粉丝极具凝聚力，固粉大成功！",
        )
      else:
        update_stats(
            fans=-4000,
            trust=-30,
            log_msg="【Stage 5】激进言论遭到媒体持续深挖，导致大面积脱粉危机！",
        )
    else:
      update_stats(
          fans=-3000,
          trust=-25,
          log_msg="【Stage 5】冷处理让大众认为默认事实，形象大受打击。",
      )

    st.session_state.stage = 6
    st.rerun()

# -------------------------------------------------------------------
# STAGE 6: 帝国剧场 - 出道最终大决选
# -------------------------------------------------------------------
elif st.session_state.game_started and st.session_state.stage == 6:
  st.subheader("🏁 Final Stage：帝国剧场 CD 出道大决选")

  if st.session_state.avatar_url:
    st.image(
        st.session_state.avatar_url,
        caption=f"{st.session_state.group} - {st.session_state.member} 的出道定妆照",
        width=300,
    )

  st.markdown("""
    <div class="event-card">
        <div class="event-title">👑 【终局审判：CD 出道记者会】</div>
        帝国剧场座无虚席闪光灯闪烁。社长坐在台前，手中正翻开那本决定命运的 <b>“CD 正式出道名单”</b>。<br><br>
        历经千难万险，你的偶像生涯将在此刻迎来终极裁决！
    </div>
    """, unsafe_allow_html=True)

  if st.button("🌟 揭晓最终出道结果 🌟", use_container_width=True):
    st.markdown("---")

    total_ability = (
        st.session_state.dance
        + st.session_state.vocal
        + st.session_state.variety
    )
    trust = st.session_state.trust
    fans = st.session_state.fans

    if trust < 25:
      st.error("💀 【结局：退所 / 遗憾离场】")
      st.write(
          f"很遗憾，{st.session_state.member}。"
          f"由于社长信任度跌至谷底（{trust}）, 你未能在事务所走到最后，最终遗憾选择退所。"
      )
    elif fans >= 7500 and total_ability >= 105 and trust >= 60:
      st.balloons()
      st.success("🎉 【结局：百万畅销 - 传奇顶流 CD 出道！】")
      st.markdown(
          f"### 👑 恭喜 {st.session_state.group} 的 **{st.session_state.member}**！\n"
          "你凭借精湛的舞台实力、极高的社长信任与庞大粉丝群，在帝国剧场顺利接过了出道金标签！"
          "出道单曲空降各大榜单首位，正式登顶日本娱乐圈新一代顶流巨星！"
      )
    elif fans >= 4000 and trust >= 40:
      st.success("✨ 【结局：闪耀登场 - 顺利 CD 出道！】")
      st.markdown(
          f"### 👏 恭喜 {st.session_state.group} 的 **{st.session_state.member}**！\n"
          "经过不懈的努力与多次危机的化解，社长最终为你敲定了出道企划！你成功跨越 Jr. 阶段，正式踏上主流明星舞台！"
      )
    else:
      st.warning("⚠️ 【结局：万年骨干 / 舞台剧专项演员】")
      st.write(
          f"很可惜，{st.session_state.member}。"
          "虽然你充满个人特色，但整体综合实力或粉丝基础距离 CD 出道还有一步之遥。"
          "社长决定让你继续深耕剧场与舞台，等待下一次机会。"
      )

    st.markdown("---")
    st.markdown("### 📜 你的星途终极档案记录")
    st.write(
        f"- 最终实力总和：**{total_ability} pt**（舞:{st.session_state.dance} / 唱:{st.session_state.vocal} / 综:{st.session_state.variety}）"
    )
    st.write(f"- 最终社长信任：**{trust} / 100**")
    st.write(f"- 最终粉丝总数：**{fans:,} 人**")
    st.write(
        f"- 收集道具背包：**{', '.join(st.session_state.inventory) if st.session_state.inventory else '无'}**"
    )

    st.markdown("#### 📖 历程大事件回顾：")
    for log in st.session_state.logs:
      st.caption(f"• {log}")

    st.write("")
    if st.button("🎮 开启新的偶像人生"):
      init_game()
      st.rerun()
