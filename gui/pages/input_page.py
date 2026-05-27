"""Input page: drag-and-drop file addition."""
from __future__ import annotations

from pathlib import Path

import customtkinter as ctk

from gui.theme import C, FONT, FONT_H2, FONT_SMALL
from gui.theme import SPACING_XS, SPACING_SM, SPACING_MD, SPACING_LG, SPACING_XL
from gui.widgets import DropZone, FileList


class InputPage(ctk.CTkFrame):
    """Page 0: drag-and-drop file input."""

    def __init__(self, parent, on_files_added, on_files_changed, **kw):
        super().__init__(parent, fg_color=C["bg"], **kw)

        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(anchor="w", padx=SPACING_XL, pady=(SPACING_LG, SPACING_XS))
        ctk.CTkLabel(hdr, text="📥", font=(FONT, 32)).pack(side="left")
        ctk.CTkLabel(hdr, text="输入文件", font=(FONT, FONT_H2, "bold"),
                     text_color=C["text"]).pack(side="left", padx=(SPACING_SM, 0))
        ctk.CTkLabel(self, text="拖放或点击添加 .txt / .md / .pdf 文件",
                     font=(FONT, FONT_SMALL), text_color=C["text_light"]).pack(
                         anchor="w", padx=SPACING_XL)

        # Drop zone
        self._drop_zone = DropZone(self, on_files_added=on_files_added)
        self._drop_zone.pack(fill="x", padx=SPACING_XL, pady=(SPACING_MD, SPACING_MD))

        # File list
        ctk.CTkLabel(self, text="▸ 已添加的文件", font=(FONT, FONT_SMALL, "bold"),
                     text_color=C["text_light"]).pack(anchor="w", padx=SPACING_XL,
                                                      pady=(SPACING_SM, SPACING_XS))
        self._file_list = FileList(self, on_files_changed=on_files_changed)
        self._file_list.pack(fill="x", padx=SPACING_XL)

    @property
    def files(self) -> list[Path]:
        return self._file_list.files

    def update_drop_zone(self, count: int):
        self._drop_zone.set_file_count(count)
