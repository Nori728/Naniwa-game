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
# 🎹 1. 钢琴块下落打歌小游戏
# -------------------------------------------------------------------
def render_piano_tiles_game():
  html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .piano-box { background: #1a0f30; border: 3px solid #ff80ab; border-radius: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.3); position: relative; overflow: hidden; width: 320px; height: 260px; }
            canvas { display: block; }
            .btn-row { display: flex; gap: 8px; margin-top: 10px; width: 320px; }
            .piano-btn { background: linear-gradient(180deg, #ab47bc, #7b1fa2); color: white; border: 2px solid #ff80ab; padding: 12px 0; font-size: 18px; font-weight: bold; border-radius: 12px; cursor: pointer; flex: 1; text-align: center; }
            .piano-btn:active { background: #ff4081; transform: scale(0.92); }
        </style>
    </head>
    <body>
        <div class="piano-box"><canvas id="pianoCanvas" width="320" height="260"></canvas></div>
        <div class="btn-row">
            <button class="piano-btn" onclick="tapTrack(0)">1</button>
            <button class="piano-btn" onclick="tapTrack(1)">2</button>
            <button class="piano-btn" onclick="tapTrack(2)">3</button>
            <button class="piano-btn" onclick="tapTrack(3)">4</button>
        </div>
        <script>
            const canvas = document.getElementById('pianoCanvas');
            const ctx = canvas.getContext('2d');
            const trackWidth = 80;
            let tiles = [], score = 0, combo = 0, timeLeft = 12, isGameOver = false;
            let timer = setInterval(() => { if(timeLeft > 0 && !isGameOver) timeLeft--; else { isGameOver = true; clearInterval(timer); clearInterval(spawner); } }, 1000);
            let spawner = setInterval(() => { if(!isGameOver) tiles.push({ track: Math.floor(Math.random()*4), y: -40, h: 40, hit: false }); }, 550);
            function tapTrack(idx) {
                if(isGameOver) return;
                let ok = false;
                for(let t of tiles) {
                    if(t.track === idx && !t.hit && t.y >= 140 && t.y <= 250) { t.hit = true; ok = true; score += 100; combo++; break; }
                }
                if(!ok) combo = 0;
            }
            function loop() {
                ctx.clearRect(0, 0, 320, 260);
                ctx.strokeStyle = '#2d1b4e';
                for(let i=1; i<4; i++) { ctx.beginPath(); ctx.moveTo(i*trackWidth, 0); ctx.lineTo(i*trackWidth, 260); ctx.stroke(); }
                ctx.fillStyle = 'rgba(255, 64, 129, 0.2)'; ctx.fillRect(0, 180, 320, 60);
                for(let i=tiles.length-1; i>=0; i--) {
                    let t = tiles[i];
                    if(!t.hit) {
                        t.y += 3.5;
                        ctx.fillStyle = '#211035'; ctx.fillRect(t.track*trackWidth+4, t.y, trackWidth-8, t.h);
                        ctx.strokeStyle = '#ea80fc'; ctx.strokeRect(t.track*trackWidth+4, t.y, trackWidth-8, t.h);
                        ctx.fillStyle = '#ff80ab'; ctx.font = '12px Arial'; ctx.fillText('🎵', t.track*trackWidth+30, t.y+25);
                        if(t.y > 260) { tiles.splice(i, 1); combo = 0; }
                    } else { tiles.splice(i, 1); }
                }
                ctx.fillStyle = '#fff'; ctx.font = 'bold 12px Arial';
                ctx.fillText("⏳ 剩余: " + timeLeft + "s", 10, 20);
                ctx.fillText("🔥 分数: " + score, 130, 20);
                ctx.fillText("⚡ Combo: " + combo, 220, 20);
                if(!isGameOver) requestAnimationFrame(loop);
                else { ctx.fillStyle = 'rgba(0,0,0,0.8)'; ctx.fillRect(0,0,320,260); ctx.fillStyle = '#00e676'; ctx.font = 'bold 18px Arial'; ctx.fillText("🎉 打歌结束！总分: " + score, 50, 135); }
            }
            loop();
        </script>
    </body>
    </html>
    """
  components.html(html_code, height=340)


# -------------------------------------------------------------------
# ⛏️ 2. 铁锹敲击土块【地下仓库盲盒挖宝】
# -------------------------------------------------------------------
def render_dirt_dig_game():
  html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .dig-box { background: #1a0f30; border: 3px solid #ff80ab; border-radius: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.3); padding: 15px; width: 320px; text-align: center; }
            .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin: 12px 0; }
            .dirt-tile { background: #5d4037; border: 2px solid #8d6e63; color: #d7ccc8; height: 50px; border-radius: 10px; font-size: 13px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
            .dirt-tile:active { transform: scale(0.95); }
            .dirt-tile.dug { background: #3e2723; border: 2px dashed #6d4c41; color: #fff; cursor: default; }
            #dig-tip { color: #ffeb3b; font-size: 13px; font-weight: bold; min-height: 20px; }
        </style>
    </head>
    <body>
        <div class="dig-box">
            <div style="color: #fff; font-weight: bold; font-size: 12px;">⛏️ 用铁锹敲开土块！(剩余铲子: <span id="shovels">6</span>)</div>
            <div class="grid" id="dirtGrid"></div>
            <div id="dig-tip">点击土块挖掘，宝物可转化为实际属性！</div>
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
                        tipEl.innerHTML = "🏆 挖宝完成！共获得 " + treasuresFound + " 件宝物加成！";
                    }
                } else {
                    el.innerHTML = '🕳️ 泥土';
                    tipEl.innerHTML = "💧 这块土下面什么都没有...";
                    tipEl.style.color = "#ff5252";
                    if (shovels === 0) {
                        isOver = true;
                        tipEl.innerHTML = "💧 铲子用光啦！共找到 " + treasuresFound + " 件宝物！";
                    }
                }
            }
            renderGrid();
        </script>
    </body>
    </html>
    """
  components.html(html_code, height=310)


# -------------------------------------------------------------------
# 🔥 Stage 9：限定 Unit 小分队概念选拔配对小游戏
# -------------------------------------------------------------------
def render_unit_selection_game():
  html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .unit-box { background: #1a0f30; border: 3px solid #ff80ab; border-radius: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.3); padding: 12px; width: 320px; text-align: center; }
            .card-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin: 10px 0; }
            .concept-card { background: linear-gradient(135deg, #4a148c, #7b1fa2); border: 2px solid #ff4081; color: #fff; padding: 12px 8px; border-radius: 10px; font-size: 12px; font-weight: bold; cursor: pointer; }
            .concept-card:active { transform: scale(0.95); }
            .concept-card.selected { background: #00e676; color: #000; border-color: #fff; }
            #unit-tip { color: #ffeb3b; font-size: 12px; font-weight: bold; min-height: 25px; margin-top: 5px; }
        </style>
    </head>
    <body>
        <div class="unit-box">
            <div style="color: #ffeb3b; font-weight: bold; font-size: 13px;">🏆 限定 Unit 小分队概念选拔赛</div>
            <div style="color: #fff; font-size: 11px; margin-top: 4px;">请在 10 秒内点击选择 3 个最契合的舞台核心词汇！</div>
            <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 4px;">⏳ 剩余: <span id="uTime">10</span>s | 已选: <span id="selectedCount">0</span>/3</div>
            
            <div class="card-grid" id="cardContainer"></div>
            <div id="unit-tip">点击卡片组合你的梦幻小分队！</div>
        </div>
        <script>
            const pool = [
                {id: 1, text: '🔥 炸裂齐舞', valid: true},
                {id: 2, text: '🎸 摇滚乐队', valid: true},
                {id: 3, text: '✨ 王道耀眼', valid: true},
                {id: 4, text: '🤡 爆笑综艺', valid: false},
                {id: 5, text: '💧 忧伤抒情', valid: false},
                {id: 6, text: '🌙 暗黑吸血鬼', valid: true}
            ];
            let selected = [];
            let timeLeft = 10;
            let isOver = false;

            const container = document.getElementById('cardContainer');
            const tipEl = document.getElementById('unit-tip');
            const timeEl = document.getElementById('uTime');
            const countEl = document.getElementById('selectedCount');

            function renderCards() {
                container.innerHTML = '';
                pool.forEach(item => {
                    let card = document.createElement('div');
                    card.className = 'concept-card' + (selected.includes(item.id) ? ' selected' : '');
                    card.innerText = item.text;
                    card.onclick = () => selectCard(item.id, card);
                    container.appendChild(card);
                });
            }

            let timer = setInterval(() => {
                if (timeLeft > 0 && !isOver) {
                    timeLeft--;
                    timeEl.innerText = timeLeft;
                } else if (!isOver) {
                    finishSelection();
                }
            }, 1000);

            function selectCard(id, el) {
                if (isOver) return;
                if (selected.includes(id)) {
                    selected = selected.filter(i => i !== id);
                } else {
                    if (selected.length < 3) {
                        selected.push(id);
                    }
                }
                countEl.innerText = selected.length;
                renderCards();
                if (selected.length === 3) {
                    finishSelection();
                }
            }

            function finishSelection() {
                isOver = true;
                clearInterval(timer);
                let correctCount = selected.filter(id => pool.find(p => p.id === id).valid).length;
                if (correctCount >= 2) {
                    tipEl.innerHTML = "🎉 企划大获成功！小分队出道预定！";
                    tipEl.style.color = "#00e676";
                } else {
                    tipEl.innerHTML = "💧 风格略显杂乱，需调整再接再厉！";
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
# 👗 3. 精致暖暖风：偶像男装/多风格纸娃娃换装间
# -------------------------------------------------------------------
def render_dress_up_game():
  html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .dress-box { background: #1a0f30; border: 3px solid #ff80ab; border-radius: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.3); padding: 12px; width: 320px; text-align: center; }
            canvas { display: block; margin: 0 auto; background: linear-gradient(135deg, #2b1055, #7597de); border-radius: 12px; border: 2px solid #ff4081; box-shadow: inset 0 0 15px rgba(0,0,0,0.4); }
            .category-row { display: flex; justify-content: center; gap: 4px; margin-top: 10px; }
            .cat-btn { background: #4a148c; color: white; border: 1px solid #ff80ab; padding: 6px 10px; font-size: 11px; font-weight: bold; border-radius: 8px; cursor: pointer; }
            .cat-btn.active { background: #ff4081; box-shadow: 0 0 8px #ff4081; }
            .items-row { display: flex; justify-content: center; gap: 6px; margin-top: 8px; flex-wrap: wrap; }
            .item-btn { background: linear-gradient(45deg, #ab47bc, #7b1fa2); color: white; border: 1px solid #ea80fc; padding: 6px 10px; font-size: 11px; font-weight: bold; border-radius: 8px; cursor: pointer; }
            .item-btn:active { transform: scale(0.95); }
        </style>
    </head>
    <body>
        <div class="dress-box">
            <div style="color: #ffeb3b; font-weight: bold; font-size: 13px; margin-bottom: 6px;">✨ 杂志封面：偶像纸娃娃高级定制间</div>
            <canvas id="dollCanvas" width="296" height="185"></canvas>
            
            <div class="category-row">
                <button class="cat-btn active" onclick="setCategory('hair')">💇 发型</button>
                <button class="cat-btn" onclick="setCategory('top')">🧥 上衣</button>
                <button class="cat-btn" onclick="setCategory('bottom')">👖 裤装</button>
                <button class="cat-btn" onclick="setCategory('shoes')">👟 鞋子</button>
            </div>
            
            <div class="items-row" id="itemOptions"></div>
        </div>
        <script>
            const canvas = document.getElementById('dollCanvas');
            const ctx = canvas.getContext('2d');

            let currentCat = 'hair';
            let outfit = {
                hair: { name: '日系抓发', type: 'hair1' },
                top: { name: '学院西装', type: 'top1' },
                bottom: { name: '修身黑裤', type: 'bot1' },
                shoes: { name: '经典皮鞋', type: 'shoe1' }
            };

            const options = {
                hair: [
                    { name: '日系抓发', type: 'hair1' },
                    { name: '韩系微卷', type: 'hair2' },
                    { name: '耀眼狼尾', type: 'hair3' }
                ],
                top: [
                    { name: '学院西装', type: 'top1' },
                    { name: '华丽战袍', type: 'top2' },
                    { name: '宽松连帽衫', type: 'top3' }
                ],
                bottom: [
                    { name: '修身黑裤', type: 'bot1' },
                    { name: '工装潮裤', type: 'bot2' },
                    { name: '亮片西裤', type: 'bot3' }
                ],
                shoes: [
                    { name: '经典皮鞋', type: 'shoe1' },
                    { name: '高帮马丁', type: 'shoe2' },
                    { name: '运动板鞋', type: 'shoe3' }
                ]
            };

            function setCategory(cat) {
                currentCat = cat;
                document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
                event.target.classList.add('active');
                renderOptions();
            }

            function renderOptions() {
                const row = document.getElementById('itemOptions');
                row.innerHTML = '';
                options[currentCat].forEach(opt => {
                    let btn = document.createElement('button');
                    btn.className = 'item-btn';
                    btn.innerText = opt.name;
                    btn.onclick = () => {
                        outfit[currentCat] = opt;
                        drawDoll();
                    };
                    row.appendChild(btn);
                });
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

            function drawDoll() {
                ctx.clearRect(0, 0, 296, 185);

                let grad = ctx.createRadialGradient(148, 92, 10, 148, 92, 90);
                grad.addColorStop(0, 'rgba(255, 255, 255, 0.25)');
                grad.addColorStop(1, 'rgba(255, 255, 255, 0)');
                ctx.fillStyle = grad;
                ctx.fillRect(0, 0, 296, 185);

                ctx.fillStyle = '#fceade';
                ctx.fillRect(141, 62, 14, 15);
                ctx.beginPath();
                ctx.arc(148, 48, 20, 0, Math.PI*2);
                ctx.fill();

                ctx.fillStyle = '#2b1055';
                ctx.beginPath();
                ctx.arc(141, 47, 2, 0, Math.PI*2);
                ctx.arc(155, 47, 2, 0, Math.PI*2);
                ctx.fill();

                ctx.fillStyle = outfit.bottom.type === 'bot1' ? '#1f2421' : (outfit.bottom.type === 'bot2' ? '#5c677d' : '#4a3000');
                if(outfit.bottom.type === 'bot1') {
                    ctx.fillRect(135, 110, 12, 45);
                    ctx.fillRect(149, 110, 12, 45);
                } else if(outfit.bottom.type === 'bot2') {
                    ctx.fillRect(133, 110, 14, 45);
                    ctx.fillRect(149, 110, 14, 45);
                } else {
                    ctx.fillStyle = '#b5838d';
                    ctx.fillRect(134, 110, 13, 45);
                    ctx.fillRect(149, 110, 13, 45);
                }

                if(outfit.top.type === 'top1') {
                    ctx.fillStyle = '#2b2d42';
                    drawRoundedRect(ctx, 125, 72, 46, 42, 6);
                    ctx.fillStyle = '#ffffff';
                    ctx.beginPath(); ctx.moveTo(148, 72); ctx.lineTo(142, 88); ctx.lineTo(154, 88); ctx.fill();
                    ctx.fillStyle = '#d90429';
                    ctx.fillRect(146, 85, 4, 14);
                } else if(outfit.top.type === 'top2') {
                    ctx.fillStyle = '#ffb703';
                    drawRoundedRect(ctx, 122, 70, 52, 44, 8);
                    ctx.fillStyle = '#fb8500';
                    ctx.fillRect(122, 90, 52, 6);
                } else {
                    ctx.fillStyle = '#8338ec';
                    drawRoundedRect(ctx, 126, 72, 44, 42, 10);
                    ctx.fillStyle = '#3a86ff';
                    ctx.fillRect(140, 72, 16, 12);
                }

                ctx.fillStyle = outfit.shoes.type === 'shoe1' ? '#000000' : (outfit.shoes.type === 'shoe2' ? '#382b22' : '#ffffff');
                ctx.fillRect(131, 155, 14, 10);
                ctx.fillRect(151, 155, 14, 10);

                ctx.fillStyle = '#3a0ca3';
                if(outfit.hair.type === 'hair1') {
                    ctx.beginPath();
                    ctx.arc(148, 42, 22, Math.PI, Math.PI * 2);
                    ctx.lineTo(172, 50); ctx.lineTo(148, 30); ctx.lineTo(124, 50);
                    ctx.fill();
                } else if(outfit.hair.type === 'hair2') {
                    ctx.beginPath();
                    ctx.arc(148, 40, 23, 0, Math.PI * 2);
                    ctx.fill();
                } else {
                    ctx.beginPath();
                    ctx.arc(148, 42, 22, Math.PI, Math.PI * 2);
                    ctx.fillRect(123, 40, 6, 22);
                    ctx.fillRect(167, 40, 6, 22);
                    ctx.fill();
                }

                ctx.fillStyle = '#ffeb3b'; ctx.font = 'bold 11px Arial';
                ctx.fillText("🎨 穿搭: " + outfit.top.name + " + " + outfit.bottom.name, 12, 20);
            }

            setCategory('hair');
            drawDoll();
        </script>
    </body>
    </html>
    """
  ]
  components.html(html_code, height=275)


# -------------------------------------------------------------------
# 🥞 4. 双人动态互动【实体双层松饼左右摆动堆高游戏】
# -------------------------------------------------------------------
def render_pancake_stack_game(member_name):
  html_code = (
      """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .pancake-box { background: #1a0f30; border: 3px solid #ff80ab; border-radius: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.3); padding: 10px; width: 320px; text-align: center; }
            canvas { display: block; margin: 0 auto; background: #211035; border-radius: 10px; border: 2px solid #ff4081; }
            .drop-btn { background: linear-gradient(45deg, #ff4081, #ab47bc); color: white; border: none; padding: 10px 0; font-size: 15px; font-weight: bold; border-radius: 15px; cursor: pointer; width: 300px; margin-top: 8px; box-shadow: 0 4px 10px rgba(255,64,129,0.4); }
            .drop-btn:active { transform: scale(0.95); }
        </style>
    </head>
    <body>
        <div class="pancake-box">
            <div style="color: #ffeb3b; font-weight: bold; font-size: 12px; margin-bottom: 4px;">🥞 后台双人互动：与 """
      + member_name
      + """ 的松饼叠高挑战！</div>
            <canvas id="pancakeCanvas" width="300" height="195"></canvas>
            <button class="drop-btn" onclick="dropPancake()">🥞 看准时机：放下松饼！</button>
        </div>
        <script>
            const canvas = document.getElementById('pancakeCanvas');
            const ctx = canvas.getContext('2d');

            let swingX = 150, swingDir = 2.2;
            let stack = [{x: 100, y: 165, w: 100, h: 22}];
            let current = {x: 150, y: 35, w: 90, h: 22, dropping: false, vy: 0};
            let score = 0, isGameOver = false;
            let memberComment = "加油！看准中心叠上去！";

            function dropPancake() {
                if (isGameOver || current.dropping) return;
                current.dropping = true;
                current.x = swingX - current.w / 2;
                current.vy = 4.0;
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
                drawRoundedRect(ctx, x, y, w, h, 6);
                ctx.strokeStyle = '#bc6c25';
                ctx.lineWidth = 2;
                ctx.stroke();

                ctx.fillStyle = '#faedcd';
                ctx.fillRect(x + 10, y + 6, w - 20, 4);

                if (isBase || y < 140) {
                    ctx.fillStyle = '#ffffff';
                    ctx.beginPath();
                    ctx.arc(x + w / 2, y + 4, 8, 0, Math.PI * 2);
                    ctx.fill();
                }
            }

            function loop() {
                ctx.clearRect(0, 0, 300, 195);

                ctx.fillStyle = '#2d1b4e';
                ctx.fillRect(5, 5, 135, 30);
                ctx.fillStyle = '#00e676'; ctx.font = 'bold 11px Arial';
                ctx.fillText("🧑‍🎤 你 (层数: " + score + ")", 12, 23);

                ctx.fillStyle = '#2d1b4e';
                ctx.fillRect(160, 5, 135, 30);
                ctx.fillStyle = '#ff80ab'; ctx.font = 'bold 11px Arial';
                ctx.fillText("🌟 """ + member_name + """", 168, 23);

                if (!current.dropping && !isGameOver) {
                    swingX += swingDir;
                    if (swingX > 230 || swingX < 70) swingDir *= -1;
                    ctx.strokeStyle = '#ff80ab'; ctx.lineWidth = 2;
                    ctx.beginPath(); ctx.moveTo(swingX, 40); ctx.lineTo(swingX, 60); ctx.stroke();
                } else if (current.dropping) {
                    current.y += current.vy;
                    let top = stack[stack.length - 1];
                    if (current.y + current.h >= top.y) {
                        current.dropping = false;
                        let overlap = Math.min(current.x + current.w, top.x + top.w) - Math.max(current.x, top.x);
                        if (overlap > 25) {
                            score++;
                            let newW = Math.max(45, current.w - 5);
                            stack.push({ x: current.x, y: top.y - 22, w: newW, h: 22 });
                            current = { x: 150, y: 35, w: newW, h: 22, dropping: false, vy: 0 };
                            memberComment = score >= 5 ? "太稳了！绝佳默契！" : "干得漂亮！继续保持！";
                            if (stack.length >= 7) isGameOver = true;
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
                    drawPancakeEntity(ctx, drawX, current.dropping ? current.y : 60, current.w, current.h, false);
                }

                ctx.fillStyle = 'rgba(0,0,0,0.4)';
                ctx.fillRect(0, 172, 300, 23);
                ctx.fillStyle = '#ffeb3b'; ctx.font = '11px Arial';
                ctx.fillText("💬 队友 """ + member_name + """: " + memberComment, 12, 188);

                if (isGameOver) {
                    ctx.fillStyle = 'rgba(0,0,0,0.85)'; ctx.fillRect(0, 0, 300, 195);
                    ctx.fillStyle = '#00e676'; ctx.font = 'bold 16px Arial';
                    ctx.fillText("🎉 堆高挑战完成！总得分: " + score, 40, 100);
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
  components.html(html_code, height=275)


# -------------------------------------------------------------------
# ⏱️ 5. 演唱会后台紧急换装 QTE 小游戏
# -------------------------------------------------------------------
def render_wardrobe_qte_game(member_name):
  html_code = (
      """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .qte-box { background: #1a0f30; border: 3px solid #ff80ab; border-radius: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.3); padding: 15px; width: 320px; text-align: center; }
            .qte-target { font-size: 32px; background: #2d1b4e; border: 2px dashed #ff4081; border-radius: 12px; padding: 10px; margin: 10px 0; color: #fff; }
            .qte-btns { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-top: 10px; }
            .q-btn { background: linear-gradient(45deg, #ff4081, #ab47bc); color: white; border: none; padding: 12px 0; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
            .q-btn:active { transform: scale(0.95); }
        </style>
    </head>
    <body>
        <div class="qte-box">
            <div style="color: #ffeb3b; font-weight: bold; font-size: 13px;">⏱️ 演唱会暗场 30 秒：紧急换装 QTE！</div>
            <div style="color: #fff; font-size: 11px; margin-top: 4px;">"""
      + member_name
      + """ 跑过来帮你一把！点击匹配的换装动作！</div>
            <div class="qte-target" id="targetAction">🧥 扣上舞台战袍纽扣</div>
            <div style="color: #00e676; font-size: 12px; font-weight: bold;">🔥 成功连击: <span id="qteScore">0</span> / 5 | ⏳ <span id="qTime">10</span>s</div>
            <div class="qte-btns">
                <button class="q-btn" onclick="pressQTE('扣纽扣')">🧥 扣纽扣</button>
                <button class="q-btn" onclick="pressQTE('戴耳返')">🎧 戴耳返</button>
                <button class="q-btn" onclick="pressQTE('拿话筒')">🎤 拿话筒</button>
                <button class="q-btn" onclick="pressQTE('正领带')">👔 正领带</button>
            </div>
        </div>
        <script>
            const actions = ['扣纽扣', '戴耳返', '拿话筒', '正领带'];
            const actionIcons = { '扣纽扣': '🧥 扣上舞台战袍纽扣', '戴耳返': '🎧 戴上专业无线耳返', '拿话筒': '🎤 拿起闪耀定制话筒', '正领带': '👔 快速整理好演出领带' };
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
                    document.getElementById('targetAction').innerText = score >= 5 ? "🎉 换装完美成功！闪亮登场！" : "💧 时间到！有点手忙脚乱...";
                }
            }, 1000);

            function pressQTE(act) {
                if (isOver) return;
                if (act === current) {
                    score++;
                    document.getElementById('qteScore').innerText = score;
                    if (score >= 5) {
                        isOver = true;
                        document.getElementById('targetAction').innerText = "🎉 换装完美成功！闪亮登场！";
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
  components.html(html_code, height=295)


# -------------------------------------------------------------------
# 🤝 6. 成员双人互动【默契猜拳对决】
# -------------------------------------------------------------------
def render_member_duel_game(member_name):
  html_code = (
      """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .duel-box { background: #1a0f30; border: 3px solid #ff80ab; border-radius: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.3); padding: 15px; width: 320px; text-align: center; }
            .vs-display { display: flex; justify-content: space-around; align-items: center; margin: 15px 0; color: #fff; font-size: 16px; font-weight: bold; }
            .avatar { background: #2d1b4e; border: 2px solid #ff4081; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; font-size: 24px; margin: 0 auto 5px auto; }
            .duel-btns { display: flex; gap: 8px; margin-top: 10px; }
            .d-btn { background: linear-gradient(45deg, #ff4081, #ab47bc); color: white; border: none; padding: 12px 0; font-size: 15px; font-weight: bold; border-radius: 12px; cursor: pointer; flex: 1; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
            .d-btn:active { transform: scale(0.95); }
            #duel-result { color: #ffeb3b; font-size: 14px; font-weight: bold; margin-top: 10px; min-height: 24px; }
        </style>
    </head>
    <body>
        <div class="duel-box">
            <div style="color: #ffeb3b; font-weight: bold; font-size: 14px;">🤝 与 """
      + member_name
      + """ 的后台默契猜拳对决！</div>
            <div class="vs-display">
                <div>
                    <div class="avatar">🧑‍🎤</div>
                    <div>你</div>
                    <div id="playerChoice" style="font-size: 20px; margin-top: 5px;">❓</div>
                </div>
                <div style="color:#ff4081; font-size: 20px; font-weight:bold;">VS</div>
                <div>
                    <div class="avatar">🌟</div>
                    <div>"""
      + member_name
      + """</div>
                    <div id="memberChoice" style="font-size: 20px; margin-top: 5px;">❓</div>
                </div>
            </div>
            <div id="duel-result">请选择你的出拳，赢过 """
      + member_name
      + """ 提升团员羁绊！</div>
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
                    resMsg = "🤝 平局！两人默契十足！";
                } else if (
                    (pChoice === '石头' && mChoice === '剪刀') ||
                    (pChoice === '剪刀' && mChoice === '布') ||
                    (pChoice === '布' && mChoice === '石头')
                ) {
                    resMsg = "🎉 赢了！"""
      + member_name
      + """ 为你鼓掌欢呼！";
                    resColor = "#00e676";
                    wins++;
                } else {
                    resMsg = "💧 输啦！"""
      + member_name
      + """ 得意地笑了起来！";
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
  components.html(html_code, height=310)


# -------------------------------------------------------------------
# 🍜 7. 成员双人互动【深夜拉面大胃王比拼】
# -------------------------------------------------------------------
def render_ramen_battle_game(member_name):
  html_code = (
      """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .battle-box { background: #1a0f30; border: 3px solid #ff80ab; border-radius: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.3); padding: 15px; width: 320px; text-align: center; }
            .bowl { font-size: 45px; margin: 10px 0; }
            .score-row { display: flex; justify-content: space-around; color: #fff; font-size: 14px; font-weight: bold; margin-bottom: 10px; }
            .eat-btn { background: linear-gradient(45deg, #ff5252, #ffeb3b); color: #333; border: none; padding: 14px 0; font-size: 17px; font-weight: bold; border-radius: 20px; cursor: pointer; width: 100%; box-shadow: 0 4px 15px rgba(255,82,82,0.5); }
            .eat-btn:active { transform: scale(0.95); }
        </style>
    </head>
    <body>
        <div class="battle-box">
            <div style="color: #ffeb3b; font-weight: bold; font-size: 14px;">🍜 深夜食堂：与 """
      + member_name
      + """ 的拉面大胃王对决！</div>
            <div class="bowl" id="bowlIcon">🍜</div>
            <div class="score-row">
                <div>你吃面: <span id="playerBowls" style="color:#00e676; font-size:16px;">0</span> 碗</div>
                <div>"""
      + member_name
      + """: <span id="memberBowls" style="color:#ff4081; font-size:16px;">0</span> 碗</div>
            </div>
            <div id="ramen-tip" style="color: #fff; font-size: 12px; font-weight: bold; margin-bottom: 8px;">⏳ 倒计时: <span id="rTime">10</span>s | 疯狂猛点按钮炫面！</div>
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
                    let resultText = pBowls > mBowls ? "🎉 你赢了！打破了大胃王纪录！" : "💧 输给 """
      + member_name
      + """ 了！对方吃得太快了！";
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
  components.html(html_code, height=310)


# -------------------------------------------------------------------
# 🌟 8. 演唱会手灯狂热小游戏
# -------------------------------------------------------------------
def render_lightstick_game():
  html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .light-box { background: #1a0f30; border: 3px solid #ff80ab; border-radius: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.3); padding: 15px; width: 320px; text-align: center; }
            .color-display { width: 90px; height: 90px; border-radius: 50%; margin: 10px auto; box-shadow: 0 0 20px rgba(255,255,255,0.4); border: 3px solid #fff; }
            .color-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 10px; }
            .color-btn { padding: 12px 0; font-size: 15px; font-weight: bold; border-radius: 12px; border: none; color: white; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
            .color-btn:active { transform: scale(0.95); }
        </style>
    </head>
    <body>
        <div class="light-box">
            <div style="color: #ffeb3b; font-weight: bold; font-size: 13px;">🌟 演唱会手灯狂热！按下与上方匹配的颜色！</div>
            <div class="color-display" id="targetColorBox"></div>
            <div id="light-tip" style="color: #fff; font-size: 12px; font-weight: bold;">⏳ 剩余: <span id="timeVal">12</span>s | 得分: <span id="scoreVal">0</span></div>
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
  )
  components.html(html_code, height=290)


# -------------------------------------------------------------------
# ⚡ 9. 15 秒灯光闪避生存小游戏
# -------------------------------------------------------------------
def render_dodge_canvas_game():
  html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
            .canvas-box { background: #1a0f30; border: 3px solid #ff80ab; border-radius: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.3); position: relative; overflow: hidden; width: 320px; height: 210px; }
            canvas { display: block; }
            .ctrl-panel { display: flex; gap: 15px; margin-top: 10px; width: 320px; justify-content: center; }
            .move-btn { background: linear-gradient(45deg, #ff4081, #ab47bc); color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 20px; cursor: pointer; flex: 1; }
            .move-btn:active { transform: scale(0.95); }
        </style>
    </head>
    <body>
        <div class="canvas-box"><canvas id="dodgeCanvas" width="320" height="210"></canvas></div>
        <div class="ctrl-panel">
            <button class="move-btn" onclick="movePlayer(-1)">⬅️ 往左闪避</button>
            <button class="move-btn" onclick="movePlayer(1)">往右闪避 ➡️</button>
        </div>
        <script>
            const canvas = document.getElementById('dodgeCanvas');
            const ctx = canvas.getContext('2d');
            let lane = 1, lanesX = [60, 160, 260], playerY = 170, obstacles = [], hp = 3, timeLeft = 15, isGameOver = false;
            let timer = setInterval(() => { if(timeLeft > 0 && !isGameOver) timeLeft--; else { isGameOver = true; clearInterval(timer); clearInterval(spawner); } }, 1000);
            let spawner = setInterval(() => { if(!isGameOver) obstacles.push({ lane: Math.floor(Math.random()*3), y: -20, speed: 4.0 }); }, 550);
            function movePlayer(dir) { if(!isGameOver) { lane += dir; if(lane < 0) lane = 0; if(lane > 2) lane = 2; } }
            function loop() {
                ctx.clearRect(0, 0, 320, 210);
                ctx.strokeStyle = '#2d1b4e'; ctx.lineWidth = 2; ctx.setLineDash([4, 4]);
                [110, 210].forEach(x => { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 210); ctx.stroke(); });
                ctx.setLineDash([]);
                for (let i = obstacles.length - 1; i >= 0; i--) {
                    let obs = obstacles[i]; obs.y += obs.speed;
                    ctx.fillStyle = '#ff5252'; ctx.beginPath(); ctx.arc(lanesX[obs.lane], obs.y, 13, 0, Math.PI*2); ctx.fill();
                    ctx.fillStyle = '#fff'; ctx.font = '11px Arial'; ctx.fillText('💡', lanesX[obs.lane]-6, obs.y+4);
                    if (obs.y >= playerY-15 && obs.y <= playerY+15 && obs.lane === lane) {
                        hp--; obstacles.splice(i, 1); if(hp <= 0) isGameOver = true;
                    } else if (obs.y > 230) { obstacles.splice(i, 1); }
                }
                let px = lanesX[lane];
                ctx.fillStyle = '#ff4081'; ctx.beginPath(); ctx.arc(px, playerY, 14, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = '#fff'; ctx.font = '12px Arial'; ctx.fillText('⭐', px-6, playerY+4);
                ctx.fillStyle = '#fff'; ctx.font = 'bold 13px Arial'; ctx.fillText("⏱️ 倒计时: " + timeLeft + "s", 15, 20);
                ctx.fillStyle = '#ff4081'; ctx.fillText("❤️ 生命: " + "❤️".repeat(Math.max(0, hp)), 210, 20);
                if (!isGameOver) requestAnimationFrame(loop);
                else { ctx.fillStyle = 'rgba(0,0,0,0.85)'; ctx.fillRect(0,0,320,210); ctx.fillStyle = '#00e676'; ctx.font = 'bold 18px Arial'; ctx.fillText("🎉 生存挑战成功！", 70, 105); }
            }
            loop();
        </script>
    </body>
    </html>
    """
  )
  components.html(html_code, height=300)


# -------------------------------------------------------------------
# 📖 精简平衡至 25 章的剧情数据库
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

  if st.session_state.stress >= 70:
    st.warning(
        f"⚠️ **【压力预警】** 压力值已达 **{st.session_state.stress}%**！{member} 悄悄塞给你一罐热可可：“别把自己逼太紧，大家都在呢。”"
    )
    st.session_state.stress = 30
    st.session_state.bond += 10

  is_free_training_day = curr_stage in [3, 20]  # Stage 9 为小分队选拔互动游戏

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

  # 阶段 9 🔥（限定 Unit 小分队概念选拔小游戏）
  elif curr_stage == 9:
    st.subheader("📍 Stage 9：【社内企划】限定 Unit 小分队概念选拔赛")
    st.markdown(
        f'<div class="event-card"><b>🏆 【小分队概念选拔游戏】</b><br>事务所突然下达了全新企划通知！要在 10 秒内为 <b>{member}</b> 与你所在的组合挑选出 3 个最核心的舞台概念卡牌，冲击限定单曲出道！</div>',
        unsafe_allow_html=True,
    )
    render_unit_selection_game()

    if st.button("➔ 选拔结束，锁定小分队企划！"):
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

  # 阶段 17：👗 精致暖暖风男装纸娃娃换装
  elif curr_stage == 17:
    st.subheader("📍 Stage 17：【杂志封面拍摄】偶像纸娃娃高级定制间")
    st.markdown(
        '<div class="event-card"><b>👗 【奇迹暖暖风：男装换装搭配间】</b><br>即将拍摄出道单曲的杂志封面！请在下方为男神模特自由搭配<b>精致发型、男团西装/战袍、潮酷裤装与鞋子</b>！</div>',
        unsafe_allow_html=True,
    )
    render_dress_up_game()

    if st.button("➔ 搭配完成，拍摄封面！"):
      st.session_state.fans += 2000
      st.session_state.variety += 20
      st.session_state.stage += 1
      st.rerun()

  # 阶段 18：🤝 成员双人互动【默契猜拳对决】
  elif curr_stage == 18:
    st.subheader(f"📍 Stage 18：【后台趣味互动·与 {member} 的默契对决】")
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
