# gui/chat_bubble.py

import tkinter as tk

class ChatBubbleManager:
    def __init__(self, parent, font):
        self.parent = parent
        self.font = font

    def create_bubble(self, role, text):
        bg_color = {"system": "#f0f0f0", "user": "#cce5ff", "npc": "#ffcce5"}.get(role, "#eeeeee")
        align = "w" if role in ["npc", "system"] else "e"
        side = "left" if align == "w" else "right"

        outer = tk.Frame(self.parent, bg="white", pady=2)
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
        label.pack(side=side, anchor=align, padx=10)
        outer.pack(anchor=align, fill="x", padx=5, pady=2)

    def start_stream_bubble(self, role):
        bg_color = {"npc": "#ffcce5"}.get(role, "#eeeeee")
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
        return label
