# gui/input_frame.py
# coding: utf-8
"""
输入框模块。
遵循 Google Python 风格指南，增加详细中文注释。
"""

import tkinter as tk  # 导入 Tkinter 库

class InputFrame(tk.Frame):
    """
    聊天输入框组件。
    """
    def __init__(self, master, callback):
        """
        初始化输入框。
        Args:
            master: 父级容器。
            callback: 发送消息回调函数。
        """
        super().__init__(master)
        self.entry = tk.Entry(self)  # 文本输入框
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", lambda e: self.on_send())  # 回车发送
        tk.Button(self, text="发送", command=self.on_send).pack(side=tk.RIGHT)  # 发送按钮
        self.callback = callback  # 回调函数

    def on_send(self) -> None:
        """
        发送消息事件处理。
        """
        text = self.entry.get().strip()  # 获取输入内容
        if text:
            self.callback(text)  # 调用回调
            self.entry.delete(0, tk.END)  # 清空输入框
