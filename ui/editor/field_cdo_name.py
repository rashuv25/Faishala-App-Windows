# -*- coding: utf-8 -*-
"""CDO name field component using ttk Combobox."""

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from typing import Callable

from ui.theme import AppTheme
from database.local_db import LocalDatabase


class CDONameField(ctk.CTkFrame):
    """CDO name selection/input field."""

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
        """Create CDO name field."""
        saved_names = self.local_db.get_dictionary_items("cdo_names")

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Mudda.TCombobox",
            padding=6
        )

        self.var = tk.StringVar(value=self.default_value)

        self.combo = ttk.Combobox(
            self,
            textvariable=self.var,
            values=saved_names,
            state="normal",
            width=18,
            style="Mudda.TCombobox",
            font=(AppTheme.FONT_FAMILY_FALLBACK, 12)
        )
        self.combo.pack(fill="x")

        self.combo.bind("<<ComboboxSelected>>", self._on_change)
        self.combo.bind("<KeyRelease>", self._on_change)
        self.combo.bind("<FocusOut>", self._on_change)

    def _on_change(self, event=None):
        """Handle value change."""
        if self.on_change:
            self.on_change(self.var.get())

    def get_value(self) -> str:
        """Get CDO name."""
        return self.var.get()

    def set_value(self, value: str):
        """Set CDO name."""
        self.var.set(value)