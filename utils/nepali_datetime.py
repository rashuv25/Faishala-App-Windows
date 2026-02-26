# -*- coding: utf-8 -*-
"""Nepali date/time utilities."""

from typing import Dict, List, Tuple
from config.constants import NEPALI_MONTHS, NEPALI_DAYS, NEPALI_NUMBERS

try:
    import nepali_datetime
    NEPALI_DATETIME_AVAILABLE = True
except ImportError:
    NEPALI_DATETIME_AVAILABLE = False


class NepaliDateTimeHelper:
    """Helper class for Nepali date/time operations."""
    
    @staticmethod
    def get_today() -> Dict:
        """Get today's Nepali date."""
        if NEPALI_DATETIME_AVAILABLE:
            today = nepali_datetime.date.today()
            return {
                'year': today.year,
                'month': today.month,
                'month_name': NEPALI_MONTHS[today.month - 1],
                'day': today.day,
                'weekday': today.weekday() + 1,
                'weekday_name': NEPALI_DAYS[today.weekday() + 1]
            }
        return {
            'year': 2081,
            'month': 1,
            'month_name': NEPALI_MONTHS[0],
            'day': 1,
            'weekday': 1,
            'weekday_name': NEPALI_DAYS[1]
        }
    
    @staticmethod
    def to_nepali_number(num: int) -> str:
        """Convert integer to Nepali number string."""
        return ''.join(NEPALI_NUMBERS.get(d, d) for d in str(num))
    
    @staticmethod
    def get_years_range(start: int = 2070, end: int = 2090) -> List[int]:
        """Get range of Nepali years."""
        return list(range(start, end + 1))
    
    @staticmethod
    def get_months() -> List[str]:
        """Get list of Nepali months."""
        return NEPALI_MONTHS.copy()
    
    @staticmethod
    def get_days_in_month(year: int, month: int) -> int:
        """Get number of days in a Nepali month."""
        # Simplified - actual implementation needs BS calendar data
        if NEPALI_DATETIME_AVAILABLE:
            try:
                return nepali_datetime.date(year, month, 1).max_day
            except:
                pass
        
        # Default days per month (approximate)
        default_days = [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30]
        return default_days[month - 1] if 1 <= month <= 12 else 30
    
    @staticmethod
    def get_weekdays() -> Dict[int, str]:
        """Get weekday names."""
        return NEPALI_DAYS.copy()