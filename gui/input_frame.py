# gui/input_frame.py
import tkinter as tk

class InputFrame(tk.Frame):
    def __init__(self, master, callback):
        super().__init__(master)
        self.entry = tk.Entry(self)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", lambda e: self.on_send())
        tk.Button(self, text="发送", command=self.on_send).pack(side=tk.RIGHT)
        self.callback = callback

    def on_send(self):
        text = self.entry.get().strip()
        if text:
            self.callback(text)
            self.entry.delete(0, tk.END)
