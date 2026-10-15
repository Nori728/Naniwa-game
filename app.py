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

# 3. 页面样式配置
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
        padding: 20px;
        border-radius: 16px;
        border: 2px solid #ff2a75;
        box-shadow: 0px 8px 25px rgba(255, 42, 117, 0.35);
        margin: 12px 0;
        font-size: 15px;
        line-height: 1.7;
    }
    .cute-info {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 14px;
        padding: 16px;
        border: 2px dashed #ff2a75;
        color: #2b0c4f;
        font-weight: 700;
        font-size: 15px;
        margin-bottom: 14px;
    }
    label { color: #ffeb3b !important; font-weight: bold !important; }
    .stButton > button {
        background: linear-gradient(45deg, #ff2a75, #9c27b0) !important;
        color: white !important;
        font-size: 15px !important;
        font-weight: bold !important;
        border-radius: 14px !important;
        border: 2px solid #ff80ab !important;
        padding: 10px 20px !important;
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


def apply_game_result(success):
  if success:
    st.session_state.dance += 15
    st.session_state.vocal += 15
    st.session_state.fans += 500
    st.success("🎉 游戏挑战成功！实力分与粉丝数大幅提升！")
  else:
    st.session_state.dance = max(0, st.session_state.dance - 8)
    st.session_state.vocal = max(0, st.session_state.vocal - 8)
    st.session_state.rap = max(0, st.session_state.rap - 5)
    st.session_state.variety = max(0, st.session_state.variety - 5)
    st.session_state.stress += 15
    st.error(
        "❌ 游戏失败！系统已自动扣除全项实力分，心智受损！请继续努力争取CD出道机会！"
    )
  st.session_state.stage += 1
  time.sleep(1.5)
  st.rerun()


# -------------------------------------------------------------------
# 初次甄选考核组件
# -------------------------------------------------------------------
def render_audition_vocal_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; color: #fff; }
    .box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; padding: 12px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.96); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 12px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .vocal-btn { background: linear-gradient(135deg, #ff4081, #ab47bc); color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 20px; cursor: pointer; margin-top: 10px; }
    </style></head><body>
    <div class="box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">🎤 甄选项目：Vocal 高音考核</div>
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
                else if(!isOver) { endAudition(false); }
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
            } else { tipEl.innerHTML = "<span style='color:#ff5252;'>💧 音准飘忽！</span>"; }
        }

        function endAudition(success) {
            if(isOver) return; isOver = true; clearInterval(timer); clearInterval(animator);
            if(success) {
                tipEl.innerHTML = "<span style='color:#00e676;'>🎉 考核大成功！</span>";
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'success'}, '*'), 1000);
            } else {
                tipEl.innerHTML = "<span style='color:#ff5252;'>❌ 游戏失败！系统自动扣除实力分与心智！</span>";
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'fail'}, '*'), 1200);
            }
        }
    </script></body></html>
    """
  res = components.html(html_code, height=275, key="audition_game_component")
  if res == "success":
    st.session_state.vocal += 30
    st.session_state.passed_audition = True
    st.success("🎉 甄选大成功！正式签约成为练习生！")
    time.sleep(1)
    st.rerun()
  elif res == "fail":
    st.session_state.vocal = max(0, st.session_state.vocal - 10)
    st.session_state.dance = max(0, st.session_state.dance - 10)
    st.session_state.stress += 25
    st.session_state.passed_audition = True
    st.warning("⚠️ 甄选考核失利，全项实力分扣除 10 pt！已勉强编入预备营。")
    time.sleep(1.2)
    st.rerun()


# -------------------------------------------------------------------
# 各类日常互动小游戏组件 (使用稳定的固化 Key)
# -------------------------------------------------------------------
def render_piano_tiles_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .piano-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 14px; position: relative; overflow: hidden; width: 300px; height: 210px; }
    canvas { display: block; }
    .btn-row { display: flex; gap: 6px; margin-top: 8px; width: 300px; }
    .piano-btn { background: linear-gradient(180deg, #ab47bc, #7b1fa2); color: white; border: 2px solid #ff80ab; padding: 8px 0; font-size: 15px; font-weight: bold; border-radius: 10px; cursor: pointer; flex: 1; text-align: center; }
    .piano-btn:active { background: #ff4081; }
    .start-overlay { position: absolute; top:0; left:0; width:300px; height:210px; background: rgba(26,15,48,0.92); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 20px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    </style></head><body>
    <div class="piano-box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:10px; font-size:13px;">🎹 三轨道下落打歌特训</div>
            <button class="start-btn" onclick="startGame()">▶️ 点击开始挑战</button>
        </div>
        <canvas id="pianoCanvas" width="300" height="210"></canvas>
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
            document.getElementById('startOverlay').style.display = 'none'; isStarted = true;
            timer = setInterval(() => { if(timeLeft > 0 && !isGameOver) timeLeft--; else { isGameOver = true; clearInterval(timer); clearInterval(spawner); checkResult(); } }, 1000);
            spawner = setInterval(() => { if(!isGameOver && isStarted) tiles.push({ track: Math.floor(Math.random()*4), y: -35, h: 35, hit: false }); }, 500);
            loop();
        }
        function tapTrack(idx) {
            if(!isStarted || isGameOver) return; let ok = false;
            for(let t of tiles) { if(t.track === idx && !t.hit && t.y >= 100 && t.y <= 200) { t.hit = true; ok = true; score += 100; combo++; break; } }
            if(!ok) combo = 0;
        }
        function checkResult() {
            ctx.fillStyle = 'rgba(0,0,0,0.88)'; ctx.fillRect(0,0,300,210); 
            ctx.fillStyle = score >= 800 ? '#00e676' : '#ff5252'; ctx.font = 'bold 13px Arial';
            if(score >= 800) {
                ctx.fillText("🎉 打歌成功！得分: " + score, 40, 110);
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'success'}, '*'), 1000);
            } else {
                ctx.fillText("❌ 游戏失败，实力分扣除！", 50, 95);
                ctx.font = '11px Arial';
                ctx.fillText("请继续努力争取CD出道机会！", 55, 125);
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'fail'}, '*'), 1200);
            }
        }
        function loop() {
            ctx.clearRect(0, 0, 300, 210); ctx.strokeStyle = '#2d1b4e';
            for(let i=1; i<4; i++) { ctx.beginPath(); ctx.moveTo(i*trackWidth, 0); ctx.lineTo(i*trackWidth, 210); ctx.stroke(); }
            ctx.fillStyle = 'rgba(255, 64, 129, 0.2)'; ctx.fillRect(0, 140, 300, 50);
            for(let i=tiles.length-1; i>=0; i--) {
                let t = tiles[i];
                if(!t.hit) {
                    t.y += 4.0; ctx.fillStyle = '#211035'; ctx.fillRect(t.track*trackWidth+4, t.y, trackWidth-8, t.h);
                    ctx.strokeStyle = '#ea80fc'; ctx.strokeRect(t.track*trackWidth+4, t.y, trackWidth-8, t.h);
                    ctx.fillStyle = '#ff80ab'; ctx.font = '11px Arial'; ctx.fillText('🎵', t.track*trackWidth+26, t.y+22);
                    if(t.y > 210) { tiles.splice(i, 1); combo = 0; }
                } else { tiles.splice(i, 1); }
            }
            ctx.fillStyle = '#fff'; ctx.font = 'bold 11px Arial'; ctx.fillText("⏳ 剩余: " + timeLeft + "s", 10, 18); ctx.fillText("🔥 分数: " + score, 120, 18); ctx.fillText("⚡ Combo: " + combo, 210, 18);
            if(!isGameOver) requestAnimationFrame(loop);
        }
    </script></body></html>
    """
  res = components.html(html_code, height=275, key=f"game_piano_{curr_stage}")
  if res == "success":
    apply_game_result(True)
  elif res == "fail":
    apply_game_result(False)


