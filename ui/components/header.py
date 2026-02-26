# -*- coding: utf-8 -*-
"""Header component with logo and app name."""

import customtkinter as ctk
from PIL import Image
from pathlib import Path

from config.settings import Settings
from ui.theme import AppTheme


class Header(ctk.CTkFrame):
    """Application header widget."""
    
    def __init__(self, parent):
        """Initialize header."""
        super().__init__(
            parent,
            fg_color=AppTheme.CARD_COLOR,
            height=AppTheme.HEADER_HEIGHT,
            corner_radius=0
        )
        self.pack_propagate(False)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create header widgets."""
        # Center container
        center_frame = ctk.CTkFrame(self, fg_color="transparent")
        center_frame.pack(expand=True)
        
        # Nepal Emblem
        self._add_emblem(center_frame)
        
        # App name
        name_label = ctk.CTkLabel(
            center_frame,
            text=Settings.APP_NAME,
            font=AppTheme.get_font("title", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        name_label.pack(side="left", padx=10)
    
    def _add_emblem(self, parent):
        """Add Nepal emblem."""
        emblem_path = Settings.IMAGES_DIR / "nepal_emblem.png"
        
        if emblem_path.exists():
            try:
                image = Image.open(emblem_path)
                image = image.resize((50, 50), Image.LANCZOS)
                photo = ctk.CTkImage(light_image=image, size=(50, 50))
                
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