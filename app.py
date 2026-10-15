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

# 3. 样式美化（橙光视觉风）
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1a0f30 0%, #2d1b4e 50%, #4a148c 100%);
        color: #ffffff;
    }
    .event-card {
        background: rgba(45, 27, 78, 0.85);
        color: #ffffff;
        padding: 22px;
        border-radius: 18px;
        border: 2px solid #ff4081;
        box-shadow: 0px 10px 30px rgba(255, 64, 129, 0.4);
        margin: 14px 0;
        font-size: 15px;
        line-height: 1.7;
    }
    .cute-info {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 14px;
        padding: 16px;
        border: 2px dashed #ff4081;
        color: #4a148c;
        font-weight: 600;
        margin-bottom: 14px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
    }
    .stButton > button {
        background: linear-gradient(45deg, #ff4081, #ab47bc) !important;
        color: white !important;
        font-size: 15px !important;
        font-weight: bold !important;
        border-radius: 18px !important;
        border: none !important;
        padding: 10px 22px !important;
        box-shadow: 0px 4px 15px rgba(255, 64, 129, 0.5);
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
# 甄选专属互动小游戏组件（Vocal / Dance / Rap / 杂耍）
# -------------------------------------------------------------------


def render_audition_vocal_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; padding: 12px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.95); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 12px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .vocal-btn { background: linear-gradient(135deg, #ff4081, #ab47bc); color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 20px; cursor: pointer; margin-top: 10px; }
    .vocal-btn:active { transform: scale(0.92); }
    </style></head><body>
    <div class="box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">🎤 甄选项目：Vocal 高音长音挑战</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px;">当光标移动到 🎯 完美绿区时按下保持高音！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始 Vocal 考核</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">🎤 Vocal 甄选：长音爆发力</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 3px;">✨ 完美高音: <span id="vScore">0</span> / 4 | ⏳ <span id="vTime">12</span>s</div>
        <div style="background: #211035; border: 2px solid #ab47bc; border-radius: 8px; height: 35px; margin: 12px 0; position: relative; overflow: hidden;">
            <div style="position: absolute; left: 115px; width: 70px; height: 100%; background: rgba(0, 230, 118, 0.4); border-left: 2px dashed #00e676; border-right: 2px dashed #00e676;">🎯</div>
            <div id="vCursor" style="position: absolute; left: 0px; width: 8px; height: 100%; background: #ff4081; border-radius: 4px;"></div>
        </div>
        <button class="vocal-btn" onclick="hitVocal()">🎶 稳定高音！</button>
        <div id="v-tip" style="color: #fff; font-size: 11px; margin-top: 5px;">看准绿区稳住气息！</div>
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
                score++;
                scoreEl.innerText = score;
                tipEl.innerHTML = "<span style='color:#00e676;'>🎉 完美高音震撼全场！</span>";
            } else {
                tipEl.innerHTML = "<span style='color:#ff5252;'>💧 音准飘忽，气息不稳！</span>";
            }
        }

        function endAudition() {
            isOver = true; clearInterval(timer); clearInterval(animator);
            if(score >= 3) { tipEl.innerHTML = "<span style='color:#00e676;'>🎉 Vocal 甄选大成功！顺利晋级！</span>"; }
            else { tipEl.innerHTML = "<span style='color:#ff5252;'>💧 发挥失常，但评委网开一面让你通过！</span>"; }
        }
    </script></body></html>
    """
  components.html(html_code, height=275)


def render_audition_dance_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; padding: 12px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.95); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 12px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .click-btn { background: linear-gradient(135deg, #ff4081, #ab47bc); color: white; border: none; width: 140px; height: 65px; font-size: 18px; font-weight: bold; border-radius: 32px; cursor: pointer; box-shadow: 0 4px 15px rgba(255, 64, 129, 0.5); margin: 10px 0; }
    .click-btn:active { transform: scale(0.92); }
    </style></head><body>
    <div class="box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">💃 甄选项目：Dance 舞步爆发连击</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px;">12秒内疯狂点击按钮，达成 70 下以上！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始 Dance 考核</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">💃 Dance 甄选：动感舞步连击</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 5px;">🔥 舞步连击: <span id="dCount">0</span> / 70 | ⏳ <span id="dTime">12</span>s</div>
        <button class="click-btn" onclick="handleDance()">🕺 疯狂卡点！</button>
        <div id="d-tip" style="color: #fff; font-size: 11px;">展现极致的身体协调与爆发力！</div>
    </div>
    <script>
        let count = 0, timeLeft = 12, isStarted = false, isOver = false, timer;
        const countEl = document.getElementById('dCount'), timeEl = document.getElementById('dTime'), tipEl = document.getElementById('d-tip');

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            isStarted = true;
            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) {
                    timeLeft--;
                    timeEl.innerText = timeLeft;
                } else if(!isOver) {
                    isOver = true;
                    clearInterval(timer);
                    if(count >= 70) {
                        tipEl.innerHTML = "<span style='color:#00e676;'>🎉 舞步燃爆全场！首席舞者预定！</span>";
                    } else {
                        tipEl.innerHTML = "<span style='color:#ff5252;'>💧 体力不支，动作稍显僵硬...</span>";
                    }
                }
            }, 1000);
        }

        function handleDance() {
            if(!isStarted || isOver) return;
            count++;
            countEl.innerText = count;
        }
    </script></body></html>
    """
  components.html(html_code, height=265)


def render_audition_rap_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; padding: 12px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.95); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 12px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .rap-btn { background: linear-gradient(135deg, #ff4081, #ab47bc); color: white; border: none; width: 140px; height: 65px; font-size: 18px; font-weight: bold; border-radius: 32px; cursor: pointer; box-shadow: 0 4px 15px rgba(255, 64, 129, 0.5); margin: 10px 0; }
    .rap-btn:active { transform: scale(0.92); }
    </style></head><body>
    <div class="box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">🔥 甄选项目：Rap 机关枪快嘴连击</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px;">12秒内疯狂点击按钮，达成 80 下以上！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始 Rap 考核</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">🔥 Rap 甄选：快嘴节奏风暴</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 5px;">⚡ 快嘴连击: <span id="rCount">0</span> / 80 | ⏳ <span id="rTime">12</span>s</div>
        <button class="rap-btn" onclick="handleRap()">🎤 疯狂输出！</button>
        <div id="r-tip" style="color: #fff; font-size: 11px;">用密集的韵律掌控全场空气！</div>
    </div>
    <script>
        let count = 0, timeLeft = 12, isStarted = false, isOver = false, timer;
        const countEl = document.getElementById('rCount'), timeEl = document.getElementById('rTime'), tipEl = document.getElementById('r-tip');

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            isStarted = true;
            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) {
                    timeLeft--;
                    timeEl.innerText = timeLeft;
                } else if(!isOver) {
                    isOver = true;
                    clearInterval(timer);
                    if(count >= 80) {
                        tipEl.innerHTML = "<span style='color:#00e676;'>🎉 节奏风暴！全场评委起立鼓掌！</span>";
                    } else {
                        tipEl.innerHTML = "<span style='color:#ff5252;'>💧 词句卡壳，气势稍逊一筹...</span>";
                    }
                }
            }, 1000);
        }

        function handleRap() {
            if(!isStarted || isOver) return;
            count++;
            countEl.innerText = count;
        }
    </script></body></html>
    """
  components.html(html_code, height=265)


def render_audition_variety_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; padding: 12px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.95); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 12px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin: 10px auto; width: 240px; }
    .tile { background: linear-gradient(135deg, #ab47bc, #7b1fa2); border: 2px solid #ff80ab; color: #fff; height: 50px; font-size: 18px; font-weight: bold; border-radius: 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
    .tile:active { transform: scale(0.92); }
    </style></head><body>
    <div class="box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">🤡 甄选项目：特殊才艺平衡杂耍</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px;">点击互换9宫格道具，按 1 到 9 排序！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始杂耍考核</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">🤡 特殊才艺：道具平衡拼图</div>
        <div class="grid" id="vGrid"></div>
        <div id="v-tip" style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 3px;">✨ 点击两两交换道具复原平衡！</div>
    </div>
    <script>
        let board = [3, 1, 5, 2, 8, 4, 9, 6, 7];
        let target = [1, 2, 3, 4, 5, 6, 7, 8, 9];
        let firstSelected = null;
        const gridEl = document.getElementById('vGrid'), tipEl = document.getElementById('v-tip');

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            renderBoard();
        }

        function renderBoard() {
            gridEl.innerHTML = '';
            board.forEach((val, idx) => {
                let tile = document.createElement('div');
                tile.className = 'tile';
                tile.innerText = '🤹‍♂️' + val;
                if(firstSelected === idx) tile.style.border = '2px solid #00e676';
                tile.onclick = () => selectTile(idx);
                gridEl.appendChild(tile);
            });
        }

        function selectTile(idx) {
            if(firstSelected === null) {
                firstSelected = idx;
                renderBoard();
            } else {
                let temp = board[firstSelected];
                board[firstSelected] = board[idx];
                board[idx] = temp;
                firstSelected = null;
                renderBoard();
                checkWin();
            }
        }

        function checkWin() {
            if(board.every((v, i) => v === target[i])) {
                tipEl.innerHTML = "<span style='color:#00e676;'>🎉 杂耍道具完美平衡！全场爆笑惊叹！</span>";
            }
        }
    </script></body></html>
    """
  components.html(html_code, height=275)


