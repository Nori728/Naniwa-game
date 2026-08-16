import streamlit as st

# ==================== 1. 页面配置与 CSS 动画 ====================
st.set_page_config(page_title="偶像乙女游戏", page_icon="💖", layout="centered")

# ==================== 2. 全局背景音乐 (BGM) ====================
st.audio("audio/bgm.mp3", autoplay=True, loop=True)

# ==================== 3. 成员定义与状态初始化 ====================
MEMBERS = ["丈君", "大酱", "布丁", "高恭", "流星", "米七", "谦杜"]

if "step" not in st.session_state:
    st.session_state.step = 0
if "affection" not in st.session_state:
    st.session_state.affection = {m: 0 for m in MEMBERS}
if "current_dialogue" not in st.session_state:
    st.session_state.current_dialogue = ""
if "current_img" not in st.session_state:
    st.session_state.current_img = ""
if "player_role" not in st.session_state:
    st.session_state.player_role = ""

# 结算立绘图片映射表
MEMBER_IMAGES = {
    "丈君": "images/zhang_jun.gif",
    "大酱": "images/da_jiang.gif",
    "布丁": "images/bu_ding.gif",
    "高恭": "images/gao_gong.gif",
    "流星": "images/liu_xing.gif",
    "米七": "images/mi_qi.gif",
    "谦杜": "images/qian_du.gif"
}