def render_shout_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .shout-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; padding: 12px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.95); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 12px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .shout-click-btn { background: linear-gradient(135deg, #ff4081, #ab47bc); color: white; border: none; width: 130px; height: 60px; font-size: 16px; font-weight: bold; border-radius: 30px; cursor: pointer; margin: 12px 0; }
    </style></head><body>
    <div class="shout-box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:10px; font-size:13px;">📣 声量呐喊大作战</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始呐喊</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">📣 街头突击应援声量对决</div>
        <div style="color: #00e676; font-size: 12px; font-weight: bold; margin-top: 5px;">🔥 点击数: <span id="sCount">0</span> / 80 | ⏳ <span id="sTime">15</span>s</div>
        <button class="shout-click-btn" onclick="handleClick()">🗣️ 疯狂呐喊！</button>
        <div id="s-tip" style="color: #fff; font-size: 11px;">用尽全力把声音传达到广场每个角落！</div>
    </div>
    <script>
        let count = 0, timeLeft = 15, isStarted = false, isOver = false, timer;
        const countEl = document.getElementById('sCount'), timeEl = document.getElementById('sTime'), tipEl = document.getElementById('s-tip');

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none'; isStarted = true;
            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) { timeLeft--; timeEl.innerText = timeLeft; }
                else if(!isOver) {
                    isOver = true; clearInterval(timer);
                    if(count >= 80) {
                        tipEl.innerHTML = "<span style='color:#00e676;'>🎉 声量爆表！应援大获全胜！</span>";
                        setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'success'}, '*'), 1000);
                    } else {
                        tipEl.innerHTML = "<span style='color:#ff5252; font-size:10px;'>❌ 游戏失败，实力分扣除！请继续努力争取CD出道机会！</span>";
                        setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'fail'}, '*'), 1200);
                    }
                }
            }, 1000);
        }

        function handleClick() {
            if(!isStarted || isOver) return;
            count++; countEl.innerText = count;
        }
    </script></body></html>
    """
  res = components.html(html_code, height=255, key=f"game_shout_{curr_stage}")
  if res == "success":
    apply_game_result(True)
  elif res == "fail":
    apply_game_result(False)


def render_dodge_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .game-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 14px; position: relative; overflow: hidden; width: 300px; height: 210px; }
    canvas { display: block; }
    .btn-row { display: flex; gap: 8px; margin-top: 8px; width: 300px; }
    .dodge-btn { background: linear-gradient(135deg, #ff4081, #7b1fa2); color: white; border: 2px solid #ff80ab; padding: 8px 0; font-size: 13px; font-weight: bold; border-radius: 10px; cursor: pointer; flex: 1; text-align: center; }
    .start-overlay { position: absolute; top:0; left:0; width:300px; height:210px; background: rgba(26,15,48,0.92); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 20px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    </style></head><body>
    <div class="game-box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">⚡ 舞台灯泡避险突围</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始躲避</button>
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
            document.getElementById('startOverlay').style.display = 'none'; isStarted = true;
            timer = setInterval(() => { if(timeLeft > 0 && !isGameOver) timeLeft--; else { isGameOver = true; clearInterval(timer); clearInterval(spawner); checkResult(); } }, 1000);
            spawner = setInterval(() => { if(!isGameOver && isStarted) obstacles.push({ lane: Math.floor(Math.random()*3), y: -30 }); }, 700);
            loop();
        }

        function movePlayer(dir) {
            if(!isStarted || isGameOver) return;
            if(dir === 0) playerLane = 1; else playerLane = Math.max(0, Math.min(2, playerLane + dir));
        }

        function checkResult() {
            ctx.fillStyle = 'rgba(0,0,0,0.88)'; ctx.fillRect(0, 0, 300, 210);
            if(score >= 5) {
                ctx.fillStyle = '#00e676'; ctx.font = 'bold 15px Arial';
                ctx.fillText("🎉 闪避成功！得分: " + score, 45, 110);
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'success'}, '*'), 1000);
            } else {
                ctx.fillStyle = '#ff5252'; ctx.font = 'bold 13px Arial';
                ctx.fillText("❌ 游戏失败，实力分扣除！", 50, 95);
                ctx.font = '11px Arial';
                ctx.fillText("请继续努力争取CD出道机会！", 55, 125);
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'fail'}, '*'), 1200);
            }
        }

        function loop() {
            ctx.clearRect(0, 0, 300, 210); ctx.strokeStyle = '#2d1b4e';
            for(let i=1; i<3; i++) { ctx.beginPath(); ctx.moveTo(i*trackWidth, 0); ctx.lineTo(i*trackWidth, 210); ctx.stroke(); }
            for(let i = obstacles.length - 1; i >= 0; i--) {
                let obs = obstacles[i]; obs.y += 3.5; ctx.font = '22px Arial'; ctx.fillText('💡', obs.lane * trackWidth + 36, obs.y);
                if(obs.y >= 155 && obs.y <= 195 && obs.lane === playerLane) { score = Math.max(0, score - 1); obstacles.splice(i, 1); }
                else if(obs.y > 210) { score += 1; obstacles.splice(i, 1); }
            }
            ctx.font = '26px Arial'; ctx.fillText('🧍‍♂️', playerLane * trackWidth + 34, 185);
            ctx.fillStyle = '#fff'; ctx.font = 'bold 11px Arial'; ctx.fillText("⏳ 剩余: " + timeLeft + "s", 10, 18); ctx.fillText("🛡️ 得分: " + score, 210, 18);
            if(!isGameOver) requestAnimationFrame(loop);
        }
    </script></body></html>
    """
  res = components.html(html_code, height=270, key=f"game_dodge_{curr_stage}")
  if res == "success":
    apply_game_result(True)
  elif res == "fail":
    apply_game_result(False)


def render_dig_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .game-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; padding: 10px; width: 300px; text-align: center; }
    .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin: 8px 0; }
    .soil-tile { background: linear-gradient(135deg, #5d4037, #3e2723); border: 2px solid #8d6e63; border-radius: 8px; height: 50px; font-size: 22px; display: flex; align-items: center; justify-content: center; cursor: pointer; color: #fff; }
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
        let opened = Array(9).fill(false), foundCount = 0, digLeft = 6, isOver = false;
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
            opened[idx] = true; digLeft--;
            document.getElementById('digLeft').innerText = digLeft;
            if(items[idx] !== '🧱') {
                foundCount++; document.getElementById('digScore').innerText = foundCount;
                tipEl.innerHTML = "<span style='color:#00e676;'>🎉 挖到宝物 (" + items[idx] + ")！</span>";
                if(foundCount >= 3) { 
                    isOver = true; tipEl.innerHTML = "<span style='color:#00e676;'>🎉 3个宝物全找齐！</span>";
                    setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'success'}, '*'), 1000);
                }
            } else { tipEl.innerHTML = "<span style='color:#ff5252;'>🧱 挖到了普通泥土...</span>"; }
            if(digLeft === 0 && foundCount < 3) {
                isOver = true;
                tipEl.innerHTML = "<span style='color:#ff5252; font-size:10px;'>❌ 游戏失败，实力分扣除！请继续努力争取CD出道机会！</span>";
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'fail'}, '*'), 1200);
            }
            renderGrid();
        }
        renderGrid();
    </script></body></html>
    """
  res = components.html(html_code, height=255, key=f"game_dig_{curr_stage}")
  if res == "success":
    apply_game_result(True)
  elif res == "fail":
    apply_game_result(False)


def render_whack_mole_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .mole-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; padding: 10px; width: 300px; text-align: center; position: relative; }
    .mole-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin: 8px 0; }
    .hole { background: #211035; border: 2px solid #ab47bc; border-radius: 10px; height: 50px; font-size: 22px; display: flex; align-items: center; justify-content: center; cursor: pointer; }
    .start-overlay { position: absolute; top:0; left:0; width:300px; height:100%; background: rgba(26,15,48,0.92); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 12px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    </style></head><body>
    <div class="mole-box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:10px; font-size:13px;">🔨 击退狗仔队防卫战</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始挑战</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">🔨 击退狗仔队：打掉偷拍镜头！</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 3px;">🔥 击退狗仔: <span id="mScore">0</span> / 8 | ⏳ <span id="mTime">14</span>s</div>
        <div class="mole-grid" id="moleGrid"></div>
        <div id="m-tip" style="color: #fff; font-size: 11px;">别误伤 💖 粉丝！只点 📷 狗仔！</div>
    </div>
    <script>
        let score = 0, timeLeft = 14, isStarted = false, isOver = false, activeIdx = -1, activeType = '', timer, spawner;
        const gridEl = document.getElementById('moleGrid'), tipEl = document.getElementById('m-tip');

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none'; isStarted = true;
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
                    if(score >= 8) {
                        tipEl.innerHTML = "<span style='color:#00e676;'>🎉 成功击退所有狗仔！</span>";
                        setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'success'}, '*'), 1000);
                    } else {
                        tipEl.innerHTML = "<span style='color:#ff5252; font-size:10px;'>❌ 游戏失败，实力分扣除！请继续努力争取CD出道机会！</span>";
                        setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'fail'}, '*'), 1200);
                    }
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
                if(score >= 8) { 
                    isOver = true; clearInterval(timer); clearInterval(spawner); 
                    tipEl.innerHTML = "<span style='color:#00e676;'>🎉 成功击退所有狗仔！</span>";
                    setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'success'}, '*'), 1000);
                }
            } else { score = Math.max(0, score - 2); document.getElementById('mScore').innerText = score; activeIdx = -1; renderHoles(); }
        }
        renderHoles();
    </script></body></html>
    """
  res = components.html(html_code, height=260, key=f"game_mole_{curr_stage}")
  if res == "success":
    apply_game_result(True)
  elif res == "fail":
    apply_game_result(False)


