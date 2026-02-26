# -*- coding: utf-8 -*-
"""Tapsil (तपसिल) dynamic list field component."""

import customtkinter as ctk
from typing import Callable, List

from ui.theme import AppTheme
from config.constants import DEFAULT_TAPSIL_POINTS
from utils.helpers import to_nepali_number


class TapsilField(ctk.CTkFrame):
    """Dynamic tapsil points list with CRUD operations."""
    
    def __init__(
        self,
        parent,
        points: List[str] = None,
        on_change: Callable[[List[str]], None] = None
    ):
        """Initialize tapsil field."""
        super().__init__(parent, fg_color="transparent")
        
        self.on_change = on_change
        self.points = points if points and len(points) > 0 else DEFAULT_TAPSIL_POINTS.copy()
        self.point_widgets = []
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create tapsil widgets."""
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="तपसिल",
            font=AppTheme.get_font("normal", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        title_label.pack(anchor="w", pady=(0, 10))
        
        # Points container
        self.points_container = ctk.CTkFrame(self, fg_color="transparent")
        self.points_container.pack(fill="x")
        
        # Render existing points
        for i, point in enumerate(self.points):
            self._add_point_widget(i, point)
        
        # Add button
        self.add_btn = ctk.CTkButton(
            self,
            text="+ नयाँ तपसिल थप्नुहोस् (Add New Tapsil)",
            font=AppTheme.get_font("normal"),
            fg_color="transparent",
            hover_color=AppTheme.BACKGROUND_COLOR,
            text_color=AppTheme.PRIMARY_COLOR,
            anchor="w",
            command=self._add_new_point
        )
        self.add_btn.pack(anchor="w", pady=10)
    
    def _add_point_widget(self, index: int, value: str = ""):
        """Add a tapsil point widget."""
        point_frame = ctk.CTkFrame(self.points_container, fg_color="transparent")
        point_frame.pack(fill="x", pady=5)
        
        # Text area (content comes first, number at end)
        text_area = ctk.CTkTextbox(
            point_frame,
            height=80,
            font=AppTheme.get_font("normal"),
            wrap="word"
        )
        text_area.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        if value:
            text_area.insert("1.0", value)
        
        text_area.bind("<KeyRelease>", lambda e, idx=index: self._on_point_change(idx))
        
        # Number label (with dots)
        nepali_num = to_nepali_number(index + 1)
        number_label = ctk.CTkLabel(
            point_frame,
            text=f"...{nepali_num}",
            font=AppTheme.get_font("normal", bold=True),
            text_color=AppTheme.TEXT_PRIMARY,
            width=50
        )
        number_label.pack(side="left", padx=(0, 5))
        
        # Delete button
        delete_btn = ctk.CTkButton(
            point_frame,
            text="🗑️",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=AppTheme.BACKGROUND_COLOR,
            text_color=AppTheme.ERROR_COLOR,
            command=lambda idx=index: self._delete_point(idx)
        )
        delete_btn.pack(side="right")
        
        # Store widget reference
        self.point_widgets.append({
            'frame': point_frame,
            'text_area': text_area,
            'number_label': number_label
        })
    
    def _on_point_change(self, index: int):
        """Handle point text change."""
        if index < len(self.point_widgets):
            text_area = self.point_widgets[index]['text_area']
            self.points[index] = text_area.get("1.0", "end-1c")
            
            if self.on_change:
                self.on_change(self.points.copy())
    
    def _add_new_point(self):
        """Add a new empty point."""
        new_index = len(self.points)
        self.points.append("")
        self._add_point_widget(new_index, "")
        
        if self.on_change:
            self.on_change(self.points.copy())
    
    def _delete_point(self, index: int):
        """Delete a point."""
        # Always keep at least one point
        if len(self.points) <= 1:
            self.points[0] = ""
            self.point_widgets[0]['text_area'].delete("1.0", "end")
            if self.on_change:
                self.on_change(self.points.copy())
            return
        
        # Remove from data
        self.points.pop(index)
        
        # Remove widget
        widget = self.point_widgets.pop(index)
        widget['frame'].destroy()
        
        # Renumber remaining points
        self._renumber_points()
        
        if self.on_change:
            self.on_change(self.points.copy())
    
    def _renumber_points(self):
        """Renumber all points after deletion."""
        for i, widget in enumerate(self.point_widgets):
            nepali_num = to_nepali_number(i + 1)
            widget['number_label'].configure(text=f"...{nepali_num}")
    
    def get_points(self) -> List[str]:
        """Get all points."""
        return self.points.copy()
    
    def set_points(self, points: List[str]):
        """Set all points."""
        # Clear existing
        for widget in self.point_widgets:
            widget['frame'].destroy()
        self.point_widgets.clear()
        
        # Set new points
        self.points = points if points and len(points) > 0 else DEFAULT_TAPSIL_POINTS.copy()
        for i, point in enumerate(self.points):
            self._add_point_widget(i, point)