# -------------------------------------------------------------------
# 原有小游戏组件库保持原样
# -------------------------------------------------------------------
def render_piano_tiles_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .piano-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 14px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); position: relative; overflow: hidden; width: 300px; height: 220px; }
    canvas { display: block; }
    .btn-row { display: flex; gap: 6px; margin-top: 8px; width: 300px; }
    .piano-btn { background: linear-gradient(180deg, #ab47bc, #7b1fa2); color: white; border: 2px solid #ff80ab; padding: 10px 0; font-size: 16px; font-weight: bold; border-radius: 10px; cursor: pointer; flex: 1; text-align: center; }
    .piano-btn:active { background: #ff4081; transform: scale(0.92); }
    .start-overlay { position: absolute; top:0; left:0; width:300px; height:220px; background: rgba(26,15,48,0.92); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 20px; font-size: 15px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    </style></head><body>
    <div class="piano-box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:10px; font-size:13px;">🎹 准备好开始打歌了吗？</div>
            <button class="start-btn" onclick="startGame()">▶️ 点击开始挑战</button>
        </div>
        <canvas id="pianoCanvas" width="300" height="220"></canvas>
    </div>
    <div class="btn-row">
        <button class="piano-btn" onclick="tapTrack(0)">1</button>
        <button class="piano-btn" onclick="tapTrack(1)">2</button>
        <button class="piano-btn" onclick="tapTrack(2)">3</button>
        <button class="piano-btn" onclick="tapTrack(3)">4</button>
    </div>
    <script>
        const canvas = document.getElementById('pianoCanvas'); const ctx = canvas.getContext('2d'); const trackWidth = 75;
        let tiles = [], score = 0, combo = 0, timeLeft = 12, isStarted = false, isGameOver = false, timer, spawner;
        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            isStarted = true;
            timer = setInterval(() => { if(timeLeft > 0 && !isGameOver) timeLeft--; else { isGameOver = true; clearInterval(timer); clearInterval(spawner); } }, 1000);
            spawner = setInterval(() => { if(!isGameOver && isStarted) tiles.push({ track: Math.floor(Math.random()*4), y: -35, h: 35, hit: false }); }, 500);
            loop();
        }
        function tapTrack(idx) {
            if(!isStarted || isGameOver) return; let ok = false;
            for(let t of tiles) { if(t.track === idx && !t.hit && t.y >= 110 && t.y <= 210) { t.hit = true; ok = true; score += 100; combo++; break; } }
            if(!ok) combo = 0;
        }
        function loop() {
            ctx.clearRect(0, 0, 300, 220); ctx.strokeStyle = '#2d1b4e';
            for(let i=1; i<4; i++) { ctx.beginPath(); ctx.moveTo(i*trackWidth, 0); ctx.lineTo(i*trackWidth, 220); ctx.stroke(); }
            ctx.fillStyle = 'rgba(255, 64, 129, 0.2)'; ctx.fillRect(0, 150, 300, 50);
            for(let i=tiles.length-1; i>=0; i--) {
                let t = tiles[i];
                if(!t.hit) {
                    t.y += 4.0; ctx.fillStyle = '#211035'; ctx.fillRect(t.track*trackWidth+4, t.y, trackWidth-8, t.h);
                    ctx.strokeStyle = '#ea80fc'; ctx.strokeRect(t.track*trackWidth+4, t.y, trackWidth-8, t.h);
                    ctx.fillStyle = '#ff80ab'; ctx.font = '11px Arial'; ctx.fillText('🎵', t.track*trackWidth+26, t.y+22);
                    if(t.y > 220) { tiles.splice(i, 1); combo = 0; }
                } else { tiles.splice(i, 1); }
            }
            ctx.fillStyle = '#fff'; ctx.font = 'bold 11px Arial'; ctx.fillText("⏳ 剩余: " + timeLeft + "s", 10, 18); ctx.fillText("🔥 分数: " + score, 120, 18); ctx.fillText("⚡ Combo: " + combo, 210, 18);
            if(!isGameOver) requestAnimationFrame(loop);
            else { 
                ctx.fillStyle = 'rgba(0,0,0,0.88)'; ctx.fillRect(0,0,300,220); 
                if(score >= 800) { ctx.fillStyle = '#00e676'; ctx.font = 'bold 16px Arial'; ctx.fillText("🎉 打歌挑战成功！总分: " + score, 35, 115); }
                else { ctx.fillStyle = '#ff5252'; ctx.font = 'bold 16px Arial'; ctx.fillText("💧 挑战失败！分数未达标: " + score, 15, 115); }
            }
        }
    </script></body></html>
    """
  components.html(html_code, height=295)


def render_shout_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .shout-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); padding: 12px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.95); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 12px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .shout-click-btn { background: linear-gradient(135deg, #ff4081, #ab47bc); color: white; border: none; width: 140px; height: 70px; font-size: 18px; font-weight: bold; border-radius: 35px; cursor: pointer; box-shadow: 0 4px 15px rgba(255, 64, 129, 0.5); margin: 15px 0; }
    .shout-click-btn:active { transform: scale(0.92); }
    </style></head><body>
    <div class="shout-box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:10px; font-size:13px;">📣 声量呐喊连击大作战</div>
            <div style="color:#fff; font-size:11px; margin-bottom:12px;">20秒内疯狂点击，点击超过90下！</div>
            <button class="start-btn" onclick="startGame()">▶️ 点击开始呐喊</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">📣 街头突击应援声量对决</div>
        <div style="color: #00e676; font-size: 12px; font-weight: bold; margin-top: 5px;">🔥 点击数: <span id="sCount">0</span> / 90 | ⏳ <span id="sTime">20</span>s</div>
        <button class="shout-click-btn" onclick="handleClick()">🗣️ 疯狂呐喊！</button>
        <div id="s-tip" style="color: #fff; font-size: 11px;">用尽全力把声音传达到广场每个角落！</div>
    </div>
    <script>
        let count = 0, timeLeft = 20, isStarted = false, isOver = false, timer;
        const countEl = document.getElementById('sCount'), timeEl = document.getElementById('sTime'), tipEl = document.getElementById('s-tip');

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            isStarted = true;
            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) {
                    timeLeft--;
                    timeEl.innerText = timeLeft;
                } else if(!isOver) {
                    isOver = true;
                    clearInterval(timer);
                    if(count >= 90) {
                        tipEl.innerHTML = "<span style='color:#00e676;'>🎉 声量爆表！应援大获全胜！</span>";
                    } else {
                        tipEl.innerHTML = "<span style='color:#ff5252;'>💧 声量不足90下，宣传效果不佳...</span>";
                    }
                }
            }, 1000);
        }

        function handleClick() {
            if(!isStarted || isOver) return;
            count++;
            countEl.innerText = count;
        }
    </script></body></html>
    """
  components.html(html_code, height=275)


def render_dodge_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .game-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 14px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); position: relative; overflow: hidden; width: 300px; height: 210px; }
    canvas { display: block; }
    .btn-row { display: flex; gap: 8px; margin-top: 8px; width: 300px; }
    .dodge-btn { background: linear-gradient(135deg, #ff4081, #7b1fa2); color: white; border: 2px solid #ff80ab; padding: 9px 0; font-size: 14px; font-weight: bold; border-radius: 10px; cursor: pointer; flex: 1; text-align: center; }
    .dodge-btn:active { background: #ff4081; transform: scale(0.92); }
    .start-overlay { position: absolute; top:0; left:0; width:300px; height:210px; background: rgba(26,15,48,0.92); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 20px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    </style></head><body>
    <div class="game-box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">⚡ 三轨道下落躲避灯泡</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px; text-align:center; padding:0 10px;">12秒内左右移动，避开上方掉落的 💡 故障灯泡！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始躲避挑战</button>
        </div>
        <canvas id="dodgeCanvas" width="300" height="210"></canvas>
    </div>
    <div class="btn-row">
        <button class="dodge-btn" onclick="movePlayer(-1)">⬅️ 往左</button>
        <button class="dodge-btn" style="background: linear-gradient(135deg, #ab47bc, #4a148c);" onclick="movePlayer(0)">⏺️ 居中</button>
        <button class="dodge-btn" onclick="movePlayer(1)">往右 ➡️</button>
    </div>
    <script>
        const canvas = document.getElementById('dodgeCanvas'); const ctx = canvas.getContext('2d'); const trackWidth = 100;
        let playerLane = 1, obstacles = [], score = 0, timeLeft = 12, isStarted = false, isGameOver = false, timer, spawner;

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            isStarted = true;
            timer = setInterval(() => { if(timeLeft > 0 && !isGameOver) timeLeft--; else { isGameOver = true; clearInterval(timer); clearInterval(spawner); } }, 1000);
            spawner = setInterval(() => { if(!isGameOver && isStarted) obstacles.push({ lane: Math.floor(Math.random()*3), y: -30 }); }, 700);
            loop();
        }

        function movePlayer(dir) {
            if(!isStarted || isGameOver) return;
            if(dir === 0) playerLane = 1;
            else playerLane = Math.max(0, Math.min(2, playerLane + dir));
        }

        function loop() {
            ctx.clearRect(0, 0, 300, 210); ctx.strokeStyle = '#2d1b4e';
            for(let i=1; i<3; i++) { ctx.beginPath(); ctx.moveTo(i*trackWidth, 0); ctx.lineTo(i*trackWidth, 210); ctx.stroke(); }
            
            for(let i = obstacles.length - 1; i >= 0; i--) {
                let obs = obstacles[i];
                obs.y += 3.5;
                ctx.font = '22px Arial';
                ctx.fillText('💡', obs.lane * trackWidth + 36, obs.y);
                
                if(obs.y >= 155 && obs.y <= 195 && obs.lane === playerLane) {
                    score = Math.max(0, score - 1);
                    obstacles.splice(i, 1);
                } else if(obs.y > 210) {
                    score += 1;
                    obstacles.splice(i, 1);
                }
            }

            ctx.font = '26px Arial';
            ctx.fillText('🧍‍♂️', playerLane * trackWidth + 34, 185);

            ctx.fillStyle = '#fff'; ctx.font = 'bold 11px Arial';
            ctx.fillText("⏳ 剩余: " + timeLeft + "s", 10, 18);
            ctx.fillText("🛡️ 得分: " + score, 210, 18);

            if(!isGameOver) requestAnimationFrame(loop);
            else {
                ctx.fillStyle = 'rgba(0,0,0,0.88)'; ctx.fillRect(0, 0, 300, 210);
                ctx.fillStyle = score >= 5 ? '#00e676' : '#ff5252';
                ctx.font = 'bold 15px Arial';
                ctx.fillText(score >= 5 ? "🎉 闪避挑战成功！得分: " + score : "💧 闪避不及！得分: " + score, 45, 110);
            }
        }
    </script></body></html>
    """
  components.html(html_code, height=275)


def render_dig_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .game-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; padding: 10px; width: 300px; text-align: center; }
    .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin: 8px 0; }
    .soil-tile { background: linear-gradient(135deg, #5d4037, #3e2723); border: 2px solid #8d6e63; border-radius: 8px; height: 50px; font-size: 22px; display: flex; align-items: center; justify-content: center; cursor: pointer; color: #fff; }
    .soil-tile:active { transform: scale(0.92); }
    </style></head><body>
    <div class="game-box">
        <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">⛏️ 地下仓库·9宫格3宝物盲盒挖掘</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 3px;">💎 找到宝物: <span id="digScore">0</span> / 3 | ⛏️ 剩余次数: <span id="digLeft">6</span></div>
        <div class="grid" id="digGrid"></div>
        <div id="dig-tip" style="color: #fff; font-size: 11px;">9个土块里藏着3个宝物，限挖6次！</div>
    </div>
    <script>
        let treasures = ['💎', '🎸', '📸'];
        let items = ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱', treasures[0], treasures[1], treasures[2]];
        items.sort(() => Math.random() - 0.5);

        let opened = Array(9).fill(false);
        let foundCount = 0;
        let digLeft = 6;
        let isOver = false;

        const gridEl = document.getElementById('digGrid'), tipEl = document.getElementById('dig-tip');

        function renderGrid() {
            gridEl.innerHTML = '';
            items.forEach((item, idx) => {
                let tile = document.createElement('div'); tile.className = 'soil-tile';
                tile.innerText = opened[idx] ? item : '🟫';
                tile.onclick = () => digTile(idx);
                gridEl.appendChild(tile);
            });
        }

        function digTile(idx) {
            if(isOver || opened[idx] || digLeft <= 0) return;
            opened[idx] = true;
            digLeft--;
            document.getElementById('digLeft').innerText = digLeft;

            if(items[idx] !== '🧱') {
                foundCount++;
                document.getElementById('digScore').innerText = foundCount;
                tipEl.innerHTML = "<span style='color:#00e676;'>🎉 挖到珍贵宝物 (" + items[idx] + ")！能力全面提升！</span>";
                if(foundCount >= 3) {
                    isOver = true;
                    tipEl.innerHTML = "<span style='color:#00e676;'>🎉 太神了！3个宝物全部找齐！</span>";
                }
            } else {
                tipEl.innerHTML = "<span style='color:#ff5252;'>🧱 挖到了普通泥土...</span>";
            }

            if(digLeft === 0 && foundCount < 3) {
                isOver = true;
                tipEl.innerHTML = "<span style='color:#ff5252;'>💧 挖掘次数已用完，寻宝结束！</span>";
            }
            renderGrid();
        }
        renderGrid();
    </script></body></html>
    """
  components.html(html_code, height=265)


def render_whack_mole_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .mole-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); padding: 10px; width: 300px; text-align: center; position: relative; }
    .mole-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin: 8px 0; }
    .hole { background: #211035; border: 2px solid #ab47bc; border-radius: 10px; height: 50px; font-size: 22px; display: flex; align-items: center; justify-content: center; cursor: pointer; }
    .hole:active { transform: scale(0.92); }
    .start-overlay { position: absolute; top:0; left:0; width:300px; height:100%; background: rgba(26,15,48,0.92); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 12px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    </style></head><body>
    <div class="mole-box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:10px; font-size:13px;">🔨 击退狗仔防卫战</div>
            <button class="start-btn" onclick="startGame()">▶️ 点击开始挑战</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">🔨 击退狗仔队：点击打掉偷拍镜头！</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 3px;">🔥 击退狗仔: <span id="mScore">0</span> / 8 | ⏳ <span id="mTime">14</span>s</div>
        <div class="mole-grid" id="moleGrid"></div>
        <div id="m-tip" style="color: #fff; font-size: 11px;">小心别误伤 💖 粉丝！只点击 📷 狗仔！</div>
    </div>
    <script>
        let score = 0, timeLeft = 14, isStarted = false, isOver = false, holes = Array(9).fill('🕳️'), activeIdx = -1, activeType = '', timer, spawner;
        const gridEl = document.getElementById('moleGrid'), tipEl = document.getElementById('m-tip');

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            isStarted = true;
            spawner = setInterval(() => {
                if(isOver || !isStarted) return;
                activeIdx = Math.floor(Math.random() * 9);
                activeType = Math.random() > 0.3 ? 'paparazzi' : 'fan';
                renderHoles();
            }, 600);

            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) { timeLeft--; document.getElementById('mTime').innerText = timeLeft; }
                else if(!isOver) {
                    isOver = true; clearInterval(timer); clearInterval(spawner); activeIdx = -1; renderHoles();
                    if(score >= 8) tipEl.innerHTML = "<span style='color:#00e676;'>🎉 成功击退所有偷拍狗仔！公关胜利！</span>";
                    else tipEl.innerHTML = "<span style='color:#ff5252;'>💧 击退失败！狗仔抓到了漏洞照片...</span>";
                }
            }, 1000);
            renderHoles();
        }

        function renderHoles() {
            gridEl.innerHTML = '';
            for(let i=0; i<9; i++) {
                let h = document.createElement('div'); h.className = 'hole';
                h.innerText = (i === activeIdx && isStarted) ? (activeType === 'paparazzi' ? '📷' : '💖') : '🕳️';
                h.onclick = () => hitHole(i);
                gridEl.appendChild(h);
            }
        }

        function hitHole(idx) {
            if(!isStarted || isOver || idx !== activeIdx) return;
            if(activeType === 'paparazzi') {
                score++; document.getElementById('mScore').innerText = score;
                activeIdx = -1; renderHoles();
                if(score >= 8) { isOver = true; clearInterval(timer); clearInterval(spawner); tipEl.innerHTML = "<span style='color:#00e676;'>🎉 成功击退所有偷拍狗仔！公关胜利！</span>"; }
            } else {
                score = Math.max(0, score - 2); document.getElementById('mScore').innerText = score;
                activeIdx = -1; renderHoles();
            }
        }
        renderHoles();
    </script></body></html>
    """
  components.html(html_code, height=270)


def render_snapshot_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .game-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; padding: 10px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.95); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 12px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .snap-btn { background: linear-gradient(135deg, #ff4081, #ab47bc); color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 20px; cursor: pointer; margin-top: 10px; }
    .snap-btn:active { transform: scale(0.92); }
    </style></head><body>
    <div class="game-box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">📸 杂志封面快门抓拍</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px;">当光标移动到 🎯 完美区时按下快门！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始拍摄</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">📸 快门抓拍大作战</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 3px;">✨ 成功抓拍: <span id="snapScore">0</span> / 5 | ⏳ <span id="snapTime">12</span>s</div>
        <div style="background: #211035; border: 2px solid #ab47bc; border-radius: 8px; height: 35px; margin: 12px 0; position: relative; overflow: hidden;">
            <div style="position: absolute; left: 115px; width: 70px; height: 100%; background: rgba(0, 230, 118, 0.4); border-left: 2px dashed #00e676; border-right: 2px dashed #00e676;">🎯</div>
            <div id="barCursor" style="position: absolute; left: 0px; width: 8px; height: 100%; background: #ff4081; border-radius: 4px;"></div>
        </div>
        <button class="snap-btn" onclick="takePhoto()">📷 咔嚓！按下快门</button>
        <div id="snap-tip" style="color: #fff; font-size: 11px; margin-top: 5px;">看准绿框瞬间按下！</div>
    </div>
    <script>
        let score = 0, timeLeft = 12, isStarted = false, isOver = false, cursorX = 0, dir = 3, timer, animator;
        const cursorEl = document.getElementById('barCursor'), timeEl = document.getElementById('snapTime'), scoreEl = document.getElementById('snapScore'), tipEl = document.getElementById('snap-tip');

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            isStarted = true;
            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) { timeLeft--; timeEl.innerText = timeLeft; }
                else if(!isOver) { endSnap(); }
            }, 1000);
            animator = setInterval(() => {
                if(isOver || !isStarted) return;
                cursorX += dir;
                if(cursorX <= 0 || cursorX >= 284) dir *= -1;
                cursorEl.style.left = cursorX + 'px';
            }, 20);
        }

        function takePhoto() {
            if(!isStarted || isOver) return;
            if(cursorX >= 115 && cursorX <= 185) {
                score++;
                scoreEl.innerText = score;
                tipEl.innerHTML = "<span style='color:#00e676;'>🎉 完美的封面瞬间！绝杀！</span>";
            } else {
                tipEl.innerHTML = "<span style='color:#ff5252;'>💧 拍虚了，表情没管理好！</span>";
            }
        }

        function endSnap() {
            isOver = true; clearInterval(timer); clearInterval(animator);
            if(score >= 3) { tipEl.innerHTML = "<span style='color:#00e676;'>🎉 杂志大片拍摄大成功！</span>"; }
            else { tipEl.innerHTML = "<span style='color:#ff5252;'>💧 拍摄未达标，错失封面！</span>"; }
        }
    </script></body></html>
    """
  components.html(html_code, height=275)


