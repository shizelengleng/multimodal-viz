"""Design tokens: colors, fonts, spacing, and dimensions for the GUI.

Uses CustomTkinter for native rounded widgets — no more Canvas hacks.
"""
from __future__ import annotations

# ═══════════════════════════════════════════════════════════════
# CustomTkinter Configuration
# ═══════════════════════════════════════════════════════════════
CTK_APPEARANCE_MODE = "light"
CTK_COLOR_THEME    = "green"

FONT       = "Microsoft YaHei"
FONT_MONO  = "Consolas"

# ═══════════════════════════════════════════════════════════════
# Typographic Scale  (desktop-optimized)
# ═══════════════════════════════════════════════════════════════
FONT_H1      = 30
FONT_H2      = 22
FONT_H3      = 18
FONT_BODY    = 16
FONT_SMALL   = 14
FONT_CAPTION = 12

# ═══════════════════════════════════════════════════════════════
# Spacing Scale  (6px baseline grid)
# ═══════════════════════════════════════════════════════════════
SPACING_XS   = 6
SPACING_SM   = 12
SPACING_MD   = 18
SPACING_LG   = 24
SPACING_XL   = 36
SPACING_XXL  = 48

# ═══════════════════════════════════════════════════════════════
# Corner Radii  (for custom-drawn areas only — CTk widgets use
# their own corner_radius parameter)
# ═══════════════════════════════════════════════════════════════
RADIUS_SM  = 6
RADIUS_MD  = 8
RADIUS_LG  = 10

# ═══════════════════════════════════════════════════════════════
# Layout Dimensions
# ═══════════════════════════════════════════════════════════════
SIDEBAR_WIDTH          = 280
SIDEBAR_ITEM_HEIGHT    = 72
SIDEBAR_SECTION_HEIGHT = 56
TITLE_BAR_HEIGHT       = 40
STATUS_BAR_HEIGHT      = 30
DROPZONE_HEIGHT        = 260
FILELIST_HEIGHT        = 160
WINDOW_MIN_WIDTH       = 1200
WINDOW_MIN_HEIGHT      = 750

# ═══════════════════════════════════════════════════════════════
# Color Palette
# ═══════════════════════════════════════════════════════════════
C = {
    # ── Surface hierarchy ──
    "bg":              "#F5F7F5",
    "card_bg":         "#FFFFFF",
    "card_border":      "#DEE2DE",
    "input_bg":        "#FDFDFD",
    "sep":             "#E8E8E8",

    # ── Text hierarchy ──
    "text":            "#3A3A3A",
    "text_secondary":  "#666666",
    "text_light":      "#999999",
    "text_hint":       "#AAAAAA",
    "text_inverse":    "#FFFFFF",

    # ── Brand accent ──
    "accent":          "#2F8D63",
    "accent_hover":    "#2E805C",
    "accent_pressed":  "#267A52",
    "accent_light":    "#E8F5EE",

    # ── Button tokens (for CTkButton customization) ──
    "btn_secondary_bg":      "#F0F0F0",
    "btn_secondary_hover_bg":"#E0E0E0",
    "btn_secondary_fg":      "#666666",

    # ── Semantic colors ──
    "success":         "#13A10E",
    "success_light":   "#E8F5E9",
    "danger":          "#E57373",
    "danger_light":    "#FDEAEA",
    "warning":         "#F9A825",
    "warning_light":   "#FFF8E1",
    "info":            "#1976D2",
    "info_light":      "#E3F2FD",

    # ── Custom title bar ──
    "titlebar_bg":           "#2C3E35",
    "titlebar_fg":           "#CCD5CF",
    "titlebar_btn_hover":    "#3D5448",
    "titlebar_close_hover":  "#E57373",

    # ── Sidebar ──
    "sidebar_bg":           "#E8EDE8",
    "sidebar_fg":           "#5A6C5A",
    "sidebar_active_bg":    "#FFFFFF",
    "sidebar_active_fg":    "#2F8D63",
    "sidebar_hover_bg":     "#DCE4DC",
    "sidebar_border":       "#CDD8CD",
    "sidebar_item_text":    "#4A5E4A",
    "sidebar_section_fg":   "#9AAA9A",
    "sidebar_separator":    "#CFD8CF",

    # ── Drop zone ──
    "drop_bg":              "#FAFDFA",
    "drop_border":          "#A5D6A7",
    "drop_hover_bg":        "#EEF7EE",
    "drop_hover_border":    "#2F8D63",
    "drop_icon":            "#A5D6A7",
    "drop_icon_hint":       "#66BB6A",

    # ── Mode selector cards ──
    "mode_card_bg":             "#F9FBF9",
    "mode_card_border":         "#DEE2DE",
    "mode_card_selected_bg":    "#E8F5EE",
    "mode_card_selected_border":"#2F8D63",
    "mode_card_hover_bg":       "#F0F4F0",
    "mode_card_hover_border":   "#A5C8A5",
    "mode_card_text":           "#555555",
    "mode_card_selected_text":  "#2F8D63",
    "mode_card_desc":           "#999999",

    # ── Toast ──
    "toast_bg":             "#FFFFFF",
    "toast_border":         "#DDDDDD",
    "toast_success_bar":    "#13A10E",
    "toast_error_bar":      "#E57373",
    "toast_warning_bar":    "#F9A825",
    "toast_info_bar":       "#1976D2",

    # ── Misc ──
    "window_control":       "#999999",
    "file_icon":            "#555555",
    "close_btn":            "#CCCCCC",
    "close_btn_hover":      "#E57373",
    "status_dot_ok":        "#2F8D63",
    "status_dot_none":      "#E57373",
    "status_dot_checking":  "#888888",
}
