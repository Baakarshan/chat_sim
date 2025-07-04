# gui/window.py

import tkinter as tk
from controller.chat_controller import ChatController
from gui.chat_frame import ChatFrame
from gui.input_frame import InputFrame
from model.history import load_history, clear_history
from model.scene import get_prompt
from utils.debug_tools import debug_print
import sys
import os

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("校园恋爱模拟器")
        self.geometry("480x640")
        self.resizable(True, True)  # ✅ 允许拖拽窗口大小

        self.chat_frame = ChatFrame(self)
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        self.input_frame = InputFrame(self, self.on_send)
        self.input_frame.pack(fill=tk.X)

        self.ctrl = ChatController(self.chat_frame, auto_intro=False)

        self.control_panel = self._build_controls()
        self._load_history_if_any()

        if self.history:
            self.chat_frame.add_message("system", "———— 以上为历史记录 ————")

        self.after(100, self._start_intro_if_needed)
        self.after(200, lambda: self.chat_frame.canvas.yview_moveto(1.0))  # ✅ 启动时滚动到底部
        self.update_status()

    def _build_controls(self):
        frame = tk.Frame(self, bg="#f0f0f0", pady=4)
        frame.pack(fill=tk.X)

        self.aff_label = tk.Label(frame, text="好感度: 0", width=12, anchor="w")
        self.emotion_label = tk.Label(frame, text="情绪: neutral", width=14, anchor="w")
        self.status_label = tk.Label(frame, text="状态: 放空", width=14, anchor="w")

        restart_btn = tk.Button(frame, text="重新开始", command=self.on_restart)
        quit_btn = tk.Button(frame, text="关闭游戏", command=self.quit)

        self.aff_label.pack(side=tk.LEFT, padx=5)
        self.emotion_label.pack(side=tk.LEFT, padx=5)
        self.status_label.pack(side=tk.LEFT, padx=5)
        restart_btn.pack(side=tk.RIGHT, padx=5)
        quit_btn.pack(side=tk.RIGHT, padx=5)

        return frame

    def _load_history_if_any(self):
        self.history = load_history()
        if not self.history:
            return
        debug_print("加载历史记录条数：", len(self.history))
        for msg in self.history:
            role = msg["role"]
            if role == "assistant":
                role = "npc"
            self.chat_frame.add_message(role, msg["content"])

    def _start_intro_if_needed(self):
        if not self.history:
            debug_print("首次启动，注入初始旁白")
            self.ctrl.push_system(get_prompt(self.ctrl.state.current_scene))

    def on_send(self, text):
        self.ctrl.on_user_input(text)
        self.update_status()

    def update_status(self):
        aff = self.ctrl.state.affection
        emo = self.ctrl.state.emotion
        stat = getattr(self.ctrl.state, "status", "放空")
        self.aff_label.config(text=f"好感度: {aff}")
        self.emotion_label.config(text=f"情绪: {emo}")
        self.status_label.config(text=f"状态: {stat}")

    def on_restart(self):
        clear_history()
        self.ctrl.state.reset()
        python = sys.executable
        os.execl(python, python, *sys.argv)
