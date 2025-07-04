# controller/stream_handler.py

import time
from model.chatbot_api import chat_stream
from model.emotion_prompt import build_emotion_prompt
from model.scene import get_prompt
from controller.helpers import is_sentence_end
from model.history import save_history
from model.emotion_state_picker import pick_emotion_state
from utils.debug_tools import debug_print

def handle_stream_response(chat_frame, state, history):
    # 构建系统 prompt（根据当前情绪）
    prompt_text = build_emotion_prompt(state.emotion)
    debug_print("生成系统提示：", prompt_text)

    emotion_prompt = {"role": "system", "content": prompt_text}
    messages = [emotion_prompt] + history

    reply_full = ""
    current_sentence = ""

    # ✅ 主线程安全创建初始气泡
    chat_frame.after(0, lambda: chat_frame.start_stream_reply("npc"))

    for chunk in chat_stream(messages):
        debug_print("收到模型片段：", chunk)
        reply_full += chunk
        current_sentence += chunk
        time.sleep(len(chunk) / 10)

        if is_sentence_end(current_sentence):
            sentence = current_sentence.strip()
            chat_frame.after(0, lambda s=sentence: chat_frame.stream_append(s))
            current_sentence = ""

    # ✅ 收尾残留内容
    if current_sentence.strip():
        chat_frame.after(0, lambda s=current_sentence.strip(): chat_frame.stream_append(s))

    chat_frame.after(0, chat_frame.finalize_stream_reply)

    debug_print("最终回复：", reply_full)
    history.append({"role": "assistant", "content": reply_full})

    # ✅ 让 AI 判断情绪状态
    emotion, status = pick_emotion_state(history, reply_full, state.current_scene)
    debug_print("AI判断情绪：", emotion)
    debug_print("AI判断状态：", status)
    state.emotion = emotion
    state.status = status

    # ✅ 场景推进判断
    state.check_scene_transition()

    if state.current_scene == "wedding":
        chat_frame.after(0, lambda: chat_frame.add_message("system", get_prompt("wedding")))
        state.is_finished = True

    save_history(history)
    state.save()

    # ✅ 通知界面更新状态栏
    chat_frame.after(0, chat_frame.master.update_status)
