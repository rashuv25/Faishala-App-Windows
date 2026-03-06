# # -*- coding: utf-8 -*-
# """Nepali date validation for monthly login."""

# from typing import Tuple
# from database.local_db import LocalDatabase

# try:
#     import nepali_datetime
#     NEPALI_DATETIME_AVAILABLE = True
# except ImportError:
#     NEPALI_DATETIME_AVAILABLE = False


# class NepaliDateValidator:
#     """Validates Nepali date for login requirements."""
    
#     def __init__(self):
#         """Initialize validator."""
#         self.local_db = LocalDatabase()
    
#     def get_current_nepali_month(self) -> Tuple[int, int]:
#         """Get current Nepali year and month."""
#         if NEPALI_DATETIME_AVAILABLE:
#             now = nepali_datetime.date.today()
#             return (now.year, now.month)
#         else:
#             # Fallback - return dummy values (should not happen in production)
#             return (2081, 1)
    
#     def get_current_nepali_date(self) -> dict:
#         """Get current Nepali date details."""
#         if NEPALI_DATETIME_AVAILABLE:
#             now = nepali_datetime.date.today()
#             return {
#                 'year': now.year,
#                 'month': now.month,
#                 'day': now.day,
#                 'weekday': now.weekday() + 1  # 1 = Sunday
#             }
#         else:
#             return {
#                 'year': 2081,
#                 'month': 1,
#                 'day': 1,
#                 'weekday': 1
#             }
    
#     def is_new_nepali_month(self) -> bool:
#         """Check if current month is different from last login month."""
#         current_year, current_month = self.get_current_nepali_month()
        
#         # Get stored login info
#         stored_year = self.local_db.get_setting('last_login_nepali_year')
#         stored_month = self.local_db.get_setting('last_login_nepali_month')
        
#         if stored_year is None or stored_month is None:
#             return True  # First time login
        
#         if int(stored_year) != current_year or int(stored_month) != current_month:
#             return True
        
#         return False
    
#     def update_login_month(self) -> None:
#         """Update stored login month."""
#         current_year, current_month = self.get_current_nepali_month()
#         self.local_db.set_setting('last_login_nepali_year', str(current_year))
#         self.local_db.set_setting('last_login_nepali_month', str(current_month))






# -*- coding: utf-8 -*-
"""Nepali date validation for monthly login."""

from typing import Tuple
from database.local_db import LocalDatabase

try:
    import nepali_datetime
    NEPALI_DATETIME_AVAILABLE = True
except ImportError:
    NEPALI_DATETIME_AVAILABLE = False


class NepaliDateValidator:
    """Validates Nepali date for login requirements."""

    def __init__(self):
        """Initialize validator."""
        self.local_db = LocalDatabase()

    def get_current_nepali_month(self) -> Tuple[int, int]:
        """Get current Nepali year and month."""
        if NEPALI_DATETIME_AVAILABLE:
            now = nepali_datetime.date.today()
            return (now.year, now.month)
        # Fallback (dev only)
        return (2081, 1)

    def get_current_nepali_date(self) -> dict:
        """Get current Nepali date details."""
        if NEPALI_DATETIME_AVAILABLE:
            now = nepali_datetime.date.today()
            return {
                "year": now.year,
                "month": now.month,
                "day": now.day,
                "weekday": now.weekday() + 1  # 1 = Sunday
            }
        return {"year": 2081, "month": 1, "day": 1, "weekday": 1}

    def get_grace_days(self, default: int = 3) -> int:
        """How many days into new Nepali month offline login is allowed when internet is unavailable."""
        value = self.local_db.get_setting("monthly_verify_grace_days")
        if value is None:
            return default
        try:
            days = int(str(value).strip())
            return days if days >= 0 else default
        except Exception:
            return default

    def within_grace_period(self) -> bool:
        """True if today is within the allowed grace days of the Nepali month."""
        # If nepali_datetime isn't available, don't block users in dev
        if not NEPALI_DATETIME_AVAILABLE:
            return True

        day = self.get_current_nepali_date().get("day", 1)
        grace_days = self.get_grace_days(default=3)
        # Example: grace_days=3 => allow day 1,2,3
        return int(day) <= int(grace_days)

    def is_new_nepali_month(self) -> bool:
        """Check if current month is different from last verified/login month stored in app_settings."""
        current_year, current_month = self.get_current_nepali_month()

        stored_year = self.local_db.get_setting("last_login_nepali_year")
        stored_month = self.local_db.get_setting("last_login_nepali_month")

        if stored_year is None or stored_month is None:
            return True  # First time (no stored state)

        try:
            if int(stored_year) != int(current_year) or int(stored_month) != int(current_month):
                return True
        except Exception:
            return True

        return False

    def update_login_month(self) -> None:
        """Update stored login month (app_settings)."""
        current_year, current_month = self.get_current_nepali_month()
        self.local_db.set_setting("last_login_nepali_year", str(current_year))
        self.local_db.set_setting("last_login_nepali_month", str(current_month))