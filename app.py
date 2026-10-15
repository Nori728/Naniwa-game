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

# 2. 团队与成员数据（全团按年龄从大到小严格排序）
IDOL_GROUPS = {
    "KinKi Kids": ["堂本光一", "堂本刚"],
    "ARASHI (岚)": ["大野智", "樱井翔", "相叶雅纪", "二宫和也", "松本润"],
    "Kis-My-Ft2": [
        "北山宏光",
        "千贺健永",
        "宫田俊哉",
        "横尾涉",
        "藤谷太辅",
        "玉森裕太",
        "二阶堂高嗣",
    ],
    "NEWS": ["小山庆一郎", "加藤成亮", "增田贵久"],
    "Hey! Say! JUMP": [
        "薮宏太",
        "高木雄也",
        "伊野尾慧",
        "八乙女光",
        "有冈大贵",
        "山田凉介",
        "中岛裕翔",
        "知念侑李",
    ],
    "SUPER EIGHT": ["横山裕", "村上信五", "丸山隆平", "安田章大", "大仓忠义"],
    "WEST.": [
        "中间淳太",
        "滨田崇裕",
        "桐山照史",
        "神山智洋",
        "重冈大毅",
        "藤井流星",
        "小泷望",
    ],
    "Snow Man": [
        "深泽辰哉",
        "佐久间大介",
        "渡边翔太",
        "宫馆凉太",
        "岩本照",
        "阿部亮平",
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
        "高桥恭平",
        "大西流星",
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
    "KEY TO LIT": ["中村岭亚", "井上瑞稀", "桥本凉", "猪狩苍弥", "佐佐木大光"],
    "B&ZAI": [
        "菅田琳宁",
        "本高克树",
        "矢花黎",
        "今野大辉",
        "岩崎大昇",
        "佐野晶哉",
        "川崎星辉",
    ],
    "ACEes": ["浮所飞贵", "那须雄登", "佐藤龙我", "作间龙斗", "深田龙生"],
}

# 3. 样式美化
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #120824 0%, #1f103d 50%, #31115c 100%);
        color: #ffffff;
    }
    .event-card {
        background: rgba(30, 18, 56, 0.95);
        color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        border: 2px solid #ff2a75;
        box-shadow: 0px 8px 25px rgba(255, 42, 117, 0.35);
        margin: 16px 0;
        font-size: 16px;
        line-height: 1.8;
    }
    .cute-info {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 14px;
        padding: 18px;
        border: 2px dashed #ff2a75;
        color: #2b0c4f;
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 16px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
    }
    label {
        color: #ffeb3b !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    .stTextInput input, .stSelectbox select, .stRadio div {
        color: #ffffff !important;
        font-weight: bold !important;
    }
    .stButton > button {
        background: linear-gradient(45deg, #ff2a75, #9c27b0) !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 16px !important;
        border: 2px solid #ff80ab !important;
        padding: 12px 24px !important;
        box-shadow: 0px 4px 15px rgba(255, 42, 117, 0.5);
        touch-action: manipulation;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# 4. 初始化数据
def init_game():
  st.session_state.game_started = False
  st.session_state.passed_audition = False
  st.session_state.audition_track = ""
  st.session_state.stage = 1
  st.session_state.player_name = ""
  st.session_state.group = ""
  st.session_state.lucky_item = ""

  st.session_state.energy = 100
  st.session_state.stress = 20
  st.session_state.dance = 20
  st.session_state.vocal = 20
  st.session_state.variety = 20
  st.session_state.rap = 20
  st.session_state.fans = 100
  st.session_state.trust = 50
  st.session_state.bond = 10


if "game_started" not in st.session_state:
  init_game()


def get_rand_member():
  members = IDOL_GROUPS.get(st.session_state.group, ["前辈"])
  return random.choice(members)


# -------------------------------------------------------------------
# 甄选考核小游戏（松饼采用纯 CSS GPU 硬件加速往返运动，绝对丝滑不跳帧）
# -------------------------------------------------------------------


def render_audition_vocal_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; color: #fff; }
    .box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; padding: 12px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.96); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 12px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .vocal-btn { background: linear-gradient(135deg, #ff4081, #ab47bc); color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 20px; cursor: pointer; margin-top: 10px; }
    .vocal-btn:active { transform: scale(0.92); }
    </style></head><body>
    <div class="box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">🎤 甄选项目考核</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px;">当光标进入 🎯 绿区时点击稳定高音（需抓中4次）！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始考核</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 13px;">🎤 声音爆发力考核</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 3px;">✨ 完美抓准: <span id="vScore">0</span> / 4 | ⏳ <span id="vTime">12</span>s</div>
        <div style="background: #211035; border: 2px solid #ab47bc; border-radius: 8px; height: 35px; margin: 12px 0; position: relative; overflow: hidden;">
            <div style="position: absolute; left: 115px; width: 70px; height: 100%; background: rgba(0, 230, 118, 0.4); border-left: 2px dashed #00e676; border-right: 2px dashed #00e676;">🎯</div>
            <div id="vCursor" style="position: absolute; left: 0px; width: 8px; height: 100%; background: #ff4081; border-radius: 4px;"></div>
        </div>
        <button class="vocal-btn" onclick="hitVocal()">🎶 稳定高音！</button>
        <div id="v-tip" style="color: #fff; font-size: 11px; margin-top: 5px;">看准绿区瞬间稳住气息！</div>
    </div>
    <script>
        let score = 0, timeLeft = 12, isStarted = false, isOver = false, cursorX = 0, dir = 3.5, timer, animator;
        const cursorEl = document.getElementById('vCursor'), timeEl = document.getElementById('vTime'), scoreEl = document.getElementById('vScore'), tipEl = document.getElementById('v-tip');

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            isStarted = true;
            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) { timeLeft--; timeEl.innerText = timeLeft; }
                else if(!isOver) { endAudition(); }
            }, 1000);
            
            animator = setInterval(() => {
                if(isOver || !isStarted) return;
                cursorX += dir;
                if(cursorX <= 0 || cursorX >= 284) dir *= -1;
                cursorEl.style.left = cursorX + 'px';
            }, 20);
        }

        function hitVocal() {
            if(!isStarted || isOver) return;
            if(cursorX >= 115 && cursorX <= 185) {
                score++; scoreEl.innerText = score;
                tipEl.innerHTML = "<span style='color:#00e676;'>🎉 完美高音震撼全场！</span>";
                if(score >= 4) endAudition(true);
            } else {
                tipEl.innerHTML = "<span style='color:#ff5252;'>💧 音准飘忽，气息不稳！</span>";
            }
        }

        function endAudition(success = false) {
            isOver = true; clearInterval(timer); clearInterval(animator);
            if(success || score >= 3) { tipEl.innerHTML = "<span style='color:#00e676;'>🎉 考核大成功！顺利晋级！</span>"; }
            else { tipEl.innerHTML = "<span style='color:#ff5252;'>💧 练习生初试未达标，但评委网开一面！</span>"; }
        }
    </script></body></html>
    """
  components.html(html_code, height=275)


def render_audition_dance_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; color: #fff; }
    .box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; padding: 12px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.96); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 12px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .arrow-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin: 12px 0; }
    .arrow-node { background: #211035; border: 2px solid #553377; border-radius: 12px; padding: 12px 0; font-size: 26px; font-weight: bold; cursor: pointer; color: #666; }
    .arrow-node.active { background: linear-gradient(135deg, #00e676, #00b0ff); color: #fff; border: 2px solid #fff; box-shadow: 0 0 20px #00e676, 0 0 30px #00b0ff; transform: scale(1.06); }
    .arrow-node:active { transform: scale(0.92); }
    </style></head><body>
    <div class="box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">💃 甄选项目考核</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px;">看准哪个箭头发光高亮，迅速按下发光的箭头！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始考核</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 13px;">💃 霓虹卡点考核</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 3px;">✨ 精准击中: <span id="dScore">0</span> / 7 | ⏳ <span id="dTime">12</span>s</div>
        
        <div class="arrow-container">
            <div class="arrow-node" id="btn-up" onclick="pressArrow('up')">⬆️ 上</div>
            <div class="arrow-node" id="btn-down" onclick="pressArrow('down')">⬇️ 下</div>
            <div class="arrow-node" id="btn-left" onclick="pressArrow('left')">⬅️ 左</div>
            <div class="arrow-node" id="btn-right" onclick="pressArrow('right')">➡️ 右</div>
        </div>
        
        <div id="d-tip" style="color: #fff; font-size: 11px;">看准亮起来的箭头迅速点击！</div>
    </div>
    <script>
        let score = 0, timeLeft = 12, isStarted = false, isOver = false, timer, currentActive = '';
        const dirs = ['up', 'down', 'left', 'right'];
        const scoreEl = document.getElementById('dScore'), timeEl = document.getElementById('dTime'), tipEl = document.getElementById('d-tip');

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            isStarted = true;
            nextHighlight();
            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) { timeLeft--; timeEl.innerText = timeLeft; }
                else if(!isOver) { endDance(); }
            }, 1000);
        }

        function nextHighlight() {
            if(isOver) return;
            dirs.forEach(d => document.getElementById('btn-' + d).classList.remove('active'));
            currentActive = dirs[Math.floor(Math.random() * dirs.length)];
            document.getElementById('btn-' + currentActive).classList.add('active');
        }

        function pressArrow(dir) {
            if(!isStarted || isOver) return;
            if(dir === currentActive) {
                score++;
                scoreEl.innerText = score;
                tipEl.innerHTML = "<span style='color:#00e676;'>🎉 完美踩中发光节点！</span>";
                if(score >= 7) endDance(true);
                else nextHighlight();
            } else {
                tipEl.innerHTML = "<span style='color:#ff5252;'>💧 没按中发光的箭头！拍子错了！</span>";
            }
        }

        function endDance(success = false) {
            isOver = true; clearInterval(timer);
            dirs.forEach(d => document.getElementById('btn-' + d).classList.remove('active'));
            if(success || score >= 6) { tipEl.innerHTML = "<span style='color:#00e676;'>🎉 考核大成功！</span>"; }
            else { tipEl.innerHTML = "<span style='color:#ff5252;'>💧 节奏跟不上发光节点！未达标！</span>"; }
        }
    </script></body></html>
    """
  components.html(html_code, height=315)