def render_snapshot_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .game-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; padding: 10px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.95); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 12px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .snap-btn { background: linear-gradient(135deg, #ff4081, #ab47bc); color: white; border: none; padding: 10px 20px; font-size: 15px; font-weight: bold; border-radius: 20px; cursor: pointer; margin-top: 8px; }
    </style></head><body>
    <div class="game-box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">📸 杂志封面快门抓拍</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始拍摄</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">📸 快门抓拍大作战</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 3px;">✨ 成功抓拍: <span id="snapScore">0</span> / 5 | ⏳ <span id="snapTime">12</span>s</div>
        <div style="background: #211035; border: 2px solid #ab47bc; border-radius: 8px; height: 35px; margin: 10px 0; position: relative; overflow: hidden;">
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
            document.getElementById('startOverlay').style.display = 'none'; isStarted = true;
            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) { timeLeft--; timeEl.innerText = timeLeft; }
                else if(!isOver) { endSnap(false); }
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
                score++; scoreEl.innerText = score; tipEl.innerHTML = "<span style='color:#00e676;'>🎉 完美封面瞬间！</span>";
                if(score >= 5) endSnap(true);
            } else { tipEl.innerHTML = "<span style='color:#ff5252;'>💧 拍虚了！</span>"; }
        }

        function endSnap(success) {
            if(isOver) return; isOver = true; clearInterval(timer); clearInterval(animator);
            if(success) {
                tipEl.innerHTML = "<span style='color:#00e676;'>🎉 杂志大片大成功！</span>";
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'success'}, '*'), 1000);
            } else {
                tipEl.innerHTML = "<span style='color:#ff5252; font-size:10px;'>❌ 游戏失败，实力分扣除！请继续努力争取CD出道机会！</span>";
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'fail'}, '*'), 1200);
            }
        }
    </script></body></html>
    """
  res = components.html(html_code, height=265, key=f"game_snap_{curr_stage}")
  if res == "success":
    apply_game_result(True)
  elif res == "fail":
    apply_game_result(False)


def render_wink_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .game-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 14px; position: relative; overflow: hidden; width: 300px; height: 210px; }
    canvas { display: block; }
    .btn-row { display: flex; gap: 6px; margin-top: 8px; width: 300px; }
    .wink-btn { background: linear-gradient(135deg, #ff4081, #7b1fa2); color: white; border: 2px solid #ff80ab; padding: 8px 0; font-size: 13px; font-weight: bold; border-radius: 10px; cursor: pointer; flex: 1; text-align: center; }
    .start-overlay { position: absolute; top:0; left:0; width:300px; height:210px; background: rgba(26,15,48,0.92); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 20px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    </style></head><body>
    <div class="game-box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">🌟 Wink 电眼狙击（光波弹特效版）</div>
            <div style="color:#fff; font-size:10px; margin-bottom:8px; text-align:center; padding:0 10px;">射中 💖 闪烁得分 | 射到 💣 引发爆炸扣分！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始巡游</button>
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
        let playerLane = 1, targets = [], bullets = [], effects = [], score = 0, timeLeft = 12, isStarted = false, isGameOver = false, timer, spawner;

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none'; isStarted = true;
            timer = setInterval(() => {
                if(timeLeft > 0 && !isGameOver) {
                    timeLeft--;
                } else if(!isGameOver) {
                    isGameOver = true; clearInterval(timer); clearInterval(spawner); checkResult();
                }
            }, 1000);
            spawner = setInterval(() => {
                if(!isGameOver && isStarted) {
                    let type = Math.random() > 0.3 ? 'heart' : 'bomb';
                    targets.push({ lane: Math.floor(Math.random()*3), y: -25, type: type });
                }
            }, 750);
            loop();
        }

        function moveWink(dir) {
            if(!isStarted || isGameOver) return;
            playerLane = Math.max(0, Math.min(2, playerLane + dir));
        }

        function winkAction() {
            if(!isStarted || isGameOver) return;
            bullets.push({ lane: playerLane, y: 175 });
        }

        function checkResult() {
            ctx.fillStyle = 'rgba(0,0,0,0.88)'; ctx.fillRect(0, 0, 300, 210);
            if(score >= 5) {
                ctx.fillStyle = '#00e676'; ctx.font = 'bold 15px Arial';
                ctx.fillText("🎉 电眼狙击成功！得分: " + score, 40, 110);
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'success'}, '*'), 1000);
            } else {
                ctx.fillStyle = '#ff5252'; ctx.font = 'bold 13px Arial';
                ctx.fillText("❌ 游戏失败，实力分扣除！", 50, 95);
                ctx.font = '11px Arial';
                ctx.fillText("请继续努力争取CD出道机会！", 55, 125);
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'fail'}, '*'), 1200);
            }
        }

        function loop() {
            ctx.clearRect(0, 0, 300, 210); ctx.strokeStyle = '#2d1b4e';
            for(let i=1; i<3; i++) { ctx.beginPath(); ctx.moveTo(i*trackWidth, 0); ctx.lineTo(i*trackWidth, 210); ctx.stroke(); }

            for(let i = targets.length - 1; i >= 0; i--) {
                let t = targets[i];
                t.y += 2.8;
                ctx.font = '22px Arial';
                ctx.fillText(t.type === 'heart' ? '💖' : '💣', t.lane * trackWidth + 36, t.y);
                if(t.y > 210) targets.splice(i, 1);
            }

            for(let i = bullets.length - 1; i >= 0; i--) {
                let b = bullets[i];
                b.y -= 7.5;
                ctx.font = '18px Arial';
                ctx.fillText('💫', b.lane * trackWidth + 38, b.y);

                for(let j = targets.length - 1; j >= 0; j--) {
                    let t = targets[j];
                    if(t.lane === b.lane && Math.abs(t.y - b.y) < 20) {
                        if(t.type === 'heart') {
                            score += 1;
                            effects.push({ x: t.lane * trackWidth + 40, y: t.y, text: '✨闪烁+1', color: '#00e676', life: 20 });
                        } else {
                            score = Math.max(0, score - 2);
                            effects.push({ x: t.lane * trackWidth + 40, y: t.y, text: '💥爆炸-2', color: '#ff5252', life: 20 });
                        }
                        targets.splice(j, 1);
                        bullets.splice(i, 1);
                        break;
                    }
                }
                if(b && b.y < 0) bullets.splice(i, 1);
            }

            for(let i = effects.length - 1; i >= 0; i--) {
                let eff = effects[i];
                ctx.fillStyle = eff.color;
                ctx.font = 'bold 13px Arial';
                ctx.fillText(eff.text, eff.x - 15, eff.y);
                eff.y -= 1; eff.life--;
                if(eff.life <= 0) effects.splice(i, 1);
            }

            ctx.font = '26px Arial'; ctx.fillText('😉', playerLane * trackWidth + 34, 185);
            ctx.fillStyle = '#fff'; ctx.font = 'bold 11px Arial';
            ctx.fillText("⏳ 剩余: " + timeLeft + "s", 10, 18);
            ctx.fillText("💖 狙击得分: " + score, 160, 18);

            if(!isGameOver) requestAnimationFrame(loop);
        }
    </script></body></html>
    """
  res = components.html(html_code, height=270, key=f"game_wink_{curr_stage}")
  if res == "success":
    apply_game_result(True)
  elif res == "fail":
    apply_game_result(False)


