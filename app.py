import streamlit as st
import random
import os

# -----------------------------------------------------------------------------
# 1. 页面基本配置与自定义背景 CSS
# -----------------------------------------------------------------------------
st.set_page_config(page_title="浪花男子心动日常", page_icon="💖", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #ffdde1 0%, #ee9ca7 50%, #a1c4fd 100%);
        background-attachment: fixed;
        background-size: cover;
    }
    .stMainBlockContainer {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def safe_image(img_path, caption=None):
    if not img_path:
        return
    if str(img_path).startswith("http"):
        st.image(img_path, caption=caption, use_container_width=True)
    elif os.path.exists(img_path):
        st.image(img_path, caption=caption, use_container_width=True)
    else:
        st.warning(f"图片路径或网址无法加载: {img_path}")

def safe_audio(audio_path):
    if audio_path and os.path.exists(audio_path):
        try:
            st.audio(audio_path, loop=True, autoplay=True)
        except Exception:
            pass

# -----------------------------------------------------------------------------
# 2. 成员数据配置
# -----------------------------------------------------------------------------
MEMBERS = {
    "丈君": {
        "nick": "丈君", 
        "trait": "搞笑又可靠的大哥哥", 
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRxeLPXR2kAxnf8Z0uNFWIH7j_vjPcrr8Eg1qWtaTSoPKTvTMcZtXXX6Kn&s=10", 
        "color": "💙 蓝色"
    },
    "大酱": {
        "nick": "大酱", 
        "trait": "热情太阳般的 C 位", 
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEiQYHWo7za_O6O-FerVkj5mA2s49UBL3hj_Tfmu-npd2yfIz1OJSCHD8n&s=10", 
        "color": "🔴 红色"
    },
    "布丁": {
        "nick": "布丁", 
        "trait": "温柔体贴又吃得超香的队长", 
        "img": "https://img-mdpr.freetls.fastly.net/article/H0CW/nm/H0CW_-CrOagXoRlSyQPOD6_zSqLjGNjyrfLRLWlqECw.jpg?width=750&disable=upscale&auto=webp&quality=80", 
        "color": "💚 绿色"
    },
    "高恭": {
        "nick": "高恭", 
        "trait": "自恋又亚撒西的八嘎帅哥", 
        "img": "https://img-mdpr.freetls.fastly.net/article/d4sb/nm/d4sbe7H-P8R6sUQpAshcntVT8-h0ZPcuMe3icV8aOm4.jpg?width=750&disable=upscale&auto=webp&quality=80", 
        "color": "💜 紫色"
    },
    "流星": {
        "nick": "流星", 
        "trait": "眼睛会闪光的小恶魔", 
        "img": "https://oggi.jp/wp-content/uploads/2023/03/DMA-DSC00151_2-2.jpg", 
        "color": "🧡 橙色"
    },
    "米七": {
        "nick": "米七", 
        "trait": "高挑帅气的长腿王子", 
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvYWZ1rSHkldisNtmwbvxSYNjR8FWjj4_wdyKxw84_h0SabJN81yYpsGXL&s=10", 
        "color": "💖 粉色"
    },
    "谦杜": {
        "nick": "谦杜", 
        "trait": "时尚又有主见的小恶魔末子", 
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRs8ILDomyP9A6WZPtgig1e6IyPPmSpxS8HSYiRImU0uSqXicpvyNrHV8A&s=10", 
        "color": "💛 黄色"
    },
}

ROLES = ["经纪人", "粉丝/地下恋", "青梅竹马", "在日留学生or打工人"]

# -----------------------------------------------------------------------------
# 3. 7 人专属独立剧情与个性化台词大数据库
# -----------------------------------------------------------------------------
CHARACTER_SCRIPTS = {
    "经纪人": {
        "丈君": {
            1: {
                "title": "🎬 第一幕：后台的斗嘴日常",
                "desc": "离上台还有 10 分钟，藤原丈一郎正靠在化妆台前对着镜子练习耍帅，顺便用余光瞥见你走过来。",
                "choices": [
                    {"label": "🅰️ 顺着他的话打趣：『哟，大明星今天这帅气度超标了，少照两面镜子吧！』", "key": "A"},
                    {"label": "🅱️ 递上手卡正色道：『行了，别自恋了，下一档通告的采访提纲看完了吗？』", "key": "B"},
                    {"label": "🆎 假装严肃：『再不抓紧彩排，今晚的夜宵串炸直接取消！』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『喂喂！什么叫少照两面镜子，我这叫对舞台负责好不好！不过……今晚的串炸你得请客！』", "score": 20},
                    "B": {"text": "『看过了看过了，不就是那些梗嘛，交给我藤原丈一郎绝对稳妥！』", "score": 15},
                    "AB": {"text": "『别介啊经纪人大人！我排练还不行吗，千万别取消串炸！』", "score": 5}
                }
            },
            2: {
                "title": "🎬 第二幕：突发的服装危机",
                "desc": "中场换装时间仅剩 1 分钟，丈君急得满头大汗——他的舞台外套拉链竟然卡住了！",
                "choices": [
                    {"label": "🅰️ 迅速上前帮他理顺拉链，拍拍他肩膀：『别急，深呼吸，有我在呢。』", "key": "A"},
                    {"label": "🅱️ 赶紧招呼服装老师：『快来人，这边服装出状况了！』", "key": "B"},
                    {"label": "🆎 调侃道：『你这是最近棒球打多了把肩膀练宽了吧？』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『（身体微微一僵，随后笑开）哇……刚才那一瞬间，你比经纪人看起来更像我的救世主。』", "score": 20},
                    "B": {"text": "『谢啦！老师快救救我，下半场要来不及登场了！』", "score": 15},
                    "AB": {"text": "『才不是！分明是这衣服太小气了！』", "score": 5}
                }
            },
            3: {
                "title": "🎬 第三幕：深夜保姆车的靠肩",
                "desc": "演出圆满结束，回程的保姆车上很安静，丈君累得直打哈欠，脑袋一点一点的。",
                "choices": [
                    {"label": "🅰️ 轻轻把他的头扶到自己肩膀上：『累了就靠一会儿吧，到地方我叫你。』", "key": "A"},
                    {"label": "🅱️ 递过一瓶水：『辛苦了，喝口水提提神。』", "key": "B"},
                    {"label": "🆎 拿行程表敲敲他：『别睡死过去，明早还有早班通告呢！』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『（顺势靠过来，声音有些含糊）嗯……有你在真好，先让我借个肩膀充会儿电……』", "score": 25},
                    "B": {"text": "『谢啦，正好喉咙干得要命，你总是这么贴心。』", "score": 15},
                    "AB": {"text": "『呜哇……让我再睡 5 分钟嘛，经纪人大人！』", "score": 5}
                }
            }
        },
        "大酱": {
            1: {
                "title": "🎬 第一幕：C 位的赛前焦虑",
                "desc": "离上台还有 10 分钟，西畑大吾一个人坐在角落反复确认手卡，眉头微微皱着，显得有些紧绷。",
                "choices": [
                    {"label": "🅰️ 走过去递上一杯温茶：『大吾，你已经做得很好了，放轻松。』", "key": "A"},
                    {"label": "🅱️ 拍拍手提醒大家：『好啦，准备集合对流程了！』", "key": "B"},
                    {"label": "🆎 坐在他旁边开玩笑：『怎么啦，C 位大人的台词又忘啦？』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『（握着温茶，紧绷的肩膀放松下来）嗯……只要有你在旁边看着，我心里就踏实多了。』", "score": 20},
                    "B": {"text": "『收到!我这就来，谢谢你总是这么细心地帮大家掌控全局。』", "score": 15},
                    "AB": {"text": "『才没忘呢！我只是在脑海里把走位再过一遍……』", "score": 5}
                }
            },
            2: {
                "title": "🎬 第二幕：麦克风小故障",
                "desc": "后台候场时，大酱的耳麦突然传出刺鼻的杂音，距离登场只有半分钟了。",
                "choices": [
                    {"label": "🅰️ 飞速帮他摘下耳麦重新调试：『别慌，看着我，来得及！』", "key": "A"},
                    {"label": "🅱️ 冲音响师大喊：『这里耳麦有问题，快换备用的！』", "key": "B"},
                    {"label": "🆎 催促道：『快点快点，马上要切镜头了！』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『（看着你认真的侧脸）呼……刚才那一瞬间心跳差点漏了一拍，多亏有你。』", "score": 20},
                    "B": {"text": "『谢谢老师！音响师快帮我换一下！』", "score": 15},
                    "AB": {"text": "『我知道的……马上就好！』", "score": 5}
                }
            },
            3: {
                "title": "🎬 第三幕：深夜的温柔卸防",
                "desc": "深夜收工的车上，大吾卸下了面对镜头时的完美笑容，疲惫地揉着太阳穴。",
                "choices": [
                    {"label": "🅰️ 轻轻帮他揉揉太阳穴：『今天真的辛苦了，靠着休息会儿吧。』", "key": "A"},
                    {"label": "🅱️ 把热饮递给他：『喝点热的暖暖胃，今天表现超级棒。』", "key": "B"},
                    {"label": "🆎 翻看平板：『明天的通告变动我发你手机上了，记得看。』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『（顺势把头轻轻靠在你肩上）只有在你面前，我才能卸下这颗作为 C 位的心……真想一直这样。』", "score": 25},
                    "B": {"text": "『谢谢你，今天你也跟着跑前跑后，比我还要辛苦呢。』", "score": 15},
                    "AB": {"text": "『好……我等下就看，先让我闭眼靠一会儿。』", "score": 5}
                }
            }
        },
        "布丁": {
            1: {
                "title": "🎬 第一幕：元气队长的大吃一惊",
                "desc": "离上台还有 10 分钟，大桥和也正对着空气练习开场大喊，结果差点把自己呛到。",
                "choices": [
                    {"label": "🅰️ 笑着递上润喉茶：『队长大人，还没上台嗓子可不能喊哑啦。』", "key": "A"},
                    {"label": "🅱️ 拿行程表敲敲他：『收敛点，保持体力，要上场了。』", "key": "B"},
                    {"label": "🆎 调侃道：『你是不是又在后台偷吃布丁了？』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『（发出标志性的笑声）吸了一口热茶：太暖了！感觉元气全满，等会儿演出完带我去吃烧肉吧！』", "score": 20},
                    "B": {"text": "『好嘞！麦克风准备完毕，大桥队长随时准备冲锋——！』", "score": 15},
                    "AB": {"text": "『哎呀被发现了？我刚才确实在想草莓布丁的事……这就来！』", "score": 5}
                }
            },
            2: {
                "title": "🎬 第二幕：元气的衣领小麻烦",
                "desc": "快要登台时，布丁的胸针不小心勾住了衣领，急得他直转圈。",
                "choices": [
                    {"label": "🅰️ 笑着走过去轻巧解开：『别乱动，像个小孩子一样。』", "key": "A"},
                    {"label": "🅱️ 招呼服装师：『快来帮他解一下胸针。』", "key": "B"},
                    {"label": "🆎 拍他背一下：『站好别动，我来扯开它！』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『哇！你好厉害！你简直是我的超级经纪人英雄！等下给你比个最大的心～！』", "score": 20},
                    "B": {"text": "『谢谢老师！多亏反应快，差点戳到自己！』", "score": 15},
                    "AB": {"text": "『痛痛痛！轻点轻点，衣服要破啦！』", "score": 5}
                }
            },
            3: {
                "title": "🎬 第三幕：保姆车上的大型犬撒娇",
                "desc": "回程车上，大桥和也毫无防备地趴在座位上，像一只玩累的大狗狗。",
                "choices": [
                    {"label": "🅰️ 摸摸他的头发：『今天辛苦啦，睡吧。』", "key": "A"},
                    {"label": "🅱️ 把外套盖在他身上：『别着凉了。』", "key": "B"},
                    {"label": "🆎 捏他脸颊：『醒醒，口水都要流出来啦！』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『（蹭蹭你的手心）唔……你的手好暖和，晚安好梦哦经纪人酱～』", "score": 25},
                    "B": {"text": "『哇，好贴心！有你当经纪人真的太幸福了！』", "score": 15},
                    "AB": {"text": "『才没有流口水！我只是在梦里吃烧肉呢！』", "score": 5}
                }
            }
        },
        "高恭": {
            1: {
                "title": "🎬 第一幕：自恋少年的对镜整理",
                "desc": "离上台还有 10 分钟，高桥恭平正拿着发胶第 5 次调整自己额前的刘海。",
                "choices": [
                    {"label": "🅰️ 走过去拿走发胶：『已经够帅了，再喷就成硬壳了。』", "key": "A"},
                    {"label": "🅱️ 看了看表：『高桥大人，还有 10 分钟，可以停止欣赏美貌了吗？』", "key": "B"},
                    {"label": "🆎 毫不留情吐槽：『刘海歪了 0.1 毫米，重弄吧。』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『切，我才没有紧张呢！我可是全日本最帅的高桥恭平，发型必须完美无瑕！』", "score": 15},
                    "B": {"text": "『知道了知道了！我的造型和麦克风都是最完美的，放心吧。』", "score": 20},
                    "AB": {"text": "『喂！哪里歪了！别吓我，我这可是精心抓的造型！』", "score": 5}
                }
            },
            2: {
                "title": "🎬 第二幕：帅气造型的意外",
                "desc": "换装时，恭平的外套袖口不小心撕开了一个小口子，他正对着镜子叹气。",
                "choices": [
                    {"label": "🅰️ 拿针线飞速帮他缝好：『好啦，不影响你耍帅。』", "key": "A"},
                    {"label": "🅱️ 叫来服装师紧急更换备用服装。卡", "key": "B"},
                    {"label": "🆎 嘲笑他：『这就是动作太嚣张的报应。』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『（脸颊微红）喂……针线活这么利落干嘛，显得我很笨拙耶，不过……谢啦。』", "score": 20},
                    "B": {"text": "『老师救命！快帮我换那件更帅的备用衣！』", "score": 15},
                    "AB": {"text": "『这叫随性街头风懂不懂！才不是报应！』", "score": 5}
                }
            },
            3: {
                "title": "🎬 第三幕：车窗旁的傲娇靠肩",
                "desc": "回程车上，恭平看着窗外的霓虹发呆，一副酷酷的模样。",
                "choices": [
                    {"label": "🅰️ 轻轻把他的头拉向自己：『累了就靠着，别装酷了。』", "key": "A"},
                    {"label": "🅱️ 递过耳机：『听会儿歌放松下吧。』", "key": "B"},
                    {"label": "🆎 拍他脑袋：『看什么呢，快闭眼睡觉。』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『（别过头，耳根微红）才不是我想靠的……是你的肩膀正好贴过来的而已哦。』", "score": 25},
                    "B": {"text": "『哦，放那吧。看在你这么照顾我的份上，给你打 99 分。』", "score": 15},
                    "AB": {"text": "『知道啦！帅哥也是需要睡眠来养颜的啊，别打我头！』", "score": 5}
                }
            }
        },
        "流星": {
            1: {
                "title": "🎬 第一幕：小恶魔的赛前偷袭",
                "desc": "离上台还有 10 分钟，大西流星突然笑眯眯地转过身，戳了戳你的胳膊。",
                "choices": [
                    {"label": "🅰️ 捏捏他的脸蛋：『又在打什么鬼主意呢，快对台本。』", "key": "A"},
                    {"label": "🅱️ 严肃正色：『流星大人，认真一点，马上登场了。』", "key": "B"},
                    {"label": "🆎 威胁道：『再闹今晚的甜点没收！』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『（眨大眼睛）哼哼，我在想……有你在鼓励我，那我是不是可以向经纪人索要一个专属的后台抱抱作为奖励呢？』", "score": 20},
                    "B": {"text": "『收到指令～流星大人已经准备好散发无限魅力啦！』", "score": 15},
                    "AB": {"text": "『呜哇！太残忍了！经纪人酱一点都不可爱，对爱豆要温柔一点嘛！』", "score": 5}
                }
            },
            2: {
                "title": "🎬 第二幕：眼妆的小危机",
                "desc": "登台前照镜子，流星发现眼角亮片稍微有些晕染。",
                "choices": [
                    {"label": "🅰️ 拿棉签细心地帮他擦拭：『别动，闭上眼，我来弄。』", "key": "A"},
                    {"label": "🅱️ 提醒他：『流星，眼角好像晕了，快补一下。』", "key": "B"},
                    {"label": "🆎 笑着说：『这样也挺好看的，像是泪痣妆。』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『嘻嘻，刚才近距离看我，有没有被流星的眼妆电到呀？』", "score": 20},
                    "B": {"text": "『效率真高！不愧是我们最厉害的经纪人酱～』", "score": 15},
                    "AB": {"text": "『略略略～这种小意外流星大人分分钟解决！』", "score": 5}
                }
            },
            3: {
                "title": "🎬 第三幕：车内的软糯撒娇",
                "desc": "回程车上，流星困得直揉眼睛，把玩着你的衣角。",
                "choices": [
                    {"label": "🅰️ 把他拉到肩上靠着：『困了就睡吧，我看着你。』", "key": "A"},
                    {"label": "🅱️ 递上温热的奶茶：『喝口甜的解解乏。』", "key": "B"},
                    {"label": "🆎 拍拍他：『坐好啦，马上到宿舍了。』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『（小声咕哝）借你的肩膀用一下，作为交换，明天允许你帮我买珍珠奶茶哦～』", "score": 25},
                    "B": {"text": "『奶茶收到啦，今天辛苦你照顾小恶魔流星咯！』", "score": 15},
                    "AB": {"text": "『哼！毫无同情心的经纪人！小心我在明天的 Vlog 里吐槽你！』", "score": 5}
                }
            }
        },
        "米七": {
            1: {
                "title": "🎬 第一幕：长腿王子的紧张时刻",
                "desc": "离上台还有 10 分钟，道枝骏佑修长的身影站在窗前，正深深地吸气吐气。",
                "choices": [
                    {"label": "🅰️ 走过去递过水杯：『骏佑，放轻松，你在舞台上一直都很耀眼。』", "key": "A"},
                    {"label": "🅱️ 确认流程：『麦克风和耳返都调试好了，没问题吧？』", "key": "B"},
                    {"label": "🆎 开玩笑道：『个子长太高把氧气都吸完了吗，怎么直叹气？』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『（脸红着接过去）谢谢你……有你这句话，我感觉心跳平静多了，我会加油的！』", "score": 20},
                    "B": {"text": "『好的！我这就重新检查一遍设备，谢谢你的提醒！』", "score": 15},
                    "AB": {"text": "『非常抱歉！是我注意力不集中了，我这就去调整状态！』", "score": 5}
                }
            },
            2: {
                "title": "🎬 第二幕：台词本的慌乱",
                "desc": "上台前一秒，米七不小心把台词手卡散落了一地，急忙蹲下去捡。",
                "choices": [
                    {"label": "🅰️ 陪着一起蹲下收拾，指尖不小心碰到一起：『别急，慢慢来。』", "key": "A"},
                    {"label": "🅱️ 帮他快速把纸张整理好塞回手里：『给，拿稳了。』", "key": "B"},
                    {"label": "🆎 吐槽：『怎么这么粗心，快要上场啦！』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『（慌乱地低头，耳朵爆红）那个……指尖碰到了……谢谢你帮我弄好！』", "score": 20},
                    "B": {"text": "『谢谢你反应这么快，差点误了大事！』", "score": 15},
                    "AB": {"text": "『对不起对不起！都是我太粗心了！』", "score": 5}
                }
            },
            3: {
                "title": "🎬 第三幕：保姆车上的轻声呢喃",
                "desc": "深夜车内，米七靠在窗边，睡眼惺忪地看着你。",
                "choices": [
                    {"label": "🅰️ 顺势把他的头轻轻靠向自己：『睡吧，到地方我叫你。』", "key": "A"},
                    {"label": "🅱️ 递上毛毯：『盖好别着凉了。』", "key": "B"},
                    {"label": "🆎 提醒道：『快闭眼休息，明天还有杂志拍摄。』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『（迷迷糊糊靠过来，轻声说）不要离开我……有你在真好……』", "score": 25},
                    "B": {"text": "『谢谢你，你也早点休息，今天陪着我们辛苦了。』", "score": 15},
                    "AB": {"text": "『啊！抱歉我睡着了！我这就起来看明天的资料！』", "score": 5}
                }
            }
        },
        "谦杜": {
            1: {
                "title": "🎬 第一幕：时尚末子的赛前摇摆",
                "desc": "离上台还有 10 分钟，长尾谦杜正跟着耳机里的音乐小幅度地扭动身体。",
                "choices": [
                    {"label": "🅰️ 笑着打趣：『时尚icon大人，台风练得不错嘛，上台别忘词哦。』", "key": "A"},
                    {"label": "🅱️ 拍拍他肩膀：『音乐停一下，检查一下耳返电量。』", "key": "B"},
                    {"label": "🆎 严肃警告：『不准在后台跳舞，站好！』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『耶！得到经纪人的专属 Buff 加持！今天的舞台演出绝对爆棚！』", "score": 20},
                    "B": {"text": "『OK～服装和麦克风都很完美，等我上去炸翻全场吧！』", "score": 15},
                    "AB": {"text": "『别急别急嘛！我只是在思考今天的台风怎么走最潮！』", "score": 5}
                }
            },
            2: {
                "title": "🎬 第二幕：潮牌帽衫的小意外",
                "desc": "候场时，谦杜自己设计的潮牌外套抽绳不小心散开了，蝴蝶结打成死结。",
                "choices": [
                    {"label": "🅰️ 细心地帮他把结解开：『真是拿你没办法，像个长不大的小孩。』", "key": "A"},
                    {"label": "🅱️ 帮他直接塞进口袋里：『这样就行了，别管它。』", "key": "B"},
                    {"label": "🆎 强行扯开：『快上台了，别整这些花里胡哨的！』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『哇！手速这么快？不愧是我的专属经纪人！这套 Look 完美救回！』", "score": 20},
                    "B": {"text": "『谢啦！完美隐藏，不愧是你！』", "score": 15},
                    "AB": {"text": "『喂！我这可是最新时尚设计，粗鲁！』", "score": 5}
                }
            },
            3: {
                "title": "🎬 第三幕：深夜车内的潮酷靠肩",
                "desc": "深夜回程车上，谦杜把帽衫帽子一戴，直接往座椅上一倒。",
                "choices": [
                    {"label": "🅰️ 把他的头轻轻拨到自己肩上：『累了就靠一会儿。』", "key": "A"},
                    {"label": "🅱️ 递上一瓶热饮：『喝点东西再睡。』", "key": "B"},
                    {"label": "🆎 敲敲他帽子：『别把帽子拉那么低，闷不闷。』", "key": "AB"}
                ],
                "feedbacks": {
                    "A": {"text": "『（把帽衫帽子一戴，顺势倒在你肩上）借我当个枕头，明天请你喝潮牌咖啡！』", "score": 25},
                    "B": {"text": "『谢啦！补充水分，明天又是活力满满的一天！』", "score": 15},
                    "AB": {"text": "『知道了啦——经纪人大人比我妈妈管得还宽呢～！』", "score": 5}
                }
            }
        }
    }
}
# ==========================================
# 5. 主界面渲染与剧情推进循环
# ==========================================
char_char_info = CHARACTER_SCRIPTS[st.session_state.current_role][st.session_state.current_member]
st.title("💖 浪花男子心动日常")
st.caption(f"当前互动对象：**{st.session_state.current_char}**（{char_info['tag']}）")
st.write(f"_{char_info['desc']}_")

st.divider()

# 显示上一次选择的剧情反馈
if st.session_state.last_feedback:
    st.info(st.session_state.last_feedback)

# 分幕剧情推进与判定
scenes = char_info["scenes"]

# 第一幕
if st.session_state.story_stage == 1:
    s1 = scenes["s1"]
    st.subheader(s1["title"])
    st.write(s1["text"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"A. {s1['opt_A']}"):
            luck = random.randint(1, 10)
            if luck > 4 or (st.session_state.gacha_buff and "心动" in st.session_state.gacha_buff[1]):
                st.session_state.scores["heart"] += 2
            else:
                st.session_state.scores["trust"] += 1
            st.session_state.last_feedback = f"反馈：{s1['res_A']}"
            st.session_state.story_stage = 2
            st.rerun()

    with col2:
        if st.button(f"B. {s1['opt_B']}"):
            luck = random.randint(1, 10)
            if luck > 4 or (st.session_state.gacha_buff and "信任" in st.session_state.gacha_buff[1]):
                st.session_state.scores["trust"] += 2
            else:
                st.session_state.scores["heart"] += 1
            st.session_state.last_feedback = f"反馈：{s1['res_B']}"
            st.session_state.story_stage = 2
            st.rerun()

# 第二幕
elif st.session_state.story_stage == 2:
    s2 = scenes["s2"]
    st.subheader(s2["title"])
    st.write(s2["text"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"A. {s2['opt_A']}"):
            st.session_state.scores["heart"] += random.choice([1, 2])
            st.session_state.last_feedback = f"反馈：{s2['res_A']}"
            st.session_state.story_stage = 3
            st.rerun()

    with col2:
        if st.button(f"B. {s2['opt_B']}"):
            st.session_state.scores["trust"] += random.choice([1, 2])
            st.session_state.last_feedback = f"反馈：{s2['res_B']}"
            st.session_state.story_stage = 3
            st.rerun()

# 第三幕：结局结算
elif st.session_state.story_stage == 3:
    st.subheader("📖 本日结局收录")

    heart_score = st.session_state.scores["heart"]
    trust_score = st.session_state.scores["trust"]

    if heart_score >= trust_score:
        st.success(char_info["endings"]["heart"])
    else:
        st.warning(char_info["endings"]["trust"])

    st.write(f"（本次互动隐藏数值结算 — 心动值：{heart_score} | 信任度：{trust_score}）")

    if st.button("开启新的一天 / 重新开始"):
        st.session_state.story_stage = 1
        st.session_state.scores = {"heart": 0, "trust": 0}
        st.session_state.last_feedback = ""
        st.rerun()
                    