# ==================== 4. 剧情数据库 (4身份 x 7人 x 5幕) ====================
# 结构：(选项文本, 角色台词, 场景专属图片路径)
STORY_DATA = {
    "经纪人": {
        1: {
            "title": "🎬 第一幕：后台行程与考勤Check",
            "opts": {
                "丈君": ("确认走位：『核对一下待会儿的走位和麦克风。』", "『有你这个金牌经纪人在，我完全不担心！』", "images/manager_act1_zhang.gif"),
                "大酱": ("递上行程表：『等下的联访流程看过了吗？』", "『看过了！放心，我回答绝对得体！』", "images/manager_act1_da.gif"),
                "布丁": ("检查服装：『服装领结稍微偏了，我帮你整整。』", "『嘿嘿，谢谢你～多亏你这么细心！』", "images/manager_act1_buding.gif"),
                "高恭": ("确认状态：『嗓子怎么样？要不要喝润喉茶？』", "『刚刚好，听到你的声音我就踏实了。』", "images/manager_act1_gaogong.gif"),
                "流星": ("提醒走位：『等下第 3 首歌记得从升降台走。』", "『收到！我会用最帅的姿势上台的！』", "images/manager_act1_liuxing.gif"),
                "米七": ("沟通休息时间：『再等 10 分钟就可以休息了。』", "『没关系，只要能看着你忙碌就很满足。』", "images/manager_act1_miqi.gif"),
                "谦杜": ("调试器材：『吉他音轨我已经和音响师对接好了。』", "『太靠谱了！待会的第一音符为你而弹！』", "images/manager_act1_qiandu.gif")
            }
        },
        2: {
            "title": "🎬 第二幕：舞台中场紧急应变",
            "opts": {
                "丈君": ("递上毛巾：『中场休息只有 3 分钟，快补水！』", "『呼……幸好有你在台侧接住我！』", "images/manager_act2_zhang.gif"),
                "大酱": ("帮忙换装：『外套袖口有点卡，我拉开一下。』", "『离我这么近……我会心跳加速打乱呼吸的。』", "images/manager_act2_da.gif"),
                "布丁": ("递上能量棒：『吃一口补充血糖！』", "『好甜！感觉又有体力在台上蹦蹦跳跳了！』", "images/manager_act2_buding.gif"),
                "高恭": ("拭去汗水：『跳得太卖力了，别脱水。』", "『有你照顾我，这点累根本不算什么。』", "images/manager_act2_gaogong.gif"),
                "流星": ("打气加油：『刚才的舞段引爆全场了！』", "『那是当然！因为我的眼光一直在你身上！』", "images/manager_act2_liuxing.gif"),
                "米七": ("递上冰镇饮料：『凉一下降降温。』", "『谢谢……手贴在一起的温度比饮料还冰呢。』", "images/manager_act2_miqi.gif"),
                "谦杜": ("调整耳返：『听得清伴奏吗？』", "『耳返里最清晰的，始终是你叮嘱我的声音。』", "images/manager_act2_qiandu.gif")
            }
        },
        3: {
            "title": "🎬 第三幕：演出成功后的发布会后台",
            "opts": {
                "丈君": ("递上答记问提纲：『记者提问别紧张。』", "『只要你在镜头后陪着我，我就能对答如流。』", "images/manager_act3_zhang.gif"),
                "大酱": ("赞许微笑了：『今天表现给满分！』", "『得到你的夸奖，比拿大奖还开心！』", "images/manager_act3_da.gif"),
                "布丁": ("做偷偷打气手势：『等下采访结束吃大餐！』", "『好耶！我要坐在你旁边吃！』", "images/manager_act3_buding.gif"),
                "高恭": ("整理发型：『碎发理一下，上镜更好看。』", "『嗯……你想怎么理都听你的。』", "images/manager_act3_gaogong.gif"),
                "流星": ("比赞：『刚才临场反应太棒了！』", "『全靠你平时训练有方嘛！夸我不如多陪我聊会～』", "images/manager_act3_liuxing.gif"),
                "米七": ("轻声提醒：『累的话眼神可以少看镜头。』", "『那我只看着你，可以吗？』", "images/manager_act3_miqi.gif"),
                "谦杜": ("递上手帕：『记者问完就去休息。』", "『嗯，等结束了我有话想单独对你说。』", "images/manager_act3_qiandu.gif")
            }
        },
        4: {
            "title": "🎬 第四幕：深夜庆功宴后的专车上",
            "opts": {
                "丈君": ("调低空调：『别吹风感冒了。』", "『今晚别把我当明星，只当普通男孩子好吗？』", "images/manager_act4_zhang.gif"),
                "大酱": ("肩靠肩坐着：『累了就闭眼眯会儿。』", "『你的肩膀比任何枕头都要让人安心。』", "images/manager_act4_da.gif"),
                "布丁": ("递上热饮：『暖暖胃再睡。』", "『今天辛苦你陪我们跑一天了，快喝一口。』", "images/manager_act4_buding.gif"),
                "高恭": ("看着车窗外的夜景：『明天有一整天假。』", "『那明天……能把时间私心留给我吗？』", "images/manager_act4_gaogong.gif"),
                "流星": ("分享耳机：『听听今天的现场音频吧。』", "『这首歌我的高音，是想着你才唱出来的。』", "images/manager_act4_liuxing.gif"),
                "米七": ("牵起你的手：『今天太忙，都没怎么好好说话。』", "『别抽开手……就让我握一会儿就好。』", "images/manager_act4_miqi.gif"),
                "谦杜": ("侧头看你：『辛苦你了，经纪人小姐。』", "『比起经纪人，我更想听你只叫我的名字。』", "images/manager_act4_qiandu.gif")
            }
        },
        5: {
            "title": "🎬 第五幕：清晨事务所的清晨告白",
            "opts": {
                "丈君": ("走向丈君：『早安，今天也要一起加油！』", "『以后不只是工作，你的余生我也想一起加油！』", "images/manager_act5_zhang.gif"),
                "大酱": ("走向大酱：『这是今天的行程安排。』", "『相比行程，我更关心我的心什么时候能住进你心里。』", "images/manager_act5_da.gif"),
                "布丁": ("走向布丁：『早安！给你带了早餐。』", "『以后每天的早餐，我都想跟你一起吃！』", "images/manager_act5_buding.gif"),
                "高恭": ("走向高恭：『昨晚睡得好吗？』", "『梦里全是你，你说我睡得好不好？』", "images/manager_act5_gaogong.gif"),
                "流星": ("走向流星：『今天有新歌录制哦。』", "『我想写一首只属于我们俩的情感！』", "images/manager_act5_liuxing.gif"),
                "米七": ("走向米七：『早安，看起来精神不错。』", "『因为一想到早起能见到你，我就睡不着了。』", "images/manager_act5_miqi.gif"),
                "谦杜": ("走向谦杜：『准备好开启新一天了吗？』", "『只要你在我身边，每一天都是最美好的开端。』", "images/manager_act5_qiandu.gif")
            }
        }
    },
    "粉丝/地下恋": {
        1: {
            "title": "🎬 第一幕：后台休息室的秘密碰面",
            "opts": {
                "丈君": ("悄悄递手幅：『只属于你的独家应援！』", "『嘘……被看到就糟糕了，但你能来我超开心！』", "images/fan_act1_zhang.gif"),
                "大酱": ("塞私房零食：『辛苦啦，偷偷给你带的。』", "『只有你还记得我最爱吃这个，真想抱抱你。』", "images/fan_act1_da.gif"),
                "布丁": ("拿出周边请他签名：『能帮我签在这个位置吗？』", "『签这里不够，我想在你的心上盖个章！』", "images/fan_act1_buding.gif"),
                "高恭": ("戴着帽子低头过去：『没被狗仔发现吧？』", "『放心，我安排了工作人员避开镜头，快坐下。』", "images/fan_act1_gaogong.gif"),
                "流星": ("拉拉衣服：『今天的舞台造型太帅了！』", "『是吗？那为了你，我待会台上再帅一点！』", "images/fan_act1_liuxing.gif"),
                "米七": ("角落小声说话：『后台人好多，好紧张。』", "『握住我的手就不紧张了，别松开哦。』", "images/fan_act1_miqi.gif"),
                "谦杜": ("递上手写信：『给你的信，回家再看。』", "『我现在就想看，因为里面一定写满了爱意！』", "images/fan_act1_qiandu.gif")
            }
        },
        2: {
            "title": "🎬 第二幕：观众席与舞台的暗号交流",
            "opts": {
                "丈君": ("举起专属灯牌：『我在第一排看着你！』", "『台上看到你的那一刻，我整个人都亮起来了！』", "images/fan_act2_zhang.gif"),
                "大酱": ("比心互动：『接住我的爱心！』", "『在台上接收到了！我也暗搓搓比了个心给你！』", "images/fan_act2_da.gif"),
                "布丁": ("挥舞应援棒：『跟着节奏晃动。』", "『你的应援棒晃得最可爱，我一眼就认出来了！』", "images/fan_act2_buding.gif"),
                "高恭": ("眼神锁死舞台：『专注地看着他唱深情歌。』", "『刚才那句台词，我完全是看着你的眼睛唱的。』", "images/fan_act2_gaogong.gif"),
                "流星": ("尖叫欢呼：『流星最棒啦！』", "『听到你的声音了！今晚我是你一个人的偶像！』", "images/fan_act2_liuxing.gif"),
                "米七": ("温情凝视：『默默在台下为你加油。』", "『有你在台下，这片星海才有了意义。』", "images/fan_act2_miqi.gif"),
                "谦杜": ("弹吉他指台下：『他在 Solo 时指向了你。』", "『那个动作是只属于我们俩的秘密暗号！』", "images/fan_act2_qiandu.gif")
            }
        },
        3: {
            "title": "🎬 第三幕：退场通道的闪躲与拥抱",
            "opts": {
                "丈君": ("躲在通道阴影里：『演出太成功啦！』", "『（一把抱住你）让我抱一秒，充充电……』", "images/fan_act3_zhang.gif"),
                "大酱": ("递上湿纸巾：『擦擦汗，别着凉。』", "『真想公开我们的关系，再也不用躲躲藏藏。』", "images/fan_act3_da.gif"),
                "布丁": ("塞入口香糖：『辛苦啦！』", "『跟你在后台悄悄约会，感觉像偷吃糖果一样甜！』", "images/fan_act3_buding.gif"),
                "高恭": ("把鸭舌帽按低：『警卫走过来了！』", "『别怕，我把你挡在怀里，谁也看不到。』", "images/fan_act3_gaogong.gif"),
                "流星": ("击掌庆祝：『今晚你帅爆了！』", "『击掌变扣指！今晚去我家续杯甜言蜜语？』", "images/fan_act3_liuxing.gif"),
                "米七": ("小声告别：『我要先回观众席了。』", "『别走……再陪我待三分钟，就三分钟。』", "images/fan_act3_miqi.gif"),
                "谦杜": ("披上他的外套：『别被路人认出来。』", "『外套上有我的香水味，就像我一直在陪着你。』", "images/fan_act3_qiandu.gif")
            }
        },
        4: {
            "title": "🎬 第四幕：深夜私人公寓的秘密约会",
            "opts": {
                "丈君": ("开门迎他：『外面没有记者吧？』", "『没有！终于能卸下所有伪装，好好拥抱你了。』", "images/fan_act4_zhang.gif"),
                "大酱": ("倒一杯热牛奶：『今天辛苦了。』", "『只要能回到有你的房间，再累都烟消云散了。』", "images/fan_act4_da.gif"),
                "布丁": ("一起窝在沙发：『要看今天的演唱会回放吗？』", "『不看电视，我只想看着你的脸。』", "images/fan_act4_buding.gif"),
                "高恭": ("帮他摘下口罩：『辛苦了，我的明星先生。』", "『在你面前，我只是那个深深爱着你的普通男人。』", "images/fan_act4_gaogong.gif"),
                "流星": ("递上拖鞋：『快进来吧。』", "『回家真好！最喜欢你在这个家等我的样子。』", "images/fan_act4_liuxing.gif"),
                "米七": ("靠在他肩膀上：『今天看到万人为你欢呼呢。』", "『万人的欢呼，也抵不过你一句温柔的问候。』", "images/fan_act4_miqi.gif"),
                "谦杜": ("拿吉他弹奏：『能弹一首专属于我的歌吗？』", "『遵命，我的专属听众，只为你一个人演奏。』", "images/fan_act4_qiandu.gif")
            }
        },
        5: {
            "title": "🎬 第五幕：黎明前的浪漫誓言",
            "opts": {
                "丈君": ("走向丈君：『天快亮了，要准备回去了吗？』", "『总有一天，我要在万人面前牵起你的手！』", "images/fan_act5_zhang.gif"),
                "大酱": ("走向大酱：『帮你把帽子戴好。』", "『等我登顶的那一天，我们就向全世界公开！』", "images/fan_act5_da.gif"),
                "布丁": ("走向布丁：『下次什么时候能再见？』", "『很快！只要你想我，我随时飞奔来见你！』", "images/fan_act5_buding.gif"),
                "高恭": ("走向高恭：『注意安全，路上小心。』", "『我的心留在这里了，你一定要替我保管好。』", "images/fan_act5_gaogong.gif"),
                "流星": ("走向流星：『在台上也要想我哦。』", "『放心！我的每一个笑容，都是给你看的！』", "images/fan_act5_liuxing.gif"),
                "米七": ("走向米七：『我会一直当你的头号粉丝。』", "『比起头号粉丝，我更想让你当我的终生伴侣。』", "images/fan_act5_miqi.gif"),
                "谦杜": ("走向谦杜：『期待你写的新歌。』", "『每一首歌的灵感都是你，你就是我的缪斯。』", "images/fan_act5_qiandu.gif")
            }
        }
    },
    "青梅竹马": {
        1: {
            "title": "🎬 第一幕：熟悉的家常便当盒",
            "opts": {
                "丈君": ("递上便当：『阿姨让我带给你的蛋包饭。』", "『哇！还是小时候的味道，有你在真好！』", "images/child_act1_zhang.gif"),
                "大酱": ("拿毛巾揉他头发：『又不好好擦头发。』", "『嘿嘿，小时候你不就经常这样帮我擦嘛～』", "images/child_act1_da.gif"),
                "布丁": ("递上布丁：『还记得你小时候最爱吃这个。』", "『一点都没变！你还是最懂我口味的人！』", "images/child_act1_buding.gif"),
                "高恭": ("帮他理领带：『从小到大笨手笨脚的。』", "『反正有你帮我整理，我就懒得学会啦！』", "images/child_act1_gaogong.gif"),
                "流星": ("打趣聊天：『小不点居然真的当大明星了。』", "『什么小不点！我现在比你高多了好吗！』", "images/child_act1_liuxing.gif"),
                "米七": ("递上热麦茶：『家里带的，快喝点。』", "『还是你带的水最合我胃口，谢谢你啊。』", "images/child_act1_miqi.gif"),
                "谦杜": ("拿照片调侃：『我这里还有你小时候黑历史照片哦。』", "『快收起来！万一被团员看到我形象就全毁啦！』", "images/child_act1_qiandu.gif")
            }
        },
        2: {
            "title": "🎬 第二幕：儿时回忆与舞台蜕变",
            "opts": {
                "丈君": ("指着舞台：『没想到你站在上面这么亮眼。』", "『以前在公园表演给你的情景，你还记得吗？』", "images/child_act2_zhang.gif"),
                "大酱": ("递上润喉糖：『小时候你唱歌嗓子哑了也是吃这个。』", "『对啊，每次我生病都是你守护在我身边。』", "images/child_act2_da.gif"),
                "布丁": ("分享小零食：『小时候我们俩总抢这个吃。』", "『这次我不跟你抢了，全都留给你吃！』", "images/child_act2_buding.gif"),
                "高恭": ("看着台上的他：『真的长成很可靠的大人了呢。』", "『可是在你面前，我依然是那个想依赖你的少年。』", "images/child_act2_gaogong.gif"),
                "流星": ("拍拍他肩膀：『帅气程度快赶上当年邻家大哥了。』", "『什么邻家大哥，我现在只想做你的唯一选择！』", "images/child_act2_liuxing.gif"),
                "米七": ("温情微笑：『阿姨在家里也在看直播呢。』", "『那她有没有问起，我什么时候带你回家？』", "images/child_act2_miqi.gif"),
                "谦杜": ("拿旧吉他挑弹：『这把吉他跟小时候那把好像。』", "『当年为你弹的第一首歌，我现在还能背出来。』", "images/child_act2_qiandu.gif")
            }
        },
        3: {
            "title": "🎬 第三幕：后台休息室的怀念时光",
            "opts": {
                "丈君": ("并排坐在沙发上：『今天很累吧？』", "『只要能跟你聊聊天，疲惫瞬间就没了。』", "images/child_act3_zhang.gif"),
                "大酱": ("拿热敷贴给他：『肩膀又酸了吗？』", "『还是你贴得最到位，从小到大都没变。』", "images/child_act3_da.gif"),
                "布丁": ("分一块蛋糕：『尝尝这个新口味。』", "『好甜！跟你小时候给我做的一模一样！』", "images/child_act3_buding.gif"),
                "高恭": ("帮你倒水：『倒是我在被你照顾呢。』", "『因为我早就发誓，长大后换我来照顾你。』", "images/child_act3_gaogong.gif"),
                "流星": ("比划身高：『确实比小时候高不少。』", "『那当然！现在的我，足够为你遮风挡雨了！』", "images/child_act3_liuxing.gif"),
                "米七": ("帮你拉好外套：『别吹后台的冷气。』", "『你对我这么好，就不怕我这辈子离不开你吗？』", "images/child_act3_miqi.gif"),
                "谦杜": ("哼哼旧童谣：『还记得这首歌吗？』", "『记得！那是我们童年最美好的旋律。』", "images/child_act3_qiandu.gif")
            }
        },
        4: {
            "title": "🎬 第四幕：回家路上的晚风漫步",
            "opts": {
                "丈君": ("走在熟悉的小路上：『跟小时候一模一样。』", "『唯一不同的是，我现在想牵着你的手走下去。』", "images/child_act4_zhang.gif"),
                "大酱": ("指着路灯：『当年我们在这里捉过萤火虫。』", "『现在的我，只想把最亮的光芒献给你。』", "images/child_act4_da.gif"),
                "布丁": ("买路边热热的烤红薯：『分你一半！』", "『好香！还是跟你一起吃东西最开心了！』", "images/child_act4_buding.gif"),
                "高恭": ("为你挡去迎面来的自行车：『小心！』", "『（拉住你）从小你就慌慌张张的，没我不行吧？』", "images/child_act4_gaogong.gif"),
                "流星": ("小跑起来：『来比比谁先跑到巷子口！』", "『输的人要答应赢的人一个要求！不许耍赖！』", "images/child_act4_liuxing.gif"),
                "米七": ("看着漫天繁星：『今晚的夜空真美。』", "『相比星空，我更喜欢侧头看着你微笑的样子。』", "images/child_act4_miqi.gif"),
                "谦杜": ("轻轻扣住你的手：『风有点大呢。』", "『手太冷了……就这样让我握着暖一暖吧。』", "images/child_act4_qiandu.gif")
            }
        },
        5: {
            "title": "🎬 第五幕：家门口的温情心声",
            "opts": {
                "丈君": ("走向丈君：『到家啦，快进去吧。』", "『我们认识这么多年了，以后……能换个身份陪伴吗？』", "images/child_act5_zhang.gif"),
                "大酱": ("走向大酱：『阿姨还在等你吃饭呢。』", "『比起吃饭，我更想先听听你的心意。』", "images/child_act5_da.gif"),
                "布丁": ("走向布丁：『明天见啦！』", "『不要明天见，我现在就想跟你一直在一起！』", "images/child_act5_buding.gif"),
                "高恭": ("走向高恭：『晚安，做个好梦。』", "『有你的梦，一定全是甜甜的浪漫。』", "images/child_act5_gaogong.gif"),
                "流星": ("走向流星：『明天还要早起跑行程呢。』", "『知道啦！但你必须答应我，明天第一眼要看到我！』", "images/child_act5_liuxing.gif"),
                "米七": ("走向米七：『快回去休息吧。』", "『陪伴了我整个童年的你，愿意陪伴我的余生吗？』", "images/child_act5_miqi.gif"),
                "谦杜": ("走向谦杜：『今天很开心，谢谢你。』", "『谢什么！我们之间，早就不分彼此了。』", "images/child_act5_qiandu.gif")
            }
        }
    },
    "在日留学生or打工人": {
        1: {
            "title": "🎬 第一幕：后台兼职打工的意外偶遇",
            "opts": {
                "丈君": ("递上翻译资料：『今天的现场日语台词我已经翻译好了。』", "『日语进步神速啊！有你在后台沟通顺畅多了！』", "images/worker_act1_zhang.gif"),
                "大酱": ("帮忙整理道具箱：『打工人加油！』", "『辛苦你了！等兼职结束我请你吃拉面！』", "images/worker_act1_da.gif"),
                "布丁": ("送上快餐盒饭：『打工人的午餐到了。』", "『哇！你帮我领的这份看起来最好吃！』", "images/worker_act1_buding.gif"),
                "高恭": ("递上打工签到表：『请在这里签字。』", "『签好了。异国打拼很辛苦吧？有困难随时找我。』", "images/worker_act1_gaogong.gif"),
                "流星": ("帮忙搬运音响：『放着我来吧！』", "『怎么能让女孩子搬重物！快放下我来！』", "images/worker_act1_liuxing.gif"),
                "米七": ("用中文打招呼：『你好，辛苦啦！』", "『（惊讶）中文！为了你我也有在好好学中文哦！』", "images/worker_act1_miqi.gif"),
                "谦杜": ("拿水问候：『打工累了吗？』", "『不累！看到你们在舞台上闪闪发光，我也充满能量！』", "images/worker_act1_qiandu.gif")
            }
        },
        2: {
            "title": "🎬 第二幕：异国文化与语言的交流",
            "opts": {
                "丈君": ("教他一句中文：『试试用中文跟粉丝打招呼？』", "『“我爱你”是这么发音的对吗？我想对你一个人说。』", "images/worker_act2_zhang.gif"),
                "大酱": ("分享家乡零食：『尝尝我们家乡特产！』", "『好吃！以后去你的家乡，你一定要当我的导游！』", "images/worker_act2_da.gif"),
                "布丁": ("聊异国生活：『刚来日本时经常迷路呢。』", "『以后你想去哪，我都当你的专属导航！』", "images/worker_act2_buding.gif"),
                "高恭": ("关心学业打工：『兼职和学习能兼顾吗？』", "『别太拼了，要是累坏了我可是会心疼的。』", "images/worker_act2_gaogong.gif"),
                "流星": ("做趣味口音对比：『我的日语口音可爱吗？』", "『超可爱！每次听你说话我都想摸摸你的头！』", "images/worker_act2_liuxing.gif"),
                "米七": ("交流家乡文化：『我们家乡也有很美的风景。』", "『真想有一天，能跟你一起去你的家乡看看。』", "images/worker_act2_miqi.gif"),
                "谦杜": ("用中文唱流行歌：『哼唱一段中文旋律。』", "『声音真好听！能教教我这首歌怎么唱吗？』", "images/worker_act2_qiandu.gif")
            }
        },
        3: {
            "title": "🎬 第三幕：后台休息室的互相疗愈",
            "opts": {
                "丈君": ("递上温热的茶水：『独自在异国打拼辛苦了。』", "『你也是啊！我们都在为了梦想努力，一起加油！』", "images/worker_act3_zhang.gif"),
                "大酱": ("帮他拿创可贴：『舞蹈动作练习受伤了吗？』", "『一点小伤，但你给我贴上后就不痛了。』", "images/worker_act3_da.gif"),
                "布丁": ("分享打工趣事：『今天遇到了很有趣的客人。』", "『哈哈！听你说话心情总能变得特别好！』", "images/worker_act3_buding.gif"),
                "高恭": ("递上日语学习笔记：『这个语法不太懂。』", "『过来坐下，我手把手教你怎么用。』", "images/worker_act3_gaogong.gif"),
                "流星": ("比划打工动作：『今天搬了一下午箱子。』", "『辛苦啦！来，我的手臂借你当靠枕！』", "images/worker_act3_liuxing.gif"),
                "米七": ("互相加油鼓劲：『我们都要成为更好的人。』", "『有你的鼓励，我觉得自己能征服全世界！』", "images/worker_act3_miqi.gif"),
                "谦杜": ("拿吉他轻弹：『为你弹一首疗愈的曲子。』", "『希望这首曲子，能治愈你在异国他乡的所有孤独。』", "images/worker_act3_qiandu.gif")
            }
        },
        4: {
            "title": "🎬 第四幕：打工结束后的电车站台",
            "opts": {
                "丈君": ("并排等电车：『末班车快来了。』", "『真希望这趟电车永远不要来，能多陪你一会儿。』", "images/worker_act4_zhang.gif"),
                "大酱": ("买自动贩卖机饮料：『热可可给你。』", "『握着热可可，感觉整个冬天都不冷了。』", "images/worker_act4_da.gif"),
                "布丁": ("看着电车进站：『今天打工很充实！』", "『跟你在一起的时间，才是我一天中最充实的时刻。』", "images/worker_act4_buding.gif"),
                "高恭": ("挡住风口：『站台风大，往我身后站。』", "『异国他乡很冷，但我的怀抱随时为你敞开。』", "images/worker_act4_gaogong.gif"),
                "流星": ("挥手道别：『明天我还有课呢。』", "『那上完课……能来我的练习室看我吗？』", "images/worker_act4_liuxing.gif"),
                "米七": ("轻轻拉住你的衣角：『车来了……』", "『（小声）明天……还能在后台看到你吗？』", "images/worker_act4_miqi.gif"),
                "谦杜": ("戴着耳机分享音乐：『听听看这首新曲。』", "『写这首歌的时候，心里全是你站在台侧的样子。』", "images/worker_act4_qiandu.gif")
            }
        },
        5: {
            "title": "🎬 第五幕：东京塔夜景下的温暖拥抱",
            "opts": {
                "丈君": ("走向丈君：『东京的夜景真美啊。』", "『在这个陌生的城市里，你就是我最想珍惜的风景。』", "images/worker_act5_zhang.gif"),
                "大酱": ("走向大酱：『谢谢你一直照顾我这个留学生。』", "『不是照顾，是我发自内心想靠近你、守护你。』", "images/worker_act5_da.gif"),
                "布丁": ("走向布丁：『打工能遇到你，真是太幸运了。』", "『遇到你也是我这辈子最大的幸运！』", "images/worker_act5_buding.gif"),
                "高恭": ("走向高恭：『异国生活因为你变得温暖了。』", "『以后你的每一个四季，我都想陪你一起度过。』", "images/worker_act5_gaogong.gif"),
                "流星": ("走向流星：『今天也要梦想成真哦！』", "『我的梦想里，必须要有你才算完美！』", "images/worker_act5_liuxing.gif"),
                "米七": ("走向米七：『谢谢你带给我的温暖。』", "『这份温暖是相互的，你早已成为了我的避风港。』", "images/worker_act5_miqi.gif"),
                "谦杜": ("走向谦杜：『音乐跨越了语言的界限呢。』", "『爱意也是，无论来自哪里，我的心都为你跳动。』", "images/worker_act5_qiandu.gif")
            }
        }
    }
}

