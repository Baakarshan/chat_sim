# gui/chat_bubble.py

import tkinter as tk
import textwrap
from utils.debug_tools import debug_print

class ChatBubbleManager:
    def __init__(self, parent, font):
        self.parent = parent
        self.font = font

    def create_bubble(self, role, text):
        bubble_text = self._wrap_text(text)
        bg_color = {
            "system": "#f0f0f0",
            "user": "#cce5ff",
            "npc": "#ffcce5"
        }.get(role, "#eeeeee")

        align_side = "left" if role in ["npc", "system"] else "right"
        align_anchor = "w" if role in ["npc", "system"] else "e"

        outer = tk.Frame(self.parent, bg="white", pady=2)
        label = tk.Label(
            outer,
            text=bubble_text,
            bg=bg_color,
            font=self.font,
            justify="left",
            anchor="w",
            wraplength=320,
            padx=10,
            pady=6
        )
        label.pack(side=align_side, anchor=align_anchor, padx=10)
        outer.pack(anchor=align_anchor, fill="x", padx=5, pady=2)

    def start_stream_bubble(self, role):
        bg_color = {
            "npc": "#ffcce5"
        }.get(role, "#eeeeee")

        outer = tk.Frame(self.parent, bg="white", pady=2)
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
        label.pack(side="left", anchor="w", padx=10)
        outer.pack(anchor="w", fill="x", padx=5, pady=2)

        debug_print("新建 stream 气泡")
        return label

    def _wrap_text(self, text):
        return "\n".join(textwrap.wrap(text, width=30))
