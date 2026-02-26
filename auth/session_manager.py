# -*- coding: utf-8 -*-
"""Session management."""

from typing import Optional


class SessionManager:
    """Manages user session state."""
    
    _instance: Optional['SessionManager'] = None
    
    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._user_id = None
            cls._instance._username = None
            cls._instance._token = None
        return cls._instance
    
    def set_session(self, user_id: int, username: str, token: str) -> None:
        """Set current session."""
        self._user_id = user_id
        self._username = username
        self._token = token
    
    def clear_session(self) -> None:
        """Clear current session."""
        self._user_id = None
        self._username = None
        self._token = None
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in."""
        return self._user_id is not None
    
    @property
    def user_id(self) -> Optional[int]:
        """Get current user ID."""
        return self._user_id
    
    @property
    def username(self) -> Optional[str]:
        """Get current username."""
        return self._username
    
    @property
    def token(self) -> Optional[str]:
        """Get current session token."""
        return self._token