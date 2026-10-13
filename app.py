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
        padding: 24px;
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
      '<div class="cute-info">✨ 欢迎来到 STARTO 偶像养成营！请先输入你的名字，然后选择心仪的组合，开启充满未知与挑战的练习生生涯！</div>',
      unsafe_allow_html=True,
  )

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
# 游戏主流程（扩展至丰富的剧情与多样化反应微游戏）
# -------------------------------------------------------------------
if st.session_state.game_started:
  curr_stage = st.session_state.stage
  is_free_training_day = curr_stage in [3, 6, 9, 13, 17]

  # 1. 自由排程特训日（完全无数值提示）
  if is_free_training_day and curr_stage < 22:
    st.subheader(f"🗓️ 第 {curr_stage} 阶段：自主特训与日常安排")
    st.info(
        "💡 **自主安排日**：今天没有集体课程，请根据当前的体力状况自由安排行程！"
    )

    col1, col2 = st.columns(2)
    with col1:
      if st.button("💃 在舞蹈房死磕高难度步法"):
        if st.session_state.energy < 20:
          st.error("⚠️ 你感到极度疲惫，体力不足，快去休息吧！")
        else:
          st.session_state.dance += random.randint(15, 25)
          st.session_state.energy -= 20
          st.session_state.stage += 1
          st.rerun()
      if st.button("🎤 到声乐室练习高音发声"):
        if st.session_state.energy < 20:
          st.error("⚠️ 嗓子有些哑了，体力不足，快去休息吧！")
        else:
          st.session_state.vocal += random.randint(15, 25)
          st.session_state.energy -= 20
          st.session_state.stage += 1
          st.rerun()
    with col2:
      member_name = get_rand_member()
      if st.button(f"🍲 与 {member_name} 约去吃烤肉聊心事"):
        if st.session_state.energy < 15:
          st.error("⚠️ 太累了，连出门的精力都没有啦！")
        else:
          st.session_state.bond += 15
          st.session_state.fans += 300
          st.session_state.energy -= 15
          st.session_state.stage += 1
          st.rerun()
      if st.button("💤 回宿舍彻底躺平休息"):
        st.session_state.energy = min(100, st.session_state.energy + 40)
        st.session_state.stage += 1
        st.rerun()

  elif curr_stage < 22:
    st.subheader(f"📍 阶段 {curr_stage} / 21")
    member = get_rand_member()

    # 2. 反应小游戏 A：【看准时机按下去】节奏打歌音符判定！
    if curr_stage in [2, 10, 16]:
      st.markdown(f"""
            <div class="event-card">
                <b>🎮 【互动小游戏：全开麦节拍音符卡点】</b><br>
                歌曲副歌的高能瞬间来临！前方正在高速落下节奏音符，请死死盯着节拍，<b>看准时机在最完美的一瞬间按下按钮</b>！
            </div>
            """, unsafe_allow_html=True)

      # 模拟随机节奏落点判定
      if "target_beat" not in st.session_state:
        st.session_state.target_beat = random.choice([
            "🔥 【BEAT 1】",
            "⚡ 【BEAT 2】",
            "🌟 【BEAT 3】",
        ])

      st.markdown(
          f'<div class="game-box">🎶 当前流动的节奏音符：<b>{st.session_state.target_beat}</b><br>请凭手速和反应，在节拍正中心时立刻点击下方按钮！</div>',
          unsafe_allow_html=True,
      )

      col_hit1, col_hit2, col_hit3 = st.columns(3)
      with col_hit1:
        hit_1 = st.button("🔥 拍下 1")
      with col_hit2:
        hit_2 = st.button("⚡ 拍下 2")
      with col_hit3:
        hit_3 = st.button("🌟 拍下 3")

      # 判断玩家点击时机
      pressed = None
      if hit_1:
        pressed = "🔥 【BEAT 1】"
      elif hit_2:
        pressed = "⚡ 【BEAT 2】"
      elif hit_3:
        pressed = "🌟 【BEAT 3】"

      if pressed:
        if pressed == st.session_state.target_beat:
          st.balloons()
          st.success("🎯 **PERFECT！完美卡点！** 节奏精准无误，全场粉丝疯狂尖叫！")
          st.session_state.fans += 1500
          st.session_state.dance += 20
        else:
          st.warning(
              "⚠️ **MISS！稍微拍快或拍慢了一点点！** 节拍略有瑕疵，不过顺利过关。"
          )
          st.session_state.trust -= 3
        # 清除当前目标节拍，进入下一关
        del st.session_state.target_beat
        st.session_state.stage += 1
        st.rerun()

    # 3. 反应小游戏 B：【舞台跳格子/走位闪避危机】
    elif curr_stage in [5, 14, 19]:
      st.markdown(f"""
            <div class="event-card">
                <b>🎮 【互动小游戏：舞台走位安全跳格子】</b><br>
                在大型巨蛋巡演中，升降台由于机械故障突然出现错位！舞台地面随机亮起了三个方向的格子，<b>只有一个是安全正确的走位格</b>，请凭直觉迅速选择！
            </div>
            """, unsafe_allow_html=True)

      if "correct_lane" not in st.session_state:
        st.session_state.correct_lane = random.choice([
            "左侧安全通道",
            "中央主升降格",
            "右侧延伸舞台",
        ])

      col_l, col_m, col_r = st.columns(3)
      with col_l:
        choice_l = st.button("⬅️ 左侧安全通道")
      with col_m:
        choice_m = st.button("⬆️ 中央主升降格")
      with col_r:
        choice_r = st.button("➡️ 右侧延伸舞台")

      selected_lane = None
      if choice_l:
        selected_lane = "左侧安全通道"
      elif choice_m:
        selected_lane = "中央主升降格"
      elif choice_r:
        selected_lane = "右侧延伸舞台"

      if selected_lane:
        if selected_lane == st.session_state.correct_lane:
          st.balloons()
          st.success(
              "🎯 **完美闪避！** 你以极佳的舞台反应力精准踩中安全格，动作帅气逼人！"
          )
          st.session_state.fans += 1200
          st.session_state.trust += 10
        else:
          st.warning(
              "⚠️ **踩空了！** 你不小心撞到了道具，踉跄了一下，不过凭借丰富经验迅速稳住！"
          )
          st.session_state.trust -= 5
        del st.session_state.correct_lane
        st.session_state.stage += 1
        st.rerun()

    # 4. 丰富多元的剧情与故事关卡
    else:
      story_pool = [
          {
              "title": "📖 练习室深夜的偶遇",
              "desc": (
                  f"深夜两点，整个练习室只剩下你和 {member}。他转过身看着满头大汗的你，"
                  "递过来一瓶冰镇苏打水：“"
                  f"{st.session_state.player_name}，最近看你每天都练到这么晚，是为了追求怎样的舞台呢？”"
              ),
              "opt1": (
                  "“想成为能和大家并肩闪耀、绝不拖后腿的核心存在。”"
              ),
              "opt2": "“单纯觉得在舞台上挥洒汗水的自己，非常帅气！”",
          },
          {
              "title": "☕ 前辈休息室的残酷现实",
              "desc": (
                  f"前辈组合今天在隔壁录音，你鼓起勇气前去观摩。前辈看着你们的排练录像，"
                  "语重心长地说道：“Jr. 的时期转瞬即逝，光靠努力是不够的，你们必须找到属于自己的‘绝对记忆点’。”"
              ),
              "opt1": "把前辈的话牢牢记在笔记本上，决定明天开始开发个人绝招。",
              "opt2": "笑着向前辈道谢，并承诺会用最热血的团魂证明自己。",
          },
          {
              "title": "⚡ 突发！八卦周刊的深夜跟拍",
              "desc": "结束外景拍摄回宿舍的路上，你敏锐地发现街角暗处有闪光灯一闪而过——是八卦周刊的狗仔偷拍！",
              "opt1": "立刻保持冷静，目不斜视地走过，随后第一时间向社长报备。",
              "opt2": "微笑着对镜头方向挥了挥手，大大方方展现顶级少年的阳光感。",
          },
          {
              "title": "📺 冠名综艺的残酷整蛊考验",
              "desc": (
                  f"在录制组合冠名综艺时，节目组安排了毫无防备的‘落穴整蛊’！你和 {member}"
                  " 一起中招掉进了满是粉末的陷阱里，全场爆笑如雷！"
              ),
              "opt1": "第一时间从粉末里爬出来做出生无可恋的夸张表情包！",
              "opt2": "笑着把粉末抹到队友脸上，带头开启欢乐的大混战！",
          },
          {
              "title": "🎶 录音棚里找不到感觉的瓶颈期",
              "desc": "新单曲录制进行到关键时刻，你的声线因为连续高强度赶通告而有些沙哑，制作人在录音室里皱起了眉头。",
              "opt1": "主动请求休息10分钟调整状态，用温水润喉后重新完美进麦。",
              "opt2": "选择用带点沙哑磁性的独特嗓音硬唱下来，意外呈现出绝佳的情感张力！",
          },
      ]

      # 根据关卡轮流展示不同的精彩故事
      story_item = story_pool[(curr_stage * 3) % len(story_pool)]

      st.markdown(f"""
            <div class="event-card">
                <b>{story_item['title']}</b><br><br>
                {story_item['desc']}
            </div>
            """, unsafe_allow_html=True)

      if st.button(f"1. {story_item['opt1']}"):
        st.session_state.dance += 10
        st.session_state.fans += 500
        st.session_state.trust += 5
        st.session_state.stage += 1
        st.rerun()

      if st.button(f"2. {story_item['opt2']}"):
        st.session_state.variety += 15
        st.session_state.fans += 600
        st.session_state.bond += 10
        st.session_state.stage += 1
        st.rerun()

  # -------------------------------------------------------------------
  # STAGE 22: 帝国剧场终局裁决
  # -------------------------------------------------------------------
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
          st.session_state.fans >= 2000
          and total_ability >= 120
          and st.session_state.trust >= 50
      ):
        st.balloons()
        st.success(
            f"🎉 恭喜 **{st.session_state.player_name}**！你凭借惊人的手速反应、无数次汗水与不可替代的团队羁绊，与 **{st.session_state.group}** 的伙伴们完美闪耀帝国剧场，正式华丽出道！"
        )
      else:
        st.warning(
            f"⚠️ 遗憾！**{st.session_state.player_name}** 的综合表现距离完美标准还有一丝差距，社长安排你继续深耕舞台，未来可期！"
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
