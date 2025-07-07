# gui/chat_bubble.py
# coding: utf-8
"""
聊天气泡管理模块。
遵循 Google Python 风格指南，增加详细中文注释。
"""

import tkinter as tk  # 导入 Tkinter 库

class ChatBubbleManager:
    """
    聊天气泡管理器，负责在界面上创建和管理聊天气泡。
    """
    def __init__(self, parent, font):
        """
        初始化气泡管理器。
        Args:
            parent: 父级 Tkinter 容器。
            font: 使用的字体。
        """
        self.parent = parent  # 聊天气泡的父容器
        self.font = font  # 聊天气泡字体

    def create_bubble(self, role: str, text: str) -> None:
        """
        创建一个静态聊天气泡。
        Args:
            role: 消息角色（system/user/npc）。
            text: 显示的文本内容。
        """
        bg_color = {"system": "#f0f0f0", "user": "#cce5ff", "npc": "#ffcce5"}.get(role, "#eeeeee")  # 背景色
        align = "w" if role in ["npc", "system"] else "e"  # 对齐方式
        side = "left" if align == "w" else "right"  # 侧边

        outer = tk.Frame(self.parent, bg="white", pady=2)  # 外部容器
        label = tk.Label(
            outer,
            text=text,
            bg=bg_color,
            font=self.font,
            justify="left",
            anchor="w",
            wraplength=320,
            padx=10,
            pady=6
        )
        label.pack(side=side, anchor=align, padx=10)  # 放置标签
        outer.pack(anchor=align, fill="x", padx=5, pady=2)  # 放置外部容器

    def start_stream_bubble(self, role: str):
        """
        创建一个用于流式输出的气泡（初始内容为空）。
        Args:
            role: 消息角色（npc等）。
        Returns:
            label: 可动态更新内容的 Label。
        """
        bg_color = {"npc": "#ffcce5"}.get(role, "#eeeeee")  # 背景色
        outer = tk.Frame(self.parent, bg="white", pady=2)  # 外部容器
        label = tk.Label(
            outer,
            text="",
            bg=bg_color,
            font=self.font,
            justify="left",
            anchor="w",
            wraplength=320,
            padx=10,
            pady=6
        )
        label.pack(side="left", anchor="w", padx=10)  # 放置标签
        outer.pack(anchor="w", fill="x", padx=5, pady=2)  # 放置外部容器
        return label  # 返回可动态更新的标签
