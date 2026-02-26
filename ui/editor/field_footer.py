# -*- coding: utf-8 -*-
"""Footer field component (Typist and CDO signature)."""

import customtkinter as ctk
from typing import Callable

from ui.theme import AppTheme
from database.local_db import LocalDatabase


class FooterField(ctk.CTkFrame):
    """Footer with typist name and CDO signature fields."""
    
    def __init__(
        self,
        parent,
        typist_name: str = "",
        cdo_name: str = "",
        on_typist_change: Callable[[str], None] = None,
        on_cdo_change: Callable[[str], None] = None
    ):
        """Initialize footer field."""
        super().__init__(parent, fg_color="transparent")
        
        self.on_typist_change = on_typist_change
        self.on_cdo_change = on_cdo_change
        
        self.typist_name = typist_name
        self.cdo_name = cdo_name
        
        self.local_db = LocalDatabase()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create footer widgets."""
        # Container for side-by-side layout
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", expand=True)
        
        # Configure grid columns
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        
        # Left side - Typist
        typist_frame = ctk.CTkFrame(container, fg_color="transparent")
        typist_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        typist_row = ctk.CTkFrame(typist_frame, fg_color="transparent")
        typist_row.pack(anchor="w")
        
        typist_label = ctk.CTkLabel(
            typist_row,
            text="टिपोट गर्ने ना.सु.",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        typist_label.pack(side="left", padx=(0, 10))
        
        # Get saved typist names
        saved_typists = self.local_db.get_dictionary_items("typist_names")
        
        if saved_typists:
            self.typist_input = ctk.CTkComboBox(
                typist_row,
                values=saved_typists,
                width=200,
                height=AppTheme.INPUT_HEIGHT,
                font=AppTheme.get_font("normal"),
                dropdown_font=AppTheme.get_font("normal"),
                command=self._on_typist_select
            )
            if self.typist_name:
                self.typist_input.set(self.typist_name)
            self.typist_input.bind("<KeyRelease>", self._on_typist_type)
        else:
            self.typist_input = ctk.CTkEntry(
                typist_row,
                width=200,
                height=AppTheme.INPUT_HEIGHT,
                font=AppTheme.get_font("normal"),
                placeholder_text="नाम..."
            )
            if self.typist_name:
                self.typist_input.insert(0, self.typist_name)
            self.typist_input.bind("<KeyRelease>", self._on_typist_type)
        
        self.typist_input.pack(side="left")
        
        # Right side - CDO Signature
        cdo_frame = ctk.CTkFrame(container, fg_color="transparent")
        cdo_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 0))
        
        # Signature dots
        dots_label = ctk.CTkLabel(
            cdo_frame,
            text="................................",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        dots_label.pack(anchor="e")
        
        # CDO Name
        saved_cdo_names = self.local_db.get_dictionary_items("cdo_names")
        
        if saved_cdo_names:
            self.cdo_input = ctk.CTkComboBox(
                cdo_frame,
                values=saved_cdo_names,
                width=200,
                height=AppTheme.INPUT_HEIGHT,
                font=AppTheme.get_font("normal"),
                dropdown_font=AppTheme.get_font("normal"),
                command=self._on_cdo_select
            )
            if self.cdo_name:
                self.cdo_input.set(self.cdo_name)
            self.cdo_input.bind("<KeyRelease>", self._on_cdo_type)
        else:
            self.cdo_input = ctk.CTkEntry(
                cdo_frame,
                width=200,
                height=AppTheme.INPUT_HEIGHT,
                font=AppTheme.get_font("normal"),
                placeholder_text="CDO नाम..."
            )
            if self.cdo_name:
                self.cdo_input.insert(0, self.cdo_name)
            self.cdo_input.bind("<KeyRelease>", self._on_cdo_type)
        
        self.cdo_input.pack(anchor="e", pady=5)
        
        # Designation
        designation_label = ctk.CTkLabel(
            cdo_frame,
            text="प्रमुख जिल्ला अधिकारी",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        designation_label.pack(anchor="e")
    
    def _on_typist_select(self, value: str):
        """Handle typist dropdown selection."""
        if self.on_typist_change:
            self.on_typist_change(value)
    
    def _on_typist_type(self, event):
        """Handle typist typing."""
        if self.on_typist_change:
            self.on_typist_change(self.get_typist_value())
    
    def _on_cdo_select(self, value: str):
        """Handle CDO dropdown selection."""
        if self.on_cdo_change:
            self.on_cdo_change(value)
    
    def _on_cdo_type(self, event):
        """Handle CDO typing."""
        if self.on_cdo_change:
            self.on_cdo_change(self.get_cdo_value())
    
    def get_typist_value(self) -> str:
        """Get typist name value."""
        return self.typist_input.get()
    
    def get_cdo_value(self) -> str:
        """Get CDO name value."""
        return self.cdo_input.get()
    
    def set_typist_name(self, value: str):
        """Set typist name."""
        if isinstance(self.typist_input, ctk.CTkComboBox):
            self.typist_input.set(value)
        else:
            self.typist_input.delete(0, "end")
            self.typist_input.insert(0, value)
    
    def set_cdo_name(self, value: str):
        """Set CDO name (for auto-linking)."""
        if isinstance(self.cdo_input, ctk.CTkComboBox):
            self.cdo_input.set(value)
        else:
            self.cdo_input.delete(0, "end")
            self.cdo_input.insert(0, value)