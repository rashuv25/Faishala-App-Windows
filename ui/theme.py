# -*- coding: utf-8 -*-
"""Application theme and styling."""

import customtkinter as ctk
from config.settings import Settings


class AppTheme:
    """Application theme configuration."""

    # Colors (light, dark)
    PRIMARY_COLOR = ("#1a73e8", "#3b82f6")
    SECONDARY_COLOR = ("#4285f4", "#60a5fa")
    SUCCESS_COLOR = ("#34a853", "#22c55e")
    WARNING_COLOR = ("#fbbc04", "#f59e0b")
    ERROR_COLOR = ("#ea4335", "#ef4444")

    BACKGROUND_COLOR = ("#f5f5f5", "#111827")
    SIDEBAR_COLOR = ("#ffffff", "#1f2937")
    CARD_COLOR = ("#ffffff", "#1f2937")

    TEXT_PRIMARY = ("#202124", "#f9fafb")
    TEXT_SECONDARY = ("#5f6368", "#d1d5db")
    TEXT_LIGHT = ("#ffffff", "#ffffff")

    BORDER_COLOR = ("#dadce0", "#374151")
    HOVER_LIGHT = ("#e8e8e8", "#374151")
    ROW_HOVER = ("#e8f4fc", "#243447")
    DELETE_HOVER = ("#ffebee", "#4b1d1d")
    RENAME_HOVER = ("#e3f2fd", "#1e3a5f")
    DUPLICATE_HOVER = ("#e8f5e9", "#1d3b2a")
    EXPORT_HOVER = ("#fff3e0", "#4b3621")

    # Fonts
    FONT_FAMILY = "Kalimati"
    FONT_FAMILY_FALLBACK = "Arial"

    FONT_SIZE_SMALL = 12
    FONT_SIZE_NORMAL = 14
    FONT_SIZE_LARGE = 16
    FONT_SIZE_TITLE = 20
    FONT_SIZE_HEADER = 24

    # Dimensions
    SIDEBAR_WIDTH = 200
    HEADER_HEIGHT = 80
    BUTTON_HEIGHT = 40
    INPUT_HEIGHT = 40

    PADDING_SMALL = 5
    PADDING_NORMAL = 10
    PADDING_LARGE = 20

    BORDER_RADIUS = 8

    @classmethod
    def apply_theme(cls):
        """Apply saved theme to CustomTkinter."""
        ctk.set_default_color_theme("blue")
        theme = cls.get_saved_theme()
        ctk.set_appearance_mode(theme)
        cls._patch_clickable_cursors()

    @classmethod
    def get_saved_theme(cls) -> str:
        """Get saved theme from app_settings."""
        try:
            from database.local_db import LocalDatabase
            db = LocalDatabase()
            saved = (db.get_setting("theme") or "light").strip().lower()
            if saved in ("light", "dark", "system"):
                return saved
        except Exception:
            pass
        return "light"

    @classmethod
    def set_theme(cls, theme: str):
        """Apply theme immediately."""
        theme = (theme or "light").strip().lower()
        if theme not in ("light", "dark", "system"):
            theme = "light"
        ctk.set_appearance_mode(theme)

    @classmethod
    def _patch_clickable_cursors(cls):
        """Make clickable widgets show pointer cursor by default."""
        def patch_cursor(widget_class):
            if getattr(widget_class, "_app_cursor_patched", False):
                return

            original_init = widget_class.__init__

            def wrapped_init(self, *args, **kwargs):
                kwargs.setdefault("cursor", "hand2")
                original_init(self, *args, **kwargs)

            widget_class.__init__ = wrapped_init
            widget_class._app_cursor_patched = True

        for widget_class in (
            ctk.CTkButton,
            ctk.CTkSwitch,
            ctk.CTkOptionMenu,
            ctk.CTkRadioButton,
            ctk.CTkCheckBox,
            ctk.CTkSegmentedButton,
        ):
            try:
                patch_cursor(widget_class)
            except Exception:
                pass

    @classmethod
    def get_font(cls, size: str = "normal", bold: bool = False) -> tuple:
        """Get font tuple."""
        sizes = {
            "small": cls.FONT_SIZE_SMALL,
            "normal": cls.FONT_SIZE_NORMAL,
            "large": cls.FONT_SIZE_LARGE,
            "title": cls.FONT_SIZE_TITLE,
            "header": cls.FONT_SIZE_HEADER
        }

        font_size = sizes.get(size, cls.FONT_SIZE_NORMAL)
        weight = "bold" if bold else "normal"

        return (cls.FONT_FAMILY, font_size, weight)

    @classmethod
    def get_button_style(cls, variant: str = "primary") -> dict:
        """Get button style configuration."""
        styles = {
            "primary": {
                "fg_color": cls.PRIMARY_COLOR,
                "hover_color": cls.SECONDARY_COLOR,
                "text_color": cls.TEXT_LIGHT,
                "height": cls.BUTTON_HEIGHT,
                "corner_radius": cls.BORDER_RADIUS
            },
            "secondary": {
                "fg_color": cls.CARD_COLOR,
                "hover_color": cls.BACKGROUND_COLOR,
                "text_color": cls.TEXT_PRIMARY,
                "border_width": 1,
                "border_color": cls.BORDER_COLOR,
                "height": cls.BUTTON_HEIGHT,
                "corner_radius": cls.BORDER_RADIUS
            },
            "danger": {
                "fg_color": cls.ERROR_COLOR,
                "hover_color": ("#d33426", "#b91c1c"),
                "text_color": cls.TEXT_LIGHT,
                "height": cls.BUTTON_HEIGHT,
                "corner_radius": cls.BORDER_RADIUS
            }
        }
        return styles.get(variant, styles["primary"])