def render_outfit_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; }
    .game-box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 14px; position: relative; overflow: hidden; width: 300px; height: 210px; }
    canvas { display: block; }
    .btn-row { display: flex; gap: 8px; margin-top: 8px; width: 300px; }
    .outfit-btn { background: linear-gradient(135deg, #ff4081, #7b1fa2); color: white; border: 2px solid #ff80ab; padding: 8px 0; font-size: 13px; font-weight: bold; border-radius: 10px; cursor: pointer; flex: 1; text-align: center; }
    .start-overlay { position: absolute; top:0; left:0; width:300px; height:210px; background: rgba(26,15,48,0.92); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 20px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    </style></head><body>
    <div class="game-box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">🧺 三轨道下落接战袍</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始接物</button>
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
            document.getElementById('startOverlay').style.display = 'none'; isStarted = true;
            timer = setInterval(() => {
                if(timeLeft > 0 && !isGameOver) {
                    timeLeft--;
                } else if(!isGameOver) {
                    isGameOver = true; clearInterval(timer); clearInterval(spawner); checkResult();
                }
            }, 1000);
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
            if(dir === 0) basketLane = 1; else basketLane = Math.max(0, Math.min(2, basketLane + dir));
        }

        function checkResult() {
            ctx.fillStyle = 'rgba(0,0,0,0.88)'; ctx.fillRect(0, 0, 300, 210);
            if(score >= 5) {
                ctx.fillStyle = '#00e676'; ctx.font = 'bold 15px Arial';
                ctx.fillText("🎉 接战袍成功！得分: " + score, 40, 110);
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'success'}, '*'), 1000);
            } else {
                ctx.fillStyle = '#ff5252'; ctx.font = 'bold 13px Arial';
                ctx.fillText("❌ 游戏失败，实力分扣除！", 50, 95);
                ctx.font = '11px Arial';
                ctx.fillText("请继续努力争取CD出道机会！", 55, 125);
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'fail'}, '*'), 1200);
            }
        }

        function loop() {
            ctx.clearRect(0, 0, 300, 210); ctx.strokeStyle = '#2d1b4e';
            for(let i=1; i<3; i++) { ctx.beginPath(); ctx.moveTo(i*trackWidth, 0); ctx.lineTo(i*trackWidth, 210); ctx.stroke(); }
            for(let i = items.length - 1; i >= 0; i--) {
                let it = items[i]; it.y += 3.5; ctx.font = '22px Arial'; ctx.fillText(it.type, it.lane * trackWidth + 36, it.y);
                if(it.y >= 155 && it.y <= 195 && it.lane === basketLane) {
                    if(it.type === '🧥') score += 1; else score = Math.max(0, score - 1);
                    items.splice(i, 1);
                } else if(it.y > 210) { items.splice(i, 1); }
            }
            ctx.font = '26px Arial'; ctx.fillText('🧺', basketLane * trackWidth + 34, 185);
            ctx.fillStyle = '#fff'; ctx.font = 'bold 11px Arial'; ctx.fillText("⏳ 剩余: " + timeLeft + "s", 10, 18); ctx.fillText("🧥 得分: " + score, 210, 18);
            if(!isGameOver) requestAnimationFrame(loop);
        }
    </script></body></html>
    """
  res = components.html(html_code, height=270, key=f"game_outfit_{curr_stage}")
  if res == "success":
    apply_game_result(True)
  elif res == "fail":
    apply_game_result(False)


def render_watermelon_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; color: #fff; }
    .box { background: #1a0f30; border: 2px solid #ff2a75; border-radius: 14px; padding: 10px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.96); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 14px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .top-panel { display: flex; justify-content: space-between; align-items: center; background: #211035; border: 1px solid #ab47bc; border-radius: 8px; padding: 4px 10px; margin-bottom: 6px; font-size: 11px; }
    .next-preview { font-size: 20px; background: rgba(255,255,255,0.1); border-radius: 6px; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; }
    .game-container { background: #211035; border: 2px solid #ab47bc; border-radius: 10px; height: 170px; position: relative; overflow: hidden; cursor: pointer; }
    .drop-guide { position: absolute; top: 0; width: 2px; height: 100%; background: rgba(255,235,59,0.7); border-left: 1px dashed #ffeb3b; pointer-events: none; }
    .ball { position: absolute; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; transform: translate(-50%, -50%); box-shadow: 0 3px 6px rgba(0,0,0,0.3); }
    </style></head><body>
    <div class="box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:6px; font-size:13px;">🍉 偶像萌物合成大西瓜</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px;">看准顶部黄色瞄准线，点击箱子内部垂直下落萌物！合成出西瓜蛋糕胜利！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始挑战</button>
        </div>
        <div class="top-panel">
            <div>✨ 最高: <span id="wLevel" style="color:#ffeb3b;">🍙 小饭团</span> | ⏳ <span id="wTime">40</span>s</div>
            <div style="display:flex; align-items:center; gap:5px;"><span>NEXT:</span><div class="next-preview" id="nextPreview">🍙</div></div>
        </div>
        <div class="game-container" id="gameBoard" onclick="boardClick(event)">
            <div class="drop-guide" id="guideLine" style="left: 150px;"></div>
        </div>
        <div id="w-tip" style="color: #fff; font-size: 11px; margin-top: 5px;">跟随黄线，点击投放萌物！</div>
    </div>
    <script>
        let timeLeft = 40, isStarted = false, isOver = false, timer, balls = [];
        const boardEl = document.getElementById('gameBoard'), timeEl = document.getElementById('wTime'), lvlEl = document.getElementById('wLevel'), tipEl = document.getElementById('w-tip'), guideLine = document.getElementById('guideLine'), nextPreview = document.getElementById('nextPreview');
        
        const items = [
            { name: '🍙 小饭团', size: 26, emoji: '🍙' },
            { name: '🧢 应援帽', size: 36, emoji: '🧢' },
            { name: '🎧 音乐耳机', size: 46, emoji: '🎧' },
            { name: '🎤 黄金话筒', size: 56, emoji: '🎤' },
            { name: '🏆 闪亮奖杯', size: 68, emoji: '🏆' },
            { name: '🌟 终极大西瓜蛋糕', size: 82, emoji: '🍉' }
        ];

        let nextIdx = 0, maxAchievedIdx = 0;

        function getRandomSpawnIdx() { return Math.random() < 0.7 ? 0 : 1; }

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none';
            isStarted = true; nextIdx = getRandomSpawnIdx(); updatePreview();
            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) {
                    timeLeft--; timeEl.innerText = timeLeft;
                } else if(!isOver) {
                    endGame(false);
                }
            }, 1000);
        }

        function updatePreview() { nextPreview.innerText = items[nextIdx].emoji; }

        boardEl.onmousemove = (e) => {
            let rect = boardEl.getBoundingClientRect();
            let x = Math.max(20, Math.min(280, e.clientX - rect.left));
            guideLine.style.left = x + 'px';
        };

        function boardClick(e) {
            if(!isStarted || isOver) return;
            let rect = boardEl.getBoundingClientRect();
            let clickX = Math.max(25, Math.min(275, e.clientX - rect.left));
            balls.push({ x: clickX, y: 25, level: nextIdx });
            nextIdx = getRandomSpawnIdx(); updatePreview();
            settleBalls(); renderBalls();
        }

        function settleBalls() {
            for(let i = 0; i < balls.length; i++) {
                let b = balls[i], targetY = 145;
                for(let j = 0; j < balls.length; j++) {
                    if(i === j) continue;
                    let other = balls[j];
                    if(Math.abs(b.x - other.x) < (items[b.level].size/2 + items[other.level].size/2 - 2) && other.y > b.y) {
                        let candidateY = other.y - items[other.level].size;
                        if(candidateY < targetY) targetY = candidateY;
                    }
                }
                b.y = targetY;
            }
            for(let i = 0; i < balls.length; i++) {
                for(let j = i + 1; j < balls.length; j++) {
                    let b1 = balls[i], b2 = balls[j];
                    if(Math.hypot(b1.x - b2.x, b1.y - b2.y) < (items[b1.level].size/2 + items[b2.level].size/2 + 4)) {
                        if(b1.level === b2.level && b1.level < items.length - 1) {
                            b1.level++;
                            if(b1.level > maxAchievedIdx) { maxAchievedIdx = b1.level; lvlEl.innerText = items[maxAchievedIdx].name; }
                            balls.splice(j, 1);
                            tipEl.innerHTML = "<span style='color:#00e676;'>🎉 进化为 " + items[b1.level].name + "！</span>";
                            if(b1.level >= items.length - 1) { 
                                renderBalls(); 
                                isOver = true; clearInterval(timer);
                                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'success'}, '*'), 1000);
                                return; 
                            }
                            break;
                        }
                    }
                }
            }
        }

        function renderBalls() {
            boardEl.querySelectorAll('.ball').forEach(el => el.remove());
            balls.forEach(b => {
                let info = items[b.level];
                let el = document.createElement('div');
                el.className = 'ball'; el.style.width = info.size + 'px'; el.style.height = info.size + 'px';
                el.style.left = b.x + 'px'; el.style.top = b.y + 'px';
                el.innerText = info.emoji; boardEl.appendChild(el);
            });
        }

        function endGame(success) {
            if(isOver) return; isOver = true; clearInterval(timer);
            if(success) {
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'success'}, '*'), 500);
            } else {
                tipEl.innerHTML = "<span style='color:#ff5252;'>❌ 游戏失败，实力分扣除！</span>";
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'fail'}, '*'), 1200);
            }
        }
    </script></body></html>
    """
  res = components.html(html_code, height=340, key=f"game_watermelon_{curr_stage}")
  if res == "success":
    apply_game_result(True)
  elif res == "fail":
    apply_game_result(False)