def render_wink_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .game-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 14px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); position: relative; overflow: hidden; width: 300px; height: 210px; }
    canvas { display: block; }
    .btn-row { display: flex; gap: 6px; margin-top: 8px; width: 300px; }
    .wink-btn { background: linear-gradient(135deg, #ff4081, #7b1fa2); color: white; border: 2px solid #ff80ab; padding: 9px 0; font-size: 13px; font-weight: bold; border-radius: 10px; cursor: pointer; flex: 1; text-align: center; }
    .wink-btn:active { background: #ff4081; transform: scale(0.92); }
    .start-overlay { position: absolute; top:0; left:0; width:300px; height:210px; background: rgba(26,15,48,0.92); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 20px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    </style></head><body>
    <div class="game-box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">🌟 三轨道下落 Wink 电眼狙击</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px; text-align:center; padding:0 10px;">10秒内左右移动，当 💖 粉丝掉落时按下发射 Wink！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始电眼巡游</button>
        </div>
        <canvas id="winkCanvas" width="300" height="210"></canvas>
    </div>
    <div class="btn-row">
        <button class="wink-btn" onclick="moveWink(-1)">⬅️ 往左</button>
        <button class="wink-btn" style="background: linear-gradient(45deg, #00e676, #00b0ff); color:#000;" onclick="winkAction()">😉 发射Wink</button>
        <button class="wink-btn" onclick="moveWink(1)">往右 ➡️</button>
    </div>
    <script>
        const canvas = document.getElementById('winkCanvas'); const ctx = canvas.getContext('2d'); const trackWidth = 100;
        let playerLane = 1, fans = [], score = 0, timeLeft = 10, isStarted = false, isGameOver = false, timer, spawner;

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            isStarted = true;
            timer = setInterval(() => { if(timeLeft > 0 && !isGameOver) timeLeft--; else { isGameOver = true; clearInterval(timer); clearInterval(spawner); } }, 1000);
            spawner = setInterval(() => { if(!isGameOver && isStarted) fans.push({ lane: Math.floor(Math.random()*3), y: -30 }); }, 800);
            loop();
        }

        function moveWink(dir) {
            if(!isStarted || isGameOver) return;
            playerLane = Math.max(0, Math.min(2, playerLane + dir));
        }

        function winkAction() {
            if(!isStarted || isGameOver) return;
            let hit = false;
            for(let i = fans.length - 1; i >= 0; i--) {
                let f = fans[i];
                if(f.y >= 130 && f.y <= 195 && f.lane === playerLane) {
                    score++;
                    fans.splice(i, 1);
                    hit = true;
                    break;
                }
            }
        }

        function loop() {
            ctx.clearRect(0, 0, 300, 210); ctx.strokeStyle = '#2d1b4e';
            for(let i=1; i<3; i++) { ctx.beginPath(); ctx.moveTo(i*trackWidth, 0); ctx.lineTo(i*trackWidth, 210); ctx.stroke(); }
            
            for(let i = fans.length - 1; i >= 0; i--) {
                let f = fans[i];
                f.y += 3.2;
                ctx.font = '22px Arial';
                ctx.fillText('💖', f.lane * trackWidth + 36, f.y);
                if(f.y > 210) { fans.splice(i, 1); }
            }

            ctx.font = '26px Arial';
            ctx.fillText('😉', playerLane * trackWidth + 34, 185);

            ctx.fillStyle = '#fff'; ctx.font = 'bold 11px Arial';
            ctx.fillText("⏳ 剩余: " + timeLeft + "s", 10, 18);
            ctx.fillText("💖 得分: " + score, 210, 18);

            if(!isGameOver) requestAnimationFrame(loop);
            else {
                ctx.fillStyle = 'rgba(0,0,0,0.88)'; ctx.fillRect(0, 0, 300, 210);
                ctx.fillStyle = score >= 4 ? '#00e676' : '#ff5252';
                ctx.font = 'bold 15px Arial';
                ctx.fillText(score >= 4 ? "🎉 电眼狙击成功！得分: " + score : "💧 表现平平！得分: " + score, 45, 110);
            }
        }
    </script></body></html>
    """
  components.html(html_code, height=275)


def render_outfit_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .game-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 14px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); position: relative; overflow: hidden; width: 300px; height: 210px; }
    canvas { display: block; }
    .btn-row { display: flex; gap: 8px; margin-top: 8px; width: 300px; }
    .outfit-btn { background: linear-gradient(135deg, #ff4081, #7b1fa2); color: white; border: 2px solid #ff80ab; padding: 9px 0; font-size: 14px; font-weight: bold; border-radius: 10px; cursor: pointer; flex: 1; text-align: center; }
    .outfit-btn:active { background: #ff4081; transform: scale(0.92); }
    .start-overlay { position: absolute; top:0; left:0; width:300px; height:210px; background: rgba(26,15,48,0.92); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 20px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    </style></head><body>
    <div class="game-box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">🧺 三轨道下落接战袍</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px; text-align:center; padding:0 10px;">12秒内移动篮子接住 🧥 战袍(+1)，避开 🧦 脏袜子(-1)！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始接物挑战</button>
        </div>
        <canvas id="outfitCanvas" width="300" height="210"></canvas>
    </div>
    <div class="btn-row">
        <button class="outfit-btn" onclick="moveBasket(-1)">⬅️ 篮子向左</button>
        <button class="outfit-btn" style="background: linear-gradient(135deg, #ab47bc, #4a148c);" onclick="moveBasket(0)">⏺️ 居中</button>
        <button class="outfit-btn" onclick="moveBasket(1)">篮子向右 ➡️</button>
    </div>
    <script>
        const canvas = document.getElementById('outfitCanvas'); const ctx = canvas.getContext('2d'); const trackWidth = 100;
        let basketLane = 1, items = [], score = 0, timeLeft = 12, isStarted = false, isGameOver = false, timer, spawner;

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            isStarted = true;
            timer = setInterval(() => { if(timeLeft > 0 && !isGameOver) timeLeft--; else { isGameOver = true; clearInterval(timer); clearInterval(spawner); } }, 1000);
            spawner = setInterval(() => {
                if(!isGameOver && isStarted) {
                    let type = Math.random() > 0.35 ? '🧥' : '🧦';
                    items.push({ lane: Math.floor(Math.random()*3), y: -30, type: type });
                }
            }, 750);
            loop();
        }

        function moveBasket(dir) {
            if(!isStarted || isGameOver) return;
            if(dir === 0) basketLane = 1;
            else basketLane = Math.max(0, Math.min(2, basketLane + dir));
        }

        function loop() {
            ctx.clearRect(0, 0, 300, 210); ctx.strokeStyle = '#2d1b4e';
            for(let i=1; i<3; i++) { ctx.beginPath(); ctx.moveTo(i*trackWidth, 0); ctx.lineTo(i*trackWidth, 210); ctx.stroke(); }
            
            for(let i = items.length - 1; i >= 0; i--) {
                let itm = items[i];
                itm.y += 3.5;
                ctx.font = '22px Arial';
                ctx.fillText(itm.type, itm.lane * trackWidth + 36, itm.y);
                
                if(itm.y >= 155 && itm.y <= 195 && itm.lane === basketLane) {
                    if(itm.type === '🧥') score += 1;
                    else score = Math.max(0, score - 1);
                    items.splice(i, 1);
                } else if(itm.y > 210) {
                    items.splice(i, 1);
                }
            }

            ctx.font = '26px Arial';
            ctx.fillText('🧺', basketLane * trackWidth + 32, 185);

            ctx.fillStyle = '#fff'; ctx.font = 'bold 11px Arial';
            ctx.fillText("⏳ 剩余: " + timeLeft + "s", 10, 18);
            ctx.fillText("🧺 得分: " + score, 210, 18);

            if(!isGameOver) requestAnimationFrame(loop);
            else {
                ctx.fillStyle = 'rgba(0,0,0,0.88)'; ctx.fillRect(0, 0, 300, 210);
                ctx.fillStyle = score >= 4 ? '#00e676' : '#ff5252';
                ctx.font = 'bold 15px Arial';
                ctx.fillText(score >= 4 ? "🎉 战袍抢救成功！得分: " + score : "💧 手忙脚乱！得分: " + score, 45, 110);
            }
        }
    </script></body></html>
    """
  components.html(html_code, height=275)


def render_memory_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .game-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; padding: 10px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.95); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 12px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .card-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin: 10px 0; }
    .mem-card { background: linear-gradient(135deg, #ab47bc, #7b1fa2); border: 1.5px solid #ff80ab; border-radius: 8px; height: 48px; font-size: 20px; display: flex; align-items: center; justify-content: center; cursor: pointer; }
    .mem-card:active { transform: scale(0.92); }
    </style></head><body>
    <div class="game-box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">🃏 应援卡记忆翻牌</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px;">30秒内翻开并配对所有粉丝应援卡！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始翻牌挑战</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">🃏 粉丝感谢祭·记忆翻牌</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 3px;">✨ 已配对: <span id="mMatch">0</span> / 4 | ⏳ <span id="mTime">30</span>s</div>
        <div class="card-grid" id="cardGrid"></div>
        <div id="mem-tip" style="color: #fff; font-size: 11px;">找出相同的应援图标进行配对！</div>
    </div>
    <script>
        let symbols = ['💖', '🌟', '🎵', '🎤', '💖', '🌟', '🎵', '🎤'];
        let cards = [], flipped = [], matchedPairs = 0, timeLeft = 30, isStarted = false, isOver = false, timer;
        const gridEl = document.getElementById('cardGrid'), timeEl = document.getElementById('mTime'), matchEl = document.getElementById('mMatch'), tipEl = document.getElementById('mem-tip');

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            isStarted = true;
            symbols.sort(() => Math.random() - 0.5);
            cards = symbols.map((s, i) => ({ id: i, symbol: s, isOpen: false, isMatched: false }));
            renderCards();
            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) { timeLeft--; timeEl.innerText = timeLeft; }
                else if(!isOver) { endMem(false); }
            }, 1000);
        }

        function renderCards() {
            gridEl.innerHTML = '';
            cards.forEach((c, idx) => {
                let card = document.createElement('div'); card.className = 'mem-card';
                card.innerText = (c.isOpen || c.isMatched) ? c.symbol : '❓';
                card.onclick = () => flipCard(idx);
                gridEl.appendChild(card);
            });
        }

        function flipCard(idx) {
            if(!isStarted || isOver || cards[idx].isOpen || cards[idx].isMatched || flipped.length >= 2) return;
            cards[idx].isOpen = true; flipped.push(idx); renderCards();
            if(flipped.length === 2) {
                let [i1, i2] = flipped;
                if(cards[i1].symbol === cards[i2].symbol) {
                    cards[i1].isMatched = true; cards[i2].isMatched = true;
                    matchedPairs++; matchEl.innerText = matchedPairs;
                    flipped = [];
                    if(matchedPairs === 4) { endMem(true); }
                } else {
                    setTimeout(() => {
                        cards[i1].isOpen = false; cards[i2].isOpen = false;
                        flipped = []; renderCards();
                    }, 600);
                }
            }
        }

        function endMem(success) {
            isOver = true; clearInterval(timer);
            if(success) { tipEl.innerHTML = "<span style='color:#00e676;'>🎉 完美记忆所有老粉应援物！</span>"; }
            else { tipEl.innerHTML = "<span style='color:#ff5252;'>💧 时间耗尽，记忆卡壳了！</span>"; }
        }
    </script></body></html>
    """
  components.html(html_code, height=275)


def render_puzzle_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .puzzle-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; padding: 10px; width: 300px; text-align: center; }
    .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin: 10px auto; width: 240px; }
    .p-tile { background: linear-gradient(135deg, #ab47bc, #7b1fa2); border: 2px solid #ff80ab; color: #fff; height: 55px; font-size: 18px; font-weight: bold; border-radius: 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
    .p-tile:active { transform: scale(0.92); }
    </style></head><body>
    <div class="puzzle-box">
        <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">🚚 巨蛋盛典：9宫格花车轨道抢修拼图</div>
        <div style="color: #fff; font-size: 11px; margin-top: 2px;">点击任意两个方块互换位置，将轨道按 1 至 9 正确排序！</div>
        <div class="grid" id="pGrid"></div>
        <div id="p-tip" style="color:#00e676; font-size:11px; font-weight:bold; margin-top:5px;">✨ 点击两两交换方块以复原轨道！</div>
    </div>
    <script>
        let board = [3, 1, 5, 2, 8, 4, 9, 6, 7];
        let target = [1, 2, 3, 4, 5, 6, 7, 8, 9];
        let firstSelected = null;
        const gridEl = document.getElementById('pGrid'), tipEl = document.getElementById('p-tip');

        function renderBoard() {
            gridEl.innerHTML = '';
            board.forEach((val, idx) => {
                let tile = document.createElement('div');
                tile.className = 'p-tile';
                tile.innerText = '🛤️' + val;
                if(firstSelected === idx) tile.style.border = '2px solid #00e676';
                tile.onclick = () => selectTile(idx);
                gridEl.appendChild(tile);
            });
        }

        function selectTile(idx) {
            if(firstSelected === null) {
                firstSelected = idx;
                renderBoard();
            } else {
                let temp = board[firstSelected];
                board[firstSelected] = board[idx];
                board[idx] = temp;
                firstSelected = null;
                renderBoard();
                checkWin();
            }
        }

        function checkWin() {
            if(board.every((v, i) => v === target[i])) {
                tipEl.innerHTML = "<span style='color:#00e676;'>🎉 9宫格轨道完美连通！花车顺利启动！</span>";
            }
        }
        renderBoard();
    </script></body></html>
    """
  components.html(html_code, height=295)


