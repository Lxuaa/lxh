from api import call_zhipu_api
from roles import get_break_rules
from jsonbin import save_latest_reply

# 修正参数定义语法错误+规范缩进后的chat_once函数
def chat_once(history, user_input, role_prompt, bin_id=None, access_key=None):
    # 添加用户输入到对话历史
    history.append({"role": "user", "content": user_input})

    # 构造系统消息（角色提示词+规则）
    system_message = role_prompt + "\n\n" + get_break_rules()
    # 构造API请求的消息列表（系统消息+对话历史，排除第一个默认消息）
    api_messages = [{"role": "system", "content": system_message}] + history[1:]

    # 调用智谱API获取回复
    result = call_zhipu_api(api_messages)
    # 提取AI回复内容（适配智谱API的返回格式）
    reply = result['choices'][0]['message']['content']

    # 将AI回复添加到对话历史
    history.append({"role": "assistant", "content": reply})

    # 若传入bin_id和access_key，保存最新回复到JSONBin
    if bin_id and access_key:
        save_latest_reply(reply, bin_id, access_key)

    # 返回AI回复内容
    return reply
