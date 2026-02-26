# -*- coding: utf-8 -*-
"""Main application screen with sidebar navigation."""

import customtkinter as ctk
from typing import Callable, Optional

from ui.theme import AppTheme
from ui.components.sidebar import Sidebar
from ui.components.header import Header
from .dashboard_screen import DashboardScreen
from .dictionary_screen import DictionaryScreen
from .editor_screen import EditorScreen
from .trash_screen import TrashScreen
from .settings_screen import SettingsScreen
from auth.session_manager import SessionManager


class MainScreen(ctk.CTkFrame):
    """Main application screen."""
    
    def __init__(self, parent, on_logout: Callable):
        """Initialize main screen."""
        super().__init__(parent, fg_color=AppTheme.BACKGROUND_COLOR)
        
        self.on_logout = on_logout
        self.session = SessionManager()
        self.current_content: Optional[ctk.CTkFrame] = None
        self.current_document_id: Optional[int] = None
        self.sidebar_visible = True
        
        self._create_layout()
        self._show_dashboard()
    
    def _create_layout(self):
        """Create main layout with header and sidebar."""
        # Header
        self.header = Header(self)
        self.header.pack(fill="x", side="top")
        
        # Container for sidebar and content
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        # Sidebar
        self.sidebar = Sidebar(
            self.main_container,
            username=self.session.username or "User",
            on_dashboard=self._show_dashboard,
            on_dictionary=self._show_dictionary,
            on_trash=self._show_trash,
            on_settings=self._show_settings,
            on_logout=self._handle_logout
        )
        self.sidebar.pack(fill="y", side="left")
        
        # Content area
        self.content_area = ctk.CTkFrame(
            self.main_container,
            fg_color=AppTheme.BACKGROUND_COLOR
        )
        self.content_area.pack(fill="both", expand=True, side="left")
    
    def _show_sidebar(self):
        """Show the sidebar."""
        if not self.sidebar_visible:
            self.sidebar.pack(fill="y", side="left", before=self.content_area)
            self.sidebar_visible = True
    
    def _hide_sidebar(self):
        """Hide the sidebar."""
        if self.sidebar_visible:
            self.sidebar.pack_forget()
            self.sidebar_visible = False
    
    def _show_dashboard(self):
        """Show dashboard screen."""
        self._clear_content()
        self._show_sidebar()
        self.sidebar.set_active("dashboard")
        
        self.current_content = DashboardScreen(
            self.content_area,
            on_create_document=self._create_new_document,
            on_edit_document=self._edit_document
        )
        self.current_content.pack(fill="both", expand=True)
    
    def _show_dictionary(self):
        """Show dictionary screen."""
        self._clear_content()
        self._show_sidebar()
        self.sidebar.set_active("dictionary")
        
        self.current_content = DictionaryScreen(self.content_area)
        self.current_content.pack(fill="both", expand=True)
    
    def _show_trash(self):
        """Show trash screen."""
        self._clear_content()
        self._show_sidebar()
        self.sidebar.set_active("trash")
        
        self.current_content = TrashScreen(self.content_area)
        self.current_content.pack(fill="both", expand=True)
    
    def _show_settings(self):
        """Show settings screen."""
        self._clear_content()
        self._show_sidebar()
        self.sidebar.set_active("settings")
        
        self.current_content = SettingsScreen(self.content_area)
        self.current_content.pack(fill="both", expand=True)
    
    def _show_editor(self, document_id: int):
        """Show document editor screen."""
        self._clear_content()
        self._hide_sidebar()  # Hide sidebar when editing
        self.current_document_id = document_id
        
        self.current_content = EditorScreen(
            self.content_area,
            document_id=document_id,
            on_back=self._show_dashboard
        )
        self.current_content.pack(fill="both", expand=True)
    
    def _create_new_document(self, document_name: str):
        """Create new document and open editor."""
        from core.document_manager import DocumentManager
        
        doc_manager = DocumentManager()
        document_id = doc_manager.create_document(document_name)
        self._show_editor(document_id)
    
    def _edit_document(self, document_id: int):
        """Open document for editing."""
        self._show_editor(document_id)
    
    def _handle_logout(self):
        """Handle logout."""
        from auth.authenticator import Authenticator
        
        authenticator = Authenticator()
        authenticator.logout()
        self.on_logout()
    
    def _clear_content(self):
        """Clear content area."""
        if self.current_content:
            self.current_content.destroy()
            self.current_content = None