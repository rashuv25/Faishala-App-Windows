# -*- coding: utf-8 -*-
"""District field component using ttk Combobox for better dropdown behavior."""

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from typing import Callable

from ui.theme import AppTheme
from config.districts import NEPAL_DISTRICTS_SORTED


class DistrictField(ctk.CTkFrame):
    """District selection field."""

    def __init__(
        self,
        parent,
        default_value: str = "",
        on_change: Callable[[str], None] = None
    ):
        """Initialize district field."""
        super().__init__(parent, fg_color="transparent")

        self.on_change = on_change
        self.value = default_value or "मोरङ"

        self._create_widgets()

    def _create_widgets(self):
        """Create district dropdown."""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Mudda.TCombobox",
            padding=6
        )

        self.var = tk.StringVar(value=self.value)

        self.combo = ttk.Combobox(
            self,
            textvariable=self.var,
            values=NEPAL_DISTRICTS_SORTED,
            state="readonly",
            width=14,
            style="Mudda.TCombobox",
            font=(AppTheme.FONT_FAMILY_FALLBACK, 12)
        )
        self.combo.pack(fill="x")

        self.combo.bind("<<ComboboxSelected>>", self._on_select)

    def _on_select(self, event=None):
        """Handle district selection."""
        if self.on_change:
            self.on_change(self.var.get())

    def get_value(self) -> str:
        """Get selected district."""
        return self.var.get()

    def set_value(self, value: str):
        """Set selected district."""
        self.var.set(value)