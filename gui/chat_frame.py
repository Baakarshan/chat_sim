# gui/chat_frame.py
# coding: utf-8
"""
聊天主界面框架。
遵循 Google Python 风格指南，增加详细中文注释。
"""

import tkinter as tk  # 导入 Tkinter 库
from tkinter import font as tkFont  # 导入字体模块
from .chat_bubble import ChatBubbleManager  # 导入气泡管理器
from utils.debug_tools import debug_print  # 导入调试打印
import platform  # 导入平台判断

class ChatFrame(tk.Frame):
    """
    聊天主界面，包含滚动、气泡等。
    """
    def __init__(self, master):
        super().__init__(master)
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)  # 聊天内容画布
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)  # 垂直滚动条
        self.inner_frame = tk.Frame(self.canvas, bg="white")  # 内部内容框架

        self.inner_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")  # 嵌入内容
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.font = tkFont.Font(family="微软雅黑", size=10)  # 聊天气泡字体
        self.bubble_mgr = ChatBubbleManager(self.inner_frame, self.font)  # 气泡管理器

        self.inner_frame.bind("<Configure>", self._on_frame_configure)  # 内容变化时更新滚动区域
        self.canvas.bind("<Configure>", self._on_canvas_resize)  # 画布大小变化时调整内容宽度

        # 鼠标滚轮支持（跨平台）
        system = platform.system()
        if system in ("Windows", "Darwin"):
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        else:
            self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
            self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

        self.stream_role = None  # 当前流式角色
        self.stream_label = None  # 当前流式标签
        self.stream_text = ""  # 当前流式文本

    def _on_frame_configure(self, event):
        """
        内容区域变化时，更新滚动区域。
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_resize(self, event):
        """
        画布大小变化时，调整内容宽度。
        """
        self.canvas.itemconfig(self.inner_window, width=event.width)

    def _on_mousewheel(self, event):
        """
        鼠标滚轮滚动事件。
        """
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def scroll_to_bottom(self):
        """
        滚动到底部。
        """
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def add_message(self, role: str, text: str) -> None:
        """
        添加静态聊天气泡。
        Args:
            role: 消息角色。
            text: 消息内容。
        """
        debug_print(f"添加静态气泡 [{role}]：{text}")
        self.bubble_mgr.create_bubble(role, text)
        self.scroll_to_bottom()

    def start_stream_reply(self, role: str) -> None:
        """
        开始流式生成回复气泡。
        Args:
            role: 消息角色。
        """
        debug_print("开始流式生成回复气泡")
        self.stream_role = role
        self.stream_label = self.bubble_mgr.start_stream_bubble(role)
        self.stream_text = ""
        self.scroll_to_bottom()

    def stream_append(self, text_chunk: str) -> None:
        """
        追加流式文本到当前气泡。
        Args:
            text_chunk: 新增文本。
        """
        if self.stream_label is None:
            self.stream_label = self.bubble_mgr.start_stream_bubble(self.stream_role)

        self.stream_text += text_chunk
        self.stream_label.config(text=self.stream_text)
        self.stream_label.update_idletasks()
        self.scroll_to_bottom()

    def finalize_stream_reply(self) -> None:
        """
        结束流式回复，处理空气泡或补全内容。
        """
        if self.stream_label:
            if not self.stream_label.cget("text").strip() and self.stream_text.strip():
                self.stream_label.config(text=self.stream_text.strip())
            elif not self.stream_text.strip():
                debug_print("移除空气泡")
                self.stream_label.destroy()

            self.stream_label = None
            self.scroll_to_bottom()
