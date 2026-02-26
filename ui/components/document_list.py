# # -*- coding: utf-8 -*-
# """Document list component."""

# import customtkinter as ctk
# from typing import Callable, Dict, List

# from ui.theme import AppTheme


# class DocumentList(ctk.CTkScrollableFrame):
#     """Document list widget."""
    
#     def __init__(
#         self,
#         parent,
#         on_edit: Callable[[int], None],
#         on_rename: Callable[[int, str], None],
#         on_delete: Callable[[int], None]
#     ):
#         """Initialize document list."""
#         super().__init__(parent, fg_color="transparent")
        
#         self.on_edit = on_edit
#         self.on_rename = on_rename
#         self.on_delete = on_delete
        
#         self.documents: Dict[str, List[Dict]] = {}
    
#     def set_documents(self, grouped_documents: Dict[str, List[Dict]]):
#         """Set and display documents grouped by date."""
#         self.documents = grouped_documents
#         self._refresh_display()
    
#     def _refresh_display(self):
#         """Refresh document display."""
#         # Clear existing widgets
#         for widget in self.winfo_children():
#             widget.destroy()
        
#         if not self.documents:
#             # Empty state
#             empty_label = ctk.CTkLabel(
#                 self,
#                 text="कुनै कागजात फेला परेन (No documents found)",
#                 font=AppTheme.get_font("normal"),
#                 text_color=AppTheme.TEXT_SECONDARY
#             )
#             empty_label.pack(pady=50)
#             return
        
#         # Display documents grouped by date
#         for date_key, docs in sorted(self.documents.items(), reverse=True):
#             self._create_date_group(date_key, docs)
    
#     def _create_date_group(self, date_key: str, documents: List[Dict]):
#         """Create a date group with documents."""
#         # Date header
#         date_frame = ctk.CTkFrame(self, fg_color="transparent")
#         date_frame.pack(fill="x", pady=(20, 10))
        
#         date_label = ctk.CTkLabel(
#             date_frame,
#             text=f"📅 {date_key}",
#             font=AppTheme.get_font("normal", bold=True),
#             text_color=AppTheme.TEXT_PRIMARY
#         )
#         date_label.pack(anchor="w")
        
#         # Documents card
#         card = ctk.CTkFrame(
#             self,
#             fg_color=AppTheme.CARD_COLOR,
#             corner_radius=AppTheme.BORDER_RADIUS
#         )
#         card.pack(fill="x", pady=(0, 10))
        
#         for doc in documents:
#             self._create_document_row(card, doc)
    
#     def _create_document_row(self, parent, document: Dict):
#         """Create a document row."""
#         row = ctk.CTkFrame(parent, fg_color="transparent")
#         row.pack(fill="x", padx=15, pady=8)
        
#         # Document icon and name
#         name_frame = ctk.CTkFrame(row, fg_color="transparent")
#         name_frame.pack(side="left", fill="x", expand=True)
        
#         icon = ctk.CTkLabel(
#             name_frame,
#             text="📄",
#             font=AppTheme.get_font("normal")
#         )
#         icon.pack(side="left", padx=(0, 10))
        
#         name = ctk.CTkLabel(
#             name_frame,
#             text=document.get('document_name', 'Untitled'),
#             font=AppTheme.get_font("normal"),
#             text_color=AppTheme.TEXT_PRIMARY
#         )
#         name.pack(side="left")
        
#         # Action buttons
#         actions_frame = ctk.CTkFrame(row, fg_color="transparent")
#         actions_frame.pack(side="right")
        
#         doc_id = document.get('id')
        
#         # Edit button
#         edit_btn = ctk.CTkButton(
#             actions_frame,
#             text="Edit",
#             width=60,
#             height=30,
#             font=AppTheme.get_font("small"),
#             command=lambda: self.on_edit(doc_id),
#             **AppTheme.get_button_style("secondary")
#         )
#         edit_btn.pack(side="left", padx=2)
        
#         # Rename button
#         rename_btn = ctk.CTkButton(
#             actions_frame,
#             text="Rename",
#             width=70,
#             height=30,
#             font=AppTheme.get_font("small"),
#             command=lambda: self._show_rename_popup(doc_id, document.get('document_name', '')),
#             **AppTheme.get_button_style("secondary")
#         )
#         rename_btn.pack(side="left", padx=2)
        
#         # Delete button
#         delete_btn = ctk.CTkButton(
#             actions_frame,
#             text="🗑️",
#             width=30,
#             height=30,
#             fg_color="transparent",
#             hover_color=AppTheme.BACKGROUND_COLOR,
#             text_color=AppTheme.ERROR_COLOR,
#             command=lambda: self.on_delete(doc_id)
#         )
#         delete_btn.pack(side="left", padx=2)
    
