"""Output page: directory selection, mode selector, progress."""
from __future__ import annotations

import tkinter as tk

import customtkinter as ctk

from gui.theme import C, FONT, FONT_H2, FONT_H3, FONT_BODY, FONT_SMALL, FONT_CAPTION
from gui.theme import SPACING_XS, SPACING_SM, SPACING_MD, SPACING_LG, SPACING_XL, SPACING_XXL
from gui.theme import RADIUS_MD


class OutputPage(ctk.CTkFrame):
    """Page 1: output directory, mode selector, action buttons, progress."""

    def __init__(self, parent, output_dir: tk.StringVar, on_start, on_browse, on_open_dir,
                 mode_var: tk.StringVar | None = None, **kw):
        super().__init__(parent, fg_color=C["bg"], **kw)
        self._output_dir = output_dir
        self._on_start = on_start
        self._on_browse = on_browse
        self._on_open_dir = on_open_dir
        self._mode_var = mode_var or tk.StringVar(value="auto")

        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(anchor="w", padx=SPACING_XL, pady=(SPACING_LG, SPACING_XS))
        ctk.CTkLabel(hdr, text="📤", font=(FONT, 32)).pack(side="left")
        ctk.CTkLabel(hdr, text="输出设置", font=(FONT, FONT_H2, "bold"),
                     text_color=C["text"]).pack(side="left", padx=(SPACING_SM, 0))
        ctk.CTkLabel(self, text="选择知识图谱生成结果的保存位置",
                     font=(FONT, FONT_SMALL), text_color=C["text_light"]).pack(
                         anchor="w", padx=SPACING_XL)

        # ── Output directory card ──
        card = ctk.CTkFrame(self, fg_color=C["card_bg"], corner_radius=RADIUS_MD,
                            border_width=1, border_color=C["card_border"])
        card.pack(fill="x", padx=SPACING_XL, pady=(SPACING_MD, SPACING_MD))

        ctk.CTkLabel(card, text="生成产物保存位置", font=(FONT, FONT_H3, "bold"),
                     text_color=C["text"]).pack(anchor="w", padx=SPACING_LG, pady=(SPACING_LG, 0))
        ctk.CTkLabel(card, text="知识图谱 HTML、JSON 数据和叙述文章将保存到此目录",
                     font=(FONT, FONT_CAPTION), text_color=C["text_light"]).pack(
                         anchor="w", padx=SPACING_LG, pady=(2, SPACING_SM))

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=SPACING_LG, pady=(0, SPACING_LG))

        self._out_entry = ctk.CTkEntry(row, textvariable=output_dir, font=(FONT, FONT_BODY),
                                       height=38)
        self._out_entry.pack(side=tk.LEFT, fill="x", expand=True)

        self._browse_btn = ctk.CTkButton(row, text="📁  浏览", font=(FONT, FONT_BODY),
                                          width=100, command=self._on_browse,
                                          fg_color=C["accent"], hover_color=C["accent_hover"])
        self._browse_btn.pack(side=tk.RIGHT, padx=(SPACING_SM, 0))

        # ── Mode selector card ──
        mode_card = ctk.CTkFrame(self, fg_color=C["card_bg"], corner_radius=RADIUS_MD,
                                 border_width=1, border_color=C["card_border"])
        mode_card.pack(fill="x", padx=SPACING_XL, pady=(0, SPACING_MD))

        ctk.CTkLabel(mode_card, text="📊  可视化模式", font=(FONT, FONT_H3, "bold"),
                     text_color=C["text"]).pack(anchor="w", padx=SPACING_LG, pady=(SPACING_LG, 0))
        ctk.CTkLabel(mode_card, text="选择知识图谱的展示布局和结构方式",
                     font=(FONT, FONT_CAPTION), text_color=C["text_light"]).pack(
                         anchor="w", padx=SPACING_LG, pady=(2, SPACING_MD))

        modes = [
            ("concept-map", "🕸", "概念图", "力导向布局，概念自由展开"),
            ("mind-map", "🧠", "思维导图", "中心辐射，分支延展"),
            ("flowchart", "📋", "流程图", "层级递进，步骤清晰"),
            ("timeline", "📅", "时间线", "时间序列，事件串联"),
            ("auto", "🤖", "自动", "AI 自动选择最佳布局"),
        ]

        mode_row = ctk.CTkFrame(mode_card, fg_color="transparent")
        mode_row.pack(fill="x", padx=SPACING_LG, pady=(0, SPACING_LG))

        self._mode_frames: list[dict] = []
        for i, (value, icon, name, desc) in enumerate(modes):
            frm = ctk.CTkFrame(mode_row, fg_color=C["mode_card_bg"],
                               corner_radius=RADIUS_MD, border_width=1,
                               border_color=C["mode_card_border"])
            frm.pack(side=tk.LEFT, fill="x", expand=True,
                     padx=(0 if i == 0 else SPACING_XS, SPACING_XS if i == 4 else 0))

            ctk.CTkLabel(frm, text=f"{icon}  {name}",
                         font=(FONT, FONT_SMALL, "bold"),
                         text_color=C["mode_card_text"]).pack(pady=(SPACING_SM, 0))
            ctk.CTkLabel(frm, text=desc, font=(FONT, FONT_CAPTION),
                         text_color=C["mode_card_desc"]).pack(pady=(2, SPACING_SM))

            for child in frm.winfo_children():
                child.bind("<Button-1>", lambda e, v=value: self._select_mode(v))
                child.configure(cursor="hand2")

            self._mode_frames.append({"frame": frm, "value": value})

        self._select_mode("auto")

        # ── Action buttons ──
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(fill="x", padx=SPACING_XL, pady=SPACING_LG)

        self._start_btn = ctk.CTkButton(btn_row, text="▶  开始生成",
                                         font=(FONT, FONT_H3, "bold"),
                                         height=48, command=self._on_start,
                                         fg_color=C["accent"],
                                         hover_color=C["accent_hover"])
        self._start_btn.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, SPACING_SM))

        self._open_btn = ctk.CTkButton(btn_row, text="📁  打开输出目录",
                                        font=(FONT, FONT_H3), height=48,
                                        command=self._on_open_dir,
                                        fg_color=C["btn_secondary_bg"],
                                        hover_color=C["btn_secondary_hover_bg"],
                                        text_color=C["btn_secondary_fg"])
        self._open_btn.pack(side=tk.LEFT, fill="x", expand=True, padx=(SPACING_SM, 0))

        # ── Progress ──
        self._progress = ctk.CTkProgressBar(self, height=8,
                                            fg_color=C["accent_light"],
                                            progress_color=C["accent"],
                                            mode="determinate")
        self._progress.pack(fill="x", padx=SPACING_XL, pady=(SPACING_XS, 0))
        self._progress.set(0)

        self._status_label = ctk.CTkLabel(self, text="", font=(FONT, FONT_CAPTION),
                                          text_color=C["text_light"])
        self._status_label.pack(anchor="w", padx=SPACING_XL, pady=(2, 0))

    def set_progress(self, value: float):
        self._progress.set(value / 100)

    def set_status(self, text: str):
        self._status_label.configure(text=text)

    def start_indeterminate(self):
        self._progress.set(0)
        self._progress.start()

    def stop_indeterminate(self):
        self._progress.stop()
        self._progress.set(1.0)

    def set_start_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self._start_btn.configure(state=state)

    def set_start_text(self, text: str):
        self._start_btn.configure(text=text)

    def get_mode(self) -> str:
        return self._mode_var.get()

    def _select_mode(self, value: str):
        self._mode_var.set(value)
        for item in self._mode_frames:
            is_sel = item["value"] == value
            fg = C["mode_card_selected_bg"] if is_sel else C["mode_card_bg"]
            bc = C["mode_card_selected_border"] if is_sel else C["mode_card_border"]
            tc = C["mode_card_selected_text"] if is_sel else C["mode_card_text"]
            frm = item["frame"]
            frm.configure(fg_color=fg, border_color=bc)
            for child in frm.winfo_children():
                if isinstance(child, ctk.CTkLabel):
                    child.configure(text_color=tc)