def render_2048_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; color: #fff; }
    .box { background: #1a0f30; border: 2px solid #ff2a75; border-radius: 14px; padding: 12px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.96); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 14px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .grid-2048 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; background: #211035; border: 2px solid #ab47bc; padding: 6px; border-radius: 10px; margin: 8px auto; width: 200px; height: 200px; }
    .tile-2048 { background: #31115c; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: bold; color: #fff; }
    .controls { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; width: 160px; margin: 4px auto; }
    .c-btn { background: #ab47bc; border: none; color: #fff; padding: 8px; border-radius: 6px; font-weight: bold; cursor: pointer; }
    </style></head><body>
    <div class="box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:6px; font-size:13px;">🎵 音乐 32 合成大挑战</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px;">通过方向按钮合并音符，只要合成出 <b>32</b> 即可胜利！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始挑战</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 13px;">🎵 音乐演播室·合成32</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 2px;">✨ 最高合成: <span id="maxTile">2</span> | ⏳ <span id="tTime">18</span>s</div>
        <div class="grid-2048" id="board2048"></div>
        <div class="controls">
            <div></div><button class="c-btn" onclick="slide('up')">⬆️</button><div></div>
            <button class="c-btn" onclick="slide('left')">⬅️</button><button class="c-btn" onclick="slide('down')">⬇️</button><button class="c-btn" onclick="slide('right')">➡️</button>
        </div>
        <div id="t-tip" style="color: #fff; font-size: 11px; margin-top: 4px;">点击方向按钮合并音符！</div>
    </div>
    <script>
        let timeLeft = 18, isStarted = false, isOver = false, timer, board = [[2, 0, 2], [0, 4, 0], [2, 0, 0]], maxVal = 2;
        const timeEl = document.getElementById('tTime'), maxTileEl = document.getElementById('maxTile'), tipEl = document.getElementById('t-tip'), boardEl = document.getElementById('board2048');

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none'; isStarted = true; renderBoard();
            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) {
                    timeLeft--; timeEl.innerText = timeLeft;
                } else if(!isOver) {
                    endGame(false);
                }
            }, 1000);
        }

        function renderBoard() {
            boardEl.innerHTML = '';
            for(let r=0; r<3; r++) {
                for(let c=0; c<3; c++) {
                    let val = board[r][c], div = document.createElement('div');
                    div.className = 'tile-2048'; div.innerText = val === 0 ? '' : val;
                    if(val > 0) div.style.background = `hsl(${(Math.log2(val)*55)%360}, 70%, 45%)`;
                    boardEl.appendChild(div);
                }
            }
            maxTileEl.innerText = maxVal;
        }

        function addRandom() {
            let empty = [];
            for(let r=0; r<3; r++) for(let c=0; c<3; c++) if(board[r][c] === 0) empty.push({r, c});
            if(empty.length > 0) {
                let cell = empty[Math.floor(Math.random() * empty.length)];
                board[cell.r][cell.c] = Math.random() < 0.8 ? 2 : 4;
            }
        }

        function slide(dir) {
            if(!isStarted || isOver) return;
            let moved = false;
            if(dir === 'left' || dir === 'right') {
                for(let r=0; r<3; r++) {
                    let row = board[r].filter(v => v !== 0); if(dir === 'right') row.reverse();
                    for(let i=0; i<row.length-1; i++) { if(row[i] === row[i+1]) { row[i] *= 2; row[i+1] = 0; if(row[i] > maxVal) maxVal = row[i]; } }
                    row = row.filter(v => v !== 0); while(row.length < 3) { if(dir === 'right') row.unshift(0); else row.push(0); }
                    if(dir === 'right') row.reverse(); if(JSON.stringify(board[r]) !== JSON.stringify(row)) moved = true; board[r] = row;
                }
            } else {
                for(let c=0; c<3; c++) {
                    let col = [board[0][c], board[1][c], board[2][c]].filter(v => v !== 0); if(dir === 'down') col.reverse();
                    for(let i=0; i<col.length-1; i++) { if(col[i] === col[i+1]) { col[i] *= 2; col[i+1] = 0; if(col[i] > maxVal) maxVal = col[i]; } }
                    col = col.filter(v => v !== 0); while(col.length < 3) { if(dir === 'down') col.unshift(0); else col.push(0); }
                    if(dir === 'down') col.reverse(); for(let r=0; r<3; r++) board[r][c] = col[r]; moved = true;
                }
            }
            if(moved) {
                addRandom(); renderBoard();
                tipEl.innerHTML = "<span style='color:#00e676;'>🎉 合并成功！</span>";
                if(maxVal >= 32) {
                    isOver = true; clearInterval(timer);
                    setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'success'}, '*'), 500);
                }
            }
        }

        function endGame(success) {
            if(isOver) return; isOver = true; clearInterval(timer);
            if(success) {
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'success'}, '*'), 500);
            } else {
                tipEl.innerHTML = "<span style='color:#ff5252;'>❌ 游戏失败，实力分扣除！</span>";
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'fail'}, '*'), 1200);
            }
        }
    </script></body></html>
    """
  res = components.html(html_code, height=360, key=f"game_2048_{curr_stage}")
  if res == "success":
    apply_game_result(True)
  elif res == "fail":
    apply_game_result(False)


def render_parkour_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; color: #fff; }
    .box { background: #1a0f30; border: 2px solid #ff2a75; border-radius: 14px; padding: 12px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.96); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 14px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .game-box { background: #211035; border: 2px solid #ab47bc; border-radius: 10px; height: 120px; position: relative; overflow: hidden; margin: 6px 0; }
    canvas { display: block; }
    .jump-btn { background: linear-gradient(135deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 22px; font-size: 15px; font-weight: bold; border-radius: 20px; cursor: pointer; margin-top: 4px; }
    </style></head><body>
    <div class="box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">🏃 红毯冲刺：真实滚动跑酷挑战</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px;">障碍物会从右向左滚动袭来！点击按钮 <b>⬆️ 跃起跳过障碍</b>（跳过6次胜利）！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始跑酷</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 13px;">🏃 颁奖红毯·横板滚动跑酷</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 3px;">✨ 成功跳过: <span id="pScore">0</span> / 6 | ⏳ <span id="pTime">15</span>s</div>
        <div class="game-box">
            <canvas id="parkourCanvas" width="276" height="120"></canvas>
        </div>
        <button class="jump-btn" onclick="jumpAction()">⬆️ 跃起跳过障碍！</button>
        <div id="p-tip" style="color: #fff; font-size: 11px; margin-top: 4px;">看准时机起跳避开相机与路障！</div>
    </div>
    <script>
        const canvas = document.getElementById('parkourCanvas'); const ctx = canvas.getContext('2d');
        let score = 0, timeLeft = 15, isStarted = false, isOver = false, timer, spawner;
        let player = { x: 40, y: 80, vy: 0, isJumping: false, size: 28 };
        let obstacles = [], bgX = 0;

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none'; isStarted = true;
            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) {
                    timeLeft--; document.getElementById('pTime').innerText = timeLeft;
                } else if(!isOver) {
                    endGame(false);
                }
            }, 1000);
            spawner = setInterval(() => {
                if(!isOver && isStarted) {
                    let type = Math.random() > 0.5 ? '📷' : '📦';
                    obstacles.push({ x: 300, y: 82, type: type, passed: false });
                }
            }, 1400);
            loop();
        }

        function jumpAction() {
            if(!isStarted || isOver || player.isJumping) return;
            player.isJumping = true; player.vy = -8.5;
        }

        function endGame(success) {
            if(isOver) return; isOver = true; clearInterval(timer); clearInterval(spawner);
            ctx.fillStyle = 'rgba(0,0,0,0.85)'; ctx.fillRect(0, 0, 276, 120);
            if(success) {
                ctx.fillStyle = '#00e676'; ctx.font = 'bold 15px Arial';
                ctx.fillText("🎉 红毯跑酷大胜利！", 65, 65);
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'success'}, '*'), 1000);
            } else {
                ctx.fillStyle = '#ff5252'; ctx.font = 'bold 13px Arial';
                ctx.fillText("❌ 游戏失败，实力分扣除！", 50, 50);
                ctx.font = '11px Arial';
                ctx.fillText("请继续努力争取CD出道机会！", 55, 75);
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'fail'}, '*'), 1200);
            }
        }

        function loop() {
            ctx.clearRect(0, 0, 276, 120);

            bgX -= 3; if(bgX <= -30) bgX = 0;
            ctx.strokeStyle = '#ff2a75'; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(0, 108); ctx.lineTo(276, 108); ctx.stroke();
            ctx.fillStyle = '#31115c';
            for(let i = bgX; i < 276; i += 30) {
                ctx.fillRect(i, 109, 15, 11);
            }

            if(player.isJumping) {
                player.y += player.vy; player.vy += 0.65;
                if(player.y >= 80) { player.y = 80; player.isJumping = false; player.vy = 0; }
            }
            ctx.font = '26px Arial'; ctx.fillText('🏃‍♂️', player.x, player.y + 10);

            for(let i = obstacles.length - 1; i >= 0; i--) {
                let obs = obstacles[i];
                obs.x -= 3.2;
                ctx.font = '22px Arial'; ctx.fillText(obs.type, obs.x, obs.y + 10);

                if(Math.abs(obs.x - player.x) < 22 && player.y > 65) {
                    score = Math.max(0, score - 1);
                    obstacles.splice(i, 1);
                    document.getElementById('p-tip').innerHTML = "<span style='color:#ff5252;'>💥 撞到障碍物了！</span>";
                } else if(!obs.passed && obs.x < player.x) {
                    obs.passed = true; score++;
                    document.getElementById('pScore').innerText = score;
                    document.getElementById('p-tip').innerHTML = "<span style='color:#00e676;'>🎉 完美起跳！</span>";
                    if(score >= 6) endGame(true);
                } else if(obs.x < -30) {
                    obstacles.splice(i, 1);
                }
            }

            if(!isOver) requestAnimationFrame(loop);
        }
    </script></body></html>
    """
  res = components.html(html_code, height=340, key=f"game_parkour_{curr_stage}")
  if res == "success":
    apply_game_result(True)
  elif res == "fail":
    apply_game_result(False)


