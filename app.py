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
    "ARASHI (岚)": ["大野智", "樱井翔", "相叶雅纪", "二宫和也", "松本润"],
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
# 小游戏组件库（含打地鼠防狗仔、中等难度延长版拼图等）
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


# 优化后的 Stage 27 数字拼图：时间延长至 50 秒，难度调为中等（40步随机打乱）
def render_puzzle_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .puzzle-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); padding: 10px; width: 300px; text-align: center; }
    .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin: 8px 0; width: 210px; }
    .p-tile { background: linear-gradient(135deg, #ab47bc, #7b1fa2); border: 1.5px solid #ff80ab; color: #fff; height: 55px; font-size: 20px; font-weight: bold; border-radius: 10px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
    .p-tile:active { transform: scale(0.92); }
    .p-tile.empty { background: rgba(255,255,255,0.05); border: 1.5px dashed #4a148c; cursor: default; }
    </style></head><body>
    <div class="puzzle-box">
        <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">🚚 巨蛋盛典：抢修花车移动轨道（中等难度）</div>
        <div style="color: #fff; font-size: 11px; margin-top: 2px;">点击空格邻近方块，50秒内按顺序复原轨道（1-8）！</div>
        <div style="display: flex; justify-content: center;"><div class="grid" id="pGrid"></div></div>
        <div id="p-tip" style="color:#00e676; font-size:11px; font-weight:bold;">⏳ 剩余时间: <span id="pTime">50</span>s</div>
    </div>
    <script>
        let board = [1, 2, 3, 4, 5, 6, 7, 8, 0];
        let emptyIdx = 8, timeLeft = 50, isOver = false;
        
        // 中等难度：打乱 40 步（比原来 80 步更适中，时间延长至 50 秒）
        function shuffleBoard() {
            for(let step = 0; step < 40; step++) {
                let validMoves = [];
                let r = Math.floor(emptyIdx / 3), c = emptyIdx % 3;
                if(r > 0) validMoves.push(emptyIdx - 3);
                if(r < 2) validMoves.push(emptyIdx + 3);
                if(c > 0) validMoves.push(emptyIdx - 1);
                if(c < 2) validMoves.push(emptyIdx + 1);
                let target = validMoves[Math.floor(Math.random() * validMoves.length)];
                board[emptyIdx] = board[target];
                board[target] = 0;
                emptyIdx = target;
            }
            if(board.every((v, i) => v === [1,2,3,4,5,6,7,8,0][i])) { shuffleBoard(); }
        }
        shuffleBoard();

        const gridEl = document.getElementById('pGrid'), tipEl = document.getElementById('p-tip');

        let timer = setInterval(() => {
            if (timeLeft > 0 && !isOver) { timeLeft--; document.getElementById('pTime').innerText = timeLeft; }
            else if (!isOver) {
                isOver = true; clearInterval(timer);
                tipEl.innerHTML = "<span style='color:#ff5252;'>💧 时间耗尽，花车轨道拼凑失败！</span>";
            }
        }, 1000);

        function renderBoard() {
            gridEl.innerHTML = '';
            for(let i=0; i<9; i++) {
                let tile = document.createElement('div');
                if(board[i] === 0) { tile.className = 'p-tile empty'; }
                else { tile.className = 'p-tile'; tile.innerText = board[i]; tile.onclick = () => moveTile(i); }
                gridEl.appendChild(tile);
            }
        }

        function moveTile(idx) {
            if(isOver) return;
            let row = Math.floor(idx / 3), col = idx % 3, eRow = Math.floor(emptyIdx / 3), eCol = emptyIdx % 3;
            if (Math.abs(row - eRow) + Math.abs(col - eCol) === 1) {
                board[emptyIdx] = board[idx]; board[idx] = 0; emptyIdx = idx;
                renderBoard(); checkWin();
            }
        }

        function checkWin() {
            if(board.every((v, i) => v === [1, 2, 3, 4, 5, 6, 7, 8, 0][i])) {
                isOver = true; clearInterval(timer);
                tipEl.innerHTML = "<span style='color:#00e676;'>🎉 轨道拼接成功！花车顺利启动！</span>";
            }
        }
        renderBoard();
    </script></body></html>
    """
  components.html(html_code, height=270)


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
# 游戏主流程（拓展至 30 章）
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

  # Stage 2：打歌挑战
  elif curr_stage == 2:
    st.subheader("📍 Stage 2：【全开麦打歌·节奏考验】")
    st.markdown(
        '<div class="event-card"><b>🎹 【打歌考验】</b><br>电视台全开麦直播打歌！检验你平时的声乐与舞蹈综合实力。</div>',
        unsafe_allow_html=True,
    )
    if st.button("🎬 开始全开麦打歌表现"):
      power = st.session_state.dance + st.session_state.vocal
      if power >= 50:
        st.success(
            "🎉 **打歌大获成功！** 全开麦完美闭环，吸粉无数！\n\n✨ 奖励：粉丝 +2000，舞蹈 +25"
        )
        st.session_state.fans += 2000
        st.session_state.dance += 25
      else:
        st.error(
            "💧 **打歌挑战失败！** 气息不稳，遭到导播批评！\n\n⚠️ 惩罚：压力 +20，体力 -15，粉丝无增长"
        )
        st.session_state.stress += 20
        st.session_state.energy = max(0, st.session_state.energy - 15)
      if st.button("➔ 进入下一阶段"):
        st.session_state.stage += 1
        st.rerun()

  # Stage 6：粉丝应援声量对决
  elif curr_stage == 6:
    st.subheader(f"📍 Stage 6：【粉丝应援大作战】与 {member} 的声量对决")
    st.markdown(
        f'<div class="event-card"><b>📣 【街头应援考验】</b><br>街头突击宣传，考验你与 <b>{member}</b> 的默契与人气号召力。</div>',
        unsafe_allow_html=True,
    )
    if st.button("🎤 进行街头声量大声呐喊！"):
      if st.session_state.variety + st.session_state.bond >= 40:
        st.success(
            f"🎉 **应援大获全胜！** 现场人山人海，声量爆表！\n\n✨ 奖励：团员羁绊 +20，综艺感 +20"
        )
        st.session_state.bond += 20
        st.session_state.variety += 20
      else:
        st.error(
            "💧 **应援声量不足！** 围观群众寥寥无几，宣传效果不佳。\n\n⚠️ 惩罚：压力 +15，士气受挫"
        )
        st.session_state.stress += 15
      if st.button("➔ 进入下一阶段"):
        st.session_state.stage += 1
        st.rerun()

  # 🚨 Stage 9：突发危机
  elif curr_stage == 9:
    st.subheader("📍 Stage 9：【突发事件】深夜街头突击生放送（直播）！")
    st.markdown(
        f'<div class="event-card"><b>📡 【突发危机抉择】</b><br>刚结束排练和 {member} 走在涩谷街头，电视台摄影车突然把镜头怼到你们脸前，主持人随机要求现场即兴表现！</div>',
        unsafe_allow_html=True,
    )
    c1 = st.button(
        "1. 当场清唱自创高音段落！【🎤 歌唱+25，💖 粉丝+800 | ⚠️ 🔥 压力+20】"
    )
    c2 = st.button(
        "2. 拉过队友搞怪模仿社长！【🤡 综艺+30，💞 羁绊+20 | ⚠️ 🛡️ 信任度-15】"
    )
    c3 = st.button(
        "3. 礼貌推给队长稳妥应对！【🛡️ 信任度+15，🔥 压力-10 | ⚠️ 💖 粉丝-200】"
    )
    if c1:
      st.session_state.vocal += 25
      st.session_state.fans += 800
      st.session_state.stress += 20
      st.session_state.stage += 1
      st.rerun()
    if c2:
      st.session_state.variety += 30
      st.session_state.bond += 20
      st.session_state.trust -= 15
      st.session_state.stage += 1
      st.rerun()
    if c3:
      st.session_state.trust += 15
      st.session_state.stress = max(0, st.session_state.stress - 10)
      st.session_state.fans = max(0, st.session_state.fans - 200)
      st.session_state.stage += 1
      st.rerun()

  # Stage 10：舞台危机闪避
  elif curr_stage == 10:
    st.subheader("📍 Stage 10：【夏日风暴音乐节·舞台危机闪避】")
    st.markdown(
        '<div class="event-card"><b>🎮 【极限避险考验】</b><br>户外音乐节突降狂风暴雨，舞台灯光摇晃坠落，考验你的临场反应！</div>',
        unsafe_allow_html=True,
    )
    if st.button("⚡ 开启极限闪避判定"):
      if random.random() > 0.3:
        st.success(
            "🎉 **极限闪避成功！** 有惊无险安然度过风暴！\n\n✨ 奖励：粉丝 +2500，综艺感 +25"
        )
        st.session_state.fans += 2500
        st.session_state.variety += 25
      else:
        st.error(
            "💥 **闪避失败！** 被坠落的道具砸中狼狈摔倒！\n\n⚠️ 惩罚：压力 +25，体力大幅受损！"
        )
        st.session_state.stress += 25
        st.session_state.energy = max(0, st.session_state.energy - 25)
      if st.button("➔ 进入下一阶段"):
        st.session_state.stage += 1
        st.rerun()

  # Stage 11：仓库挖宝
  elif curr_stage == 11:
    st.subheader("📍 Stage 11：【事务所地下仓库·铁锹盲盒挖宝】")
    st.markdown(
        '<div class="event-card"><b>⛏️ 【挖宝考验】</b><br>在事务所地下仓库挥舞铲子寻找前辈留下的珍贵宝物。</div>',
        unsafe_allow_html=True,
    )
    if st.button("🔨 开始用力挖宝！"):
      loot = random.choice([
          (
              "💎 挖到金唱片与奖杯！",
              "🎉 **挖宝大成功！** 找到了绝版宝物！\n\n✨ 奖励：歌唱 +20，舞蹈 +20，粉丝 +1500",
              20,
              20,
              1500,
              0,
          ),
          (
              "🧱 只挖到了一堆普通泥土...",
              "💧 **挖宝失败！** 汗流浃背却什么都没找到。\n\n⚠️ 惩罚：白忙一场，压力 +10",
              0,
              0,
              0,
              10,
          ),
      ])
      st.info(loot[0])
      if loot[5] == 0:
        st.success(loot[1])
        st.session_state.vocal += loot[2]
        st.session_state.dance += loot[3]
        st.session_state.fans += loot[4]
      else:
        st.error(loot[1])
        st.session_state.stress += loot[5]
      if st.button("➔ 进入下一阶段"):
        st.session_state.stage += 1
        st.rerun()

  # Stage 12：游戏 - 🔨 击退狗仔队（打地鼠互动小游戏强势登场！）
  elif curr_stage == 12:
    st.subheader("📍 Stage 12：【防卫战】地下停车场狗仔队突袭！")
    st.markdown(
        '<div class="event-card"><b>🔨 【打地鼠互动小游戏：击退狗仔】</b><br>点击开始后，在 14 秒内点击敲击 <b>📷 狗仔</b>（击退 8 次以上），千万别误伤 <b>💖 粉丝</b>！</div>',
        unsafe_allow_html=True,
    )
    render_whack_mole_game()
    if st.button("➔ 公关结束，进入下一阶段"):
      st.session_state.fans += 1800
      st.session_state.trust += 15
      st.session_state.stage += 1
      st.rerun()

  # 🚨 Stage 13：突发危机
  elif curr_stage == 13:
    st.subheader("📍 Stage 13：【突发危机】八卦周刊跟拍偷拍！")
    st.markdown(
        '<div class="event-card"><b>⚡ 【突发危机抉择】</b><br>八卦周刊拍到了你深夜与友人聚会的照片并恶意解读，网络舆论一时间沸沸扬扬！</div>',
        unsafe_allow_html=True,
    )
    c1 = st.button(
        "1. 连夜向社长坦白原委配合公关【🛡️ 信任度+20 | ⚠️ 💖 粉丝-400，🔥 压力+15】"
    )
    c2 = st.button(
        "2. 博客发长文宣誓“爱只属于舞台”【💖 粉丝+1500 | ⚠️ 🛡️ 信任度-25】"
    )
    c3 = st.button(
        "3. 保持沉寂，用下次舞台实力说话【💃 舞蹈+20，🎤 歌唱+20 | ⚠️ 💖 粉丝-500】"
    )
    if c1:
      st.session_state.trust += 20
      st.session_state.fans = max(0, st.session_state.fans - 400)
      st.session_state.stress += 15
      st.session_state.stage += 1
      st.rerun()
    if c2:
      st.session_state.fans += 1500
      st.session_state.trust -= 25
      st.session_state.stage += 1
      st.rerun()
    if c3:
      st.session_state.dance += 20
      st.session_state.vocal += 20
      st.session_state.fans = max(0, st.session_state.fans - 500)
      st.session_state.stage += 1
      st.rerun()

  # Stage 15：杂志封面快门抓拍
  elif curr_stage == 15:
    st.subheader("📍 Stage 15：【杂志封面拍摄】闪光灯快门抓拍")
    st.markdown(
        '<div class="event-card"><b>📸 【时尚摄影考验】</b><br>《Myojo》杂志封面大片拍摄，检验你的镜头感与表情管理。</div>',
        unsafe_allow_html=True,
    )
    if st.button("📷 面对镜头开始瞬间抓拍"):
      if st.session_state.variety >= 40:
        st.success(
            "🎉 **封面拍摄大成功！** 眼神绝杀，大片完美诞生！\n\n✨ 奖励：粉丝 +2000，综艺感 +25"
        )
        st.session_state.fans += 2000
        st.session_state.variety += 25
      else:
        st.error(
            "💧 **拍摄失败！** 镜头感生疏，表情略显僵硬。\n\n⚠️ 惩罚：错失封面，压力 +15"
        )
        st.session_state.stress += 15
      if st.button("➔ 进入下一阶段"):
        st.session_state.stage += 1
        st.rerun()

  # 🚨 Stage 18：突发危机
  elif curr_stage == 18:
    st.subheader(f"📍 Stage 18：【突发危机】队友 {member} 临演前突发高烧！")
    st.markdown(
        f'<div class="event-card"><b>🚑 【突发危机抉择】</b><br>开演前 1 小时，核心成员 {member} 突发高烧晕倒无法登台！他的高音和舞蹈空出了大块缺口！</div>',
        unsafe_allow_html=True,
    )
    c1 = st.button(
        "1. 挺身而出，30分钟硬记高音救场！【🎤 歌唱+30，💖 粉丝+1000 | ⚠️ 🔥"
        " 压力+25】"
    )
    c2 = st.button(
        "2. 协助队长重排走位填补空缺【🛡️ 信任度+20，💃 舞蹈+15 | ⚠️ 💖 无额外粉丝】"
    )
    c3 = st.button(
        "3. 在后台照顾队友并安抚情绪【💞 羁绊+30 | ⚠️ 缺席彩排，🛡️ 信任度-10】"
    )
    if c1:
      st.session_state.vocal += 30
      st.session_state.fans += 1000
      st.session_state.stress += 25
      st.session_state.stage += 1
      st.rerun()
    if c2:
      st.session_state.trust += 20
      st.session_state.dance += 15
      st.session_state.stage += 1
      st.rerun()
    if c3:
      st.session_state.bond += 30
      st.session_state.trust -= 10
      st.session_state.stage += 1
      st.rerun()

  # Stage 20：Wink电眼狙击战
  elif curr_stage == 20:
    st.subheader("📍 Stage 20：【巨蛋花车巡游】Wink大神·全场电眼狙击")
    st.markdown(
        '<div class="event-card"><b>⚡ 【电眼狙击考验】</b><br>巨蛋花车巡游面对数万粉丝，释放你的专属 Wink 电眼！</div>',
        unsafe_allow_html=True,
    )
    if st.button("🌟 释放全场电眼 Wink"):
      if st.session_state.variety >= 50:
        st.success(
            "🎉 **电眼狙击大成功！** 全场粉丝尖叫声雷动！\n\n✨ 奖励：粉丝大涨 +3000"
        )
        st.session_state.fans += 3000
      else:
        st.error(
            "💧 **电眼释放失败！** 动作不够自信，反应慢了半拍。\n\n⚠️ 惩罚：略显尴尬，压力 +15"
        )
        st.session_state.stress += 15
      if st.button("➔ 进入下一阶段"):
        st.session_state.stage += 1
        st.rerun()

  # Stage 22：战袍接衣物
  elif curr_stage == 22:
    st.subheader(f"📍 Stage 22：【演唱会暗场】与 {member} 的战袍抢救战")
    st.markdown(
        f'<div class="event-card"><b>🧺 【后台换装考验】</b><br>暗场仅有 12 秒，必须在黑暗中争分夺秒抢救演出战袍。</div>',
        unsafe_allow_html=True,
    )
    if st.button("🏃‍♂️ 争分夺秒抢救战袍"):
      if st.session_state.dance >= 50:
        st.success(
            "🎉 **战袍抢救成功！** 完美换装闪亮登台！\n\n✨ 奖励：粉丝 +2000"
        )
        st.session_state.fans += 2000
      else:
        st.error(
            "💧 **手忙脚乱失败！** 错拿了臭袜子，差点误了登台时间！\n\n⚠️ 惩罚：惊出一身冷汗，压力 +15"
        )
        st.session_state.stress += 15
      if st.button("➔ 进入下一阶段"):
        st.session_state.stage += 1
        st.rerun()

  # Stage 24：记忆翻牌粉丝感谢祭
  elif curr_stage == 24:
    st.subheader("📍 Stage 24：【粉丝感谢祭】应援卡记忆考验")
    st.markdown(
        '<div class="event-card"><b>🃏 【记忆翻牌考验】</b><br>面对粉丝送上的心意卡片，考验你的专注力与记忆力。</div>',
        unsafe_allow_html=True,
    )
    if st.button("🧠 开启记忆翻牌挑战"):
      if random.random() > 0.2:
        st.success(
            "🎉 **记忆翻牌成功！** 完美认出每一位老粉的应援物！\n\n✨ 奖励：粉丝 +2500，团员羁绊 +20"
        )
        st.session_state.fans += 2500
        st.session_state.bond += 20
      else:
        st.error(
            "💧 **翻牌记忆失败！** 记性卡壳叫错了粉丝名字。\n\n⚠️ 惩罚：略显尴尬，压力 +15"
        )
        st.session_state.stress += 15
      if st.button("➔ 进入下一阶段"):
        st.session_state.stage += 1
        st.rerun()

  # Stage 27：花车轨道拼图抢修（中等难度 50 秒）
  elif curr_stage == 27:
    st.subheader(f"📍 Stage 27：【巨蛋盛典】抢修 {member} 的花车移动轨道")
    st.markdown(
        '<div class="event-card"><b>🚚 【机械轨道抢修】</b><br>中等难度拼图：50秒内点击空格邻近方块，按 1-8 顺序复原轨道！</div>',
        unsafe_allow_html=True,
    )
    render_puzzle_game()
    if st.button("➔ 轨道复原，前往出道前夜！"):
      st.session_state.fans += 3500
      st.session_state.stage += 1
      st.rerun()

  # 📖 日常外务与剧情章节
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
        14: {
            "title": "🎭 Stage 14：【外务】帝国剧场舞台剧试镜",
            "desc": "你获得了经典舞台剧的试镜资格，导演要求现场演练高难度威亚和武打！",
            "opt1": "咬牙克服恐高，反复练空中翻滚。",
            "opt2": "专注于台词念白与眼神爆发力。",
            "opt3": "主动拉着同台伙伴互相对戏。",
        },
        16: {
            "title": "🎤 Stage 16：前辈全国巡演后台帮工与学习",
            "desc": f"全员被派往前辈的巨蛋巡演后台帮忙递麦克风与整理服装。{member} 看着满场灯海眼含渴望。",
            "opt1": "“总有一天，这灯海会为我们而亮！”",
            "opt2": "观摩前辈走位，做满整页笔记。",
            "opt3": "主动帮劳累的工作人员分发便当。",
        },
        17: {
            "title": "🎁 Stage 17：小型剧场 Live 粉丝近距离感谢祭",
            "desc": "在小型剧场举办的感谢祭上，你需要安排互动环节，近距离回应粉丝。",
            "opt1": "唱专属应援词极致宠粉。",
            "opt2": "准备搞怪抽奖互动送漫画。",
            "opt3": "表演高难度特技翻滚。",
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
  # STAGE 30: 帝国剧场终局裁决
  # -------------------------------------------------------------------
  else:
    st.subheader("🏁 Stage 30：帝国剧场 CD 出道终局裁决")
    st.markdown(
        """
        <div class="event-card">
            <b>✨ 【命运的聚光灯】</b><br>
            帝国剧场金碧辉煌，全日本数百家媒体的闪光灯不断闪烁。历经 30 章的汗水与成长，社长坐在话筒前，即将宣读最终的 CD 出道考核结果！
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🌟 揭晓最终出道结果 🌟", use_container_width=True):
      st.markdown("---")
      total = (
          st.session_state.dance
          + st.session_state.vocal
          + st.session_state.variety
      )

      if st.session_state.fans >= 3000 and total >= 160:
        st.balloons()
        st.success(
            f"🎉 恭喜 **{st.session_state.player_name}**！你携带【{st.session_state.lucky_item}】，与 **{st.session_state.group}** 的伙伴们历经 30 章的汗水与磨砺，完美闪耀帝国剧场，正式华丽 CD 出道！"
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
          f"- 💖 粉丝数：**{st.session_state.fans:,} 人** | 💞 团员羁绊：**{st.session_state.bond}** | 🛡️ 事务所信任：**{st.session_state.trust}**"
      )

      st.write("")
      if st.button("🎮 开启全新练习生人生"):
        init_game()
        st.rerun()
