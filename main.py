"""Multimodal Knowledge Graph Viz — Desktop GUI Application."""
from __future__ import annotations

import os
import sys
import tkinter as tk

if sys.platform == 'win32':
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, 'reconfigure'):
            try:
                s.reconfigure(encoding='utf-8', errors='replace')
            except Exception:
                pass
    os.environ.setdefault('PYTHONUTF8', '1')
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')

if not getattr(sys, 'frozen', False):
    sys.path.insert(0, str(__file__).rstrip("main.py"))

FONT = "Microsoft YaHei"


class SplashScreen:
    """Small loading window shown during app startup."""

    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.win.overrideredirect(True)
        self.win.attributes('-topmost', True)
        self.win.configure(bg="#2C3E35")

        w, h = 360, 200
        sw = self.win.winfo_screenwidth()
        sh = self.win.winfo_screenheight()
        self.win.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        # Prevent this Toplevel from appearing in taskbar
        self.win.attributes('-toolwindow', True)

        tk.Label(self.win, text="📊", font=(FONT, 36), bg="#2C3E35",
                 fg="#FFFFFF").pack(pady=(32, 0))
        tk.Label(self.win, text="知识图谱可视化生成器",
                 font=(FONT, 16, "bold"), bg="#2C3E35",
                 fg="#CCD5CF").pack()
        tk.Label(self.win, text="v0.5.3", font=(FONT, 10),
                 bg="#2C3E35", fg="#7A8A7A").pack(pady=(2, 14))

        from customtkinter import CTkProgressBar
        self.bar = CTkProgressBar(self.win, width=280, height=6,
                                  fg_color="#3D5448",
                                  progress_color="#2F8D63",
                                  corner_radius=3,
                                  mode="determinate")
        self.bar.pack()
        self.bar.start()

        tk.Label(self.win, text="正在加载...", font=(FONT, 10),
                 bg="#2C3E35", fg="#7A8A7A").pack(pady=(8, 0))

    def destroy(self):
        self.bar.stop()
        self.win.destroy()


def main():
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    # Create root Tk first (prevents auto-root from Toplevel)
    try:
        from tkinterdnd2 import TkinterDnD
        root = TkinterDnD.Tk()
    except ImportError:
        root = tk.Tk()

    # Hide root until fully built — position off-screen at 1x1
    root.geometry("1x1+-200+-200")
    root.withdraw()

    splash = SplashScreen(root)
    splash.win.update()  # force full paint before heavy imports

    from app.main_window import App
    app = App(root=root)
    splash.destroy()
    root.deiconify()  # show the ready window
    app.run()


if __name__ == "__main__":
    main()