def render_stage29_catch_game():
  html_code = """
    <!DOCTYPE html><html><head><style>
    body { background: transparent; margin: 0; display: flex; flex-direction: column; align-items: center; font-family: system-ui, sans-serif; color: #fff; }
    .box { background: #1a0f30; border: 2px solid #ff80ab; border-radius: 12px; padding: 10px; width: 300px; text-align: center; position: relative; }
    .start-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(26,15,48,0.95); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 12px; }
    .start-btn { background: linear-gradient(45deg, #00e676, #00b0ff); color: #000; border: none; padding: 10px 18px; font-size: 14px; font-weight: bold; border-radius: 12px; cursor: pointer; }
    .game-box { background: #211035; border: 2px solid #ab47bc; border-radius: 10px; height: 130px; position: relative; overflow: hidden; margin: 6px 0; }
    canvas { display: block; }
    .btn-row { display: flex; gap: 6px; margin-top: 4px; width: 300px; }
    .ctrl-btn { background: linear-gradient(135deg, #ff4081, #7b1fa2); color: white; border: 2px solid #ff80ab; padding: 8px 0; font-size: 13px; font-weight: bold; border-radius: 10px; cursor: pointer; flex: 1; text-align: center; }
    </style></head><body>
    <div class="box">
        <div id="startOverlay" class="start-overlay">
            <div style="color:#ffeb3b; font-weight:bold; margin-bottom:8px; font-size:13px;">🌟 出道前夜：后台音符接歌特训</div>
            <div style="color:#fff; font-size:11px; margin-bottom:10px;">控制底部的衣架篮子左右移动，接住飘落的 🎵 音乐符（接满6个胜利，避开炸弹）！</div>
            <button class="start-btn" onclick="startGame()">▶️ 开始特训</button>
        </div>
        <div style="color: #ffeb3b; font-weight: bold; font-size: 12px;">🌟 收集音符·决选特训</div>
        <div style="color: #00e676; font-size: 11px; font-weight: bold; margin-top: 2px;">✨ 收集音符: <span id="cScore">0</span> / 6 | ⏳ <span id="cTime">15</span>s</div>
        <div class="game-box">
            <canvas id="catchCanvas" width="276" height="130"></canvas>
        </div>
        <div class="btn-row">
            <button class="ctrl-btn" onclick="moveBasket(-1)">⬅️ 靠左</button>
            <button class="ctrl-btn" style="background: linear-gradient(135deg, #ab47bc, #4a148c);" onclick="moveBasket(0)">⏺️ 居中</button>
            <button class="ctrl-btn" onclick="moveBasket(1)">靠右 ➡️</button>
        </div>
        <div id="c-tip" style="color: #fff; font-size: 11px; margin-top: 4px;">移动篮子接住音符！</div>
    </div>
    <script>
        const canvas = document.getElementById('catchCanvas'); const ctx = canvas.getContext('2d'); const trackWidth = 92;
        let basketLane = 1, items = [], score = 0, timeLeft = 15, isStarted = false, isOver = false, timer, spawner;

        function startGame() {
            document.getElementById('startOverlay').style.display = 'none'; isStarted = true;
            timer = setInterval(() => {
                if(timeLeft > 0 && !isOver) {
                    timeLeft--; document.getElementById('cTime').innerText = timeLeft;
                } else if(!isOver) {
                    endGame(false);
                }
            }, 1000);
            spawner = setInterval(() => {
                if(!isOver && isStarted) {
                    let type = Math.random() > 0.3 ? '🎵' : '💣';
                    items.push({ lane: Math.floor(Math.random()*3), y: -20, type: type });
                }
            }, 850);
            loop();
        }

        function moveBasket(dir) {
            if(!isStarted || isGameOver) return;
            if(dir === 0) basketLane = 1; else basketLane = Math.max(0, Math.min(2, basketLane + dir));
        }

        function endGame(success) {
            if(isOver) return; isOver = true; clearInterval(timer); clearInterval(spawner);
            ctx.fillStyle = 'rgba(0,0,0,0.85)'; ctx.fillRect(0, 0, 276, 130);
            if(success) {
                ctx.fillStyle = '#00e676'; ctx.font = 'bold 15px Arial';
                ctx.fillText("🎉 决选特训大成功！", 65, 65);
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'success'}, '*'), 1000);
            } else {
                ctx.fillStyle = '#ff5252'; ctx.font = 'bold 13px Arial';
                ctx.fillText("❌ 游戏失败，实力分扣除！", 50, 45);
                ctx.font = '11px Arial';
                ctx.fillText("请继续努力争取CD出道机会！", 55, 75);
                setTimeout(() => window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'fail'}, '*'), 1200);
            }
        }

        function loop() {
            ctx.clearRect(0, 0, 276, 130); ctx.strokeStyle = '#2d1b4e';
            for(let i=1; i<3; i++) { ctx.beginPath(); ctx.moveTo(i*trackWidth, 0); ctx.lineTo(i*trackWidth, 130); ctx.stroke(); }

            for(let i = items.length - 1; i >= 0; i--) {
                let it = items[i]; it.y += 2.8;
                ctx.font = '22px Arial'; ctx.fillText(it.type, it.lane * trackWidth + 32, it.y);

                if(it.y >= 95 && it.y <= 125 && it.lane === basketLane) {
                    if(it.type === '🎵') {
                        score++;
                        document.getElementById('cScore').innerText = score;
                        document.getElementById('c-tip').innerHTML = "<span style='color:#00e676;'>🎉 接住音符 +1！</span>";
                        if(score >= 6) endGame(true);
                    } else {
                        score = Math.max(0, score - 1);
                        document.getElementById('c-tip').innerHTML = "<span style='color:#ff5252;'>💥 炸弹减分！</span>";
                    }
                    items.splice(i, 1);
                } else if(it.y > 130) {
                    items.splice(i, 1);
                }
            }

            ctx.font = '26px Arial'; ctx.fillText('🧺', basketLane * trackWidth + 28, 118);

            if(!isOver) requestAnimationFrame(loop);
        }
    </script></body></html>
    """
  res = components.html(html_code, height=320, key=f"game_catch_{curr_stage}")
  if res == "success":
    apply_game_result(True)
  elif res == "fail":
    apply_game_result(False)


