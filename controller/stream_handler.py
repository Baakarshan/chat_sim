# controller/stream_handler.py

import time
import threading
from model.chatbot_api import chat_stream
from model.emotion_prompt import build_emotion_prompt
from model.scene import get_prompt
from controller.helpers import is_sentence_end
from model.history import save_history
from model.emotion_state_picker import pick_emotion_state
from utils.debug_tools import debug_print
from controller.stream_utils import split_reply_into_blocks, safe_append_text

def handle_stream_response(chat_frame, state, history):
    prompt_text = build_emotion_prompt(state.emotion)
    debug_print("生成系统提示：", prompt_text)

    emotion_prompt = {"role": "system", "content": prompt_text}
    messages = [emotion_prompt] + history

    reply_full = ""
    all_chunks = []

    for chunk in chat_stream(messages):
        debug_print("收到模型片段：", chunk)
        reply_full += chunk
        all_chunks.append(chunk)
        time.sleep(len(chunk) / 10)

    reply_blocks = split_reply_into_blocks(reply_full)

    for block in reply_blocks:
        if not block.strip():
            continue
        debug_print("流式生成一段气泡：", block)
        chat_frame.after(0, lambda: chat_frame.start_stream_reply("npc"))

        sentence = ""
        for char in block:
            sentence += char
            if is_sentence_end(sentence) or len(sentence) >= 30:
                temp_sentence = sentence.strip()
                if temp_sentence:
                    chat_frame.after(0, lambda s=temp_sentence: safe_append_text(chat_frame, s))
                    time.sleep(len(temp_sentence) / 10)
                sentence = ""

        if sentence.strip():
            temp_sentence = sentence.strip()
            chat_frame.after(0, lambda s=temp_sentence: safe_append_text(chat_frame, s))

        chat_frame.after(0, chat_frame.finalize_stream_reply)

    debug_print("最终回复：", reply_full)
    history.append({"role": "assistant", "content": reply_full})

    emotion, status = pick_emotion_state(history, reply_full, state.current_scene)
    debug_print("AI判断情绪：", emotion)
    debug_print("AI判断状态：", status)
    state.emotion = emotion
    state.status = status

    state.check_scene_transition()
    if state.current_scene == "wedding":
        chat_frame.after(0, lambda: chat_frame.add_message("system", get_prompt("wedding")))
        state.is_finished = True

    save_history(history)
    state.save()
    chat_frame.after(0, chat_frame.master.update_status)
