# -*- coding: utf-8 -*-
"""Filter bar component."""

import customtkinter as ctk
from typing import Callable

from ui.theme import AppTheme


class FilterBar(ctk.CTkFrame):
    """Filter bar widget."""
    
    def __init__(self, parent, on_filter: Callable[[str, str], None]):
        """Initialize filter bar."""
        super().__init__(parent, fg_color="transparent")
        
        self.on_filter = on_filter
        self.filter_type = ctk.StringVar(value="none")
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create filter widgets."""
        label = ctk.CTkLabel(
            self,
            text="Filter by:",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        label.pack(side="left", padx=(0, 10))
        
        # Date radio button
        date_radio = ctk.CTkRadioButton(
            self,
            text="Date",
            variable=self.filter_type,
            value="date",
            font=AppTheme.get_font("normal"),
            command=self._on_filter_change
        )
        date_radio.pack(side="left", padx=(0, 10))
        
        # Name radio button
        name_radio = ctk.CTkRadioButton(
            self,
            text="Name",
            variable=self.filter_type,
            value="name",
            font=AppTheme.get_font("normal"),
            command=self._on_filter_change
        )
        name_radio.pack(side="left", padx=(0, 10))
        
        # Clear filter
        clear_btn = ctk.CTkButton(
            self,
            text="Clear",
            width=60,
            font=AppTheme.get_font("small"),
            fg_color="transparent",
            hover_color=AppTheme.BACKGROUND_COLOR,
            text_color=AppTheme.TEXT_SECONDARY,
            command=self._clear_filter
        )
        clear_btn.pack(side="left")
    
    def _on_filter_change(self):
        """Handle filter type change."""
        filter_type = self.filter_type.get()
        if filter_type != "none":
            self.on_filter(filter_type, "")
    
    def _clear_filter(self):
        """Clear filter."""
        self.filter_type.set("none")
        self.on_filter("none", "")