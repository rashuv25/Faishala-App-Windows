# # -*- coding: utf-8 -*-
# """User authentication logic."""

# import hashlib
# import secrets
# from typing import Optional, Dict, Tuple

# from database.local_db import LocalDatabase
# from database.remote_db import RemoteDatabase
# from .session_manager import SessionManager
# from .nepali_date_validator import NepaliDateValidator


# class Authenticator:
#     """Handles user authentication."""
    
#     def __init__(self):
#         """Initialize authenticator."""
#         self.local_db = LocalDatabase()
#         self.remote_db = RemoteDatabase()
#         self.session_manager = SessionManager()
#         self.date_validator = NepaliDateValidator()
    
#     def hash_password(self, password: str) -> str:
#         """Hash password using SHA-256."""
#         return hashlib.sha256(password.encode()).hexdigest()
    
#     def generate_token(self) -> str:
#         """Generate secure session token."""
#         return secrets.token_hex(32)
    
#     def needs_online_login(self) -> bool:
#         """Check if user needs to login online (new Nepali month)."""
#         return self.date_validator.is_new_nepali_month()
    
#     def login(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
#         """
#         Attempt to login user.
        
#         Returns:
#             Tuple of (success, message, user_data)
#         """
#         password_hash = self.hash_password(password)
        
#         # Check if online login is required
#         if self.needs_online_login():
#             # Try remote authentication
#             if not self.remote_db.is_connected():
#                 return (False, "इन्टरनेट आवश्यक छ। कृपया इन्टरनेट जडान गर्नुहोस्।", None)
            
#             user = self.remote_db.verify_credentials(username, password_hash)
#             if not user:
#                 return (False, "गलत प्रयोगकर्ता नाम वा पासवर्ड।", None)
            
#             # Update local database
#             token = self.generate_token()
#             nepali_year, nepali_month = self.date_validator.get_current_nepali_month()
            
#             self.local_db.update_user_login(
#                 user['id'], 
#                 nepali_year,
#                 nepali_month, 
#                 token
#             )
            
#             self.session_manager.set_session(user['id'], username, token)
#             return (True, "सफलतापूर्वक लगइन भयो।", user)
        
#         else:
#             # Offline login - check local database
#             user = self.local_db.get_user_by_username(username)
            
#             if not user:
#                 return (False, "प्रयोगकर्ता फेला परेन। कृपया इन्टरनेट जडान गर्नुहोस्।", None)
            
#             if user['password_hash'] != password_hash:
#                 return (False, "गलत पासवर्ड।", None)
            
#             # Check session token
#             if user['session_token']:
#                 self.session_manager.set_session(user['id'], username, user['session_token'])
#                 return (True, "सफलतापूर्वक लगइन भयो।", user)
            
#             return (False, "सत्र समाप्त भयो। कृपया इन्टरनेट जडान गरी लगइन गर्नुहोस्।", None)
    
#     def logout(self) -> None:
#         """Logout current user."""
#         self.session_manager.clear_session()






# -*- coding: utf-8 -*-
"""User authentication logic."""

import hashlib
import secrets
from typing import Optional, Dict, Tuple

from config.settings import Settings
from database.local_db import LocalDatabase
from database.remote_db import RemoteDatabase
from .session_manager import SessionManager
from .nepali_date_validator import NepaliDateValidator


class Authenticator:
    """Handles user authentication."""
    
    def __init__(self):
        """Initialize authenticator."""
        self.local_db = LocalDatabase()
        self.remote_db = RemoteDatabase()
        self.session_manager = SessionManager()
        self.date_validator = NepaliDateValidator()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def generate_token(self) -> str:
        """Generate secure session token."""
        return secrets.token_hex(32)
    
    def needs_online_login(self) -> bool:
        """Check if user needs to login online (new Nepali month)."""
        # Skip online check if in offline/development mode
        if Settings.OFFLINE_MODE:
            return False
        
        return self.date_validator.is_new_nepali_month()
    
    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Attempt to login user.
        
        Returns:
            Tuple of (success, message, user_data)
        """
        password_hash = self.hash_password(password)
        
        # Check if online login is required
        if self.needs_online_login():
            # Try remote authentication
            if not self.remote_db.is_connected():
                return (False, "इन्टरनेट आवश्यक छ। कृपया इन्टरनेट जडान गर्नुहोस्।", None)
            
            user = self.remote_db.verify_credentials(username, password_hash)
            if not user:
                return (False, "गलत प्रयोगकर्ता नाम वा पासवर्ड।", None)
            
            # Update local database
            token = self.generate_token()
            nepali_year, nepali_month = self.date_validator.get_current_nepali_month()
            
            self.local_db.update_user_login(
                user['id'], 
                nepali_year,
                nepali_month, 
                token
            )
            
            self.session_manager.set_session(user['id'], username, token)
            return (True, "सफलतापूर्वक लगइन भयो।", user)
        
        else:
            # Offline login - check local database
            user = self.local_db.get_user_by_username(username)
            
            if not user:
                return (False, "प्रयोगकर्ता फेला परेन।", None)
            
            if user['password_hash'] != password_hash:
                return (False, "गलत पासवर्ड।", None)
            
            # Create session for offline use
            token = user.get('session_token') or self.generate_token()
            self.session_manager.set_session(user['id'], username, token)
            
            # Update login date
            nepali_year, nepali_month = self.date_validator.get_current_nepali_month()
            self.local_db.update_user_login(user['id'], nepali_year, nepali_month, token)
            
            return (True, "सफलतापूर्वक लगइन भयो।", user)
    
    def logout(self) -> None:
        """Logout current user."""
        self.session_manager.clear_session()