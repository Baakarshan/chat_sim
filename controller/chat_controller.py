# controller/chat_controller.py

import threading
from model.history import load_history, save_history
from model.game_state import GameState
from controller.stream_handler import handle_stream_response
from utils.debug_tools import debug_print

class ChatController:
    def __init__(self, chat_frame, update_status_callback=None, auto_intro=True):
        self.chat_frame = chat_frame
        self.update_status_callback = update_status_callback
        self.state = GameState.load()
        self.history = load_history()
        self._first_prompt_shown = False

        # ✅ 删除自动生成旁白的逻辑，让 window_init 控制 intro 显示

    def push_system(self, text):
        """添加系统气泡到聊天框"""
        self.chat_frame.after(0, lambda: self.chat_frame.add_message("system", text))
        self.history.append({"role": "system", "content": text})

    def on_user_input(self, text):
        """处理用户输入，记录并触发 AI 回复"""
        debug_print("玩家输入：", text)
        self.chat_frame.after(0, lambda: self.chat_frame.add_message("user", text))
        self.history.append({"role": "user", "content": text})

        # 启动异步 AI 回复线程，传入 UI 刷新回调
        threading.Thread(
            target=handle_stream_response,
            args=(self.chat_frame, self.state, self.history, self.update_status_callback),
            daemon=True
        ).start()
