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
        background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%);
    }
    .main-header {
        font-size: 2.2rem;
        color: #e11d48;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0;
    }
    .sub-header {
        text-align: center;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .card-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 2. 7人全员基础数据源与写真
# -----------------------------------------------------------------------------
MEMBERS = {
    "丈君": {"trait": "搞笑又可靠的大哥哥", "color": "蓝色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRxeLPXR2kAxnf8Z0uNFWIH7j_vjPcrr8Eg1qWtaTSoPKTvTMcZtXXX6Kn&s=10"},
    "大酱": {"trait": "热情太阳般的 C 位", "color": "红色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEiQYHWo7za_O6O-FerVkj5mA2s49UBL3hj_Tfmu-npd2yfIz1OJSCHD8n&s=10"},
    "布丁": {"trait": "温柔体贴又元气的队长", "color": "绿色", "img": "https://img-mdpr.freetls.fastly.net/article/H0CW/nm/H0CW_-CrOagXoRlSyQPOD6_zSqLjGNjyrfLRLWlqECw.jpg?width=750"},
    "高恭": {"trait": "自恋又帅气的傲娇少年", "color": "紫色", "img": "https://img-mdpr.freetls.fastly.net/article/d4sb/nm/d4sbe7H-P8R6sUQpAshcntVT8-h0ZPcuMe3icV8aOm4.jpg?width=750"},
    "流星": {"trait": "眼睛会闪光的小恶魔", "color": "橙色", "img": "https://oggi.jp/wp-content/uploads/2023/03/DMA-DSC00151_2-2.jpg"},
    "米七": {"trait": "高挑清纯的长腿王子", "color": "粉色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvYWZ1rSHkldisNtmwbvxSYNjR8FWjj4_wdyKxw84_h0SabJN81yYpsGXL&s=10"},
    "谦杜": {"trait": "时尚又有主见的末子", "color": "黄色", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRs8ILDomyP9A6WZPtgig1e6IyPPmSpxS8HSYiRImU0uSqXicpvyNrHV8A&s=10"},
}

ROLES = ["经纪人", "青梅竹马", "在日留学生or打工人"]

# 总幕数（可在此自由修改，比如改成 5 代表 5 幕）
MAX_ACT = 4

# -----------------------------------------------------------------------------
# 3. 核心全员精细化剧情数据库 (支持扩展到 4 幕)
# -----------------------------------------------------------------------------
DETAILED_STORIES = {
    "经纪人": {
        "丈君": {
            1: {
                "title": "🎬 第一幕：后台行程与考勤Check",
                "choices": [
                    ("顺着他的话打趣：『紧张的话，要不要我给你一个爱的鼓励？』", "『呜哇，你别突然这么正经，搞得我心跳比待会录节目还快！』", 20),
                    ("递上提词卡严肃道：『少废话，第三个笑话梗你刚才排练又忘词了！』", "『好啦好啦，金牌经纪人大人饶命！有你在后台盯着，我绝对不会砸场子的！』", 15),
                    ("默默递上一杯冰麦茶不说话", "『还是你最懂我……虽然平时总管着我，但其实最离不开的就是你啦。』", 25)
                ]
            },
            2: {
                "title": "🎬 第二幕：深夜保姆车的后座独处",
                "choices": [
                    ("假装靠在车窗边闭目养神", "（悄悄把肩膀挪过来让你靠着）『累了就靠一会儿吧……有我在，安心睡到终点站。』", 25),
                    ("翻看接下来的行程表轻声提醒他早点休息", "『工作狂经纪人小姐，现在是私人时间，不许再看文件了，快看着我。』", 20),
                    ("小声调侃他今天在节目里的搞笑失误", "『喂！那是个意外！不过……能让你一直笑着，就算出糗也值了。』", 15)
                ]
            },
            3: {
                "title": "🎬 第三幕：清晨事务所天台的对峙",
                "choices": [
                    ("迎上他的目光：『怎么了？是有新的通告安排吗？』", "『以后不只是工作上的搭档……我的余生，我也想申请做你专属的唯一伴侣。』", 30),
                    ("有些害羞地别过头去", "『别把脸转过去嘛……我好不容易鼓起勇气对你表白，给点面子笑一笑好不好？』", 25)
                ]
            },
            4: {
                "title": "🎬 第四幕：杀青后的浪漫专属邀约",
                "choices": [
                    ("笑着答应他的私下约会", "『太好了！这可是你亲口答应的私下约会，不准反悔哦！』", 30),
                    ("假装傲娇地挑挑眉", "『好啦，看在你最近表现不错的份上，勉强答应你啦。』", 25)
                ]
            }
        },
        "大酱": {
            1: {
                "title": "🎬 第一幕：联访前夕的紧急对词",
                "choices": [
                    ("拍拍他的肩膀：『放轻松，以你的口才绝对没问题。』", "『听到你这么说，我突然就有底气了！等下采访我一定超常发挥！』", 20),
                    ("递上提纲：『这一段记者可能会挖坑，注意应答。』", "『有你把关我一万个放心……不过，采访结束后必须陪我喝一杯奶茶！』", 25),
                    ("假装板起脸：『要是表现不好扣你鸡腿。』", "『别介介！经纪人大人手下留情，我马上进入营业状态还不行嘛！』", 15)
                ]
            },
            2: {
                "title": "🎬 第二幕：后台更衣室的短暂喘息",
                "choices": [
                    ("帮他调整衣领：『今天这套造型很适合你。』", "『离我这么近……我会心跳加速、连台词都快忘光啦。』", 25),
                    ("递上温水：『润润嗓子，下一场直播要开始了。』", "『谢谢你……每次有你在背后默默支持，我就什么都不怕了。』", 20),
                    ("调侃道：『刚才镜头前笑得挺灿烂嘛。』", "『因为看到你在侧幕对着我笑呀，那可是我的独家能量源。』", 15)
                ]
            },
            3: {
                "title": "🎬 第三幕：深夜收工后的真情流露",
                "choices": [
                    ("收拾好公文包：『很晚了，今天辛苦啦。』", "『辛苦是不辛苦，就是……好想让我们的关系不只是工作。做我女朋友吧？』", 30),
                    ("笑着看他：『大明星还有什么吩咐吗？』", "『唯一的吩咐就是——以后你的每个深夜，都只能留给我一个人。』", 25)
                ]
            },
            4: {
                "title": "🎬 第四幕：闪光灯外的纯粹对视",
                "choices": [
                    ("轻轻握住他的手回应", "『手好暖……从今以后，我的镜头里和心里，全都是你。』", 30),
                    ("笑着戳戳他的脸", "『好啦，大明星，我们该去过二人世界了。』", 25)
                ]
            }
        },
        "布丁": {
            1: {
                "title": "🎬 第一幕：队长后台的元气补充",
                "choices": [
                    ("递上一块点心：『看你排练消耗挺大，补充点能量。』", "『哇！还是你最贴心！吃了这个我感觉又能连跳三个小时了！』", 25),
                    ("提醒道：『队长，等下的会议发言稿准备好了吗？』", "『嘿嘿，有你在我身边当智囊，我只要负责帅气登场就好啦！』", 20),
                    ("假装生气：『不许偷吃零食，保持身材！』", "『好啦好啦听你的！那……以后我的身材和心，也都全权交给你管理好不好？』", 25)
                ]
            },
            2: {
                "title": "🎬 第二幕：演唱会中场休息的击掌",
                "choices": [
                    ("伸手和他用力击掌：『上半场表现完美！』", "『耶！这下可算没辜负你平时的辛苦排练监督！』", 20),
                    ("递上毛巾细心擦汗：『快擦擦，别感冒了。』", "（满脸傻笑地看着你）『有你照顾我，我真的觉得我是世界上最幸福的队长。』", 25),
                    ("笑着催促：『快换衣服，别让大家等。』", "『遵命！等巡演结束，你一定要答应我一个私下约会的请求哦！』", 20)
                ]
            },
            3: {
                "title": "🎬 第三幕：庆功宴后的单独驻足",
                "choices": [
                    ("看着他认真说：『今天辛苦啦，队长大人。』", "『一点都不辛苦！只要能一直和你并肩走下去，我愿意当一辈子你的专属大男孩。』", 30),
                    ("拍拍他肩膀：『早点回去休息吧。』", "『不要急着走嘛……今晚我有话想对你说：我喜欢你，做我的人吧！』", 25)
                ]
            },
            4: {
                "title": "🎬 第四幕：星空下的队长告白誓言",
                "choices": [
                    ("笑着点头：『好呀，以后我来管着你。』", "『太棒了！有你在，我的队长生涯绝对是满分甜蜜！』", 30)
                ]
            }
        },
        "高恭": {
            1: {
                "title": "🎬 第一幕：后台的傲娇过招",
                "choices": [
                    ("敲敲他的桌子：『造型做完了吗？马上要走了。』", "『催什么催，本大爷自有分寸……不过，今天你穿这身还挺好看的。』", 15),
                    ("递上润喉糖：『少耍帅了，快把这个含着护嗓子。』", "（耳根微红地接过去）『啰嗦……下次别买这么甜的。』", 25),
                    ("假装没看见他直接走过去", "『喂！你就这么无视我？本大爷这么帅，你多看一眼会死啊！』", 20)
                ]
            },
            2: {
                "title": "🎬 第二幕：演唱会侧幕的笨拙温柔",
                "choices": [
                    ("强行把毛巾糊他头上：『热死你得了，快擦汗！』", "『喂！发型会被你弄乱的啦！……不过，谢谢你每次都第一时间冲过来。』", 25),
                    ("温柔地帮他擦拭额头汗水", "（瞬间僵住，眼神飘忽）『……干嘛突然这么温柔，犯规了吧你。』", 30),
                    ("翻个白眼：『嫌弃的话毛巾自己拿去。』", "『别走啊！我开玩笑的还不行吗？快帮我擦，手酸……』", 15)
                ]
            },
            3: {
                "title": "🎬 第三幕：空无一人的休息室告白",
                "choices": [
                    ("疑惑地看着他：『还有什么东西忘带了吗？』", "『笨蛋……我是说，以后本大爷的专属温柔只对你一个人开放，听见没！』", 30),
                    ("笑着逗他：『傲娇可是追不到人的哦。』", "『谁、谁傲娇了！总之……不许拒绝我，从今天起你就是我的人了！』", 25)
                ]
            },
            4: {
                "title": "🎬 第四幕：傲娇少年的最终投降",
                "choices": [
                    ("笑着戳他泛红的耳朵：『好啦，知道啦。』", "『不准笑！……总之，以后不许再把视线投给别人了。』", 30)
                ]
            }
        },
        "流星": {
            1: {
                "title": "🎬 第一幕：时尚化妆间的恶魔微笑",
                "choices": [
                    ("帮他调整发卡：『今天这个造型很适合你。』", "『那是当然！不过……你在我旁边，我总忍不住想逗逗你。』", 20),
                    ("严肃道：『不许乱动，马上要上台了。』", "『好嘛好嘛，听经纪人姐姐的话。只要你待会笑一下，我就乖乖听话。』", 25),
                    ("把行程表拍在他桌上：『自己看接下来的通告。』", "『这么凶呀？不过你生气的样子也超可爱，真想藏起来只给我一个人看。』", 15)
                ]
            },
            2: {
                "title": "🎬 第二幕：闪光灯后的悄悄话",
                "choices": [
                    ("递上冰饮：『刚才台上wink得挺熟练嘛。』", "『那是营业需要！但我刚才那个眼神，其实是专门对着台侧的你抛的哦。』", 25),
                    ("戳戳他脸颊：『少油嘴滑舌的。』", "『才没有油嘴滑舌！面对你我说的可都是真心话，不信你听我心跳。』", 20),
                    ("收拾好杂物准备离开", "『别走太快嘛……今晚收工后陪我去吃甜品，不许拒绝！』", 20)
                ]
            },
            3: {
                "title": "🎬 第三幕：化妆台镜子前的直球告白",
                "choices": [
                    ("拍拍他肩膀：『收工啦，今天表现很棒。』", "『表现再好，没有你的奖励也是白搭。做我女朋友，这就是我想要的最高奖励。』", 30),
                    ("笑着反问：『小恶魔也有正经的时候？』", "『对你我什么时候不正经了！认真说，我的余生都交给你了，接不接受？』", 25)
                ]
            },
            4: {
                "title": "🎬 第四幕：小恶魔的独占宣言",
                "choices": [
                    ("笑着答应：『好呀，以后只准对我一个人笑。』", "『遵命！我的专属经纪人大人，余生请多指教！』", 30)
                ]
            }
        },
        "米七": {
            1: {
                "title": "🎬 第一幕：时尚杂志拍摄后台的低语",
                "choices": [
                    ("帮他仔细整理领口：『今天这套造型非常完美哦。』", "（低头看着你，耳根微微泛红）『每次你这样帮我整理……我都觉得心跳好快，快没办法专心拍照了。』", 25),
                    ("调侃道：『不愧是国宝级帅哥，今天闪闪发光呢。』", "『别笑话我了……你在旁边看着我的时候，我才没办法集中注意力呢。』", 15),
                    ("公事公办地拍拍他肩膀：『快去候场吧，别耽误时间。』", "『好冷淡……明明刚才摄影师夸我时，我只想听你一个人的夸奖。』", 20)
                ]
            },
            2: {
                "title": "🎬 第二幕：收工后的私下对剧本",
                "choices": [
                    ("疑惑回望：『怎么了？后面的台词有什么不懂的吗？』", "『台词我都懂……我只是在想，什么时候才能让你只做我一个人的专属经纪人。』", 25),
                    ("拍拍他的肩膀：『快把最后一段对完好早点收工休息！』", "『好吧……既然你这么急着收工，那今晚收工后必须陪我一起去吃拉面作为惩罚！』", 20),
                    ("故意逗他：『大明星有什么指示呀？』", "『指示就是……不许再看别人，今晚你的视线只能留给我一个人。』", 25)
                ]
            },
            3: {
                "title": "🎬 第三幕：深夜车库的温柔心意",
                "choices": [
                    ("惊讶回头：『米七？怎么还不回去？』", "『因为还没对你说完最重要的话……做我的恋人吧，好吗？』", 30),
                    ("顺势握住他的手笑着调侃", "『不是在做梦……只要能一直牵着你的手，我就拥有了全世界的光芒。』", 25)
                ]
            },
            4: {
                "title": "🎬 第四幕：长腿王子的最终告白",
                "choices": [
                    ("笑着与他十指紧扣：『好，以后一直陪着你。』", "『太好了……有你在，我才是真正被光芒包围的人。』", 30)
                ]
            }
        },
        "谦杜": {
            1: {
                "title": "🎬 第一幕：服装间的时尚灵感突击",
                "choices": [
                    ("打量他的潮服：『今天的私服很有个性嘛。』", "『那当然！这可是我特意为了今天能吸引你的目光搭配的！』", 25),
                    ("提醒他：『快把麦克风戴好，别耽误试音。』", "『好啦好啦，经纪人大人管得真宽……不过我就喜欢你管着我的样子。』", 20),
                    ("递上行程资料：『看看明天的通告安排。』", "『明天行程先放一边，今晚你得答应陪我去看新出的时尚展！』", 15)
                ]
            },
            2: {
                "title": "🎬 第二幕：彩排间隙的吉他伴奏",
                "choices": [
                    ("听着吉他音色赞叹：『弹得越来越好了。』", "『这首歌的旋律，是我看着你时脑子里自然蹦出来的音符哦。』", 25),
                    ("开玩笑道：『要不要考虑给经纪人写首歌？』", "『早就写好了！歌名就叫《专属经纪人》，只差你点头当女主角了。』", 25),
                    ("催促道：『别偷懒，音箱还没调好呢。』", "『遵命！不过等下调试完，你必须请我喝咖啡作为补偿。』", 20)
                ]
            },
            3: {
                "title": "🎬 第三幕：录音棚门口的浪漫直球",
                "choices": [
                    ("顺手帮他理了理衣领：『今天工作结束啦。』", "『工作结束了，但我们的恋爱才刚要开始。做我女朋友，好不好？』", 30),
                    ("笑着挑眉：『你这小子又在打什么主意。』", "『绝对不是打主意，是蓄谋已久！把心交给我，绝对不会让你输的。』", 25)
                ]
            },
            4: {
                "title": "🎬 第四幕：末子的潮酷专属契约",
                "choices": [
                    ("笑着点头答应：『好呀，我的专属音乐人。』", "『耶！接下来我会为你写出世界上最甜的情歌！』", 30)
                ]
            }
        }
    }
}

# 青梅竹马与打工人群组若无第4幕，系统会自动提供动态兜底，无需担心报错！
# (你可以参照上面经纪人的格式，在其它身份里任意补充第 4 幕)

# -----------------------------------------------------------------------------
# 4. Session State 初始化
# -----------------------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0  # 0: 选择身份 ➔ 1: 选择攻略对象 ➔ 2+: 剧情幕 ➔ 5: 结算
if "player_role" not in st.session_state:
    st.session_state.player_role = ""
if "target_member" not in st.session_state:
    st.session_state.target_member = ""
if "current_act" not in st.session_state:
    st.session_state.current_act = 1
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "dialogue_history" not in st.session_state:
    st.session_state.dialogue_history = []

# -----------------------------------------------------------------------------
# 5. 页面核心逻辑与渲染
# -----------------------------------------------------------------------------
st.markdown('<p class="main-header">💖 偶像专属心动企划</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">全员 7 人满配 ＋ 三大身份分支 ＋ 多幕沉浸式剧情 (当前共 {MAX_ACT} 幕)</p>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 阶段 0：选择身份
# -----------------------------------------------------------------------------
if st.session_state.step == 0:
    st.subheader("🎭 第一步：请选择你在故事中的身份：")
    selected_role = st.radio("你的身份定位：", ROLES)
    
    if st.button("确认身份，挑选心动对象 ➔", type="primary", use_container_width=True):
        st.session_state.player_role = selected_role
        st.session_state.step = 1
        st.rerun()

# -----------------------------------------------------------------------------
# 阶段 1：选择攻略对象 (7人全量可选)
# -----------------------------------------------------------------------------
elif st.session_state.step == 1:
    st.subheader(f"💖 第二步：当前身份【{st.session_state.player_role}】，请从下方 7 位成员中选择你想攻略的对象：")
    
    chosen_member = st.selectbox("选择你的心动男主角：", list(MEMBERS.keys()))
    
    m_info = MEMBERS[chosen_member]
    st.markdown(
        f"""
        <div class="card-box" style="text-align: center;">
            <img src="{m_info['img']}" width="100%" style="border-radius: 12px; max-height: 300px; object-fit: cover;">
            <p style="margin-top: 10px; font-weight: bold; font-size: 1.1rem; color: #e11d48;">✨ {chosen_member} ({m_info['trait']})</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 重新选择身份"):
            st.session_state.step = 0
            st.rerun()
    with col2:
        if st.button("开启专属恋爱剧情 ➔", type="primary"):
            st.session_state.target_member = chosen_member
            st.session_state.current_act = 1
            st.session_state.total_score = 0
            st.session_state.dialogue_history = []
            st.session_state.step = 2  # 进入第一幕
            st.rerun()

# -----------------------------------------------------------------------------
# 阶段 2 及以后：动态剧情幕推进 (自动支持 MAX_ACT 幕数)
# -----------------------------------------------------------------------------
elif st.session_state.step >= 2 and st.session_state.step < 5:
    role = st.session_state.player_role
    member = st.session_state.target_member
    act = st.session_state.current_act
    
    m_info = MEMBERS[member]
    
    # 动态获取当前身份、当前成员、当前幕的剧本（若没写该幕，自动兜底生成）
    role_stories = DETAILED_STORIES.get(role, {})
    member_story = role_stories.get(member, {})
    scene_data = member_story.get(act, {
        "title": f"🎬 第 {act} 幕：心动日常进展中",
        "choices": [
            ("微笑着向他靠近一步", f"『怎么突然靠这么近……不过，我一点也不讨厌。』", 20),
            ("调侃他今天的表情很有趣", f"『好啊你，居然敢笑话我！看我怎么“惩罚”你～』", 15),
            ("安静地陪伴在他身旁", f"『只要有你陪着，哪怕什么都不做也是最幸福的时光。』", 25)
        ]
    })
    
    st.markdown(f"### 🎭 当前身份：【{role}】 | 攻略对象：**{member}** (第 {act}/{MAX_ACT} 幕)")
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 15px;">
            <img src="{m_info['img']}" width="100%" style="border-radius: 12px; max-height: 220px; object-fit: cover;">
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.subheader(scene_data["title"])
    
    # 展示历史对话记录
    if st.session_state.dialogue_history:
        st.markdown("---")
        for item in st.session_state.dialogue_history:
            st.markdown(f"💬 **你**：{item['choice_text']}")
            st.success(f"💖 **{member} 的回应**：{item['reply_text']}")
        st.markdown("---")
    
    st.markdown("👉 **请根据他的性格做出你的回应：**")
    for idx, (c_text, r_text, score_val) in enumerate(scene_data["choices"]):
        if st.button(c_text, key=f"choice_btn_{act}_{idx}", use_container_width=True):
            st.session_state.dialogue_history.append({
                "choice_text": c_text,
                "reply_text": r_text
            })
            st.session_state.total_score += score_val
            
            # 核心判定：如果还没到最高幕数，就继续推进；如果到了，就进入最终结局结算
            if act < MAX_ACT:
                st.session_state.current_act += 1
            else:
                st.session_state.step = 5  # 进入最终结局结算
            st.rerun()

# -----------------------------------------------------------------------------
# 阶段 5：专属结局结算 (全员 7 人独立专属告白)
# -----------------------------------------------------------------------------
elif st.session_state.step == 5:
    role = st.session_state.player_role
    member = st.session_state.target_member
    score = st.session_state.total_score
    m_info = MEMBERS[member]
    
    st.balloons()
    st.header("🏆 专属心动结局结算")
    st.success(f"在【{role}】身份下，你与 **{member}** 共同经历 {MAX_ACT} 幕历练，最终羁绊得分为：**{score} 分**！")
    
    st.markdown(
        f"""
        <div class="card-box" style="text-align: center;">
            <img src="{m_info['img']}" width="100%" style="border-radius: 12px; max-height: 320px; object-fit: cover;">
            <p style="margin-top: 15px; font-weight: bold; font-size: 1.2rem; color: #e11d48;">✨ 达成 HE 专属告白结局：【{member} × {role}】</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 7人全员独立的专属告白情话
    ENDING_QUOTES = {
        "丈君": "『无论是聚光灯下的万人瞩目，还是狭窄后台的疲惫时刻……只要你在我身旁，我就是最闪耀的那个。做我唯一的专属偏爱，好吗？』",
        "大酱": "『这些日子谢谢你一直包容我、陪在我身旁。比起那些遥不可及的奖杯，我现在最想拥抱和拥有的，只有你一个。』",
        "布丁": "『所有好吃的布丁我都想分你一半，不，全给你也可以！只要……你愿意把你的余生也分我一半！』",
        "高恭": "『在你面前，我不用扮演那个完美酷炫的大人。未来的路还很长，我想带着最真实的心，牵着你一直走下去。』",
        "流星": "『每一次眨眼和微笑，都是只对你一个人的营业。不，不对……我对你的爱才不是营业，是百分之百的真心！』",
        "米七": "『每次累到想放弃的时候，只要看到你，我就能重新充满力量。别离开我……变成我余生唯一的避风港吧。』",
        "谦杜": "『我写了那么多好听的旋律，但只有面对你时，我才明白那些音符真正的意义。这首为你而写的歌，你想听一辈子吗？』"
    }
    
    quote = ENDING_QUOTES.get(member, f"『能遇见你，是我这辈子最幸运的奇迹。今后的每一天，我的眼里都只有你。』")
    
    st.markdown(
        f"""
        > {quote}
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        if st.button("🔄 重新攻略当前角色", use_container_width=True):
            st.session_state.current_act = 1
            st.session_state.total_score = 0
            st.session_state.dialogue_history = []
            st.session_state.step = 2
            st.rerun()
    with col_r2:
        if st.button("🏠 返回主菜单/更换身份", use_container_width=True):
            st.session_state.step = 0
            st.session_state.player_role = ""
            st.session_state.target_member = ""
            st.session_state.current_act = 1
            st.session_state.total_score = 0
            st.session_state.dialogue_history = []
            st.rerun()
