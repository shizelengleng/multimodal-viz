"""Reusable widgets: DropZone and FileList."""
from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk

from gui.theme import C, FONT, FONT_H2, FONT_H3, FONT_SMALL, FONT_CAPTION
from gui.theme import RADIUS_LG, SPACING_XS, SPACING_SM, DROPZONE_HEIGHT, FILELIST_HEIGHT


class DropZone(ctk.CTkFrame):
    """Drag-and-drop area with rounded border. Accepts .txt/.md/.pdf."""

    def __init__(self, parent, on_files_added, **kw):
        super().__init__(parent, corner_radius=RADIUS_LG, border_width=2,
                         border_color=C["drop_border"], fg_color=C["drop_bg"], **kw)
        self.on_files_added = on_files_added
        self._file_count = 0

        self.configure(height=DROPZONE_HEIGHT)

        # Inner container for centering
        self._inner = ctk.CTkFrame(self, fg_color="transparent")
        self._inner.pack(expand=True, fill=tk.BOTH)

        self._icon = ctk.CTkLabel(self._inner, text="", font=(FONT, 44),
                                  text_color=C["drop_icon"])
        self._icon.pack(pady=(48, 0))

        self._title = ctk.CTkLabel(self._inner, text="", font=(FONT, FONT_H2, "bold"),
                                   text_color=C["accent"])
        self._title.pack(pady=(8, 0))

        self._subtitle = ctk.CTkLabel(self._inner, text="", font=(FONT, FONT_SMALL))
        self._subtitle.pack()

        self._hint = ctk.CTkLabel(self._inner, text="", font=(FONT, FONT_CAPTION),
                                  text_color=C["text_hint"])
        self._hint.pack()

        self._set_state("idle")

        self._inner.bind("<Button-1>", self._on_click)
        self._inner.bind("<Enter>", lambda e: self._set_state(
            "hover" if self._file_count == 0 else "has_files"))
        self._inner.bind("<Leave>", lambda e: self._set_state(
            "idle" if self._file_count == 0 else "has_files"))

        for w in (self._icon, self._title, self._subtitle, self._hint):
            w.bind("<Button-1>", self._on_click)
            w.configure(cursor="hand2")

        try:
            from tkinterdnd2 import DND_FILES
            self.drop_target_register(DND_FILES)
            self.dnd_bind("<<Drop>>", self._on_drop)
        except Exception:
            pass

    def _set_state(self, state):
        if state == "hover":
            self.configure(fg_color=C["drop_hover_bg"], border_color=C["drop_hover_border"])
            self._icon.configure(text_color=C["drop_icon_hint"])
        elif state == "has_files":
            self.configure(fg_color=C["accent_light"], border_color=C["drop_border"])
            self._icon.configure(text_color=C["accent"])
        else:
            self.configure(fg_color=C["drop_bg"], border_color=C["drop_border"])
            self._icon.configure(text_color=C["drop_icon"])

    def set_file_count(self, count: int):
        self._file_count = count
        if count > 0:
            self._icon.configure(text="✅")
            self._title.configure(text=f"已添加 {count} 个文件")
            self._subtitle.configure(text="点击或拖放添加更多文件", text_color=C["text_light"])
            self._hint.configure(text="")
        else:
            self._icon.configure(text="📂")
            self._title.configure(text="拖放文件到此处")
            self._subtitle.configure(text="支持  .txt  .md  .pdf  格式", text_color=C["drop_icon_hint"])
            self._hint.configure(text="点击亦可选择文件")
        self._set_state("has_files" if count > 0 else "idle")

    def _on_click(self, event):
        paths = filedialog.askopenfilenames(
            title="选择文件",
            filetypes=[("支持的文件", "*.txt *.md *.pdf"), ("所有文件", "*.*")])
        if paths:
            self.on_files_added([Path(p) for p in paths])

    def _on_drop(self, event):
        paths = []
        for p in event.data.strip("{}").split("} {"):
            p = p.strip()
            if p:
                pp = Path(p)
                if pp.suffix.lower() in (".txt", ".md", ".pdf"):
                    paths.append(pp)
        if paths:
            self.on_files_added(paths)


class FileList(ctk.CTkScrollableFrame):
    """Scrollable list of added files with remove buttons."""

    def __init__(self, parent, on_files_changed, **kw):
        super().__init__(parent, fg_color=C["card_bg"], corner_radius=RADIUS_LG,
                         height=FILELIST_HEIGHT, **kw)
        self.on_files_changed = on_files_changed
        self._files: list[Path] = []
        self._show_empty()

    def _show_empty(self):
        for w in self.winfo_children():
            w.destroy()
        ctk.CTkLabel(self, text="尚未添加文件", font=(FONT, FONT_CAPTION),
                     text_color=C["text_hint"]).pack(anchor=tk.W, pady=SPACING_XS)

    def add_files(self, paths: list[Path]):
        existing = {f.resolve() for f in self._files}
        new = [p for p in paths if p.resolve() not in existing]
        if not new:
            return
        self._files.extend(new)
        self._rebuild()
        self.on_files_changed(len(self._files))

    def _rebuild(self):
        for w in self.winfo_children():
            w.destroy()
        if not self._files:
            self._show_empty()
            return
        for f in self._files:
            row = ctk.CTkFrame(self, fg_color="transparent")
            row.pack(fill=tk.X, pady=1)
            icon = "📄" if f.suffix.lower() != ".pdf" else "📕"
            ctk.CTkLabel(row, text=f"  {icon}  {f.name}", font=(FONT, FONT_SMALL),
                        text_color=C["text_secondary"], anchor="w").pack(side=tk.LEFT)

            x = ctk.CTkLabel(row, text=" ✕ ", font=(FONT, FONT_SMALL, "bold"),
                            text_color=C["close_btn"], cursor="hand2")
            x.pack(side=tk.RIGHT, padx=(8, 0))
            x.bind("<Button-1>", lambda e, fp=f: self._remove_file(fp))
            x.bind("<Enter>", lambda e, lbl=x: lbl.configure(text_color=C["close_btn_hover"]))
            x.bind("<Leave>", lambda e, lbl=x: lbl.configure(text_color=C["close_btn"]))

    def _remove_file(self, fp: Path):
        self._files = [f for f in self._files if f != fp]
        self._rebuild()
        self.on_files_changed(len(self._files))

    @property
    def files(self) -> list[Path]:
        return list(self._files)
