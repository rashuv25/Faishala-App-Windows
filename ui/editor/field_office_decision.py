# -*- coding: utf-8 -*-
"""Office decision (कार्यालयको ठहर) field component."""

import customtkinter as ctk
from typing import Callable

from ui.theme import AppTheme
from config.constants import DEFAULT_OFFICE_DECISION, TAB_SPACES


class OfficeDecisionField(ctk.CTkFrame):
    """Office decision text area with default content."""
    
    def __init__(
        self,
        parent,
        value: str = "",
        on_change: Callable[[str], None] = None
    ):
        """Initialize office decision field."""
        super().__init__(parent, fg_color="transparent")
        
        self.on_change = on_change
        self.value = value if value else DEFAULT_OFFICE_DECISION
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create office decision widgets."""
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="कार्यालयको ठहर",
            font=AppTheme.get_font("normal", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        title_label.pack(anchor="w", pady=(0, 10))
        
        # Text area
        self.text_area = ctk.CTkTextbox(
            self,
            height=300,
            font=AppTheme.get_font("normal"),
            wrap="word"
        )
        self.text_area.pack(fill="x", expand=True)
        
        # Insert default/existing content with indentation
        indented_value = self._add_indentation(self.value)
        self.text_area.insert("1.0", indented_value)
        
        # Bind events
        self.text_area.bind("<KeyRelease>", self._on_text_change)
        self.text_area.bind("<Tab>", self._handle_tab)
    
    def _add_indentation(self, text: str) -> str:
        """Add indentation to start of paragraphs."""
        indent = " " * TAB_SPACES
        lines = text.split('\n')
        indented_lines = []
        
        for line in lines:
            if line.strip():
                # Add indent if line doesn't already have it
                if not line.startswith(indent) and not line.startswith('\t'):
                    line = indent + line
            indented_lines.append(line)
        
        return '\n'.join(indented_lines)
    
    def _handle_tab(self, event):
        """Handle Tab key for indentation."""
        self.text_area.insert("insert", " " * TAB_SPACES)
        return "break"  # Prevent default tab behavior
    
    def _on_text_change(self, event):
        """Handle text change."""
        if self.on_change:
            self.on_change(self.get_value())
    
    def get_value(self) -> str:
        """Get text value."""
        return self.text_area.get("1.0", "end-1c")
    
    def set_value(self, value: str):
        """Set text value."""
        self.text_area.delete("1.0", "end")
        indented_value = self._add_indentation(value)
        self.text_area.insert("1.0", indented_value)