import random
import time
import streamlit as st
import streamlit.components.v1 as components

# 1. 页面基础配置
st.set_page_config(
    page_title="星途闪耀：我的练习生日常",
    page_icon="🌟",
    layout="centered",
)

# 2. 团队与成员数据（按年龄从大到小严格排序）
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

# 3. 页面样式
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


# 4. 初始化数据
def init_game():
  st.session_state.game_started = False
  st.session_state.stage = 1
  st.session_state.player_name = ""
  st.session_state.group = ""
  st.session_state.lucky_item = ""

  st.session_state.energy = 100
  st.session_state.dance = 20
  st.session_state.vocal = 20
  st.session_state.variety = 20
  st.session_state.fans = 100
  st.session_state.trust = 50
  st.session_state.bond = 10


if "game_started" not in st.session_state:
  init_game()


def get_rand_member():
  members = IDOL_GROUPS.get(st.session_state.group, ["前辈"])
  return random.choice(members)


# 极速指针摆动小游戏渲染器
def render_pointer_minigame(speed=3, target_start=40, target_width=20):
  html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: system-ui, sans-serif;
                background-color: transparent;
                margin: 0;
                padding: 10px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            .game-container {{
                background: #2d1b4e;
                border: 3px solid #ff80ab;
                border-radius: 16px;
                padding: 20px;
                width: 90%;
                max-width: 400px;
                text-align: center;
                box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            }}
            .bar-bg {{
                position: relative;
                width: 100%;
                height: 36px;
                background: #1a0f30;
                border-radius: 18px;
                overflow: hidden;
                border: 2px solid #ea80fc;
                margin: 15px 0;
            }}
            .target-zone {{
                position: absolute;
                left: {target_start}%;
                width: {target_width}%;
                height: 100%;
                background: linear-gradient(90deg, #00e676, #b9f6ca, #00e676);
                box-shadow: 0 0 10px #00e676;
            }}
            .pointer {{
                position: absolute;
                top: 0;
                left: 0%;
                width: 6px;
                height: 100%;
                background-color: #ffeb3b;
                box-shadow: 0 0 12px #ffeb3b;
                transition: transform 0.016s linear;
            }}
            .hit-btn {{
                background: linear-gradient(45deg, #ff4081, #ab47bc);
                color: white;
                border: none;
                padding: 14px 32px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 25px;
                cursor: pointer;
                box-shadow: 0 5px 15px rgba(255, 64, 129, 0.4);
                touch-action: manipulation;
                width: 100%;
                margin-top: 10px;
            }}
            #result-msg {{
                color: #ffeb3b;
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
                min-height: 24px;
            }}
        </style>
    </head>
    <body>
        <div class="game-container">
            <div style="color: #ffffff; font-weight: bold; font-size: 15px;">🎯 看准时机！在指针进入【绿色判定区】时击打！</div>
            <div class="bar-bg">
                <div class="target-zone"></div>
                <div class="pointer" id="pointer"></div>
            </div>
            <div id="result-msg">⏱️ 指针高速摆动中...</div>
            <button class="hit-btn" id="stopBtn" onclick="stopPointer()">🔥 就是现在！看准按下！</button>
        </div>
        <script>
            let pos = 0;
            let dir = 1;
            let speed = {speed};
            let isStopped = false;
            let animId;
            const pointer = document.getElementById('pointer');
            const resultMsg = document.getElementById('result-msg');
            const targetStart = {target_start};
            const targetEnd = {target_start} + {target_width};

            function updatePointer() {{
                if (isStopped) return;
                pos += dir * speed;
                if (pos >= 98) {{ pos = 98; dir = -1; }}
                if (pos <= 0) {{ pos = 0; dir = 1; }}
                pointer.style.left = pos + '%';
                animId = requestAnimationFrame(updatePointer);
            }}

            function stopPointer() {{
                if (isStopped) return;
                isStopped = true;
                cancelAnimationFrame(animId);
                if (pos >= targetStart && pos <= targetEnd) {{
                    resultMsg.innerHTML = "🎉 PERFECT! 完美命中目标点！";
                    resultMsg.style.color = "#00e676";
                }} else {{
                    resultMsg.innerHTML = "⚠️ GREAT! 成功完成挑战！";
                    resultMsg.style.color = "#ffeb3b";
                }}
                document.getElementById('stopBtn').disabled = true;
                document.getElementById('stopBtn').style.opacity = '0.6';
            }}
            updatePointer();
        </script>
    </body>
    </html>
    """
  components.html(html_code, height=210)


# 真正能在屏幕上点、小人会动、躲避坠落障碍的【舞台跳格子躲避画布小游戏】
def render_dodge_canvas_game():
  html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                background: transparent;
                margin: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                font-family: system-ui, sans-serif;
            }
            .canvas-box {
                background: #1a0f30;
                border: 3px solid #ff80ab;
                border-radius: 16px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.3);
                position: relative;
                overflow: hidden;
                width: 320px;
                height: 200px;
            }
            canvas {
                display: block;
            }
            .ctrl-panel {
                display: flex;
                gap: 15px;
                margin-top: 12px;
                width: 320px;
                justify-content: center;
            }
            .move-btn {
                background: linear-gradient(45deg, #ff4081, #ab47bc);
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 20px;
                cursor: pointer;
                box-shadow: 0 4px 10px rgba(255, 64, 129, 0.4);
                touch-action: manipulation;
                flex: 1;
            }
            .move-btn:active {
                transform: scale(0.95);
            }
            #info-tip {
                color: #4a148c;
                font-weight: bold;
                font-size: 14px;
                margin-top: 8px;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="canvas-box">
            <canvas id="dodgeCanvas" width="320" height="200"></canvas>
        </div>
        <div class="ctrl-panel">
            <button class="move-btn" onclick="movePlayer(-1)">⬅️ 往左闪避</button>
            <button class="move-btn" onclick="movePlayer(1)">往右闪避 ➡️</button>
        </div>
        <div id="info-tip">⚡ 躲避坠落的舞台灯光！坚持 10 秒即为胜利！</div>

        <script>
            const canvas = document.getElementById('dodgeCanvas');
            const ctx = canvas.getContext('2d');

            // 玩家位置：3个跑道 (0: 左, 1: 中, 2: 右)
            let lane = 1;
            const lanesX = [60, 160, 260];
            let playerY = 165;
            
            // 障碍物数组
            let obstacles = [];
            let score = 0;
            let isGameOver = false;
            let gameInterval;
            let obstacleTimer;

            function movePlayer(dir) {
                if (isGameOver) return;
                lane += dir;
                if (lane < 0) lane = 0;
                if (lane > 2) lane = 2;
            }

            // 键盘左右键支持
            window.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowLeft') movePlayer(-1);
                if (e.key === 'ArrowRight') movePlayer(1);
            });

            function spawnObstacle() {
                if (isGameOver) return;
                let randomLane = Math.floor(Math.random() * 3);
                obstacles.push({ lane: randomLane, y: -20, speed: 3.5 });
            }

            function updateGame() {
                ctx.clearRect(0, 0, 320, 200);

                // 绘制舞台跑道线
                ctx.strokeStyle = '#2d1b4e';
                ctx.lineWidth = 2;
                ctx.setLineDash([4, 4]);
                [110, 210].forEach(x => {
                    ctx.beginPath();
                    ctx.moveTo(x, 0);
                    ctx.lineTo(x, 200);
                    ctx.stroke();
                });
                ctx.setLineDash([]);

                // 更新与绘制障碍物（坠落灯光）
                for (let i = obstacles.length - 1; i >= 0; i--) {
                    let obs = obstacles[i];
                    obs.y += obs.speed;
                    
                    // 绘制坠落的舞台灯光/道具
                    ctx.fillStyle = '#ff5252';
                    ctx.beginPath();
                    ctx.arc(lanesX[obs.lane], obs.y, 12, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.fillStyle = '#ffffff';
                    ctx.font = '10px Arial';
                    ctx.fillText('💡', lanesX[obs.lane] - 6, obs.y + 4);

                    // 碰撞检测
                    if (obs.y >= playerY - 15 && obs.y <= playerY + 15 && obs.lane === lane) {
                        isGameOver = true;
                        document.getElementById('info-tip').innerHTML = "💥 哎呀被砸中了！不过有惊无险顺利过关！";
                        document.getElementById('info-tip').style.color = "#d32f2f";
                    }

                    // 移除超出屏幕的障碍
                    if (obs.y > 220) {
                        obstacles.splice(i, 1);
                        score += 10;
                    }
                }

                // 绘制可爱的偶像小人
                let px = lanesX[lane];
                ctx.fillStyle = '#ff4081';
                ctx.beginPath();
                ctx.arc(px, playerY, 14, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#ffffff';
                ctx.font = '12px Arial';
                ctx.fillText('⭐', px - 6, playerY + 4);

                // 绘制分数
                ctx.fillStyle = '#ffffff';
                ctx.font = '12px Arial';
                ctx.fillText("得分: " + score, 15, 20);

                if (!isGameOver) {
                    requestAnimationFrame(updateGame);
                } else {
                    ctx.fillStyle = 'rgba(0,0,0,0.6)';
                    ctx.fillRect(0, 0, 320, 200);
                    ctx.fillStyle = '#00e676';
                    ctx.font = 'bold 18px Arial';
                    ctx.fillText("🎉 成功闪避挑战完成！", 60, 105);
                }
            }

            obstacleTimer = setInterval(spawnObstacle, 900);
            updateGame();
        </script>
    </body>
    </html>
    """
  components.html(html_code, height=270)


