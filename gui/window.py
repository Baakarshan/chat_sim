# gui/window.py

import tkinter as tk
from controller.chat_controller import ChatController
from gui.chat_frame import ChatFrame
from gui.input_frame import InputFrame
from gui.control_panel import build_control_panel
from gui.window_init import load_history_if_any, start_intro_if_needed
from model.history import reset_history
from utils.debug_tools import debug_print
import sys
import os

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("校园恋爱模拟器")
        self.geometry("480x640")
        self.resizable(True, True)

        self.chat_frame = ChatFrame(self)
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        self.input_frame = InputFrame(self, self.on_send)
        self.input_frame.pack(fill=tk.X)

        # ✅ 显式传入 UI 刷新函数
        self.ctrl = ChatController(self.chat_frame, update_status_callback=self.update_status)

        self.control_panel = build_control_panel(self)

        self.history = load_history_if_any(self.ctrl, self.chat_frame)
        self.after(100, lambda: start_intro_if_needed(self.ctrl, self.chat_frame, self.history))
        self.update_status()

    def on_send(self, text):
        """处理发送按钮事件"""
        self.ctrl.on_user_input(text)

    def update_status(self):
        """同步状态栏显示：好感度、情绪、状态"""
        state = self.ctrl.state
        self.control_panel["aff"].config(text=f"好感度: {state.favor}")
        self.control_panel["emo"].config(text=f"情绪: {state.emotion}")
        self.control_panel["stat"].config(text=f"状态: {state.status}")
        debug_print("已更新状态栏：", state.favor, state.emotion, state.status)

    def on_restart(self):
        """重启游戏（保留当前窗口）"""
        reset_history()
        self.ctrl.state.reset()
        python = sys.executable
        os.execl(python, python, *sys.argv)