def render_audition_rap_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; color: #fff; }
    .box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; padding: 12px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.96); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 12px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .light-box { font-size: 40px; margin: 10px 0; background: #211035; border: 2px solid #ab47bc; border-radius: 10px; padding: 6px; }
    .color-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; margin-top: 6px; }
    .c-btn { border: none; padding: 10px 0; font-size: 14px; font-weight: bold; border-radius: 8px; cursor: pointer; color: #fff; }
    .c-btn:active { transform: scale(0.92); }
    </style></head><body>
    <div class="box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">🔥 甄选项目考核</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px;">根据闪烁灯光颜色点击对应按钮（需达7次）！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始考核</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 13px;">🔥 节奏色彩考核</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 3px;">✨ 匹配成功: <span id="rScore">0</span> / 7 | ⏳ <span id="rTime">12</span>s</div>
        <div class="light-box" id="targetLight">🔴</div>
        <div class="color-grid">
            <button class="c-btn" style="background: #e53935;" onclick="pressColor('red')">🔴 红色</button>
            <button class="c-btn" style="background: #fbc02d; color:#000;" onclick="pressColor('yellow')">🟡 黄色</button>
            <button class="c-btn" style="background: #1e88e5;" onclick="pressColor('blue')">🔵 蓝色</button>
            <button class="c-btn" style="background: #43a047;" onclick="pressColor('green')">🟢 绿色</button>
        </div>
        <div id="r-tip" style="color: #fff; font-size: 11px; margin-top: 6px;">看准闪烁灯光颜色迅速按下！</div>
    </div>
    <script>
        let score = 0, timeLeft = 12, isStarted = false, isOver = false, timer;
        const colors = [
            { name: 'red', emoji: '🔴' },
            { name: 'yellow', emoji: '🟡' },
            { name: 'blue', emoji: '🔵' },
            { name: 'green', emoji: '🟢' }
        ];
        let currentColor = colors[0];
        const lightEl = document.getElementById('targetLight'), scoreEl = document.getElementById('rScore'), timeEl = document.getElementById('rTime'), tipEl = document.getElementById('r-tip');

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            isStarted = true;
            nextColor();
            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) { timeLeft--; timeEl.innerText = timeLeft; }
                else if(!isOver) { endRap(); }
            }, 1000);
        }

        function nextColor() {
            if(isOver) return;
            currentColor = colors[Math.floor(Math.random() * colors.length)];
            lightEl.innerText = currentColor.emoji;
        }

        function pressColor(cName) {
            if(!isStarted || isOver) return;
            if(cName === currentColor.name) {
                score++; scoreEl.innerText = score;
                tipEl.innerHTML = "<span style='color:#00e676;'>🎉 节奏完美契合！</span>";
                if(score >= 7) endRap(true);
                else nextColor();
            } else {
                tipEl.innerHTML = "<span style='color:#ff5252;'>💧 颜色按错，说唱断拍！</span>";
            }
        }

        function endRap(success = false) {
            isOver = true; clearInterval(timer);
            if(success || score >= 6) { tipEl.innerHTML = "<span style='color:#00e676;'>🎉 考核大成功！</span>"; }
            else { tipEl.innerHTML = "<span style='color:#ff5252;'>💧 节奏偏离，未达标！</span>"; }
        }
    </script></body></html>
    """
  components.html(html_code, height=310)


def render_audition_variety_game():
  # 极致丝滑升级：使用纯 CSS 动画 GPU 硬件加速摆动，彻底告别卡顿与跳帧
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; color: #fff; }
    .box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; padding: 12px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.96); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 12px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .stage-area { background: #211035; border: 2px solid #ab47bc; border-radius: 10px; height: 130px; margin: 10px 0; position: relative; overflow: hidden; }
    
    @keyframes swing {
        0% { transform: translateX(5px); }
        50% { transform: translateX(235px); }
        100% { transform: translateX(5px); }
    }
    .moving-pancake { position: absolute; top: 8px; left: 0px; font-size: 26px; height: 30px; animation: swing 2.2s ease-in-out infinite alternate; will-change: transform; }
    
    .plate { position: absolute; bottom: 8px; left: 110px; width: 80px; height: 12px; background: #e0e0e0; border-radius: 6px; border: 2px solid #bdbdbd; text-align: center; font-size: 9px; color: #333; line-height: 12px; font-weight: bold; }
    .pancake-stack { position: absolute; bottom: 22px; width: 100%; display: flex; flex-direction: column-reverse; align-items: center; }
    .pancake-item { font-size: 22px; line-height: 18px; height: 18px; }
    .drop-btn { background: linear-gradient(135deg, #ff2a75, #ab47bc); color: white; border: none; padding: 10px 24px; font-size: 15px; font-weight: bold; border-radius: 20px; cursor: pointer; margin-top: 5px; }
    .drop-btn:active { transform: scale(0.92); }
    </style></head><body>
    <div class="box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">🤹 甄选项目考核</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px;">星光松饼在顶部平稳左右摆动，看准正下方托盘中央时机落下（成功叠高4层）！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始考核</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 13px;">🤹 堆松饼技巧考核</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 3px;">🥞 成功叠高: <span id="pScore">0</span> / 4 | ⏳ <span id="pTime">15</span>s</div>
        
        <div class="stage-area">
            <div class="moving-pancake" id="movingPancake">🥞</div>
            <div class="pancake-stack" id="pancakeStack"></div>
            <div class="plate">🍽️ 托盘</div>
        </div>

        <button class="drop-btn" onclick="dropPancake()">🥞 落下松饼！</button>
        <div id="p-tip" style="color: #fff; font-size: 11px; margin-top: 5px;">看准松饼平移到托盘中央的瞬间按下！</div>
    </div>
    <script>
        let score = 0, timeLeft = 15, isStarted = false, isOver = false, timer;
        const cakeEl = document.getElementById('movingPancake'), stackEl = document.getElementById('pancakeStack'), scoreEl = document.getElementById('pScore'), timeEl = document.getElementById('pTime'), tipEl = document.getElementById('p-tip');

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            isStarted = true;
            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) { timeLeft--; timeEl.innerText = timeLeft; }
                else if(!isOver) { endPancake(); }
            }, 1000);
        }

        function dropPancake() {
            if(!isStarted || isOver) return;
            // 获取当前 CSS 动画实时像素坐标
            let matrix = window.getComputedStyle(cakeEl).transform;
            let currentX = 120; // 默认容错中点
            if (matrix && matrix !== 'none') {
                let values = matrix.split(', ');
                currentX = parseFloat(values[4]); // 获取 matrix 的 translateX 实时值
            }
            
            // 托盘中心对应 translateX 大约在 90px 到 170px 之间
            if(currentX >= 85 && currentX <= 175) {
                score++;
                scoreEl.innerText = score;
                let item = document.createElement('div');
                item.className = 'pancake-item';
                item.innerText = '🥞';
                stackEl.appendChild(item);
                tipEl.innerHTML = "<span style='color:#00e676;'>🎉 完美的平衡！松饼稳稳落下！</span>";
                if(score >= 4) endPancake(true);
            } else {
                tipEl.innerHTML = "<span style='color:#ff5252;'>💧 偏离中心！松饼滑落倾斜了！</span>";
            }
        }

        function endPancake(success = false) {
            isOver = true; clearInterval(timer);
            cakeEl.style.animationPlayState = 'paused';
            if(success || score >= 3) { tipEl.innerHTML = "<span style='color:#00e676;'>🎉 特技考核通关！完美定格！</span>"; }
            else { tipEl.innerHTML = "<span style='color:#ff5252;'>💧 没叠够层数，松饼塔倒了！</span>"; }
        }
    </script></body></html>
    """
  components.html(html_code, height=330)


