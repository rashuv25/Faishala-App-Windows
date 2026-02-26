# -*- coding: utf-8 -*-
"""Settings screen UI."""

import customtkinter as ctk
from typing import Dict

from ui.theme import AppTheme
from database.local_db import LocalDatabase
from config.settings import Settings


class SettingsScreen(ctk.CTkFrame):
    """Settings screen widget."""
    
    def __init__(self, parent):
        """Initialize settings screen."""
        super().__init__(parent, fg_color=AppTheme.BACKGROUND_COLOR)
        
        self.local_db = LocalDatabase()
        self.settings = self._load_settings()
        
        self._create_widgets()
    
    def _load_settings(self) -> Dict[str, str]:
        """Load settings from database."""
        return self.local_db.get_all_settings()
    
    def _create_widgets(self):
        """Create settings widgets."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 25))
        
        icon_label = ctk.CTkLabel(
            header_frame,
            text="⚙️",
            font=("Arial", 32)
        )
        icon_label.pack(side="left", padx=(0, 12))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Settings",
            font=AppTheme.get_font("title", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        title_label.pack(side="left")
        
        # Settings sections
        self._create_app_info_section(container)
        self._create_appearance_section(container)
        self._create_document_section(container)
        self._create_data_section(container)
    
    def _create_section(self, parent, title: str, icon: str) -> ctk.CTkFrame:
        """Create a settings section."""
        section = ctk.CTkFrame(
            parent,
            fg_color=AppTheme.CARD_COLOR,
            corner_radius=10,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR
        )
        section.pack(fill="x", pady=(0, 15))
        
        # Section header
        header = ctk.CTkFrame(section, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(15, 10))
        
        icon_label = ctk.CTkLabel(
            header,
            text=icon,
            font=("Arial", 20)
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        title_label = ctk.CTkLabel(
            header,
            text=title,
            font=AppTheme.get_font("normal", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        title_label.pack(side="left")
        
        # Content frame
        content = ctk.CTkFrame(section, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=(0, 15))
        
        return content
    
    def _create_app_info_section(self, parent):
        """Create app info section."""
        content = self._create_section(parent, "App Information", "ℹ️")
        
        # App name
        self._create_info_row(content, "App Name:", Settings.APP_NAME)
        self._create_info_row(content, "Version:", Settings.APP_VERSION)
        self._create_info_row(content, "Developer:", "Your Company Name")
    
    def _create_appearance_section(self, parent):
        """Create appearance section."""
        content = self._create_section(parent, "Appearance", "🎨")
        
        # Theme selection
        theme_frame = ctk.CTkFrame(content, fg_color="transparent")
        theme_frame.pack(fill="x", pady=5)
        
        theme_label = ctk.CTkLabel(
            theme_frame,
            text="Theme:",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY,
            width=150,
            anchor="w"
        )
        theme_label.pack(side="left")
        
        self.theme_var = ctk.StringVar(value=self.settings.get('theme', 'light'))
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["Light", "Dark", "System"],
            variable=self.theme_var,
            width=200,
            height=35,
            font=AppTheme.get_font("normal"),
            command=self._on_theme_change
        )
        theme_menu.pack(side="left")
        
        # Note: Theme change might require app restart
        theme_note = ctk.CTkLabel(
            content,
            text="Note: Theme changes will apply on next restart",
            font=AppTheme.get_font("small"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        theme_note.pack(anchor="w", pady=(5, 0))
    
    def _create_document_section(self, parent):
        """Create document settings section."""
        content = self._create_section(parent, "Document Settings", "📄")
        
        # Default district
        district_frame = ctk.CTkFrame(content, fg_color="transparent")
        district_frame.pack(fill="x", pady=5)
        
        district_label = ctk.CTkLabel(
            district_frame,
            text="Default District:",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY,
            width=150,
            anchor="w"
        )
        district_label.pack(side="left")
        
        from config.districts import NEPAL_DISTRICTS_SORTED
        
        self.district_var = ctk.StringVar(value=self.settings.get('default_district', Settings.DEFAULT_DISTRICT))
        district_menu = ctk.CTkOptionMenu(
            district_frame,
            values=NEPAL_DISTRICTS_SORTED,
            variable=self.district_var,
            width=200,
            height=35,
            font=AppTheme.get_font("normal"),
            command=self._on_district_change
        )
        district_menu.pack(side="left")
        
        # Auto-save
        autosave_frame = ctk.CTkFrame(content, fg_color="transparent")
        autosave_frame.pack(fill="x", pady=10)
        
        autosave_label = ctk.CTkLabel(
            autosave_frame,
            text="Auto-save:",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY,
            width=150,
            anchor="w"
        )
        autosave_label.pack(side="left")
        
        self.autosave_var = ctk.BooleanVar(value=self.settings.get('autosave', 'true') == 'true')
        autosave_switch = ctk.CTkSwitch(
            autosave_frame,
            text="Enabled",
            variable=self.autosave_var,
            font=AppTheme.get_font("normal"),
            command=self._on_autosave_change
        )
        autosave_switch.pack(side="left")
    
    def _create_data_section(self, parent):
        """Create data section."""
        content = self._create_section(parent, "Data & Storage", "💾")
        
        # Database location
        self._create_info_row(content, "Database:", str(Settings.DATABASE_PATH))
        
        # Trash auto-delete
        trash_frame = ctk.CTkFrame(content, fg_color="transparent")
        trash_frame.pack(fill="x", pady=5)
        
        trash_label = ctk.CTkLabel(
            trash_frame,
            text="Auto-delete trash after:",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY,
            width=150,
            anchor="w"
        )
        trash_label.pack(side="left")
        
        trash_info = ctk.CTkLabel(
            trash_frame,
            text="30 days",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        trash_info.pack(side="left")
    
    def _create_info_row(self, parent, label: str, value: str):
        """Create an info row."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=5)
        
        label_widget = ctk.CTkLabel(
            row,
            text=label,
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY,
            width=150,
            anchor="w"
        )
        label_widget.pack(side="left")
        
        value_widget = ctk.CTkLabel(
            row,
            text=value,
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        value_widget.pack(side="left")
    
    def _on_theme_change(self, value: str):
        """Handle theme change."""
        self.local_db.set_setting('theme', value.lower())
    
    def _on_district_change(self, value: str):
        """Handle district change."""
        self.local_db.set_setting('default_district', value)
    
    def _on_autosave_change(self):
        """Handle auto-save toggle."""
        value = 'true' if self.autosave_var.get() else 'false'
        self.local_db.set_setting('autosave', value)