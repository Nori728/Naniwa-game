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

# 2. 团队与成员数据
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

# 3. 样式美化（橙光游戏视觉风：高级霓虹渐变、丝滑卡片）
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
  st.session_state.stage = 1
  st.session_state.player_name = ""
  st.session_state.group = ""
  st.session_state.lucky_item = ""

  st.session_state.energy = 100
  st.session_state.stress = 20
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


# -------------------------------------------------------------------
# 🎮 小游戏 1：经典钢琴块打歌
# -------------------------------------------------------------------
def render_piano_tiles_game():
  html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .piano-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 14px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); position: relative; overflow: hidden; width: 300px; height: 220px; }
            canvas { display: block; }
            .btn-row { display: flex; gap: 6px; margin-top: 8px; width: 300px; }
            .piano-btn { background: linear-gradient(180deg, #ab47bc, #7b1fa2); color: white; border: 2px solid #ff80ab; padding: 10px 0; font-size: 16px; font-weight: bold; border-radius: 10px; cursor: pointer; flex: 1; text-align: center; }
            .piano-btn:active { background: #ff4081; transform: scale(0.92); }
        </style>
    </head>
    <body>
        <div class="piano-box"><canvas id="pianoCanvas" width="300" height="220"></canvas></div>
        <div class="btn-row">
            <button class="piano-btn" onclick="tapTrack(0)">1</button>
            <button class="piano-btn" onclick="tapTrack(1)">2</button>
            <button class="piano-btn" onclick="tapTrack(2)">3</button>
            <button class="piano-btn" onclick="tapTrack(3)">4</button>
        </div>
        <script>
            const canvas = document.getElementById('pianoCanvas');
            const ctx = canvas.getContext('2d');
            const trackWidth = 75;
            let tiles = [], score = 0, combo = 0, timeLeft = 12, isGameOver = false;
            let timer = setInterval(() => { if(timeLeft > 0 && !isGameOver) timeLeft--; else { isGameOver = true; clearInterval(timer); clearInterval(spawner); } }, 1000);
            let spawner = setInterval(() => { if(!isGameOver) tiles.push({ track: Math.floor(Math.random()*4), y: -35, h: 35, hit: false }); }, 550);
            function tapTrack(idx) {
                if(isGameOver) return;
                let ok = false;
                for(let t of tiles) {
                    if(t.track === idx && !t.hit && t.y >= 120 && t.y <= 210) { t.hit = true; ok = true; score += 100; combo++; break; }
                }
                if(!ok) combo = 0;
            }
            function loop() {
                ctx.clearRect(0, 0, 300, 220);
                ctx.strokeStyle = '#2d1b4e';
                for(let i=1; i<4; i++) { ctx.beginPath(); ctx.moveTo(i*trackWidth, 0); ctx.lineTo(i*trackWidth, 220); ctx.stroke(); }
                ctx.fillStyle = 'rgba(255, 64, 129, 0.2)'; ctx.fillRect(0, 150, 300, 50);
                for(let i=tiles.length-1; i>=0; i--) {
                    let t = tiles[i];
                    if(!t.hit) {
                        t.y += 3.5;
                        ctx.fillStyle = '#211035'; ctx.fillRect(t.track*trackWidth+4, t.y, trackWidth-8, t.h);
                        ctx.strokeStyle = '#ea80fc'; ctx.strokeRect(t.track*trackWidth+4, t.y, trackWidth-8, t.h);
                        ctx.fillStyle = '#ff80ab'; ctx.font = '11px Arial'; ctx.fillText('🎵', t.track*trackWidth+26, t.y+22);
                        if(t.y > 220) { tiles.splice(i, 1); combo = 0; }
                    } else { tiles.splice(i, 1); }
                }
                ctx.fillStyle = '#fff'; ctx.font = 'bold 11px Arial';
                ctx.fillText("⏳ 剩余: " + timeLeft + "s", 10, 18);
                ctx.fillText("🔥 分数: " + score, 120, 18);
                ctx.fillText("⚡ Combo: " + combo, 210, 18);
                if(!isGameOver) requestAnimationFrame(loop);
                else { ctx.fillStyle = 'rgba(0,0,0,0.8)'; ctx.fillRect(0,0,300,220); ctx.fillStyle = '#00e676'; ctx.font = 'bold 16px Arial'; ctx.fillText("🎉 打歌结束！总分: " + score, 45, 115); }
            }
            loop();
        </script>
    </body>
    </html>
    """
  components.html(html_code, height=295)


# -------------------------------------------------------------------
# ⛏️ 小游戏 2：盲盒挖宝
# -------------------------------------------------------------------
def render_dirt_dig_game():
  html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .dig-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 14px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); padding: 10px; width: 300px; text-align: center; }
            .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin: 8px 0; }
            .dirt-tile { background: #5d4037; border: 2px solid #8d6e63; color: #d7ccc8; height: 42px; border-radius: 8px; font-size: 11px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 3px 5px rgba(0,0,0,0.3); }
            .dirt-tile:active { transform: scale(0.95); }
            .dirt-tile.dug { background: #3e2723; border: 2px dashed #6d4c41; color: #fff; cursor: default; }
            #dig-tip { color: #ffeb3b; font-size: 11px; font-weight: bold; min-height: 18px; }
        </style>
    </head>
    <body>
        <div class="dig-box">
            <div style="color: #fff; font-weight: bold; font-size: 11px;">⛏️ 用铁锹敲开土块！(剩余铲子: <span id="shovels">6</span>)</div>
            <div class="grid" id="dirtGrid"></div>
            <div id="dig-tip">点击土块挖掘宝物转化为实际属性！</div>
        </div>
        <script>
            let tiles = Array(12).fill(false);
            let contents = Array(12).fill('💨 空');
            let shovels = 6;
            let treasuresFound = 0;
            let isOver = false;

            let placed = 0;
            const prizePool = ['💎 金唱片(+500粉)', '✨ 签名照(+15绊)', '🏆 奖杯(+20能力)'];
            while(placed < 3) {
                let idx = Math.floor(Math.random() * 12);
                if(!tiles[idx]) {
                    tiles[idx] = true;
                    contents[idx] = prizePool[placed % prizePool.length];
                    placed++;
                }
            }

            const gridEl = document.getElementById('dirtGrid');
            const tipEl = document.getElementById('dig-tip');
            const shovelEl = document.getElementById('shovels');

            function renderGrid() {
                gridEl.innerHTML = '';
                for(let i=0; i<12; i++) {
                    let btn = document.createElement('div');
                    btn.className = 'dirt-tile';
                    btn.innerHTML = '🧱 土块';
                    btn.onclick = () => digTile(i, btn);
                    gridEl.appendChild(btn);
                }
            }

            function digTile(idx, el) {
                if (isOver || shovels <= 0 || el.classList.contains('dug')) return;
                shovels--;
                shovelEl.innerText = shovels;
                el.classList.add('dug');

                if (tiles[idx]) {
                    el.innerHTML = contents[idx];
                    el.style.background = '#00e676';
                    el.style.color = '#000';
                    treasuresFound++;
                    tipEl.innerHTML = "🎉 挖到 " + contents[idx] + "！";
                    tipEl.style.color = "#00e676";
                    if (treasuresFound === 3 || shovels === 0) {
                        isOver = true;
                        tipEl.innerHTML = "🏆 挖宝完成！共获得 " + treasuresFound + " 件宝物！";
                    }
                } else {
                    el.innerHTML = '🕳️ 泥土';
                    tipEl.innerHTML = "💧 这块土下面什么都没有...";
                    tipEl.style.color = "#ff5252";
                    if (shovels === 0) {
                        isOver = true;
                        tipEl.innerHTML = "💧 铲子用光啦！找到 " + treasuresFound + " 件宝物！";
                    }
                }
            }
            renderGrid();
        </script>
    </body>
    </html>
    """
  components.html(html_code, height=255)


# -------------------------------------------------------------------
# 🔥 小游戏 3：小分队企划多选题
# -------------------------------------------------------------------
def render_unit_selection_game():
  html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .unit-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 14px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); padding: 10px; width: 300px; text-align: center; }
            .question-title { color: #ffeb3b; font-weight: bold; font-size: 12px; margin-bottom: 4px; line-height: 1.4; }
            .card-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; margin: 8px 0; }
            .concept-card { background: linear-gradient(135deg, #4a148c, #7b1fa2); border: 2px solid #ff4081; color: #fff; padding: 8px 6px; border-radius: 8px; font-size: 11px; font-weight: bold; cursor: pointer; min-height: 38px; display: flex; align-items: center; justify-content: center; text-align: center; }
            .concept-card:active { transform: scale(0.95); }
            .concept-card.selected { background: #00e676; color: #000; border-color: #fff; }
            .submit-btn { background: linear-gradient(45deg, #ff4081, #ab47bc); color: white; border: none; padding: 7px 0; font-size: 12px; font-weight: bold; border-radius: 8px; cursor: pointer; width: 100%; margin-top: 4px; }
            #unit-tip { color: #fff; font-size: 11px; font-weight: bold; min-height: 18px; margin-top: 4px; }
        </style>
    </head>
    <body>
        <div class="unit-box">
            <div style="color: #fff; font-weight: bold; font-size: 11px;">🏆 小分队企划考题选拔 (至少选2个正确项)</div>
            <div class="question-title" id="qText">加载中...</div>
            
            <div class="card-grid" id="cardContainer"></div>
            <button class="submit-btn" onclick="submitAnswers()">✨ 提交企划答案</button>
            <div id="unit-tip">点击卡片多选，选好后点击提交！</div>
        </div>
        <script>
            const questions = [
                {
                    title: "题目1：为了迎合年度巨蛋巡演，小分队单曲必须具备哪些现场爆发力？",
                    options: [
                        {text: "🔥 炸裂齐舞", correct: true},
                        {text: "🤡 纯搞笑串场", correct: false},
                        {text: "✨ 耀眼灯光应援配合", correct: true},
                        {text: "💤 慢节奏摇篮曲", correct: false}
                    ]
                },
                {
                    title: "题目2：在电视台打歌节目中，如何让新人小分队瞬间抓住观众眼球？",
                    options: [
                        {text: "🎸 强劲摇滚乐队编曲", correct: true},
                        {text: "📷 镜头前绝杀 Wink 放电", correct: true},
                        {text: "📖 来段精彩绝伦的一发技", correct: false},
                        {text: "🧍 呆立舞台毫无表情", correct: false}
                    ]
                },
                {
                    title: "题目3：当粉丝票选暗黑吸血鬼主题时，你们需要展现的舞台特质是？",
                    options: [
                        {text: "🌙 极致神秘张力", correct: true},
                        {text: "🎈 幼儿园童趣风格", correct: false},
                        {text: "⚡ 高燃高音爆发", correct: true},
                        {text: "🍲 在台上现场煮拉面", correct: false}
                    ]
                }
            ];

            const currentQ = questions[Math.floor(Math.random() * questions.length)];
            document.getElementById('qText').innerText = currentQ.title;

            let selectedIndices = [];
            const container = document.getElementById('cardContainer');
            const tipEl = document.getElementById('unit-tip');

            function renderCards() {
                container.innerHTML = '';
                currentQ.options.forEach((opt, idx) => {
                    let card = document.createElement('div');
                    card.className = 'concept-card' + (selectedIndices.includes(idx) ? ' selected' : '');
                    card.innerText = opt.text;
                    card.onclick = () => toggleSelect(idx);
                    container.appendChild(card);
                });
            }

            function toggleSelect(idx) {
                if (selectedIndices.includes(idx)) {
                    selectedIndices = selectedIndices.filter(i => i !== idx);
                } else {
                    if (selectedIndices.length < 3) {
                        selectedIndices.push(idx);
                    }
                }
                renderCards();
            }

            function submitAnswers() {
                let correctSelected = selectedIndices.filter(idx => currentQ.options[idx].correct).length;
                if (correctSelected >= 2) {
                    tipEl.innerHTML = "🎉 答题成功！企划完美，小分队出道！";
                    tipEl.style.color = "#00e676";
                } else {
                    tipEl.innerHTML = "💧 未达到至少2个正确项，企划遗憾流产！";
                    tipEl.style.color = "#ff5252";
                }
            }

            renderCards();
        </script>
    </body>
    </html>
    """
  components.html(html_code, height=275)


# -------------------------------------------------------------------
# ⚡ Wink大神：巨蛋巡演·全场电眼狙击战
# -------------------------------------------------------------------
def render_eyecatch_game():
  html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .game-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 14px; box-shadow: 0 6px 20px rgba(255,64,129,0.4); position: relative; overflow: hidden; width: 300px; height: 230px; }
            canvas { display: block; }
            .ctrl-panel { display: flex; gap: 6px; margin-top: 8px; width: 300px; justify-content: center; }
            .m-btn { background: linear-gradient(45deg, #ff4081, #ab47bc); color: white; border: none; padding: 10px 0; font-size: 13px; font-weight: bold; border-radius: 10px; cursor: pointer; flex: 1; box-shadow: 0 3px 8px rgba(0,0,0,0.3); }
            .m-btn:active { transform: scale(0.95); background: #00e676; color: #000; }
        </style>
    </head>
    <body>
        <div class="game-box"><canvas id="eyeCanvas" width="300" height="230"></canvas></div>
        <div class="ctrl-panel">
            <button class="m-btn" onclick="movePlayer(-1)">⬅️ 往左移动</button>
            <button class="m-btn" onclick="fireWink()">⚡ 发射电眼！</button>
            <button class="m-btn" onclick="movePlayer(1)">往右移动 ➡️</button>
        </div>
        <script>
            const canvas = document.getElementById('eyeCanvas');
            const ctx = canvas.getContext('2d');
            let lane = 1, lanesX = [55, 150, 245], playerY = 190;
            let items = [], score = 0, hp = 3, timeLeft = 15, isGameOver = false;
            let laserEffect = null;

            let timer = setInterval(() => { 
                if(timeLeft > 0 && !isGameOver) timeLeft--; 
                else { isGameOver = true; clearInterval(timer); clearInterval(spawner); } 
            }, 1000);

            let spawner = setInterval(() => { 
                if(!isGameOver) {
                    let type = Math.random() > 0.35 ? 'heart' : 'bomb';
                    items.push({ lane: Math.floor(Math.random()*3), y: -20, speed: 3.2, type: type }); 
                }
            }, 600);

            function movePlayer(dir) { 
                if(!isGameOver) { lane += dir; if(lane < 0) lane = 0; if(lane > 2) lane = 2; } 
            }

            function fireWink() {
                if(isGameOver) return;
                laserEffect = { lane: lane, timer: 12 };
                
                for(let i = items.length - 1; i >= 0; i--) {
                    let it = items[i];
                    if(it.lane === lane && it.y >= 80 && it.y <= 210) {
                        if(it.type === 'heart') {
                            score += 200;
                        } else {
                            hp--; 
                            if(hp <= 0) isGameOver = true;
                        }
                        items.splice(i, 1);
                        break;
                    }
                }
            }

            function loop() {
                ctx.clearRect(0, 0, 300, 230);
                
                ctx.strokeStyle = 'rgba(255, 128, 171, 0.15)'; ctx.lineWidth = 1.5; ctx.setLineDash([4, 4]);
                [100, 200].forEach(x => { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 230); ctx.stroke(); });
                ctx.setLineDash([]);

                for (let i = items.length - 1; i >= 0; i--) {
                    let it = items[i]; it.y += it.speed;
                    ctx.font = '20px Arial';
                    ctx.fillText(it.type === 'heart' ? '💖' : '💣', lanesX[it.lane]-10, it.y+10);
                    if (it.y > 230) items.splice(i, 1);
                }

                if(laserEffect && laserEffect.timer > 0) {
                    ctx.strokeStyle = '#00ffff'; ctx.lineWidth = 4;
                    ctx.shadowBlur = 15; ctx.shadowColor = '#00ffff';
                    ctx.beginPath();
                    ctx.moveTo(lanesX[laserEffect.lane], playerY);
                    ctx.lineTo(lanesX[laserEffect.lane], 0);
                    ctx.stroke();
                    ctx.shadowBlur = 0;
                    laserEffect.timer--;
                }

                let px = lanesX[lane];
                ctx.font = '24px Arial';
                ctx.fillText('🌟', px-12, playerY+10);

                ctx.fillStyle = '#fff'; ctx.font = 'bold 11px Arial';
                ctx.fillText("⏱️ 倒计时: " + timeLeft + "s", 10, 18);
                ctx.fillText("💖 得分: " + score, 110, 18);
                ctx.fillStyle = '#ff5252'; ctx.fillText("❤️ " + "❤️".repeat(Math.max(0, hp)), 210, 18);

                if (!isGameOver) requestAnimationFrame(loop);
                else { 
                    ctx.fillStyle = 'rgba(0,0,0,0.88)'; ctx.fillRect(0,0,300,230); 
                    ctx.fillStyle = '#00e676'; ctx.font = 'bold 16px Arial'; 
                    ctx.fillText("🎉 电眼狙击秀圆满成功！", 55, 115); 
                    ctx.fillStyle = '#ffeb3b'; ctx.font = '13px Arial';
                    ctx.fillText("最终得分: " + score, 110, 140);
                }
            }
            loop();
        </script>
    </body>
    </html>
    """
  components.html(html_code, height=295)


# -------------------------------------------------------------------
# 📸 杂志封面快门抓拍
# -------------------------------------------------------------------
def render_magazine_photo_game():
  html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .photo-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 14px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); padding: 10px; width: 300px; text-align: center; }
            .viewfinder { background: linear-gradient(135deg, #2b1055, #4a148c); border: 3px dashed #00e676; border-radius: 10px; padding: 12px; margin: 8px 0; color: #fff; font-size: 15px; font-weight: bold; }
            .photo-btns { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin-top: 8px; }
            .p-btn { background: linear-gradient(180deg, #ff4081, #7b1fa2); color: white; border: 1.5px solid #ff80ab; padding: 10px 0; font-size: 12px; font-weight: bold; border-radius: 8px; cursor: pointer; }
            .p-btn:active { transform: scale(0.95); background: #00e676; color: #000; }
        </style>
    </head>
    <body>
        <div class="photo-box">
            <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">📸 杂志封面拍摄：闪光灯快门抓拍！</div>
            <div style="color: #fff; font-size: 11px; margin-top: 2px;">看准监视器，捕捉模特最完美的瞬间！</div>
            <div class="viewfinder" id="targetPose">✨ 捕捉侧颜绝杀</div>
            <div style="color: #00e676; font-size: 11px; font-weight: bold;">🔥 完美快门: <span id="pScore">0</span> / 6 | ⏳ <span id="pTime">10</span>s</div>
            <div class="photo-btns">
                <button class="p-btn" onclick="pressPhoto('侧颜')">📷 侧颜</button>
                <button class="p-btn" onclick="pressPhoto('大笑')">😁 大笑</button>
                <button class="p-btn" onclick="pressPhoto('眼神')">👀 眼神</button>
            </div>
        </div>
        <script>
            const poses = [
                { type: '侧颜', label: '✨ 监视器指示：【捕捉侧颜绝杀】' },
                { type: '大笑', label: '😁 监视器指示：【抓拍阳光大笑】' },
                { type: '眼神', label: '👀 监视器指示：【锁定电眼特写】' }
            ];
            let currentPose = poses[0], score = 0, timeLeft = 10, isOver = false;

            function nextPose() {
                if (isOver) return;
                currentPose = poses[Math.floor(Math.random() * poses.length)];
                document.getElementById('targetPose').innerText = currentPose.label;
            }

            let timer = setInterval(() => {
                if (timeLeft > 0 && !isOver) {
                    timeLeft--; document.getElementById('pTime').innerText = timeLeft;
                } else {
                    isOver = true; clearInterval(timer);
                    document.getElementById('targetPose').innerText = score >= 6 ? "🎉 杂志封面大片完美诞生！" : "快门按得有点手忙脚乱...";
                }
            }, 1000);

            function pressPhoto(type) {
                if (isOver) return;
                if (type === currentPose.type) {
                    score++;
                    document.getElementById('pScore').innerText = score;
                    if (score >= 6) {
                        isOver = true;
                        document.getElementById('targetPose').innerText = "🎉 杂志封面大片完美诞生！";
                    } else {
                        nextPose();
                    }
                }
            }
            nextPose();
        </script>
    </body>
    </html>
    """
  components.html(html_code, height=275)


# -------------------------------------------------------------------
# 🪵 带指针的平衡木挑战
# -------------------------------------------------------------------
def render_balance_game():
  html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .bal-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 14px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); padding: 10px; width: 300px; text-align: center; }
            .bar-container { background: #211035; border: 2px solid #ff4081; border-radius: 10px; height: 38px; margin: 8px 0; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; }
            .balance-bar { position: absolute; width: 100%; height: 100%; display: flex; justify-content: space-around; align-items: center; padding: 0 10px; box-sizing: border-box; }
            .zone { font-size: 11px; font-weight: bold; color: rgba(255,255,255,0.4); }
            .zone.active { color: #ffeb3b; text-shadow: 0 0 8px #ff4081; }
            .pointer { position: absolute; width: 6px; height: 32px; background: #00e676; border-radius: 3px; box-shadow: 0 0 10px #00e676; transition: left 0.15s ease; left: 144px; top: 3px; }
            .bal-btns { display: flex; gap: 8px; margin-top: 8px; }
            .b-btn { background: linear-gradient(180deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 0; font-size: 13px; font-weight: bold; border-radius: 8px; cursor: pointer; flex: 1; }
            .b-btn:active { transform: scale(0.95); }
        </style>
    </head>
    <body>
        <div class="bal-box">
            <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">🪵 后台热身：顶杂志平衡木挑战！</div>
            <div style="color: #fff; font-size: 11px; margin-top: 2px;">看指针偏向哪边，点击对应按钮拉回中心！</div>
            
            <div class="bar-container">
                <div class="balance-bar">
                    <span class="zone" id="zLeft">⬅️ 左倾</span>
                    <span class="zone active" id="zCenter">⭐ 中心平衡</span>
                    <span class="zone" id="zRight">右倾 ➡️</span>
                </div>
                <div class="pointer" id="balPointer"></div>
            </div>

            <div style="color: #00e676; font-size: 11px; font-weight: bold;">🔥 稳定得分: <span id="balScore">0</span> / 6 | ⏳ <span id="balTime">10</span>s</div>
            <div class="bal-btns">
                <button class="b-btn" onclick="shiftBal(-1)">⬅️ 点左边拉回</button>
                <button class="b-btn" onclick="shiftBal(1)">点右边拉回 ➡️</button>
            </div>
        </div>
        <script>
            let targetPos = 0; 
            let score = 0, timeLeft = 10, isOver = false;

            function nextTarget() {
                if (isOver) return;
                targetPos = Math.floor(Math.random() * 3) - 1; 
                updateVisuals();
            }

            function updateVisuals() {
                const pointer = document.getElementById('balPointer');
                const zLeft = document.getElementById('zLeft');
                const zCenter = document.getElementById('zCenter');
                const zRight = document.getElementById('zRight');

                zLeft.className = 'zone' + (targetPos === -1 ? ' active' : '');
                zCenter.className = 'zone' + (targetPos === 0 ? ' active' : '');
                zRight.className = 'zone' + (targetPos === 1 ? ' active' : '');

                if (targetPos === -1) pointer.style.left = '45px';
                if (targetPos === 0) pointer.style.left = '144px';
                if (targetPos === 1) pointer.style.left = '243px';
            }

            let timer = setInterval(() => {
                if (timeLeft > 0 && !isOver) {
                    timeLeft--; document.getElementById('balTime').innerText = timeLeft;
                } else {
                    isOver = true; clearInterval(timer);
                    document.getElementById('balPointer').style.background = '#ff5252';
                }
            }, 1000);

            function shiftBal(dir) {
                if (isOver) return;
                if (dir === targetPos) {
                    score++;
                    document.getElementById('balScore').innerText = score;
                    if (score >= 6) {
                        isOver = true;
                        document.getElementById('zCenter').innerText = "🎉 完美通关！";
                    } else {
                        nextTarget();
                    }
                } else {
                    score = Math.max(0, score - 1);
                    document.getElementById('balScore').innerText = score;
                }
            }
            nextTarget();
        </script>
    </body>
    </html>
    """
  components.html(html_code, height=275)


def render_pancake_stack_game(member_name):
  html_code = (
      """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .pancake-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); padding: 8px; width: 300px; text-align: center; }
            canvas { display: block; margin: 0 auto; background: #211035; border-radius: 8px; border: 1.5px solid #ff4081; }
            .drop-btn { background: linear-gradient(45deg, #ff4081, #ab47bc); color: white; border: none; padding: 8px 0; font-size: 13px; font-weight: bold; border-radius: 12px; cursor: pointer; width: 280px; margin-top: 6px; box-shadow: 0 3px 8px rgba(255,64,129,0.4); }
            .drop-btn:active { transform: scale(0.95); }
        </style>
    </head>
    <body>
        <div class="pancake-box">
            <div style="color: #ffeb3b; font-weight: bold; font-size: 11px; margin-bottom: 3px;">🥞 后台互动：与 """
      + member_name
      + """ 的松饼叠高挑战！</div>
            <canvas id="pancakeCanvas" width="280" height="165"></canvas>
            <button class="drop-btn" onclick="dropPancake()">🥞 看准时机：放下松饼！</button>
        </div>
        <script>
            const canvas = document.getElementById('pancakeCanvas');
            const ctx = canvas.getContext('2d');

            let swingX = 140, swingDir = 2.0;
            let stack = [{x: 95, y: 140, w: 90, h: 18}];
            let current = {x: 140, y: 30, w: 80, h: 18, dropping: false, vy: 3.5};
            let score = 0, isGameOver = false;
            let memberComment = "加油！看准中心叠上去！";

            function dropPancake() {
                if (isGameOver || current.dropping) return;
                current.dropping = true;
                current.x = swingX - current.w / 2;
                current.vy = 3.5;
            }

            function drawRoundedRect(ctx, x, y, width, height, radius) {
                ctx.beginPath();
                ctx.moveTo(x + radius, y);
                ctx.lineTo(x + width - radius, y);
                ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
                ctx.lineTo(x + width, y + height - radius);
                ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
                ctx.lineTo(x + radius, y + height);
                ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
                ctx.lineTo(x, y + radius);
                ctx.quadraticCurveTo(x, y, x + radius, y);
                ctx.closePath();
                ctx.fill();
            }

            function drawPancakeEntity(ctx, x, y, w, h, isBase) {
                ctx.fillStyle = '#d4a373';
                drawRoundedRect(ctx, x, y, w, h, 5);
                ctx.strokeStyle = '#bc6c25';
                ctx.lineWidth = 1.5;
                ctx.stroke();

                ctx.fillStyle = '#faedcd';
                ctx.fillRect(x + 8, y + 5, w - 16, 3);

                if (isBase || y < 120) {
                    ctx.fillStyle = '#ffffff';
                    ctx.beginPath();
                    ctx.arc(x + w / 2, y + 3, 6, 0, Math.PI * 2);
                    ctx.fill();
                }
            }

            function loop() {
                ctx.clearRect(0, 0, 280, 165);

                ctx.fillStyle = '#2d1b4e';
                ctx.fillRect(5, 4, 125, 24);
                ctx.fillStyle = '#00e676'; ctx.font = 'bold 10px Arial';
                ctx.fillText("🧑‍🎤 你 (层数: " + score + ")", 10, 20);

                ctx.fillStyle = '#2d1b4e';
                ctx.fillRect(150, 4, 125, 24);
                ctx.fillStyle = '#ff80ab'; ctx.font = 'bold 10px Arial';
                ctx.fillText("🌟 """ + member_name + """", 155, 20);

                if (!current.dropping && !isGameOver) {
                    swingX += swingDir;
                    if (swingX > 210 || swingX < 70) swingDir *= -1;
                    ctx.strokeStyle = '#ff80ab'; ctx.lineWidth = 1.5;
                    ctx.beginPath(); ctx.moveTo(swingX, 32); ctx.lineTo(swingX, 48); ctx.stroke();
                } else if (current.dropping) {
                    current.y += current.vy;
                    let top = stack[stack.length - 1];
                    if (current.y + current.h >= top.y) {
                        current.dropping = false;
                        let overlap = Math.min(current.x + current.w, top.x + top.w) - Math.max(current.x, top.x);
                        if (overlap > 20) {
                            score++;
                            let newW = Math.max(40, current.w - 4);
                            stack.push({ x: current.x, y: top.y - 18, w: newW, h: 18 });
                            current = { x: 140, y: 30, w: newW, h: 18, dropping: false, vy: 3.5 };
                            memberComment = score >= 5 ? "太稳了！绝佳默契！" : "干得漂亮！继续保持！";
                            if (stack.length >= 6) isGameOver = true;
                        } else {
                            memberComment = "哎呀歪了！太可惜啦！";
                            isGameOver = true;
                        }
                    }
                }

                for (let i = 0; i < stack.length; i++) {
                    let p = stack[i];
                    drawPancakeEntity(ctx, p.x, p.y, p.w, p.h, i === 0);
                }

                if (!isGameOver) {
                    let drawX = current.dropping ? current.x : (swingX - current.w / 2);
                    drawPancakeEntity(ctx, drawX, current.dropping ? current.y : 48, current.w, current.h, false);
                }

                ctx.fillStyle = 'rgba(0,0,0,0.4)';
                ctx.fillRect(0, 146, 280, 19);
                ctx.fillStyle = '#ffeb3b'; ctx.font = '10px Arial';
                ctx.fillText("💬 队友 """ + member_name + """: " + memberComment, 10, 160);

                if (isGameOver) {
                    ctx.fillStyle = 'rgba(0,0,0,0.85)'; ctx.fillRect(0, 0, 280, 165);
                    ctx.fillStyle = '#00e676'; ctx.font = 'bold 15px Arial';
                    ctx.fillText("🎉 堆高完成！总得分: " + score, 40, 90);
                } else {
                    requestAnimationFrame(loop);
                }
            }
            loop();
        </script>
    </body>
    </html>
    """
  )
  components.html(html_code, height=245)


def render_wardrobe_qte_game(member_name):
  html_code = (
      """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .qte-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); padding: 10px; width: 300px; text-align: center; }
            .qte-target { font-size: 24px; background: #2d1b4e; border: 2px dashed #ff4081; border-radius: 10px; padding: 8px; margin: 8px 0; color: #fff; }
            .qte-btns { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; margin-top: 8px; }
            .q-btn { background: linear-gradient(45deg, #ff4081, #ab47bc); color: white; border: none; padding: 10px 0; font-size: 13px; font-weight: bold; border-radius: 10px; cursor: pointer; }
            .q-btn:active { transform: scale(0.95); }
        </style>
    </head>
    <body>
        <div class="qte-box">
            <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">⏱️ 演唱会暗场 30 秒：紧急换装 QTE！</div>
            <div style="color: #fff; font-size: 11px; margin-top: 3px;">"""
      + member_name
      + """ 帮你一把！点击匹配动作！</div>
            <div class="qte-target" id="targetAction">🧥 扣上战袍纽扣</div>
            <div style="color: #00e676; font-size: 11px; font-weight: bold;">🔥 连击: <span id="qteScore">0</span> / 5 | ⏳ <span id="qTime">10</span>s</div>
            <div class="qte-btns">
                <button class="q-btn" onclick="pressQTE('扣纽扣')">🧥 扣纽扣</button>
                <button class="q-btn" onclick="pressQTE('戴耳返')">🎧 戴耳返</button>
                <button class="q-btn" onclick="pressQTE('拿话筒')">🎤 拿话筒</button>
                <button class="q-btn" onclick="pressQTE('正领带')">👔 正领带</button>
            </div>
        </div>
        <script>
            const actions = ['扣纽扣', '戴耳返', '拿话筒', '正领带'];
            const actionIcons = { '扣纽扣': '🧥 扣上战袍纽扣', '戴耳返': '🎧 戴上无线耳返', '拿话筒': '🎤 拿起定制话筒', '正领带': '👔 整理演出领带' };
            let current = '扣纽扣', score = 0, timeLeft = 10, isOver = false;

            function nextAction() {
                if (isOver) return;
                current = actions[Math.floor(Math.random() * actions.length)];
                document.getElementById('targetAction').innerText = actionIcons[current];
            }

            let timer = setInterval(() => {
                if (timeLeft > 0 && !isOver) {
                    timeLeft--; document.getElementById('qTime').innerText = timeLeft;
                } else {
                    isOver = true; clearInterval(timer);
                    document.getElementById('targetAction').innerText = score >= 5 ? "🎉 换装成功！登场！" : "💧 时间到！手忙脚乱...";
                }
            }, 1000);

            function pressQTE(act) {
                if (isOver) return;
                if (act === current) {
                    score++;
                    document.getElementById('qteScore').innerText = score;
                    if (score >= 5) {
                        isOver = true;
                        document.getElementById('targetAction').innerText = "🎉 换装成功！登场！";
                    } else {
                        nextAction();
                    }
                }
            }
            nextAction();
        </script>
    </body>
    </html>
    """
  )
  components.html(html_code, height=270)


def render_member_duel_game(member_name):
  html_code = (
      """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .duel-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); padding: 10px; width: 300px; text-align: center; }
            .vs-display { display: flex; justify-content: space-around; align-items: center; margin: 10px 0; color: #fff; font-size: 14px; font-weight: bold; }
            .avatar { background: #2d1b4e; border: 2px solid #ff4081; border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; font-size: 20px; margin: 0 auto 4px auto; }
            .duel-btns { display: flex; gap: 6px; margin-top: 8px; }
            .d-btn { background: linear-gradient(45deg, #ff4081, #ab47bc); color: white; border: none; padding: 10px 0; font-size: 14px; font-weight: bold; border-radius: 10px; cursor: pointer; flex: 1; box-shadow: 0 3px 8px rgba(0,0,0,0.3); }
            .d-btn:active { transform: scale(0.95); }
            #duel-result { color: #ffeb3b; font-size: 12px; font-weight: bold; margin-top: 8px; min-height: 20px; }
        </style>
    </head>
    <body>
        <div class="duel-box">
            <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">🤝 与 """
      + member_name
      + """ 的后台猜拳对决！</div>
            <div class="vs-display">
                <div>
                    <div class="avatar">🧑‍🎤</div>
                    <div>你</div>
                    <div id="playerChoice" style="font-size: 18px; margin-top: 3px;">❓</div>
                </div>
                <div style="color:#ff4081; font-size: 18px; font-weight:bold;">VS</div>
                <div>
                    <div class="avatar">🌟</div>
                    <div>"""
      + member_name
      + """</div>
                    <div id="memberChoice" style="font-size: 18px; margin-top: 3px;">❓</div>
                </div>
            </div>
            <div id="duel-result">请出拳，赢过 """
      + member_name
      + """ 提升羁绊！</div>
            <div class="duel-btns">
                <button class="d-btn" onclick="playDuel('石头')">✊ 石头</button>
                <button class="d-btn" onclick="playDuel('剪刀')">✌️ 剪刀</button>
                <button class="d-btn" onclick="playDuel('布')">🖐️ 布</button>
            </div>
        </div>
        <script>
            const choices = ['石头', '剪刀', '布'];
            const icons = { '石头': '✊', '剪刀': '✌️', '布': '🖐️' };
            let wins = 0;

            function playDuel(pChoice) {
                let mChoice = choices[Math.floor(Math.random() * choices.length)];
                document.getElementById('playerChoice').innerText = icons[pChoice];
                document.getElementById('memberChoice').innerText = icons[mChoice];

                let resMsg = "";
                let resColor = "#ffeb3b";
                if (pChoice === mChoice) {
                    resMsg = "🤝 平局！默契十足！";
                } else if (
                    (pChoice === '石头' && mChoice === '剪刀') ||
                    (pChoice === '剪刀' && mChoice === '布') ||
                    (pChoice === '布' && mChoice === '石头')
                ) {
                    resMsg = "🎉 赢了！"""
      + member_name
      + """ 为你欢呼！";
                    resColor = "#00e676";
                    wins++;
                } else {
                    resMsg = "💧 输啦！"""
      + member_name
      + """ 得意地笑！";
                    resColor = "#ff5252";
                }
                document.getElementById('duel-result').innerHTML = resMsg + " (胜场: " + wins + ")";
                document.getElementById('duel-result').style.color = resColor;
            }
        </script>
    </body>
    </html>
    """
  )
  components.html(html_code, height=275)


def render_ramen_battle_game(member_name):
  html_code = (
      """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .battle-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); padding: 10px; width: 300px; text-align: center; }
            .bowl { font-size: 38px; margin: 6px 0; }
            .score-row { display: flex; justify-content: space-around; color: #fff; font-size: 13px; font-weight: bold; margin-bottom: 8px; }
            .eat-btn { background: linear-gradient(45deg, #ff5252, #ffeb3b); color: #333; border: none; padding: 12px 0; font-size: 15px; font-weight: bold; border-radius: 16px; cursor: pointer; width: 100%; box-shadow: 0 3px 10px rgba(255,82,82,0.5); }
            .eat-btn:active { transform: scale(0.95); }
        </style>
    </head>
    <body>
        <div class="battle-box">
            <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">🍜 深夜食堂：与 """
      + member_name
      + """ 的拉面大胃王！</div>
            <div class="bowl" id="bowlIcon">🍜</div>
            <div class="score-row">
                <div>你吃面: <span id="playerBowls" style="color:#00e676; font-size:15px;">0</span> 碗</div>
                <div>"""
      + member_name
      + """: <span id="memberBowls" style="color:#ff4081; font-size:15px;">0</span> 碗</div>
            </div>
            <div id="ramen-tip" style="color: #fff; font-size: 11px; font-weight: bold; margin-bottom: 6px;">⏳ 倒计时: <span id="rTime">10</span>s | 疯狂猛点按钮炫面！</div>
            <button class="eat-btn" onclick="eatRamen()">🥢 狂炫拉面！</button>
        </div>
        <script>
            let pBowls = 0, mBowls = 0, timeLeft = 10, isOver = false;
            const pSpan = document.getElementById('playerBowls');
            const mSpan = document.getElementById('memberBowls');
            const tSpan = document.getElementById('rTime');
            const bowl = document.getElementById('bowlIcon');

            let aiTimer = setInterval(() => {
                if (!isOver) {
                    if (Math.random() > 0.3) { mBowls++; mSpan.innerText = mBowls; }
                }
            }, 600);

            let clock = setInterval(() => {
                if (timeLeft > 0 && !isOver) {
                    timeLeft--; tSpan.innerText = timeLeft;
                } else {
                    isOver = true; clearInterval(clock); clearInterval(aiTimer);
                    let resultText = pBowls > mBowls ? "🎉 你赢了！大胃王纪录！" : "💧 输给 """
      + member_name
      + """ 了！吃太快啦！";
                    document.getElementById('ramen-tip').innerHTML = resultText;
                    document.getElementById('ramen-tip').style.color = pBowls > mBowls ? "#00e676" : "#ff5252";
                }
            }, 1000);

            function eatRamen() {
                if (isOver) return;
                pBowls++;
                pSpan.innerText = pBowls;
                bowl.style.transform = "scale(1.2)";
                setTimeout(() => bowl.style.transform = "scale(1)", 100);
            }
        </script>
    </body>
    </html>
    """
  )
  components.html(html_code, height=275)


def render_lightstick_game():
  html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .light-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); padding: 10px; width: 300px; text-align: center; }
            .color-display { width: 75px; height: 75px; border-radius: 50%; margin: 8px auto; box-shadow: 0 0 15px rgba(255,255,255,0.4); border: 2.5px solid #fff; }
            .color-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-top: 8px; }
            .color-btn { padding: 10px 0; font-size: 13px; font-weight: bold; border-radius: 10px; border: none; color: white; cursor: pointer; box-shadow: 0 3px 8px rgba(0,0,0,0.3); }
            .color-btn:active { transform: scale(0.95); }
        </style>
    </head>
    <body>
        <div class="light-box">
            <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">🌟 手灯狂热！按下与上方匹配的颜色！</div>
            <div class="color-display" id="targetColorBox"></div>
            <div id="light-tip" style="color: #fff; font-size: 11px; font-weight: bold;">⏳ 剩余: <span id="timeVal">12</span>s | 得分: <span id="scoreVal">0</span></div>
            <div class="color-grid">
                <button class="color-btn" style="background: #ff5252;" onclick="checkColor('red')">❤️ 红色</button>
                <button class="color-btn" style="background: #448aff;" onclick="checkColor('blue')">💙 蓝色</button>
                <button class="color-btn" style="background: #ffeb3b; color:#333;" onclick="checkColor('yellow')">💛 黄色</button>
                <button class="color-btn" style="background: #00e676;" onclick="checkColor('green')">💚 绿色</button>
            </div>
        </div>
        <script>
            const colors = ['red', 'blue', 'yellow', 'green'];
            const colorHex = { red: '#ff5252', blue: '#448aff', yellow: '#ffeb3b', green: '#00e676' };
            let currentTarget = 'red', score = 0, timeLeft = 12, isGameOver = false;
            const box = document.getElementById('targetColorBox');
            const timeSpan = document.getElementById('timeVal');
            const scoreSpan = document.getElementById('scoreVal');

            function changeTarget() {
                if (isGameOver) return;
                currentTarget = colors[Math.floor(Math.random() * colors.length)];
                box.style.background = colorHex[currentTarget];
            }
            let targetInterval = setInterval(changeTarget, 1000);
            changeTarget();

            let gameTimer = setInterval(() => {
                if (timeLeft > 0 && !isGameOver) {
                    timeLeft--; timeSpan.innerText = timeLeft;
                } else {
                    isGameOver = true; clearInterval(gameTimer); clearInterval(targetInterval);
                    box.style.background = '#ab47bc';
                    document.getElementById('light-tip').innerHTML = "🎉 应援结束！得分: " + score;
                }
            }, 1000);

            function checkColor(c) {
                if (isGameOver) return;
                if (c === currentTarget) { score += 150; scoreSpan.innerText = score; changeTarget(); }
                else { score = Math.max(0, score - 50); scoreSpan.innerText = score; }
            }
        </script>
    </body>
    </html>
    """
  components.html(html_code, height=265)


def render_dodge_canvas_game():
  html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .canvas-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); position: relative; overflow: hidden; width: 300px; height: 185px; }
            canvas { display: block; }
            .ctrl-panel { display: flex; gap: 10px; margin-top: 8px; width: 300px; justify-content: center; }
            .move-btn { background: linear-gradient(45deg, #ff4081, #ab47bc); color: white; border: none; padding: 10px 0; font-size: 14px; font-weight: bold; border-radius: 16px; cursor: pointer; flex: 1; }
            .move-btn:active { transform: scale(0.95); }
        </style>
    </head>
    <body>
        <div class="canvas-box"><canvas id="dodgeCanvas" width="300" height="185"></canvas></div>
        <div class="ctrl-panel">
            <button class="move-btn" onclick="movePlayer(-1)">⬅️ 往左闪避</button>
            <button class="move-btn" onclick="movePlayer(1)">往右闪避 ➡️</button>
        </div>
        <script>
            const canvas = document.getElementById('dodgeCanvas');
            const ctx = canvas.getContext('2d');
            let lane = 1, lanesX = [55, 150, 245], playerY = 150, obstacles = [], hp = 3, timeLeft = 15, isGameOver = false;
            let timer = setInterval(() => { if(timeLeft > 0 && !isGameOver) timeLeft--; else { isGameOver = true; clearInterval(timer); clearInterval(spawner); } }, 1000);
            let spawner = setInterval(() => { if(!isGameOver) obstacles.push({ lane: Math.floor(Math.random()*3), y: -20, speed: 4.0 }); }, 550);
            function movePlayer(dir) { if(!isGameOver) { lane += dir; if(lane < 0) lane = 0; if(lane > 2) lane = 2; } }
            function loop() {
                ctx.clearRect(0, 0, 300, 185);
                ctx.strokeStyle = '#2d1b4e'; ctx.lineWidth = 2; ctx.setLineDash([4, 4]);
                [100, 200].forEach(x => { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 185); ctx.stroke(); });
                ctx.setLineDash([]);
                for (let i = obstacles.length - 1; i >= 0; i--) {
                    let obs = obstacles[i]; obs.y += obs.speed;
                    ctx.fillStyle = '#ff5252'; ctx.beginPath(); ctx.arc(lanesX[obs.lane], obs.y, 11, 0, Math.PI*2); ctx.fill();
                    ctx.fillStyle = '#fff'; ctx.font = '10px Arial'; ctx.fillText('💡', lanesX[obs.lane]-5, obs.y+3);
                    if (obs.y >= playerY-13 && obs.y <= playerY+13 && obs.lane === lane) {
                        hp--; obstacles.splice(i, 1); if(hp <= 0) isGameOver = true;
                    } else if (obs.y > 200) { obstacles.splice(i, 1); }
                }
                let px = lanesX[lane];
                ctx.fillStyle = '#ff4081'; ctx.beginPath(); ctx.arc(px, playerY, 12, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = '#fff'; ctx.font = '11px Arial'; ctx.fillText('⭐', px-5, playerY+3);
                ctx.fillStyle = '#fff'; ctx.font = 'bold 12px Arial'; ctx.fillText("⏱️ 倒计时: " + timeLeft + "s", 12, 18);
                ctx.fillStyle = '#ff4081'; ctx.fillText("❤️ 生命: " + "❤️".repeat(Math.max(0, hp)), 195, 18);
                if (!isGameOver) requestAnimationFrame(loop);
                else { ctx.fillStyle = 'rgba(0,0,0,0.88)'; ctx.fillRect(0,0,300,185); ctx.fillStyle = '#00e676'; ctx.font = 'bold 16px Arial'; ctx.fillText("🎉 生存挑战成功！", 75, 98); }
            }
            loop();
        </script>
    </body>
    </html>
    """
  components.html(html_code, height=250)


# -------------------------------------------------------------------
# 剧情数据库（已加入新增的突发街头生放送剧情）
# -------------------------------------------------------------------
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
          "title": "📡 Stage 14：【突发事件】深夜街头突击生放送（直播）！",
          "desc": f"刚结束排练和 {member} 走在涩谷街头，电视台的‘突击深夜街头生放送’摄影车突然把镜头怼到你们脸前，主持人随机要求现场即兴表现！",
          "opt1": "当场清唱一段未公开的自创高音段落，惊艳全网直播间！",
          "opt2": "一把拉过身边的队友开始疯狂搞笑模仿社长，节目效果直接拉满上热搜！",
          "opt3": "礼貌微笑并把镜头推给队长：“我们团长有话说！”",
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
          "title": "🏢 Stage 19：社长办公室的神秘闭门谈话",
          "desc": "深夜排练结束后，你被社长助理单独叫进了顶楼办公室。社长看着你厚厚的一叠成长记录，露出了意味深长的笑容。",
          "opt1": "目光坚定地直视社长：“我已经准备好承担更大的责任了！”",
          "opt2": "谦逊地向社长鞠躬：“感谢事务所一直以来的培养与照顾。”",
          "opt3": "坦诚说出自己对未来音乐风格的构想与野心。",
      },
      22: {
          "title": "🍕 Stage 22：宿舍里的深夜披萨作战",
          "desc": f"距离出道决定日只剩最后几天，大家紧绷的神经有些支撑不住。{member} 偷偷订了外卖披萨送到宿舍，招呼大家围坐在一起放松。",
          "opt1": "大口吃披萨并讲冷笑话，把沉重的气氛瞬间活跃起来。",
          "opt2": "借着汽水向大家举杯：“不管结果如何，能和大家相遇太好了。”",
          "opt3": "吃完后主动默默把客厅和厨房收拾得干干净净。",
      },
      24: {
          "title": "🌙 Stage 24：出道发布会彩排的最后通牒",
          "desc": "明天就是全日本各大电视台转播的出道决选发布会。最后一次彩排中，导播对你们的走位和队形提出了极其严苛的修改意见。",
          "opt1": "带头留下来陪大家连夜加练 3 小时，直到全员零失误。",
          "opt2": "逐一帮队友调整领带和耳返，展现出极强的核心凝聚力。",
          "opt3": "闭目养神调整心态，用绝对沉稳的自信感染所有人。",
      },
  }


# 主标题
st.title("💖 星途闪耀：我的练习生日常")

# -------------------------------------------------------------------
# STAGE 0: 开局
# -------------------------------------------------------------------
if not st.session_state.game_started:
  st.markdown(
      '<div class="cute-info">✨ 欢迎来到 STARTO 偶像养成营！请输入你的名字，选择心仪组合并抽取开局传奇幸运物！</div>',
      unsafe_allow_html=True,
  )

  name_input = st.text_input(
      "✏️ 请输入你的名字（或昵称）：", placeholder="例如：小夏"
  )

  st.markdown("---")
  selected_group = st.selectbox(
      "选择你想加入/并肩作战的组合：", list(IDOL_GROUPS.keys())
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

  if st.session_state.stress >= 70:
    st.warning(
        f"⚠️ **【压力预警】** 压力值已达 **{st.session_state.stress}%**！{member} 悄悄塞给你一罐热可可：“别把自己逼太紧，大家都在呢。”"
    )
    st.session_state.stress = 30
    st.session_state.bond += 10

  is_free_training_day = curr_stage in [3, 16]

  if is_free_training_day and curr_stage < 25:
    st.subheader(f"🗓️ Stage {curr_stage}：自主特训与日常安排")
    st.info(
        f"💡 **自主安排日** | 🎒 当前幸运物：【{st.session_state.lucky_item}】 | 🔥 压力值: {st.session_state.stress}%"
    )

    col1, col2 = st.columns(2)
    with col1:
      if st.button("💃 在舞蹈房死磕高难度步法"):
        if st.session_state.energy < 20:
          st.error("⚠️ 体力不足，快去休息吧！")
        else:
          st.session_state.dance += random.randint(15, 25)
          st.session_state.energy -= 20
          st.session_state.stress += 15
          st.session_state.stage += 1
          st.rerun()
      if st.button("🎤 到声乐室练习高音发声"):
        if st.session_state.energy < 20:
          st.error("⚠️ 嗓子有些哑了，快去休息吧！")
        else:
          st.session_state.vocal += random.randint(15, 25)
          st.session_state.energy -= 20
          st.session_state.stress += 10
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
          st.session_state.stress = max(0, st.session_state.stress - 20)
          st.session_state.stage += 1
          st.rerun()
      if st.button("💤 回宿舍彻底躺平休息"):
        st.session_state.energy = min(100, st.session_state.energy + 40)
        st.session_state.stress = max(0, st.session_state.stress - 30)
        st.session_state.stage += 1
        st.rerun()

  # 阶段 3：🌙 宿舍深夜真心话卡牌
  elif curr_stage == 3:
    st.subheader(
        f"📍 Stage 3：【宿舍深夜心跳】与 {member} 的真心话大冒险卡牌"
    )
    st.markdown(
        f'<div class="event-card"><b>🃏 【真心话大冒险卡牌抉择】</b><br>深夜熄灯后，宿舍里几个人围坐在一起玩真心话卡牌。轮到你抽牌了，你抽到了一张闪光心跳卡：<b>“如果必须在组合里选一个人作为永远的搭档，你的真实想法是？”</b></div>',
        unsafe_allow_html=True,
    )

    c1 = st.button(
        f"1. 毫不犹豫指向身边的 {member}：“当然是选最懂我的你啦！”"
    )
    c2 = st.button("2. 大笑著把卡牌传给下一个人：“秘密，这是商业机密！”")
    c3 = st.button(
        "3. 认真地看向全员：“我想和大家所有人一起永远站在舞台上。”"
    )

    if c1:
      st.session_state.bond += 25
      st.session_state.stage += 1
      st.rerun()
    if c2:
      st.session_state.variety += 15
      st.session_state.stage += 1
      st.rerun()
    if c3:
      st.session_state.fans += 500
      st.session_state.trust += 10
      st.session_state.stage += 1
      st.rerun()

  # 阶段 6：🎹 钢琴块下落打歌
  elif curr_stage == 6:
    st.subheader("📍 Stage 6：【全开麦打歌·节奏钢琴块】")
    st.markdown(
        '<div class="event-card"><b>🎹 【打歌小游戏：下落式节奏钢琴块】</b><br>打歌现场高能来临！点击下方 1-2-3-4 按钮敲击下落的钢琴块，持续 12 秒！</div>',
        unsafe_allow_html=True,
    )
    render_piano_tiles_game()

    if st.button("➔ 演奏结束，点击进入下一阶段"):
      st.session_state.fans += 1500
      st.session_state.dance += 20
      st.session_state.stage += 1
      st.rerun()

  # 阶段 9 🔥（小分队企划答题选拔游戏）
  elif curr_stage == 9:
    st.subheader("📍 Stage 9：【社内企划】限定 Unit 小分队答题选拔赛")
    st.markdown(
        f'<div class="event-card"><b>🏆 【小分队企划选拔游戏】</b><br>事务所派发了核心企划考题！请为 <b>{member}</b> 与你所在的组合在下方选项中<b>选出至少 2 个正确选项</b>提交！</div>',
        unsafe_allow_html=True,
    )
    render_unit_selection_game()

    if st.button("➔ 选拔答题完毕，锁定企划！"):
      st.session_state.dance += 25
      st.session_state.fans += 1200
      st.session_state.bond += 20
      st.session_state.stage += 1
      st.rerun()

  # 阶段 10：🍜 深夜拉面大胃王比拼
  elif curr_stage == 10:
    st.subheader(f"📍 Stage 10：【深夜食堂·与 {member} 的拉面大胃王决战】")
    st.markdown(
        f'<div class="event-card"><b>🍜 【双人互动小游戏：深夜拉面大胃王】</b><br>排练完大家来到拉面店，你和 <b>{member}</b> 展开了 10 秒钟狂炫拉面比拼！疯狂点击按钮赢过他！</div>',
        unsafe_allow_html=True,
    )
    render_ramen_battle_game(member)

    if st.button("➔ 饱餐结束，点击进入下一阶段"):
      st.session_state.bond += 18
      st.session_state.variety += 15
      st.session_state.stage += 1
      st.rerun()

  # 阶段 12：⛏️ 铁锹敲击土块【地下仓库盲盒挖宝】
  elif curr_stage == 12:
    st.subheader("📍 Stage 12：【事务所地下仓库·铁锹盲盒挖宝】")
    st.markdown(
        '<div class="event-card"><b>⛏️ 【挖宝小游戏：铁锹敲开土块寻找盲盒】</b><br>在事务所地下仓库的土层中隐藏着绝版宝物！敲开土块，获得的宝物将直接转化为你的粉丝与能力加成！</div>',
        unsafe_allow_html=True,
    )
    render_dirt_dig_game()

    if st.button("➔ 挖宝结束，领取属性并进入下一阶段"):
      st.session_state.fans += 1500
      st.session_state.dance += 10
      st.session_state.variety += 15
      st.session_state.stage += 1
      st.rerun()

  # 阶段 15：🥞 实体双层松饼动态摆动堆高
  elif curr_stage == 15:
    st.subheader(f"📍 Stage 15：【后台双人互动·松饼动态摆动堆高】")
    st.markdown(
        f'<div class="event-card"><b>🥞 【双人互动小游戏：松饼左右摆动堆高】</b><br>在休息室里，你和 <b>{member}</b> 比赛叠松饼！上方松饼会自动左右摆动，看准时机点击落下，堆得越高你们的羁绊越深！</div>',
        unsafe_allow_html=True,
    )
    render_pancake_stack_game(member)

    if st.button("➔ 游戏结束，点击进入下一阶段"):
      st.session_state.bond += 25
      st.session_state.stage += 1
      st.rerun()

  # 阶段 17：⚡ 【电眼辣妹风】巨蛋花车电眼狙击战
  elif curr_stage == 17:
    st.subheader("📍 Stage 17：【巨蛋花车巡游】全场电眼狙击战")
    st.markdown(
        '<div class="event-card"><b>⚡ 【经典电眼辣妹风：电眼狙击战】</b><br>花车驶过应援席！左右移动控制偶像位置，看准下落的粉红爱心 (💖) 点击<b>发射电眼激光</b>收集粉丝，同时小心避开黑色炸弹 (💣)！</div>',
        unsafe_allow_html=True,
    )
    render_eyecatch_game()

    if st.button("➔ 电眼狙击战结束，粉丝好感暴涨！"):
      st.session_state.fans += 2500
      st.session_state.variety += 25
      st.session_state.stage += 1
      st.rerun()

  # 阶段 18：📸 杂志封面闪光灯快门抓拍
  elif curr_stage == 18:
    st.subheader("📍 Stage 18：【杂志封面拍摄】闪光灯快门抓拍 QTE")
    st.markdown(
        '<div class="event-card"><b>📸 【时尚摄影小游戏：快门抓拍挑战】</b><br>出道杂志大片拍摄现场！看准监视器指示（侧颜/大笑/眼神），在下方精准按下快门按键！</div>',
        unsafe_allow_html=True,
    )
    render_magazine_photo_game()

    if st.button("➔ 拍摄大获成功，进入下一阶段！"):
      st.session_state.fans += 1800
      st.session_state.variety += 25
      st.session_state.stage += 1
      st.rerun()

  # 阶段 19：🪵 带指针的平衡木挑战
  elif curr_stage == 19:
    st.subheader("📍 Stage 19：【后台休息室】顶杂志平衡木热身")
    st.markdown(
        '<div class="event-card"><b>🪵 【趣味平衡小游戏：顶杂志热身】</b><br>上台前为了防止身体紧绷，大家在后台玩顶杂志平衡木游戏！看准上方带有指针的彩色进度条，及时点击对应方向拉回中心！</div>',
        unsafe_allow_html=True,
    )
    render_balance_game()

    if st.button("➔ 热身完毕，准备迎接巨蛋巡演！"):
      st.session_state.bond += 20
      st.session_state.dance += 15
      st.session_state.stage += 1
      st.rerun()

  # 阶段 20：⏱️ 演唱会后台紧急换装 QTE 小游戏
  elif curr_stage == 20:
    st.subheader(f"📍 Stage 20：【演唱会暗场】与 {member} 的紧急换装 QTE")
    st.markdown(
        f'<div class="event-card"><b>⏱️ 【后台紧急换装 QTE】</b><br>巨蛋演唱会现场两首歌之间的暗场只有短短 30 秒！你需要快速完成换装动作，{member} 会在旁边帮你递耳返和拿话筒！</div>',
        unsafe_allow_html=True,
    )
    render_wardrobe_qte_game(member)

    if st.button("➔ 换装完毕，冲上舞台！"):
      st.session_state.fans += 1800
      st.session_state.stage += 1
      st.rerun()

  # 阶段 21：🌟 演唱会手灯狂热
  elif curr_stage == 21:
    st.subheader("📍 Stage 21：【巨蛋巡演·全场手灯狂热互动】")
    st.markdown(
        '<div class="event-card"><b>🌟 【手灯狂热小游戏：全场应援色同步】</b><br>演唱会高潮来临！全场粉丝手灯颜色在不断变化，<b>请点击下方对应的颜色按钮与上方保持一致</b>！</div>',
        unsafe_allow_html=True,
    )
    render_lightstick_game()

    if st.button("➔ 应援结束，点击进入下一阶段"):
      st.session_state.fans += 2000
      st.session_state.vocal += 20
      st.session_state.stage += 1
      st.rerun()

  # 阶段 22：🤝 成员双人互动【默契猜拳对决】
  elif curr_stage == 22:
    st.subheader(f"📍 Stage 22：【后台趣味互动·与 {member} 的默契对决】")
    st.markdown(
        f'<div class="event-card"><b>🤝 【双人互动小游戏：后台猜拳对决】</b><br>在演出间隙，你和 <b>{member}</b> 玩起了后台经典猜拳游戏！赢了可以大幅提升团员羁绊！</div>',
        unsafe_allow_html=True,
    )
    render_member_duel_game(member)

    if st.button("➔ 互动结束，点击进入下一阶段"):
      st.session_state.bond += 20
      st.session_state.fans += 1500
      st.session_state.stage += 1
      st.rerun()

  # 阶段 23：⚡ 15 秒灯光闪避生存
  elif curr_stage == 23:
    st.subheader("📍 Stage 23：【巨蛋巡演·舞台事故紧急闪避】")
    st.markdown(
        '<div class="event-card"><b>🎮 【生存闪避小游戏：15秒极限危机】</b><br>舞台灯光坠落！点击左右闪避按钮坚持 15 秒自动通关！</div>',
        unsafe_allow_html=True,
    )
    render_dodge_canvas_game()

    if st.button("🌟 生存挑战结束，前往出道前夜！"):
      st.session_state.fans += 2200
      st.session_state.variety += 25
      st.session_state.stage += 1
      st.rerun()

  # 海量剧情关卡（25章以内）
  elif curr_stage < 25:
    st.subheader(f"📍 Stage {curr_stage} / 25")

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
      st.session_state.stress += 10
      st.session_state.stage += 1
      st.rerun()
    if c2:
      st.session_state.vocal += 12
      st.session_state.fans += 450
      st.session_state.stress += 10
      st.session_state.stage += 1
      st.rerun()
    if c3:
      st.session_state.variety += 15
      st.session_state.bond += 10
      st.session_state.stage += 1
      st.rerun()

  # -------------------------------------------------------------------
  # STAGE 25: 帝国剧场终局裁决
  # -------------------------------------------------------------------
  else:
    st.subheader("🏁 Stage 25：帝国剧场 CD 出道决选")
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

      if st.session_state.fans >= 2200 and total >= 140:
        st.balloons()
        st.success(
            f"🎉 恭喜 **{st.session_state.player_name}**！你携带【{st.session_state.lucky_item}】，与 **{st.session_state.group}** 的伙伴们历经 25 章的汗水与磨砺，完美闪耀帝国剧场，正式华丽 CD 出道！"
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
