import random
import time
import streamlit as st

# 1. 页面基础配置
st.set_page_config(
    page_title="星途闪耀：我的练习生日常",
    page_icon="🌟",
    layout="centered",
)

# 2. 团队与成员数据（已按年龄从大到小严格排序）
IDOL_GROUPS = {
    "ARASHI (岚)": ["大野智", "樱井翔", "相叶雅纪", "二宫和也", "松本润"],
    "WEST.": [
        "中间淳太",
        "桐山照史",
        "滨田崇裕",
        "重冈大毅",
        "神山智洋",
        "藤井流星",
        "小泷望",
    ],
    "SUPER EIGHT": ["横山裕", "村上信五", "丸山隆平", "安田章大", "大仓忠义"],
    "Snow Man": [
        "深泽辰哉",
        "岩本照",
        "宫馆凉太",
        "渡边翔太",
        "阿部亮平",
        "佐久间大介",
        "向井康二",
        "目黑莲",
        "ラウール",
    ],
    "SixTONES": [
        "高地优吾",
        "京本大我",
        "杰西 (Jesse)",
        "田中树",
        "松村北斗",
        "森本慎太郎",
    ],
    "Aぇ! group (A少年)": [
        "末泽诚也",
        "草间理查德敬太",
        "正门良规",
        "小岛健",
        "佐野晶哉",
    ],
    "浪花男子 (なにわ男子)": [
        "藤原丈一郎",
        "大桥和也",
        "西畑大吾",
        "大西流星",
        "高桥恭平",
        "道枝骏佑",
        "长尾谦杜",
    ],
    "King & Prince": ["岸优太", "平野紫耀", "神宫寺勇太", "永濑廉", "高桥海人"],
    "Travis Japan": [
        "川岛如惠留",
        "七五三挂龙也",
        "吉泽闲也",
        "中村海人",
        "宫近海斗",
        "松仓海斗",
        "松田元太",
    ],
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
}

