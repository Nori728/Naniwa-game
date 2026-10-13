import random
import time
import streamlit as st

# 1. 页面基础配置
st.set_page_config(
    page_title="星途闪耀：我的练习生日常",
    page_icon="🌟",
    layout="centered",
)

# 2. 团队数据（已按年龄严格从大到小排序）
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

# 3. 页面样式美化（高颜值极简风格）
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
    div[data-testid="stRadio"] div[role="radiogroup"] > label {
        background-color: #ffffff;
        padding: 12px 18px;
        border-radius: 15px;
        margin-bottom: 8px;
        border: 2px solid #ea80fc;
        transition: all 0.2s ease;
        color: #4a148c;
        font-weight: 600;
        touch-action: manipulation;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background-color: #f3e5f5;
        border-color: #ff4081;
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

  # 后台隐形数值（玩家不可见）
  st.session_state.energy = 100  # 体力
  st.session_state.dance = 20  # 舞蹈
  st.session_state.vocal = 20  # 歌唱
  st.session_state.variety = 20  # 综艺
  st.session_state.fans = 100  # 粉丝数
  st.session_state.trust = 50  # 社长信任度
  st.session_state.bond = 10  # 团员羁绊值

  st.session_state.logs = []


if "game_started" not in st.session_state:
  init_game()


# 获取随机团员辅助函数
def get_rand_member():
  members = IDOL_GROUPS.get(st.session_state.group, ["前辈"])
  return random.choice(members)


# 主标题
st.title("💖 星途闪耀：我的练习生日常")

# -------------------------------------------------------------------
# STAGE 0: 开局设定（输入名字与选择组合）
# -------------------------------------------------------------------
if not st.session_state.game_started:
  st.markdown(
      '<div class="cute-info">✨ 欢迎来到 STARTO 偶像养成营！请输入你的名字，并选择想加入/同行研修的组合！</div>',
      unsafe_allow_html=True,
  )

  name_input = st.text_input(
      "✏️ 请输入你的名字（或昵称）：", placeholder="例如：酱酱 / 小夏"
  )

  st.markdown("---")
  st.markdown("#### 🏢 请选择想加入/同行研修的组合：")

  # 手机适配单选按钮
  selected_group = st.radio(
      "点击选择组合：", list(IDOL_GROUPS.keys()), key="group_radio"
  )

  st.markdown("---")
  if st.button("🚀 签订研修契约，开启练习生生涯！", use_container_width=True):
    if not name_input.strip():
      st.error("请先输入名字哦！")
    else:
      st.session_state.player_name = name_input.strip()
      st.session_state.group = selected_group
      st.session_state.game_started = True
      st.rerun()

# -------------------------------------------------------------------
# 游戏主流程（剧情事件 + 自由排程，无显式数据面板）
# -------------------------------------------------------------------
if st.session_state.game_started:
  curr_stage = st.session_state.stage

  # 规则：特定节点触发【自由自主排程日】
  is_free_training_day = curr_stage in [2, 5, 8, 12, 15, 18]

  if is_free_training_day and curr_stage < 20:
    st.subheader("🗓️ 自由特训与日常安排")
    st.info(
        "💡 **自主安排日**：今天没有集体课程，你可以自由安排练习、休息或与同伴互动。"
    )

    col1, col2 = st.columns(2)
    with col1:
      if st.button("💃 在舞蹈房死磕高难度步法"):
        if st.session_state.energy < 20:
          st.error("⚠️ 你感到极度疲惫，已经没有精力继续高强度练习了，快去休息吧！")
        else:
          gain = random.randint(15, 25)
          st.session_state.dance += gain
          st.session_state.energy -= 20
          st.session_state.logs.append(
              "在舞蹈房对着镜子反复练习，舞步更加娴熟自然。"
          )
          st.session_state.stage += 1
          st.rerun()

      if st.button("🎤 到声乐室练习高音与发声"):
        if st.session_state.energy < 20:
          st.error("⚠️ 你感到极度疲惫，嗓子有些哑了，快去休息吧！")
        else:
          gain = random.randint(15, 25)
          st.session_state.vocal += gain
          st.session_state.energy -= 20
          st.session_state.logs.append(
              "在声乐室练习发声技巧，开嗓效果显著。"
          )
          st.session_state.stage += 1
          st.rerun()

    with col2:
      member_name = get_rand_member()
      if st.button(f"🍲 与 {member_name} 相约去吃烤肉聊心事"):
        if st.session_state.energy < 15:
          st.error("⚠️ 你太累了，连出门吃饭的精力都没有了，快去休息吧！")
        else:
          st.session_state.bond += 15
          st.session_state.fans += 300
          st.session_state.energy -= 15
          st.session_state.logs.append(
              f"与 {member_name} 深夜吃烤肉，聊起了许多对未来的憧憬，感情加深。"
          )
          st.session_state.stage += 1
          st.rerun()

      if st.button("💤 回宿舍彻底休息躺平"):
        st.session_state.energy = min(100, st.session_state.energy + 40)
        st.session_state.logs.append("睡了个大饱觉，整个人恢复了精气神！")
        st.session_state.stage += 1
        st.rerun()

  # 普通剧情关卡（根据当前能力隐形判定）
  elif curr_stage < 20:
    st.subheader(f"📍 阶段 {curr_stage}")

    member = get_rand_member()

    if curr_stage == 1:
      st.markdown(f"""
            <div class="event-card">
                <b>🎵 【雨后练习室的汗水】</b><br>
                今天基础舞蹈课强度极大，大家都瘫坐在地上。{member} 擦着汗走过来拍了拍你的肩膀：“{st.session_state.player_name}，刚才那个转身动作重心有点偏哦，要不要再试一次？”
            </div>
            """, unsafe_allow_html=True)

      c1 = st.button("1. 挑战：独自留下来对着镜子死磕动作直到深夜")
      c2 = st.button("2. 递上买来的冰麦茶，和大家结伴回宿舍聊聊天")

      if c1:
        if st.session_state.dance >= 15:
          st.success(
              f"✨ 你的专注与执着感动了大家！{member} 回头看到了你加练的背影，默默为你点赞。"
          )
          st.session_state.dance += 20
        else:
          st.error("❌ 动作发力不对导致轻微拉伤，体力消耗巨大！")
          st.session_state.energy -= 30
        st.session_state.stage += 1
        st.rerun()

      if c2:
        st.session_state.bond += 10
        st.session_state.fans += 200
        st.session_state.stage += 1
        st.rerun()

    else:
      # 动态生成剧情
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
          {
              "title": "📖 杂志采访时刻",
              "desc": "记者问起你平时私底下和团里谁关系最好、最大的爱好是什么。",
              "opt1": "分享与队友们深夜吃烤肉的搞笑日常。",
              "opt2": "聊聊自己最近研究的音乐创作与编曲。",
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

  # -------------------------------------------------------------------
  # STAGE 20: 终局 CD 出道决选
  # -------------------------------------------------------------------
  else:
    st.subheader("🏁 帝国剧场 CD 出道决选（终局裁决）")

    st.markdown(f"""
        <div class="event-card">
            <b>✨ 【命运的聚光灯】</b><br>
            帝国剧场金碧辉煌，全日本数百家媒体的闪光灯不断闪烁。社长坐在话筒前，即将宣读今年正式获得 <b>CD 出道</b> 资格的最终名单！
        </div>
        """, unsafe_allow_html=True)

    if st.button("🌟 揭晓最终出道裁决与终局档案 🌟", use_container_width=True):
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
            f"🎉 恭喜 **{st.session_state.player_name}**！你凭借出色的综合实力与不可替代的团队羁绊，与 **{st.session_state.group}** 成功获得 CD 出道资格！"
        )
      else:
        st.warning(
            f"⚠️ 遗憾！**{st.session_state.player_name}** 的综合爆发力距离主流 CD 出道还有一小步，社长安排你继续作为组合的中坚力量深耕舞台！"
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

      st.markdown("#### 📖 你的星途回忆手记：")
      for log in st.session_state.logs:
        st.caption(f"• {log}")

      st.write("")
      if st.button("🎮 开启全新练习生人生"):
        init_game()
        st.rerun()
