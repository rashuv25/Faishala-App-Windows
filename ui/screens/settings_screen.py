# -*- coding: utf-8 -*-
"""Settings screen UI."""

import tkinter as tk
from tkinter import ttk
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

        content = ctk.CTkFrame(section, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=(0, 15))

        return content

    def _create_app_info_section(self, parent):
        """Create app info section."""
        content = self._create_section(parent, "App Information", "ℹ️")
        self._create_info_row(content, "App Name:", Settings.APP_NAME)
        self._create_info_row(content, "Version:", Settings.APP_VERSION)
        self._create_info_row(content, "Developer:", "Your Company Name")

    def _create_appearance_section(self, parent):
        """Create appearance section."""
        content = self._create_section(parent, "Appearance", "🎨")

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

        saved_theme = self.settings.get("theme", "light").lower()
        theme_display_value = saved_theme.capitalize() if saved_theme in ("light", "dark", "system") else "Light"

        self.theme_var = ctk.StringVar(value=theme_display_value)
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

        theme_note = ctk.CTkLabel(
            content,
            text="Theme changes now apply immediately.",
            font=AppTheme.get_font("small"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        theme_note.pack(anchor="w", pady=(5, 0))

    def _create_document_section(self, parent):
        """Create document settings section."""
        content = self._create_section(parent, "Document Settings", "📄")

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

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Settings.TCombobox", padding=6)

        district_value = self.settings.get("default_district", Settings.DEFAULT_DISTRICT)
        self.district_var = tk.StringVar(value=district_value)

        self.district_menu = ttk.Combobox(
            district_frame,
            textvariable=self.district_var,
            values=NEPAL_DISTRICTS_SORTED,
            state="readonly",
            width=18,
            style="Settings.TCombobox",
            font=(AppTheme.FONT_FAMILY_FALLBACK, 12)
        )
        self.district_menu.pack(side="left")
        self.district_menu.bind("<<ComboboxSelected>>", self._on_district_change_event)

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

        self.autosave_var = ctk.BooleanVar(
            value=self.settings.get("autosave", "true") == "true"
        )
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

        self._create_info_row(content, "Database:", str(Settings.DATABASE_PATH))

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

        # Developer options
        if Settings.DEBUG:
            dev_divider = ctk.CTkLabel(
                content,
                text="Developer Options",
                font=AppTheme.get_font("normal", bold=True),
                text_color=AppTheme.TEXT_PRIMARY
            )
            dev_divider.pack(anchor="w", pady=(15, 5))

            rb_frame = ctk.CTkFrame(content, fg_color="transparent")
            rb_frame.pack(fill="x", pady=5)

            rb_label = ctk.CTkLabel(
                rb_frame,
                text="Remote backup (silent):",
                font=AppTheme.get_font("normal"),
                text_color=AppTheme.TEXT_PRIMARY,
                width=150,
                anchor="w"
            )
            rb_label.pack(side="left")

            rb_default = str(self.settings.get("remote_backup_enabled", "false")).lower() in ("true", "1", "yes", "on")
            self.remote_backup_var = ctk.BooleanVar(value=rb_default)

            rb_switch = ctk.CTkSwitch(
                rb_frame,
                text="Enabled",
                variable=self.remote_backup_var,
                onvalue=True,
                offvalue=False,
                font=AppTheme.get_font("normal"),
                command=self._on_remote_backup_change
            )
            rb_switch.pack(side="left", padx=(10, 0))

            rb_hint = ctk.CTkLabel(
                content,
                text="Uploads DOCX backups only if a Supabase backup request exists.",
                font=AppTheme.get_font("small"),
                text_color=AppTheme.TEXT_SECONDARY
            )
            rb_hint.pack(anchor="w", pady=(2, 0))

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
        theme = value.lower()
        self.local_db.set_setting("theme", theme)
        self.settings["theme"] = theme
        AppTheme.set_theme(theme)

    def _on_district_change_event(self, event=None):
        """Handle district change from ttk combobox."""
        value = self.district_var.get()
        self.local_db.set_setting("default_district", value)
        self.settings["default_district"] = value

    def _on_autosave_change(self):
        """Handle auto-save toggle."""
        value = "true" if self.autosave_var.get() else "false"
        self.local_db.set_setting("autosave", value)
        self.settings["autosave"] = value

    def _on_remote_backup_change(self):
        """Handle remote backup toggle."""
        value = "true" if getattr(self, "remote_backup_var", None) and self.remote_backup_var.get() else "false"
        self.local_db.set_setting("remote_backup_enabled", value)
        self.settings["remote_backup_enabled"] = value