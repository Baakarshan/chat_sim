# gui/chat_frame.py

import tkinter as tk
from tkinter import font as tkFont
from .chat_bubble import ChatBubbleManager
from utils.debug_tools import debug_print
import platform

class ChatFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner_frame = tk.Frame(self.canvas, bg="white")

        self.inner_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.font = tkFont.Font(family="微软雅黑", size=10)
        self.bubble_mgr = ChatBubbleManager(self.inner_frame, self.font)

        self.inner_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        # 鼠标滚轮支持
        system = platform.system()
        if system in ("Windows", "Darwin"):
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        else:
            self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
            self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

        self.stream_role = None
        self.stream_label = None
        self.stream_text = ""

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_resize(self, event):
        self.canvas.itemconfig(self.inner_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def scroll_to_bottom(self):
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def add_message(self, role, text):
        debug_print(f"添加静态气泡 [{role}]：{text}")
        self.bubble_mgr.create_bubble(role, text)
        self.scroll_to_bottom()

    def start_stream_reply(self, role):
        debug_print("开始流式生成回复气泡")
        self.stream_role = role
        self.stream_label = self.bubble_mgr.start_stream_bubble(role)
        self.stream_text = ""
        self.scroll_to_bottom()

    def stream_append(self, text_chunk):
        if self.stream_label is None:
            self.stream_label = self.bubble_mgr.start_stream_bubble(self.stream_role)

        self.stream_text += text_chunk
        self.stream_label.config(text=self.stream_text)
        self.stream_label.update_idletasks()
        self.scroll_to_bottom()

    def finalize_stream_reply(self):
        if self.stream_label:
            if not self.stream_label.cget("text").strip() and self.stream_text.strip():
                self.stream_label.config(text=self.stream_text.strip())
            elif not self.stream_text.strip():
                debug_print("移除空气泡")
                self.stream_label.destroy()

            self.stream_label = None
            self.scroll_to_bottom()
