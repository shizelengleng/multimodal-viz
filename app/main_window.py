"""Main application window — custom chrome, layout, navigation, processing."""
from __future__ import annotations

import os
import queue
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk

from app.services import process_file
from gui.theme import (C, FONT, FONT_H2, FONT_CAPTION,
                       CTK_APPEARANCE_MODE, CTK_COLOR_THEME,
                       TITLE_BAR_HEIGHT, STATUS_BAR_HEIGHT,
                       WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT,
                       SPACING_MD, SPACING_LG, SPACING_SM)
from gui.sidebar import Sidebar
from gui.pages import InputPage, OutputPage, SettingsPage, ResultsPage
from gui.toast import Toast


def get_app_dir() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).parent.parent


def get_env_path() -> Path:
    return get_app_dir() / ".env"


def get_config_path() -> Path:
    return get_app_dir() / "config" / "settings.cfg"


def load_env_file() -> bool:
    env_path = get_env_path()
    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv(env_path, override=True)
        return True
    return False


def is_api_configured() -> bool:
    load_env_file()
    return bool(os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("MIMO_API_KEY"))


def get_active_provider() -> str:
    if os.environ.get("DEEPSEEK_API_KEY"):
        return "deepseek"
    if os.environ.get("MIMO_API_KEY"):
        return "mimo"
    return "deepseek"


