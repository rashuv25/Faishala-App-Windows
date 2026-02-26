# -*- coding: utf-8 -*-
"""Main application window."""

import customtkinter as ctk
from typing import Optional

from config.settings import Settings
from .theme import AppTheme
from .screens.login_screen import LoginScreen
from .screens.main_screen import MainScreen
from auth.session_manager import SessionManager
from backup.sync_manager import SyncManager


class MuddaPhaisalaApp:
    """Main application class."""
    
    def __init__(self):
        """Initialize application."""
        # Apply theme
        AppTheme.apply_theme()
        
        # Create main window
        self.window = ctk.CTk()
        self.window.title(f"{Settings.APP_NAME} - {Settings.APP_NAME_ENGLISH}")
        self.window.geometry(f"{Settings.WINDOW_WIDTH}x{Settings.WINDOW_HEIGHT}")
        self.window.minsize(Settings.MIN_WINDOW_WIDTH, Settings.MIN_WINDOW_HEIGHT)
        
        # Center window
        self._center_window()
        
        # Initialize managers
        self.session = SessionManager()
        self.sync_manager = SyncManager()
        
        # Current screen
        self.current_screen: Optional[ctk.CTkFrame] = None
        
        # Show appropriate screen
        self._show_initial_screen()
        
        # Bind close event
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _center_window(self):
        """Center window on screen."""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def _show_initial_screen(self):
        """Show login or main screen based on session."""
        if self.session.is_logged_in():
            self.show_main_screen()
        else:
            self.show_login_screen()
    
    def show_login_screen(self):
        """Show login screen."""
        self._clear_current_screen()
        self.current_screen = LoginScreen(
            self.window,
            on_login_success=self.show_main_screen
        )
        self.current_screen.pack(fill="both", expand=True)
    
    def show_main_screen(self):
        """Show main application screen."""
        self._clear_current_screen()
        self.current_screen = MainScreen(
            self.window,
            on_logout=self.show_login_screen
        )
        self.current_screen.pack(fill="both", expand=True)
        
        # Check for backup requests (silent)
        self.sync_manager.check_and_sync()
    
    def _clear_current_screen(self):
        """Clear current screen."""
        if self.current_screen:
            self.current_screen.destroy()
            self.current_screen = None
    
    def _on_close(self):
        """Handle window close."""
        self.window.destroy()
    
    def run(self):
        """Run the application."""
        self.window.mainloop()