# # -*- coding: utf-8 -*-
# """Nepali date field component."""

# import customtkinter as ctk
# from typing import Callable, Optional

# from ui.theme import AppTheme
# from config.constants import NEPALI_MONTHS, NEPALI_DAYS
# from utils.nepali_datetime import NepaliDateTimeHelper
# from utils.helpers import to_nepali_number


# class DateField(ctk.CTkFrame):
#     """Nepali date picker field."""
    
#     def __init__(
#         self,
#         parent,
#         year: Optional[int] = None,
#         month: Optional[int] = None,
#         day: Optional[int] = None,
#         day_num: Optional[int] = None,
#         on_change: Callable[[int, int, int, int], None] = None
#     ):
#         """Initialize date field."""
#         super().__init__(parent, fg_color="transparent")
        
#         self.on_change = on_change
#         self.date_helper = NepaliDateTimeHelper()
        
#         # Get today's date as default
#         today = self.date_helper.get_today()
        
#         self.year = year if year else today['year']
#         self.month = month if month else today['month']
#         self.day = day if day else today['day']
#         self.day_num = day_num if day_num else today['weekday']
        
#         self._create_widgets()
    
#     def _create_widgets(self):
#         """Create date picker widgets."""
#         # Container
#         container = ctk.CTkFrame(self, fg_color="transparent")
#         container.pack(anchor="w")
        
#         # "ईति सम्वत" label
#         prefix_label = ctk.CTkLabel(
#             container,
#             text="ईति सम्वत",
#             font=AppTheme.get_font("normal"),
#             text_color=AppTheme.TEXT_PRIMARY
#         )
#         prefix_label.pack(side="left", padx=(0, 10))
        
#         # Year dropdown
#         years = [str(y) for y in self.date_helper.get_years_range(2070, 2090)]
#         self.year_dropdown = ctk.CTkComboBox(
#             container,
#             values=years,
#             width=80,
#             height=AppTheme.INPUT_HEIGHT,
#             font=AppTheme.get_font("normal"),
#             command=self._on_year_change
#         )
#         self.year_dropdown.set(str(self.year))
#         self.year_dropdown.pack(side="left", padx=(0, 5))
        
#         # "साल" label
#         sal_label = ctk.CTkLabel(
#             container,
#             text="साल",
#             font=AppTheme.get_font("normal"),
#             text_color=AppTheme.TEXT_PRIMARY
#         )
#         sal_label.pack(side="left", padx=(0, 10))
        
#         # Month dropdown
#         self.month_dropdown = ctk.CTkComboBox(
#             container,
#             values=NEPALI_MONTHS,
#             width=100,
#             height=AppTheme.INPUT_HEIGHT,
#             font=AppTheme.get_font("normal"),
#             command=self._on_month_change
#         )
#         self.month_dropdown.set(NEPALI_MONTHS[self.month - 1])
#         self.month_dropdown.pack(side="left", padx=(0, 10))
        
#         # Day dropdown
#         days = [str(d) for d in range(1, 33)]
#         self.day_dropdown = ctk.CTkComboBox(
#             container,
#             values=days,
#             width=60,
#             height=AppTheme.INPUT_HEIGHT,
#             font=AppTheme.get_font("normal"),
#             command=self._on_day_change
#         )
#         self.day_dropdown.set(str(self.day))
#         self.day_dropdown.pack(side="left", padx=(0, 5))
        
#         # "गते रोज" label
#         gate_label = ctk.CTkLabel(
#             container,
#             text="गते रोज",
#             font=AppTheme.get_font("normal"),
#             text_color=AppTheme.TEXT_PRIMARY
#         )
#         gate_label.pack(side="left", padx=(0, 5))
        
#         # Day number dropdown (1-7)
#         day_nums = [str(d) for d in range(1, 8)]
#         self.day_num_dropdown = ctk.CTkComboBox(
#             container,
#             values=day_nums,
#             width=60,
#             height=AppTheme.INPUT_HEIGHT,
#             font=AppTheme.get_font("normal"),
#             command=self._on_day_num_change
#         )
#         self.day_num_dropdown.set(str(self.day_num))
#         self.day_num_dropdown.pack(side="left", padx=(0, 5))
        
#         # "शुभम्" label
#         shubham_label = ctk.CTkLabel(
#             container,
#             text="शुभम्",
#             font=AppTheme.get_font("normal"),
#             text_color=AppTheme.TEXT_PRIMARY
#         )
#         shubham_label.pack(side="left")
    
#     def _on_year_change(self, value: str):
#         """Handle year change."""
#         self.year = int(value)
#         self._notify_change()
    
#     def _on_month_change(self, value: str):
#         """Handle month change."""
#         self.month = NEPALI_MONTHS.index(value) + 1
#         self._notify_change()
    
#     def _on_day_change(self, value: str):
#         """Handle day change."""
#         self.day = int(value)
#         self._notify_change()
    
#     def _on_day_num_change(self, value: str):
#         """Handle day number change."""
#         self.day_num = int(value)
#         self._notify_change()
    
#     def _notify_change(self):
#         """Notify parent of change."""
#         if self.on_change:
#             self.on_change(self.year, self.month, self.day, self.day_num)
    
#     def get_date(self) -> dict:
#         """Get current date values."""
#         return {
#             'year': self.year,
#             'month': self.month,
#             'day': self.day,
#             'day_num': self.day_num
#         }
    
#     def set_date(self, year: int, month: int, day: int, day_num: int):
#         """Set date values."""
#         self.year = year
#         self.month = month
#         self.day = day
#         self.day_num = day_num
        
