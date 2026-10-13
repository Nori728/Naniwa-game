import random
import time
import streamlit as st

# 1. 页面基础配置
st.set_page_config(
    page_title="偶像培养计划：星途甄选",
    page_icon="🌟",
    layout="centered",
)

# 2. STARTO / 杰尼斯组合与成员数据（已按年龄严格从大到小排序）
IDOL_GROUPS = {
    "ARASHI (岚)": {
        "members": ["大野智", "樱井翔", "相叶雅纪", "二宫和也", "松本润"]
    },
    "WEST.": {
        "members": [
            "中间淳太",
            "桐山照史",
            "滨田崇裕",
            "重冈大毅",
            "神山智洋",
            "藤井流星",
            "小泷望",
        ]
    },
    "SUPER EIGHT": {
        "members": ["横山裕", "村上信五", "丸山隆平", "安田章大", "大仓忠义"]
    },
    "Snow Man": {
        "members": [
            "深泽辰哉",
            "岩本照",
            "宫馆凉太",
            "渡边翔太",
            "阿部亮平",
            "佐久间大介",
            "向井康二",
            "目黑莲",
            "ラウール",
        ]
    },
    "SixTONES": {
        "members": [
            "高地优吾",
            "京本大我",
            "杰西 (Jesse)",
            "田中树",
            "松村北斗",
            "森本慎太郎",
        ]
    },
    "Aぇ! group (A少年)": {
        "members": [
            "末泽诚也",
            "草间理查德敬太",
            "正门良规",
            "小岛健",
            "佐野晶哉",
        ]
    },
    "浪花男子 (なにわ男子)": {
        "members": [
            "藤原丈一郎",
            "大桥和也",
            "西畑大吾",
            "大西流星",
            "高桥恭平",
            "道枝骏佑",
            "长尾谦杜",
        ]
    },
    "King & Prince": {
        "members": ["岸优太", "平野紫耀", "神宫寺勇太", "永濑廉", "高桥海人"]
    },
    "Travis Japan": {
        "members": [
            "川岛如惠留",
            "七五三挂龙也",
            "吉泽闲也",
            "中村海人",
            "宫近海斗",
            "松仓海斗",
            "松田元太",
        ]
    },
    "KEY TO LIT": {
        "members": ["岩崎大昇", "井上瑞稀", "中村岭亚", "猪狩苍弥", "佐佐木大光"]
    },
    "B&ZAI": {
        "members": [
            "桥本凉",
            "矢花黎",
            "今野大辉",
            "菅田琳宁",
            "本高克树",
            "铃木悠仁",
            "川崎星辉",
            "稻叶通阳",
        ]
    },
    "ACEes": {"members": ["浮所飞贵", "那须雄登", "作间龙斗", "深田龙生", "佐藤龙我"]},
}

# 3. 极简高颜值 UI 设计
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

  st.session_state.dance = random.randint(15, 25)
  st.session_state.vocal = random.randint(15, 25)
  st.session_state.variety = random.randint(15, 25)
  st.session_state.fans = 100
  st.session_state.trust = 40
  st.session_state.logs = []


if "game_started" not in st.session_state:
  init_game()


# 隐藏属性更新辅助函数
def update_hidden_stats(dance=0, vocal=0, variety=0, fans=0, trust=0, log_msg=""):
  if st.session_state.lucky_item == "👟 加厚防滑特制舞鞋" and dance > 0:
    dance += 5
  elif (
      st.session_state.lucky_item == "📖 记满心得的旧笔记本"
      and (vocal > 0 or variety > 0)
  ):
    vocal = int(vocal * 1.3)
    variety = int(variety * 1.3)
  elif st.session_state.lucky_item == "🍲 深夜暖心关东煮" and fans > 0:
    fans = int(fans * 1.25)
  elif st.session_state.lucky_item == "🍀 前辈送的开光御守" and trust < 0:
    trust = int(trust * 0.5)

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
st.title("💖 偶像培养计划：星途甄选")

