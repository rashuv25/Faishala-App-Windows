# -*- coding: utf-8 -*-
"""Mudda and case number field component."""

import customtkinter as ctk
from typing import Callable

from ui.theme import AppTheme


class MuddaField(ctk.CTkFrame):
    """Mudda and case number fields (stacked vertically)."""
    
    def __init__(
        self,
        parent,
        mudda_value: str = "",
        mudda_number_value: str = "",
        on_mudda_change: Callable[[str], None] = None,
        on_number_change: Callable[[str], None] = None
    ):
        """Initialize mudda fields."""
        super().__init__(parent, fg_color="transparent")
        
        self.on_mudda_change = on_mudda_change
        self.on_number_change = on_number_change
        
        self.mudda_value = mudda_value
        self.mudda_number_value = mudda_number_value
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create mudda input fields."""
        # Mudda row
        mudda_row = ctk.CTkFrame(self, fg_color="transparent")
        mudda_row.pack(fill="x", pady=5)
        
        mudda_label = ctk.CTkLabel(
            mudda_row,
            text="मुद्दा :",
            font=AppTheme.get_font("normal", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        mudda_label.pack(side="left", padx=(0, 10))
        
        self.mudda_entry = ctk.CTkEntry(
            mudda_row,
            width=400,
            height=AppTheme.INPUT_HEIGHT,
            font=AppTheme.get_font("normal"),
            placeholder_text="मुद्दाको प्रकार..."
        )
        self.mudda_entry.pack(side="left", fill="x", expand=True)
        
        if self.mudda_value:
            self.mudda_entry.insert(0, self.mudda_value)
        
        self.mudda_entry.bind("<KeyRelease>", self._on_mudda_type)
        
        # Case number row
        number_row = ctk.CTkFrame(self, fg_color="transparent")
        number_row.pack(fill="x", pady=5)
        
        number_label = ctk.CTkLabel(
            number_row,
            text="मु. द. नं. :",
            font=AppTheme.get_font("normal", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        number_label.pack(side="left", padx=(0, 10))
        
        self.number_entry = ctk.CTkEntry(
            number_row,
            width=400,
            height=AppTheme.INPUT_HEIGHT,
            font=AppTheme.get_font("normal"),
            placeholder_text="मुद्दा दर्ता नं..."
        )
        self.number_entry.pack(side="left", fill="x", expand=True)
        
        if self.mudda_number_value:
            self.number_entry.insert(0, self.mudda_number_value)
        
        self.number_entry.bind("<KeyRelease>", self._on_number_type)
    
    def _on_mudda_type(self, event):
        """Handle mudda text change."""
        if self.on_mudda_change:
            self.on_mudda_change(self.mudda_entry.get())
    
    def _on_number_type(self, event):
        """Handle case number change."""
        if self.on_number_change:
            self.on_number_change(self.number_entry.get())
    
    def get_mudda_value(self) -> str:
        """Get mudda value."""
        return self.mudda_entry.get()
    
    def get_number_value(self) -> str:
        """Get case number value."""
        return self.number_entry.get()
    
    def set_mudda_value(self, value: str):
        """Set mudda value."""
        self.mudda_entry.delete(0, "end")
        self.mudda_entry.insert(0, value)
    
    def set_number_value(self, value: str):
        """Set case number value."""
        self.number_entry.delete(0, "end")
        self.number_entry.insert(0, value)