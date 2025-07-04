# gui/window.py

import tkinter as tk
from controller.chat_controller import ChatController
from gui.chat_frame import ChatFrame
from gui.input_frame import InputFrame
from gui.control_panel import build_control_panel
from gui.window_init import load_history_if_any, start_intro_if_needed
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

        self.ctrl = ChatController(self.chat_frame, auto_intro=False)

        self.control_panel = build_control_panel(self)

        self.history = load_history_if_any(self.ctrl, self.chat_frame)
        self.after(100, lambda: start_intro_if_needed(self.ctrl, self.chat_frame, self.history))

        self.after(200, lambda: self.chat_frame.canvas.yview_moveto(1.0))
        self.update_status()

    def on_send(self, text):
        self.ctrl.on_user_input(text)
        self.update_status()

    def update_status(self):
        aff = self.ctrl.state.affection
        emo = self.ctrl.state.emotion
        stat = getattr(self.ctrl.state, "status", "放空")
        self.control_panel["aff"].config(text=f"好感度: {aff}")
        self.control_panel["emo"].config(text=f"情绪: {emo}")
        self.control_panel["stat"].config(text=f"状态: {stat}")

    def on_restart(self):
        from model.history import clear_history
        self.ctrl.state.reset()
        clear_history()
        python = sys.executable
        os.execl(python, python, *sys.argv)
