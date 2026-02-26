# -*- coding: utf-8 -*-
"""Application theme and styling."""

import customtkinter as ctk
from config.settings import Settings


class AppTheme:
    """Application theme configuration."""
    
    # Colors
    PRIMARY_COLOR = "#1a73e8"
    SECONDARY_COLOR = "#4285f4"
    SUCCESS_COLOR = "#34a853"
    WARNING_COLOR = "#fbbc04"
    ERROR_COLOR = "#ea4335"
    
    BACKGROUND_COLOR = "#f5f5f5"
    SIDEBAR_COLOR = "#ffffff"
    CARD_COLOR = "#ffffff"
    
    TEXT_PRIMARY = "#202124"
    TEXT_SECONDARY = "#5f6368"
    TEXT_LIGHT = "#ffffff"
    
    BORDER_COLOR = "#dadce0"
    
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
        """Apply theme to CustomTkinter."""
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
    
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
                "hover_color": "#d33426",
                "text_color": cls.TEXT_LIGHT,
                "height": cls.BUTTON_HEIGHT,
                "corner_radius": cls.BORDER_RADIUS
            }
        }
        return styles.get(variant, styles["primary"])