#     def _show_rename_popup(self, doc_id: int, current_name: str):
#         """Show rename popup."""
#         from ui.components.popup import RenamePopup
        
#         popup = RenamePopup(
#             self,
#             current_name=current_name,
#             on_rename=lambda new_name: self.on_rename(doc_id, new_name)
#         )




# -*- coding: utf-8 -*-
"""Document list component."""

import customtkinter as ctk
from typing import Callable, Dict, List

from ui.theme import AppTheme


class DocumentList(ctk.CTkScrollableFrame):
    """Document list widget."""
    
    def __init__(
        self,
        parent,
        on_edit: Callable[[int], None],
        on_rename: Callable[[int, str], None],
        on_delete: Callable[[int], None]
    ):
        """Initialize document list."""
        super().__init__(parent, fg_color="transparent")
        
        self.on_edit = on_edit
        self.on_rename = on_rename
        self.on_delete = on_delete
        
        self.documents: Dict[str, List[Dict]] = {}
    
    def set_documents(self, grouped_documents: Dict[str, List[Dict]]):
        """Set and display documents grouped by date."""
        self.documents = grouped_documents
        self._refresh_display()
    
    def _refresh_display(self):
        """Refresh document display."""
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        if not self.documents:
            # Empty state
            empty_label = ctk.CTkLabel(
                self,
                text="कुनै कागजात फेला परेन (No documents found)",
                font=AppTheme.get_font("normal"),
                text_color=AppTheme.TEXT_SECONDARY
            )
            empty_label.pack(pady=50)
            return
        
        # Display documents grouped by date
        for date_key, docs in sorted(self.documents.items(), reverse=True):
            self._create_date_group(date_key, docs)
    
    def _create_date_group(self, date_key: str, documents: List[Dict]):
        """Create a date group with documents."""
        # Date header
        date_frame = ctk.CTkFrame(self, fg_color="transparent")
        date_frame.pack(fill="x", pady=(20, 10))
        
        date_label = ctk.CTkLabel(
            date_frame,
            text=f"📅 {date_key}",
            font=AppTheme.get_font("normal", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        date_label.pack(anchor="w")
        
        # Documents card
        card = ctk.CTkFrame(
            self,
            fg_color=AppTheme.CARD_COLOR,
            corner_radius=AppTheme.BORDER_RADIUS
        )
        card.pack(fill="x", pady=(0, 10))
        
        for doc in documents:
            self._create_document_row(card, doc)
    
    def _create_document_row(self, parent, document: Dict):
        """Create a document row."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=8)
        
        # Document icon and name
        name_frame = ctk.CTkFrame(row, fg_color="transparent")
        name_frame.pack(side="left", fill="x", expand=True)
        
        icon = ctk.CTkLabel(
            name_frame,
            text="📄",
            font=AppTheme.get_font("normal")
        )
        icon.pack(side="left", padx=(0, 10))
        
        name = ctk.CTkLabel(
            name_frame,
            text=document.get('document_name', 'Untitled'),
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        name.pack(side="left")
        
        # Action buttons
        actions_frame = ctk.CTkFrame(row, fg_color="transparent")
        actions_frame.pack(side="right")
        
        doc_id = document.get('id')
        
        # Edit button
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="Edit",
            width=60,
            height=30,
            font=AppTheme.get_font("small"),
            fg_color=AppTheme.CARD_COLOR,
            hover_color=AppTheme.BACKGROUND_COLOR,
            text_color=AppTheme.TEXT_PRIMARY,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR,
            corner_radius=AppTheme.BORDER_RADIUS,
            command=lambda: self.on_edit(doc_id)
        )
        edit_btn.pack(side="left", padx=2)
        
        # Rename button
        rename_btn = ctk.CTkButton(
            actions_frame,
            text="Rename",
            width=70,
            height=30,
            font=AppTheme.get_font("small"),
            fg_color=AppTheme.CARD_COLOR,
            hover_color=AppTheme.BACKGROUND_COLOR,
            text_color=AppTheme.TEXT_PRIMARY,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR,
            corner_radius=AppTheme.BORDER_RADIUS,
            command=lambda: self._show_rename_popup(doc_id, document.get('document_name', ''))
        )
        rename_btn.pack(side="left", padx=2)
        
        # Delete button
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=AppTheme.BACKGROUND_COLOR,
            text_color=AppTheme.ERROR_COLOR,
            command=lambda: self.on_delete(doc_id)
        )
        delete_btn.pack(side="left", padx=2)
    
    def _show_rename_popup(self, doc_id: int, current_name: str):
        """Show rename popup."""
        from ui.components.popup import RenamePopup
        
        popup = RenamePopup(
            self,
            current_name=current_name,
            on_rename=lambda new_name: self.on_rename(doc_id, new_name)
        )