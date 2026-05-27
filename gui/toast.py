"""Toast notification system — auto-dismissing overlays."""
from __future__ import annotations

import tkinter as tk

import customtkinter as ctk

from gui.theme import C, FONT


class Toast:
    """Lightweight, auto-dismissing notification positioned at bottom-right.

    Usage:
        Toast.success(parent, "设置已保存")
        Toast.error(parent, "API Key 无效")
        Toast.warning(parent, "请先添加文件")
        Toast.info(parent, "处理中...")
    """

    _active: list[tk.Toplevel] = []

    @classmethod
    def _show(cls, parent, title: str, message: str, bar_color: str,
              duration: int = 2500):
        top = tk.Toplevel(parent)
        top.overrideredirect(True)
        top.attributes("-topmost", True)
        top.configure(bg=C["card_bg"], highlightbackground=C["toast_border"],
                      highlightthickness=1)

        # Colored left bar
        bar = ctk.CTkFrame(top, fg_color=bar_color, width=4, corner_radius=0)
        bar.pack(side=tk.LEFT, fill=tk.Y)

        body = ctk.CTkFrame(top, fg_color=C["card_bg"])
        body.pack(side=tk.LEFT, fill=tk.BOTH, padx=16, pady=12)

        ctk.CTkLabel(body, text=title, font=(FONT, 10, "bold"),
                     text_color=C["text"]).pack(anchor="w")
        if message:
            ctk.CTkLabel(body, text=message, font=(FONT, 9),
                         text_color=C["text_light"], wraplength=300).pack(
                             anchor="w", pady=(2, 0))

        # Position at bottom-right of parent
        top.update_idletasks()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        tw = top.winfo_reqwidth()
        th = top.winfo_reqheight()

        x = px + pw - tw - 24
        y = py + ph - th - 36 - len(cls._active) * (th + 12)
        top.geometry(f"{tw}x{th}+{x}+{y}")

        cls._active.append(top)

        def dismiss():
            if top in cls._active:
                cls._active.remove(top)
            try:
                top.destroy()
            except tk.TclError:
                pass

        def _fade(step=10):
            if top not in cls._active:
                return
            nonlocal alpha
            alpha = max(0.0, alpha - 0.1)
            if alpha <= 0.0:
                dismiss()
            else:
                try:
                    top.attributes("-alpha", alpha)
                    top.after(40, lambda: _fade(step))
                except tk.TclError:
                    pass

        if duration > 0:
            alpha = 1.0
            top.after(duration, lambda: _fade())

        for w in (top, bar, body):
            w.bind("<Button-1>", lambda e: dismiss())
        for child in body.winfo_children():
            child.bind("<Button-1>", lambda e: dismiss())

    @classmethod
    def success(cls, parent, message: str, duration: int = 2500):
        cls._show(parent, "✓  成功", message, C["toast_success_bar"], duration)

    @classmethod
    def error(cls, parent, message: str, duration: int = 4000):
        cls._show(parent, "✗  错误", message, C["toast_error_bar"], duration)

    @classmethod
    def warning(cls, parent, message: str, duration: int = 3000):
        cls._show(parent, "⚠  提示", message, C["toast_warning_bar"], duration)

    @classmethod
    def info(cls, parent, message: str, duration: int = 2000):
        cls._show(parent, "ℹ  信息", message, C["toast_info_bar"], duration)
