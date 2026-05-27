"""Sidebar — hamburger toggle: 280px ↔ 72px square items."""
from __future__ import annotations

import customtkinter as ctk

from gui.theme import (C, FONT, FONT_SMALL, FONT_CAPTION,
                       SIDEBAR_WIDTH, SIDEBAR_ITEM_HEIGHT, SIDEBAR_SECTION_HEIGHT)

COLLAPSED_WIDTH = SIDEBAR_ITEM_HEIGHT  # 72px


class Sidebar(ctk.CTkFrame):
    """Left navigation bar with hamburger toggle.
    Collapsed: 72px wide, icon-only square items.
    Expanded: 280px wide, icon + text.
    """

    def __init__(self, parent, on_select, width=SIDEBAR_WIDTH, **kw):
        super().__init__(parent, fg_color=C["sidebar_bg"], width=width,
                         corner_radius=0, **kw)
        self.pack_propagate(False)
        self.on_select = on_select
        self._items: list[dict] = []
        self._sections: list[dict] = []
        self._active_idx = 0
        self._collapsed = False
        self._expanded_width = width

        # ── Hamburger toggle ──
        self._toggle_frame = ctk.CTkFrame(self, fg_color=C["sidebar_bg"],
                                          height=SIDEBAR_ITEM_HEIGHT, corner_radius=0)
        self._toggle_frame.pack(fill="x")
        self._toggle_frame.pack_propagate(False)

        self._hamburger = ctk.CTkLabel(self._toggle_frame, text="☰",
                                        font=(FONT, 28), text_color=C["sidebar_fg"],
                                        cursor="hand2")
        self._hamburger.pack(expand=True)
        self._hamburger.bind("<Button-1>", lambda e: self.toggle())

        def _hb_enter(e):
            self._toggle_frame.configure(fg_color=C["sidebar_hover_bg"])
            self._hamburger.configure(fg_color=C["sidebar_hover_bg"])
        def _hb_leave(e):
            self._toggle_frame.configure(fg_color=C["sidebar_bg"])
            self._hamburger.configure(fg_color="transparent")
        self._toggle_frame.bind("<Enter>", _hb_enter)
        self._toggle_frame.bind("<Leave>", _hb_leave)
        self._hamburger.bind("<Enter>", _hb_enter)
        self._hamburger.bind("<Leave>", _hb_leave)

    def add_section(self, title: str):
        sep = ctk.CTkFrame(self, height=1, fg_color=C["sidebar_separator"],
                           corner_radius=0)
        sep.pack(fill="x")

        hdr = ctk.CTkFrame(self, fg_color=C["sidebar_bg"],
                           height=SIDEBAR_SECTION_HEIGHT, corner_radius=0)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text=title, font=(FONT, FONT_CAPTION, "bold"),
                     text_color=C["sidebar_section_fg"], anchor="w").pack(
                         fill="both", padx=24, pady=(14, 4))

        self._sections.append({"sep": sep, "hdr": hdr})

    def add_spacer(self):
        """Push subsequent items to the bottom."""
        spacer = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        spacer.pack(fill="both", expand=True)
        self._spacer = spacer

    def add_item(self, icon: str, label: str) -> int:
        idx = len(self._items)

        container = ctk.CTkFrame(self, fg_color=C["sidebar_bg"],
                                 height=SIDEBAR_ITEM_HEIGHT, corner_radius=0)
        container.pack(fill="x")
        container.pack_propagate(False)

        bar = ctk.CTkFrame(container, fg_color=C["sidebar_bg"], width=4,
                           corner_radius=0)
        bar.place(x=0, y=0, relheight=1)

        inner = ctk.CTkFrame(container, fg_color=C["sidebar_bg"])
        inner.pack(side="left", fill="both", expand=True, padx=(24, 16))

        icon_lbl = ctk.CTkLabel(inner, text=icon, font=(FONT, 24),
                                text_color=C["sidebar_fg"])
        icon_lbl.pack(side="left", padx=(0, 16))

        text_lbl = ctk.CTkLabel(inner, text=label, font=(FONT, FONT_SMALL),
                                text_color=C["sidebar_item_text"], anchor="w")
        text_lbl.pack(side="left", fill="x", expand=True, pady=16)

        for w in (container, inner, icon_lbl, text_lbl):
            w.bind("<Button-1>", lambda e, i=idx: self.set_active(i))
            w.bind("<Enter>", lambda e, c=container, i=idx: self._on_enter(c, i))
            w.bind("<Leave>", lambda e, c=container, i=idx: self._on_leave(c, i))
            w.configure(cursor="hand2")

        self._items.append({
            "container": container, "inner": inner, "bar": bar,
            "icon": icon_lbl, "text": text_lbl,
        })
        return idx

    # ── Toggle ─────────────────────────────────────────────────

    def toggle(self):
        """Toggle sidebar between expanded (280px) and collapsed (72px)."""
        self._collapsed = not self._collapsed

        if self._collapsed:
            self.configure(width=COLLAPSED_WIDTH)
            for item in self._items:
                item["text"].pack_forget()
                item["inner"].pack_forget()
                item["icon"].pack_forget()
                item["inner"].pack(side="left", fill="both", expand=True)
                item["icon"].pack(expand=True)
                item["icon"].configure(font=(FONT, 28))
            for sec in self._sections:
                sec["sep"].pack_forget()
                sec["hdr"].pack_forget()
            if hasattr(self, '_spacer'):
                self._spacer.pack_forget()
            self._hamburger.configure(text="☰", font=(FONT, 24))
        else:
            self.configure(width=self._expanded_width)
            for item in self._items:
                item["icon"].pack_forget()
                item["inner"].pack_forget()
                item["text"].pack_forget()
                item["inner"].pack(side="left", fill="both", expand=True,
                                   padx=(24, 16))
                item["icon"].pack(side="left", padx=(0, 16))
                item["text"].pack(side="left", fill="x", expand=True, pady=16)
                item["icon"].configure(font=(FONT, 24))
            for sec in self._sections:
                sec["sep"].pack(fill="x")
                sec["hdr"].pack(fill="x")
            if hasattr(self, '_spacer'):
                # Re-pack before the last item (⚙ settings) to keep it at the bottom
                last_container = self._items[-1]["container"]
                self._spacer.pack(fill="both", expand=True, before=last_container)
            self._hamburger.configure(text="☰", font=(FONT, 28))

    # ── Hover / Active ─────────────────────────────────────────

    def _on_enter(self, container, idx):
        if idx == self._active_idx:
            return
        item = self._items[idx]
        bg = C["sidebar_hover_bg"]
        for key in ("container", "inner", "icon", "text"):
            item[key].configure(fg_color=bg)
        container.configure(fg_color=bg)

    def _on_leave(self, container, idx):
        if idx == self._active_idx:
            return
        item = self._items[idx]
        bg = C["sidebar_bg"]
        for key in ("container", "inner", "icon", "text"):
            item[key].configure(fg_color=bg)
        container.configure(fg_color=bg)

    def set_active(self, idx: int):
        if idx == self._active_idx:
            return
        if self._active_idx < len(self._items):
            old = self._items[self._active_idx]
            old["container"].configure(fg_color=C["sidebar_bg"])
            old["inner"].configure(fg_color=C["sidebar_bg"])
            old["bar"].configure(fg_color=C["sidebar_bg"])
            old["icon"].configure(text_color=C["sidebar_fg"],
                                  fg_color=C["sidebar_bg"])
            old["text"].configure(text_color=C["sidebar_item_text"],
                                  fg_color=C["sidebar_bg"])
        self._active_idx = idx
        new = self._items[idx]
        new["container"].configure(fg_color=C["sidebar_active_bg"])
        new["inner"].configure(fg_color=C["sidebar_active_bg"])
        new["bar"].configure(fg_color=C["accent"])
        new["icon"].configure(text_color=C["sidebar_active_fg"],
                              fg_color=C["sidebar_active_bg"])
        new["text"].configure(text_color=C["sidebar_active_fg"],
                              fg_color=C["sidebar_active_bg"])
        self.on_select(idx)
