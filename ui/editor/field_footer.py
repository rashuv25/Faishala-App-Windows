# -*- coding: utf-8 -*-
"""Footer field component."""

import tkinter as tk
from tkinter import ttk
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
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("Mudda.TCombobox", padding=6)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", expand=True)

        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        # Typist card
        typist_card = ctk.CTkFrame(
            container,
            fg_color=AppTheme.BACKGROUND_COLOR,
            corner_radius=10,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR
        )
        typist_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        typist_inner = ctk.CTkFrame(typist_card, fg_color="transparent")
        typist_inner.pack(fill="x", padx=12, pady=12)

        typist_label = ctk.CTkLabel(
            typist_inner,
            text="टिपोट गर्ने ना.सु.",
            font=AppTheme.get_font("normal", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        typist_label.pack(anchor="w", pady=(0, 8))

        saved_typists = self.local_db.get_dictionary_items("typist_names")
        self.typist_var = tk.StringVar(value=self.typist_name)

        self.typist_input = ttk.Combobox(
            typist_inner,
            textvariable=self.typist_var,
            values=saved_typists,
            state="normal",
            style="Mudda.TCombobox",
            font=(AppTheme.FONT_FAMILY_FALLBACK, 12)
        )
        self.typist_input.pack(fill="x")
        self.typist_input.bind("<<ComboboxSelected>>", self._on_typist_change)
        self.typist_input.bind("<KeyRelease>", self._on_typist_change)
        self.typist_input.bind("<FocusOut>", self._on_typist_change)

        # Signature card
        cdo_card = ctk.CTkFrame(
            container,
            fg_color=AppTheme.BACKGROUND_COLOR,
            corner_radius=10,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR
        )
        cdo_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        cdo_inner = ctk.CTkFrame(cdo_card, fg_color="transparent")
        cdo_inner.pack(fill="x", padx=12, pady=12)

        dots_label = ctk.CTkLabel(
            cdo_inner,
            text="................................",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        dots_label.pack(anchor="e", pady=(0, 8))

        saved_cdo_names = self.local_db.get_dictionary_items("cdo_names")
        self.cdo_var = tk.StringVar(value=self.cdo_name)

        self.cdo_input = ttk.Combobox(
            cdo_inner,
            textvariable=self.cdo_var,
            values=saved_cdo_names,
            state="normal",
            style="Mudda.TCombobox",
            font=(AppTheme.FONT_FAMILY_FALLBACK, 12)
        )
        self.cdo_input.pack(fill="x", pady=(0, 8))
        self.cdo_input.bind("<<ComboboxSelected>>", self._on_cdo_change)
        self.cdo_input.bind("<KeyRelease>", self._on_cdo_change)
        self.cdo_input.bind("<FocusOut>", self._on_cdo_change)

        designation_label = ctk.CTkLabel(
            cdo_inner,
            text="प्रमुख जिल्ला अधिकारी",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        designation_label.pack(anchor="e")

    def _on_typist_change(self, event=None):
        """Handle typist change."""
        if self.on_typist_change:
            self.on_typist_change(self.typist_var.get())

    def _on_cdo_change(self, event=None):
        """Handle CDO change."""
        if self.on_cdo_change:
            self.on_cdo_change(self.cdo_var.get())

    def get_typist_value(self) -> str:
        """Get typist value."""
        return self.typist_var.get()

    def get_cdo_value(self) -> str:
        """Get CDO value."""
        return self.cdo_var.get()

    def set_typist_name(self, value: str):
        """Set typist value."""
        self.typist_var.set(value)

    def set_cdo_name(self, value: str):
        """Set CDO value."""
        self.cdo_var.set(value)