# ==================== 核心渲染引擎 ====================
def render_choice_step(role_name, act_num, next_step):
    """渲染选项幕（支持传入不同场景图片）"""
    act_data = STORY_DATA[role_name][act_num]
    st.subheader(act_data["title"])
    st.write(f"（当前身份：【{role_name}】）")

    for member in MEMBERS:
        # 解包 3 个变量：选项文字, 角色台词, 场景图片路径
        btn_text, dialogue, scene_img = act_data["opts"][member]
        if st.button(f"走向 {member}：{btn_text}"):
            st.session_state.affection[member] += 15
            st.session_state.current_dialogue = dialogue
            st.session_state.current_img = scene_img  # 保存该幕选择的专属场景图片
            st.session_state.step = next_step
            st.rerun()

def render_display_step(next_step, is_final=False):
    """渲染对话展示幕"""
    st.subheader("💬 成员的回应：")
    if st.session_state.current_img:
        st.image(st.session_state.current_img, width=300)
    st.success(st.session_state.current_dialogue)

    btn_label = "查看最终好感度结算与告白结局 💖 ➔" if is_final else "继续前往下一幕 ➔"
    if st.button(btn_label):
        st.session_state.step = next_step
        st.rerun()

def render_ending_step():
    """渲染专属结局结算"""
    st.header("🏆 专属结局结算中...")

    best_member = max(st.session_state.affection, key=st.session_state.affection.get)
    score = st.session_state.affection[best_member]
    role = st.session_state.player_role
    st.balloons()
    st.success(f"在【{role}】的故事线中，与你羁绊最深的团员是：**{best_member}**（好感度：{score} 分）！")
    
    ENDINGS = {
        "丈君": "『无论是万人瞩目的舞台，还是狭窄的后台通道……只要你在我视野里，我就能闪闪发光。做我唯一的那个特别存在，好吗？』",
        "大酱": "『这些日子谢谢你一直陪在我身旁。比起那些遥不可及的奖项，我现在最想拥抱和拥有的，只有你而已。』",
        "布丁": "『所有好吃的甜点我都想分你一半，不，全给你也可以！只要……你愿意把你的余生也分我一半！』",
        "高恭": "『在你面前，我不用扮演那个完美的大人。未来的路还很长，我想带着最真实的自己，牵着你一直走下去。』",
        "流星": "『看见了吗？今晚所有的光芒和掌声，都是因为你在台下看着我才爆发出来的！你就是我永不熄灭的幸运星！』",
        "米七": "『每次累到想放弃的时候，只要靠在你身边就能重新充满力量。别离开我……变成我专属的港湾吧。』",
        "谦杜": "『我写了那么多关于爱的歌词，但只有面对你时，我才明白那些旋律真正的意义。这首为你而写的歌，你想听一辈子吗？』"
    }
    
    st.markdown(f"### 💖 【{best_member} × {role}】专属心动结局")
    if best_member in MEMBER_IMAGES:
        st.image(MEMBER_IMAGES[best_member], width=300)
    st.write(ENDINGS.get(best_member, f"【{best_member}】温柔地凝视着你，向你诉说着独一无二的心意..."))
    st.write("---")
    if st.button("🔄 重新选择身份/开始新游戏"):
        st.session_state.step = 0
        st.session_state.affection = {m: 0 for m in MEMBERS}
        st.session_state.current_dialogue = ""
        st.session_state.current_img = ""
        st.session_state.player_role = ""
        st.rerun()