# -------------------------------------------------------------------
# 三大特殊突发外务小游戏组件
# -------------------------------------------------------------------


def render_watermelon_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; color: #fff; }
    .box { background: #1a0f30; border: 2px solid #ff2a75; border-radius: 14px; padding: 12px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.96); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 14px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .game-board { background: #211035; border: 2px solid #ab47bc; border-radius: 10px; height: 160px; position: relative; overflow: hidden; display: flex; flex-wrap: wrap; align-content: flex-end; padding: 6px; gap: 6px; justify-content: center; }
    .ball { border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    .drop-action-btn { background: linear-gradient(135deg, #ff2a75, #ab47bc); color: white; border: none; padding: 10px 20px; font-size: 15px; font-weight: bold; border-radius: 20px; cursor: pointer; margin-top: 10px; }
    .drop-action-btn:active { transform: scale(0.92); }
    </style></head><body>
    <div class="box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">🍉 顶奢综艺外务：合成大西瓜挑战</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px; padding: 0 10px;">15秒内不断投放道具合成，达到 <b>Lv.5 终极大西瓜徽章</b> 即可通关！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始合成挑战</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 13px;">🍉 偶像大西瓜合成演播室</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 3px;">✨ 最高合成: <span id="wLevel">Lv.1 萌新徽章</span> | ⏳ <span id="wTime">15</span>s</div>
        <div class="game-board" id="watermelonBoard"></div>
        <button class="drop-action-btn" onclick="dropNewBall()">➕ 投放新道具合成！</button>
        <div id="w-tip" style="color: #fff; font-size: 11px; margin-top: 6px;">点击按钮合成升级，冲刺大西瓜！</div>
    </div>
    <script>
        let timeLeft = 15, isStarted = false, isOver = false, timer, maxLvl = 1;
        const boardEl = document.getElementById('watermelonBoard'), timeEl = document.getElementById('wTime'), lvlEl = document.getElementById('wLevel'), tipEl = document.getElementById('w-tip');
        const levels = [
            { name: 'Lv.1 萌新徽章', size: '30px', color: '#e91e63' },
            { name: 'Lv.2 闪耀卡片', size: '42px', color: '#9c27b0' },
            { name: 'Lv.3 专属手办', size: '56px', color: '#3f51b5' },
            { name: 'Lv.4 黄金话筒', size: '70px', color: '#00bcd4' },
            { name: 'Lv.5 🌟 终极大西瓜', size: '86px', color: '#00e676' }
        ];

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            isStarted = true;
            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) { timeLeft--; timeEl.innerText = timeLeft; }
                else if(!isOver) { endWatermelon(false); }
            }, 1000);
        }

        function dropNewBall() {
            if(!isStarted || isOver) return;
            if(maxLvl < 5) {
                maxLvl++;
                lvlEl.innerText = levels[maxLvl-1].name;
                let b = document.createElement('div');
                b.className = 'ball';
                b.style.width = levels[maxLvl-1].size;
                b.style.height = levels[maxLvl-1].size;
                b.style.background = levels[maxLvl-1].color;
                b.innerText = 'W' + maxLvl;
                boardEl.appendChild(b);
                tipEl.innerHTML = "<span style='color:#00e676;'>🎉 成功合成升级到 " + levels[maxLvl-1].name + "！</span>";
                if(maxLvl >= 5) {
                    endWatermelon(true);
                }
            }
        }

        function endWatermelon(success = false) {
            isOver = true; clearInterval(timer);
            if(success) {
                tipEl.innerHTML = "<span style='color:#00e676; font-weight:bold;'>🎉 达成终极大西瓜！通告大获全胜！</span>";
            } else {
                tipEl.innerHTML = "<span style='color:#ff5252; font-weight:bold;'>💧 时间耗尽，合成未达成终极目标！</span>";
            }
        }
    </script></body></html>
    """
  components.html(html_code, height=330)


def render_match_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; color: #fff; }
    .box { background: #1a0f30; border: 2px solid #ff2a75; border-radius: 14px; padding: 12px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.96); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 14px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin: 10px auto; width: 220px; }
    .m-tile { background: linear-gradient(135deg, #ab47bc, #7b1fa2); border: 2px solid #ff80ab; height: 55px; font-size: 22px; border-radius: 10px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
    .m-tile:active { transform: scale(0.92); }
    </style></head><body>
    <div class="box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">🧩 音乐消消乐：连线消除大作战</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px; padding: 0 10px;">15秒内点击消除 <b>6组同色音符</b> 即可通关！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始消除挑战</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 13px;">🧩 音乐消除祭·连击挑战</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 3px;">✨ 已消除组数: <span id="mScore">0</span> / 6 | ⏳ <span id="mTime">15</span>s</div>
        <div class="grid" id="matchGrid"></div>
        <div id="m-tip" style="color: #fff; font-size: 11px; margin-top: 4px;">点击相同颜色的偶像音符进行消除！</div>
    </div>
    <script>
        let score = 0, timeLeft = 15, isStarted = false, isOver = false, timer;
        let tiles = ['🎵', '🎶', '🎤', '🎵', '🎶', '🎤', '🌟', '🌟', '🎵'];
        const gridEl = document.getElementById('matchGrid'), scoreEl = document.getElementById('mScore'), timeEl = document.getElementById('mTime'), tipEl = document.getElementById('m-tip');

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            isStarted = true;
            renderTiles();
            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) { timeLeft--; timeEl.innerText = timeLeft; }
                else if(!isOver) { endMatch(false); }
            }, 1000);
        }

        function renderTiles() {
            tiles.sort(() => Math.random() - 0.5);
            gridEl.innerHTML = '';
            tiles.forEach((t, idx) => {
                let div = document.createElement('div');
                div.className = 'm-tile';
                div.innerText = t;
                div.onclick = () => clickTile(idx);
                gridEl.appendChild(div);
            });
        }

        function clickTile(idx) {
            if(!isStarted || isOver) return;
            score++;
            scoreEl.innerText = score;
            tipEl.innerHTML = "<span style='color:#00e676;'>🎉 成功消除一组合拍音符！</span>";
            if(score >= 6) {
                endMatch(true);
            } else {
                renderTiles();
            }
        }

        function endMatch(success = false) {
            isOver = true; clearInterval(timer);
            if(success) {
                tipEl.innerHTML = "<span style='color:#00e676; font-weight:bold;'>🎉 消除挑战大成功！通告完美拿下！</span>";
            } else {
                tipEl.innerHTML = "<span style='color:#ff5252; font-weight:bold;'>💧 时间耗尽，连线消除未达标！</span>";
            }
        }
    </script></body></html>
    """
  components.html(html_code, height=330)


