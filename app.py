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
          log_msg="【Stage 1】你吸收了少量颜粉，但社长对