# ==================== 流程控制与路线判定 ====================
if st.session_state.step == 0:
    st.title("💖 偶像后台物语")
    st.subheader("请选择你的身份：")
    roles = ["经纪人", "粉丝/地下恋", "青梅竹马", "在日留学生or打工人"]
    role = st.radio("你的身份是：", roles)
    if st.button("开始专属故事线 ➔"):
        st.session_state.player_role = role
        if role == "经纪人":
            st.session_state.step = 100
        elif role == "粉丝/地下恋":
            st.session_state.step = 200
        elif role == "青梅竹马":
            st.session_state.step = 300
        elif role == "在日留学生or打工人":
            st.session_state.step = 400
        st.rerun()

# 💼 路线 A：经纪人专属线 (Step 100 ~ 110)
elif st.session_state.step == 100: render_choice_step("经纪人", 1, 101)
elif st.session_state.step == 101: render_display_step(102)
elif st.session_state.step == 102: render_choice_step("经纪人", 2, 103)
elif st.session_state.step == 103: render_display_step(104)
elif st.session_state.step == 104: render_choice_step("经纪人", 3, 105)
elif st.session_state.step == 105: render_display_step(106)
elif st.session_state.step == 106: render_choice_step("经纪人", 4, 107)
elif st.session_state.step == 107: render_display_step(108)
elif st.session_state.step == 108: render_choice_step("经纪人", 5, 109)
elif st.session_state.step == 109: render_display_step(110, is_final=True)
elif st.session_state.step == 110: render_ending_step()