# 主标题
st.title("💖 星途闪耀：我的练习生日常")

# -------------------------------------------------------------------
# STAGE 0: 开局封面
# -------------------------------------------------------------------
if not st.session_state.game_started:
  st.markdown(
      '<div class="cute-info">✨ 欢迎来到 STARTO 偶像养成营！请输入名字、选择组合、抽取幸运物并选择【初次甄选考核项目】！</div>',
      unsafe_allow_html=True,
  )

  name_input = st.text_input(
      "✏️ 你的练习生名字 / 昵称：", placeholder="例如：酱酱 / 小夏"
  )
  selected_group = st.selectbox(
      "🎶 选择你想并肩作战的出道组合（按年龄排序）：", list(IDOL_GROUPS.keys())
  )

  st.subheader("🎁 抽开局传奇幸运物扭蛋")
  if "temp_gacha" not in st.session_state:
    st.session_state.temp_gacha = ""

  if st.button("🎲 点击抽取开局传奇幸运物！"):
    gacha_pool = [
        "🍀 前辈送的开光御守（遇危机扣除信任度减半）",
        "👟 加厚防滑特制舞鞋（舞蹈与舞台爆发力提升）",
        "🎸 已故摇滚前辈的吉他拨片（声乐收益翻倍）",
        "🍱 前辈亲制爱心便当（大幅降低压力并回满体力）",
        "📸 绝版未公开杂志拍立得（公关与信任度拉满）",
        "📖 记满心得的旧笔记本（歌唱与综艺收益提升）",
    ]
    st.session_state.temp_gacha = random.choice(gacha_pool)

  if st.session_state.temp_gacha:
    st.success(f"✨ 你抽中了：**{st.session_state.temp_gacha}**")

  st.markdown("---")
  st.subheader("🌟 选择你的初次甄选表演项目")
  audition_selection = st.radio(
      "请选择你在甄选大舞台上展示的绝活：",
      [
          "1. 🎤 Vocal 歌唱爆发力展示",
          "2. 💃 舞台 Dance 节奏卡点展示",
          "3. 🔥 Rap 节奏色彩匹配展示",
          "4. 🤹 松饼杂耍平衡特技展示",
      ],
  )

  if st.button("🚀 进入甄选考核舞台！", use_container_width=True):
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
      f'<div class="event-card"><b>🎯 甄选考核进行中：</b><br>完成下方的小游戏考核，倒计时结束系统将自动判定！</div>',
      unsafe_allow_html=True,
  )

  render_audition_vocal_game()

