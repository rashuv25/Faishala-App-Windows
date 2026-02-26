# -*- coding: utf-8 -*-
"""Dictionary screen UI."""

import customtkinter as ctk
from typing import List

from ui.theme import AppTheme
from database.local_db import LocalDatabase


class DictionaryScreen(ctk.CTkFrame):
    """Dictionary management screen."""
    
    def __init__(self, parent):
        """Initialize dictionary screen."""
        super().__init__(parent, fg_color=AppTheme.BACKGROUND_COLOR)
        
        self.local_db = LocalDatabase()
        self._create_widgets()
    
    def _create_widgets(self):
        """Create dictionary widgets."""
        # Container with padding
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            container,
            text="शब्दकोश (Dictionary)",
            font=AppTheme.get_font("title", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        title.pack(anchor="w", pady=(0, 20))
        
        # Description
        desc = ctk.CTkLabel(
            container,
            text="ड्रपडाउनमा प्रयोग हुने नामहरू व्यवस्थापन गर्नुहोस्",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        desc.pack(anchor="w", pady=(0, 30))
        
        # Categories container
        categories_frame = ctk.CTkFrame(container, fg_color="transparent")
        categories_frame.pack(fill="both", expand=True)
        
        # CDO Names Category
        self._create_category_section(
            categories_frame,
            "प्रमुख जिल्ला अधिकारी नामहरू (CDO Names)",
            "cdo_names"
        )
        
        # Typist Names Category
        self._create_category_section(
            categories_frame,
            "टिपोट गर्ने ना.सु. नामहरू (Typist Names)",
            "typist_names"
        )
    
    def _create_category_section(self, parent, title: str, category: str):
        """Create a category section."""
        # Section frame
        section = ctk.CTkFrame(
            parent,
            fg_color=AppTheme.CARD_COLOR,
            corner_radius=AppTheme.BORDER_RADIUS
        )
        section.pack(fill="x", pady=(0, 20), padx=0, ipady=15, ipadx=15)
        
        # Section title
        title_label = ctk.CTkLabel(
            section,
            text=title,
            font=AppTheme.get_font("large", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        title_label.pack(anchor="w", padx=15, pady=(10, 15))
        
        # Items list frame
        items_frame = ctk.CTkFrame(section, fg_color="transparent")
        items_frame.pack(fill="x", padx=15)
        
        # Load and display items
        items = self.local_db.get_dictionary_items(category)
        
        for item in items:
            self._create_item_row(items_frame, category, item)
        
        # Add new item row
        add_frame = ctk.CTkFrame(section, fg_color="transparent")
        add_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        entry = ctk.CTkEntry(
            add_frame,
            width=300,
            height=AppTheme.INPUT_HEIGHT,
            placeholder_text="नयाँ नाम थप्नुहोस्...",
            font=AppTheme.get_font("normal")
        )
        entry.pack(side="left", padx=(0, 10))
        
        add_btn = ctk.CTkButton(
            add_frame,
            text="+ थप्नुहोस्",
            width=100,
            font=AppTheme.get_font("normal"),
            command=lambda e=entry, c=category, s=section: self._add_item(e, c, s),
            **AppTheme.get_button_style("primary")
        )
        add_btn.pack(side="left")
        
        # Store reference for refresh
        section.items_frame = items_frame
        section.category = category
    
    def _create_item_row(self, parent, category: str, value: str):
        """Create an item row."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=2)
        
        label = ctk.CTkLabel(
            row,
            text=value,
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        label.pack(side="left")
        
        delete_btn = ctk.CTkButton(
            row,
            text="🗑️",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=AppTheme.BACKGROUND_COLOR,
            text_color=AppTheme.ERROR_COLOR,
            command=lambda: self._delete_item(category, value, row)
        )
        delete_btn.pack(side="right")
    
    def _add_item(self, entry: ctk.CTkEntry, category: str, section):
        """Add new item to category."""
        value = entry.get().strip()
        if value:
            success = self.local_db.add_dictionary_item(category, value)
            if success:
                entry.delete(0, "end")
                self._create_item_row(section.items_frame, category, value)
    
    def _delete_item(self, category: str, value: str, row: ctk.CTkFrame):
        """Delete item from category."""
        self.local_db.delete_dictionary_item(category, value)
        row.destroy()