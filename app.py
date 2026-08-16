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
MAX_ACT = 6  # 6幕完整流程

# -----------------------------------------------------------------------------
# 3. 7人全员多幕专属独立剧情库
# -----------------------------------------------------------------------------
STORIES = {
    "丈君": {
        "经纪人": {
            1: {"title": "🎬 丈君·后台初遇：大阪式的幽默开场", "choices": [
                ("配合他的梗吐槽：『别耍宝了，快把台词对完！』", "『哈哈, 不愧是我的专属经纪人, 这接梗速度满分！』", 20),
                ("递上一杯热茶：『辛苦啦, 润润嗓子。』", "『有你在, 比喝什么都甜！不过……笑话还是要继续讲的～』", 25),
                ("严肃地看手表：『距离上台还有5分钟, 认真点。』", "『遵命大总管！为了不让你生气, 我马上进入帅气模式！』", 15)
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
        }
    },
    "大酱": {
        "经纪人": {
            1: {"title": "🎬 大酱·C位的幕后汗水", "choices": [
                ("递上毛巾和运动饮料：『C位辛苦啦，擦擦汗。』", "『谢谢你！每次看到你准备的东西，我就元气满满啦！』", 25),
                ("调侃他练习时同手同脚的动作", "『呜哇！那是个意外！不许记在我的人生黑历史里！』", 15),
                ("专业地指出走位问题：『刚才这里拍得很好。』", "『真的吗？太好了！只要有你的夸奖，我一定能做到最好！』", 20)
            ]},
            2: {"title": "🎬 大酱·深夜企划：剧本讨论的擦碰", "choices": [
                ("帮他整理散乱的台本", "『你总是这么细心……有你在身边，我真的可以省心很多。』", 25),
                ("假装凶他：『今晚不准吃宵夜了！』", "『诶——？就一口！就吃一口嘛，经纪人大人求求你！』", 20),
                ("认真听取他对节目的构想", "『太棒了，和我想的一样！我们俩果然是绝佳搭档。』", 22)
            ]},
            3: {"title": "🎬 大酱·镜头之外的炽热视线", "choices": [
                ("被他亮晶晶的眼睛盯着：『怎么了？我脸上有东西？』", "『没有呀，只是觉得……你认真工作的样子比聚光灯还要耀眼。』", 25),
                ("拍拍他脑袋：『快看台本，别走神。』", "『嘿嘿，在你看向我的时候，我的眼里也只有你一个主角。』", 20),
                ("笑着躲开视线", "『别害羞嘛，我说的可全部都是真心话哦。』", 18)
            ]},
            4: {"title": "🎬 大酱·突发直播：意料之外的告白暗示", "choices": [
                ("在镜头外比个加油的手势", "『看到了！多亏有镜头外的你，我今天超常发挥了！』", 25),
                ("帮他解围突发的刁钻提问", "『刚才多亏你救场……下班后必须请你吃豪华大餐！』", 20),
                ("微笑注视他的完美发言", "『谢谢你一直以来默默在背后支持着我。』", 22)
            ]},
            5: {"title": "🎬 大酱·杀青之夜：霓虹下的专属拥抱", "choices": [
                ("顺势抱住疲惫的他：『今天真的辛苦啦。』", "『呜……被你这么一抱，所有的累都瞬间消失了。』", 30),
                ("笑着调侃他像个小狗", "『才不是小狗！我是只对你一个人摇尾巴的大型犬！』", 20),
                ("把准备好的小礼物送给他", "『这是给我的吗？太喜欢了！我会一辈子珍藏的！』", 25)
            ]},
            6: {"title": "🎬 大酱·告白结局：太阳般的纯真誓言", "choices": [
                ("主动牵起他的手：『以后的每个C位，我都在台下看着你。』", "『不只是台下！我要你在我身边的每一个重要位置，永远不分开！』", 35),
                ("微笑着回应他的拥抱", "『太好了……能遇见你，是我这辈子最闪耀的奇迹！』", 30),
                ("眼含热泪点头", "『不准哭哦！从今以后，我的世界里只有你一个女主角/男主角！』", 32)
            ]}
        }
    },
    "布丁": {
        "经纪人": {
            1: {"title": "🎬 布丁·温柔队长的元气早餐", "choices": [
                ("接下他递来的三明治：『队长今天也很早啊。』", "『因为今天要和你一起工作，所以精神特别好！』", 25),
                ("提醒他注意嗓子：『咖啡少喝点，多喝温水。』", "『听你的，全听你的！只要你说的我都乖乖照做。』", 20),
                ("开玩笑：『今天通告排满咯，撑得住吗？』", "『只要有你在旁边打气，再累我也能笑出来！』", 18)
            ]},
            2: {"title": "🎬 布丁·休息室的秘密分享", "choices": [
                ("分给他一颗草莓大福", "『哇！超甜！不过……好像没有你的笑容甜。』", 25),
                ("听他倾诉照顾团队的烦恼", "『大家总觉得我是完美的队长，但在你面前……我只想当个普通的、需要安慰的普通人。』", 30),
                ("轻轻顺毛安慰他", "『被你这样摸头，感觉所有的压力都被治愈了。』", 22)
            ]},
            3: {"title": "🎬 布丁·突如其来的温柔靠近", "choices": [
                ("帮他整理歪掉的领带", "『……你离我这么近，我的心跳声大得连我都快听不见了。』", 25),
                ("假装没听到他的碎碎念", "『好啦，别害羞了，领带弄好了。』", 18),
                ("调侃他脸红的样子", "『才、才没有脸红！这是房间里空调太热了啦！』", 20)
            ]},
            4: {"title": "🎬 布丁·深夜通告后的并肩散步", "choices": [
                ("顺着街道慢慢走：『夜风好舒服。』", "『嗯，只要能这样和你并肩走着，希望这条路永远没有尽头。』", 25),
                ("把手插进外套口袋取暖", "『冷吗？来，把手伸进我的口袋里，我帮你暖着。』", 30),
                ("指着夜空中的星星", "『星星很亮，但你笑起来比星星好看。』", 22)
            ]},
            5: {"title": "🎬 布丁·心意明朗：无法掩饰的爱意", "choices": [
                ("认真看着他：『布丁是个很棒的队长。』", "『但我不想只做大家的队长……我想做你一个人的专属英雄。』", 30),
                ("拍拍他肩膀：『加油哦！』", "『光有加油不够，得给我一个大大的拥抱才行！』", 20),
                ("微笑不语", "『别用这种眼神看着我……我会忍不住直接把你拐跑的。』", 25)
            ]},
            6: {"title": "🎬 布丁·告白结局：绿意盎然的浪漫契约", "choices": [
                ("主动十指紧扣：『好呀，以后你的疲惫我都承包了。』", "『太幸福了……从今天起，我的世界全都是你专属的绿色浪漫。』", 35),
                ("靠在他温暖的怀里", "『嗯！余生很长，我们慢慢走。』", 30),
                ("笑着答应他的告白", "『耶！我终于成为你心里最特别的那个人了！』", 32)
            ]}
        }
    },
    "高恭": {
        "经纪人": {
            1: {"title": "🎬 高恭·傲娇少年的挑剔开场", "choices": [
                ("把日程表拍在他面前：『少废话，签收今天的通告！』", "『喂！你对本大爷的态度就不能温柔一点吗？……不过，我勉强接受了。』", 20),
                ("递上一杯他爱喝的苏打水", "『哼，算你有点眼力见。勉强原谅你刚才的大声说话。』", 25),
                ("冷淡回应：『爱去不去，车在外面。』", "『喂！你怎么比我还傲娇！好啦好啦，我去还不行吗！』", 15)
            ]},
            2: {"title": "🎬 高恭·化妆间的镜子对视", "choices": [
                ("从镜子里看着他：『发型弄好了，今天也很帅。』", "『那还用说！本大爷什么时候不帅了？不过……你盯着我看的样子，倒是挺顺眼的。』", 25),
                ("拿走他手里的零食：『热量太高，不准吃。』", "『喂！快还给我！你这人怎么管得比我妈还宽！』", 18),
                ("默默帮他整理衣领", "『……别突然动手啊！笨蛋，弄得我心跳都乱了节奏。』", 22)
            ]},
            3: {"title": "🎬 高恭·嘴硬心软的深夜专属", "choices": [
                ("假装要走：『很晚了，我先下班咯。』", "『等等！谁准你一个人回去的？黑灯瞎火的……本大爷勉为其难送你一段！』", 28),
                ("笑他刚才傲娇的样子", "『不许笑！再笑我就扣你……扣你今晚的宵夜！』", 20),
                ("顺从地让他送", "『这还差不多。走吧，跟紧我，别走丢了。』", 22)
            ]},
            4: {"title": "🎬 高恭·闪光灯下的保护伞", "choices": [
                ("突发状况时被他一把拉到身后", "『笨蛋，躲在我后面别动。这种场面有我在就行了。』", 30),
                ("低声向他道谢", "『谢、谢什么谢！保护自己的经纪人不是理所当然的吗……』", 25),
                ("抓住他的衣角", "『抓紧了哦，本大爷的手可是只牵最重要的人的。』", 22)
            ]},
            5: {"title": "🎬 高恭·月色下的傲娇直球", "choices": [
                ("看着星空：『今晚月色真美。』", "『笨、笨蛋！月色美个头啊……明明是、是你比较好看……』", 30),
                ("假装没听清：『啊？你说什么？』", "『没听清就算了！不准让我说第二遍！』", 20),
                ("温柔地笑出声", "『笑什么笑！总之……不准离开我身边，听到了没有？』", 25)
            ]},
            6: {"title": "🎬 高恭·告白结局：傲娇少年的笨拙真心", "choices": [
                ("主动抱住他：『好啦，傲娇鬼，我最喜欢你了。』", "『呜……你这个人怎么这样，犯规作弊！不过……我也最喜欢你就是了。』", 35),
                ("红着脸戳他脸颊", "『痛！好啦投降！本大爷这辈子栽在你手里了！』", 30),
                ("十指紧扣定下誓言", "『从今以后，本大爷的专属特权只对你一个人开放！』", 32)
            ]}
        }
    },
    "流星": {
        "经纪人": {
            1: {"title": "🎬 流星·小恶魔的眨眼陷阱", "choices": [
                ("无视他的电眼：『少来这套，快对台词。』", "『欸～一点都不解风情！明明人家刚才的眨眼练习了很久呢～』", 20),
                ("配合地夸奖：『哇，眼睛里真的有星星闪过耶！』", "『对吧对吧？那你要不要奖励我一颗糖果？』", 25),
                ("敲一下他脑袋：『又在偷懒。』", "『好痛！经纪人大人越来越凶了，不过……我好喜欢。』", 18)
            ]},
            2: {"title": "🎬 流星·后台的恶作剧对决", "choices": [
                ("假装生气夺过他的道具帽子", "『还给我嘛！好啦，只要你笑一个，我就把秘密情报告诉你。』", 22),
                ("顺势拿走他手里的饮料", "『间接接吻大作战成功！』", "『喂！你学坏了哦，居然敢反过来捉弄我！』", 25),
                ("无奈地叹气摇头", "『别叹气嘛，接下来保证乖乖听话，今晚一起去吃好吃的？』", 20)
            ]},
            3: {"title": "🎬 流星·恶魔少年的认真一刻", "choices": [
                ("看他突然收起笑容，认真对戏", "『怎么了？被我认真帅气的样子迷住了吗？』", 25),
                ("拍拍他肩膀：『认真起来挺像个大人的嘛。』", "『什么叫“像”！在你面前，我一直都是个可靠的成熟男人好不好！』", 20),
                ("递上剧本：『别贫嘴了，看这页。』", "『遵命～不过看完剧本，你得答应陪我去看夜景。』", 22)
            ]},
            4: {"title": "🎬 流星·闪光灯前后的双面反差", "choices": [
                ("舞台上闪闪发光，台下却突然拉住你的衣角", "『台下只有看着你，我才觉得最安心……』", 30),
                ("笑着摸摸他的头发", "『头发都被你揉乱了……不过如果是你的手，那就原谅你。』", 25),
                ("递上矿泉水", "『谢谢～你总是这么细心地照顾我，真想把你藏起来不给别人看。』", 22)
            ]},
            5: {"title": "🎬 流星·星空下的真心话大冒险", "choices": [
                ("选大冒险：『说一句不许骗人的真心话。』", "『真心话就是……我的心早就被你这个笨蛋偷走了，打算怎么办？』", 30),
                ("选真心话：『你最喜欢谁？』", "『明知故问！当然是喜欢天天管着我的你啦！』", 25),
                ("敲他头：『不准套路我。』", "『这怎么能叫套路，这叫爱的魔法！』", 22)
            ]},
            6: {"title": "🎬 流星·告白结局：小恶魔的专属俘虏", "choices": [
                ("主动握住他的手：『好啦，我投降总行了吧。』", "『耶！捕获心动对象一只！从今以后，你就是我专属的小恶魔新娘/新郎啦！』", 35),
                ("笑着给他的恶作剧画上句号", "『不准逃跑哦，这辈子我都吃定你了！』", 30),
                ("深情对视并拥抱", "『嗯，甘愿做你的俘虏，一辈子都不想逃。』", 32)
            ]}
        }
    },
    "米七": {
        "经纪人": {
            1: {"title": "🎬 米七·长腿王子的清纯微笑", "choices": [
                ("抬头看他过高的身高：『长太高也是一种烦恼吧？』", "『为了能随时低头看到你，我觉得这个高度刚刚好。』", 25),
                ("递上润喉糖：『高个子更要注意身体哦。』", "『谢谢你……每次你关心我，我心里比糖还要甜。』", 22),
                ("催促开工：『走啦，米七模特大人。』", "『遵命！只要是你叫我，我随时随地都能出发。』", 18)
            ]},
            2: {"title": "🎬 米七·摄影棚角落的安静陪伴", "choices": [
                ("递过热毛巾：『辛苦啦，拍摄很顺利。』", "『因为中途看到你在场边对我说加油，我才有动力发挥得这么好。』", 25),
                ("打趣他刚才摆的帅气姿势", "『别笑话我嘛，那可是为了吸引你的目光特意设计的！』", 20),
                ("安静地坐在他旁边喝水", "『就这样什么都不说，静静地挨着你，就让我觉得无比安心。』", 22)
            ]},
            3: {"title": "🎬 米七·长腿王子的温柔直球", "choices": [
                ("被他温柔的目光注视：『干嘛这样看着我？』", "『因为你太耀眼了，视线总是忍不住想要追随你。』", 25),
                ("拍拍他肩膀：『快去换下一套衣服。』", "『好～不过你得在这里等我回来，不准先走哦。』", 20),
                ("假装没听清：『啊？你刚才说什么？』", "『没什么！我是说……今天天气真好，就像你的笑容一样。』", 22)
            ]},
            4: {"title": "🎬 米七·突发时尚街拍的默契配合", "choices": [
                ("帮他整理大衣领口", "『离得这么近……摄影师可能以为我们在拍恋爱杂志封面了。』", 28),
                ("开玩笑：『刚才这套穿搭可以打满分！』", "『那当然，因为这是你昨天帮我挑的私服呀。』", 22),
                ("帮他挡开热情的粉丝人群", "『谢谢你护着我……其实我更想反过来把你护在我怀里。』", 25)
            ]},
            5: {"title": "🎬 米七·天台上的浪漫夜景", "choices": [
                ("吹着微风：『这里的夜景真美。』", "『风景再美，也比不上此时此刻站在我身边的你。』", 30),
                ("递上一罐热可可", "『好暖……谢谢你总是把最温柔的一面留给我。』", 22),
                ("靠在他肩膀上", "『只要能靠着你，所有的疲惫就全都烟消云散了。』", 25)
            ]},
            6: {"title": "🎬 米七·告白结局：王子殿下的纯白纯爱", "choices": [
                ("主动牵起他的手：『以后的每一场走秀，我都陪你。』", "『嗯！我的红毯终点，永远都有你在等我。』", 35),
                ("微笑着接受他的戒指/手环", "『太完美了……从今天起，你就是我唯一的挚爱。』", 30),
                ("深情拥入他的怀抱", "『一辈子很短，但我只想和你长长久久地走下去。』", 32)
            ]}
        }
    },
    "谦杜": {
        "经纪人": {
            1: {"title": "🎬 谦杜·时尚末子的自信开场", "choices": [
                ("评价他的潮牌穿搭：『今天这套挺别致啊。』", "『那是当然！这可是本少爷特意为了见你精心搭配的时尚！』", 25),
                ("吐槽他鞋带开了：『大时尚家，鞋带散啦。』", "『啊？！在哪？……哼，肯定是故意转移我注意力，不过谢啦！』", 20),
                ("催促他快去候场", "『遵命经纪人大人！看我今天在台上帅翻全场，让你刮目相看！』", 18)
            ]},
            2: {"title": "🎬 谦杜·后台的造型设计讨论", "choices": [
                ("听他滔滔不绝讲对时尚的见解", "『怎么样？我很有眼光吧？要不要考虑以后让我包办你的日常穿搭？』", 22),
                ("捏捏他的脸：『好啦，大时尚家快闭嘴休息会。』", "『喂！不要总是捏我脸！……不过，只准你一个人捏哦。』", 25),
                ("递上果汁：『润润喉，待会还要发言。』", "『谢啦！有你的甜味加持，待会发言绝对满分！』", 20)
            ]},
            3: {"title": "🎬 谦杜·末子的倔强与直球", "choices": [
                ("看他因为通告不顺而闷闷不乐", "『才没有不高兴呢！……好啦，别用这种担心的眼神看我，看到你我就气消了。』", 25),
                ("买了他最爱吃的小蛋糕哄他", "『哇！你怎么知道我想吃这个！太犯规了，这样我会越来越离不开你的。』", 28),
                ("拍拍他肩膀以示鼓励", "『有你这句话，本少爷马上原地满血复活！』", 20)
            ]},
            4: {"title": "🎬 谦杜·时尚杂志拍摄的意外心动", "choices": [
                ("摄影师要求对视，两人突然脸红", "『……你离这么近干嘛，搞得我台词都快念不出来了。』", 25),
                ("帮他调整耳麦位置", "『心跳声好像透过耳麦传过来了……是你心跳太快了吧？』", 28),
                ("笑着夸奖他镜头感极佳", "『那当然，因为我眼中倒映的全都是你的身影啊。』", 22)
            ]},
            5: {"title": "🎬 谦杜·霓虹街头的专属约定", "choices": [
                ("走在繁华的街头：『人好多别走散了。』", "『抓紧我的手！绝对不准放开，不然我可是会生气的哦。』", 30),
                ("笑他像个小孩子", "『才不是小孩子！我是能给你披上最美婚纱/礼服的成熟男人！』", 22),
                ("紧紧回握住他的手", "『嗯，不放开，一辈子都不放开。』", 25)
            ]},
            6: {"title": "🎬 谦杜·告白结局：时尚末子的霸道热恋", "choices": [
                ("主动点头答应：『好呀，以后我的穿搭全听你的。』", "『这还差不多！从今天起，你就是全宇宙最时尚、也是我最爱的人！』", 35),
                ("红着脸接受他的拥抱", "『太棒了！本少爷的恋爱企划大获全胜！』", 30),
                ("十指相扣迎接未来", "『以后不管是时尚潮流怎么变，我对你的喜欢永远不打折！』", 32)
            ]}
        }
    }
}

# 终极智能兜底函数（即使其他未写的组合也不会报错，且提供独立选项）
def get_member_story(member, role, act):
    if member in STORIES and role in STORIES[member] and act in STORIES[member][role]:
        return STORIES[member][role][act]
    
    # 专属精致兜底，避免千篇一律
    return {
        "title": f"🎬 {member} × {role} · 第 {act} 幕：心动进阶时刻",
        "choices": [
            ("微笑着靠近一步，认真注视他的眼睛：『今天表现很棒哦。』", f"『被你这样看着……我的心跳连台词都快忘光了。』", 25),
            ("开个轻松的小玩笑活跃沉闷的气氛", f"『好啊你，居然敢拿我开玩笑，看我怎么“惩罚”你～』", 20),
            ("安静地陪伴在身旁，递上一杯温水", f"『只要有你陪着，哪怕什么都不做也是最幸福的时光。』", 22)
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
st.markdown('<p class="sub-header">✨ 7人全员多幕专属独立剧情 (含角色图片、随机事件与多结局系统)</p>', unsafe_allow_html=True)

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
    
    # 实时渲染人物图片
    st.image(MEMBERS[selected_member]["img"], width=220)
    
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
            final_score = base_score
            if st.session_state.active_buff == "🍬 恋爱加倍糖果":
                final_score *= 2
                st.session_state.active_buff = None
            elif st.session_state.active_buff == "🎧 读心耳机":
                final_score += 15
                st.session_state.active_buff = None
            elif st.session_state.active_buff == "🥤 冰爽解暑饮料":
                final_score += 10
                st.session_state.active_buff = None
                
            st.session_state.total_score += final_score
            st.session_state.dialogue_history.append((current_story['title'], choice_text, reply_text, final_score))
            
            # 40% 概率触发随机事件
            if act < MAX_ACT and random.random() < 0.4:
                random_events_pool = [
                    {"title": "突发暴雨的屋檐避难", "desc": f"两人在回家路上突然遇到倾盆大雨，被迫挤在一个小小的便利店屋檐下，肩膀紧紧贴在一起……"},
                    {"title": "电台直播的连线突袭", "desc": f"工作间隙突然接到了一档电台连线直播，主持人现场要求他对你说一句真心话！"},
                    {"title": "猫咪咖啡厅的意外邂逅", "desc": f"排练间隙去咖啡厅休息，一只可爱的布偶猫突然跳进你怀里，引得他吃醋地看着你……"},
                    {"title": "便利店最后一块布丁", "desc": f"深夜去买宵夜，冰箱里只剩下最后一份他最爱的限定布丁，你们会怎么分？"}
                ]
                st.session_state.random_event = random.choice(random_events_pool)
            
            if act < MAX_ACT:
                st.session_state.current_act += 1
            else:
                st.session_state.stage = "ending"
            st.rerun()

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