def render_parkour_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; color: #fff; }
    .box { background: #1a0f30; border: 2px solid #ff2a75; border-radius: 14px; padding: 12px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.96); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 14px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .track { background: #211035; border: 2px solid #ab47bc; border-radius: 10px; height: 110px; position: relative; overflow: hidden; display: flex; align-items: flex-end; padding: 10px; }
    .runner { font-size: 28px; position: absolute; left: 30px; bottom: 10px; transition: bottom 0.15s; }
    .jump-btn { background: linear-gradient(135deg, #00e676, #00b0ff); color: #000; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 20px; cursor: pointer; margin-top: 10px; }
    .jump-btn:active { transform: scale(0.92); }
    </style></head><body>
    <div class="box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">🏃 红毯冲刺：横版跳跃跑酷挑战</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px; padding: 0 10px;">15秒内看准障碍物连续点击 <b>⬆️ 跃起跳过</b>（需成功跳过6次）！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始跑酷挑战</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 13px;">🏃 颁奖典礼红毯·极限跳跃</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 3px;">✨ 成功跳过: <span id="pScore">0</span> / 6 | ⏳ <span id="pTime">15</span>s</div>
        <div class="track" id="trackArea">
            <div class="runner" id="runnerEl">🏃‍♂️</div>
            <div id="obstacle" style="position: absolute; right: -20px; bottom: 10px; font-size: 24px;">🚧</div>
        </div>
        <button class="jump-btn" onclick="jumpAction()">⬆️ 跃起跳过障碍！</button>
        <div id="p-tip" style="color: #fff; font-size: 11px; margin-top: 4px;">看准时机点击按钮跳过狗仔与路障！</div>
    </div>
    <script>
        let score = 0, timeLeft = 15, isStarted = false, isOver = false, timer, isJumping = false;
        const runnerEl = document.getElementById('runnerEl'), scoreEl = document.getElementById('pScore'), timeEl = document.getElementById('pTime'), tipEl = document.getElementById('p-tip');

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            isStarted = true;
            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) { timeLeft--; timeEl.innerText = timeLeft; }
                else if(!isOver) { endParkour(false); }
            }, 1000);
        }

        function jumpAction() {
            if(!isStarted || isOver || isJumping) return;
            isJumping = true;
            runnerEl.style.bottom = '55px';
            score++;
            scoreEl.innerText = score;
            tipEl.innerHTML = "<span style='color:#00e676;'>🎉 完美起跳！成功避开障碍！</span>";
            
            setTimeout(() => {
                runnerEl.style.bottom = '10px';
                isJumping = false;
            }, 350);

            if(score >= 6) {
                endParkour(true);
            }
        }

        function endParkour(success = false) {
            isOver = true; clearInterval(timer);
            if(success) {
                tipEl.innerHTML = "<span style='color:#00e676; font-weight:bold;'>🎉 红毯突围成功！聚光灯全聚焦于你！</span>";
            } else {
                tipEl.innerHTML = "<span style='color:#ff5252; font-weight:bold;'>💧 时间耗尽，红毯表现狼狈错失奖项！</span>";
            }
        }
    </script></body></html>
    """
  components.html(html_code, height=330)


# 主标题
st.title("💖 星途闪耀：我的练习生日常")

# -------------------------------------------------------------------
# STAGE 0: 开局封面
# -------------------------------------------------------------------
if not st.session_state.game_started:
  st.markdown(
      '<div class="cute-info">✨ 欢迎来到 STARTO 偶像养成营！请在下方完成你的入营登记：输入名字、选择心仪组合、抽取传奇幸运物，并选定你的【初次甄选表演项目】！</div>',
      unsafe_allow_html=True,
  )

  name_input = st.text_input(
      "✏️ 你的练习生名字 / 昵称：", placeholder="例如：酱酱 / 小夏"
  )
  st.markdown("---")

  selected_group = st.selectbox(
      "🎶 选择你想并肩作战的出道组合（全团按年龄排序）：",
      list(IDOL_GROUPS.keys()),
  )
  st.markdown("---")

  st.subheader("🎁 抽开局传奇幸运物扭蛋")
  if "temp_gacha" not in st.session_state:
    st.session_state.temp_gacha = ""

  if st.button("🎲 点击抽取你的开局传奇幸运物！"):
    gacha_pool = [
        "🍀 前辈送的开光御守（遇到危机扣除信任度减半）",
        "👟 加厚防滑特制舞鞋（舞蹈练习与舞台爆发力大幅提升）",
        "🎸 已故摇滚前辈的吉他拨片（声乐与音乐特训收益翻倍）",
        "🍱 传说中的前辈亲制爱心便当（大幅降低压力并瞬间回满体力）",
        "📸 绝版未公开杂志拍立得（危机公关与信任度直接拉满）",
        "📖 记满心得的旧笔记本（歌唱与综艺事件收益大幅提升）",
    ]
    st.session_state.temp_gacha = random.choice(gacha_pool)

  if st.session_state.temp_gacha:
    st.success(f"✨ 你抽中了：**{st.session_state.temp_gacha}**")

  st.markdown("---")
  st.subheader("🌟 选择你的初次甄选表演项目")
  audition_selection = st.radio(
      "请选择你最擅长、并在甄选大舞台上展示的项目：",
      [
          "1. 🎤 Vocal 歌唱爆发力展示",
          "2. 💃 舞台 Dance 节奏卡点展示",
          "3. 🔥 Rap 节奏色彩匹配展示",
          "4. 🤹 特技杂耍平衡展示",
      ],
  )

  st.markdown("---")
  if st.button(
      "🚀 签订研修契约，进入甄选考核舞台！", use_container_width=True
  ):
    if not name_input.strip():
      st.error("❌ 请先输入你的名字哦！")
    else:
      if not st.session_state.temp_gacha:
        st.session_state.temp_gacha = "📖 记满心得的旧笔记本"
      st.session_state.player_name = name_input.strip()
      st.session_state.group = selected_group
      st.session_state.lucky_item = st.session_state.temp_gacha

      if audition_selection.startswith("1"):
        st.session_state.audition_track = "vocal"
      elif audition_selection.startswith("2"):
        st.session_state.audition_track = "dance"
      elif audition_selection.startswith("3"):
        st.session_state.audition_track = "rap"
      else:
        st.session_state.audition_track = "variety"

      st.session_state.game_started = True
      st.rerun()

# -------------------------------------------------------------------
# STAGE 0.5: 独立甄选考核小游戏
# -------------------------------------------------------------------
elif not st.session_state.passed_audition:
  st.subheader("🌟 【练习生甄选大舞台】现场考核")
  st.markdown(
      f'<div class="event-card"><b>🎯 甄选考核进行中：</b><br>请在下方完成专属考核，成功过关即可正式签约！</div>',
      unsafe_allow_html=True,
  )

  if st.session_state.audition_track == "vocal":
    render_audition_vocal_game()
  elif st.session_state.audition_track == "dance":
    render_audition_dance_game()
  elif st.session_state.audition_track == "rap":
    render_audition_rap_game()
  else:
    render_audition_variety_game()

  st.markdown("---")
  if st.button(
      "🌟 完成考核，接受社长与评委的最终裁决！", use_container_width=True
  ):
    if st.session_state.audition_track == "vocal":
      st.session_state.vocal += 30
    elif st.session_state.audition_track == "dance":
      st.session_state.dance += 30
    elif st.session_state.audition_track == "rap":
      st.session_state.rap += 30
    else:
      st.session_state.variety += 30

    st.session_state.passed_audition = True
    st.success(
        "🎉 评委席全票通过！恭喜你正式成为 STARTO 事务所的签约 Jr 练习生！"
    )
    time.sleep(1)
    st.rerun()

# -------------------------------------------------------------------
# 游戏主流程
# -------------------------------------------------------------------
else:
  curr_stage = st.session_state.stage
  member = get_rand_member()

  if st.session_state.stress >= 70:
    st.warning(
        f"⚠️ **【压力预警】** 压力值已达 **{st.session_state.stress}%**！{member} 悄悄塞给你一罐热可可：“别把自己逼太紧，大家都在呢。”"
    )
    st.session_state.stress = 30
    st.session_state.bond += 10

  # 自主特训日（Stage 4 & Stage 16 & Stage 26）
  if curr_stage in [4, 16, 26]:
    st.subheader(f"🗓️ Stage {curr_stage}：自主特训与日常安排")
    st.info(
        f"💡 **自主安排日** | 🎒 当前幸运物：【{st.session_state.lucky_item}】 | 🔥 压力值: {st.session_state.stress}%"
    )
    col1, col2 = st.columns(2)
    with col1:
      if st.button("💃 在舞蹈房死磕高难度步法"):
        st.session_state.dance += random.randint(15, 25)
        st.session_state.stress += 10
        st.session_state.stage += 1
        st.rerun()
      if st.button("🎤 到声乐室练习高音发声"):
        st.session_state.vocal += random.randint(15, 25)
        st.session_state.stress += 10
        st.session_state.stage += 1
        st.rerun()
    with col2:
      if st.button(f"🍲 与 {member} 相约去吃烤肉聊心事"):
        st.session_state.bond += 15
        st.session_state.fans += 300
        st.session_state.stress = max(0, st.session_state.stress - 20)
        st.session_state.stage += 1
        st.rerun()
      if st.button("💤 回宿舍彻底躺平休息"):
        st.session_state.energy = min(100, st.session_state.energy + 40)
        st.session_state.stress = max(0, st.session_state.stress - 30)
        st.session_state.stage += 1
        st.rerun()

  # 特殊高张力外务危机挑战 1：🍉 Stage 15 顶奢综艺合成大西瓜挑战
  elif curr_stage == 15:
    st.subheader(
        "📍 Stage 15：【高风险外务】国民顶奢黄金档综艺独家通告邀请"
    )
    st.markdown(
        """
        <div class="event-card">
            <b>🍉 【特殊危机挑战说明】</b><br>
            你迎来了国民级黄金档综艺的唯一宝贵通告机会！各大事务所竞争极其惨烈。<br>
            - <b>选择接受挑战（合成大西瓜）</b>：若成功，各项指标全方位暴涨，人气飙升！若失败，将遭受高层严厉质疑，直接扣除大量信任度与粉丝！<br>
            - <b>选择稳妥放弃</b>：安全无风险，但错失爆红机遇。
        </div>
        """,
        unsafe_allow_html=True,
    )

    choice = st.radio(
        "是否接受这项高风险、高回报的顶奢综艺通告挑战？",
        ["🔥 接受挑战！誓要拿下国民综艺曝光！", "🛡️ 稳妥拒绝，专注于基础练习"],
    )
    if choice.startswith("🔥"):
      st.markdown("---")
      render_watermelon_game()
      col1, col2 = st.columns(2)
      with col1:
        if st.button("🏆 挑战成功！结算丰厚奖励"):
          st.session_state.vocal += 40
          st.session_state.dance += 40
          st.session_state.variety += 50
          st.session_state.fans += 5000
          st.session_state.trust += 25
          st.success(
              "🎉 **【大获全胜：国民综艺ACE诞生！】** 恭喜！你凭借出色的合成表现震撼全场导演组，国民知名度呈指数级暴涨！各项指标全线大丰收！"
          )
          time.sleep(1)
          st.session_state.stage = 16
          st.rerun()
      with col2:
        if st.button("💧 挑战失败/未达标！接受惨痛惩罚"):
          st.session_state.trust -= 20
          st.session_state.fans = max(0, st.session_state.fans - 1500)
          st.session_state.stress += 40
          st.error(
              "💥 **【惨痛失利：通告泡汤与信任雪崩】** 由于表现不佳，现场气氛尴尬，不仅通告被同台竞争对手顶替，事务所高层对你的信任度也大幅跌落！"
          )
          time.sleep(1)
          st.session_state.stage = 16
          st.rerun()
    else:
      if st.button("➔ 确认放弃，进入下一阶段"):
        st.session_state.stage = 16
        st.rerun()

  # 特殊高张力外务危机挑战 2：🧩 Stage 20 大型音乐节连线消除挑战
  elif curr_stage == 20:
    st.subheader("📍 Stage 20：【高风险外务】全亚洲跨年音乐祭核心表演位")
    st.markdown(
        """
        <div class="event-card">
            <b>🧩 【特殊危机挑战说明】</b><br>
            全亚洲跨年音乐祭总导演临时点将，要求你在直播前完成极高难度的“音乐消除祭”盲验考核！<br>
            - <b>接受挑战（连线消除）</b>：成功则一战成名，粉丝数狂飙！失败则遭到全网群嘲，惩罚极重！
        </div>
        """,
        unsafe_allow_html=True,
    )

    choice = st.radio(
        "是否接受跨年音乐祭的连线消除考核挑战？",
        ["🔥 接受挑战！绝不放过任何舞台！", "🛡️ 稳妥拒绝，保守等待安排"],
    )
    if choice.startswith("🔥"):
      st.markdown("---")
      render_match_game()
      col1, col2 = st.columns(2)
      with col1:
        if st.button("🏆 挑战成功！结算丰厚奖励"):
          st.session_state.vocal += 45
          st.session_state.rap += 40
          st.session_state.fans += 6000
          st.session_state.trust += 30
          st.success(
              "🎉 **【大获全胜：全网疯狂圈粉！】** 完美通关！你展现出了无可挑剔的音乐节奏掌控力，粉丝数暴涨，全网热搜第一！"
          )
          time.sleep(1)
          st.session_state.stage = 21
          st.rerun()
      with col2:
        if st.button("💧 挑战失败/未达标！接受惨痛惩罚"):
          st.session_state.trust -= 25
          st.session_state.fans = max(0, st.session_state.fans - 2000)
          st.session_state.stress += 45
          st.error(
              "💥 **【惨痛失利：舞台失误与舆论反噬】** 考核失利，不仅错失了黄金表演位，还被黑粉抓住痛脚大肆带节奏，压力瞬间拉满！"
          )
          time.sleep(1)
          st.session_state.stage = 21
          st.rerun()
    else:
      if st.button("➔ 确认放弃，进入下一阶段"):
        st.session_state.stage = 21
        st.rerun()

  # 特殊高张力外务危机挑战 3：🏃 Stage 24 日本金唱片大赏红毯跳跃跑酷挑战
  elif curr_stage == 24:
    st.subheader("📍 Stage 24：【高风险外务】日本金唱片大赏红毯极限突围")
    st.markdown(
        """
        <div class="event-card">
            <b>🏃 【特殊危机挑战说明】</b><br>
            金唱片大赏红毯现场突发狗仔围堵与直播事故！你必须在镜头前完成极限红毯跳跃突围！<br>
            - <b>接受挑战（横版跑酷跳跃）</b>：成功则拿下年度最具人气大奖！失败则形象大跌，遭遇事务所冷藏危机！
        </div>
        """,
        unsafe_allow_html=True,
    )

    choice = st.radio(
        "是否接受金唱片大赏红毯极限突围挑战？",
        ["🔥 接受挑战！闪耀红毯绝不退缩！", "🛡️ 稳妥拒绝，低调走完流程"],
    )
    if choice.startswith("🔥"):
      st.markdown("---")
      render_parkour_game()
      col1, col2 = st.columns(2)
      with col1:
        if st.button("🏆 挑战成功！结算丰厚奖励"):
          st.session_state.dance += 50
          st.session_state.variety += 45
          st.session_state.fans += 8000
          st.session_state.trust += 35
          st.success(
              "🎉 **【大获全胜：红毯封神与金奖加冕】** 完美跑酷突围！你矫健的身姿与完美的表情管理惊艳全亚洲媒体，斩获年度至高荣耀！"
          )
          time.sleep(1)
          st.session_state.stage = 25
          st.rerun()
      with col2:
        if st.button("💧 挑战失败/未达标！接受惨痛惩罚"):
          st.session_state.trust -= 30
          st.session_state.fans = max(0, st.session_state.fans - 2500)
          st.session_state.stress += 50
          st.error(
              "💥 **【惨痛失利：红毯摔倒与形象重创】** 突围失败，在直播镜头前狼狈不堪，不仅丢尽颜面，还遭到事务所严厉警告与无限期通告削减！"
          )
          time.sleep(1)
          st.session_state.stage = 25
          st.rerun()
    else:
      if st.button("➔ 确认放弃，进入下一阶段"):
        st.session_state.stage = 25
        st.rerun()

  # 📖 常规剧情章节与突发危机
  elif curr_stage < 30:
    st.subheader(f"📍 Stage {curr_stage} / 30")
    s_db = {
        1: {
            "title": "🎵 Stage 1：雨后练习室的汗水",
            "desc": f"雨后的东京空气潮湿，练习室镜子蒙上雾气。{member} 擦着汗过来：“刚才转身重心偏了，要不要再试一次？”",
            "opt1": "虚心请教，对着镜子死磕到深夜。",
            "opt2": "递上冰麦茶，和大家回宿舍聊天。",
            "opt3": "早点回去休息保持体能。",
        },
        2: {
            "title": "📺 Stage 2：地方电视台初登场",
            "desc": "你迎来了人生第一次上电视节目的机会，面对镜头虽然有些紧张，但全员状态拉满。",
            "opt1": "紧跟队长节奏，稳妥完成初舞台。",
            "opt2": "超常发挥，贡献了全场最亮眼的单人镜头。",
            "opt3": "在后台和队友互相打气加油。",
        },
        3: {
            "title": "🃏 Stage 3：【宿舍深夜心跳】真心话卡牌",
            "desc": "深夜熄灯后，宿舍里几个人围坐在一起玩卡牌。你抽到了闪光卡：“如果在组合里选一个人作为永远的搭档？”",
            "opt1": f"指向身边的 {member}：“选最懂我的你！”",
            "opt2": "大笑着传给下一位：“商业机密！”",
            "opt3": "认真看向全员：“选大家所有人！”",
        },
        5: {
            "title": "📺 Stage 5：【外务】户外泥潭搞笑综艺录制",
            "desc": "你被安排参加著名户外泥潭挑战节目！导演要求你在泥潭里抓泥鳅时做出偶像表情管理！",
            "opt1": "完全抛弃包袱，直接摔进泥潭爆笑造梗！",
            "opt2": "咬牙保持完美微笑，走出模特步。",
            "opt3": f"拉着队友 {member} 玩泥巴造 CP 名场面。",
        },
        6: {
            "title": "📣 Stage 6：街头突击应援大作战",
            "desc": "事务所安排街头突击宣传，吸引路人驻足为你和组合呐喊应援！",
            "opt1": "卖力大喊拉拢每一位路人。",
            "opt2": "用清唱吸引人群聚集。",
            "opt3": "派发应援传单并亲切合影。",
        },
        7: {
            "title": "📻 Stage 7：【外务】深夜广播电台解忧连线",
            "desc": "你在前辈的电台节目里获得了 5 分钟试听 Corner，需要现场回答听众的烦恼来信！",
            "opt1": "读高考听众来信，给温情治愈建议。",
            "opt2": "搞笑模仿社长和前辈的声音。",
            "opt3": "推荐自己私藏的偏门摇滚歌单。",
        },
        8: {
            "title": "🍖 Stage 8：前辈团的大牌烤肉联谊",
            "desc": f"前辈团在街角烤肉店包场，邀请你们聚餐。滋滋作响的肉香中，{member} 聊起了对未来的迷茫。",
            "opt1": "“我们一定要一起站上巨蛋顶峰！”",
            "opt2": "默默烤好一整盘肉递给前辈：“大家辛苦了！”",
            "opt3": "调侃打破沉重：“红了别忘烤肉情！”",
        },
        9: {
            "title": "📍 Stage 9：【突发事件】深夜街头突击生放送（直播）！",
            "desc": f"刚结束排练和 {member} 走在涩谷街头，电视台摄影车突然把镜头怼到你们脸前，主持人随机要求现场即兴表现！",
            "opt1": "当场清唱自创高音段落！【🎤 歌唱+25，💖 粉丝+800 | ⚠️ 🔥 压力+20】",
            "opt2": "拉过队友搞怪模仿社长！【🤡 综艺+30，💞 羁绊+20 | ⚠️ 🛡️ 信任度-15】",
            "opt3": "礼貌推给队长稳妥应对！【🛡️ 信任度+15，🔥 压力-10 | ⚠️ 💖 粉丝-200】",
        },
        10: {
            "title": "⚡ Stage 10：夏日风暴音乐节舞台危机",
            "desc": "户外音乐节突遇强风与舞台故障，现场音响与灯光频频出错！",
            "opt1": "凭借清唱和强劲节奏完美控场。",
            "opt2": "临危不乱协助队友调整走位。",
            "opt3": "带头带动全场观众拍手合唱。",
        },
        11: {
            "title": "⛏️ Stage 11：事务所地下仓库寻宝",
            "desc": "你在事务所尘封的地下仓库里翻找前辈留下的绝版绝密档案与道具！",
            "opt1": "仔细翻找每一个木箱。",
            "opt2": "直奔贴着金唱片标签的角落。",
            "opt3": "和队友合力搬开重物共同寻宝。",
        },
        12: {
            "title": "🔨 Stage 12：地下停车场狗仔队突袭",
            "desc": "刚录完节目走出地下停车场，数名狗仔扛着长枪短炮突然围堵上来！",
            "opt1": "果断护住队友，冷静周旋突围。",
            "opt2": "面带微笑礼貌配合拍照。",
            "opt3": "迅速上车关门避开闪光灯。",
        },
        13: {
            "title": "📍 Stage 13：【黑暗面波折】资源遭恶意顶替与排挤！",
            "desc": "你原本内定的杂志核心单人页和电视节目通告，在临录制前夕被高层关系户空降顶替。队友私下提醒你这只是圈子残酷冰山的一角……",
            "opt1": "咽下委屈，在深夜无人的练习室疯狂加练宣泄不甘【💃 舞蹈+25，🔥 压力+20】",
            "opt2": "找高层据理力争，用实力和人气争取公开公平竞争【🛡️ 信任度+20，💖 粉丝+1000】",
            "opt3": "心态崩盘陷入自我怀疑，想要逃避训练【⚠️ 信任度-20，🔥 压力+30】",
        },
        14: {
            "title": "🎭 Stage 14：【外务】帝国剧场舞台剧试镜",
            "desc": "你获得了经典舞台剧的试镜资格，导演要求现场演练高难度威亚和武打！",
            "opt1": "咬牙克服恐高，反复练空中翻滚。",
            "opt2": "专注于台词念白与眼神爆发力。",
            "opt3": "主动拉着同台伙伴互相对戏。",
        },
        17: {
            "title": "📍 Stage 17：【黑暗面波折】网络黑粉恶意造谣与带节奏！",
            "desc": "匿名论坛突然出现大量针对你的恶意谣言和抹黑通稿，质疑你的业务能力并试图劝退粉丝，舆论陷入冰点。",
            "opt1": "发布直面质疑的个人直拍和实力反击舞台，用作品说话【💖 粉丝+2000，🎤 歌唱+25】",
            "opt2": "配合事务所冷处理，不给黑粉眼神和流量【🛡️ 信任度+15，🔥 压力+10】",
            "opt3": "情绪崩溃与黑粉在网络上互撕【⚠️ 信任度-30，🔥 压力+40】",
        },
        18: {
            "title": f"📍 Stage 18：【突发危机】队友 {member} 临演前突发高烧！",
            "desc": f"开演前 1 小时，核心成员 {member} 突发高烧晕倒无法登台！他的高音和舞蹈空出了大块缺口！",
            "opt1": "挺身而出，30分钟硬记高音救场！【🎤 歌唱+30，💖 粉丝+1000 | ⚠️ 🔥 压力+25】",
            "opt2": "协助队长重排走位填补空缺【🛡️ 信任度+20，💃 舞蹈+15 | ⚠️ 💖 无额外粉丝】",
            "opt3": "在后台照顾队友并安抚情绪【💞 羁绊+30 | ⚠️ 缺席彩排，🛡️ 信任度-10】",
        },
        19: {
            "title": "🏢 Stage 19：社长办公室的顶楼闭门谈话",
            "desc": "深夜排练结束后，你被单独叫进了顶楼办公室。社长看着你厚厚的一叠记录，露出笑意。",
            "opt1": "目光坚定：“我已经准备好承担更大责任！”",
            "opt2": "谦逊鞠躬感谢事务所培养。",
            "opt3": "坦诚说出对未来音乐风格的野心。",
        },
        21: {
            "title": "🍕 Stage 21：宿舍里的深夜披萨作战",
            "desc": f"距离出道决定日只剩最后几天。{member} 偷偷订了外卖披萨送到宿舍，招呼大家放松。",
            "opt1": "讲冷笑话活跃气氛。",
            "opt2": "举杯：“能和大家相遇太好了！”",
            "opt3": "吃完主动把厨房收拾得干干净净。",
        },
        22: {
            "title": "🎬 Stage 22：黄金档专属冠名番宣录制",
            "desc": "你们迎来了属于自己组合的第一档黄金档冠名番宣节目，全员精神抖擞！",
            "opt1": "主动抛梗承担节目搞笑担当。",
            "opt2": "认真配合每一个游戏环节。",
            "opt3": "照顾镜头较少的队友增加曝光。",
        },
        23: {
            "title": "📺 Stage 23：黄金档搞笑综艺嘉宾连线",
            "desc": "你被选为代表参加全国黄金档搞笑综艺，面对老牌主持人的尖锐提问！",
            "opt1": "自嘲爆料宿舍奇葩趣事。",
            "opt2": "展示一秒变帅气的绝技。",
            "opt3": "温情分享组合一路走来的不容易。",
        },
        25: {
            "title": "🎤 Stage 25：全国巡演千秋乐（终官场）幕后感动",
            "desc": f"全国巡演最后一场幕后，全员围在圆阵里，{member} 眼含泪光伸向下臂。",
            "opt1": "紧紧扣住大家的手，大喊：“我们是最棒的！”",
            "opt2": "给每一位队友递上润喉茶与擦汗毛巾。",
            "opt3": "拿出手机记录下大家最真实的笑容。",
        },
        27: {
            "title": "📸 Stage 27：出道单曲封面与概念写真拍摄",
            "desc": "出道单曲的封面及写真拍摄在东京湾海边进行，摄影师要求展现极致的少年感！",
            "opt1": "迎着海风展现张力十足的眼神杀。",
            "opt2": "和队友打闹抓拍最自然的笑容。",
            "opt3": "配合服装摆出最高难度的时尚造型。",
        },
        28: {
            "title": "🌌 Stage 28：天台上的星空誓言",
            "desc": "决选前夜，你和伙伴们站在事务所天台上，俯瞰繁华的东京夜景。",
            "opt1": "对着星空高喊：“要在巨蛋顶峰见！”",
            "opt2": "给每一位队友写下一张心意贺卡。",
            "opt3": "默默握紧拳头下定决胜决心。",
        },
        29: {
            "title": "🌙 Stage 29：出道决选发布会彩排最后通牒",
            "desc": "明天就是全日本决选发布会。导播对最后走位提出了极其严苛的修改意见！",
            "opt1": "带头留下来连夜加练3小时。",
            "opt2": "帮队友调整领带耳返展凝聚力。",
            "opt3": "沉稳自信感染所有人。",
        },
    }

    story = s_db.get(
        curr_stage,
        {
            "title": f"📍 Stage {curr_stage}：日常与磨练",
            "desc": f"组合今天迎来了紧张的日常排练，{member} 在身边给你加油打气！",
            "opt1": "死磕舞蹈细节。",
            "opt2": "研究歌词情感。",
            "opt3": "设计有趣的组内互动。",
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

    if curr_stage in [9, 13, 17, 18]:
      if c1:
        if curr_stage == 9:
          st.session_state.vocal += 25
          st.session_state.fans += 800
          st.session_state.stress += 20
        elif curr_stage == 13:
          st.session_state.dance += 25
          st.session_state.stress += 20
        elif curr_stage == 17:
          st.session_state.fans += 2000
          st.session_state.vocal += 25
        elif curr_stage == 18:
          st.session_state.vocal += 30
          st.session_state.fans += 1000
          st.session_state.stress += 25
        st.session_state.stage += 1
        st.rerun()
      if c2:
        if curr_stage == 9:
          st.session_state.variety += 30
          st.session_state.bond += 20
          st.session_state.trust -= 15
        elif curr_stage == 13:
          st.session_state.trust += 20
          st.session_state.fans += 1000
        elif curr_stage == 17:
          st.session_state.trust += 15
          st.session_state.stress += 10
        elif curr_stage == 18:
          st.session_state.trust += 20
          st.session_state.dance += 15
        st.session_state.stage += 1
        st.rerun()
      if c3:
        if curr_stage == 9:
          st.session_state.trust += 15
          st.session_state.stress = max(0, st.session_state.stress - 10)
          st.session_state.fans = max(0, st.session_state.fans - 200)
        elif curr_stage == 13:
          st.session_state.trust -= 20
          st.session_state.stress += 30
        elif curr_stage == 17:
          st.session_state.trust -= 30
          st.session_state.stress += 40
        elif curr_stage == 18:
          st.session_state.bond += 30
          st.session_state.trust -= 10
        st.session_state.stage += 1
        st.rerun()
    else:
      if c1:
        st.session_state.dance += 15
        st.session_state.fans += 300
        st.session_state.stress += 5
        st.session_state.stage += 1
        st.rerun()
      if c2:
        st.session_state.vocal += 15
        st.session_state.fans += 350
        st.session_state.stress += 5
        st.session_state.stage += 1
        st.rerun()
      if c3:
        st.session_state.variety += 15
        st.session_state.bond += 10
        st.session_state.stage += 1
        st.rerun()

  # -------------------------------------------------------------------
  # STAGE 30: 帝国剧场终局裁决与个性化称号结算
  # -------------------------------------------------------------------
  else:
    st.subheader("🏁 Stage 30：帝国剧场 CD 出道终局裁决")
    st.markdown(
        """
        <div class="event-card">
            <b>✨ 【命运的聚光灯】</b><br>
            帝国剧场金碧辉煌，全日本数百家媒体的闪光灯不断闪烁。历经 30 章的汗水、波折与成长，社长坐在话筒前，即将宣读最终的 CD 出道考核结果！
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🌟 揭晓最终出道结果与个人称号 🌟", use_container_width=True):
      st.markdown("---")
      total = (
          st.session_state.dance
          + st.session_state.vocal
          + st.session_state.variety
          + st.session_state.rap
      )

      max_attr = max(
          st.session_state.vocal,
          st.session_state.dance,
          st.session_state.variety,
          st.session_state.rap,
      )
      title_desc = ""
      if max_attr == st.session_state.vocal and st.session_state.vocal >= 150:
        title_desc = (
            "🎤 **【恭喜作为大主唱出道！】** 你的天籁高音和磁性声线征服了全场，"
            "成为组合当之无愧的灵魂歌姬/主唱大人！"
        )
      elif max_attr == st.session_state.dance and st.session_state.dance >= 150:
        title_desc = (
            "💃 **【恭喜作为大主舞出道！】** 你的肢体爆发力与完美卡点惊艳四座，"
            "每次登台都是视觉焦点的首席舞者！"
        )
      elif (
          max_attr == st.session_state.variety
          and st.session_state.variety >= 150
      ):
        title_desc = (
            "🤡 **【恭喜拿下团体综艺位/ACE担当！】** 你的幽默感与控场能力满分，"
            "是组合里无可替代的综艺之神与全能 ACE！"
        )
      elif max_attr == st.session_state.rap and st.session_state.rap >= 150:
        title_desc = (
            "🔥 **【恭喜作为王牌 Rap 担当出道！】** 你的快嘴说唱与节奏爆发力炸裂全场，"
            "为组合注入了最强烈的个性色彩！"
        )
      else:
        title_desc = "🌟 **【全能实力派出道】** 各项均衡发展的舞台多面手！"

      if (
          st.session_state.fans >= 3000
          and total >= 180
          and st.session_state.trust >= 40
      ):
        if st.session_state.bond >= 35:
          st.balloons()
          st.success(
              f"🎉 **【完美结局：组合华丽出道】**\n\n{title_desc}\n\n"
              f"恭喜 **{st.session_state.player_name}**！你携带【{st.session_state.lucky_item}】，与"
              f" **{st.session_state.group}**"
              " 的伙伴们历经风雨、跨越黑暗面波折与深厚羁绊，全员闪耀帝国剧场，正式以完整组合名义华丽"
              " CD 出道！"
          )
        else:
          st.warning(
              f"🎤 **【意难平结局：孤高 Solo 出道】**\n\n{title_desc}\n\n"
              f"虽然你的个人实力顶尖、粉丝无数，但由于一路走来与队友交流较少、**团员羁绊（{st.session_state.bond}"
              " pt）过低**……\n\n"
              "社长最终拍板：**取消组合出道名额，改由你个人 Solo"
              " 出道！**。灯光虽然为你一人闪耀，但后台却显得格外孤单。"
          )
      elif st.session_state.trust < 40:
        st.error(
            f"🛡️ **【信任危机结局：无限期雪藏】**\n\n"
            f"因为前期累积的事务所信任度过低（仅剩 {st.session_state.trust}"
            " pt），高层认为你风波不断、难以掌控，决选当天社长直接驳回了你的出道企划，未来堪忧……"
        )
      else:
        st.warning(
            f"⚠️ **{st.session_state.player_name}**"
            " 你的粉丝数或综合实力尚差火候（粉丝需 $\ge 3000$，三维总和需 $\ge"
            " 180$），社长安排你继续深耕舞台，未来可期！"
        )

      st.markdown("---")
      st.markdown(
          f"### 📊 练习生【{st.session_state.player_name}】的终极能力档案"
      )
      st.write(
          f"- 💃 舞蹈：**{st.session_state.dance} pt** | 🎤"
          f" 歌唱：**{st.session_state.vocal} pt** | 🔥"
          f" Rap：**{st.session_state.rap} pt** | 🤡"
          f" 综艺：**{st.session_state.variety} pt**"
      )
      st.write(
          f"- 💖 粉丝数：**{st.session_state.fans:,} 人** | 💞"
          f" 团员羁绊：**{st.session_state.bond} pt** | 🛡️"
          f" 事务所信任：**{st.session_state.trust} pt**"
      )

      st.write("")
      if st.button("🎮 开启全新练习生人生"):
        init_game()
        st.rerun()
