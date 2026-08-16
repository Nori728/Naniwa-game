import streamlit as st
import random

# -----------------------------------------------------------------------------
# 1. 页面基本配置与样式
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
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 2. 基础数据源 (7人全员数据)
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
MAX_ACT = 4

# -----------------------------------------------------------------------------
# 3. 独立且富有个性差异的剧情库 (按 身份 -> 幕数 定制)
# -----------------------------------------------------------------------------
STORIES = {
    "经纪人": {
        1: {
            "title": "🎬 第一幕：后台初遇与行程对焦",
            "choices": [
                ("严格合上行程本：『今天通告很满，打起精神来！』", "『好啦好啦，有你在身边的行程，再累我也甘之如饴～』", 20),
                ("悄悄递上一罐冰可乐：『辛苦啦，先放松一下。』", "『哇！不愧是我的专属经纪人，总是这么懂我！』", 25),
                ("顺手帮他整理了一下凌乱的衣领", "『……别突然靠这么近啊，我的心跳都要被你弄乱了。』", 15)
            ]
        },
        2: {
            "title": "🎬 第二幕：深夜休息室的私密对谈",
            "choices": [
                ("坐在旁边听他倾诉练习生时期的趣事", "『那时候多亏有你陪着，现在想起来心里还是暖洋洋的。』", 20),
                ("调侃他刚才舞台上破音的小失误", "『喂！这种黑历史不许拿出来说！看我怎么“报复”你～』", 15),
                ("默默把外套披在疲惫睡去的他身上", "『（迷迷糊糊睁开眼抓住你的手）别走……再陪我一会儿。』", 25)
            ]
        },
        3: {
            "title": "🎬 第三幕：闪光灯外的单独对峙",
            "choices": [
                ("直视他的眼睛：『身为艺人，不许把情绪写在脸上面对粉丝。』", "『对粉丝我可是100%完美哦，但对你……我没办法伪装。』", 25),
                ("无奈地叹口气，捏捏他的脸颊：『拿你没办法。』", "『哼，只准对你一个人这样撒娇，别人可没有这待遇！』", 20),
                ("假装公事公办：『那今晚的加训惩罚取消不了哦。』", "『如果是你的惩罚……那我可得好好“争取”一下福利了。』", 15)
            ]
        },
        4: {
            "title": "🎬 第四幕：演唱会落幕后的专属契约",
            "choices": [
                ("主动伸出手十指相扣：『接下来的路，我也要一直守护你。』", "『说好了哦！从今以后，你不仅是我的经纪人，更是我的唯一。』", 30),
                ("红着眼眶笑着递上杀青花束", "『不许哭！以后有我在的舞台，永远只为你一个人绽放。』", 25),
                ("直接拉过他的手贴在自己心口", "『听到了吗？为了你，这里一直在疯狂地为你一个人跳动。』", 35)
            ]
        }
    },
    "青梅竹马": {
        1: {
            "title": "🎬 第一幕：放学路上的旧地重游",
            "choices": [
                ("敲一下他的脑袋：『大明星，别忘了是谁帮你带的便当！』", "『痛！好啦好啦，从小到大就数你最爱欺负我～』", 20),
                ("顺势抢过他的耳机分戴一只：『听什么呢这么入迷？』", "『听你最喜欢的歌啊……其实，我更喜欢听你说话的声音。』", 25),
                ("默默跟在他身后，像小时候一样扯住他的衣角", "『真是的，怎么长这么大了还跟个小孩子一样依赖我。』", 15)
            ]
        },
        2: {
            "title": "🎬 第二幕：秘密基地的童年回忆杀",
            "choices": [
                ("翻出尘封的相册，毫不留情地嘲笑他小时候的糗照", "『喂！快住手！那张照片绝对不能流传出去！』", 15),
                ("递上一块亲手做的甜点：『尝尝看跟小时候味道一样吗？』", "『嗯！不管过多久，还是你做的味道最能治愈我。』", 25),
                ("盘腿坐在他身旁，听他倾诉出道后的烦恼", "『只有在你面前，我才可以卸下所有防备，做回原来的自己。』", 20)
            ]
        },
        3: {
            "title": "🎬 第三幕：突如其来的心跳距离",
            "choices": [
                ("伸手帮他拂去发梢落下的樱花瓣", "『……干嘛突然离这么近，弄得我怪不好意思的。』", 25),
                ("开玩笑似地撞了他一下：『现在当了大明星，就把我忘啦？』", "『笨蛋，不管走到哪，你永远是我心底最重要的人。』", 20),
                ("假装严肃：『身为青梅，我有义务监督你的身材管理！』", "『好好好，全听你的大管家！今晚想吃什么我都陪你。』", 15)
            ]
        },
        4: {
            "title": "🎬 第四幕：从青梅竹马到心动恋人",
            "choices": [
                ("笑着用额头抵住他的额头：『以后的路，我们一起走。』", "『嗯！从青梅到白头，这次换我来好好照顾你。』", 30),
                ("眼眶微热：『看着你闪闪发光，我真的好骄傲。』", "『傻瓜，你眼里的光，才是我前进的最大动力。』", 25),
                ("傲娇地扭过头：『勉为其难答应做你女朋友/男朋友啦！』", "『求之不得！这可是我从小到大唯一想要的愿望。』", 35)
            ]
        }
    },
    "在日学生or打工人": {
        1: {
            "title": "🎬 第一幕：异国他乡的电车站偶遇",
            "choices": [
                ("用熟练的日式温柔语气微笑道：『加油哦！今天也要元气满满！』", "『听到你的声音，今天的疲惫瞬间就烟消云散了！』", 20),
                ("递上一份便利店买的中文零食和热咖啡", "『哇！在这个异国他乡能吃到这个，简直是最大的救赎！』", 25),
                ("有些局促地用日语小声问：『那个……请问有什么需要我帮忙的吗？』", "『哈哈，你的中文发音听起来比日语还要可爱呢！』", 15)
            ]
        },
        2: {
            "title": "🎬 第二幕：异国文化交流与深夜倾心",
            "choices": [
                ("分享家乡美食，聊起异国趣事", "『真好啊，听你讲这些，我都忍不住想跟着你回去了。』", 20),
                ("聊起打工的辛苦：『虽然有点累，但很充实。』", "『P语不通，真想回国了……不过有你陪着，就没那么苦啦。』", 15),
                ("笑着鼓励他：『日语有进步哦，真不愧是我的大明星！』", "『那是当然！为了能听懂你的夸奖，我可是偷偷下了苦功的。』", 25)
            ]
        },
        3: {
            "title": "🎬 第三幕：深夜电车台的末班车并排等候",
            "choices": [
                ("笑眯眯地开玩笑：『P今天工作很充实，电车票我包啦！』", "『P工辛苦啦！等会儿工作结束我请你吃好吃的充电宝！』", 20),
                ("关切地看着他因练习而磨破的手指", "『（默默戴上口罩不说话，但眼神里满是心疼）』", 25),
                ("故意逗他：『大明星在异国也要注意表情管理哦！』", "『面对你的时候，根本没办法维持什么表情管理啦……』", 15)
            ]
        },
        4: {
            "title": "🎬 第四幕：浪漫的终极告白契约",
            "choices": [
                ("在灯光暗下的角落里，紧紧握住对方的手", "『不管易在人群中找到了你……这一次我再也不想松开你的手了！』", 30),
                ("笑着点头：『无论别人怎么看，你才是我最重要的选择！』", "『嗯！从今以后，我的世界里全都是你的倒影。』", 25),
                ("眼眶湿润：『谢谢你在异国给我的所有温柔。』", "『该说谢谢的是我，因为你，异乡才变成了真正的家。』", 35)
            ]
        }
    }
}

