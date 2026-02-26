# -*- coding: utf-8 -*-
"""Undo/Redo functionality."""

from typing import Any, List, Optional, Dict
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class StateSnapshot:
    """Represents a state snapshot."""
    field_name: str
    value: Any
    cursor_position: Optional[int] = None


class UndoRedoManager:
    """Manages undo/redo operations."""
    
    def __init__(self, max_history: int = 100):
        """Initialize undo/redo manager."""
        self.max_history = max_history
        self._undo_stack: List[StateSnapshot] = []
        self._redo_stack: List[StateSnapshot] = []
    
    def save_state(self, field_name: str, value: Any, cursor_pos: Optional[int] = None) -> None:
        """Save current state for undo."""
        snapshot = StateSnapshot(
            field_name=field_name,
            value=deepcopy(value),
            cursor_position=cursor_pos
        )
        self._undo_stack.append(snapshot)
        
        # Clear redo stack on new action
        self._redo_stack.clear()
        
        # Limit history size
        if len(self._undo_stack) > self.max_history:
            self._undo_stack.pop(0)
    
    def undo(self) -> Optional[StateSnapshot]:
        """Undo last action."""
        if not self._undo_stack:
            return None
        
        snapshot = self._undo_stack.pop()
        self._redo_stack.append(snapshot)
        
        # Return previous state
        if self._undo_stack:
            return self._undo_stack[-1]
        return None
    
    def redo(self) -> Optional[StateSnapshot]:
        """Redo last undone action."""
        if not self._redo_stack:
            return None
        
        snapshot = self._redo_stack.pop()
        self._undo_stack.append(snapshot)
        return snapshot
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return len(self._undo_stack) > 0
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return len(self._redo_stack) > 0
    
    def clear(self) -> None:
        """Clear all history."""
        self._undo_stack.clear()
        self._redo_stack.clear()