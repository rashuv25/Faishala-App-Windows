# -*- coding: utf-8 -*-
"""CDO Name field with dropdown component."""

import customtkinter as ctk
from typing import Callable, List

from ui.theme import AppTheme
from database.local_db import LocalDatabase


class CDONameField(ctk.CTkFrame):
    """CDO Name input with dropdown suggestions."""
    
    def __init__(
        self,
        parent,
        default_value: str = "",
        on_change: Callable[[str], None] = None
    ):
        """Initialize CDO name field."""
        super().__init__(parent, fg_color="transparent")
        
        self.on_change = on_change
        self.default_value = default_value
        self.local_db = LocalDatabase()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create CDO name input with dropdown."""
        # Get saved CDO names
        saved_names = self.local_db.get_dictionary_items("cdo_names")
        
        if saved_names:
            # Use combobox if there are saved names
            self.input = ctk.CTkComboBox(
                self,
                values=saved_names,
                width=200,
                height=AppTheme.INPUT_HEIGHT,
                font=AppTheme.get_font("normal"),
                dropdown_font=AppTheme.get_font("normal"),
                command=self._on_dropdown_select
            )
            if self.default_value:
                self.input.set(self.default_value)
            
            # Bind typing event
            self.input.bind("<KeyRelease>", self._on_type)
        else:
            # Use simple entry if no saved names
            self.input = ctk.CTkEntry(
                self,
                width=200,
                height=AppTheme.INPUT_HEIGHT,
                font=AppTheme.get_font("normal"),
                placeholder_text="CDO नाम..."
            )
            if self.default_value:
                self.input.insert(0, self.default_value)
            
            # Bind typing event
            self.input.bind("<KeyRelease>", self._on_type)
        
        self.input.pack()
    
    def _on_dropdown_select(self, value: str):
        """Handle dropdown selection."""
        if self.on_change:
            self.on_change(value)
    
    def _on_type(self, event):
        """Handle typing in field."""
        if self.on_change:
            self.on_change(self.get_value())
    
    def get_value(self) -> str:
        """Get current value."""
        return self.input.get()
    
    def set_value(self, value: str):
        """Set current value."""
        if isinstance(self.input, ctk.CTkComboBox):
            self.input.set(value)
        else:
            self.input.delete(0, "end")
            self.input.insert(0, value)