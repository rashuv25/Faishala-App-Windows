# -*- coding: utf-8 -*-
"""Trash screen UI."""

import customtkinter as ctk
from ui.components.scrollable_frame import ScrollableFrame
from typing import Callable, List, Dict
from datetime import datetime

from ui.theme import AppTheme
from ui.components.popup import ConfirmPopup
from core.document_manager import DocumentManager


class TrashScreen(ctk.CTkFrame):
    """Trash screen widget."""
    
    def __init__(self, parent):
        """Initialize trash screen."""
        super().__init__(parent, fg_color=AppTheme.BACKGROUND_COLOR)
        
        self.doc_manager = DocumentManager()
        self._create_widgets()
        self._load_documents()
    
    def _create_widgets(self):
        """Create trash widgets."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Title
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left")
        
        icon_label = ctk.CTkLabel(
            title_frame,
            text="🗑️",
            font=("Arial", 32)
        )
        icon_label.pack(side="left", padx=(0, 12))
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="Trash",
            font=AppTheme.get_font("title", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        title_label.pack(side="left")
        
        # Info text
        info_label = ctk.CTkLabel(
            title_frame,
            text="  (Items are automatically deleted after 30 days)",
            font=AppTheme.get_font("small"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        info_label.pack(side="left", padx=(10, 0))
        
        # Empty Trash button
        self.empty_btn = ctk.CTkButton(
            header_frame,
            text="🗑️ Empty Trash",
            width=130,
            height=38,
            font=AppTheme.get_font("normal"),
            fg_color=AppTheme.ERROR_COLOR,
            hover_color="#d33426",
            text_color=AppTheme.TEXT_LIGHT,
            corner_radius=8,
            command=self._confirm_empty_trash
        )
        self.empty_btn.pack(side="right")
        
        # Count label
        self.count_label = ctk.CTkLabel(
            container,
            text="",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        self.count_label.pack(anchor="w", pady=(0, 10))
        
                # Documents container
        self.documents_container = ScrollableFrame(
            container,
            fg_color="transparent",
            scrollbar_button_color=AppTheme.BORDER_COLOR,
            scrollbar_button_hover_color=AppTheme.TEXT_SECONDARY
        )
        self.documents_container.pack(fill="both", expand=True)
    
    def _load_documents(self):
        """Load and display trash documents."""
        documents = self.doc_manager.get_trash_documents()
        self._render_documents(documents)
        
        # Update count
        count = len(documents)
        self.count_label.configure(text=f"{count} item(s) in trash")
        
        # Enable/disable empty button
        if count > 0:
            self.empty_btn.configure(state="normal")
        else:
            self.empty_btn.configure(state="disabled")
    
    def _render_documents(self, documents: List[Dict]):
        """Render documents."""
        # Clear existing
        for widget in self.documents_container.winfo_children():
            widget.destroy()
        
        if not documents:
            empty_frame = ctk.CTkFrame(self.documents_container, fg_color="transparent")
            empty_frame.pack(expand=True, pady=50)
            
            empty_icon = ctk.CTkLabel(empty_frame, text="🗑️", font=("Arial", 50))
            empty_icon.pack(pady=(0, 15))
            
            empty_label = ctk.CTkLabel(
                empty_frame,
                text="Trash is empty",
                font=AppTheme.get_font("normal"),
                text_color=AppTheme.TEXT_SECONDARY,
                justify="center"
            )
            empty_label.pack()
            return
        
        # Card for all items
        card = ctk.CTkFrame(
            self.documents_container,
            fg_color=AppTheme.CARD_COLOR,
            corner_radius=10,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR
        )
        card.pack(fill="x", pady=(10, 0))
        
        for doc in documents:
            self._create_document_row(card, doc)
    
    def _create_document_row(self, parent, document: Dict):
        """Create a document row."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=10)
        
        # Left side: Document info
        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        icon = ctk.CTkLabel(
            info_frame,
            text="📄",
            font=("Arial", 20)
        )
        icon.pack(side="left", padx=(0, 12))
        
        # Name and delete date
        text_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        text_frame.pack(side="left")
        
        name_label = ctk.CTkLabel(
            text_frame,
            text=document.get('document_name', 'Untitled'),
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        name_label.pack(anchor="w")
        
        # Calculate days remaining
        deleted_date = document.get('deleted_date', '')
        days_text = self._get_days_remaining(deleted_date)
        
        date_label = ctk.CTkLabel(
            text_frame,
            text=days_text,
            font=AppTheme.get_font("small"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        date_label.pack(anchor="w")
        
        # Right side: Action buttons
        actions_frame = ctk.CTkFrame(row, fg_color="transparent")
        actions_frame.pack(side="right")
        
        doc_id = document.get('id')
        
        # Restore button
        restore_btn = ctk.CTkButton(
            actions_frame,
            text="↩️ Restore",
            width=90,
            height=32,
            font=AppTheme.get_font("small"),
            fg_color=AppTheme.SUCCESS_COLOR,
            hover_color="#2d9348",
            text_color=AppTheme.TEXT_LIGHT,
            corner_radius=6,
            command=lambda: self._restore_document(doc_id)
        )
        restore_btn.pack(side="left", padx=5)
        
        # Delete permanently button
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️ Delete",
            width=90,
            height=32,
            font=AppTheme.get_font("small"),
            fg_color=AppTheme.ERROR_COLOR,
            hover_color="#d33426",
            text_color=AppTheme.TEXT_LIGHT,
            corner_radius=6,
            command=lambda: self._confirm_delete(doc_id, document.get('document_name', ''))
        )
        delete_btn.pack(side="left", padx=5)
    
    def _get_days_remaining(self, deleted_date: str) -> str:
        """Calculate days remaining before auto-delete."""
        try:
            deleted = datetime.fromisoformat(deleted_date)
            days_passed = (datetime.now() - deleted).days
            days_remaining = 30 - days_passed
            
            if days_remaining <= 0:
                return "Will be deleted soon"
            elif days_remaining == 1:
                return "1 day remaining"
            else:
                return f"{days_remaining} days remaining"
        except Exception:
            return "30 days remaining"
    
    def _restore_document(self, doc_id: int):
        """Restore document from trash."""
        self.doc_manager.restore_document(doc_id)
        self._load_documents()
    
    def _confirm_delete(self, doc_id: int, doc_name: str):
        """Confirm permanent deletion."""
        popup = ConfirmPopup(
            self,
            title="Permanently Delete",
            message=f"Are you sure you want to permanently delete '{doc_name}'?\n\nThis action cannot be undone.",
            on_confirm=lambda: self._permanent_delete(doc_id),
            confirm_text="Delete",
            cancel_text="Cancel"
        )
    
    def _permanent_delete(self, doc_id: int):
        """Permanently delete document."""
        self.doc_manager.permanent_delete_document(doc_id)
        self._load_documents()
    
    def _confirm_empty_trash(self):
        """Confirm emptying trash."""
        popup = ConfirmPopup(
            self,
            title="Empty Trash",
            message="Are you sure you want to permanently delete all items in trash?\n\nThis action cannot be undone.",
            on_confirm=self._empty_trash,
            confirm_text="Empty Trash",
            cancel_text="Cancel"
        )
    
    def _empty_trash(self):
        """Empty trash."""
        self.doc_manager.empty_trash()
        self._load_documents()