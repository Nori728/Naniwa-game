import streamlit as st
import random

# -----------------------------------------------------------------------------
# 1. 页面基本配置与样式 (粉嫩心动风)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="偶像专属心动企划", page_icon="💖", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 50%, #fce7f3 100%);
    }
    .main-header {
        font-size: 2.2rem;
        color: #e11d48;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
    }
    .sub-header {
        text-align: center;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .card-box {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 8px 16px rgba(225, 29, 72, 0.08);
        margin-bottom: 20px;
        border: 1px solid #fbcfe8;
    }
    .gacha-box {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #fde68a;
        margin-bottom: 15px;
    }
    .event-box {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #7dd3fc;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 2. 基础数据源 (7人全员数据、颜色、性格、图片)
# -----------------------------------------------------------------------------
MEMBERS = {
    "丈君": {"trait": "搞笑又可靠的大哥哥", "color": "蓝色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRxeLPXR2kAxnf8Z0uNFWIH7j_vjPcrr8Eg1qWtaTSoPKTvTMcZtXXX6Kn&s=10"},
    "大酱": {"trait": "热情太阳般的 C 位", "color": "红色", "img": "https://gingerweb.jp/wp-content/uploads/2023/06/nishihatadaigo.jpg"},
    "布丁": {"trait": "温柔体贴又元气的队长", "color": "绿色", "img": "https://img-mdpr.freetls.fastly.net/article/H0CW/nm/H0CW_-CrOagXoRlSyQPOD6_zSqLjGNjyrfLRLWlqECw.jpg?width=750"},
    "高恭": {"trait": "自恋又帅气的傲娇少年", "color": "紫色", "img": "https://img-mdpr.freetls.fastly.net/article/d4sb/nm/d4sbe7H-P8R6sUQpAshcntVT8-h0ZPcuMe3icV8aOm4.jpg?width=750"},
    "流星": {"trait": "眼睛会闪光的小恶魔", "color": "橙色", "img": "https://oggi.jp/wp-content/uploads/2023/03/DMA-DSC00151_2-2.jpg"},
    "米七": {"trait": "高挑清纯的长腿王子", "color": "粉色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvYWZ1rSHkldisNtmwbvxSYNjR8FWjj4_wdyKxw84_h0SabJN81yYpsGXL&s=10"},
    "谦杜": {"trait": "时尚又有主见的末子", "color": "黄色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRs8ILDomyP9A6WZPtgig1e6IyPPmSpxS8HSYiRImU0uSqXicpvyNrHV8A&s=10"},
}

ROLES = ["经纪人", "青梅竹马", "在日学生or打工人"]
MAX_ACT = 6  # 扩展到6幕，让游戏流程更长

# -----------------------------------------------------------------------------
# 3. 7人 × 3身份 剧情库 (已扩充至6幕)
# -----------------------------------------------------------------------------
STORIES = {
    "丈君": {
        "经纪人": {
            1: {"title": "🎬 丈君·后台初遇：大阪式的幽默开场", "choices": [
                ("配合他的梗吐槽：『别耍宝了，快把台词对完！』", "『哈哈，不愧是我的专属经纪人，这接梗速度满分！』", 20),
                ("递上一杯热茶：『辛苦啦，润润嗓子。』", "『有你在，比喝什么都甜！不过……笑话还是要继续讲的～』", 25),
                ("严肃地看手表：『距离上台还有5分钟，认真点。』", "『遵命大总管！为了不让你生气，我马上进入帅气模式！』", 15)
            ]},
            2: {"title": "🎬 丈君·深夜对谈：卸下防备的温柔", "choices": [
                ("听他讲搞笑背后的压力，拍拍他肩膀", "『哎呀，突然这么温柔我会不习惯的……不过，有你真好。』", 20),
                ("笑他刚才在台上滑稽的动作", "『喂！那叫舞台表现力！不许笑话我！』", 15),
                ("默默陪着他看夜景，递上热咖啡", "『累的时候只要转头看到你在，我就充满电了。』", 25)
            ]},
            3: {"title": "🎬 丈君·近距离对峙：大阪男人的直球", "choices": [
                ("假装板起脸：『身为艺人要稳重！』", "『对别人我稳重，对你嘛……我只想做最真实的自己。』", 25),
                ("被逗笑：『好啦，不跟你贫嘴了。』", "『别走嘛，多看看我，今天我可是特意为你练习了帅气眼神。』", 20),
                ("调侃他：『今天表现不错，给个好评。』", "『光有好评不够，得加个“一辈子专属”的长期契约才行！』", 15)
            ]},
            4: {"title": "🎬 丈君·突发通告：电视台的秘密同行", "choices": [
                ("主动帮他挡住媒体镜头", "『谢谢你……在镜头前护着我的样子，真的很帅气。』", 25),
                ("开玩笑：『大明星传绯闻了怎么办？』", "『那就顺水推舟，直接公开说你是我的人！』", 20),
                ("低声提醒他注意安全", "『放心吧，只要你在身边，我什么都不怕。』", 15)
            ]},
            5: {"title": "🎬 丈君·心意确认：大阪的浪漫星空", "choices": [
                ("靠在他肩膀上：『明天还要继续努力哦。』", "『只要想到明天能见到你，我就浑身是劲！』", 25),
                ("假装嫌弃他话多", "『嫌弃也没用，我一辈子都要缠着你！』", 20),
                ("认真注视他", "『好啦，不闹了，我认真的……谢谢你一直陪着我。』", 30)
            ]},
            6: {"title": "🎬 丈君·告白结局：笑声与眼泪交织的浪漫", "choices": [
                ("主动握住他的手：『以后的笑声，我都承包了。』", "『太赖皮了！明明这句话应该由我这个大哥哥先说出口的……』", 30),
                ("眼眶微热地笑出来", "『不许哭哦！从今以后，我的搞笑段子里全部都是关于你的爱情故事。』", 25),
                ("深情靠进他怀里", "『嗯！不管未来多远，我们都要手拉手一直笑下去。』", 35)
            ]}
        },
        "青梅竹马": {
            1: {"title": "🎬 丈君·放学路：从小打到大的欢喜冤家", "choices": [
                ("抢过他的书包：『大明星走路还敢玩手机！』", "『喂！快还给我！青梅竹马也不能在大街上损我面子啊！』", 20),
                ("买了两支冰淇淋分他一只", "『还是你最懂我！不过这支化得比你笑得还快！』", 25),
                ("像小时候一样揪他耳朵：『放学不准乱跑！』", "『痛痛痛！遵命青梅大人，小的马上乖乖跟你回家。』", 15)
            ]},
            2: {"title": "🎬 丈君·秘密基地：童年树下的真心话", "choices": [
                ("翻出以前写给彼此的幼稚信件", "『天呐快烧掉！黑历史绝对不能让你看见！』", 15),
                ("认真听他讲梦想与成名的迷茫", "『不管我以后走得多远，你永远是我第一个想分享喜悦的人。』", 25),
                ("把零食分给他吃", "『从小到大都是你在照顾我……以后换我来保护你啦。』", 20)
            ]},
            3: {"title": "🎬 丈君·近距离对视：心跳加速的瞬间", "choices": [
                ("戳戳他的脸：『什么时候才能真正成熟点？』", "『在你面前，我一辈子都只想当个可以撒娇的小男孩。』", 20),
                ("认真看进他的眼睛：『不管你变成什么样，我都一直在。』", "『……突然这么认真干嘛，搞得我心跳快得要命。』", 25),
                ("把话题岔开：『好啦，作业写完了没？』", "『怎么一到关键时刻你就催作业！不理你了（耳根通红）。』", 15)
            ]},
            4: {"title": "🎬 丈君·校园祭典：摊位前的并肩作战", "choices": [
                ("帮他揽客：『来看大帅哥炒面啦！』", "『喂！怎么把我当招牌了！不过……为了你，多卖几盘也行！』", 20),
                ("递上面巾纸擦汗", "『谢谢……每次看你笑，我就觉得累点也无所谓。』", 25),
                ("偷吃一口炒面", "『那是留给你的！不过……你吃过的好像更甜一点。』", 15)
            ]},
            5: {"title": "🎬 丈君·月下表白前夜：无法掩饰的心跳", "choices": [
                ("戳他肩膀：『想什么呢这么出神？』", "『在想怎么才能名正言顺地把你从“青梅”变成“老婆/老公”。』", 25),
                ("假装没听见", "『不准装傻！今天必须给我个明确回应！』", 20),
                ("温柔微笑", "『好啦，听你的就是了。』", 30)
            ]},
            6: {"title": "🎬 丈君·告白结局：青梅到恋人的华丽转身", "choices": [
                ("笑着用额头抵住他的额头：『以后不准再叫我大姐头了。』", "『遵命！我的恋人大人，从今天起换我来宠你。』", 30),
                ("红着脸接受他的拥抱", "『太好了……青梅竹马什么的太慢了，我早就想成为你的唯一了！』", 25),
                ("十指相扣：『走吧，去见我们的未来。』", "『嗯！手牵手，一辈子都不放开！』", 35)
            ]}
        },
        "在日学生or打工人": {
            1: {"title": "🎬 丈君·异国偶遇：电车站的关西腔问候", "choices": [
                ("用关西腔开玩笑打招呼：『元气吗大叔！』", "『哇！居然比我还地道！异国他乡听到这个太感动了！』", 20),
                ("塞给他一块家乡带的糖果", "『甜到心里去了！今天打工的疲惫瞬间一扫而空。』", 25),
                ("帮他指路：『那边车快开了，快跑！』", "『多亏有你！不然我在东京真的要变成路痴了。』", 15)
            ]},
            2: {"title": "🎬 丈君·异国互助：居酒屋的深夜畅谈", "choices": [
                ("听他抱怨异国生活的不易", "『幸好在东京能遇见你，不然我真的要撑不下去了。』", 20),
                ("抢着付账：『今天这顿我请！』", "『那怎么行！说好下次我发工资请你的，不许抢！』", 15),
                ("笑着递上热毛巾", "『每次看你笑，我就觉得异国他乡也没那么冷了。』", 25)
            ]},
            3: {"title": "🎬 丈君·异国并肩：末班车前的约定", "choices": [
                ("开玩笑：『大明星回国后可别把我忘了哦！』", "『怎么会！我恨不得把你打包带回大阪见我爸妈呢！』", 25),
                ("默默把围巾分他一半", "『好暖……不仅是围巾，连我的心都被你填满了。』", 20),
                ("假装正经：『快赶不上末班车了。』", "『误了末班车也没关系，因为我想和你多待一会儿。』", 15)
            ]},
            4: {"title": "🎬 丈君·异国打工突发：暴雨中的便利店", "choices": [
                ("分他一把伞：『一起撑吧。』", "『伞太小了……这样吧，你全拿着，我淋湿没关系，别把你弄湿了。』", 25),
                ("买关东煮暖手", "『谢谢你给的温暖，东京的雨夜突然就不冷了。』", 20),
                ("调侃他淋湿的样子像落汤鸡", "『喂！好歹给留点面子嘛！』", 15)
            ]},
            5: {"title": "🎬 丈君·回国倒计时：东京塔下的不舍", "choices": [
                ("看着夜景：『真舍不得这里。』", "『舍不得风景还是舍不得我？如果是后者，我可以立刻留下来。』", 25),
                ("拍拍他：『别开玩笑了。』", "『我认真的！没有你的地方，哪里都不是大阪。』", 20),
                ("紧紧抱住他", "『嗯，回国后我们再也不分开了。』", 30)
            ]},
            6: {"title": "🎬 丈君·告白结局：异国星空下的真情告白", "choices": [
                ("紧紧握住他的手：『不管回国后多远，我都在。』", "『嗯！回国后我们就公开，我的未来里绝对不能没有你！』", 30),
                ("笑着流泪", "『不许哭！以后在我的个人演唱会上，你必须坐在最中间的位置看我。』", 25),
                ("靠在他怀里看着东京铁塔", "『好, 一言为定, 我们要永远在一起。』", 35)
            ]}
        }
    }
}

# 补充其他角色的基础剧情兜底字典，防止报错
def get_member_story(member, role, act):
    if member in STORIES and role in STORIES[member] and act in STORIES[member][role]:
        return STORIES[member][role][act]
    return {
        "title": f"🎬 {member} × {role} · 第 {act} 幕：专属心动时刻",
        "choices": [
            ("微笑着靠近一步，认真注视他的眼睛", f"『被你这样看着……我的心跳连台词都快忘光了。』", 20),
            ("开个轻松的小玩笑活跃气氛", f"『好啊你，居然敢拿我开玩笑，看我怎么“惩罚”你～』", 15),
            ("安静地陪伴在身旁，递上一杯温水", f"『只要有你陪着，哪怕什么都不做也是最幸福的时光。』", 25)
        ]
    }

# -----------------------------------------------------------------------------
# 4. Session State 初始化
# -----------------------------------------------------------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "menu"
if "player_role" not in st.session_state:
    st.session_state.player_role = ROLES[0]
if "target_member" not in st.session_state:
    st.session_state.target_member = "丈君"
if "current_act" not in st.session_state:
    st.session_state.current_act = 1
if "total_score" not in st.session_state:
    st.session_state.total_score = 30
if "dialogue_history" not in st.session_state:
    st.session_state.dialogue_history = []
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "active_buff" not in st.session_state:
    st.session_state.active_buff = None
if "daily_gacha_result" not in st.session_state:
    st.session_state.daily_gacha_result = None
if "random_event" not in st.session_state:
    st.session_state.random_event = None

# -----------------------------------------------------------------------------
# 5. 主界面渲染
# -----------------------------------------------------------------------------
st.markdown('<p class="main-header">💖 浪花男子心动日常</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">✨ 7人全员 × 3身份 百分之百独立个性化剧情 (含随机事件与多结局系统)</p>', unsafe_allow_html=True)

# 抽卡与扭蛋区域
st.markdown(
    """
    <div class="gacha-box">
        <h3 style="margin-top:0; color:#b45309; font-size: 1.2rem;">🎲 每日运势与道具扭蛋机</h3>
        <p style="font-size: 0.9rem; color: #78350f; margin-bottom: 10px;">消耗10积分抽取恋爱道具，并在背包中手动点击使用以获得增益效果！</p>
    </div>
    """,
    unsafe_allow_html=True
)

col_g1, col_g2 = st.columns(2)
with col_g1:
    if st.button("✨ 测测今天大势心动成员", use_container_width=True):
        lucky_name, lucky_data = random.choice(list(MEMBERS.items()))
        st.session_state.daily_gacha_result = (lucky_name, lucky_data)

with col_g2:
    if st.button("🎁 抽取心动道具 (消耗10积分)", use_container_width=True):
        if st.session_state.total_score >= 10:
            st.session_state.total_score -= 10
            items_pool = [
                ("🍬 恋爱加倍糖果", "下一次选择获得双倍好感积分！"),
                ("🎧 读心耳机", "精准洞察真实心意，额外+15积分！"),
                ("📸 SSR限定拍立得", "增加全盘浪漫氛围与结局甜度！"),
                ("🥤 冰爽解暑饮料", "恢复元气，额外+10积分！")
            ]
            item_name, item_desc = random.choice(items_pool)
            st.session_state.inventory.append(item_name)
            st.success(f"成功获得道具：{item_name}（{item_desc}）！")
        else:
            st.warning("积分不足10分，快去剧情里增加好感吧！")

if st.session_state.daily_gacha_result:
    lname, ldata = st.session_state.daily_gacha_result
    st.info(f"✨ 今日运势大吉！今日最强心动电波对象是：**{lname}**（特点：{ldata['trait']}）。快去选择他开启剧情吧！")

# 背包与Buff道具栏
if st.session_state.inventory:
    st.markdown("---")
    st.write("🎒 **你的恋爱道具背包：**")
    cols_inv = st.columns(len(st.session_state.inventory))
    for idx, item in enumerate(st.session_state.inventory):
        with cols_inv[idx]:
            if st.button(f"使用 {item}", key=f"inv_{idx}"):
                st.session_state.active_buff = item
                st.session_state.inventory.pop(idx)
                st.success(f"已激活道具：{item}！")
                st.rerun()

if st.session_state.active_buff:
    st.markdown(f"> ⚡ **当前生效增益Buff：** `{st.session_state.active_buff}`")

st.markdown("---")

# -----------------------------------------------------------------------------
# 6. 游戏流程控制 (主菜单 vs 游戏进行中 vs 随机事件触发)
# -----------------------------------------------------------------------------

# 【随机事件判定逻辑】：如果在推进幕数时随机触发
if st.session_state.random_event:
    ev = st.session_state.random_event
    st.markdown(
        f"""
        <div class="event-box">
            <h3 style="margin-top:0; color:#0369a1;">⚡ 触发突发随机事件：{ev['title']}</h3>
            <p>{ev['desc']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("✨ 接受随机事件的挑战并获得奖励 (+20积分)", use_container_width=True):
        st.session_state.total_score += 20
        st.session_state.random_event = None
        st.success("随机事件圆满完成！好感度大幅上升！")
        st.rerun()

elif st.session_state.stage == "menu":
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.subheader("🛠️ 请定制你的心动企划档案")
    
    selected_member = st.selectbox("💖 选择你的心动男主角：", list(MEMBERS.keys()))
    
    # 💡 在这里加上这行代码，就能根据你选的人物实时显示他的图片！
    st.image(MEMBERS[selected_member]["img"], width=200)
    
    selected_role = st.selectbox("🎭 选择你的专属身份：", ROLES)
    
    st.markdown(f"**当前角色特色：** {MEMBERS[selected_member]['trait']}")
    
    if st.button("🚀 开始心动企划", use_container_width=True):
        st.session_state.target_member = selected_member
        st.session_state.player_role = selected_role
        st.session_state.current_act = 1
        st.session_state.total_score = 30
        st.session_state.stage = "playing"
        st.session_state.dialogue_history = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    selected_member = st.selectbox("💖 选择你的心动男主角：", list(MEMBERS.keys()))
    selected_role = st.selectbox("🎭 选择你的专属身份：", ROLES)
    
    st.markdown(f"**当前角色特色：** {MEMBERS[selected_member]['trait']}")
    
    if st.button("🚀 开始心动企划", use_container_width=True):
        st.session_state.target_member = selected_member
        st.session_state.player_role = selected_role
        st.session_state.current_act = 1
        st.session_state.total_score = 30
        st.session_state.stage = "playing"
        st.session_state.dialogue_history = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.stage == "playing":
    m = st.session_state.target_member
    r = st.session_state.player_role
    act = st.session_state.current_act
    
    # 顶部状态栏
    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.metric("📌 当前主角", m)
    col_s2.metric("🎭 玩家身份", r)
    col_s3.metric("💖 当前心动积分", st.session_state.total_score)
    
    st.progress(act / MAX_ACT, text=f"📖 剧情推进进度：第 {act} 幕 / 共 {MAX_ACT} 幕")
    st.markdown("---")
    
    current_story = get_member_story(m, r, act)
    
    st.markdown(f"### {current_story['title']}")
    st.markdown("请做出你的心动回应：")
    
    for i, (choice_text, reply_text, base_score) in enumerate(current_story["choices"]):
        if st.button(choice_text, key=f"choice_{act}_{i}", use_container_width=True):
            # 计算加成
            final_score = base_score
            if st.session_state.active_buff == "🍬 恋爱加倍糖果":
                final_score *= 2
                st.session_state.active_buff = None # 消耗Buff
            elif st.session_state.active_buff == "🎧 读心耳机":
                final_score += 15
                st.session_state.active_buff = None
            elif st.session_state.active_buff == "🥤 冰爽解暑饮料":
                final_score += 10
                st.session_state.active_buff = None
                
            st.session_state.total_score += final_score
            st.session_state.dialogue_history.append((current_story['title'], choice_text, reply_text, final_score))
            
            # 【关键修改】：在进入下一幕前，加入 40% 概率触发“随机事件”！
            if act < MAX_ACT and random.random() < 0.4:
                random_events_pool = [
                    {"title": "突发暴雨的屋檐避难", "desc": f"两人在回家路上突然遇到倾盆大雨，被迫挤在一个小小的便利店屋檐下，肩膀紧紧贴在一起……"},
                    {"title": "电台直播的连线突袭", "desc": f"工作间隙突然接到了一档电台连线直播，主持人现场要求他对你说一句真心话！"},
                    {"title": "猫咪咖啡厅的意外邂逅", "desc": f"排练间隙去咖啡厅休息，一只可爱的布偶猫突然跳进你怀里，引得他吃醋地看着你……"},
                    {"title": "便利店最后一块布丁", "desc": f"深夜去买宵夜，冰箱里只剩下最后一份他最爱的限定布丁，你们会怎么分？"}
                ]
                st.session_state.random_event = random.choice(random_events_pool)
            
            # 推进幕数
            if act < MAX_ACT:
                st.session_state.current_act += 1
            else:
                st.session_state.stage = "ending"
            st.rerun()

    # 显示对话历史回顾
    if st.session_state.dialogue_history:
        with st.expander("📜 查看本局心动回忆录"):
            for h_title, h_c, h_r, h_score in st.session_state.dialogue_history:
                st.markdown(f"**{h_title}**")
                st.markdown(f"*你的选择*：{h_c}")
                st.markdown(f"*{m}的回应*：{h_r} *(+ {h_score} 积分)*")
                st.markdown("---")

    if st.button("🔄 重新选择角色/身份", use_container_width=True):
        st.session_state.stage = "menu"
        st.rerun()

elif st.session_state.stage == "ending":
    m = st.session_state.target_member
    score = st.session_state.total_score
    
    st.markdown(f"""
    <div class="card-box" style="text-align: center;">
        <h2>🎉 恭喜达成完美心动结局！</h2>
        <p style="font-size: 1.1rem; color: #e11d48;">你与 <b>{m}</b> 的专属企划圆满落幕！</p>
        <p>最终累计心动积分：<b>{score} 分</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    if score >= 150:
        st.balloons()
        st.success("🌟 **评价：传奇心动恋人**：你们的默契天衣无缝，连空气中都冒着粉红泡泡！")
    elif score >= 100:
        st.success("💖 **评价：甜蜜热恋中**：彼此的心意已经紧紧相连，未来每一天都是情人节！")
    else:
        st.info("✨ **评价：双向奔赴的起点**：虽然还有些青涩，但你们的未来充满无限可能！")
        
    if st.button("🔄 开启新一轮心动企划", use_container_width=True):
        st.session_state.stage = "menu"
        st.session_state.current_act = 1
        st.session_state.total_score = 30
        st.session_state.dialogue_history = []
        st.rerun()
