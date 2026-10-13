import time
import streamlit as st

# 页面基础设置
st.set_page_config(
    page_title="偶像培养计划：星途甄选", page_icon="🌟", layout="centered"
)

# 杰尼斯经典组合与成员数据
IDOL_GROUPS = {
    "Snow Man": [
        "岩本照",
        "深泽辰哉",
        "ラウール",
        "渡边翔太",
        "向井康二",
        "阿部亮平",
        "目黑莲",
        "宫馆凉太",
        "佐久间大介",
    ],
    "SixTONES": [
        "高地优吾",
        "京本大我",
        "田中树",
        "松村北斗",
        "杰西 (Jesse)",
        "森本慎太郎",
    ],
    "なにわ男子 (浪花男子)": [
        "西畑大吾",
        "大西流星",
        "道枝骏佑",
        "高桥恭平",
        "长尾谦杜",
        "藤原丈一郎",
        "大桥和也",
    ],
    "King & Prince": ["平野紫耀", "永濑廉", "高桥海人", "岸优太", "神宫寺勇太"],
    "Travis Japan": [
        "宫近海斗",
        "中村海人",
        "七五三挂龙也",
        "川岛如惠留",
        "吉泽闲也",
        "松田元太",
        "松仓海斗",
    ],
}

# 自定义 CSS 样式
st.markdown(
    """
    <style>
    .stat-box {
        background-color: #1e1e2f;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3a3a5a;
        margin-bottom: 10px;
    }
    .event-card {
        background-color: #262638;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        margin: 15px 0;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# 初始化游戏状态
def init_game():
  st.session_state.game_started = False
  st.session_state.stage = 1
  st.session_state.group = ""
  st.session_state.member = ""
  st.session_state.dance = 50
  st.session_state.vocal = 50
  st.session_state.variety = 50
  st.session_state.fans = 1000
  st.session_state.trust = 50
  st.session_state.logs = []


if "game_started" not in st.session_state:
  init_game()


# 属性更新辅助函数
def update_stats(dance=0, vocal=0, variety=0, fans=0, trust=0, log_msg=""):
  st.session_state.dance += dance
  st.session_state.vocal += vocal
  st.session_state.variety += variety
  st.session_state.fans += fans
  st.session_state.trust += trust

  # 限制范围
  st.session_state.trust = max(0, min(100, st.session_state.trust))
  st.session_state.fans = max(0, st.session_state.fans)

  if log_msg:
    st.session_state.logs.append(log_msg)


st.title("🌟 偶像培养计划：星途甄选")
st.caption("从 Jr. 研修生到帝国剧场 CD 出道！凭你的选择征服舞台吧。")

# 侧边栏：玩家当前属性面板
if st.session_state.game_started:
  st.sidebar.header(
      f"👤 {st.session_state.group} - {st.session_state.member}"
  )
  st.sidebar.markdown("---")
  st.sidebar.metric("💃 舞蹈 (Dance)", st.session_state.dance)
  st.sidebar.metric("🎤 歌唱 (Vocal)", st.session_state.vocal)
  st.sidebar.metric("🤡 综艺感 (Variety)", st.session_state.variety)
  st.sidebar.metric("📈 粉丝数量", f"{st.session_state.fans:,} 人")
  st.sidebar.metric("🤝 社长信任度", f"{st.session_state.trust} / 100")

  if st.sidebar.button("🔄 重新开始游戏"):
    init_game()
    st.rerun()

# -------------------------------------------------------------------
# 阶段 0：选角界面
# -------------------------------------------------------------------
if not st.session_state.game_started:
  st.subheader("📋 第一步：选择你的偶像身份")

  selected_group = st.selectbox("选择你想加入的组合：", list(IDOL_GROUPS.keys()))
  selected_member = st.selectbox(
      "选择你要扮演的成员：", IDOL_GROUPS[selected_group]
  )

  st.info(
      f"你选择了 **{selected_group}** 的 **{selected_member}**！"
      "你将以 Jr. 身份进入事务所，接受严苛的甄选。"
  )

  if st.button("🚀 开启偶像生涯", use_container_width=True):
    st.session_state.group = selected_group
    st.session_state.member = selected_member
    st.session_state.game_started = True
    st.rerun()

# -------------------------------------------------------------------
# 阶段 1：Jr. 研修期 (搬梯子与 Back 舞者)
# -------------------------------------------------------------------
elif st.session_state.stage == 1:
  st.markdown("### 🚩 第一阶段：Jr. 研修期 — 舞台 Back 与练习室")
  st.write(
      "你刚进入事务所，每天需要为前辈的演唱会伴舞（Back），同时在练习室进行魔鬼训练。"
  )

  st.markdown("""
    <div class="event-card">
    <b>【考核事件】</b><br>
    前辈演唱会即将来临，舞蹈编排非常复杂，而且社长（Johnny）正在台下巡视！你打算怎么做？
    </div>
    """, unsafe_allow_html=True)

  q1 = st.radio(
      "你的选择：",
      [
          "A. 拼命练舞，甚至通宵留在练习室加练（舞蹈+15，信任度+10）",
          "B. 舞蹈中规中矩，但主动帮前辈搬道具、递水（综艺+10，信任度+15）",
          "C. 偷懒划水，靠颜值站在后排比心吸引粉丝（粉丝+2000，信任度-15，舞蹈-5）",
      ],
  )

  if st.button("确认选择，进入下一阶段"):
    if "A." in q1:
      update_stats(
          dance=15, trust=10, log_msg="【Stage 1】你的硬核舞姿得到了社长的赞赏！"
      )
    elif "B." in q1:
      update_stats(
          variety=10,
          trust=15,
          log_msg="【Stage 1】前辈觉得你非常有礼貌，向社长推荐了你。",
      )
    else:
      update_stats(
          fans=2000,
          trust=-15,
          dance=-5,
          log_msg="【Stage 1】你吸收了少量颜粉，但社长对你的态度表示不满！",
      )

    st.session_state.stage = 2
    st.rerun()

# -------------------------------------------------------------------
# 阶段 2：少俱舞台与镜头争夺
# -------------------------------------------------------------------
elif st.session_state.stage == 2:
  st.markdown("### 🚩 第二阶段：《ザ少年倶楽部》电视录制")
  st.write("你获得了登上《少俱》表演的珍贵机会！这是吸引全国粉丝的关键。")

  st.markdown("""
    <div class="event-card">
    <b>【突发状况】</b><br>
    演唱过程中，你的麦克风突然断音了！而镜头正切到你的独唱特写，你会：
    </div>
    """, unsafe_allow_html=True)

  q2 = st.radio(
      "你的选择：",
      [
          "A. 丝滑切换为超炫酷的 Dance Break 舞蹈独秀（需 Dance≥60 | 成功：粉丝+5000；失败：粉丝-2000）",
          "B. 临危不乱，大声无伴奏清唱，展示极致唱功（需 Vocal≥60 | 成功：粉丝+5000，歌唱+10；失败：粉丝-2000）",
          "C. 对着镜头做一个极其有魅力的 wink 并搞怪笑场（综艺+15，粉丝+3000）",
      ],
  )

  if st.button("确认提交演出"):
    if "A." in q2:
      if st.session_state.dance >= 60:
        update_stats(
            fans=5000,
            log_msg="【Stage 2】舞技惊艳全场，少俱名场面诞生！粉丝大幅增加。",
        )
      else:
        update_stats(
            fans=-2000, log_msg="【Stage 2】舞蹈编排失误，显得有些手足无措。"
        )
    elif "B." in q2:
      if st.session_state.vocal >= 60:
        update_stats(
            fans=5000,
            vocal=10,
            log_msg="【Stage 2】绝美清唱震撼全场，成功吸粉！",
        )
      else:
        update_stats(
            fans=-2000, log_msg="【Stage 2】清唱破音，引发了网上的讨论。"
        )
    else:
      update_stats(
          variety=15,
          fans=3000,
          log_msg="【Stage 2】绝佳的综艺应变能力，圈粉无数！",
      )

    st.session_state.stage = 3
    st.rerun()

# -------------------------------------------------------------------
# 阶段 3：Jr. 祭全国巡演与偶像修养
# -------------------------------------------------------------------
elif st.session_state.stage == 3:
  st.markdown("### 🚩 第三阶段：全国巡演与偶像危机")
  st.write("组合名气大增，你们举办了 Jr. 祭全国巡演。但随之而来的还有狗仔队的关注。")

  st.markdown("""
    <div class="event-card">
    <b>【危机事件】</b><br>
    巡演结束后，有狗仔拍到你与异性朋友聚会。社长连夜找你谈话，你打算怎么处理？
    </div>
    """, unsafe_allow_html=True)

  q3 = st.radio(
      "你的选择：",
      [
          "A. 诚恳道歉，保证以后全心投入偶像事业（信任度+20，粉丝-1000）",
          "B. 坚决否认，并在博客发长文宣誓“我只属于舞台和粉丝”（粉丝+6000，信任度-15）",
          "C. 顶撞社长：“偶像也是普通人！”（信任度-35，粉丝-5000）",
      ],
  )

  if st.button("做出抉择"):
    if "A." in q3:
      update_stats(
          trust=20,
          fans=-1000,
          log_msg="【Stage 3】社长认可了你的职业态度，危机化解。",
      )
    elif "B." in q3:
      update_stats(
          fans=6000,
          trust=-15,
          log_msg="【Stage 3】粉丝极其感动，但事务所对你的控制力表示担忧。",
      )
    else:
      update_stats(
          trust=-35,
          fans=-5000,
          log_msg="【Stage 3】你激怒了高层，陷入解约危机！",
      )

    st.session_state.stage = 4
    st.rerun()

# -------------------------------------------------------------------
# 阶段 4：帝国剧场 CD 出道决选 (判定)
# -------------------------------------------------------------------
elif st.session_state.stage == 4:
  st.markdown("### 🏆 第四阶段：帝国剧场 — CD 出道大决选")
  st.write(
      "社长将在帝国剧场的记者招待会上，正式宣布今年获得 **CD 出道** 资格的组合与个人！"
  )

  if st.button("🎉 开启出道判定结果！", use_container_width=True):
    st.markdown("---")
    # 计算综合综合实力得分
    total_score = (
        st.session_state.dance
        + st.session_state.vocal
        + st.session_state.variety
    )
    trust = st.session_state.trust
    fans = st.session_state.fans

    # 判定逻辑
    if trust < 30:
      st.error("❌ 【甄选结果：解约退所】")
      st.write(
          f"很遗憾，{st.session_state.member}。由于信任度过低（{trust}），你未能在事务所立足，最终选择了退所。"
      )
    elif fans >= 12000 and total_score >= 180 and trust >= 60:
      st.balloons()
      st.success("🎉 【甄选结果：传说级 CD 出道！】")
      st.write(
          f"恭喜 **{st.session_state.group}** 的 **{st.session_state.member}**！"
          "你凭借无可挑剔的舞台实力、庞大的粉丝群体与极高的敬业度，成功拿下百万销量 CD 出道资格！"
      )
    elif fans >= 8000 and trust >= 40:
      st.success("✨ 【甄选结果：顺利 CD 出道！】")
      st.write(
          f"恭喜 **{st.session_state.group}** 的 **{st.session_state.member}**！"
          "社长为你敲定了出道单曲，你正式晋升为全职明星！"
      )
    else:
      st.warning("⚠️ 【甄选结果：继续保持 Jr. 状态】")
      st.write(
          f"很可惜，{st.session_state.member}。"
          "你的综合数值尚未达到出道要求，社长决定让你继续作为 Jr. 队长带新人，等待下一次机会。"
      )

    # 显示成长日志
    st.markdown("### 📜 你的星途历程")
    for log in st.session_state.logs:
      st.write(f"- {log}")

    if st.button("🎮 再玩一次"):
      init_game()
      st.rerun()
