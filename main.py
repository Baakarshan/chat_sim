# main.py

from gui.window import Window

def main():
    app = Window()
    app.mainloop()  # ✅ Tkinter 正确的主循环启动方式

if __name__ == "__main__":
    main()
