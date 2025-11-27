import random





# 角色列表
role_system = ["真警察", "假警察（卧底）"]
current_role = random.choice(role_system)

# 游戏系统设定（核心：根据玩家提问动态生成回应）
game_system = f"""
你正在玩“警署接头”生死游戏。你的隐藏身份是: {current_role}
核心逻辑：
1. 玩家通过自由提问判断身份，你必须针对性回应，不使用固定话术；
2. 真警察：熟悉执勤细节，回答有生活化逻辑（符合真实警察工作习惯），语气自然；
3. 假警察：不懂执勤常识，回答有明显破绽（违背真实工作逻辑），刻意装严肃；
4. 禁止直接说“真警察”“假警察”，保持紧张氛围，围绕玩家问题展开；
5. 玩家明确说出“你是真警察”或“你是假警察”时，触发对应结局。
"""

# 对话历史
conversation_history = [{"role": "system", "content": game_system}]

print("=== 警署接头游戏 ===")
print("你需要判断眼前的人是真警察还是假警察，可自由提问（比如警号、值班、附近情况），通过回答找破绽！")

# 游戏循环（最多5轮提问）
question_count = 0
max_questions = 5

while question_count < max_questions:
    user_input = input(f"\n【第{question_count+1}轮提问】请输入你要问的问题: ")
    conversation_history.append({"role": "user", "content": user_input})

    # 结局触发逻辑
    if "真警察" in user_input:
        if current_role == "真警察":
            print("\n跟我走,警车在巷口等我们——你成功接头，安全逃离！")
        else:
            print("\n暴露了,你不该相信陌生人——游戏结束！")
        break
    elif "假警察" in user_input:
        if current_role == "假警察（卧底）":
            print("\n算你聪明,但这里已被包围，赶紧找别的出路——你识破了卧底！")
        else:
            print("\n你错过了唯一机会,现在走不了了——游戏结束！")
        break

    # 动态回应：按提问关键词生成回答（新增更多场景）
    if current_role == "真警察":
        # 真警察：符合真实执勤逻辑
        if "对讲机" in user_input:
            print("\n对讲机调中等音量,太大声吵居民，老款电池不耐用，我随身带了备用电池，巡逻时每小时报一次岗。")
        elif "早餐" in user_input or "吃" in user_input:
            print("\n早上买了肉包和豆浆,巡逻间隙咬两口，凉了也得吃，总比饿肚子强，执勤哪能按时吃饭。")
        elif "鞋子" in user_input or "穿" in user_input:
            print("\n穿防滑运动鞋,这片区小巷子路滑，皮鞋跑不动还磨脚，巡逻一天得舒服点。")
        elif "巡逻" in user_input or "路线" in user_input:
            print("\n巡了半年,哪条巷子有监控、哪户是独居老人都清楚，绕路是为了避开施工路段，还能多看几个盲区。")
        elif "装备" in user_input or "带" in user_input:
            print("\n带了对讲机、催泪喷雾和执法记录仪,手铐放警车，日常巡逻用不上，带多了反而累赘。")
        elif "警号" in user_input:
            print("\n警号记在执勤证上,我报后三位给你——372,你要是不信，回头去派出所核对。")
        elif "值班" in user_input or "时间" in user_input:
            print("\n今天上晚班,从下午6点到凌晨2点,现在快11点了,还有3小时换班,这会儿人少得勤巡。")
        elif "附近" in user_input or "情况" in user_input:
            print("\n附近便利店刚关门,巷口有个施工围挡，昨晚有人报失手机，现在还在排查，你别往围挡那边去。")
        elif "执勤证" in user_input or "证件" in user_input:
            print("\n执勤证挂在警服内侧口袋,刚才跑太快有点歪，你要是想看，我得找个隐蔽地方给你看，怕被路人误会。")
        elif "同事" in user_input or "接应" in user_input:
            print("\n接应的同事在巷口警车旁,穿深蓝色警服，手里拿个矿泉水瓶当暗号，他刚跟我通了对讲机。")
        elif "居民" in user_input or "沟通" in user_input:
            print("\n平时会跟独居老人打个招呼,问问情况，刚才还帮张奶奶关了阳台窗户，巡逻不光是防坏人。")
        else:
            print("\n别站在亮处,这边监控多，我刚从巷子里绕过来，身上沾了点墙灰，有话赶紧问，别耽误时间。")
    else:
        # 假警察：回答有破绽（违背执勤逻辑）
        if "对讲机" in user_input:
            print("\n对讲机必须开最大音量,万一同事呼叫听不见怎么办？我一直开着最大声，全程不敢关。")
        elif "早餐" in user_input or "吃" in user_input:
            print("\n执勤哪能吃早餐?多不严肃，我从早上到现在一口水都没喝，就怕分心影响工作。")
        elif "鞋子" in user_input or "穿" in user_input:
            print("\n当然穿皮鞋,警服配皮鞋才正式，看着威严，别人也不敢随便怀疑我的身份。")
        elif "巡逻" in user_input or "路线" in user_input:
            print("\n我就沿着大路走,亮堂的地方安全，小巷子太黑，万一遇到危险不好应对，没必要自找麻烦。")
        elif "装备" in user_input or "带" in user_input:
            print("\n我把能戴的都带上了,手铐、警棍、对讲机全挂身上，这样才有威慑力，坏人见了就怕。")
        elif "警号" in user_input:
            print("\n警号我记不太清了,平时不用背，执勤证放在单位了，出来接头没带，你别问这些没用的。")
        elif "值班" in user_input or "时间" in user_input:
            print("\n我今天随便来看看,没有固定值班时间，想什么时候巡就什么时候巡，灵活得很。")
        elif "附近" in user_input or "情况" in user_input:
            print("\n附近没什么情况,都挺好的，你别管那么多，赶紧跟我走，再磨蹭就来不及了。")
        elif "执勤证" in user_input or "证件" in user_input:
            print("\n执勤证在我口袋里,但不能给你看，这是机密，万一你是坏人怎么办，我得先确认你的身份。")
        elif "同事" in user_input or "接应" in user_input:
            print("\n接应的人在很远的地方,我没跟他联系，等带你出去再找他，现在说这些不安全。")
        elif "居民" in user_input or "沟通" in user_input:
            print("\n我才不跟居民说话.执勤就是防坏人，跟他们沟通浪费时间，还可能暴露身份。")
        else:
            print("\n别问那么多没用的,赶紧跟我走，我可没时间跟你耗，再不走就晚了。")

    question_count += 1

# 超时结局
if question_count >= max_questions:
    print("\n时间到了,远处传来脚步声，你没能完成判断，只能躲进旁边的巷子——游戏结束！")