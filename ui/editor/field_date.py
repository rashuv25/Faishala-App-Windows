# -*- coding: utf-8 -*-
"""Nepali date field component using ttk Combobox."""

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from typing import Callable, Optional, Union

from ui.theme import AppTheme
from config.constants import NEPALI_MONTHS
from utils.nepali_datetime import NepaliDateTimeHelper


class DateField(ctk.CTkFrame):
    """Nepali date picker field."""

    def __init__(
        self,
        parent,
        year: Optional[Union[int, str]] = None,
        month: Optional[Union[int, str]] = None,
        day: Optional[Union[int, str]] = None,
        day_num: Optional[Union[int, str]] = None,
        on_change: Callable[[int, int, int, int], None] = None
    ):
        """Initialize date field."""
        super().__init__(parent, fg_color="transparent")

        self.on_change = on_change
        self.date_helper = NepaliDateTimeHelper()

        today = self.date_helper.get_today()

        self.year = self._to_int(year, today["year"])
        self.month = self._to_int(month, today["month"])
        self.day = self._to_int(day, today["day"])
        self.day_num = self._to_int(day_num, today["weekday"])

        self._create_widgets()

    def _to_int(self, value: Optional[Union[int, str]], default: int) -> int:
        """Convert value to integer safely."""
        if value is None:
            return default
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            try:
                return int(value)
            except Exception:
                return default
        return default

    def _create_widgets(self):
        """Create date picker widgets."""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("Mudda.TCombobox", padding=6)

        title_label = ctk.CTkLabel(
            self,
            text="मिति",
            font=AppTheme.get_font("normal", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        title_label.pack(anchor="w", pady=(0, 8))

        card = ctk.CTkFrame(
            self,
            fg_color=AppTheme.BACKGROUND_COLOR,
            corner_radius=10,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR
        )
        card.pack(fill="x")

        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(anchor="w", padx=12, pady=12)

        ctk.CTkLabel(
            container,
            text="ईति सम्वत",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        ).pack(side="left", padx=(0, 10))

        years = [str(y) for y in self.date_helper.get_years_range(2070, 2090)]
        self.year_var = tk.StringVar(value=str(self.year))
        self.year_dropdown = ttk.Combobox(
            container,
            textvariable=self.year_var,
            values=years,
            state="readonly",
            width=8,
            style="Mudda.TCombobox",
            font=(AppTheme.FONT_FAMILY_FALLBACK, 12)
        )
        self.year_dropdown.pack(side="left", padx=(0, 6))
        self.year_dropdown.bind("<<ComboboxSelected>>", self._on_year_change)

        ctk.CTkLabel(
            container,
            text="साल",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        ).pack(side="left", padx=(0, 10))

        self.month_var = tk.StringVar(value=NEPALI_MONTHS[self.month - 1])
        self.month_dropdown = ttk.Combobox(
            container,
            textvariable=self.month_var,
            values=NEPALI_MONTHS,
            state="readonly",
            width=10,
            style="Mudda.TCombobox",
            font=(AppTheme.FONT_FAMILY_FALLBACK, 12)
        )
        self.month_dropdown.pack(side="left", padx=(0, 10))
        self.month_dropdown.bind("<<ComboboxSelected>>", self._on_month_change)

        days = [str(d) for d in range(1, 33)]
        self.day_var = tk.StringVar(value=str(self.day))
        self.day_dropdown = ttk.Combobox(
            container,
            textvariable=self.day_var,
            values=days,
            state="readonly",
            width=5,
            style="Mudda.TCombobox",
            font=(AppTheme.FONT_FAMILY_FALLBACK, 12)
        )
        self.day_dropdown.pack(side="left", padx=(0, 6))
        self.day_dropdown.bind("<<ComboboxSelected>>", self._on_day_change)

        ctk.CTkLabel(
            container,
            text="गते रोज",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        ).pack(side="left", padx=(0, 6))

        day_nums = [str(d) for d in range(1, 8)]
        self.day_num_var = tk.StringVar(value=str(self.day_num))
        self.day_num_dropdown = ttk.Combobox(
            container,
            textvariable=self.day_num_var,
            values=day_nums,
            state="readonly",
            width=5,
            style="Mudda.TCombobox",
            font=(AppTheme.FONT_FAMILY_FALLBACK, 12)
        )
        self.day_num_dropdown.pack(side="left", padx=(0, 6))
        self.day_num_dropdown.bind("<<ComboboxSelected>>", self._on_day_num_change)

        ctk.CTkLabel(
            container,
            text="शुभम्",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        ).pack(side="left")

    def _on_year_change(self, event=None):
        try:
            self.year = int(self.year_var.get())
        except Exception:
            pass
        self._notify_change()

    def _on_month_change(self, event=None):
        try:
            self.month = NEPALI_MONTHS.index(self.month_var.get()) + 1
        except Exception:
            pass
        self._notify_change()

    def _on_day_change(self, event=None):
        try:
            self.day = int(self.day_var.get())
        except Exception:
            pass
        self._notify_change()

    def _on_day_num_change(self, event=None):
        try:
            self.day_num = int(self.day_num_var.get())
        except Exception:
            pass
        self._notify_change()

    def _notify_change(self):
        if self.on_change:
            self.on_change(self.year, self.month, self.day, self.day_num)

    def get_date(self) -> dict:
        """Get selected date."""
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "day_num": self.day_num
        }

    def set_date(self, year: int, month: int, day: int, day_num: int):
        """Set date values."""
        self.year = year
        self.month = month
        self.day = day
        self.day_num = day_num

        self.year_var.set(str(year))
        self.month_var.set(NEPALI_MONTHS[month - 1])
        self.day_var.set(str(day))
        self.day_num_var.set(str(day_num))