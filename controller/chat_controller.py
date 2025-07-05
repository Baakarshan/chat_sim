# controller/chat_controller.py

import threading
from model.history import load_history, save_history
from model.game_state import GameState
from model.scene import get_prompt
from model.scene_generator import generate_scene_intro
from controller.stream_handler import handle_stream_response
from utils.debug_tools import debug_print

class ChatController:
    def __init__(self, chat_frame, auto_intro=True):
        self.chat_frame = chat_frame
        self.state = GameState.load()
        self.history = load_history()
        self._first_prompt_shown = False

        # 初始化场景提示
        if auto_intro:
            if self.history:
                debug_print("加载已有历史，生成旁白")
                prompt = generate_scene_intro(
                    current_scene=self.state.current_scene,
                    emotion=self.state.emotion,
                    status=self.state.status,
                    history=self.history
                )
            else:
                debug_print("首次启动，使用 preset 旁白")
                prompt = get_prompt(self.state.current_scene)

            debug_print("初始场景提示：", prompt)
            self.push_system(prompt)
            self._first_prompt_shown = True

    def push_system(self, text):
        """添加系统气泡到聊天框"""
        self.chat_frame.after(0, lambda: self.chat_frame.add_message("system", text))
        self.history.append({"role": "system", "content": text})

    def on_user_input(self, text):
        """处理用户输入，记录并触发 AI 回复"""
        debug_print("玩家输入：", text)
        self.chat_frame.after(0, lambda: self.chat_frame.add_message("user", text))
        self.history.append({"role": "user", "content": text})

        # 启动异步 AI 回复线程（AI 会决定情绪、状态、好感度变化）
        threading.Thread(
            target=handle_stream_response,
            args=(self.chat_frame, self.state, self.history),
            daemon=True
        ).start()
