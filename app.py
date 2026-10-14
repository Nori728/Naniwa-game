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
# 小游戏渲染组件
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
    </style></head><body>
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
            else { 
                ctx.fillStyle = 'rgba(0,0,0,0.85)'; ctx.fillRect(0,0,300,220); 
                if(score >= 800) { ctx.fillStyle = '#00e676'; ctx.font = 'bold 16px Arial'; ctx.fillText("🎉 打歌挑战成功！总分: " + score, 35, 115); }
                else { ctx.fillStyle = '#ff5252'; ctx.font = 'bold 16px Arial'; ctx.fillText("💧 挑战失败！分数未达标: " + score, 35, 115); }
            }
        }
        loop();
    </script></body></html>
    """
  components.html(html_code, height=295)


def render_dirt_dig_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .dig-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 14px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); padding: 10px; width: 300px; text-align: center; }
    .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin: 8px 0; }
    .dirt-tile { background: #5d4037; border: 2px solid #8d6e63; color: #d7ccc8; height: 42px; border-radius: 8px; font-size: 11px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 3px 5px rgba(0,0,0,0.3); }
    .dirt-tile:active { transform: scale(0.95); }
    .dirt-tile.dug { background: #3e2723; border: 2px dashed #6d4c41; color: #fff; cursor: default; }
    #dig-tip { color: #ffeb3b; font-size: 11px; font-weight: bold; min-height: 18px; }
    </style></head><body>
    <div class="dig-box">
        <div style="color: #fff; font-weight: bold; font-size: 11px;">⛏️ 用铁锹敲开土块！(剩余铲子: <span id="shovels">6</span>)</div>
        <div class="grid" id="dirtGrid"></div>
        <div id="dig-tip">点击土块挖掘宝物转化为实际属性！</div>
    </div>
    <script>
        let tiles = Array(12).fill(false), contents = Array(12).fill('💨 空'), shovels = 6, treasuresFound = 0, isOver = false;
        let placed = 0; const prizePool = ['💎 金唱片(+500粉)', '✨ 签名照(+15绊)', '🏆 奖杯(+20能力)'];
        while(placed < 3) { let idx = Math.floor(Math.random() * 12); if(!tiles[idx]) { tiles[idx] = true; contents[idx] = prizePool[placed % prizePool.length]; placed++; } }
        const gridEl = document.getElementById('dirtGrid'), tipEl = document.getElementById('dig-tip'), shovelEl = document.getElementById('shovels');
        function renderGrid() {
            gridEl.innerHTML = '';
            for(let i=0; i<12; i++) {
                let btn = document.createElement('div'); btn.className = 'dirt-tile'; btn.innerHTML = '🧱 土块';
                btn.onclick = () => digTile(i, btn); gridEl.appendChild(btn);
            }
        }
        function digTile(idx, el) {
            if (isOver || shovels <= 0 || el.classList.contains('dug')) return;
            shovels--; shovelEl.innerText = shovels; el.classList.add('dug');
            if (tiles[idx]) {
                el.innerHTML = contents[idx]; el.style.background = '#00e676'; el.style.color = '#000'; treasuresFound++;
                tipEl.innerHTML = "🎉 挖到 " + contents[idx] + "！"; tipEl.style.color = "#00e676";
                if (treasuresFound === 3 || shovels === 0) { isOver = true; tipEl.innerHTML = "🏆 挖宝完成！找到 " + treasuresFound + " 件宝物！"; }
            } else {
                el.innerHTML = '🕳️ 泥土'; tipEl.innerHTML = "💧 这块土下面什么都没有..."; tipEl.style.color = "#ff5252";
                if (shovels === 0) { isOver = true; tipEl.innerHTML = "💧 铲子用光！找到 " + treasuresFound + " 件宝物！"; }
            }
        }
        renderGrid();
    </script></body></html>
    """
  components.html(html_code, height=255)


