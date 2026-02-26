# -*- coding: utf-8 -*-
"""Dashboard screen UI."""

import customtkinter as ctk
from ui.components.scrollable_frame import ScrollableFrame
from typing import Callable, List, Dict
import math

from ui.theme import AppTheme
from ui.components.popup import CreateDocumentPopup, ConfirmPopup, DuplicateDocumentPopup, ExportDocumentPopup, RenamePopup
from core.document_manager import DocumentManager
from export.docx_generator import DocxGenerator
from export.pdf_generator import PdfGenerator
from utils.file_handler import FileHandler
from utils.helpers import group_by_date


class HoverableDocumentRow(ctk.CTkFrame):
    """Document row with hover effect and click to edit."""
    
    def __init__(
        self, 
        parent, 
        document: Dict, 
        on_edit: Callable, 
        on_rename: Callable, 
        on_duplicate: Callable,
        on_export: Callable,
        on_delete: Callable
    ):
        """Initialize hoverable document row."""
        super().__init__(
            parent,
            fg_color="transparent",
            corner_radius=8
        )
        
        self.document = document
        self.on_edit = on_edit
        self.on_rename = on_rename
        self.on_duplicate = on_duplicate
        self.on_export = on_export
        self.on_delete = on_delete
        
        self._default_color = "transparent"
        self._hover_color = "#e8f4fc"
        
        self._create_widgets()
        self._bind_hover()
    
    def _create_widgets(self):
        """Create row widgets."""
        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=10)
        
        # Left side: Document icon and name (clickable to edit)
        name_frame = ctk.CTkFrame(inner, fg_color="transparent")
        name_frame.pack(side="left", fill="x", expand=True)
        
        self.icon = ctk.CTkLabel(
            name_frame,
            text="📄",
            font=("Arial", 20),
            cursor="hand2"
        )
        self.icon.pack(side="left", padx=(0, 12))
        
        self.name_label = ctk.CTkLabel(
            name_frame,
            text=self.document.get('document_name', 'Untitled'),
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY,
            cursor="hand2"
        )
        self.name_label.pack(side="left")
        
        # Bind click to edit
        doc_id = self.document.get('id')
        self.icon.bind("<Button-1>", lambda e: self.on_edit(doc_id))
        self.name_label.bind("<Button-1>", lambda e: self.on_edit(doc_id))
        
        # Right side: Action icons
        actions_frame = ctk.CTkFrame(inner, fg_color="transparent")
        actions_frame.pack(side="right")
        
        # Rename button (pencil icon)
        rename_btn = ctk.CTkButton(
            actions_frame,
            text="✏️",
            width=35,
            height=32,
            font=("Arial", 16),
            fg_color="transparent",
            hover_color="#e3f2fd",
            text_color=AppTheme.TEXT_PRIMARY,
            corner_radius=6,
            command=lambda: self.on_rename(doc_id, self.document.get('document_name', ''))
        )
        rename_btn.pack(side="left", padx=2)
        
        # Duplicate button
        duplicate_btn = ctk.CTkButton(
            actions_frame,
            text="📋",
            width=35,
            height=32,
            font=("Arial", 16),
            fg_color="transparent",
            hover_color="#e8f5e9",
            text_color=AppTheme.TEXT_PRIMARY,
            corner_radius=6,
            command=lambda: self.on_duplicate(doc_id, self.document.get('document_name', ''))
        )
        duplicate_btn.pack(side="left", padx=2)
        
        # Export button
        export_btn = ctk.CTkButton(
            actions_frame,
            text="📤",
            width=35,
            height=32,
            font=("Arial", 16),
            fg_color="transparent",
            hover_color="#fff3e0",
            text_color=AppTheme.TEXT_PRIMARY,
            corner_radius=6,
            command=lambda: self.on_export(doc_id, self.document.get('document_name', ''))
        )
        export_btn.pack(side="left", padx=2)
        
        # Delete button
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️",
            width=35,
            height=32,
            font=("Arial", 16),
            fg_color="transparent",
            hover_color="#ffebee",
            text_color=AppTheme.ERROR_COLOR,
            corner_radius=6,
            command=lambda: self.on_delete(doc_id)
        )
        delete_btn.pack(side="left", padx=2)
    
    def _bind_hover(self):
        """Bind hover events to row."""
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        for widget in [self.icon, self.name_label]:
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event):
        """Handle mouse enter."""
        self.configure(fg_color=self._hover_color)
    
    def _on_leave(self, event):
        """Handle mouse leave."""
        x, y = self.winfo_pointerxy()
        widget_x = self.winfo_rootx()
        widget_y = self.winfo_rooty()
        widget_width = self.winfo_width()
        widget_height = self.winfo_height()
        
        if not (widget_x <= x <= widget_x + widget_width and 
                widget_y <= y <= widget_y + widget_height):
            self.configure(fg_color=self._default_color)


