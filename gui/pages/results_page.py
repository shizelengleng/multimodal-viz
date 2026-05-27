"""Results page: processing output display."""
from __future__ import annotations

from pathlib import Path

import customtkinter as ctk

from gui.theme import C, FONT, FONT_MONO, FONT_H2, FONT_BODY, FONT_SMALL
from gui.theme import SPACING_XS, SPACING_SM, SPACING_MD, SPACING_LG, SPACING_XL
from gui.theme import RADIUS_MD


class ResultsPage(ctk.CTkFrame):
    """Page 2: processing results display."""

    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color=C["bg"], **kw)

        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(anchor="w", padx=SPACING_XL, pady=(SPACING_LG, SPACING_XS))
        ctk.CTkLabel(hdr, text="✅", font=(FONT, 32)).pack(side="left")
        ctk.CTkLabel(hdr, text="生成结果", font=(FONT, FONT_H2, "bold"),
                     text_color=C["text"]).pack(side="left", padx=(SPACING_SM, 0))
        ctk.CTkLabel(self, text="处理进度和生成文件列表",
                     font=(FONT, FONT_SMALL), text_color=C["text_light"]).pack(
                         anchor="w", padx=SPACING_XL)

        scroll = ctk.CTkScrollableFrame(self, fg_color=C["bg"],
                                        corner_radius=0,
                                        scrollbar_fg_color=C["bg"],
                                        scrollbar_button_color=C["text_light"],
                                        scrollbar_button_hover_color=C["text_secondary"])
        scroll.pack(fill="both", expand=True, padx=(SPACING_XL, SPACING_SM),
                    pady=(SPACING_MD, 0))

        card = ctk.CTkFrame(scroll, fg_color=C["card_bg"], corner_radius=RADIUS_MD,
                            border_width=1, border_color=C["card_border"])
        card.pack(fill="x", pady=(0, SPACING_LG))

        self._text = ctk.CTkTextbox(card, font=(FONT_MONO, FONT_BODY),
                                    fg_color=C["card_bg"],
                                    text_color=C["text_secondary"],
                                    wrap="word", border_width=0,
                                    corner_radius=RADIUS_MD,
                                    height=480)
        self._text.pack(fill="both", expand=True, padx=SPACING_SM, pady=SPACING_SM)
        self._text.configure(state="disabled")

    def clear(self):
        self._text.configure(state="normal")
        self._text.delete("1.0", "end")
        self._text.configure(state="disabled")

    def append_result(self, result: dict):
        self._text.configure(state="normal")
        stem = Path(result["input"]).stem
        self._text.insert("end",
            f"✓ {stem}.html  ·  {result['concepts']} 概念, {result['relations']} 关系\n")
        self._text.see("end")
        self._text.configure(state="disabled")

    def append_log(self, text: str):
        self._text.configure(state="normal")
        self._text.insert("end", text)
        self._text.see("end")
        self._text.configure(state="disabled")