def render_ramen_battle_game(member_name):
  html_code = f"""
    <!DOCTYPE html><html><head><style>
    body {{ background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }}
    .battle-box {{ background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); padding: 10px; width: 300px; text-align: center; }}
    .progress-container {{ background: #211035; border: 1.5px solid #ff4081; border-radius: 8px; height: 16px; margin: 5px 0; overflow: hidden; position: relative; }}
    .progress-bar {{ height: 100%; width: 0%; transition: width 0.1s ease; }}
    .eat-btn {{ background: linear-gradient(45deg, #ff5252, #ffeb3b); color: #333; border: none; padding: 10px 0; font-size: 14px; font-weight: bold; border-radius: 14px; cursor: pointer; width: 100%; box-shadow: 0 3px 10px rgba(255,82,82,0.5); margin-top: 6px; }}
    .eat-btn:active {{ transform: scale(0.95); }}
    </style></head><body>
    <div class="battle-box">
        <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">🍜 深夜食堂：与 {member_name} 的拉面大胃王激战！</div>
        <div style="text-align: left; font-size: 11px; color: #00e676; margin-top: 4px;">🧑‍🎤 你 (进度: <span id="pCount">0</span> 碗)</div>
        <div class="progress-container"><div class="progress-bar" id="pBar" style="background: #00e676; width: 0%;"></div></div>
        <div style="text-align: left; font-size: 11px; color: #ff4081; margin-top: 4px;">🌟 {member_name} (进度: <span id="mCount">0</span> 碗)</div>
        <div class="progress-container"><div class="progress-bar" id="mBar" style="background: #ff4081; width: 0%;"></div></div>
        <div id="ramen-tip" style="color: #fff; font-size: 11px; font-weight: bold; margin-top: 6px;">⏳ 倒计时: <span id="rTime">10</span>s | 必须超越对手才算胜利！</div>
        <button class="eat-btn" onclick="eatRamen()">🥢 疯狂猛点：炫面！</button>
    </div>
    <script>
        let pBowls = 0, mBowls = 0, timeLeft = 10, isOver = false; const targetBowls = 25;
        const pSpan = document.getElementById('pCount'), mSpan = document.getElementById('mCount');
        const pBar = document.getElementById('pBar'), mBar = document.getElementById('mBar'), tSpan = document.getElementById('rTime'), tipEl = document.getElementById('ramen-tip');
        let aiTimer = setInterval(() => {{ if (!isOver && mBowls < targetBowls) {{ mBowls += 0.8; mSpan.innerText = Math.floor(mBowls); mBar.style.width = Math.min(100, (mBowls / targetBowls) * 100) + '%'; checkWin(); }} }}, 300);
        let clock = setInterval(() => {{ if (timeLeft > 0 && !isOver) {{ timeLeft--; tSpan.innerText = timeLeft; }} else {{ if(!isOver) finishGame(); }} }}, 1000);
        function eatRamen() {{ if (isOver) return; pBowls++; pSpan.innerText = pBowls; pBar.style.width = Math.min(100, (pBowls / targetBowls) * 100) + '%'; checkWin(); }}
        function checkWin() {{ if (isOver) return; if (pBowls >= targetBowls && pBowls > mBowls) {{ isOver = true; clearInterval(clock); clearInterval(aiTimer); tipEl.innerHTML = "🎉 挑战成功！你赢过了 {member_name}！"; tipEl.style.color = "#00e676"; }} }}
        function finishGame() {{ isOver = true; clearInterval(clock); clearInterval(aiTimer); if (pBowls > mBowls) {{ tipEl.innerHTML = "🎉 挑战成功！击败了队友！"; tipEl.style.color = "#00e676"; }} else {{ tipEl.innerHTML = "💧 挑战失败！吃得太慢，输给 {member_name} 了！"; tipEl.style.color = "#ff5252"; }} }}
    </script></body></html>
    """
  components.html(html_code, height=295)


