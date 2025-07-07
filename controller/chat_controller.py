# controller/chat_controller.py
# coding: utf-8
"""
聊天控制器模块。
遵循 Google Python 风格指南，增加类型注解和详细中文注释。
"""

import threading  # 导入线程库，用于异步处理
from typing import Callable, Optional  # 类型注解
from model.history import load_history, save_history  # 导入历史记录相关方法
from model.game_state import GameState  # 导��游戏状态类
from controller.stream_handler import handle_stream_response  # 导入流式响应处理函数
from utils.debug_tools import debug_print  # 导入调试打印工具

class ChatController:
    """
    聊天控制器，负责管理聊天逻辑、状态与历史。
    """
    def __init__(self, chat_frame, update_status_callback: Optional[Callable] = None, auto_intro: bool = True):
        """
        初始化聊天控制器。
        Args:
            chat_frame: 聊天界面框架对象。
            update_status_callback: 状态更新回调函数，可选。
            auto_intro: 是否自动显示开场白。
        """
        self.chat_frame = chat_frame  # 聊天界面框架
        self.update_status_callback = update_status_callback  # 状态更新回调
        self.state = GameState.load()  # 加载游戏状态
        self.history = load_history()  # 加载历史记录
        self._first_prompt_shown = False  # 是否已显示首次提示
        # ✅ 删除自动生成旁白的逻辑，让 window_init 控制 intro 显示

    def push_system(self, text: str) -> None:
        """
        添加系统气泡到聊天框。
        Args:
            text: 系统消息文本。
        """
        self.chat_frame.after(0, lambda: self.chat_frame.add_message("system", text))  # UI 线程安全地添加系统消息
        self.history.append({"role": "system", "content": text})  # 记录到历史

    def on_user_input(self, text: str) -> None:
        """
        处理用户输入，记录并触发 AI 回复。
        Args:
            text: 用户输入文本。
        """
        debug_print("玩家输入：", text)  # 调试输出玩家输入
        self.chat_frame.after(0, lambda: self.chat_frame.add_message("user", text))  # UI 线程安全地添加用户消息
        self.history.append({"role": "user", "content": text})  # 记录到历史

        # 启动异步 AI 回复线程，传入 UI 刷新回调
        threading.Thread(
            target=handle_stream_response,  # 目标函数为流式响应处理
            args=(self.chat_frame, self.state, self.history, self.update_status_callback),  # 传递参数
            daemon=True  # 设置为守护线程
        ).start()
