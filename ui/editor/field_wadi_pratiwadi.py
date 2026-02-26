# -*- coding: utf-8 -*-
"""Wadi and Pratiwadi side-by-side field component."""

import customtkinter as ctk
from typing import Callable

from ui.theme import AppTheme


class WadiPratiwadiField(ctk.CTkFrame):
    """Wadi and Pratiwadi side-by-side text areas."""
    
    def __init__(
        self,
        parent,
        wadi_value: str = "",
        pratiwadi_value: str = "",
        on_wadi_change: Callable[[str], None] = None,
        on_pratiwadi_change: Callable[[str], None] = None
    ):
        """Initialize wadi/pratiwadi fields."""
        super().__init__(parent, fg_color="transparent")
        
        self.on_wadi_change = on_wadi_change
        self.on_pratiwadi_change = on_pratiwadi_change
        
        self.wadi_value = wadi_value
        self.pratiwadi_value = pratiwadi_value
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create side-by-side text areas."""
        # Container for side-by-side layout
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", expand=True)
        
        # Configure grid columns to be equal
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        
        # Wadi section (left)
        wadi_frame = ctk.CTkFrame(container, fg_color="transparent")
        wadi_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        wadi_label = ctk.CTkLabel(
            wadi_frame,
            text="वादी",
            font=AppTheme.get_font("normal", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        wadi_label.pack(anchor="w", pady=(0, 5))
        
        self.wadi_text = ctk.CTkTextbox(
            wadi_frame,
            height=150,
            font=AppTheme.get_font("normal"),
            wrap="word"
        )
        self.wadi_text.pack(fill="both", expand=True)
        
        if self.wadi_value:
            self.wadi_text.insert("1.0", self.wadi_value)
        
        self.wadi_text.bind("<KeyRelease>", self._on_wadi_type)
        
        # Pratiwadi section (right)
        pratiwadi_frame = ctk.CTkFrame(container, fg_color="transparent")
        pratiwadi_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        pratiwadi_label = ctk.CTkLabel(
            pratiwadi_frame,
            text="प्रतिवादी",
            font=AppTheme.get_font("normal", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        pratiwadi_label.pack(anchor="w", pady=(0, 5))
        
        self.pratiwadi_text = ctk.CTkTextbox(
            pratiwadi_frame,
            height=150,
            font=AppTheme.get_font("normal"),
            wrap="word"
        )
        self.pratiwadi_text.pack(fill="both", expand=True)
        
        if self.pratiwadi_value:
            self.pratiwadi_text.insert("1.0", self.pratiwadi_value)
        
        self.pratiwadi_text.bind("<KeyRelease>", self._on_pratiwadi_type)
    
    def _on_wadi_type(self, event):
        """Handle wadi text change."""
        if self.on_wadi_change:
            self.on_wadi_change(self.get_wadi_value())
    
    def _on_pratiwadi_type(self, event):
        """Handle pratiwadi text change."""
        if self.on_pratiwadi_change:
            self.on_pratiwadi_change(self.get_pratiwadi_value())
    
    def get_wadi_value(self) -> str:
        """Get wadi text value."""
        return self.wadi_text.get("1.0", "end-1c")
    
    def get_pratiwadi_value(self) -> str:
        """Get pratiwadi text value."""
        return self.pratiwadi_text.get("1.0", "end-1c")
    
    def set_wadi_value(self, value: str):
        """Set wadi text value."""
        self.wadi_text.delete("1.0", "end")
        self.wadi_text.insert("1.0", value)
    
    def set_pratiwadi_value(self, value: str):
        """Set pratiwadi text value."""
        self.pratiwadi_text.delete("1.0", "end")
        self.pratiwadi_text.insert("1.0", value)