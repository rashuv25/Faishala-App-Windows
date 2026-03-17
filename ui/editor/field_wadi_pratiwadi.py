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
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", expand=True)

        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        # Left card
        wadi_card = ctk.CTkFrame(
            container,
            fg_color=AppTheme.BACKGROUND_COLOR,
            corner_radius=10,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR
        )
        wadi_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        wadi_label = ctk.CTkLabel(
            wadi_card,
            text="वादी",
            font=AppTheme.get_font("normal", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        wadi_label.pack(anchor="w", padx=12, pady=(10, 6))

        self.wadi_text = ctk.CTkTextbox(
            wadi_card,
            height=160,
            font=AppTheme.get_font("normal"),
            wrap="word",
            fg_color=AppTheme.CARD_COLOR,
            border_width=0
        )
        self.wadi_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        if self.wadi_value:
            self.wadi_text.insert("1.0", self.wadi_value)

        self.wadi_text.bind("<KeyRelease>", self._on_wadi_type)

        # Right card
        pratiwadi_card = ctk.CTkFrame(
            container,
            fg_color=AppTheme.BACKGROUND_COLOR,
            corner_radius=10,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR
        )
        pratiwadi_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        pratiwadi_label = ctk.CTkLabel(
            pratiwadi_card,
            text="प्रतिवादी",
            font=AppTheme.get_font("normal", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        pratiwadi_label.pack(anchor="w", padx=12, pady=(10, 6))

        self.pratiwadi_text = ctk.CTkTextbox(
            pratiwadi_card,
            height=160,
            font=AppTheme.get_font("normal"),
            wrap="word",
            fg_color=AppTheme.CARD_COLOR,
            border_width=0
        )
        self.pratiwadi_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

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