# -----------------------------------------------------------------------------
# 4. Session State 初始化
# -----------------------------------------------------------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "menu"  # menu, story, result
if "player_role" not in st.session_state:
    st.session_state.player_role = ROLES[0]
if "target_member" not in st.session_state:
    st.session_state.target_member = "大酱"
if "current_act" not in st.session_state:
    st.session_state.current_act = 1
if "total_score" not in st.session_state:
    st.session_state.total_score = 30
if "dialogue_history" not in st.session_state:
    st.session_state.dialogue_history = []
if "inventory" not in st.session_state:
    st.session_state.inventory = []  # 存储道具名称列表
if "active_buff" not in st.session_state:
    st.session_state.active_buff = None  # 当前生效的道具效果
if "daily_gacha_result" not in st.session_state:
    st.session_state.daily_gacha_result = None

# -----------------------------------------------------------------------------
# 5. 页面核心渲染
# -----------------------------------------------------------------------------
st.markdown('<p class="main-header">💖 浪花男子心动日常</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">✨ 多身份定制剧情 ＋ 自主道具背包 ＋ 沉浸互动 (共 {MAX_ACT} 幕)</p>', unsafe_allow_html=True)

# 抽卡与扭蛋区域
st.markdown(
    """
    <div class="gacha-box">
        <h3 style="margin-top:0; color:#b45309; font-size: 1.2rem;">🎲 每日运势与道具扭蛋机</h3>
        <p style="font-size: 0.9rem; color: #78350f; margin-bottom: 10px;">测测今天的心动成员，消耗10积分抽取恋爱道具，并在背包中手动点击使用！</p>
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
                ("🎧 读心耳机", "能精准洞察他内心的真实羞涩台词。"),
                ("📸 SSR限定拍立得", "增加全盘浪漫氛围与结局甜度。"),
                ("🥤 冰爽解暑饮料", "恢复元气，解锁隐藏温柔互动。")
            ]
            item_name, item_desc = random.choice(items_pool)
            st.session_state.inventory.append(item_name)
            st.success(f"成功获得：{item_name}！(已存入下方背包)")
        else:
            st.warning("心动积分不足 10 分，快去下方剧情里累积吧！")

if st.session_state.daily_gacha_result:
    lname, ldata = st.session_state.daily_gacha_result
    st.markdown(
        f"""
        <div class="card-box" style="text-align: center;">
            <p style="color: #e11d48; font-weight: bold; font-size: 1.1rem;">🌟 今日运势爆棚中：{lname} ({ldata['trait']})</p>
            <img src="{ldata['img']}" width="100%" style="border-radius: 12px; max-height: 250px; object-fit: cover; margin-top: 5px;">
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------------------------------------------------------
# 🎒 可交互的自主道具背包区域
# -----------------------------------------------------------------------------
if st.session_state.inventory:
    st.markdown("### 🎒 我的道具背包（点击按钮手动使用）")
    
    if st.session_state.active_buff:
        st.info(f"✨ **当前生效中的道具Buff**：`{st.session_state.active_buff}` —— 将在你的下一次选择中触发！")
    
    for i, item in enumerate(list(st.session_state.inventory)):
        col_item1, col_item2 = st.columns([3, 1])
        with col_item1:
            st.markdown(f"**{item}**")
        with col_item2:
            if st.button(f"✨ 使用", key=f"use_item_{i}_{item}"):
                st.session_state.active_buff = item
                st.session_state.inventory.remove(item)
                st.success(f"已成功使用【{item}】！请在下方剧情中做出回应吧。")
                st.rerun()
    st.markdown("---")

# -----------------------------------------------------------------------------
# 菜单阶段：选择身份与攻略对象
# -----------------------------------------------------------------------------
if st.session_state.stage == "menu":
    st.subheader("📖 开启心动互动剧情")
    
    selected_role = st.selectbox("1️⃣ 请选择你的身份：", ROLES)
    selected_member = st.selectbox("2️⃣ 请选择你想攻略的成员：", list(MEMBERS.keys()))
    
    m_info = MEMBERS[selected_member]
    st.markdown(
        f"""
        <div class="card-box" style="text-align: center;">
            <img src="{m_info['img']}" width="100%" style="border-radius: 12px; max-height: 280px; object-fit: cover;">
            <p style="margin-top: 10px; font-weight: bold; font-size: 1.1rem; color: #e11d48;">✨ {selected_member} (特征：{m_info['trait']} | 专属色：{m_info['color']})</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if st.button("✨ 确认并进入多幕专属剧情 ➔", type="primary", use_container_width=True):
        st.session_state.player_role = selected_role
        st.session_state.target_member = selected_member
        st.session_state.current_act = 1
        st.session_state.dialogue_history = []
        st.session_state.stage = "story"
        st.rerun()

# -----------------------------------------------------------------------------
# 剧情互动阶段
# -----------------------------------------------------------------------------
elif st.session_state.stage == "story":
    role = st.session_state.player_role
    member = st.session_state.target_member
    act = st.session_state.current_act
    m_info = MEMBERS[member]
    
    # 获取对应身份的剧本，若无匹配则兜底到经纪人第一幕
    role_stories = STORIES.get(role, STORIES["经纪人"])
    scene_data = role_stories.get(act, role_stories[1])
    
    st.markdown(f"### 💖 【{role}】 × **{member}** (第 {act}/{MAX_ACT} 幕)")
    st.info(f"💡 当前心动指数（积分）：**{st.session_state.total_score} 分**")
    
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 15px;">
            <img src="{m_info['img']}" width="100%" style="border-radius: 12px; max-height: 200px; object-fit: cover;">
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.subheader(scene_data["title"])
    
    if st.session_state.dialogue_history:
        st.markdown("---")
        for item in st.session_state.dialogue_history:
            st.markdown(f"💬 **你**：{item['choice_text']}")
            st.success(f"💖 **{member} 的回应**：{item['reply_text']}")
        st.markdown("---")
    
    st.markdown("👉 **请做出你的回应选择：**")
    for idx, (c_text, r_text, score_val) in enumerate(scene_data["choices"]):
        if st.button(c_text, key=f"choice_btn_{act}_{idx}", use_container_width=True):
            if st.session_state.active_buff == "🍬 恋爱加倍糖果":
                score_val *= 2
                st.toast("🍬 成功触发加倍糖果！本次好感度积分翻倍！", icon="✨")
                st.session_state.active_buff = None
            elif st.session_state.active_buff:
                st.toast(f"✨ 成功触发【{st.session_state.active_buff}】的浪漫氛围加成！", icon="💖")
                score_val += 10
                st.session_state.active_buff = None
            
            st.session_state.dialogue_history.append({
                "choice_text": c_text,
                "reply_text": r_text
            })
            st.session_state.total_score += score_val
            
            if act < MAX_ACT:
                st.session_state.current_act += 1
            else:
                st.session_state.stage = "result"
            st.rerun()
            
    st.markdown("---")
    if st.button("🏠 放弃当前进度，返回主菜单"):
        st.session_state.stage = "menu"
        st.rerun()

# -----------------------------------------------------------------------------
# 结算阶段
# -----------------------------------------------------------------------------
elif st.session_state.stage == "result":
    role = st.session_state.player_role
    member = st.session_state.target_member
    score = st.session_state.total_score
    m_info = MEMBERS[member]
    
    st.balloons()
    st.header("🏆 结算：HE 甜蜜告白结局")
    st.success(f"在【{role}】的故事中，你与 **{member}** 的最终心动指数为：**{score} 分**！")
    
    st.markdown(
        f"""
        <div class="card-box" style="text-align: center;">
            <img src="{m_info['img']}" width="100%" style="border-radius: 12px; max-height: 300px; object-fit: cover;">
            <p style="margin-top: 15px; font-weight: bold; font-size: 1.2rem; color: #e11d48;">✨ 达成 HE 专属告白：【{member} × {role}】</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        > 『不管身份如何转换，在灯光下的角落里，紧紧握住你的手，这就是属于我们【{role} × {member}】独一无二的甜蜜恋情。』
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        if st.button("🔄 重新体验当前角色", use_container_width=True):
            st.session_state.current_act = 1
            st.session_state.total_score = 30
            st.session_state.dialogue_history = []
            st.session_state.stage = "story"
            st.rerun()
    with col_r2:
        if st.button("🏠 返回主菜单/更换角色", use_container_width=True):
            st.session_state.stage = "menu"
            st.session_state.current_act = 1
            st.session_state.total_score = 30
            st.session_state.dialogue_history = []
            st.session_state.inventory = []
            st.session_state.active_buff = None
            st.session_state.daily_gacha_result = None
            st.rerun()
