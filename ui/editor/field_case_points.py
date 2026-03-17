# -*- coding: utf-8 -*-
"""Case points dynamic list field component."""

import customtkinter as ctk
from typing import Callable, List

from ui.theme import AppTheme
from utils.helpers import to_nepali_number


class CasePointsField(ctk.CTkFrame):
    """Dynamic case points list."""

    def __init__(
        self,
        parent,
        points: List[str] = None,
        on_change: Callable[[List[str]], None] = None
    ):
        """Initialize case points field."""
        super().__init__(parent, fg_color="transparent")

        self.on_change = on_change
        self.points = points if points else [""]
        self.point_widgets = []

        self._create_widgets()

    def _create_widgets(self):
        """Create case points widgets."""
        title_label = ctk.CTkLabel(
            self,
            text="केसको संक्षिप्त व्यहोरा",
            font=AppTheme.get_font("normal", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        title_label.pack(anchor="w", pady=(0, 8))

        note_label = ctk.CTkLabel(
            self,
            text="प्रत्येक बुँदा अलग-अलग लेख्नुहोस्।",
            font=AppTheme.get_font("small"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        note_label.pack(anchor="w", pady=(0, 10))

        self.points_container = ctk.CTkFrame(self, fg_color="transparent")
        self.points_container.pack(fill="x")

        for i, point in enumerate(self.points):
            self._add_point_widget(i, point)

        self.add_btn = ctk.CTkButton(
            self,
            text="+ नयाँ बुँदा थप्नुहोस्",
            height=36,
            font=AppTheme.get_font("normal"),
            fg_color="transparent",
            hover_color=AppTheme.HOVER_LIGHT,
            text_color=AppTheme.PRIMARY_COLOR,
            anchor="w",
            command=self._add_new_point
        )
        self.add_btn.pack(anchor="w", pady=(10, 0))

    def _add_point_widget(self, index: int, value: str = ""):
        """Add a point widget."""
        point_card = ctk.CTkFrame(
            self.points_container,
            fg_color=AppTheme.BACKGROUND_COLOR,
            corner_radius=10,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR
        )
        point_card.pack(fill="x", pady=6)

        row = ctk.CTkFrame(point_card, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=10)

        nepali_num = to_nepali_number(index + 1)
        number_label = ctk.CTkLabel(
            row,
            text=f"{nepali_num}.",
            font=AppTheme.get_font("normal", bold=True),
            text_color=AppTheme.TEXT_PRIMARY,
            width=34,
            anchor="n"
        )
        number_label.pack(side="left", padx=(0, 10), pady=(6, 0))

        text_area = ctk.CTkTextbox(
            row,
            height=110,
            font=AppTheme.get_font("normal"),
            wrap="word",
            fg_color=AppTheme.CARD_COLOR,
            border_width=0
        )
        text_area.pack(side="left", fill="x", expand=True, padx=(0, 10))

        if value:
            text_area.insert("1.0", value)

        text_area.bind("<KeyRelease>", lambda e, idx=index: self._on_point_change(idx))

        delete_btn = ctk.CTkButton(
            row,
            text="🗑️",
            width=34,
            height=34,
            fg_color="transparent",
            hover_color=AppTheme.DELETE_HOVER,
            text_color=AppTheme.ERROR_COLOR,
            corner_radius=6,
            command=lambda idx=index: self._delete_point(idx)
        )
        delete_btn.pack(side="right", pady=(2, 0))

        self.point_widgets.append({
            "frame": point_card,
            "text_area": text_area,
            "number_label": number_label
        })

    def _on_point_change(self, index: int):
        """Handle point text change."""
        if index < len(self.point_widgets):
            text_area = self.point_widgets[index]["text_area"]
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
        if len(self.points) <= 1:
            self.points[0] = ""
            self.point_widgets[0]["text_area"].delete("1.0", "end")
            if self.on_change:
                self.on_change(self.points.copy())
            return

        self.points.pop(index)
        widget = self.point_widgets.pop(index)
        widget["frame"].destroy()
        self._renumber_points()

        if self.on_change:
            self.on_change(self.points.copy())

    def _renumber_points(self):
        """Renumber all points after deletion."""
        for i, widget in enumerate(self.point_widgets):
            nepali_num = to_nepali_number(i + 1)
            widget["number_label"].configure(text=f"{nepali_num}.")

    def get_points(self) -> List[str]:
        """Get all points."""
        return self.points.copy()

    def set_points(self, points: List[str]):
        """Set all points."""
        for widget in self.point_widgets:
            widget["frame"].destroy()
        self.point_widgets.clear()

        self.points = points if points else [""]
        for i, point in enumerate(self.points):
            self._add_point_widget(i, point)