# 3. 样式美化
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #fce4ec 0%, #f3e5f5 100%);
    }
    .event-card {
        background: #2d1b4e;
        color: #ffffff;
        padding: 22px;
        border-radius: 18px;
        border: 3px solid #ff80ab;
        box-shadow: 0px 10px 25px rgba(255, 128, 171, 0.3);
        margin: 15px 0;
        font-size: 16px;
        line-height: 1.7;
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
    .game-box {
        background: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #ab47bc;
        text-align: center;
        margin: 15px 0;
        color: #4a148c;
    }
    .stButton > button {
        background: linear-gradient(45deg, #ff4081, #ab47bc) !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 10px 25px !important;
        touch-action: manipulation;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# 4. 初始化游戏数据
def init_game():
  st.session_state.game_started = False
  st.session_state.stage = 1
  st.session_state.player_name = ""
  st.session_state.group = ""

  st.session_state.energy = 100
  st.session_state.dance = 20
  st.session_state.vocal = 20
  st.session_state.variety = 20
  st.session_state.fans = 100
  st.session_state.trust = 50
  st.session_state.bond = 10
  st.session_state.logs = []


if "game_started" not in st.session_state:
  init_game()


def get_rand_member():
  members = IDOL_GROUPS.get(st.session_state.group, ["前辈"])
  return random.choice(members)


# 主标题
st.title("💖 星途闪耀：我的练习生日常")

# -------------------------------------------------------------------
# STAGE 0: 输入名字与选团
# -------------------------------------------------------------------
if not st.session_state.game_started:
  st.markdown(
      '<div class="cute-info">✨ 欢迎来到 STARTO 偶像养成营！请先输入你的名字，然后选择心仪的组合，开启养成之旅！</div>',
      unsafe_allow_html=True,
  )

  # 稳稳找回的输入名字组件
  name_input = st.text_input(
      "✏️ 请输入你的名字（或昵称）：", placeholder="例如：酱酱 / 小夏"
  )

  st.markdown("---")
  selected_group = st.selectbox(
      "选择你想加入/并肩作战的组合：", list(IDOL_GROUPS.keys())
  )

  st.markdown("---")
  if st.button("🚀 签订研修契约，正式开启练习生生活！", use_container_width=True):
    if not name_input.strip():
      st.error("请先输入你的名字哦！")
    else:
      st.session_state.player_name = name_input.strip()
      st.session_state.group = selected_group
      st.session_state.game_started = True
      st.rerun()

# -------------------------------------------------------------------
# 游戏主流程
# -------------------------------------------------------------------
if st.session_state.game_started:
  curr_stage = st.session_state.stage
  is_free_training_day = curr_stage in [2, 5, 8, 12, 15, 18]

  # 1. 自由排程特训日
  if is_free_training_day and curr_stage < 20:
    st.subheader("🗓️ 自主特训与日常安排")
    st.info(
        "💡 **自主安排日**：今天没有集体课程，请根据当前的体力状况自由安排！"
    )

    col1, col2 = st.columns(2)
    with col1:
      if st.button("💃 在舞蹈房死磕高难度步法 (-20体力)"):
        if st.session_state.energy < 20:
          st.error("⚠️ 你感到极度疲惫，体力不足，快去休息吧！")
        else:
          gain = random.randint(15, 25)
          st.session_state.dance += gain
          st.session_state.energy -= 20
          st.session_state.stage += 1
          st.rerun()
      if st.button("🎤 到声乐室练习高音发声 (-20体力)"):
        if st.session_state.energy < 20:
          st.error("⚠️ 嗓子有些哑了，体力不足，快去休息吧！")
        else:
          gain = random.randint(15, 25)
          st.session_state.vocal += gain
          st.session_state.energy -= 20
          st.session_state.stage += 1
          st.rerun()
    with col2:
      member_name = get_rand_member()
      if st.button(f"🍲 与 {member_name} 约去吃烤肉聊心事 (-15体力)"):
        if st.session_state.energy < 15:
          st.error("⚠️ 太累了，连出门的精力都没有啦！")
        else:
          st.session_state.bond += 15
          st.session_state.fans += 300
          st.session_state.energy -= 15
          st.session_state.stage += 1
          st.rerun()
      if st.button("💤 回宿舍彻底躺平休息 (+40体力)"):
        st.session_state.energy = min(100, st.session_state.energy + 40)
        st.session_state.stage += 1
        st.rerun()

  elif curr_stage < 20:
    st.subheader(f"📍 阶段 {curr_stage} / 20")
    member = get_rand_member()

    # 2. 滑块小游戏 A：舞台爆发力精准操控 (目标值 88)
    if curr_stage in [3, 11]:
      st.markdown(f"""
            <div class="event-card">
                <b>🎮 【滑块挑战一：舞台爆发力完美狙击】</b><br>
                现场突然抽中了由 {st.session_state.player_name} 主导的舞蹈 Break！请将下方的滑块调整到完美爆发值 <b>88</b>！
            </div>
            """, unsafe_allow_html=True)

      user_power = st.slider(
          "拖动调整爆发力度 (1-100)：", 1, 100, 50, key=f"slider_{curr_stage}"
      )

      if st.button("🔥 锁定爆发力度！"):
        diff = abs(user_power - 88)
        if diff <= 5:
          st.balloons()
          st.success("🎯 **完美命中 (PERFECT)！** 全场沸腾，舞蹈实力暴涨！")
          st.session_state.fans += 1200
          st.session_state.dance += 25
        elif diff <= 20:
          st.success("✨ **良好表现 (GREAT)！** 顺利过关，动作很稳。")
          st.session_state.fans += 500
          st.session_state.dance += 10
        else:
          st.warning("⚠️ **有些偏离 (MISS)！** 稍微有点脱节，不过有惊无险。")
          st.session_state.trust -= 3
        st.session_state.stage += 1
        st.rerun()

    # 3. 滑块小游戏 B：声乐高音音准微调 (目标值 70)
    elif curr_stage in [7, 14]:
      st.markdown(f"""
            <div class="event-card">
                <b>🎮 【滑块挑战二：全开麦高音音准卡点】</b><br>
                歌曲进入了最高潮的副歌高音部分！请把滑块精确推到音准完美点 <b>70</b> 处，稳住高音！
            </div>
            """, unsafe_allow_html=True)

      user_pitch = st.slider(
          "调整你的声乐高音音准 (1-100)：", 1, 100, 40, key=f"pitch_{curr_stage}"
      )

      if st.button("🎤 稳住高音输出！"):
        diff = abs(user_pitch - 70)
        if diff <= 5:
          st.balloons()
          st.success("🎯 **神级高音 (PERFECT)！** 高音震撼全网，歌唱实力大爆发！")
          st.session_state.fans += 1500
          st.session_state.vocal += 30
        elif diff <= 20:
          st.success("✨ **平稳发挥 (GREAT)！** 完美驾驭了副歌，顺利过关。")
          st.session_state.fans += 600
          st.session_state.vocal += 15
        else:
          st.warning(
              "⚠️ **高音略微不稳 (MISS)！** 差点破音，好在及时收住。"
          )
          st.session_state.trust -= 5
        st.session_state.stage += 1
        st.rerun()

    # 4. 滑块小游戏 C：饭撒/宠粉心跳平衡度 (目标值 50)
    elif curr_stage == 17:
      st.markdown(f"""
            <div class="event-card">
                <b>🎮 【滑块挑战三：巨蛋巡演粉丝饭撒平衡】</b><br>
                面对全场挥舞的应援棒，你需要完美掌控对粉丝放电的力度，不能太冷漠也不能太油腻，将心跳值稳在 <b>50</b>！
            </div>
            """, unsafe_allow_html=True)

      user_fanservice = st.slider(
          "调整你的宠粉互动度 (1-100)：", 1, 100, 30, key=f"fs_{curr_stage}"
      )

      if st.button("💖 释放绝美饭撒！"):
        diff = abs(user_fanservice - 50)
        if diff <= 5:
          st.balloons()
          st.success("🎯 **狙击心跳 (PERFECT)！** 绝美饭撒全网疯传，粉丝暴涨！")
          st.session_state.fans += 2000
          st.session_state.variety += 25
        elif diff <= 20:
          st.success("✨ **甜美互动 (GREAT)！** 大家都接收到了你的心意。")
          st.session_state.fans += 800
          st.session_state.variety += 10
        else:
          st.warning("⚠️ **略显生疏 (MISS)！** 表情有点僵硬，不过粉丝依然很包容。")
        st.session_state.stage += 1
        st.rerun()

    # 5. 常规剧情选项关卡
    else:
      events = [
          {
              "title": "📺 临时突袭直播",
              "desc": f"节目组突然把摄像头对准了 {st.session_state.player_name}！{member} 在旁边给你使眼色！",
              "opt1": "用搞笑段子接梗，引发全场爆笑！",
              "opt2": "即兴展示一段高难练舞，展示硬实力！",
          },
          {
              "title": "⚡ 耳返走音危机",
              "desc": "现场彩排设备突发故障，耳返里全是嘈杂的杂音！",
              "opt1": "凭肌肉记忆与感觉全开麦硬扛高音！",
              "opt2": "冷静地摘下耳返，与队友依靠眼神对齐节奏。",
          },
      ]
      ev = events[curr_stage % len(events)]

      st.markdown(f"""
            <div class="event-card">
                <b>📌 【{ev['title']}】</b><br>
                {ev['desc']}
            </div>
            """, unsafe_allow_html=True)

      if st.button(f"1. {ev['opt1']}"):
        st.session_state.variety += 15
        st.session_state.fans += 400
        st.session_state.stage += 1
        st.rerun()

      if st.button(f"2. {ev['opt2']}"):
        st.session_state.dance += 15
        st.session_state.vocal += 15
        st.session_state.trust += 10
        st.session_state.stage += 1
        st.rerun()

  else:
    st.subheader("🏁 帝国剧场阶段（终局裁决）")
    st.markdown(f"""
        <div class="event-card">
            <b>✨ 【命运的聚光灯】</b><br>
            帝国剧场金碧辉煌，全日本数百家媒体的闪光灯不断闪烁。社长坐在话筒前，即将宣读最终的考核结果！
        </div>
        """, unsafe_allow_html=True)

    if st.button("🌟 揭晓最终考核结果与终局档案 🌟", use_container_width=True):
      st.markdown("---")
      total_ability = (
          st.session_state.dance
          + st.session_state.vocal
          + st.session_state.variety
      )

      if (
          st.session_state.fans >= 1800
          and total_ability >= 110
          and st.session_state.trust >= 45
      ):
        st.balloons()
        st.success(
            f"🎉 恭喜 **{st.session_state.player_name}**！你凭借出色的综合实力与不可替代的团队羁绊，与 **{st.session_state.group}** 的伙伴们完美完成了全部研修！"
        )
      else:
        st.warning(
            f"⚠️ 遗憾！**{st.session_state.player_name}** 的综合爆发力距离完美标准还有一小步，社长安排你继续深耕舞台，未来可期！"
        )

      st.markdown("---")
      st.markdown(
          f"### 📊 练习生【{st.session_state.player_name}】的终极能力解密"
      )
      st.write(
          f"- 💃 舞蹈能力：**{st.session_state.dance} pt** | 🎤 歌唱能力：**{st.session_state.vocal} pt** | 🤡 综艺表现：**{st.session_state.variety} pt**"
      )
      st.write(
          f"- 💖 粉丝总数：**{st.session_state.fans:,} 人** | 🤝 社长信任：**{st.session_state.trust}** | 💞 团员羁绊：**{st.session_state.bond}**"
      )

      st.write("")
      if st.button("🎮 开启全新练习生人生"):
        init_game()
        st.rerun()