# 游戏开始后渲染顶部栏
if st.session_state.game_started:
  st.markdown(
      f'<div class="top-dashboard">👑 当前研修生：<b>{st.session_state.member}</b>（所属：{st.session_state.group}） | 🎒 幸运物：{st.session_state.lucky_item}</div>',
      unsafe_allow_html=True,
  )

# -------------------------------------------------------------------
# STAGE 0: 选角与幸运物抽取
# -------------------------------------------------------------------
if not st.session_state.game_started:
  st.markdown(
      '<div class="cute-info">✨ 欢迎来到 STARTO 偶像养成营！请选择你的组合、成员，并抽取开局【幸运物盲盒】！</div>',
      unsafe_allow_html=True,
  )

  col_a, col_b = st.columns(2)
  with col_a:
    selected_group = st.selectbox(
        "选择心仪的偶像组合：", list(IDOL_GROUPS.keys())
    )
  with col_b:
    selected_member = st.selectbox(
        "选择你要扮演的成员：", IDOL_GROUPS[selected_group]["members"]
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
    effect_desc = {
        "🍀 前辈送的开光御守": "被动：遇到负面风波时，社长信任度扣减减半！",
        "👟 加厚防滑特制舞鞋": "被动：每次进行舞蹈练习时，舞蹈属性获得额外爆击！",
        "🍲 深夜暖心关东煮": "被动：在团体与粉丝互动阶段，粉丝增长效率提升 25%！",
        "📖 记满心得的旧笔记本": "被动：歌唱与综艺类事件收益提升 30%！",
    }
    st.success(
        f"✨ 你抽中了：**{st.session_state.temp_lucky}**！\n\n💡 **效果**：{effect_desc[st.session_state.temp_lucky]}"
    )
  else:
    st.info("请点击上方按钮抽取属于你的开局幸运物。")

  st.markdown("---")
  if st.button("🚀 带着祝福，正式开启星途之旅！", use_container_width=True):
    if not st.session_state.temp_lucky:
      st.session_state.temp_lucky = "📖 记满心得的旧笔记本"
    st.session_state.group = selected_group
    st.session_state.member = selected_member
    st.session_state.lucky_item = st.session_state.temp_lucky
    st.session_state.game_started = True
    st.rerun()

# -------------------------------------------------------------------
# 剧情数据大表（共 20 关）
# -------------------------------------------------------------------
STAGES_DATA = {
    1: {
        "title": "🎵 Stage 1：雨后练习室的汗水",
        "desc": "雨后的东京空气潮湿，练习室的镜子蒙上一层雾气。今天老师对基础舞步要求极其严苛，大家训练结束后都瘫坐在地上。",
        "choices": [
            "1. 留下来独自对着镜子把卡壳的动作练习到深夜。",
            "2. 笑着把毛巾分给同期的伙伴，结伴去买冰麦茶。",
            "3. 保持体力，早点回宿舍放松休息。",
        ],
        "effects": [
            (12, 0, 0, 0, 5, "【Stage 1】深夜加练的背影被老师记在心里。"),
            (0, 0, 10, 200, 8, "【Stage 1】温暖贴心的性格让伙伴们倍感依赖。"),
            (0, 0, 5, 50, 0, "【Stage 1】充足的休息让你第二天状态饱满。"),
        ],
    },
    2: {
        "title": "☕ Stage 2：前辈休息室的下午茶",
        "desc": "前辈组合今天在隔壁录音，你带着伴手礼敲门问候。前辈正坐着休息，顺口问起你最近的练习进度。",
        "choices": [
            "1. 虚心请教舞台上如何掌控眼神与表情。",
            "2. 讲了个幽默段子，把休息室的人都逗笑了。",
            "3. 礼貌鞠躬，简单回答“一切顺利，正在努力”。",
        ],
        "effects": [
            (0, 12, 0, 0, 12, "【Stage 2】前辈传授了宝贵的舞台真传。"),
            (0, 0, 15, 300, 8, "【Stage 2】幽默感给前辈留下了深刻印象。"),
            (0, 0, 0, 0, 5, "【Stage 2】礼仪周到，表现稳重。"),
        ],
    },
    3: {
        "title": "⚡ Stage 3：【突发】后台走错休息室！",
        "desc": "在电视台录制节目时，因为走廊太复杂，你不小心推开了一间大牌大咖的休息室！对方正在化妆，气氛瞬间有些凝固！",
        "choices": [
            "1. 立刻深度鞠躬90度，诚恳道歉并奉上自带的小点心。",
            "2. 反应极快地用极度可爱的关西腔搞笑化解尴尬。",
            "3. 倒退着小声说对不起，迅速把门关上跑掉。",
        ],
        "effects": [
            (0, 0, 5, 0, 15, "【Stage 3】高情商道歉化干戈为玉帛。"),
            (0, 0, 18, 500, 5, "【Stage 3】大咖被你逗笑，直夸你有综艺天赋！"),
            (0, 0, 0, 0, -10, "【Stage 3】慌张跑开显得有些失礼。"),
        ],
    },
    4: {
        "title": "📖 Stage 4：《Myojo》杂志小长篇专访",
        "desc": "杂志社来做日常专访，摄影师让你摆一个代表当下心情的姿势，并问你私底下最大的爱好是什么。",
        "choices": [
            "1. “最近一直在研究编曲，希望能写出属于自己的歌。”",
            "2. “喜欢收集奇怪的复古玩具，房间里到处都是。”",
            "3. “最喜欢和成员们一起吃烤肉，聊到深夜。”",
        ],
        "effects": [
            (0, 15, 0, 600, 5, "【Stage 4】才华横溢吸引了大批实力粉。"),
            (0, 0, 15, 500, 5, "【Stage 4】反差萌的爱好让读者觉得有趣。"),
            (0, 0, 10, 400, 10, "【Stage 4】团魂满满的发言极具感染力。"),
        ],
    },
    5: {
        "title": "🍖 Stage 5：深夜烤肉店的交心时刻",
        "desc": "结束密集排练，大家聚在街角的小烤肉店。滋滋作响的肉香中，同伴们开始畅谈对未来的迷茫与憧憬。",
        "choices": [
            "1. “我们一定要一起以这个组合的身份站上巨蛋！”",
            "2. 默默烤好了一整盘肉分给每个人，“快吃吧，辛苦啦。”",
            "3. “以后如果红了，绝对不忘当年分吃炒面的情谊！”",
        ],
        "effects": [
            (0, 0, 5, 800, 15, "【Stage 5】热血宣言让全队凝聚力达到顶峰。"),
            (0, 0, 5, 300, 20, "【Stage 5】体贴入微的举动赢得了极高信赖。"),
            (0, 0, 15, 400, 5, "【Stage 5】调侃让沉重的气氛轻松起来。"),
        ],
    },
    6: {
        "title": "🎭 Stage 6：帝国剧场舞台剧演练",
        "desc": "你获得了参演经典舞台剧（如《DREAM BOYS》）的机会。排练时需要进行高难度的威亚特技和武打动作。",
        "choices": [
            "1. 咬牙克服恐高，反复练习空中翻滚直到完美。",
            "2. 专注于台词念白与眼神爆发力，展现戏剧张力。",
            "3. 休息时主动拉着同台的 Jr. 互相对戏练习。",
        ],
        "effects": [
            (18, 0, 0, 500, 10, "【Stage 6】高难度动作赢得舞台剧导演盛赞。"),
            (0, 15, 0, 400, 10, "【Stage 6】精湛的文戏感染力令人刮目相看。"),
            (8, 8, 0, 300, 15, "【Stage 6】勤奋刻苦成为剧组的楷模。"),
        ],
    },
    7: {
        "title": "⚡ Stage 7：【突发】舞台威亚绳索卡住！",
        "desc": "在彩排飞天威亚时，机械轴承突然卡住，你被悬挂在离地 3 米的半空中！全场工作人员一片惊呼！",
        "choices": [
            "1. 在空中顺势摆出一个超级酷炫的 Superhero 造型并向台下打招呼！",
            "2. 保持镇定，微笑着用美声大声唱了一句名台词镇住全场。",
            "3. 抱紧安全绳，乖乖配合救援人员降落。",
        ],
        "effects": [
            (10, 0, 15, 1000, 10, "【Stage 7】神级临场反应被现场人员传为佳话！"),
            (0, 18, 5, 800, 10, "【Stage 7】镇定自若的歌声展现了强大心理素质。"),
            (0, 0, 0, 0, 5, "【Stage 7】安全降落，表现稳重。"),
        ],
    },
    8: {
        "title": "📻 Stage 8：深夜广播节目个人 Corner",
        "desc": "你在前辈的广播节目里获得了 5 分钟的个人试听 Corner，需要单独面对麦克风与听众交流。",
        "choices": [
            "1. 读了一封听众来信，并给出温柔治愈的人生建议。",
            "2. 模仿了几位前辈和队友的声音，节目效果爆棚。",
            "3. 推荐了自己最近非常喜欢的冷门音乐歌单。",
        ],
        "effects": [
            (0, 5, 10, 700, 10, "【Stage 8】温柔的电台声音俘获了大批深夜听众。"),
            (0, 0, 20, 900, 5, "【Stage 8】爆笑的模仿片段在网络上疯传。"),
            (0, 15, 0, 500, 5, "【Stage 8】独特的音乐品味展现了深厚功底。"),
        ],
    },
    9: {
        "title": "学业与练习的双重压力",
        "desc": "学校即将迎来期末考试，而同时事务所安排了连续两周的密集巡演排练，你感到有些力不从心。",
        "choices": [
            "1. 随身带着课本，在候场和通勤的电车上挤时间复习。",
            "2. 向学校请假，全力以赴投入到巡演练习中。",
            "3. 向组合里的“学霸”成员求助，请他抽空帮你补习。",
        ],
        "effects": [
            (5, 5, 0, 600, 15, "【Stage 9】勤奋兼顾的学霸形象大受好评。"),
            (12, 0, 0, 200, -5, "【Stage 9】舞台表现极佳，但学业稍有落下。"),
            (0, 0, 10, 400, 15, "【Stage 9】队友之间的互助让感情更加紧密。"),
        ],
    },
    10: {
        "title": "🏟️ Stage 10：前辈巨蛋巡演大型 Back 舞者",
        "desc": "东京巨蛋 5 万人的场馆，你们作为后排 Back 舞者出场。巨大的欢呼声震耳欲聋，聚光灯扫过全场。",
        "choices": [
            "1. 将每一个跳跃和转身做到极致精准，展现完美舞姿。",
            "2. 抓住摄像机经过的每一秒，抛出最完美的扇形饭撒（Fanservice）。",
            "3. 眼神时刻关注前辈的位置，完美配合前辈的舞台走位。",
        ],
        "effects": [
            (20, 0, 0, 800, 10, "【Stage 10】扎实的舞蹈功底在巨蛋大屏上清晰可见。"),
            (0, 0, 15, 1500, -5, "【Stage 10】神级饭撒在现场圈粉无数！"),
            (5, 0, 0, 300, 20, "【Stage 10】专业的伴舞修养深受前辈夸奖。"),
        ],
    },
    11: {
        "title": "⚡ Stage 11：【突发】耳返突然断音走调！",
        "desc": "在少俱打歌直播中，你的耳返突然断电，现场伴奏杂乱，随时面临大走音的危险！",
        "choices": [
            "1. 凭肌肉记忆与对音响的感知，全开麦硬扛高音！",
            "2. 冷静地将耳返摘下挂在耳后，与队友对齐节拍。",
            "3. 保持微笑，用口型唱完后半段。",
        ],
        "effects": [
            (0, 22, 0, 1200, 15, "【Stage 11】全开麦硬扛成功！高音震撼全网。"),
            (0, 10, 12, 800, 10, "【Stage 11】冷静自若的台风展现了专业素养。"),
            (0, 0, 5, -200, -10, "【Stage 11】假唱动作被网友捕捉，微有波折。"),
        ],
    },
    12: {
        "title": "📸 Stage 12：私服街拍与网络时尚感",
        "desc": "偶像杂志做了一期“Jr. 私服大公开”的特辑，需要你自己穿着日常私服去摄影棚拍摄。",
        "choices": [
            "1. 穿着自己精心搭配的复古潮牌，展现独特审美。",
            "2. 穿着简单干净的白色 T 恤与牛仔裤，走清爽少年感路线。",
            "3. 戴着搞怪的帽子和墨镜，走夸张个性路线。",
        ],
        "effects": [
            (0, 0, 10, 1000, 5, "【Stage 12】出色的穿搭审美成为了时尚黑马。"),
            (0, 0, 5, 800, 10, "【Stage 12】清爽王道偶像感风靡全网。"),
            (0, 0, 18, 600, 5, "【Stage 12】搞怪穿搭引发粉丝狂热讨论。"),
        ],
    },
    13: {
        "title": "📺 Stage 13：冠名综艺《Jr. 选秀挑战》",
        "desc": "组合迎来了一档网络综艺节目，需要大家在镜头前挑战极其困难的激辛美食吃到饱！",
        "choices": [
            "1. 拼尽全力大口吃完，辣到眼眶通红依然对镜头大喊“美味！”",
            "2. 夸张地做表情包，把被辣到的反应做成绝对的搞笑神场面。",
            "3. 贴心地给被辣到的队友递牛奶，默默照顾大家。",
        ],
        "effects": [
            (0, 0, 15, 900, 15, "【Stage 13】拼搏敬业的态度赢得了制作人的赞赏。"),
            (0, 0, 25, 1500, 5, "【Stage 13】表情包名场面出圈，爆火全网！"),
            (0, 0, 5, 600, 20, "【Stage 13】温柔暖男形象深入人心。"),
        ],
    },
    14: {
        "title": "⚡ Stage 14：【突发】八卦周刊偷拍风波！",
        "desc": "八卦周刊拍到了你深夜与几位男女友人聚会的照片，并撰文暗示有负面嫌疑，网络舆论狂风暴雨！",
        "choices": [
            "1. 连夜向社长诚恳坦白原委，配合公关极速澄清。",
            "2. 在官方博客发长文宣誓“我的爱只属于舞台”，硬刚媒体。",
            "3. 选择冷处理闭麦，等热度自然过去。",
        ],
        "effects": [
            (0, 0, 0, 200, 25, "【Stage 14】坦诚配合让公关极速压制负面。"),
            (0, 0, 10, 2000, -15, "【Stage 14】热血发言成功固粉！但社长稍显担忧。"),
            (0, 0, 0, -1500, -20, "【Stage 14】冷处理导致形象受到小幅受损。"),
        ],
    },
    15: {
        "title": "🎶 Stage 15：自主创作单曲与试听",
        "desc": "事务所给了你们一次机会，可以在 Showcase 上演唱一首由组合成员自己词曲创作的歌曲。",
        "choices": [
            "1. 参与吉他与和声编曲，打造抒情动人的高难度曲目。",
            "2. 负责舞蹈编排，设计一段炸裂的 Dance Break！",
            "3. 撰写 Rap 词，将组合一路走来的汗水与羁绊写进歌词。",
        ],
        "effects": [
            (0, 22, 0, 1000, 10, "【Stage 15】出色的和声编曲展示了音乐才华。"),
            (22, 0, 0, 1000, 10, "【Stage 15】炸裂的编舞成为了舞台的最大亮点。"),
            (0, 10, 15, 1200, 10, "【Stage 15】真挚的 Rap 歌词让全场粉丝落泪。"),
        ],
    },
    16: {
        "title": "🎁 Stage 16：粉丝感谢祭 LIVE",
        "desc": "在小型剧场举办的粉丝感谢祭上，你们需要安排互动环节，近距离感谢一直陪伴你们的 fans。",
        "choices": [
            "1. 为每位到场的粉丝唱一句专属应援词，宠粉拉满。",
            "2. 准备了搞怪的抽奖互动，送出自己亲手画的漫画。",
            "3. 现场表演高难度的全员特技翻滚，用实力回报粉丝。",
        ],
        "effects": [
            (0, 5, 10, 2000, 10, "【Stage 16】极致宠粉让现场变成了幸福的海洋。"),
            (0, 0, 20, 1500, 5, "【Stage 16】亲和力十足的互动广受好评。"),
            (15, 5, 0, 1200, 10, "【Stage 16】硬核实力展现让粉丝大呼过瘾。"),
        ],
    },
    17: {
        "title": "⚡ Stage 17：【突发】同伴临演前突发高烧！",
        "desc": "全国巡演首日开演前 1 小时，组合的核心主唱突然高烧倒下无法登台！他的唱歌和舞蹈段落空了出来！",
        "choices": [
            "1. 挺身而出，在 30 分钟内硬记下他的高音段落，替他全开麦主唱！",
            "2. 协助舞蹈队长重新调整全队的走位，确保舞台视觉不空缺。",
            "3. 在后台无微不至地照顾生病的同伴，安抚他的情绪。",
        ],
        "effects": [
            (0, 25, 0, 1800, 20, "【Stage 17】救场如救火！神级主唱救场震撼全场！"),
            (18, 0, 5, 1200, 20, "【Stage 17】出色的团队大局观得到了高层极高评价。"),
            (0, 0, 5, 500, 25, "【Stage 17】真挚的兄弟情谊让团队无后顾之忧。"),
        ],
    },
    18: {
        "title": "🌟 Stage 18：全国巡演千秋乐（最终场）",
        "desc": "全国巡演迎来的最后一站千秋乐，全场一片粉色应援灯海。舞台上大家都流下了激动的泪水。",
        "choices": [
            "1. 对着全场万名粉丝大喊：“谢谢你们带我们看到这么美的景色！”",
            "2. 与组合成员们紧紧拥抱在一起，围成一圈大喊加油。",
            "3. 用最完美的清唱为整场演唱会画上圆满句号。",
        ],
        "effects": [
            (0, 0, 10, 2500, 15, "【Stage 18】绝美千秋乐发言登上各大新闻头条。"),
            (0, 0, 5, 1800, 25, "【Stage 18】坚不可摧的团魂征服了现场所有人。"),
            (0, 20, 0, 2000, 15, "【Stage 18】完美的唱功为巡演写下了传奇篇章。"),
        ],
    },
    19: {
        "title": "🌙 Stage 19：出道前夜的宿舍深夜聊",
        "desc": "明早就是帝国剧场出道大决选的发布会。深夜的宿舍里没人睡得着，大家围坐在客厅地板上看着刚入所时的照片。",
        "choices": [
            "1. “不管明天结果如何，能和你们组团是我这辈子最幸运的事。”",
            "2. 拿起床头的吉他，轻声弹起大家入所第一天学的那首歌。",
            "3. 笑着用搞怪的语气打破沉重：“明天谁要是哭出来，谁就请吃一年的烤肉！”",
        ],
        "effects": [
            (0, 0, 5, 1000, 25, "【Stage 19】真挚的告白让所有人心头一暖。"),
            (0, 15, 0, 1200, 20, "【Stage 19】动人的琴声伴随着大家进入梦乡。"),
            (0, 0, 20, 800, 15, "【Stage 19】欢声笑语驱散了出道前的所有焦虑。"),
        ],
    },
    20: {
        "title": "🏆 Stage 20：帝国剧场 CD 出道决选（终局裁决）",
        "desc": "帝国剧场金碧辉煌，全日本数百家媒体的闪光灯闪烁。社长坐在话筒前，即将宣读今年正式获得 **CD 出道** 资格的最终名单！",
        "choices": [
            "🌟 挺直脊梁，怀揣这段时间的汗水与羁绊，走向聚光灯！",
        ],
        "effects": [],
    },
}


# -------------------------------------------------------------------
# 游戏主流程
# -------------------------------------------------------------------
if st.session_state.game_started:
  curr_stage = st.session_state.stage

  if curr_stage in STAGES_DATA and curr_stage < 20:
    stage_info = STAGES_DATA[curr_stage]
    st.subheader(f"📍 {stage_info['title']}")

    st.markdown(f"""
        <div class="event-card">
            <div class="event-title">📌 【剧情与抉择】</div>
            {stage_info['desc']}
        </div>
        """, unsafe_allow_html=True)

    choice = st.radio(
        "请做出你的抉择：", stage_info["choices"], key=f"s{curr_stage}"
    )

    if st.button("确认选择，进入下一阶段 ➔", use_container_width=True):
      idx = 0
      if "2." in choice:
        idx = 1
      elif "3." in choice:
        idx = 2

      d, v, va, f, t, log = stage_info["effects"][idx]
      update_hidden_stats(
          dance=d, vocal=v, variety=va, fans=f, trust=t, log_msg=log
      )

      st.session_state.stage += 1
      st.rerun()

  # -------------------------------------------------------------------
  # STAGE 20: 终局出道大决选
  # -------------------------------------------------------------------
  elif curr_stage == 20:
    stage_info = STAGES_DATA[20]
    st.subheader(f"🏁 {stage_info['title']}")

    st.markdown(f"""
        <div class="event-card">
            <div class="event-title">✨ 【命运的终章】</div>
            {stage_info['desc']}
        </div>
        """, unsafe_allow_html=True)

    if st.button("🌟 揭晓最终出道结果与终局能力档案 🌟", use_container_width=True):
      st.markdown("---")

      total_ability = (
          st.session_state.dance
          + st.session_state.vocal
          + st.session_state.variety
      )
      trust = st.session_state.trust
      fans = st.session_state.fans

      if trust < 25:
        st.error("💀 【最终结局：遗憾离场 / 另谋出路】")
        st.write(
            f"很遗憾，{st.session_state.member}。"
            f"由于社长信任度未达要求（{trust}），你与组合在出道前夕擦肩而过，选择走向了不同的道路。"
        )
      elif fans >= 12000 and total_ability >= 220 and trust >= 65:
        st.balloons()
        st.success("🎉 【最终结局：传奇顶流 - 百万销量 CD 华丽出道！】")
        st.markdown(
            f"### 👑 恭喜 {st.session_state.group} 的 **{st.session_state.member}**！\n"
            f"携带幸运物【{st.session_state.lucky_item}】的你，在长期的汗水、泪水与同伴羁绊中脱颖而出！"
            "社长在发布会上亲手递出了 CD 出道金标签！出道单曲空降各大榜单首位，你正式登上了日本娱乐圈新一代巨星顶峰！"
        )
      elif fans >= 6000 and trust >= 45:
        st.success("✨ 【最终结局：闪耀登场 - 顺利 CD 出道！】")
        st.markdown(
            f"### 👏 恭喜 {st.session_state.group} 的 **{st.session_state.member}**！\n"
            "经过不懈的努力与多次危机的化解，社长最终为你敲定了 CD 出道企划！你成功跨越 Jr. 阶段，正式踏上主流明星舞台！"
        )
      else:
        st.warning("⚠️ 【最终结局：稳扎稳打 - 剧场与舞台核心骨干】")
        st.write(
            f"很可惜，{st.session_state.member}。"
            "虽然你拥有非常温暖的日常和不错的同伴基础，但综合爆发力距离正式 CD 出道还有一小步。"
            "社长决定让你继续作为组合的中坚力量深耕舞台，未来可期！"
        )

      st.markdown("---")
      st.markdown("### 📊 你的星途能力终极档案")
      st.write(
          f"- 💃 舞蹈能力：**{st.session_state.dance} pt** | 🎤 歌唱能力：**{st.session_state.vocal} pt** | 🤡 综艺表现：**{st.session_state.variety} pt**"
      )
      st.write(f"- 🤝 社长信任度：**{trust} / 100**")
      st.write(f"- 💖 累积粉丝总数：**{fans:,} 人**")
      st.write(f"- 🎒 开局幸运物：**{st.session_state.lucky_item}**")

      st.markdown("#### 📖 你的星途手记完整回顾：")
      for log in st.session_state.logs:
        st.caption(f"• {log}")

      st.write("")
      if st.button("🎮 开启新的偶像人生"):
        init_game()
        st.rerun()