# -------------------------------------------------------------------
# STAGE 1 - 30 关卡严格精准匹配
# -------------------------------------------------------------------
else:
  curr_stage = st.session_state.stage
  member = get_rand_member()

  if st.session_state.stress >= 70:
    st.warning(
        f"⚠️ **【压力预警】** 压力值达 **{st.session_state.stress}%**！{member} 塞给你一罐热可可：“别把自己逼太紧。”"
    )
    st.session_state.stress = 30
    st.session_state.bond += 10

  st.subheader(f"📍 Stage {curr_stage} / 30")

  # --- 9大一般游戏关卡：2, 7, 9, 13, 15, 18, 21, 24, 29 ---
  if curr_stage == 2:
    st.markdown(
        f'<div class="event-card"><b>🎹 Stage 2：三轨道下落打歌特训</b><br>{member} 擦着汗过来：“先打一套下落节奏卡卡点！”</div>',
        unsafe_allow_html=True,
    )
    render_piano_tiles_game()
  elif curr_stage == 7:
    st.markdown(
        f'<div class="event-card"><b>📣 Stage 7：街头突击应援声量对决</b><br>事务所安排街头宣传，卖力大喊吸引路人注意！</div>',
        unsafe_allow_html=True,
    )
    render_shout_game()
  elif curr_stage == 9:
    st.markdown(
        f'<div class="event-card"><b>⚡ Stage 9：舞台灯泡故障避险突围</b><br>彩排时上方灯泡突然碎裂落下，灵活移动躲避故障灯泡！</div>',
        unsafe_allow_html=True,
    )
    render_dodge_game()
  elif curr_stage == 13:
    st.markdown(
        f'<div class="event-card"><b>⛏️ Stage 13：地下仓库9宫格寻宝</b><br>在事务所地下仓库的土块与盲盒里寻找前辈留下的珍贵道具！</div>',
        unsafe_allow_html=True,
    )
    render_dig_game()
  elif curr_stage == 15:
    st.markdown(
        f'<div class="event-card"><b>🔨 Stage 15：地下停车场击退狗仔队</b><br>走出地下停车场遭遇狗仔围堵，迅速打掉镜头保护隐私！</div>',
        unsafe_allow_html=True,
    )
    render_whack_mole_game()
  elif curr_stage == 18:
    st.markdown(
        f'<div class="event-card"><b>📸 Stage 18：杂志封面快门抓拍</b><br>时尚杂志封面拍摄，在光标移到完美区瞬间按下快门！</div>',
        unsafe_allow_html=True,
    )
    render_snapshot_game()
  elif curr_stage == 21:
    st.markdown(
        f'<div class="event-card"><b>🌟 Stage 21：巡演现场 Wink 电眼狙击（光波弹特效版）</b><br>移动花车巡游，发射爱心光波弹狙击粉丝，注意避开炸弹！</div>',
        unsafe_allow_html=True,
    )
    render_wink_game()
  elif curr_stage == 24:
    st.markdown(
        f'<div class="event-card"><b>🧺 Stage 24：后台三轨道下落接战袍</b><br>后台快速换装危机！用篮子接住战袍，避开脏袜子！</div>',
        unsafe_allow_html=True,
    )
    render_outfit_game()
  elif curr_stage == 29:
    st.markdown(
        f'<div class="event-card"><b>🌟 Stage 29：决选前夜·后台音符接歌特训</b><br>决选前夕在后台收集飘落的音乐音符，为终极舞台做准备！</div>',
        unsafe_allow_html=True,
    )
    render_stage29_catch_game()

  # --- 3大特殊外务大作：5, 11, 27 ---
  elif curr_stage == 5:
    st.markdown(
        f'<div class="event-card"><b>🍉 Stage 5：【顶奢外务】偶像萌物合成大西瓜挑战 (40秒版)</b><br>国民级黄金档综艺通告，跟随瞄准线垂直投放，合成出 <b>🌟 终极大西瓜蛋糕</b> 自动通关！</div>',
        unsafe_allow_html=True,
    )
    render_watermelon_game()
  elif curr_stage == 11:
    st.markdown(
        f'<div class="event-card"><b>🎵 Stage 11：【跨年音乐祭】音乐 32 合成大挑战</b><br>跨年直播前完成音乐合成考核，合成出 <b>32</b> 即可判定胜利！</div>',
        unsafe_allow_html=True,
    )
    render_2048_game()
  elif curr_stage == 27:
    st.markdown(
        f'<div class="event-card"><b>🏃 Stage 27：【金唱片大赏】红毯滚动跑酷挑战</b><br>红毯现场真实滚动跑酷！跳过 6 个迎面而来的障碍物即可突围成功！</div>',
        unsafe_allow_html=True,
    )
    render_parkour_game()

  # --- 自主特训日 (Stage 4, 16, 26) ---
  elif curr_stage in [4, 16, 26]:
    st.info(
        f"💡 **自主安排日** | 🎒 当前幸运物：【{st.session_state.lucky_item}】 | 🔥 压力值: {st.session_state.stress}%"
    )
    col1, col2 = st.columns(2)
    with col1:
      if st.button("💃 在舞蹈房死磕高难度步法"):
        st.session_state.dance += 20
        st.session_state.stress += 10
        st.session_state.stage += 1
        st.rerun()
      if st.button("🎤 到声乐室练习高音发声"):
        st.session_state.vocal += 20
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

  # --- 剧情抉择关卡 ---
  elif curr_stage < 30:
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
        6: {
            "title": "📻 Stage 6：【外务】深夜广播电台解忧连线",
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
        10: {
            "title": "⚡ Stage 10：夏日风暴音乐节舞台危机",
            "desc": "户外音乐节突遇强风与舞台故障，现场音响与灯光频频出错！",
            "opt1": "凭借清唱和强劲节奏完美控场。",
            "opt2": "临危不乱协助队友调整走位。",
            "opt3": "带头带动全场观众拍手合唱。",
        },
        12: {
            "title": "📍 Stage 12：【黑暗面波折】资源遭恶意顶替与排挤！",
            "desc": "你原本内定的杂志核心单人页和电视节目通告，在临录制前夕被高层关系户空降顶替。队友私下提醒你这只是圈子残酷冰山的一角……",
            "opt1": "咽下委屈，在深夜无人的练习室疯狂加练宣泄不甘",
            "opt2": "找高层据理力争，用实力和人气争取公开公平竞争",
            "opt3": "心态崩盘陷入自我怀疑，想要逃避训练",
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
            "opt1": "发布直面质疑的个人直拍和实力反击舞台，用作品说话",
            "opt2": "配合事务所冷处理，不给黑粉眼神和流量",
            "opt3": "情绪崩溃与黑粉在网络上互撕",
        },
        19: {
            "title": "🏢 Stage 19：社长办公室的顶楼闭门谈话",
            "desc": "深夜排练结束后，你被单独叫进了顶楼办公室。社长看着你厚厚的一叠记录，露出笑意。",
            "opt1": "目光坚定：“我已经准备好承担更大责任！”",
            "opt2": "谦逊鞠躬感谢事务所培养。",
            "opt3": "坦诚说出对未来音乐风格的野心。",
        },
        20: {
            "title": f"📍 Stage 20：【突发危机】队友 {member} 临演前突发高烧！",
            "desc": f"开演前 1 小时，核心成员 {member} 突发高烧晕倒无法登台！他的高音和舞蹈空出了大块缺口！",
            "opt1": "挺身而出，30分钟硬记高音救场",
            "opt2": "协助队长重排走位填补空缺",
            "opt3": "在后台照顾队友并安抚情绪",
        },
        22: {
            "title": "🍕 Stage 22：宿舍里的深夜披萨作战",
            "desc": f"距离出道决定日只剩最后几天。{member} 偷偷订了外卖披萨送到宿舍，招呼大家放松。",
            "opt1": "讲冷笑话活跃气氛。",
            "opt2": "举杯：“能和大家相遇太好了！”",
            "opt3": "吃完主动把厨房收拾得干干净净。",
        },
        23: {
            "title": "🎬 Stage 23：黄金档专属冠名番宣录制",
            "desc": "你们迎来了属于自己组合的第一档黄金档冠名番宣节目，全员精神抖擞！",
            "opt1": "主动抛梗承担节目搞笑担当。",
            "opt2": "认真配合每一个游戏环节。",
            "opt3": "照顾镜头较少的队友增加曝光。",
        },
        25: {
            "title": "🎤 Stage 25：全国巡演千秋乐（终官场）幕后感动",
            "desc": f"全国巡演最后一场幕后，全员围在圆阵里，{member} 眼含泪光伸向下臂。",
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
    }

    story = s_db.get(
        curr_stage,
        {
            "title": f"📍 Stage {curr_stage}：训练与蜕变",
            "desc": f"今天在练习室里，{member} 正在和你讨论接下来的舞台细节！",
            "opt1": "加练舞蹈细节。",
            "opt2": "雕琢歌词感情。",
            "opt3": "互动增加默契。",
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

    if curr_stage in [12, 17, 20]:
      if c1:
        if curr_stage == 12:
          st.session_state.dance += 25
          st.session_state.stress += 20
        elif curr_stage == 17:
          st.session_state.fans += 2000
          st.session_state.vocal += 25
        elif curr_stage == 20:
          st.session_state.vocal += 30
          st.session_state.fans += 1000
          st.session_state.stress += 25
        st.session_state.stage += 1
        st.rerun()
      if c2:
        if curr_stage == 12:
          st.session_state.trust += 20
          st.session_state.fans += 1000
        elif curr_stage == 17:
          st.session_state.trust += 15
          st.session_state.stress += 10
        elif curr_stage == 20:
          st.session_state.trust += 20
          st.session_state.dance += 15
        st.session_state.stage += 1
        st.rerun()
      if c3:
        if curr_stage == 12:
          st.session_state.trust -= 20
          st.session_state.stress += 30
        elif curr_stage == 17:
          st.session_state.trust -= 30
          st.session_state.stress += 40
        elif curr_stage == 20:
          st.session_state.bond += 30
          st.session_state.trust -= 10
        st.session_state.stage += 1
        st.rerun()
    else:
      if c1:
        st.session_state.dance += 15
        st.session_state.fans += 300
        st.session_state.stage += 1
        st.rerun()
      if c2:
        st.session_state.vocal += 15
        st.session_state.fans += 350
        st.session_state.stage += 1
        st.rerun()
      if c3:
        st.session_state.variety += 15
        st.session_state.bond += 10
        st.session_state.stage += 1
        st.rerun()

  # -------------------------------------------------------------------
  # STAGE 30: 帝国剧场 CD 出道终局裁决
  # -------------------------------------------------------------------
  elif curr_stage >= 30:
    st.subheader("🏁 Stage 30：帝国剧场 CD 出道终局裁决")
    st.markdown(
        """
        <div class="event-card">
            <b>✨ 【命运的聚光灯】</b><br>
            帝国剧场金碧辉煌，全日本数百家媒体的闪光灯不断闪烁。历经 30 章的汗水、游戏挑战与黑暗面波折，社长坐在话筒前，即将宣读最终的 CD 出道结果！
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

      if max_attr == st.session_state.vocal and st.session_state.vocal >= 140:
        title_desc = "🎤 **【恭喜作为大主唱出道！】** 天籁高音征服全场，成为灵魂主唱！"
      elif max_attr == st.session_state.dance and st.session_state.dance >= 140:
        title_desc = "💃 **【恭喜作为大主舞出道！】** 肢体爆发力惊艳四座，首席舞台担当！"
      elif (
          max_attr == st.session_state.variety
          and st.session_state.variety >= 140
      ):
        title_desc = "🤡 **【恭喜作为全能 ACE/综艺位出道！】** 幽默控场满分，全能担当！"
      else:
        title_desc = "🌟 **【全能实力派出道】** 各项均衡发展的多面手！"

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
              " 的伙伴们全员闪耀帝国剧场，正式 CD 出道！"
          )
        else:
          st.warning(
              f"🎤 **【意难平结局：孤高 Solo 出道】**\n\n{title_desc}\n\n"
              f"由于团员羁绊（{st.session_state.bond} pt）过低，社长拍板：改由你个人 Solo"
              " 出道！"
          )
      elif st.session_state.trust < 40:
        st.error(
            f"🛡️ **【信任危机结局：无限期雪藏】**\n\n事务所信任度过低（{st.session_state.trust}"
            " pt），高层取消了你的出道企划……"
        )
      else:
        st.warning(
            f"⚠️ **{st.session_state.player_name}**"
            " 粉丝数或实力尚差火候（粉丝需 $\ge 3000$，能力总和需 $\ge$ "
            "180$），继续加油深耕！"
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
