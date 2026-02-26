# -*- coding: utf-8 -*-
"""District dropdown field component."""

import customtkinter as ctk
from typing import Callable, Optional

from ui.theme import AppTheme
from config.districts import NEPAL_DISTRICTS_SORTED
from config.settings import Settings


class DistrictField(ctk.CTkFrame):
    """District selection dropdown field."""
    
    def __init__(
        self,
        parent,
        default_value: str = None,
        on_change: Callable[[str], None] = None
    ):
        """Initialize district field."""
        super().__init__(parent, fg_color="transparent")
        
        self.on_change = on_change
        self.default_value = default_value or Settings.DEFAULT_DISTRICT
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create district dropdown."""
        self.dropdown = ctk.CTkComboBox(
            self,
            values=NEPAL_DISTRICTS_SORTED,
            width=150,
            height=AppTheme.INPUT_HEIGHT,
            font=AppTheme.get_font("normal"),
            dropdown_font=AppTheme.get_font("normal"),
            command=self._on_select
        )
        self.dropdown.set(self.default_value)
        self.dropdown.pack()
    
    def _on_select(self, value: str):
        """Handle selection change."""
        if self.on_change:
            self.on_change(value)
    
    def get_value(self) -> str:
        """Get current value."""
        return self.dropdown.get()
    
    def set_value(self, value: str):
        """Set current value."""
        if value in NEPAL_DISTRICTS_SORTED:
            self.dropdown.set(value)