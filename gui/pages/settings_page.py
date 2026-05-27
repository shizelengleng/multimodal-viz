"""Settings page: API provider and key management."""
from __future__ import annotations

import os
import sys
import tkinter as tk
from pathlib import Path

import customtkinter as ctk

from gui.theme import C, FONT, FONT_MONO, FONT_H2, FONT_H3, FONT_BODY, FONT_SMALL, FONT_CAPTION
from gui.theme import SPACING_XS, SPACING_SM, SPACING_MD, SPACING_LG, SPACING_XL
from gui.theme import RADIUS_MD
from gui.toast import Toast


class SettingsPage(ctk.CTkFrame):
    """Page 3: API provider and key management."""

    def __init__(self, parent, on_saved, **kw):
        super().__init__(parent, fg_color=C["bg"], **kw)
        self._on_saved = on_saved

        from dotenv import load_dotenv
        env_path = self._get_env_path()
        if env_path.exists():
            load_dotenv(env_path, override=True)
        ds_key = os.environ.get("DEEPSEEK_API_KEY", "")
        mo_key = os.environ.get("MIMO_API_KEY", "")
        provider = "deepseek" if ds_key else ("mimo" if mo_key else "deepseek")

        # ── Fixed header ──
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(anchor="w", padx=SPACING_XL, pady=(SPACING_LG, SPACING_XS))
        ctk.CTkLabel(hdr, text="⚙", font=(FONT, 32)).pack(side="left")
        ctk.CTkLabel(hdr, text="设置", font=(FONT, FONT_H2, "bold"),
                     text_color=C["text"]).pack(side="left", padx=(SPACING_SM, 0))
        ctk.CTkLabel(self, text="配置 AI 服务以开始提取知识图谱",
                     font=(FONT, FONT_SMALL), text_color=C["text_light"]).pack(
                         anchor="w", padx=SPACING_XL)

        # ── Scrollable content ──
        scroll = ctk.CTkScrollableFrame(self, fg_color=C["bg"],
                                        corner_radius=0,
                                        scrollbar_fg_color=C["bg"],
                                        scrollbar_button_color=C["text_light"],
                                        scrollbar_button_hover_color=C["text_secondary"])
        scroll.pack(fill="both", expand=True, padx=(SPACING_XL, SPACING_SM),
                    pady=(SPACING_MD, 0))

        # Provider card
        card1 = ctk.CTkFrame(scroll, fg_color=C["card_bg"], corner_radius=RADIUS_MD,
                             border_width=1, border_color=C["card_border"])
        card1.pack(fill="x", pady=(0, SPACING_MD))

        ctk.CTkLabel(card1, text="API 提供商", font=(FONT, FONT_H3, "bold"),
                     text_color=C["text"]).pack(anchor="w", padx=SPACING_LG,
                                                pady=(SPACING_LG, 0))
        ctk.CTkLabel(card1, text="选择用于提取知识图谱的 AI 服务",
                     font=(FONT, FONT_CAPTION), text_color=C["text_light"]).pack(
                         anchor="w", padx=SPACING_LG, pady=(2, SPACING_SM))

        self._provider_var = tk.StringVar(value=provider)
        r1 = ctk.CTkFrame(card1, fg_color="transparent")
        r1.pack(fill="x", padx=SPACING_LG, pady=(0, SPACING_LG))

        ctk.CTkRadioButton(r1, text="DeepSeek  —  推荐 · 性价比高 · 中文优化",
                          variable=self._provider_var, value="deepseek",
                          font=(FONT, FONT_BODY), fg_color=C["accent"],
                          command=lambda: self._on_provider_change()).pack(anchor="w")
        ctk.CTkRadioButton(r1, text="MiMo  —  v2.5 · 多模态理解 · 知识提取",
                          variable=self._provider_var, value="mimo",
                          font=(FONT, FONT_BODY), fg_color=C["accent"],
                          command=lambda: self._on_provider_change()).pack(anchor="w", pady=(6, 0))

        # Divider
        ctk.CTkFrame(scroll, height=1, fg_color=C["sep"]).pack(
            fill="x", pady=(SPACING_XS, SPACING_MD))

        # Keys card
        card2 = ctk.CTkFrame(scroll, fg_color=C["card_bg"], corner_radius=RADIUS_MD,
                             border_width=1, border_color=C["card_border"])
        card2.pack(fill="x", pady=(0, SPACING_MD))

        # DeepSeek key
        ctk.CTkLabel(card2, text="DeepSeek API Key", font=(FONT, FONT_SMALL, "bold"),
                     text_color=C["text_secondary"]).pack(anchor="w", padx=SPACING_LG,
                                                          pady=(SPACING_LG, 0))
        self._ds_show = False
        self._ds_var = tk.StringVar(value=ds_key)
        ds_row = ctk.CTkFrame(card2, fg_color="transparent")
        ds_row.pack(fill="x", padx=SPACING_LG, pady=(SPACING_XS, 2))
        self._ds_entry = ctk.CTkEntry(ds_row, textvariable=self._ds_var, show="*",
                                       font=(FONT_MONO, FONT_BODY), height=36)
        self._ds_entry.pack(side=tk.LEFT, fill="x", expand=True)

        ds_eye = ctk.CTkButton(ds_row, text="👁", width=44, height=36,
                               fg_color=C["btn_secondary_bg"],
                               hover_color=C["btn_secondary_hover_bg"],
                               text_color=C["text_hint"],
                               command=lambda: self._toggle_ds())
        ds_eye.pack(side=tk.RIGHT, padx=(SPACING_SM, 0))

        ctk.CTkLabel(card2, text="platform.deepseek.com → API Keys",
                     font=(FONT, FONT_CAPTION), text_color=C["text_hint"]).pack(
                         anchor="w", padx=SPACING_LG, pady=(0, SPACING_LG))

        # MiMo key
        ctk.CTkLabel(card2, text="MiMo API Key", font=(FONT, FONT_SMALL, "bold"),
                     text_color=C["text_secondary"]).pack(anchor="w", padx=SPACING_LG)
        self._mo_show = False
        self._mo_var = tk.StringVar(value=mo_key)
        mo_row = ctk.CTkFrame(card2, fg_color="transparent")
        mo_row.pack(fill="x", padx=SPACING_LG, pady=(SPACING_XS, 2))
        self._mo_entry = ctk.CTkEntry(mo_row, textvariable=self._mo_var, show="*",
                                       font=(FONT_MONO, FONT_BODY), height=36)
        self._mo_entry.pack(side=tk.LEFT, fill="x", expand=True)

        mo_eye = ctk.CTkButton(mo_row, text="👁", width=44, height=36,
                               fg_color=C["btn_secondary_bg"],
                               hover_color=C["btn_secondary_hover_bg"],
                               text_color=C["text_hint"],
                               command=lambda: self._toggle_mo())
        mo_eye.pack(side=tk.RIGHT, padx=(SPACING_SM, 0))

        ctk.CTkLabel(card2, text="platform.xiaomimimo.com → API Keys",
                     font=(FONT, FONT_CAPTION), text_color=C["text_hint"]).pack(
                         anchor="w", padx=SPACING_LG, pady=(0, SPACING_LG))

        # Save button
        self._save_btn = ctk.CTkButton(card2, text="保存设置",
                                        font=(FONT, FONT_H3, "bold"),
                                        height=42, command=self._save,
                                        fg_color=C["accent"],
                                        hover_color=C["accent_hover"])
        self._save_btn.pack(anchor="w", padx=SPACING_LG, pady=(0, SPACING_LG))

        # App info
        info_card = ctk.CTkFrame(scroll, fg_color=C["card_bg"], corner_radius=RADIUS_MD,
                                 border_width=1, border_color=C["card_border"])
        info_card.pack(fill="x")

        ctk.CTkLabel(info_card, text="多模态知识图谱可视化生成器",
                     font=(FONT, FONT_BODY, "bold"), text_color=C["accent"]).pack(
                         anchor="w", padx=SPACING_LG, pady=(SPACING_LG, 0))
        ctk.CTkLabel(info_card, text="文本/PDF → 知识图谱 → 交互式 HTML",
                     font=(FONT, FONT_CAPTION), text_color=C["text_light"]).pack(
                         anchor="w", padx=SPACING_LG)
        ctk.CTkLabel(info_card, text="开发者：矢泽冷冷",
                     font=(FONT, FONT_CAPTION), text_color=C["text_hint"]).pack(
                         anchor="w", padx=SPACING_LG)
        ctk.CTkLabel(info_card, text="模型：DeepSeek V4 Pro + MiMo v2.5",
                     font=(FONT, FONT_CAPTION), text_color=C["text_hint"]).pack(
                         anchor="w", padx=SPACING_LG, pady=(0, SPACING_LG))

    def _toggle_ds(self):
        self._ds_show = not self._ds_show
        self._ds_entry.configure(show="" if self._ds_show else "*")

    def _toggle_mo(self):
        self._mo_show = not self._mo_show
        self._mo_entry.configure(show="" if self._mo_show else "*")

    def _on_provider_change(self):
        pass

    def _get_env_path(self) -> Path:
        if getattr(sys, 'frozen', False):
            return Path(sys.executable).parent / ".env"
        return Path(__file__).parent.parent.parent / ".env"

    def _save(self):
        lines = []
        ds = self._ds_var.get().strip()
        mo = self._mo_var.get().strip()
        if ds:
            lines.append(f"DEEPSEEK_API_KEY={ds}")
        if mo:
            lines.append(f"MIMO_API_KEY={mo}")
        env_path = self._get_env_path()
        env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        from dotenv import load_dotenv
        load_dotenv(env_path, override=True)
        Toast.success(self.winfo_toplevel(), "设置已保存")
        self._on_saved()