def render_eyecatch_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .game-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 14px; box-shadow: 0 6px 20px rgba(255,64,129,0.4); position: relative; overflow: hidden; width: 300px; height: 230px; }
    canvas { display: block; }
    .ctrl-panel { display: flex; gap: 6px; margin-top: 8px; width: 300px; justify-content: center; }
    .m-btn { background: linear-gradient(45deg, #ff4081, #ab47bc); color: white; border: none; padding: 10px 0; font-size: 13px; font-weight: bold; border-radius: 10px; cursor: pointer; flex: 1; box-shadow: 0 3px 8px rgba(0,0,0,0.3); }
    .m-btn:active { transform: scale(0.95); background: #00e676; color: #000; }
    </style></head><body>
    <div class="game-box"><canvas id="eyeCanvas" width="300" height="230"></canvas></div>
    <div class="ctrl-panel">
        <button class="m-btn" onclick="movePlayer(-1)">⬅️ 往左移动</button>
        <button class="m-btn" onclick="fireWink()">⚡ 发射Wink！</button>
        <button class="m-btn" onclick="movePlayer(1)">往右移动 ➡️</button>
    </div>
    <script>
        const canvas = document.getElementById('eyeCanvas'); const ctx = canvas.getContext('2d');
        let lane = 1, lanesX = [55, 150, 245], playerY = 190, items = [], particles = [], score = 0, hp = 3, timeLeft = 15, isGameOver = false, laserEffect = null;
        let timer = setInterval(() => { if(timeLeft > 0 && !isGameOver) timeLeft--; else { isGameOver = true; clearInterval(timer); clearInterval(spawner); } }, 1000);
        let spawner = setInterval(() => { if(!isGameOver) { let type = Math.random() > 0.35 ? 'heart' : 'bomb'; items.push({ lane: Math.floor(Math.random()*3), y: -20, speed: 3.2, type: type }); } }, 600);
        function movePlayer(dir) { if(!isGameOver) { lane += dir; if(lane < 0) lane = 0; if(lane > 2) lane = 2; } }
        function triggerExplosion(x, y, isGood) {
            let color = isGood ? '#ff4081' : '#ff5252';
            for(let i=0; i<12; i++) { let angle = Math.random() * Math.PI * 2; let speed = Math.random() * 3 + 1.5; particles.push({ x: x, y: y, vx: Math.cos(angle)*speed, vy: Math.sin(angle)*speed, color: color, life: 18 }); }
        }
        function fireWink() {
            if(isGameOver) return; laserEffect = { lane: lane, timer: 12 };
            for(let i = items.length - 1; i >= 0; i--) {
                let it = items[i];
                if(it.lane === lane && it.y >= 70 && it.y <= 210) {
                    if(it.type === 'heart') { score += 200; triggerExplosion(lanesX[lane], it.y, true); }
                    else { hp--; triggerExplosion(lanesX[lane], it.y, false); if(hp <= 0) isGameOver = true; }
                    items.splice(i, 1); break;
                }
            }
        }
        function loop() {
            ctx.clearRect(0, 0, 300, 230);
            ctx.strokeStyle = 'rgba(255, 128, 171, 0.15)'; ctx.lineWidth = 1.5; ctx.setLineDash([4, 4]);
            [100, 200].forEach(x => { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 230); ctx.stroke(); }); ctx.setLineDash([]);
            for (let i = items.length - 1; i >= 0; i--) { let it = items[i]; it.y += it.speed; ctx.font = '20px Arial'; ctx.fillText(it.type === 'heart' ? '💖' : '💣', lanesX[it.lane]-10, it.y+10); if (it.y > 230) items.splice(i, 1); }
            for (let i = particles.length - 1; i >= 0; i--) { let p = particles[i]; p.x += p.vx; p.y += p.vy; p.life--; ctx.fillStyle = p.color; ctx.fillRect(p.x, p.y, 4, 4); if(p.life <= 0) particles.splice(i, 1); }
            if(laserEffect && laserEffect.timer > 0) { ctx.strokeStyle = '#00ffff'; ctx.lineWidth = 4; ctx.shadowBlur = 15; ctx.shadowColor = '#00ffff'; ctx.beginPath(); ctx.moveTo(lanesX[laserEffect.lane], playerY); ctx.lineTo(lanesX[laserEffect.lane], 0); ctx.stroke(); ctx.shadowBlur = 0; laserEffect.timer--; }
            let px = lanesX[lane]; ctx.font = '24px Arial'; ctx.fillText('🌟', px-12, playerY+10);
            ctx.fillStyle = '#fff'; ctx.font = 'bold 11px Arial'; ctx.fillText("⏱️ 倒计时: " + timeLeft + "s", 10, 18); ctx.fillText("💖 得分: " + score, 110, 18); ctx.fillStyle = '#ff5252'; ctx.fillText("❤️ " + "❤️".repeat(Math.max(0, hp)), 210, 18);
            if (!isGameOver) requestAnimationFrame(loop);
            else { 
                ctx.fillStyle = 'rgba(0,0,0,0.88)'; ctx.fillRect(0,0,300,230); 
                if (hp > 0 && score >= 800) { ctx.fillStyle = '#00e676'; ctx.font = 'bold 16px Arial'; ctx.fillText("🎉 Wink大神挑战成功！", 55, 105); ctx.fillStyle = '#ffeb3b'; ctx.font = '13px Arial'; ctx.fillText("最终得分: " + score, 110, 135); }
                else { ctx.fillStyle = '#ff5252'; ctx.font = 'bold 16px Arial'; ctx.fillText("💧 挑战失败！生命耗尽或分数不足", 35, 105); ctx.fillStyle = '#fff'; ctx.font = '13px Arial'; ctx.fillText("最终得分: " + score, 110, 135); }
            }
        }
        loop();
    </script></body></html>
    """
  components.html(html_code, height=295)


def render_magazine_photo_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .photo-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 14px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); padding: 10px; width: 300px; text-align: center; }
    .viewfinder { background: linear-gradient(135deg, #2b1055, #4a148c); border: 3px dashed #00e676; border-radius: 10px; padding: 12px; margin: 8px 0; color: #fff; font-size: 15px; font-weight: bold; }
    .photo-btns { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin-top: 8px; }
    .p-btn { background: linear-gradient(180deg, #ff4081, #7b1fa2); color: white; border: 1.5px solid #ff80ab; padding: 10px 0; font-size: 12px; font-weight: bold; border-radius: 8px; cursor: pointer; }
    .p-btn:active { transform: scale(0.95); background: #00e676; color: #000; }
    </style></head><body>
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
        const poses = [{ type: '侧颜', label: '✨ 监视器指示：【捕捉侧颜绝杀】' }, { type: '大笑', label: '😁 监视器指示：【抓拍阳光大笑】' }, { type: '眼神', label: '👀 监视器指示：【锁定电眼特写】' }];
        let currentPose = poses[0], score = 0, timeLeft = 10, isOver = false;
        function nextPose() { if (isOver) return; currentPose = poses[Math.floor(Math.random() * poses.length)]; document.getElementById('targetPose').innerText = currentPose.label; }
        let timer = setInterval(() => {
            if (timeLeft > 0 && !isOver) { timeLeft--; document.getElementById('pTime').innerText = timeLeft; }
            else { isOver = true; clearInterval(timer); if(score >= 6) document.getElementById('targetPose').innerText = "🎉 杂志封面大片完美诞生！"; else document.getElementById('targetPose').innerText = "💧 拍摄失败！快门按得不够准..."; }
        }, 1000);
        function pressPhoto(type) {
            if (isOver) return;
            if (type === currentPose.type) { score++; document.getElementById('pScore').innerText = score; if (score >= 6) { isOver = true; document.getElementById('targetPose').innerText = "🎉 杂志封面大片完美诞生！"; } else nextPose(); }
        }
        nextPose();
    </script></body></html>
    """
  components.html(html_code, height=275)


def render_wardrobe_qte_game(member_name):
  html_code = f"""
    <!DOCTYPE html><html><head><style>
    body {{ background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }}
    .qte-box {{ background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); padding: 10px; width: 300px; text-align: center; }}
    .qte-target {{ font-size: 24px; background: #2d1b4e; border: 2px dashed #ff4081; border-radius: 10px; padding: 8px; margin: 8px 0; color: #fff; }}
    .qte-btns {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; margin-top: 8px; }}
    .q-btn {{ background: linear-gradient(45deg, #ff4081, #ab47bc); color: white; border: none; padding: 10px 0; font-size: 13px; font-weight: bold; border-radius: 10px; cursor: pointer; }}
    .q-btn:active {{ transform: scale(0.95); }}
    </style></head><body>
    <div class="qte-box">
        <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">⏱️ 演唱会暗场 30 秒：紧急换装 QTE！</div>
        <div style="color: #fff; font-size: 11px; margin-top: 3px;">{member_name} 帮你一把！点击匹配动作！</div>
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
        const actionIcons = {{ '扣纽扣': '🧥 扣上战袍纽扣', '戴耳返': '🎧 戴上无线耳返', '拿话筒': '🎤 拿起定制话筒', '正领带': '👔 整理演出领带' }};
        let current = '扣纽扣', score = 0, timeLeft = 10, isOver = false;
        function nextAction() {{ if (isOver) return; current = actions[Math.floor(Math.random() * actions.length)]; document.getElementById('targetAction').innerText = actionIcons[current]; }}
        let timer = setInterval(() => {{ if (timeLeft > 0 && !isOver) {{ timeLeft--; document.getElementById('qTime').innerText = timeLeft; }} else {{ isOver = true; clearInterval(timer); if(score >= 5) document.getElementById('targetAction').innerText = "🎉 换装成功！登场！"; else document.getElementById('targetAction').innerText = "💧 挑战失败！手忙脚乱..."; }} }}, 1000);
        function pressQTE(act) {{ if (isOver) return; if (act === current) {{ score++; document.getElementById('qteScore').innerText = score; if (score >= 5) {{ isOver = true; document.getElementById('targetAction').innerText = "🎉 换装成功！登场！"; }} else nextAction(); }} }}
        nextAction();
    </script></body></html>
    """
  components.html(html_code, height=270)


def render_dodge_canvas_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .canvas-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); position: relative; overflow: hidden; width: 300px; height: 185px; }
    canvas { display: block; }
    .ctrl-panel { display: flex; gap: 10px; margin-top: 8px; width: 300px; justify-content: center; }
    .move-btn { background: linear-gradient(45deg, #ff4081, #ab47bc); color: white; border: none; padding: 10px 0; font-size: 14px; font-weight: bold; border-radius: 16px; cursor: pointer; flex: 1; }
    .move-btn:active { transform: scale(0.95); }
    </style></head><body>
    <div class="canvas-box"><canvas id="dodgeCanvas" width="300" height="185"></canvas></div>
    <div class="ctrl-panel">
        <button class="move-btn" onclick="movePlayer(-1)">⬅️ 往左闪避</button>
        <button class="move-btn" onclick="movePlayer(1)">往右闪避 ➡️</button>
    </div>
    <script>
        const canvas = document.getElementById('dodgeCanvas'); const ctx = canvas.getContext('2d');
        let lane = 1, lanesX = [55, 150, 245], playerY = 150, obstacles = [], hp = 3, timeLeft = 15, isGameOver = false;
        let timer = setInterval(() => { if(timeLeft > 0 && !isGameOver) timeLeft--; else { isGameOver = true; clearInterval(timer); clearInterval(spawner); } }, 1000);
        let spawner = setInterval(() => { if(!isGameOver) obstacles.push({ lane: Math.floor(Math.random()*3), y: -20, speed: 4.0 }); }, 550);
        function movePlayer(dir) { if(!isGameOver) { lane += dir; if(lane < 0) lane = 0; if(lane > 2) lane = 2; } }
        function loop() {
            ctx.clearRect(0, 0, 300, 185);
            ctx.strokeStyle = '#2d1b4e'; ctx.lineWidth = 2; ctx.setLineDash([4, 4]); [100, 200].forEach(x => { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 185); ctx.stroke(); }); ctx.setLineDash([]);
            for (let i = obstacles.length - 1; i >= 0; i--) {
                let obs = obstacles[i]; obs.y += obs.speed; ctx.fillStyle = '#ff5252'; ctx.beginPath(); ctx.arc(lanesX[obs.lane], obs.y, 11, 0, Math.PI*2); ctx.fill(); ctx.fillStyle = '#fff'; ctx.font = '10px Arial'; ctx.fillText('💡', lanesX[obs.lane]-5, obs.y+3);
                if (obs.y >= playerY-13 && obs.y <= playerY+13 && obs.lane === lane) { hp--; obstacles.splice(i, 1); if(hp <= 0) isGameOver = true; } else if (obs.y > 200) obstacles.splice(i, 1);
            }
            let px = lanesX[lane]; ctx.fillStyle = '#ff4081'; ctx.beginPath(); ctx.arc(px, playerY, 12, 0, Math.PI*2); ctx.fill(); ctx.fillStyle = '#fff'; ctx.font = '11px Arial'; ctx.fillText('⭐', px-5, playerY+3);
            ctx.fillStyle = '#fff'; ctx.font = 'bold 12px Arial'; ctx.fillText("⏱️ 倒计时: " + timeLeft + "s", 12, 18); ctx.fillStyle = '#ff4081'; ctx.fillText("❤️ 生命: " + "❤️".repeat(Math.max(0, hp)), 195, 18);
            if (!isGameOver) requestAnimationFrame(loop);
            else { 
                ctx.fillStyle = 'rgba(0,0,0,0.88)'; ctx.fillRect(0,0,300,185); 
                if (hp > 0) { ctx.fillStyle = '#00e676'; ctx.font = 'bold 16px Arial'; ctx.fillText("🎉 生存挑战成功！", 75, 98); }
                else { ctx.fillStyle = '#ff5252'; ctx.font = 'bold 16px Arial'; ctx.fillText("💥 挑战失败！生命耗尽...", 70, 98); }
            }
        }
        loop();
    </script></body></html>
    """
  components.html(html_code, height=250)


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
# 游戏主流程（合理穿插游戏与剧情）
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

  # 自主特训日（Stage 4 & Stage 16）
  if curr_stage in [4, 16]:
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

  # Stage 2：游戏 - 🎹 钢琴块下落打歌
  elif curr_stage == 2:
    st.subheader("📍 Stage 2：【全开麦打歌·节奏钢琴块】")
    st.markdown(
        '<div class="event-card"><b>🎹 【打歌小游戏：下落式节奏钢琴块】</b><br>地方电视台录制现场！点击下方 1-2-3-4 按钮敲击下落的钢琴块，展现你的全开麦硬实力，持续 12 秒！</div>',
        unsafe_allow_html=True,
    )
    render_piano_tiles_game()
    if st.button("➔ 演奏结束，点击进入下一阶段"):
      st.session_state.fans += 1500
      st.session_state.dance += 20
      st.session_state.stage += 1
      st.rerun()

  # Stage 6：游戏 - 🍜 深夜拉面大胃王
  elif curr_stage == 6:
    st.subheader(f"📍 Stage 6：【深夜食堂·与 {member} 的拉面大胃王激战】")
    st.markdown(
        f'<div class="event-card"><b>🍜 【双人对抗小游戏：拉面大胃王】</b><br>高强度练舞结束后大家饿坏了！你和 <b>{member}</b> 展开了 10 秒钟狂炫拉面对抗，手速快才能赢！</div>',
        unsafe_allow_html=True,
    )
    render_ramen_battle_game(member)
    if st.button("➔ 饱餐结束，点击进入下一阶段"):
      st.session_state.bond += 18
      st.session_state.variety += 15
      st.session_state.stage += 1
      st.rerun()

  # Stage 9：突发事件 - 📡 深夜街头突击生放送（选项明牌化）
  elif curr_stage == 9:
    st.subheader("📍 Stage 9：【突发事件】深夜街头突击生放送（直播）！")
    st.markdown(
        f'<div class="event-card"><b>📡 【突发抉择】</b><br>刚结束排练和 {member} 走在涩谷街头，电视台的‘突击深夜生放送’摄影车突然把镜头怼到你们脸前，主持人随机要求现场即兴表现！</div>',
        unsafe_allow_html=True,
    )
    c1 = st.button(
        "1. 当场清唱未公开自创高音段落！【收益：歌唱+25，粉丝+800 | 风险：压力+15】"
    )
    c2 = st.button(
        "2. 拉过队友疯狂搞笑模仿社长！【收益：综艺+30，羁绊+20 | 风险：信任-5】"
    )
    c3 = st.button(
        "3. 礼貌微笑推给队长：“团长请说！”【收益：信任+10，稳定不出错 | 风险：粉丝无增长】"
    )
    if c1:
      st.session_state.vocal += 25
      st.session_state.fans += 800
      st.session_state.stress += 15
      st.session_state.stage += 1
      st.rerun()
    if c2:
      st.session_state.variety += 30
      st.session_state.bond += 20
      st.session_state.trust -= 5
      st.session_state.stage += 1
      st.rerun()
    if c3:
      st.session_state.trust += 10
      st.session_state.stage += 1
      st.rerun()

  # Stage 11：游戏 - ⛏️ 铁锹盲盒挖宝
  elif curr_stage == 11:
    st.subheader("📍 Stage 11：【事务所地下仓库·铁锹盲盒挖宝】")
    st.markdown(
        '<div class="event-card"><b>⛏️ 【挖宝小游戏：铁锹敲开土块寻找盲盒】</b><br>在地下仓库打扫时发现泥土层，用铁锹敲开土块寻找绝版前辈道具！</div>',
        unsafe_allow_html=True,
    )
    render_dirt_dig_game()
    if st.button("➔ 挖宝结束，领取属性并进入下一阶段"):
      st.session_state.fans += 1200
      st.session_state.dance += 15
      st.session_state.stage += 1
      st.rerun()

  # Stage 13：突发事件 - ⚡ 八卦周刊跟拍偷拍！（选项明牌化）
  elif curr_stage == 13:
    st.subheader("📍 Stage 13：【突发危机】八卦周刊跟拍偷拍！")
    st.markdown(
        '<div class="event-card"><b>⚡ 【突发危机抉择】</b><br>八卦周刊拍到了你深夜与几位友人聚会的照片，并撰文暗示有负面嫌疑，网络舆论一时间沸沸扬扬！</div>',
        unsafe_allow_html=True,
    )
    c1 = st.button(
        "1. 连夜向社长诚恳坦白原委配合公关【收益：信任+20，危机化解 | 风险：压力+10】"
    )
    c2 = st.button(
        "2. 博客发长文宣誓“我的爱只属于舞台”硬刚【收益：粉丝+1500 | 风险：信任-15】"
    )
    c3 = st.button(
        "3. 保持冷静不发声，用下次舞台回应【收益：舞蹈+20，歌唱+20 | 风险：短期粉丝-2000】"
    )
    if c1:
      st.session_state.trust += 20
      st.session_state.stress += 10
      st.session_state.stage += 1
      st.rerun()
    if c2:
      st.session_state.fans += 1500
      st.session_state.trust -= 15
      st.session_state.stage += 1
      st.rerun()
    if c3:
      st.session_state.dance += 20
      st.session_state.vocal += 20
      st.session_state.fans = max(0, st.session_state.fans - 2000)
      st.session_state.stage += 1
      st.rerun()

  # Stage 15：游戏 - 📸 杂志封面快门抓拍
  elif curr_stage == 15:
    st.subheader("📍 Stage 15：【杂志封面拍摄】闪光灯快门抓拍 QTE")
    st.markdown(
        '<div class="event-card"><b>📸 【时尚摄影小游戏：快门抓拍挑战】</b><br>出道前夕《Myojo》杂志封面大片拍摄！看准监视器指示精准按下快门！</div>',
        unsafe_allow_html=True,
    )
    render_magazine_photo_game()
    if st.button("➔ 拍摄大获成功，进入下一阶段！"):
      st.session_state.fans += 1800
      st.session_state.variety += 25
      st.session_state.stage += 1
      st.rerun()

  # Stage 18：突发事件 - ⚡ 同伴临演前突发高烧！（选项明牌化）
  elif curr_stage == 18:
    st.subheader(f"📍 Stage 18：【突发】同伴 {member} 临演前突发高烧！")
    st.markdown(
        f'<div class="event-card"><b>⚡ 【突发危机抉择】</b><br>巡演首日开演前 1 小时，核心成员 {member} 突然高烧倒下无法登台！他的唱歌和舞蹈段落瞬间空了出来！</div>',
        unsafe_allow_html=True,
    )
    c1 = st.button(
        "1. 挺身而出，30 分钟硬记高音替他主唱！【收益：歌唱+30，粉丝+1000 | 风险：压力+20】"
    )
    c2 = st.button(
        "2. 协助队长重新调整全队走位填补空缺【收益：信任+20，舞蹈+15 | 风险：无额外粉丝】"
    )
    c3 = st.button(
        "3. 在后台照顾生病同伴并安抚情绪【收益：羁绊+30 | 风险：舞台表现分无增长】"
    )
    if c1:
      st.session_state.vocal += 30
      st.session_state.fans += 1000
      st.session_state.stress += 20
      st.session_state.stage += 1
      st.rerun()
    if c2:
      st.session_state.trust += 20
      st.session_state.dance += 15
      st.session_state.stage += 1
      st.rerun()
    if c3:
      st.session_state.bond += 30
      st.session_state.stage += 1
      st.rerun()

  # Stage 20：游戏 - ⚡ 【Wink大神】巨蛋花车电眼狙击战
  elif curr_stage == 20:
    st.subheader("📍 Stage 20：【巨蛋花车巡游】Wink大神·全场电眼狙击战")
    st.markdown(
        '<div class="event-card"><b>⚡ 【Wink大神：电眼狙击战】</b><br>花车驶过万名应援席！看准下落的粉红爱心 (💖) 点击发射 Wink 激光收集粉丝！</div>',
        unsafe_allow_html=True,
    )
    render_eyecatch_game()
    if st.button("➔ 狙击战结束，粉丝好感暴涨！"):
      st.session_state.fans += 2500
      st.session_state.variety += 25
      st.session_state.stage += 1
      st.rerun()

  # Stage 22：游戏 - ⏱️ 演唱会后台紧急换装 QTE
  elif curr_stage == 22:
    st.subheader(f"📍 Stage 22：【演唱会暗场】与 {member} 的紧急换装 QTE")
    st.markdown(
        f'<div class="event-card"><b>⏱️ 【后台紧急换装 QTE】</b><br>巨蛋演唱会暗场只有 30 秒！配合 {member} 快速完成战袍换装！</div>',
        unsafe_allow_html=True,
    )
    render_wardrobe_qte_game(member)
    if st.button("➔ 换装完毕，冲上舞台！"):
      st.session_state.fans += 1800
      st.session_state.stage += 1
      st.rerun()

  # Stage 23：游戏 - 🎮 15秒灯光闪避生存
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

  # 普通剧情章节（1, 3, 5, 7, 8, 10, 12, 14, 17, 19, 21, 24）
  elif curr_stage < 25:
    st.subheader(f"📍 Stage {curr_stage} / 25")
    s_db = {
        1: {
            "title": "🎵 Stage 1：雨后练习室的汗水",
            "desc": f"雨后的东京空气潮湿，练习室镜子蒙上雾气。{member} 擦着汗过来：“刚才转身重心偏了，要不要再试一次？”",
            "opt1": "虚心请教，对着镜子练到深夜。",
            "opt2": "递上买好的冰麦茶，和大家回宿舍聊天。",
            "opt3": "谢过前辈，早点休息保持第二天体能。",
        },
        3: {
            "title": "🃏 Stage 3：【宿舍深夜心跳】真心话卡牌",
            "desc": "深夜熄灯后，宿舍里几个人围坐在一起玩卡牌。你抽到了闪光卡：“如果在组合里选一个人作为永远的搭档？”",
            "opt1": f"指向身边的 {member}：“当然是选最懂我的你！”",
            "opt2": "大笑着传给下一个人：“秘密，这是商业机密！”",
            "opt3": "认真看向全员：“我想和大家所有人永远在一起。”",
        },
        5: {
            "title": "📖 Stage 5：《Myojo》偶像杂志个人专访",
            "desc": "杂志社来做日常专访，摄影师问你私底下和团里谁关系最好、最近最沉迷的爱好是什么。",
            "opt1": f"“最近一直在和 {member} 一起研究吉他与编曲。”",
            "opt2": "“喜欢收集奇怪的复古玩具，房间里到处都是。”",
            "opt3": "“最喜欢和大家一起吃烤肉，聊到深夜也很开心。”",
        },
        7: {
            "title": "📻 Stage 7：【外务】深夜广播节目试听连线",
            "desc": "你在前辈的广播节目里获得了 5 分钟的个人试听 Corner，需要单独面对麦克风与听众交流！",
            "opt1": "读了一封听众来信，给出温柔治愈的人生建议。",
            "opt2": "模仿了几位队友和社长说话的声音，效果爆棚。",
            "opt3": "推荐了自己私藏的音乐歌单，展示深厚审美。",
        },
        8: {
            "title": "🍖 Stage 8：深夜烤肉店的交心时刻",
            "desc": f"结束密集排练，你和大家聚在街角烤肉店。滋滋作响的肉香中，{member} 谈起了对未来的迷茫。",
            "opt1": "“我们一定要一起以这个组合的身份站上巨蛋！”",
            "opt2": "默默烤好一整盘肉分给大家：“快吃吧，大家辛苦啦。”",
            "opt3": "用调侃的语气打破沉重：“以后红了可别忘了吃烤肉情谊！”",
        },
        10: {
            "title": "🎸 Stage 10：【夏日音乐节】户外风暴摇滚舞台",
            "desc": "组合获得了户外音乐节的参演资格，台上突降大雨，气氛反而被点燃到了最高潮！",
            "opt1": "冲到舞台前沿淋雨高唱，将全场气氛带到沸点！",
            "opt2": "稳定走位与音准，确保湿滑舞台上的全队安全。",
            "opt3": "与手持吉他的队友背靠背飙音，打造名场面。",
        },
        12: {
            "title": "🎬 Stage 12：首支组合 MV 拍摄现场的即兴展示",
            "desc": "在拍摄出道前首支 MV 的个人特写镜头时，导演突然要求你进行 10 秒钟自由发挥！",
            "opt1": "结合场景做出深情凝视镜头的眼神杀。",
            "opt2": "跳出一段爆破力极强的高难 Freestyle 舞蹈。",
            "opt3": "对着镜头展现阳光治愈的纯真笑容。",
        },
        14: {
            "title": "🎭 Stage 14：帝国剧场舞台剧演练",
            "desc": "你获得了参演经典舞台剧的机会。排练时需要进行高难度的威亚特技和武打动作！",
            "opt1": "咬牙克服恐高，反复练习空中翻滚直到完美。",
            "opt2": "专注于台词念白与眼神爆发力，展现戏剧张力。",
            "opt3": "休息时主动拉着同台的伙伴互相对戏练习。",
        },
        17: {
            "title": "🎁 Stage 17：粉丝感谢祭 LIVE 近距离互动",
            "desc": "在小型剧场举办的粉丝感谢祭上，你需要安排互动环节，近距离感谢粉丝。",
            "opt1": "为每位到场粉丝唱专属应援词，极致宠粉。",
            "opt2": "准备了搞怪的抽奖互动，送出自己画的漫画。",
            "opt3": "现场表演高难度全员特技翻滚，用实力回报。",
        },
        19: {
            "title": "🏢 Stage 19：社长办公室的神秘闭门谈话",
            "desc": "深夜排练结束后，你被单独叫进了顶楼办公室。社长看着你厚厚的一叠记录，露出笑意。",
            "opt1": "目光坚定地直视社长：“我已经准备好承担更大责任！”",
            "opt2": "谦逊鞠躬：“感谢事务所一直以来的培养与照顾。”",
            "opt3": "坦诚说出自己对未来音乐风格的构想与野心。",
        },
        21: {
            "title": "🍕 Stage 21：宿舍里的深夜披萨作战",
            "desc": f"距离出道决定日只剩最后几天。{member} 偷偷订了外卖披萨送到宿舍，招呼大家放松。",
            "opt1": "大口吃披萨讲冷笑话，把沉重的气氛瞬间活跃起来。",
            "opt2": "举杯：“不管结果如何，能和大家相遇太好了。”",
            "opt3": "吃完后主动默默把客厅和厨房收拾得干干净净。",
        },
        24: {
            "title": "🌙 Stage 24：出道发布会彩排的最后通牒",
            "desc": "明天就是出道决选发布会。最后一次彩排中，导播对队形提出了严苛的修改意见。",
            "opt1": "带头留下来陪大家连夜加练 3 小时，直到零失误。",
            "opt2": "逐一帮队友调整领带和耳返，展现极强凝聚力。",
            "opt3": "闭目养神调整心态，用绝对沉稳的自信感染所有人。",
        },
    }

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
