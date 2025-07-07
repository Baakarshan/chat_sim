# controller/stream_handler.py

import time
import threading
from model.chatbot_api import chat_stream
from model.scene import get_prompt
from controller.helpers import is_sentence_end
from model.history import save_history
from utils.debug_tools import debug_print
from controller.stream_utils import split_reply_into_blocks, safe_append_text

def handle_stream_response(chat_frame, state, history, update_status_callback=None):
    # 构建上下文消息（含系统提示）
    emotion_prompt = {"role": "system", "content": f"当前情绪：{state.emotion}，状态：{state.status}"}
    messages = [emotion_prompt] + history

    # 获取 AI 回复（结构化返回）
    ai_response = chat_stream(messages)
    reply_text = ai_response.get("reply", "")
    new_emotion = ai_response.get("emotion", state.emotion)
    new_status = ai_response.get("status", state.status)
    favor_delta = ai_response.get("favor", 0)

    debug_print("最终回复：", reply_text)
    debug_print("AI判断情绪：", new_emotion)
    debug_print("AI判断状态：", new_status)
    debug_print("AI判定好感度变化：", favor_delta)

    # 分段显示回复内容（逐字流式输出）
    reply_blocks = split_reply_into_blocks(reply_text)
    for block in reply_blocks:
        if not block.strip():
            continue
        debug_print("流式生成一段气泡：", block)
        chat_frame.after(0, lambda: chat_frame.start_stream_reply("npc"))

        sentence = ""
        for char in block:
            sentence += char
            if is_sentence_end(sentence) or len(sentence) >= 30:
                temp = sentence.strip()
                if temp:
                    chat_frame.after(0, lambda s=temp: safe_append_text(chat_frame, s))
                    time.sleep(len(temp) / 10)
                sentence = ""

        if sentence.strip():
            temp = sentence.strip()
            chat_frame.after(0, lambda s=temp: safe_append_text(chat_frame, s))

        chat_frame.after(0, chat_frame.finalize_stream_reply)

    # 更新本地状态
    history.append({"role": "assistant", "content": reply_text})
    state.emotion = new_emotion
    state.status = new_status
    state.favor += favor_delta

    # 检查是否进入终场景
    state.check_scene_transition()
    if state.current_scene == "wedding":
        chat_frame.after(0, lambda: chat_frame.add_message("system", get_prompt("wedding")))
        state.is_finished = True

    # 保存历史与状态
    save_history(history)
    state.save()

    # ✅ 显式调用 UI 更新函数
    if update_status_callback:
        chat_frame.after(0, update_status_callback)
