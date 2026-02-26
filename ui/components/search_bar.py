# -*- coding: utf-8 -*-
"""Search bar component."""

import customtkinter as ctk
from typing import Callable

from ui.theme import AppTheme


class SearchBar(ctk.CTkFrame):
    """Search bar widget."""
    
    def __init__(self, parent, on_search: Callable[[str], None]):
        """Initialize search bar."""
        super().__init__(parent, fg_color="transparent")
        
        self.on_search = on_search
        self._create_widgets()
    
    def _create_widgets(self):
        """Create search widgets."""
        self.entry = ctk.CTkEntry(
            self,
            width=300,
            height=AppTheme.INPUT_HEIGHT,
            placeholder_text="🔍 खोज्नुहोस्... (Search)",
            font=AppTheme.get_font("normal")
        )
        self.entry.pack(side="left", padx=(0, 10))
        
        search_btn = ctk.CTkButton(
            self,
            text="Search",
            width=80,
            font=AppTheme.get_font("normal"),
            command=self._do_search,
            **AppTheme.get_button_style("primary")
        )
        search_btn.pack(side="left")
        
        # Bind Enter key
        self.entry.bind("<Return>", lambda e: self._do_search())
    
    def _do_search(self):
        """Perform search."""
        self.on_search(self.entry.get())
    
    def clear(self):
        """Clear search entry."""
        self.entry.delete(0, "end")