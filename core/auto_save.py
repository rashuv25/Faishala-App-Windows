# -*- coding: utf-8 -*-
"""Auto-save functionality."""

from typing import Dict, Any, Callable, Optional
import threading
import time

from database.local_db import LocalDatabase


class AutoSaveManager:
    """Manages auto-save functionality."""
    
    def __init__(self, document_id: int, save_callback: Optional[Callable] = None):
        """Initialize auto-save manager."""
        self.document_id = document_id
        self.save_callback = save_callback
        self.local_db = LocalDatabase()
        self._pending_save = False
        self._last_state: Dict[str, Any] = {}
        self._lock = threading.Lock()
    
    def on_change(self, field_name: str, value: Any) -> None:
        """Called when any field changes."""
        with self._lock:
            self._last_state[field_name] = value
            self._pending_save = True
            self._save_immediately()
    
    def _save_immediately(self) -> None:
        """Save immediately (called on every keystroke)."""
        if self._pending_save and self._last_state:
            try:
                self.local_db.save_auto_save(self.document_id, self._last_state)
                if self.save_callback:
                    self.save_callback(self._last_state)
                self._pending_save = False
            except Exception as e:
                print(f"Auto-save error: {e}")
    
    def get_recovered_state(self) -> Optional[Dict[str, Any]]:
        """Get recovered state from auto-save."""
        return self.local_db.get_auto_save(self.document_id)
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current state."""
        return self._last_state.copy()