#         self.year_dropdown.set(str(year))
#         self.month_dropdown.set(NEPALI_MONTHS[month - 1])
#         self.day_dropdown.set(str(day))
#         self.day_num_dropdown.set(str(day_num))



# -*- coding: utf-8 -*-
"""Nepali date field component."""

import customtkinter as ctk
from typing import Callable, Optional, Union

from ui.theme import AppTheme
from config.constants import NEPALI_MONTHS, NEPALI_DAYS
from utils.nepali_datetime import NepaliDateTimeHelper
from utils.helpers import to_nepali_number


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
        
        # Get today's date as default
        today = self.date_helper.get_today()
        
        # Convert values to integers (handle None, string, int)
        self.year = self._to_int(year, today['year'])
        self.month = self._to_int(month, today['month'])
        self.day = self._to_int(day, today['day'])
        self.day_num = self._to_int(day_num, today['weekday'])
        
        # Ensure month is in valid range (1-12)
        if self.month < 1 or self.month > 12:
            self.month = today['month']
        
        # Ensure day is in valid range (1-32)
        if self.day < 1 or self.day > 32:
            self.day = today['day']
        
        # Ensure day_num is in valid range (1-7)
        if self.day_num < 1 or self.day_num > 7:
            self.day_num = today['weekday']
        
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
            except (ValueError, TypeError):
                return default
        
        return default
    
    def _create_widgets(self):
        """Create date picker widgets."""
        # Container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(anchor="w")
        
        # "ईति सम्वत" label
        prefix_label = ctk.CTkLabel(
            container,
            text="ईति सम्वत",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        prefix_label.pack(side="left", padx=(0, 10))
        
        # Year dropdown
        years = [str(y) for y in self.date_helper.get_years_range(2070, 2090)]
        self.year_dropdown = ctk.CTkComboBox(
            container,
            values=years,
            width=80,
            height=AppTheme.INPUT_HEIGHT,
            font=AppTheme.get_font("normal"),
            command=self._on_year_change
        )
        self.year_dropdown.set(str(self.year))
        self.year_dropdown.pack(side="left", padx=(0, 5))
        
        # "साल" label
        sal_label = ctk.CTkLabel(
            container,
            text="साल",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        sal_label.pack(side="left", padx=(0, 10))
        
        # Month dropdown
        self.month_dropdown = ctk.CTkComboBox(
            container,
            values=NEPALI_MONTHS,
            width=100,
            height=AppTheme.INPUT_HEIGHT,
            font=AppTheme.get_font("normal"),
            command=self._on_month_change
        )
        # Safe month index access
        month_index = self.month - 1
        if 0 <= month_index < len(NEPALI_MONTHS):
            self.month_dropdown.set(NEPALI_MONTHS[month_index])
        else:
            self.month_dropdown.set(NEPALI_MONTHS[0])
        self.month_dropdown.pack(side="left", padx=(0, 10))
        
        # Day dropdown
        days = [str(d) for d in range(1, 33)]
        self.day_dropdown = ctk.CTkComboBox(
            container,
            values=days,
            width=60,
            height=AppTheme.INPUT_HEIGHT,
            font=AppTheme.get_font("normal"),
            command=self._on_day_change
        )
        self.day_dropdown.set(str(self.day))
        self.day_dropdown.pack(side="left", padx=(0, 5))
        
        # "गते रोज" label
        gate_label = ctk.CTkLabel(
            container,
            text="गते रोज",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        gate_label.pack(side="left", padx=(0, 5))
        
        # Day number dropdown (1-7)
        day_nums = [str(d) for d in range(1, 8)]
        self.day_num_dropdown = ctk.CTkComboBox(
            container,
            values=day_nums,
            width=60,
            height=AppTheme.INPUT_HEIGHT,
            font=AppTheme.get_font("normal"),
            command=self._on_day_num_change
        )
        self.day_num_dropdown.set(str(self.day_num))
        self.day_num_dropdown.pack(side="left", padx=(0, 5))
        
        # "शुभम्" label
        shubham_label = ctk.CTkLabel(
            container,
            text="शुभम्",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        shubham_label.pack(side="left")
    
    def _on_year_change(self, value: str):
        """Handle year change."""
        try:
            self.year = int(value)
        except (ValueError, TypeError):
            pass
        self._notify_change()
    
    def _on_month_change(self, value: str):
        """Handle month change."""
        try:
            self.month = NEPALI_MONTHS.index(value) + 1
        except (ValueError, IndexError):
            pass
        self._notify_change()
    
    def _on_day_change(self, value: str):
        """Handle day change."""
        try:
            self.day = int(value)
        except (ValueError, TypeError):
            pass
        self._notify_change()
    
    def _on_day_num_change(self, value: str):
        """Handle day number change."""
        try:
            self.day_num = int(value)
        except (ValueError, TypeError):
            pass
        self._notify_change()
    
    def _notify_change(self):
        """Notify parent of change."""
        if self.on_change:
            self.on_change(self.year, self.month, self.day, self.day_num)
    
    def get_date(self) -> dict:
        """Get current date values."""
        return {
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'day_num': self.day_num
        }
    
    def set_date(self, year: int, month: int, day: int, day_num: int):
        """Set date values."""
        self.year = self._to_int(year, self.year)
        self.month = self._to_int(month, self.month)
        self.day = self._to_int(day, self.day)
        self.day_num = self._to_int(day_num, self.day_num)
        
        self.year_dropdown.set(str(self.year))
        
        month_index = self.month - 1
        if 0 <= month_index < len(NEPALI_MONTHS):
            self.month_dropdown.set(NEPALI_MONTHS[month_index])
        
        self.day_dropdown.set(str(self.day))
        self.day_num_dropdown.set(str(self.day_num))