# 主标题
st.title("💖 星途闪耀：我的练习生日常")

# -------------------------------------------------------------------
# STAGE 0: 开局与甄选阶段
# -------------------------------------------------------------------
if not st.session_state.game_started:
  st.markdown(
      '<div class="cute-info">✨ 欢迎来到 STARTO 偶像养成营！请输入你的名字，选择心仪组合并抽取开局传奇幸运物！</div>',
      unsafe_allow_html=True,
  )
  name_input = st.text_input(
      "✏️ 请输入你的名字（或昵称）：", placeholder="例如：酱酱 / 小夏"
  )
  st.markdown("---")
  selected_group = st.selectbox(
      "选择你想加入/并肩作战的组合（全团按年龄排序）：",
      list(IDOL_GROUPS.keys()),
  )
  st.markdown("---")
  st.subheader("🎁 抽开局传奇幸运物扭蛋")

  if "temp_gacha" not in st.session_state:
    st.session_state.temp_gacha = ""

  if st.button("🎲 点击抽取开局传奇幸运物！"):
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
  if st.button("🚀 签订研修契约，进入甄选考核！", use_container_width=True):
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
# STAGE 0.5: 练习生甄选分流考核
# -------------------------------------------------------------------
elif not st.session_state.passed_audition:
  st.subheader("🌟 【练习生甄选大舞台】初次考核定位")
  st.markdown(
      '<div class="event-card"><b>🎯 甄选环节说明：</b><br>想要成为正式 Jr 必须通过残酷的初试！请选择你擅长的初舞台表演项目，顺利完成考核即可正式进入事务所！</div>',
      unsafe_allow_html=True,
  )

  audition_choice = st.radio(
      "请选择你的初次甄选表演项目：",
      [
          "1. 🎤 Vocal（声乐高音展示）",
          "2. Dance（动感舞步卡点）",
          "3. Rap（机关枪快嘴节奏）",
          "4. 🤹 特殊才艺杂耍（平衡道具展示）",
      ],
  )
  st.markdown("---")

  if audition_choice.startswith("1"):
    st.session_state.audition_track = "vocal"
    render_audition_vocal_game()
  elif audition_choice.startswith("2"):
    st.session_state.audition_track = "dance"
    render_audition_dance_game()
  elif audition_choice.startswith("3"):
    st.session_state.audition_track = "rap"
    render_audition_rap_game()
  else:
    st.session_state.audition_track = "variety"
    render_audition_variety_game()

  st.markdown("---")
  if st.button(
      "🌟 完成考核，接受社长与评委的最终裁决！", use_container_width=True
  ):
    # 根据不同轨道给予初始属性加成
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
# 游戏主流程（Jr 时期与黑暗面波折）
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

  # Stage 2：🎹 节奏钢琴块打歌小游戏
  elif curr_stage == 2:
    st.subheader("📍 Stage 2：【全开麦打歌·节奏钢琴块】")
    st.markdown(
        '<div class="event-card"><b>🎹 【打歌小游戏：下落式节奏钢琴块】</b><br>地方电视台录制现场！点击下方按钮敲击下落的钢琴块，达到 800 分才算通过！</div>',
        unsafe_allow_html=True,
    )
    render_piano_tiles_game()
    if st.button("➔ 演奏结束，点击进入下一阶段"):
      st.session_state.fans += 1500
      st.session_state.dance += 20
      st.session_state.stage = 3
      st.rerun()

  # Stage 6：📣 声量呐喊连击小游戏
  elif curr_stage == 6:
    st.subheader(f"📍 Stage 6：【粉丝应援大作战】与 {member} 的声量对决")
    st.markdown(
        f'<div class="event-card"><b>📣 【连击互动小游戏：声量呐喊】</b><br>街头突击宣传！20秒内疯狂点击按钮，必须达到 <b>90 下以上</b> 才能让应援声量爆表！</div>',
        unsafe_allow_html=True,
    )
    render_shout_game()
    if st.button("➔ 应援结束，点击进入下一阶段"):
      st.session_state.bond += 20
      st.session_state.variety += 20
      st.session_state.stage = 7
      st.rerun()

  # Stage 10：⚡ 舞台危机：下落式三轨道躲避灯泡
  elif curr_stage == 10:
    st.subheader("📍 Stage 10：【夏日风暴音乐节·舞台危机闪避】")
    st.markdown(
        '<div class="event-card"><b>🎮 【互动小游戏：下落式三轨道躲避灯泡】</b><br>户外音乐节舞台故障！上方不断掉落 💡 故障灯泡，使用左右按钮切换轨道进行躲避！</div>',
        unsafe_allow_html=True,
    )
    render_dodge_game()
    if st.button("➔ 危机结束，点击进入下一阶段"):
      st.session_state.fans += 2500
      st.session_state.variety += 25
      st.session_state.stage = 11
      st.rerun()

  # Stage 11：⛏️ 地下仓库：9宫格3宝物盲盒挖掘
  elif curr_stage == 11:
    st.subheader("📍 Stage 11：【事务所地下仓库·敲土块开盲盒挖宝】")
    st.markdown(
        '<div class="event-card"><b>⛏️ 【互动小游戏：9宫格3宝物挖宝】</b><br>总共 9 个土块，其中藏有 3 个宝物（金唱片/吉他/拍立得），你有 6 次挖掘机会！挖到宝物即可增加对应属性！</div>',
        unsafe_allow_html=True,
    )
    render_dig_game()
    if st.button("➔ 挖宝结束，点击进入下一阶段"):
      st.session_state.vocal += 20
      st.session_state.dance += 20
      st.session_state.fans += 1500
      st.session_state.stage = 12
      st.rerun()

  # Stage 12：🔨 击退狗仔打地鼠小游戏
  elif curr_stage == 12:
    st.subheader("📍 Stage 12：【防卫战】地下停车场狗仔队突袭！")
    st.markdown(
        '<div class="event-card"><b>🔨 【打地鼠互动小游戏：击退狗仔】</b><br>在 14 秒内点击敲击 <b>📷 狗仔</b>（击退 8 次以上），千万别误伤 <b>💖 粉丝</b>！</div>',
        unsafe_allow_html=True,
    )
    render_whack_mole_game()
    if st.button("➔ 公关结束，点击进入下一阶段"):
      st.session_state.fans += 1800
      st.session_state.trust += 15
      st.session_state.stage = 13
      st.rerun()

  # Stage 15：📸 杂志封面快门抓拍小游戏
  elif curr_stage == 15:
    st.subheader("📍 Stage 15：【杂志封面拍摄】闪光灯快门抓拍")
    st.markdown(
        '<div class="event-card"><b>📸 【互动小游戏：快门抓拍】</b><br>《Myojo》杂志封面拍摄，当光标移动到绿色目标区时点击按钮瞬间抓拍！</div>',
        unsafe_allow_html=True,
    )
    render_snapshot_game()
    if st.button("➔ 拍摄结束，点击进入下一阶段"):
      st.session_state.fans += 2000
      st.session_state.variety += 25
      st.session_state.stage = 16
      st.rerun()

  # Stage 20：🌟 下落式三轨道 Wink 电眼狙击
  elif curr_stage == 20:
    st.subheader("📍 Stage 20：【巨蛋花车巡游】下落式 Wink 电眼狙击")
    st.markdown(
        '<div class="event-card"><b>⚡ 【互动小游戏：下落式三轨道电眼狙击】</b><br>巨蛋花车巡游！上方不断掉落 💖 粉丝，移动轨道并在粉丝掉落时按下发射按钮！</div>',
        unsafe_allow_html=True,
    )
    render_wink_game()
    if st.button("➔ 巡游结束，点击进入下一阶段"):
      st.session_state.fans += 3000
      st.session_state.stage = 21
      st.rerun()

  # Stage 22：🧺 下落式三轨道篮子接物战袍抢救
  elif curr_stage == 22:
    st.subheader(f"📍 Stage 22：【演唱会暗场】与 {member} 的下落式三轨道接物战")
    st.markdown(
        f'<div class="event-card"><b>🧺 【互动小游戏：下落式三轨道接物】</b><br>暗场12秒内移动篮子接住上方掉落的 🧥 战袍(+1)，避开 🧦 脏袜子(-1)！</div>',
        unsafe_allow_html=True,
    )
    render_outfit_game()
    if st.button("➔ 换装结束，点击进入下一阶段"):
      st.session_state.fans += 2000
      st.session_state.stage = 23
      st.rerun()

  # Stage 24：🃏 记忆翻牌粉丝感谢祭小游戏
  elif curr_stage == 24:
    st.subheader("📍 Stage 24：【粉丝感谢祭】应援卡记忆考验")
    st.markdown(
        '<div class="event-card"><b>🃏 【互动小游戏：记忆翻牌】</b><br>30秒内翻开并配对所有粉丝应援卡图标！</div>',
        unsafe_allow_html=True,
    )
    render_memory_game()
    if st.button("➔ 感谢祭结束，点击进入下一阶段"):
      st.session_state.fans += 2500
      st.session_state.bond += 20
      st.session_state.stage = 25
      st.rerun()

  # Stage 27：🚚 9宫格 (3x3) 花车轨道拼图小游戏
  elif curr_stage == 27:
    st.subheader(f"📍 Stage 27：【巨蛋盛典】9宫格抢修 {member} 的花车轨道")
    st.markdown(
        '<div class="event-card"><b>🚚 【互动小游戏：9宫格轨道拼图】</b><br>点击任意两个方块互换位置，将轨道按 1 至 9 正确排序！</div>',
        unsafe_allow_html=True,
    )
    render_puzzle_game()
    if st.button("➔ 轨道复原，前往出道前夜！"):
      st.session_state.fans += 3500
      st.session_state.stage = 28
      st.rerun()

  # 📖 常规剧情章节与突发危机（包含黑暗面波折剧情）
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
        23: {
            "title": "📺 Stage 23：黄金档搞笑综艺嘉宾连线",
            "desc": "你被选为代表参加全国黄金档搞笑综艺，面对老牌主持人的尖锐提问！",
            "opt1": "自嘲爆料宿舍奇葩趣事。",
            "opt2": "展示一秒变帅气的绝技。",
            "opt3": "温情分享组合一路走来的不容易。",
        },
        25: {
            "title": "🎤 Stage 25：全国巡演千秋乐（终官场）幕后感动",
            "desc": f"全国巡演最后一场幕后，全员围在圆阵里，{member} 眼含泪光伸出手臂。",
            "opt1": "紧紧扣住大家的手，大喊：“我们是最棒的！”",
            "opt2": "给每一位队友递上润喉茶与擦汗毛巾。",
            "opt3": "拿出手机记录下大家最真实的笑容。",
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

      # 评定最高属性以生成个性化出道头衔
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