# 💌 路线 B：粉丝/地下恋专属线 (Step 200 ~ 210)
elif st.session_state.step == 200: render_choice_step("粉丝/地下恋", 1, 201)
elif st.session_state.step == 201: render_display_step(202)
elif st.session_state.step == 202: render_choice_step("粉丝/地下恋", 2, 203)
elif st.session_state.step == 203: render_display_step(204)
elif st.session_state.step == 204: render_choice_step("粉丝/地下恋", 3, 205)
elif st.session_state.step == 205: render_display_step(206)
elif st.session_state.step == 206: render_choice_step("粉丝/地下恋", 4, 207)
elif st.session_state.step == 207: render_display_step(208)
elif st.session_state.step == 208: render_choice_step("粉丝/地下恋", 5, 209)
elif st.session_state.step == 209: render_display_step(210, is_final=True)
elif st.session_state.step == 210: render_ending_step()

# 🌸 路线 C：青梅竹马专属线 (Step 300 ~ 310)
elif st.session_state.step == 300: render_choice_step("青梅竹马", 1, 301)
elif st.session_state.step == 301: render_display_step(302)
elif st.session_state.step == 302: render_choice_step("青梅竹马", 2, 303)
elif st.session_state.step == 303: render_display_step(304)
elif st.session_state.step == 304: render_choice_step("青梅竹马", 3, 305)
elif st.session_state.step == 305: render_display_step(306)
elif st.session_state.step == 306: render_choice_step("青梅竹马", 4, 307)
elif st.session_state.step == 307: render_display_step(308)
elif st.session_state.step == 308: render_choice_step("青梅竹马", 5, 309)
elif st.session_state.step == 309: render_display_step(310, is_final=True)
elif st.session_state.step == 310: render_ending_step()

# ✈️ 路线 D：在日留学生or打工人专属线 (Step 400 ~ 410)
elif st.session_state.step == 400: render_choice_step("在日留学生or打工人", 1, 401)
elif st.session_state.step == 401: render_display_step(402)
elif st.session_state.step == 402: render_choice_step("在日留学生or打工人", 2, 403)
elif st.session_state.step == 403: render_display_step(404)
elif st.session_state.step == 404: render_choice_step("在日留学生or打工人", 3, 405)
elif st.session_state.step == 405: render_display_step(406)
elif st.session_state.step == 406: render_choice_step("在日留学生or打工人", 4, 407)
elif st.session_state.step == 407: render_display_step(408)
elif st.session_state.step == 408: render_choice_step("在日留学生or打工人", 5, 409)
elif st.session_state.step == 409: render_display_step(410, is_final=True)
elif st.session_state.step == 410: render_ending_step()
