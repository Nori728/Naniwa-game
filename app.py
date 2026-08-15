# 页面标题与风格设置
st.set_page_config(page_title="偶像团体内后台乙女游戏", page_icon="🌟")
st.title("🌟 后台专属恋爱故事")

# 初始化 session_state（用于在网页刷新时保存玩家的选择与好感度）
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'player_name' not in st.session_state:
    st.session_state.player_name = "玩家"
if 'role_title' not in st.session_state:
    st.session_state.role_title = "经纪人"
if 'role_desc' not in st.session_state:
    st.session_state.role_desc = ""
if 'affection' not in st.session_state:
    st.session_state.affection = {
        "丈君": 0, "大酱": 0, "布丁": 0,
        "高恭": 0, "流星": 0, "米七": 0, "谦杜": 0
    }

# 团员名单定义
member_a, member_b, member_c = "丈君", "大酱", "布丁"
member_d, member_e, member_f, member_g = "高恭", "流星", "米七", "谦杜"

# ==================== 步骤 1：角色设定 ====================
if st.session_state.step == 1:
    st.header("🎭 步骤 1：创建你的角色")
    
    player_input = st.text_input("请输入你的名字/昵称：", value="小明")
    
    role_options = [
        "1. 专属贴身经纪人（照顾大家的饮食起居，大家都很依赖你）",
        "2. 随团造型师（打造无敌舞台造型，经常近距离接触）",
        "3. 青梅竹马的特别好友（掌握所有秘密，最特别的存在）"
    ]
    role_choice = st.radio("请选择你在团体里的身份设定：", role_options)
    
    if st.button("确定身份，进入后台 ➔"):
        st.session_state.player_name = player_input
        if "1." in role_choice:
            st.session_state.role_title = "经纪人"
            st.session_state.role_desc = "作为专属经纪人，你照顾着大家的饮食起居。"
        elif "2." in role_choice:
            st.session_state.role_title = "造型师"
            st.session_state.role_desc = "作为随团造型师，你亲手打造了他们今晚完美的造型。"
        else:
            st.session_state.role_title = "竹马"
            st.session_state.role_desc = "作为青梅竹马，你见证了他们一路走来的点点滴滴。"
            
        st.session_state.step = 2
        st.rerun()

# ==================== 步骤 2：第一幕 休息室互动 ====================
elif st.session_state.step == 2:
    st.info(f"📌 身份确认：【{st.session_state.player_name}】（{st.session_state.role_desc}）")
    st.markdown("---")
    st.subheader(f"🎬 第一幕：{st.session_state.role_title}，你想走向哪一位成员？")
    
    act1_options = [
        f"1. 走向 {member_a}：拿着运动饮料，递给刚跳完舞的他。",
        f"2. 走向 {member_b}：拿着润喉糖给他，关心他的嗓子。",
        f"3. 走向 {member_c}：拿着甜点过去，陪他一起休息聊天。",
        f"4. 走向 {member_d}：拿着毛巾给他，夸奖他今天跳舞很认真。",
        f"5. 走向 {member_e}：夸奖他今天表情管理很棒。",
        f"6. 走向 {member_f}：递上热咖啡，陪他讨论刚刚的舞台表现。",
        f"7. 走向 {member_g}：拿着相机夸奖他今天的造型非常帅气。"
    ]
    
    c1 = st.radio("请选择你的行动：", act1_options)
    
    if st.button("提交选择 ➔"):
        if "1." in c1:
            st.session_state.affection[member_a] += 20
            st.session_state.act1_dialogue = f"{member_a} 大口喝下：『多亏有你！简直活过来啦！』"
        elif "2." in c1:
            st.session_state.affection[member_b] += 20
            st.session_state.act1_dialogue = f"{member_b} 惊喜地接过润喉糖：『太及时了，谢谢你一直这么细心照顾我。』"
        elif "3." in c1:
            st.session_state.affection[member_c] += 20
            st.session_state.act1_dialogue = f"{member_c} 眼睛一亮：『哇！是布丁呀！我们快坐下一起吃！』"
        elif "4." in c1:
            st.session_state.affection[member_d] += 20
            st.session_state.act1_dialogue = f"{member_d} 接过毛巾擦汗，对你笑了笑：『毕竟看着嘛，Super有动力！』"
        elif "5." in c1:
            st.session_state.affection[member_e] += 20
            st.session_state.act1_dialogue = f"{member_e} 凑近镜头对你眨眼：『那你觉得今天我是全场最好看的吗？』"
        elif "6." in c1:
            st.session_state.affection[member_f] += 20
            st.session_state.act1_dialogue = f"{member_f} 接过咖啡笑了：『还是你最懂我，刚刚舞台上真的好紧张。』"
        elif "7." in c1:
            st.session_state.affection[member_g] += 20
            st.session_state.act1_dialogue = f"{member_g} 摆出帅气姿势：『你的镜头永远最懂我最帅的角度！』"
            
        st.session_state.step = 3
        st.rerun()

# ==================== 步骤 3：第二幕 庆功宴邀请 ====================
elif st.session_state.step == 3:
    st.success(st.session_state.act1_dialogue)
    st.markdown("---")
    st.subheader("🎬 第二幕：庆功宴快结束时，你想陪谁多聊聊？")
    
    act2_options = [
        f"1. 走向 {member_a}：『跳了一整天，脚还好吗？』",
        f"2. 走向 {member_b}：『喉咙舒服点了吗？等下别再喝冰水了。』",
        f"3. 走向 {member_c}：『这份甜点我帮你留了一份，等下偷偷吃。』",
        f"4. 走向 {member_d}：『今天在舞台上超级耀眼喔！』",
        f"5. 走向 {member_e}：『刚刚台下的尖叫声几乎都是给你的呢。』",
        f"6. 走向 {member_f}：『舞台表现已经很完美了，别给自己太大压力。』",
        f"7. 走向 {member_g}：『相机里拍了好多你今天的照片，要先看吗？』"
    ]
    
    c2 = st.radio("请选择你的行动：", act2_options)
    
    if st.button("查看最终好感度与结局 💘"):
        if "1." in c2: st.session_state.affection[member_a] += 20
        elif "2." in c2: st.session_state.affection[member_b] += 20
        elif "3." in c2: st.session_state.affection[member_c] += 20
        elif "4." in c2: st.session_state.affection[member_d] += 20
        elif "5." in c2: st.session_state.affection[member_e] += 20
        elif "6." in c2: st.session_state.affection[member_f] += 20
        elif "7." in c2: st.session_state.affection[member_g] += 20
        
        st.session_state.step = 4
        st.rerun()

# ==================== 步骤 4：结局结算 ====================
elif st.session_state.step == 4:
    st.header("🏆 好感度结算中...")
    
    best_member = max(st.session_state.affection, key=st.session_state.affection.get)
    highest_score = st.session_state.affection[best_member]
    
    st.balloons()  # 触发网页彩带庆祝动画
    
    st.success(f"【结算】对你心动值最高的成员是：**{best_member}**（好感度：{highest_score} 分）")
    
    st.markdown(f"### 💖 进人 【{best_member}】 个人专属恋爱结局")
    st.info(f"**{best_member}** 在无人的后台走廊拉住你，轻声说：\n\n『{st.session_state.player_name}，不要只把我当成团员……在我心里，你永远是我的第一顺位。』")
    
    if st.button("🔄 重新开始游戏"):
        st.session_state.step = 1
        st.session_state.affection = {
            "丈君": 0, "大酱": 0, "布丁": 0,
            "高恭": 0, "流星": 0, "米七": 0, "谦杜": 0
        }
        st.rerun()
