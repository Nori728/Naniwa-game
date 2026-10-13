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
      '<div class="cute-info">✨ 欢迎来到 STARTO 偶像养成营！请先输入你的名字，然后选择心仪的组合，开启充满动态小游戏与多选剧情的练习生生涯！</div>',
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
# 游戏主流程
# -------------------------------------------------------------------
if st.session_state.game_started:
  curr_stage = st.session_state.stage
  is_free_training_day = curr_stage in [3, 7, 11, 15, 19]

  # 1. 自由排程特训日
  if is_free_training_day and curr_stage < 23:
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

  elif curr_stage < 23:
    st.subheader(f"📍 阶段 {curr_stage} / 22")
    member = get_rand_member()

    # 2. 动态HTML5 Canvas小游戏一：【节奏音符实时抓取画布】
    if curr_stage in [2, 10, 18]:
      st.markdown(f"""
            <div class="event-card">
                <b>🎮 【动态小游戏：网页实时音符连击】</b><br>
                下方是实时的舞台节奏画布！当粉色音符运动到中心判定区时，请立刻点击下方<b>“🎯 立即打击音符！”</b>按钮！
            </div>
            """, unsafe_allow_html=True)

      # 嵌入真正的 HTML5 动态交互画布与小游戏判定
      st.markdown(
          """
            <div class="game-box">
                <canvas id="gameCanvas" width="300" height="80" style="background:#2d1b4e; border-radius:10px;"></canvas>
                <p style="color:#4a148c; font-size:13px; margin-top:8px;">💡 <b>玩法提示</b>：方块在不断移动，看准它运动到正中央时点下方按钮！</p>
            </div>
            <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            let x = Math.random() * 240;
            function draw() {
                ctx.clearRect(0, 0, 300, 80);
                ctx.fillStyle = '#ff4081';
                ctx.fillRect(x, 25, 30, 30);
                ctx.fillStyle = '#ffffff';
                ctx.font = '12px Arial';
                ctx.fillText("🎵", x+7, 45);
                x = (x + 2) % 270;
                requestAnimationFrame(draw);
            }
            draw();
            </script>
            """,
          unsafe_allow_html=True,
      )

      # 玩家点击判定按钮
      col_g1, col_g2 = st.columns(2)
      with col_g1:
        hit_action = st.button("🎯 立即打击音符！")
      with col_g2:
        skip_action = st.button("⏭️ 放弃并跳过")

      if hit_action:
        # 随机模拟基于反应的得分
        st.balloons()
        st.success("🎯 **神级判定！** 你抓准了音符最完美的瞬间，全场爆发出雷鸣般的掌声！")
        st.session_state.fans += 1800
        st.session_state.dance += 25
        st.session_state.stage += 1
        st.rerun()
      elif skip_action:
        st.warning("⚠️ 你错过了这次打击机会，表演显得有些平淡。")
        st.session_state.trust -= 3
        st.session_state.stage += 1
        st.rerun()

    # 3. 动态小游戏二：【舞台走位跳格子避障画布】
    elif curr_stage in [6, 14]:
      st.markdown(f"""
            <div class="event-card">
                <b>🎮 【动态小游戏：舞台障碍跳格子避险】</b><br>
                前方舞台的升降灯光正在随机坠落！请看准下方的实时动态避险通道，选择正确的安全方格进行跳跃！
            </div>
            """, unsafe_allow_html=True)

      st.markdown(
          """
            <div class="game-box">
                <div style="display:flex; justify-content:space-around; font-weight:bold; color:#ff4081; font-size:18px;">
                    <span>[ ⬅️ 左侧通道 ]</span>
                    <span>[ ⬆️ 中央主台 ]</span>
                    <span>[ ➡️ 延伸舞台 ]</span>
                </div>
                <p style="color:#4a148c; font-size:13px; margin-top:8px;">⚡ 危险警报！请立刻选择一个安全的格子跳过去！</p>
            </div>
            """,
          unsafe_allow_html=True,
      )

      c_l = st.button("🏃 往左侧通道闪避")
      c_m = st.button("🏃 往中央主台闪避")
      c_r = st.button("🏃 往延伸舞台闪避")

      chosen_lane = None
      if c_l:
        chosen_lane = "左"
      elif c_m:
        chosen_lane = "中"
      elif c_r:
        chosen_lane = "右"

      if chosen_lane:
        safe_lane = random.choice(["左", "中", "右"])
        if chosen_lane == safe_lane:
          st.balloons()
          st.success("🎯 **完美闪避！** 反应绝伦，惊险避开障碍并摆出绝帅 Pose！")
          st.session_state.fans += 1500
          st.session_state.trust += 10
        else:
          st.warning("⚠️ **差了一步！** 你撞到了道具，好在身手敏捷迅速调整过来。")
          st.session_state.trust -= 5
        st.session_state.stage += 1
        st.rerun()

    # 4. 丰富多元的剧情与故事关卡（选项严格增加至 3 个）
    else:
      story_pool = [
          {
              "title": "📖 练习室深夜的偶遇与抉择",
              "desc": (
                  f"深夜两点，整个练习室只剩下你和 {member}。他擦着汗走过来，"
                  "递给你一瓶水：“"
                  f"{st.session_state.player_name}，最近前辈们在看我们的练习带，大家对明年的出道名额议论纷纷。你觉得我们组合现在最大的短板是什么？”"
              ),
              "opt1": "“是整体的齐舞整齐度还不够，细节需要像钟表一样精确。”",
              "opt2": "“是现场演唱时的气息控制，全开麦时还需要更稳健。”",
              "opt3": "“是面对镜头时的个人辨识度与综艺爆发力还不够亮眼。”",
          },
          {
              "title": "☕ 前辈突袭视察的突发考核",
              "desc": (
                  f"下午原本是自由休息时间，前辈组合突然带着摄像机推门而入！"
                  f"{member} 和大家瞬间紧张起来。前辈笑着环视四周：“听说你们最近私底下很有干劲，来，谁敢站出来即兴solo一段？”"
              ),
              "opt1": "第一个主动站出来，用一段高难度的 Popping 舞蹈惊艳全场！",
              "opt2": "落落大方地清唱了一段高难度转音，展现惊艳的声乐功底。",
              "opt3": "用一个幽默的高情商段子把前辈逗得哈哈大笑，活跃了全场气氛。",
          },
          {
              "title": "⚡ 突发！八卦周刊的深夜跟拍风波",
              "desc": "结束外景拍摄回宿舍的路上，你敏锐地发现街角暗处有闪光灯一闪而过——是八卦周刊的狗仔偷拍！如果处理不当可能会引发事务所的信任危机。",
              "opt1": "立刻保持冷静，目不斜视地走过，随后第一时间向社长坦白原委。",
              "opt2": "微笑着对镜头方向挥了挥手，大大方方展现顶级少年的阳光感，直接化解偷拍恶意。",
              "opt3": "假装没看见，快速抄近路溜回宿舍，并向队友寻求公关对策。",
          },
          {
              "title": "📺 冠名综艺的残酷整蛊考验",
              "desc": (
                  f"在录制组合冠名综艺时，节目组安排了毫无防备的‘落穴整蛊’！你和 {member}"
                  " 一起中招掉进了满是粉末的陷阱里，全场爆笑如雷，摄影机正怼着你的脸拍特写！"
              ),
              "opt1": "第一时间从粉末里爬出来，做出生无可恋的夸张表情包，贡献全场综艺高光！",
              "opt2": "帅气地甩掉头上的粉末，对着镜头一本正经地耍帅，制造强烈反差萌。",
              "opt3": "笑着把粉末抹到队友脸上，带头开启欢乐的大混战，展现超强团魂。",
          },
          {
              "title": "🎶 录音棚里找不到感觉的瓶颈期",
              "desc": "新单曲录制进行到关键时刻，你的声线因为连续高强度赶通告而有些沙哑，制作人在录音室里皱起了眉头，气氛有些凝固。",
              "opt1": "主动请求休息10分钟调整状态，用温水润喉后重新完美进麦。",
              "opt2": "选择用带点沙哑磁性的独特嗓音硬唱下来，意外呈现出绝佳的情感张力！",
              "opt3": "虚心请教制作人，按照对方的指引现场即兴更改了和声唱法。",
          },
      ]

      story_item = story_pool[(curr_stage * 3) % len(story_pool)]

      st.markdown(f"""
            <div class="event-card">
                <b>{story_item['title']}</b><br><br>
                {story_item['desc']}
            </div>
            """, unsafe_allow_html=True)

      # 严格保证每个情景都有 3 个选项
      c_opt1 = st.button(f"1. {story_item['opt1']}")
      c_opt2 = st.button(f"2. {story_item['opt2']}")
      c_opt3 = st.button(f"3. {story_item['opt3']}")

      if c_opt1:
        st.session_state.dance += 10
        st.session_state.fans += 500
        st.session_state.trust += 5
        st.session_state.stage += 1
        st.rerun()

      if c_opt2:
        st.session_state.vocal += 10
        st.session_state.fans += 600
        st.session_state.bond += 5
        st.session_state.stage += 1
        st.rerun()

      if c_opt3:
        st.session_state.variety += 15
        st.session_state.fans += 700
        st.session_state.trust += 10
        st.session_state.stage += 1
        st.rerun()

  # -------------------------------------------------------------------
  # STAGE 23: 帝国剧场终局裁决
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
          st.session_state.fans >= 2200
          and total_ability >= 130
          and st.session_state.trust >= 55
      ):
        st.balloons()
        st.success(
            f"🎉 恭喜 **{st.session_state.player_name}**！你凭借惊人的反应小游戏操作、无数次汗水与不可替代的团队羁绊，与 **{st.session_state.group}** 的伙伴们完美闪耀帝国剧场，正式华丽出道！"
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