# 核心海量剧情库
def get_story_database(player_name, member, group):
  return {
      1: {
          "title": "🎵 Stage 1：雨后练习室的汗水",
          "desc": f"雨后的东京空气潮湿，练习室镜子蒙上一层雾气。今天基础舞步极严，{member} 擦着汗过来：“{player_name}，刚才转身重心偏了，要不要再试一次？”",
          "opt1": "虚心请教，并独留练习室对着镜子练到深夜。",
          "opt2": "笑着递上买好的冰麦茶，和大家结伴回宿舍聊天。",
          "opt3": "谢过前辈，早点回宿舍休息保持第二天体能。",
      },
      2: {
          "title": "📺 Stage 2：【外务】地方电视台深夜综艺外景",
          "desc": "你获得了第一次地方电视台的节目外景外务！拍摄过程中，主持人突然把你拉到最前面要求你做 3 秒钟的个人介绍与放电！",
          "opt1": "毫不犹豫抛出准备好的爆笑段子与搞笑表情包！",
          "opt2": "落落大方展示一段极具反差感的美声开嗓。",
          "opt3": "面对镜头做出招牌甜美 Wink，展现王道偶像魅力。",
      },
      4: {
          "title": "☕ Stage 4：前辈休息室的冷不防考问",
          "desc": f"在电视台走廊偶遇前辈组合，前辈看了看你们最近的排练表现，笑着问：“{player_name}，你觉得在 {group} 里，你不可替代的闪光点是什么？”",
          "opt1": "“是永不服输的舞蹈干劲，绝对不给组合拉胯！”",
          "opt2": "“是调节气氛的能力，有我在休息室永远充满欢笑！”",
          "opt3": "“是对音乐的执着，希望能写出属于我们的歌曲！”",
      },
      5: {
          "title": "📖 Stage 5：《Myojo》偶像杂志个人专访",
          "desc": "杂志社来做日常专访，摄影师问你私底下和团里谁关系最好、最近最沉迷的爱好是什么。",
          "opt1": f"“最近一直在和 {member} 一起研究吉他与编曲。”",
          "opt2": "“喜欢收集奇怪的复古玩具，房间里到处都是。”",
          "opt3": "“最喜欢和大家一起吃烤肉，聊到深夜也很开心。”",
      },
      7: {
          "title": "📻 Stage 7：【外务】深夜广播节目连线",
          "desc": "你在前辈的广播节目里获得了 5 分钟的个人试听 Corner，需要单独面对麦克风与全日本听众交流！",
          "opt1": "读了一封听众来信，给出温柔治愈的人生建议。",
          "opt2": "模仿了几位队友和社长说话的声音，节目效果爆棚。",
          "opt3": "推荐了自己私藏的音乐歌单，展示深厚审美。",
      },
      8: {
          "title": "🍖 Stage 8：深夜烤肉店的交心时刻",
          "desc": f"结束密集排练，你和大家聚在街角的小烤肉店。滋滋作响的肉香中，{member} 谈起了对未来的迷茫与憧憬。",
          "opt1": "“我们一定要一起以这个组合的身份站上巨蛋！”",
          "opt2": "默默烤好一整盘肉分给大家：“快吃吧，大家辛苦啦。”",
          "opt3": "用调侃的语气打破沉重：“以后红了可别忘了吃烤肉的情谊！”",
      },
      10: {
          "title": "⚡ Stage 10：【突发外务】知名潮牌私服街拍",
          "desc": "时尚杂志做了一期“Jr. 练习生私服大公开”特辑，需要你穿着自己的日常私服去摄影棚拍摄大片！",
          "opt1": "穿着自己精心搭配的复古潮牌，展现独特审美。",
          "opt2": "穿着简单干净的白 T 恤与牛仔裤，走清爽少年感。",
          "opt3": "戴着搞怪墨镜与帽子，走夸张极具个性的路线。",
      },
      11: {
          "title": "🎭 Stage 11：帝国剧场舞台剧演练",
          "desc": "你获得了参演经典舞台剧的机会。排练时需要进行高难度的威亚特技和武打动作，导演要求极高！",
          "opt1": "咬牙克服恐高，反复练习空中翻滚直到完美。",
          "opt2": "专注于台词念白与眼神爆发力，展现戏剧张力。",
          "opt3": "休息时主动拉着同台的伙伴互相对戏练习。",
      },
      13: {
          "title": "⚡ Stage 13：【突发危机】八卦周刊跟拍偷拍！",
          "desc": "八卦周刊拍到了你深夜与几位友人聚会的照片，并撰文暗示有负面嫌疑，网络舆论一时间沸沸扬扬！",
          "opt1": "连夜向社长诚恳坦白原委，配合公关极速澄清。",
          "opt2": "在官方博客发长文宣誓“我的爱只属于舞台”硬刚。",
          "opt3": "保持冷静沉稳，用接下来的完美舞台回应质疑。",
      },
      14: {
          "title": "🎶 Stage 14：【外务】音乐节 Showcase 自创曲唱跳",
          "desc": "事务所给了一次机会，可以在音乐节上演唱一首由你们自己词曲创作的新歌！",
          "opt1": "参与吉他与和声编曲，打造抒情动人的高难度曲目。",
          "opt2": "负责舞蹈编排，设计一段炸裂的 Dance Break！",
          "opt3": "撰写 Rap 词，将大家一路走来的汗水与羁绊写进歌里。",
      },
      16: {
          "title": "⚡ Stage 16：【突发】同伴临演前突发高烧！",
          "desc": f"巡演首日开演前 1 小时，核心成员 {member} 突然高烧倒下无法登台！他的唱歌和舞蹈段落瞬间空了出来！",
          "opt1": "挺身而出，在 30 分钟内硬记下他的高音段落替他主唱！",
          "opt2": "协助队长重新调整全队的走位，确保舞台视觉不空缺。",
          "opt3": "在后台无微不至照顾生病的同伴，安抚他的情绪。",
      },
      17: {
          "title": "🎁 Stage 17：粉丝感谢祭 LIVE 近距离互动",
          "desc": "在小型剧场举办的粉丝感谢祭上，你需要安排互动环节，近距离感谢一直陪伴你们的粉丝。",
          "opt1": "为每位到场粉丝唱专属应援词，极致宠粉拉满。",
          "opt2": "准备了搞怪的抽奖互动，送出自己画的漫画。",
          "opt3": "现场表演高难度全员特技翻滚，用实力回报粉丝。",
      },
      19: {
          "title": "🌙 Stage 19：出道前夜的夜谈",
          "desc": "明早就是帝国剧场出道大决选的发布会。深夜宿舍里没人睡得着，大家围坐在客厅地板上看着入所第一天的照片。",
          "opt1": "“能和大家组团是我这辈子最幸运的事。”",
          "opt2": "拿起来床头的吉他，轻声弹起大家入所第一天学的那首歌。",
          "opt3": "笑着用搞怪语气打破沉重：“明天谁要是哭出来，谁请吃烤肉！”",
      },
  }


