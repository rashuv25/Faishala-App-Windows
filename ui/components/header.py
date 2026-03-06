# -*- coding: utf-8 -*-
"""Header component with logo, app name, and theme toggle."""

import customtkinter as ctk
from PIL import Image

from config.settings import Settings
from ui.theme import AppTheme


class Header(ctk.CTkFrame):
    """Application header widget."""

    def __init__(self, parent, on_theme_change=None):
        """Initialize header."""
        super().__init__(
            parent,
            fg_color=AppTheme.CARD_COLOR,
            height=AppTheme.HEADER_HEIGHT,
            corner_radius=0,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR
        )
        self.pack_propagate(False)

        self.on_theme_change = on_theme_change
        self._create_widgets()

    def _create_widgets(self):
        """Create header widgets."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20)

        # Left spacer
        left_spacer = ctk.CTkFrame(container, fg_color="transparent", width=130)
        left_spacer.pack(side="left")
        left_spacer.pack_propagate(False)

        # Center title block
        center_frame = ctk.CTkFrame(container, fg_color="transparent")
        center_frame.pack(side="left", expand=True)

        self._add_emblem(center_frame)

        name_label = ctk.CTkLabel(
            center_frame,
            text=Settings.APP_NAME,
            font=AppTheme.get_font("title", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        name_label.pack(side="left", padx=10)

        # Right theme block
        right_frame = ctk.CTkFrame(container, fg_color="transparent")
        right_frame.pack(side="right")

        current_theme = AppTheme.get_saved_theme()
        self.theme_var = ctk.StringVar(value="dark" if current_theme == "dark" else "light")

        sun_label = ctk.CTkLabel(
            right_frame,
            text="☀️",
            font=("Arial", 18),
            text_color=AppTheme.TEXT_PRIMARY
        )
        sun_label.pack(side="left", padx=(0, 8))

        self.theme_switch = ctk.CTkSwitch(
            right_frame,
            text="",
            variable=self.theme_var,
            onvalue="dark",
            offvalue="light",
            width=50,
            command=self._handle_theme_toggle
        )
        if self.theme_var.get() == "dark":
            self.theme_switch.select()
        else:
            self.theme_switch.deselect()
        self.theme_switch.pack(side="left")

        moon_label = ctk.CTkLabel(
            right_frame,
            text="🌙",
            font=("Arial", 18),
            text_color=AppTheme.TEXT_PRIMARY
        )
        moon_label.pack(side="left", padx=(8, 0))

    def _handle_theme_toggle(self):
        """Handle theme toggle from header."""
        theme = self.theme_var.get()
        if self.on_theme_change:
            self.on_theme_change(theme)

    def _add_emblem(self, parent):
        """Add Nepal emblem."""
        emblem_path = Settings.IMAGES_DIR / "nepal_emblem.png"

        if emblem_path.exists():
            try:
                image = Image.open(emblem_path)
                image = image.resize((50, 50), Image.LANCZOS)
                photo = ctk.CTkImage(light_image=image, dark_image=image, size=(50, 50))

                emblem_label = ctk.CTkLabel(parent, image=photo, text="")
                emblem_label.pack(side="left")
            except Exception:
                self._add_placeholder(parent)
        else:
            self._add_placeholder(parent)

    def _add_placeholder(self, parent):
        """Add placeholder for emblem."""
        placeholder = ctk.CTkLabel(
            parent,
            text="🏛️",
            font=("Arial", 30)
        )
        placeholder.pack(side="left")