class App:
    # ── Window edge grip size (for resize) ──
    GRIP_SIZE = 8

    def __init__(self, root=None):
        ctk.set_appearance_mode(CTK_APPEARANCE_MODE)
        ctk.set_default_color_theme(CTK_COLOR_THEME)

        if root is not None:
            self.root = root
        else:
            try:
                from tkinterdnd2 import TkinterDnD
                self.root = TkinterDnD.Tk()
            except ImportError:
                self.root = tk.Tk()

        # ── Custom window chrome ──
        self.root.overrideredirect(True)
        self.root.configure(bg=C["titlebar_bg"])

        # Add taskbar presence (WS_EX_APPWINDOW)
        self._add_taskbar_icon()

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        ww, wh = int(sw * 0.66), int(sh * 0.7)
        wx = (sw - ww) // 2
        wy = (sh - wh) // 2
        self.root.geometry(f"{ww}x{wh}+{wx}+{wy}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # Track window state
        self._maximized = False
        self._normal_geom = (ww, wh, wx, wy)

        self._output_dir = tk.StringVar()
        self._load_output_dir_pref()
        self._processing = False
        self._result_queue = queue.Queue()
        self._results: list[dict] = []

        self._build_ui()
        self._check_api_status()
        self._poll_queue()

    # ═══════════════════════════════════════════════════════════════
    # ── Config ──
    # ═══════════════════════════════════════════════════════════════

    def _load_output_dir_pref(self):
        cfg = get_config_path()
        out_dir = str(Path.home() / "Desktop")
        if cfg.exists():
            for line in cfg.read_text(encoding="utf-8").splitlines():
                if line.startswith("output_dir="):
                    out_dir = line.split("=", 1)[1].strip()
        self._output_dir.set(out_dir)

    def _save_output_dir_pref(self):
        cfg = get_config_path()
        cfg.parent.mkdir(parents=True, exist_ok=True)
        cfg.write_text(f"output_dir={self._output_dir.get()}\n", encoding="utf-8")

    # ═══════════════════════════════════════════════════════════════
    # ── Custom Window Chrome ──
    # ═══════════════════════════════════════════════════════════════

    def _build_title_bar(self):
        """Build a custom dark title bar with drag + window controls."""
        self._title_bar = tk.Frame(self.root, bg=C["titlebar_bg"],
                                   height=TITLE_BAR_HEIGHT, cursor="arrow")
        self._title_bar.pack(fill=tk.X)
        self._title_bar.pack_propagate(False)

        # Left: app icon
        tk.Label(self._title_bar, text="  📊", font=(FONT, 14), bg=C["titlebar_bg"],
                 fg=C["titlebar_fg"]).pack(side=tk.LEFT, pady=2)

        # Center: spacer (drag area)
        drag = tk.Frame(self._title_bar, bg=C["titlebar_bg"], cursor="fleur")
        drag.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right: window controls (pack ✕ first so it's rightmost: ─ □ ✕)
        self._max_btn = None
        for sym, cmd, hover in [
            ("✕", self.root.destroy,     C["titlebar_close_hover"]),
            ("□", self._toggle_maximize, C["titlebar_btn_hover"]),
            ("─", self._minimize,        C["titlebar_btn_hover"]),
        ]:
            btn = tk.Label(self._title_bar, text=sym, font=(FONT, 14),
                          bg=C["titlebar_bg"], fg=C["titlebar_fg"],
                          cursor="hand2", padx=16, anchor="center",
                          width=2, height=1)
            btn.pack(side=tk.RIGHT)
            btn.bind("<Button-1>", lambda e, c=cmd: c())
            btn.bind("<Enter>",
                     lambda e, b=btn, h=hover: b.config(bg=h, fg="#FFF"))
            btn.bind("<Leave>",
                     lambda e, b=btn: b.config(bg=C["titlebar_bg"],
                                               fg=C["titlebar_fg"]))
            if sym == "□":
                self._max_btn = btn

        # Drag bindings
        for w in (self._title_bar, drag):
            w.bind("<ButtonPress-1>", self._drag_start)
            w.bind("<B1-Motion>", self._drag_move)
        # Also bind on icon label
        for w in self._title_bar.winfo_children():
            if isinstance(w, tk.Label) and w.cget("text").strip() == "📊":
                w.bind("<ButtonPress-1>", self._drag_start)
                w.bind("<B1-Motion>", self._drag_move)
                break

        # Double-click title bar to maximize
        self._title_bar.bind("<Double-Button-1>", lambda e: self._toggle_maximize())

    def _build_resize_grips(self):
        """Add invisible resize grip at bottom-right corner."""
        grip = tk.Frame(self.root, bg=C["titlebar_bg"], cursor="bottom_right_corner",
                       width=self.GRIP_SIZE, height=self.GRIP_SIZE)
        grip.place(relx=1.0, rely=1.0, anchor="se")
        grip.bind("<ButtonPress-1>", self._resize_start)
        grip.bind("<B1-Motion>", self._resize_move)
        self._resize_grip = grip

    def _drag_start(self, event):
        self._drag_x = event.x_root
        self._drag_y = event.y_root

    def _drag_move(self, event):
        if self._maximized:
            return
        dx = event.x_root - self._drag_x
        dy = event.y_root - self._drag_y
        self.root.geometry(f"+{self.root.winfo_x() + dx}+{self.root.winfo_y() + dy}")
        self._drag_x = event.x_root
        self._drag_y = event.y_root

    def _resize_start(self, event):
        self._resize_x = event.x_root
        self._resize_y = event.y_root
        self._resize_w = self.root.winfo_width()
        self._resize_h = self.root.winfo_height()

    def _resize_move(self, event):
        if self._maximized:
            return
        dx = event.x_root - self._resize_x
        dy = event.y_root - self._resize_y
        nw = max(WINDOW_MIN_WIDTH, self._resize_w + dx)
        nh = max(WINDOW_MIN_HEIGHT, self._resize_h + dy)
        self.root.geometry(f"{nw}x{nh}")

    def _add_taskbar_icon(self):
        """Add WS_EX_APPWINDOW so the window appears in the taskbar."""
        import ctypes
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        hwnd = int(self.root.frame(), 16)
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_APPWINDOW)

    def _minimize(self):
        # iconify() is unreliable with overrideredirect; use Windows API
        import ctypes
        hwnd = int(self.root.frame(), 16)
        ctypes.windll.user32.ShowWindow(hwnd, 6)  # SW_MINIMIZE

    def _toggle_maximize(self):
        if self._maximized:
            w, h, x, y = self._normal_geom
            self.root.geometry(f"{w}x{h}+{x}+{y}")
            self._max_btn.config(text="□")
            self._maximized = False
        else:
            w, h = self.root.winfo_width(), self.root.winfo_height()
            x, y = self.root.winfo_x(), self.root.winfo_y()
            self._normal_geom = (w, h, x, y)
            self.root.geometry(
                f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
            self._max_btn.config(text="❐")
            self._maximized = True

    # ═══════════════════════════════════════════════════════════════
    # ── Build UI ──
    # ═══════════════════════════════════════════════════════════════

    def _build_ui(self):
        self._build_title_bar()

        # Main content shell (rounded bottom corners visually via bg)
        self._shell = tk.Frame(self.root, bg=C["bg"])
        self._shell.pack(fill=tk.BOTH, expand=True)

        # Body: sidebar + content
        body = ctk.CTkFrame(self._shell, fg_color=C["bg"], corner_radius=0)
        body.pack(fill=tk.BOTH, expand=True)

        # Sidebar separator
        ctk.CTkFrame(body, fg_color=C["sidebar_border"], width=1,
                     corner_radius=0).pack(side=tk.LEFT, fill=tk.Y)

        # Sidebar
        self._sidebar = Sidebar(body, on_select=self._on_sidebar_select)
        self._sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self._sidebar.add_item("📥", "输入文件")
        self._sidebar.add_item("📤", "输出设置")
        self._sidebar.add_item("✅", "生成结果")
        self._sidebar.add_spacer()
        self._sidebar.add_item("⚙", "API 设置")

        # Content area
        self._content_area = ctk.CTkFrame(body, fg_color=C["bg"], corner_radius=0)
        self._content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Pages
        self._input_page = InputPage(
            self._content_area,
            on_files_added=self._on_files_added,
            on_files_changed=self._on_file_count_changed,
        )
        self._mode_var = tk.StringVar(value="auto")
        self._output_page = OutputPage(
            self._content_area,
            output_dir=self._output_dir,
            on_start=self._start_processing,
            on_browse=self._browse_output_dir,
            on_open_dir=self._open_output_dir,
            mode_var=self._mode_var,
        )
        self._settings_page = SettingsPage(
            self._content_area,
            on_saved=self._check_api_status,
        )
        self._results_page = ResultsPage(self._content_area)

        self._pages = [
            self._input_page,
            self._output_page,
            self._results_page,
            self._settings_page,
        ]

        self._show_page(0)
        self._sidebar.set_active(0)

        # Status bar
        status_bar = tk.Frame(self._shell, bg=C["sep"], height=STATUS_BAR_HEIGHT)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        status_bar.pack_propagate(False)
        self._api_status = tk.Label(status_bar, text="● 检测中...",
                                    font=(FONT, FONT_CAPTION), bg=C["sep"],
                                    fg=C["status_dot_checking"])
        self._api_status.pack(side=tk.LEFT, padx=SPACING_MD)
        self._file_count_label = tk.Label(status_bar, text="",
                                          font=(FONT, FONT_CAPTION), bg=C["sep"],
                                          fg=C["text_light"])
        self._file_count_label.pack(side=tk.RIGHT, padx=SPACING_MD)

        self._build_resize_grips()

    # ═══════════════════════════════════════════════════════════════
    # ── Navigation ──
    # ═══════════════════════════════════════════════════════════════

    def _on_sidebar_select(self, idx: int):
        self._show_page(idx)

    def _show_page(self, idx: int):
        for pg in self._pages:
            pg.pack_forget()
        self._pages[idx].pack(fill=tk.BOTH, expand=True)

    # ── File management ──

    def _on_files_added(self, paths: list[Path]):
        self._input_page._file_list.add_files(paths)

    def _on_file_count_changed(self, count: int):
        self._input_page.update_drop_zone(count)
        self._file_count_label.config(text=f"📄 {count} 个文件" if count > 0 else "")

    # ── API status ──

    def _check_api_status(self):
        if is_api_configured():
            p = get_active_provider()
            name = "DeepSeek" if p == "deepseek" else "MiMo"
            self._api_status.config(text=f"● {name} 已连接", fg=C["accent"])
            self._output_page.set_start_enabled(True)
        else:
            self._api_status.config(text="● 未配置 API Key", fg=C["danger"])
            self._output_page.set_start_enabled(False)

    # ── Processing ──

    def _start_processing(self):
        if self._processing:
            return
        files = self._input_page.files
        if not files:
            Toast.warning(self.root, "请先在「📥 输入」页面添加文件")
            return
        if not is_api_configured():
            Toast.error(self.root, "请先在「⚙ 设置」页面配置 API Key", duration=4000)
            self._sidebar.set_active(3)
            self._show_page(3)
            return

        output_dir = Path(self._output_dir.get())
        self._save_output_dir_pref()
        output_dir.mkdir(parents=True, exist_ok=True)

        self._processing = True
        self._output_page.set_start_text("⏳ 处理中...")
        self._output_page.set_start_enabled(False)
        self._results_page.clear()
        self._output_page.start_indeterminate()
        self._output_page.set_status("📖 准备处理...")
        self._results.clear()

        self._sidebar.set_active(2)
        self._show_page(2)

        mode = self._mode_var.get()
        threading.Thread(target=self._process_files,
                         args=(files, output_dir, mode), daemon=True).start()

    def _process_files(self, files: list[Path], output_dir: Path, mode: str = "auto"):
        total = len(files)

        def on_status(msg):
            self._result_queue.put(("status", msg))

        for i, fp in enumerate(files):
            self._result_queue.put(("status", f"处理中 ({i+1}/{total}): {fp.name}"))
            try:
                result = process_file(fp, output_dir, mode=mode, status_callback=on_status)
                if result:
                    self._result_queue.put(("done", result))
                else:
                    self._result_queue.put(("error", f"跳过空文件: {fp.name}"))
            except Exception as e:
                err_msg = str(e)
                if "401" in err_msg or "Unauthorized" in err_msg:
                    self._result_queue.put(("auth_error", "API Key 无效"))
                elif "Connection" in err_msg or "timeout" in err_msg.lower():
                    self._result_queue.put(("error", f"网络错误: {fp.name} — {err_msg}"))
                else:
                    self._result_queue.put(("error", f"处理失败: {fp.name} — {err_msg}"))

        self._result_queue.put(("finished", None))

    def _poll_queue(self):
        try:
            while True:
                msg_type, payload = self._result_queue.get_nowait()
                if msg_type == "status":
                    self._output_page.set_status(payload)
                elif msg_type == "done":
                    self._results.append(payload)
                    self._results_page.append_result(payload)
                    d, t = len(self._results), len(self._input_page.files)
                    self._file_count_label.config(text=f"✅ {d}/{t} 已处理")
                elif msg_type == "error":
                    self._results_page.append_log(f"✗ {payload}\n")
                elif msg_type == "auth_error":
                    self.root.after(0, lambda: Toast.error(
                        self.root, "API Key 无效，请在「⚙ 设置」页面重新配置"))
                    self._results_page.append_log(f"✗ {payload}\n")
                elif msg_type == "finished":
                    self._processing = False
                    self._output_page.set_start_text("▶  开始生成")
                    self._output_page.set_start_enabled(True)
                    self._output_page.stop_indeterminate()
                    self._output_page.set_status("✓ 全部完成")
        except queue.Empty:
            pass
        self.root.after(100, self._poll_queue)

    # ── Output directory ──

    def _browse_output_dir(self):
        d = filedialog.askdirectory(title="选择输出目录",
                                    initialdir=self._output_dir.get())
        if d:
            self._output_dir.set(d)
            self._save_output_dir_pref()

    def _open_output_dir(self):
        d = Path(self._output_dir.get())
        if d.exists():
            os.startfile(str(d))
        else:
            Toast.info(self.root, "输出目录尚未创建")

    # ── Run ──

    def run(self):
        load_env_file()
        if not is_api_configured():
            self._show_page(3)
            self._sidebar.set_active(3)
        self.root.mainloop()
