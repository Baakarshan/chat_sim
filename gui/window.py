# gui/window.py
# coding: utf-8
"""
主窗口模块。
遵循 Google Python 风格指南，增加详细中文注释。
"""

import tkinter as tk  # 导入 Tkinter 库
from controller.chat_controller import ChatController  # 聊天控制器
from gui.chat_frame import ChatFrame  # 聊天界面
from gui.input_frame import InputFrame  # 输���框
from gui.control_panel import build_control_panel  # 控制面板
from gui.window_init import load_history_if_any, start_intro_if_needed  # 初始化逻辑
from model.history import reset_history  # 重置历史
from utils.debug_tools import debug_print  # 调试打印
import sys  # 系统操作
import os  # 操作系统接口

class Window(tk.Tk):
    """
    主窗口类，负责整体界面与主流程。
    """
    def __init__(self):
        super().__init__()
        self.title("校园恋爱模拟器")  # 设置窗口标题
        self.geometry("480x640")  # 设置窗口大小
        self.resizable(True, True)  # 允许缩放

        self.chat_frame = ChatFrame(self)  # 聊天内容区
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        self.input_frame = InputFrame(self, self.on_send)  # 输入区
        self.input_frame.pack(fill=tk.X)

        # ✅ 显式传入 UI 刷新函数
        self.ctrl = ChatController(self.chat_frame, update_status_callback=self.update_status)

        self.control_panel = build_control_panel(self)  # 状态栏与按钮

        self.history = load_history_if_any(self.ctrl, self.chat_frame)  # 加载历史
        self.after(100, lambda: start_intro_if_needed(self.ctrl, self.chat_frame, self.history))  # 场景 intro
        self.update_status()  # 初始化状态栏

    def on_send(self, text: str) -> None:
        """
        处理发送按钮事件。
        Args:
            text: 用户输入文本。
        """
        self.ctrl.on_user_input(text)

    def update_status(self) -> None:
        """
        同步状态栏显示：好感度、情绪、状态。
        """
        state = self.ctrl.state
        self.control_panel["aff"].config(text=f"好感度: {state.favor}")
        self.control_panel["emo"].config(text=f"情绪: {state.emotion}")
        self.control_panel["stat"].config(text=f"状态: {state.status}")
        debug_print("已更新状态栏：", state.favor, state.emotion, state.status)

    def on_restart(self) -> None:
        """
        重启游戏（保留当前窗口）。
        """
        reset_history()
        self.ctrl.state.reset()
        python = sys.executable
        os.execl(python, python, *sys.argv)