# 主标题
st.title("💖 星途闪耀：我的练习生日常")

# -------------------------------------------------------------------
# STAGE 0: 开局
# -------------------------------------------------------------------
if not st.session_state.game_started:
  st.markdown(
      '<div class="cute-info">✨ 欢迎来到 STARTO 偶像养成营！请输入你的名字，选择心仪组合并抽取开局幸运物！</div>',
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
  st.subheader("🎁 抽开局幸运物扭蛋")

  if "temp_gacha" not in st.session_state:
    st.session_state.temp_gacha = ""

  if st.button("🎲 点击抽取开局幸运物！"):
    gacha_pool = [
        "🍀 前辈送的开光御守（遇到危机扣除信任度减半）",
        "👟 加厚防滑特制舞鞋（舞蹈练习与舞台爆发力大幅提升）",
        "🍲 深夜暖心关东煮（粉丝增长效率额外提升）",
        "📖 记满心得的旧笔记本（歌唱与综艺事件收益大幅提升）",
    ]
    st.session_state.temp_gacha = random.choice(gacha_pool)

  if st.session_state.temp_gacha:
    st.success(f"✨ 你抽中了：**{st.session_state.temp_gacha}**")

  st.markdown("---")
  if st.button("🚀 签订研修契约，正式开启练习生生活！", use_container_width=True):
    if not name_input.strip():
      st.error("请先输入你的名字哦！")
    else:
      if not st.session_state.temp_gacha:
        st.session_state.temp_gacha = "📖 记满心得的旧笔记本"
      st.session_state.player_name = name_input.strip()
      st.session_state.group = selected_group
      st.session_state.lucky_item = st.session_state.temp_gacha
      st.session_state.game_started = True
      st.rerun()

# -------------------------------------------------------------------
# 游戏主流程
# -------------------------------------------------------------------
if st.session_state.game_started:
  curr_stage = st.session_state.stage
  member = get_rand_member()

  # 特训安排日
  is_free_training_day = curr_stage in [3, 9, 15]

  if is_free_training_day and curr_stage < 20:
    st.subheader(f"🗓️ Stage {curr_stage}：自主特训与日常安排")
    st.info(
        f"💡 **自主安排日** | 🎒 当前幸运物：【{st.session_state.lucky_item}】"
    )

    col1, col2 = st.columns(2)
    with col1:
      if st.button("💃 在舞蹈房死磕高难度步法"):
        if st.session_state.energy < 20:
          st.error("⚠️ 体力不足，快去休息吧！")
        else:
          st.session_state.dance += random.randint(15, 25)
          st.session_state.energy -= 20
          st.session_state.stage += 1
          st.rerun()
      if st.button("🎤 到声乐室练习高音发声"):
        if st.session_state.energy < 20:
          st.error("⚠️ 嗓子有些哑了，快去休息吧！")
        else:
          st.session_state.vocal += random.randint(15, 25)
          st.session_state.energy -= 20
          st.session_state.stage += 1
          st.rerun()
    with col2:
      if st.button(f"🍲 与 {member} 相约去吃烤肉聊心事"):
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

  # 阶段 6 与 12：极速指针挑战
  elif curr_stage in [6, 12]:
    st.subheader(f"📍 Stage {curr_stage}：【极速指针挑战关卡】")
    if curr_stage == 6:
      st.markdown(
          '<div class="event-card"><b>🎮 【舞台小游戏：Dance Break 绝佳卡点】</b><br>演唱会 Solo Dance 时间来临！指针极速摆动，在绿色区域瞬间按下按键！</div>',
          unsafe_allow_html=True,
      )
      render_pointer_minigame(speed=3.0, target_start=42, target_width=15)
    else:
      st.markdown(
          '<div class="event-card"><b>🎮 【舞台小游戏：少俱打歌高音定音】</b><br>全开麦高潮副歌段落！难度升级，请在中心瞬间精准点击！</div>',
          unsafe_allow_html=True,
      )
      render_pointer_minigame(speed=4.0, target_start=40, target_width=12)

    if st.button("➔ 挑战完毕，进入下一阶段"):
      st.session_state.fans += random.randint(1000, 1800)
      st.session_state.dance += 20
      st.session_state.stage += 1
      st.rerun()

  # 阶段 18：【真正的小人左右移动躲避坠落障碍游戏】
  elif curr_stage == 18:
    st.subheader("📍 Stage 18：【巨蛋巡演·舞台事故紧急闪避】")
    st.markdown(
        '<div class="event-card"><b>🎮 【动态躲避小游戏：舞台灯光坠落危机】</b><br>舞台灯光设备突发故障开始向下坠落！<b>请在下方点击“往左/往右闪避”按钮，控制你的偶像小人左右移动</b>，躲开坠落的灯光！</div>',
        unsafe_allow_html=True,
    )

    # 渲染真正的可交互Canvas小人闪避游戏
    render_dodge_canvas_game()

    if st.button("🌟 闪避结束，前往出道前夜！"):
      st.session_state.fans += 2000
      st.session_state.variety += 25
      st.session_state.stage += 1
      st.rerun()

  # 海量 3 选项独立剧情关卡
  elif curr_stage < 20:
    st.subheader(f"📍 Stage {curr_stage} / 20")

    s_db = get_story_database(
        st.session_state.player_name, member, st.session_state.group
    )
    story = s_db.get(
        curr_stage,
        {
            "title": f"📍 Stage {curr_stage}：日常与磨练",
            "desc": f"组合今天迎来了紧张的日常排练，{member} 在身边给你加油打气！",
            "opt1": "死磕舞蹈细节，把步法做到最精准。",
            "opt2": "研究歌词情感，展现深厚歌唱张力。",
            "opt3": "设计有趣的组内互动，拉近大家的距离。",
        },
    )

    st.markdown(f"""
        <div class="event-card">
            <b>{story['title']}</b><br><br>
            {story['desc']}
        </div>
        """, unsafe_allow_html=True)

    c1 = st.button(f"1. {story['opt1']}")
    c2 = st.button(f"2. {story['opt2']}")
    c3 = st.button(f"3. {story['opt3']}")

    if c1:
      st.session_state.dance += 12
      st.session_state.fans += 400
      st.session_state.stage += 1
      st.rerun()
    if c2:
      st.session_state.vocal += 12
      st.session_state.fans += 450
      st.session_state.stage += 1
      st.rerun()
    if c3:
      st.session_state.variety += 15
      st.session_state.bond += 10
      st.session_state.stage += 1
      st.rerun()

  # -------------------------------------------------------------------
  # STAGE 20: 帝国剧场终局裁决
  # -------------------------------------------------------------------
  else:
    st.subheader("🏁 Stage 20：帝国剧场 CD 出道决选")
    st.markdown(f"""
        <div class="event-card">
            <b>✨ 【命运的聚光灯】</b><br>
            帝国剧场金碧辉煌，全日本数百家媒体的闪光灯不断闪烁。社长坐在话筒前，即将宣读最终的考核结果！
        </div>
        """, unsafe_allow_html=True)

    if st.button("🌟 揭晓最终出道结果 🌟", use_container_width=True):
      st.markdown("---")
      total = (
          st.session_state.dance
          + st.session_state.vocal
          + st.session_state.variety
      )

      if st.session_state.fans >= 2000 and total >= 120:
        st.balloons()
        st.success(
            f"🎉 恭喜 **{st.session_state.player_name}**！你携带【{st.session_state.lucky_item}】，与 **{st.session_state.group}** 的伙伴们完美闪耀帝国剧场，正式华丽 CD 出道！"
        )
      else:
        st.warning(
            f"⚠️ **{st.session_state.player_name}** 距离完美标准还有一丝差距，社长安排你继续深耕舞台，未来可期！"
        )

      st.markdown("---")
      st.markdown(f"### 📊 练习生【{st.session_state.player_name}】的终极能力")
      st.write(
          f"- 💃 舞蹈：**{st.session_state.dance} pt** | 🎤 歌唱：**{st.session_state.vocal} pt** | 🤡 综艺：**{st.session_state.variety} pt**"
      )
      st.write(
          f"- 💖 粉丝数：**{st.session_state.fans:,} 人** | 💞 团员羁绊：**{st.session_state.bond}**"
      )

      st.write("")
      if st.button("🎮 开启全新练习生人生"):
        init_game()
        st.rerun()