class DashboardScreen(ctk.CTkFrame):
    """Dashboard screen widget."""
    
    ITEMS_PER_PAGE = 10
    
    def __init__(
        self, 
        parent, 
        on_create_document: Callable[[str], None],
        on_edit_document: Callable[[int], None]
    ):
        """Initialize dashboard screen."""
        super().__init__(parent, fg_color=AppTheme.BACKGROUND_COLOR)
        
        self.on_create_document = on_create_document
        self.on_edit_document = on_edit_document
        self.doc_manager = DocumentManager()
        self.docx_generator = DocxGenerator()
        self.pdf_generator = PdfGenerator()
        
        # State
        self.all_documents = []
        self.filtered_documents = []
        self.current_page = 1
        self.total_pages = 1
        self.sort_ascending = False
        self.is_search_active = False
        
        self._create_widgets()
        self._load_documents()
    
    def _create_widgets(self):
        """Create dashboard widgets."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # ===== TOP SECTION: Create Button (Centered) =====
        top_section = ctk.CTkFrame(container, fg_color="transparent")
        top_section.pack(fill="x", pady=(0, 25))
        
        create_btn = ctk.CTkButton(
            top_section,
            text="+ नयाँ कागजात सिर्जना गर्नुहोस् (Create New Document)",
            width=400,
            height=50,
            font=AppTheme.get_font("normal", bold=True),
            fg_color=AppTheme.PRIMARY_COLOR,
            hover_color=AppTheme.SECONDARY_COLOR,
            text_color=AppTheme.TEXT_LIGHT,
            corner_radius=10,
            command=self._show_create_popup
        )
        create_btn.pack(anchor="center")
        
        # ===== SEARCH SECTION =====
        search_section = ctk.CTkFrame(container, fg_color="transparent")
        search_section.pack(fill="x", pady=(0, 15))
        
        left_search_frame = ctk.CTkFrame(search_section, fg_color="transparent")
        left_search_frame.pack(side="left")
        
        # Sort toggle button
        self.sort_btn = ctk.CTkButton(
            left_search_frame,
            text="↓",
            width=40,
            height=40,
            font=("Arial", 18, "bold"),
            fg_color=AppTheme.CARD_COLOR,
            hover_color=AppTheme.BACKGROUND_COLOR,
            text_color=AppTheme.TEXT_PRIMARY,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR,
            corner_radius=8,
            command=self._toggle_sort
        )
        self.sort_btn.pack(side="left", padx=(0, 10))
        
        # Search entry
        self.search_entry = ctk.CTkEntry(
            left_search_frame,
            width=300,
            height=40,
            placeholder_text="🔍 खोज्नुहोस्... (Search)",
            font=AppTheme.get_font("normal"),
            corner_radius=8
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        
        # Search button
        search_btn = ctk.CTkButton(
            left_search_frame,
            text="Search",
            width=80,
            height=40,
            font=AppTheme.get_font("normal"),
            fg_color=AppTheme.PRIMARY_COLOR,
            hover_color=AppTheme.SECONDARY_COLOR,
            text_color=AppTheme.TEXT_LIGHT,
            corner_radius=8,
            command=self._do_search
        )
        search_btn.pack(side="left", padx=(0, 10))
        
        # Filter section (hidden initially)
        self.filter_frame = ctk.CTkFrame(left_search_frame, fg_color="transparent")
        
        self.filter_separator = ctk.CTkLabel(
            self.filter_frame,
            text="|",
            font=AppTheme.get_font("large"),
            text_color=AppTheme.BORDER_COLOR
        )
        self.filter_separator.pack(side="left", padx=(5, 10))
        
        filter_label = ctk.CTkLabel(
            self.filter_frame,
            text="Filter:",
            font=AppTheme.get_font("small"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        filter_label.pack(side="left", padx=(0, 8))
        
        self.filter_type = ctk.StringVar(value="name")
        
        name_radio = ctk.CTkRadioButton(
            self.filter_frame,
            text="Name",
            variable=self.filter_type,
            value="name",
            font=AppTheme.get_font("small"),
            radiobutton_width=16,
            radiobutton_height=16,
            command=self._on_filter_change
        )
        name_radio.pack(side="left", padx=(0, 10))
        
        date_radio = ctk.CTkRadioButton(
            self.filter_frame,
            text="Date",
            variable=self.filter_type,
            value="date",
            font=AppTheme.get_font("small"),
            radiobutton_width=16,
            radiobutton_height=16,
            command=self._on_filter_change
        )
        date_radio.pack(side="left", padx=(0, 10))
        
        self.clear_btn = ctk.CTkButton(
            self.filter_frame,
            text="✕ Clear",
            width=60,
            height=30,
            font=AppTheme.get_font("small"),
            fg_color="transparent",
            hover_color="#ffebee",
            text_color=AppTheme.ERROR_COLOR,
            corner_radius=6,
            command=self._clear_search
        )
        self.clear_btn.pack(side="left", padx=(5, 0))
        
        self.search_entry.bind("<Return>", lambda e: self._do_search())
        
        # ===== RESULTS INFO + PAGINATION ROW =====
        self.results_row = ctk.CTkFrame(container, fg_color="transparent")
        self.results_row.pack(fill="x", pady=(5, 10))
        
        self.results_label = ctk.CTkLabel(
            self.results_row,
            text="",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        self.results_label.pack(side="left")
        
        self.top_pagination_frame = ctk.CTkFrame(self.results_row, fg_color="transparent")
        self.top_pagination_frame.pack(side="right")
        
                # ===== DOCUMENTS SECTION =====
        self.documents_container = ScrollableFrame(
            container,
            fg_color="transparent",
            scrollbar_button_color=AppTheme.BORDER_COLOR,
            scrollbar_button_hover_color=AppTheme.TEXT_SECONDARY
        )
        self.documents_container.pack(fill="both", expand=True, pady=(0, 10))
        
        # ===== BOTTOM PAGINATION =====
        self.bottom_pagination_frame = ctk.CTkFrame(container, fg_color="transparent")
        self.bottom_pagination_frame.pack(fill="x", pady=(5, 0))
    
    def _create_pagination(self, parent_frame):
        """Create pagination controls."""
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        if self.total_pages <= 1:
            return
        
        pagination = ctk.CTkFrame(parent_frame, fg_color="transparent")
        pagination.pack(side="right")
        
        page_label = ctk.CTkLabel(
            pagination,
            text="Page",
            font=AppTheme.get_font("small"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        page_label.pack(side="left", padx=(0, 8))
        
        # Previous button
        prev_state = "normal" if self.current_page > 1 else "disabled"
        prev_btn = ctk.CTkButton(
            pagination,
            text="<",
            width=32,
            height=30,
            font=AppTheme.get_font("normal", bold=True),
            fg_color=AppTheme.CARD_COLOR if self.current_page > 1 else AppTheme.BACKGROUND_COLOR,
            hover_color=AppTheme.BORDER_COLOR,
            text_color=AppTheme.TEXT_PRIMARY if self.current_page > 1 else AppTheme.TEXT_SECONDARY,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR,
            corner_radius=6,
            command=self._prev_page if self.current_page > 1 else None,
            state=prev_state
        )
        prev_btn.pack(side="left", padx=2)
        
        # Page numbers
        start_page = max(1, self.current_page - 2)
        end_page = min(self.total_pages, start_page + 4)
        
        if end_page - start_page < 4:
            start_page = max(1, end_page - 4)
        
        if start_page > 1:
            first_btn = ctk.CTkButton(
                pagination,
                text="1",
                width=32,
                height=30,
                font=AppTheme.get_font("small"),
                fg_color=AppTheme.CARD_COLOR,
                hover_color=AppTheme.BORDER_COLOR,
                text_color=AppTheme.TEXT_PRIMARY,
                border_width=1,
                border_color=AppTheme.BORDER_COLOR,
                corner_radius=6,
                command=lambda: self._go_to_page(1)
            )
            first_btn.pack(side="left", padx=2)
            
            if start_page > 2:
                dots = ctk.CTkLabel(pagination, text="...", font=AppTheme.get_font("small"), text_color=AppTheme.TEXT_SECONDARY)
                dots.pack(side="left", padx=2)
        
        for page_num in range(start_page, end_page + 1):
            is_current = page_num == self.current_page
            
            page_btn = ctk.CTkButton(
                pagination,
                text=str(page_num),
                width=32,
                height=30,
                font=AppTheme.get_font("small", bold=is_current),
                fg_color=AppTheme.PRIMARY_COLOR if is_current else AppTheme.CARD_COLOR,
                hover_color=AppTheme.SECONDARY_COLOR if is_current else AppTheme.BORDER_COLOR,
                text_color=AppTheme.TEXT_LIGHT if is_current else AppTheme.TEXT_PRIMARY,
                border_width=0 if is_current else 1,
                border_color=AppTheme.BORDER_COLOR,
                corner_radius=6,
                command=lambda p=page_num: self._go_to_page(p)
            )
            page_btn.pack(side="left", padx=2)
        
        if end_page < self.total_pages:
            if end_page < self.total_pages - 1:
                dots = ctk.CTkLabel(pagination, text="...", font=AppTheme.get_font("small"), text_color=AppTheme.TEXT_SECONDARY)
                dots.pack(side="left", padx=2)
            
            last_btn = ctk.CTkButton(
                pagination,
                text=str(self.total_pages),
                width=32,
                height=30,
                font=AppTheme.get_font("small"),
                fg_color=AppTheme.CARD_COLOR,
                hover_color=AppTheme.BORDER_COLOR,
                text_color=AppTheme.TEXT_PRIMARY,
                border_width=1,
                border_color=AppTheme.BORDER_COLOR,
                corner_radius=6,
                command=lambda: self._go_to_page(self.total_pages)
            )
            last_btn.pack(side="left", padx=2)
        
        # Next button
        next_state = "normal" if self.current_page < self.total_pages else "disabled"
        next_btn = ctk.CTkButton(
            pagination,
            text=">",
            width=32,
            height=30,
            font=AppTheme.get_font("normal", bold=True),
            fg_color=AppTheme.CARD_COLOR if self.current_page < self.total_pages else AppTheme.BACKGROUND_COLOR,
            hover_color=AppTheme.BORDER_COLOR,
            text_color=AppTheme.TEXT_PRIMARY if self.current_page < self.total_pages else AppTheme.TEXT_SECONDARY,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR,
            corner_radius=6,
            command=self._next_page if self.current_page < self.total_pages else None,
            state=next_state
        )
        next_btn.pack(side="left", padx=2)
    
    def _load_documents(self):
        """Load and display documents."""
        self.all_documents = self.doc_manager.get_all_documents()
        self.filtered_documents = self.all_documents.copy()
        self._apply_sort()
        self._update_display()
    
    def _apply_sort(self):
        """Apply current sort order."""
        if self.sort_ascending:
            self.filtered_documents.sort(key=lambda x: x.get('created_date', ''))
        else:
            self.filtered_documents.sort(key=lambda x: x.get('created_date', ''), reverse=True)
    
    def _update_display(self):
        """Update the document display."""
        total_docs = len(self.filtered_documents)
        self.total_pages = max(1, math.ceil(total_docs / self.ITEMS_PER_PAGE))
        
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages
        
        start_idx = (self.current_page - 1) * self.ITEMS_PER_PAGE
        end_idx = start_idx + self.ITEMS_PER_PAGE
        page_documents = self.filtered_documents[start_idx:end_idx]
        
        grouped = group_by_date(page_documents)
        
        if self.is_search_active:
            search_term = self.search_entry.get().strip()
            self.results_label.configure(
                text=f"Search Results for \"{search_term}\" — {total_docs} document(s) found"
            )
        else:
            self.results_label.configure(text=f"All Documents — {total_docs} document(s)")
        
        self._render_documents(grouped)
        self._create_pagination(self.top_pagination_frame)
        self._create_pagination(self.bottom_pagination_frame)
    
    def _render_documents(self, grouped_documents: Dict[str, List[Dict]]):
        """Render documents in the container."""
        for widget in self.documents_container.winfo_children():
            widget.destroy()
        
        if not grouped_documents:
            empty_frame = ctk.CTkFrame(self.documents_container, fg_color="transparent")
            empty_frame.pack(expand=True, pady=50)
            
            empty_icon = ctk.CTkLabel(empty_frame, text="📄", font=("Arial", 50))
            empty_icon.pack(pady=(0, 15))
            
            empty_label = ctk.CTkLabel(
                empty_frame,
                text="कुनै कागजात फेला परेन\n(No documents found)",
                font=AppTheme.get_font("normal"),
                text_color=AppTheme.TEXT_SECONDARY,
                justify="center"
            )
            empty_label.pack()
            return
        
        for date_key, docs in sorted(grouped_documents.items(), reverse=not self.sort_ascending):
            self._create_date_group(date_key, docs)
    
    def _create_date_group(self, date_key: str, documents: List[Dict]):
        """Create a date group with documents."""
        date_frame = ctk.CTkFrame(self.documents_container, fg_color="transparent")
        date_frame.pack(fill="x", pady=(15, 8))
        
        file_count = len(documents)
        file_text = "file" if file_count == 1 else "files"
        
        date_label = ctk.CTkLabel(
            date_frame,
            text=f"📅 {date_key}  [{file_count} {file_text}]",
            font=AppTheme.get_font("normal", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        date_label.pack(anchor="w")
        
        card = ctk.CTkFrame(
            self.documents_container,
            fg_color=AppTheme.CARD_COLOR,
            corner_radius=10,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR
        )
        card.pack(fill="x", pady=(0, 5))
        
        for doc in documents:
            row = HoverableDocumentRow(
                card,
                document=doc,
                on_edit=self.on_edit_document,
                on_rename=self._show_rename_popup,
                on_duplicate=self._show_duplicate_popup,
                on_export=self._show_export_popup,
                on_delete=self._handle_delete
            )
            row.pack(fill="x")
    
    def _toggle_sort(self):
        """Toggle sort order."""
        self.sort_ascending = not self.sort_ascending
        self.sort_btn.configure(text="↑" if self.sort_ascending else "↓")
        
        self._apply_sort()
        self.current_page = 1
        self._update_display()
    
    def _do_search(self):
        """Perform search."""
        search_term = self.search_entry.get().strip()
        
        if search_term:
            self.is_search_active = True
            
            filter_value = self.filter_type.get()
            if filter_value == "date":
                self.filtered_documents = self.doc_manager.filter_by_date(search_term)
            else:
                self.filtered_documents = self.doc_manager.search_documents(search_term)
            
            self._apply_sort()
            self.filter_frame.pack(side="left")
        else:
            self._clear_search()
            return
        
        self.current_page = 1
        self._update_display()
    
    def _clear_search(self):
        """Clear search and reset."""
        self.search_entry.delete(0, "end")
        self.is_search_active = False
        self.filtered_documents = self.all_documents.copy()
        self._apply_sort()
        
        self.filter_frame.pack_forget()
        self.filter_type.set("name")
        
        self.current_page = 1
        self._update_display()
    
    def _on_filter_change(self):
        """Handle filter type change."""
        if self.is_search_active:
            self._do_search()
    
    def _prev_page(self):
        """Go to previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            self._update_display()
    
    def _next_page(self):
        """Go to next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._update_display()
    
    def _go_to_page(self, page: int):
        """Go to specific page."""
        if 1 <= page <= self.total_pages:
            self.current_page = page
            self._update_display()
    
    def _show_create_popup(self):
        """Show create document popup."""
        popup = CreateDocumentPopup(
            self,
            on_create=self._create_document,
            validate_name=lambda name: self.doc_manager.document_name_exists(name)
        )
    
    def _create_document(self, name: str):
        """Create new document."""
        if name.strip():
            self.on_create_document(name.strip())
    
    def _show_rename_popup(self, doc_id: int, current_name: str):
        """Show rename popup."""
        popup = RenamePopup(
            self,
            current_name=current_name,
            on_rename=lambda new_name: self._handle_rename(doc_id, new_name),
            validate_name=lambda name: self.doc_manager.document_name_exists(name, doc_id)
        )
    
    def _handle_rename(self, document_id: int, new_name: str):
        """Handle rename document."""
        self.doc_manager.rename_document(document_id, new_name)
        self._load_documents()
    
    def _show_duplicate_popup(self, doc_id: int, original_name: str):
        """Show duplicate document popup."""
        popup = DuplicateDocumentPopup(
            self,
            original_name=original_name,
            on_duplicate=lambda new_name: self._handle_duplicate(doc_id, new_name),
            validate_name=lambda name: self.doc_manager.document_name_exists(name)
        )
    
    def _handle_duplicate(self, document_id: int, new_name: str):
        """Handle duplicate document."""
        original_doc = self.doc_manager.get_document(document_id)
        
        if original_doc:
            new_doc_id = self.doc_manager.create_document(new_name)
            
            data_to_copy = {
                'district': original_doc.get('district', ''),
                'cdo_name': original_doc.get('cdo_name', ''),
                'wadi_content': original_doc.get('wadi_content', ''),
                'pratiwadi_content': original_doc.get('pratiwadi_content', ''),
                'mudda': original_doc.get('mudda', ''),
                'mudda_number': original_doc.get('mudda_number', ''),
                'case_points': original_doc.get('case_points', ['']),
                'office_decision': original_doc.get('office_decision', ''),
                'tapsil_points': original_doc.get('tapsil_points', []),
                'typist_name': original_doc.get('typist_name', ''),
                'footer_cdo_name': original_doc.get('footer_cdo_name', ''),
                'document_date_year': original_doc.get('document_date_year'),
                'document_date_month': original_doc.get('document_date_month'),
                'document_date_day': original_doc.get('document_date_day'),
                'document_date_day_num': original_doc.get('document_date_day_num'),
            }
            
            self.doc_manager.save_document(new_doc_id, data_to_copy)
            self._load_documents()
    
    def _show_export_popup(self, doc_id: int, document_name: str):
        """Show export document popup."""
        popup = ExportDocumentPopup(
            self,
            document_name=document_name,
            on_export=lambda format_type: self._handle_export(doc_id, document_name, format_type)
        )
    
    def _handle_export(self, document_id: int, document_name: str, format_type: str):
        """Handle document export."""
        document_data = self.doc_manager.get_document(document_id)
        
        if not document_data:
            return
        
        file_path = FileHandler.get_save_path(document_name, format_type)
        
        if file_path:
            if format_type == "docx":
                success = self.docx_generator.generate(document_data, file_path)
            else:
                success = self.pdf_generator.generate(document_data, file_path)
            
            if success:
                print(f"Exported successfully to {file_path}")
    
    def _handle_delete(self, document_id: int):
        """Handle delete document."""
        popup = ConfirmPopup(
            self,
            title="कागजात मेटाउनुहोस्",
            message="के तपाईं यो कागजात मेटाउन निश्चित हुनुहुन्छ?\n(Are you sure you want to delete this document?)",
            on_confirm=lambda: self._do_delete(document_id),
            confirm_text="Delete",
            cancel_text="Cancel"
        )
    
    def _do_delete(self, document_id: int):
        """Perform document deletion."""
        self.doc_manager.delete_document(document_id)
        self._load_documents()