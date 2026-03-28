# -*- coding: utf-8 -*-
"""Main application window."""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from typing import Optional

from config.settings import Settings
from auth.session_manager import SessionManager
from auth.nepali_date_validator import NepaliDateValidator
from database.local_db import LocalDatabase
from backup.sync_manager import SyncManager

from .theme import AppTheme
from .screens.login_screen import LoginScreen
from .screens.main_screen import MainScreen


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

        # Apply global Tk / ttk fonts
        self._apply_global_fonts()

        # Center window
        self._center_window()

        # Initialize managers
        self.session = SessionManager()
        self.local_db = LocalDatabase()
        self.date_validator = NepaliDateValidator()
        self.sync_manager = None

        if not Settings.OFFLINE_MODE:
            try:
                from backup.sync_manager import SyncManager
                self.sync_manager = SyncManager()
            except Exception:
                self.sync_manager = None

        # Try to restore last session (only if monthly online login is not required)
        self._restore_session_if_allowed()

        # Current screen
        self.current_screen: Optional[ctk.CTkFrame] = None

        # Show appropriate screen
        self._show_initial_screen()

        # Bind close event
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)

    def _apply_global_fonts(self):
        """Apply global fonts for native Tk and ttk widgets."""
        try:
            normal_font = AppTheme.get_tk_font("normal")
            small_font = AppTheme.get_tk_font("small")
            title_font = AppTheme.get_tk_font("title", bold=True)

            # Global Tk defaults
            self.window.option_add("*Font", normal_font)
            self.window.option_add("*Label.Font", normal_font)
            self.window.option_add("*Entry.Font", normal_font)
            self.window.option_add("*Text.Font", normal_font)
            self.window.option_add("*Listbox.Font", normal_font)
            self.window.option_add("*Menu.Font", normal_font)
            self.window.option_add("*TCombobox*Listbox.font", normal_font)

            style = ttk.Style(self.window)
            try:
                style.theme_use("clam")
            except Exception:
                pass

            style.configure(".", font=normal_font)
            style.configure("TLabel", font=normal_font)
            style.configure("TButton", font=normal_font)
            style.configure("TEntry", font=normal_font)
            style.configure("TCombobox", font=small_font, padding=6)
            style.configure("Mudda.TCombobox", font=small_font, padding=6)
            style.configure("Settings.TCombobox", font=small_font, padding=6)
            style.configure("Treeview", font=normal_font)
            style.configure("Treeview.Heading", font=title_font)

        except Exception as e:
            if Settings.DEBUG:
                print(f"[App] Global font apply error: {e}")

    def _center_window(self):
        """Center window on screen."""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def _restore_session_if_allowed(self):
        """Restore session from local DB if allowed (silent)."""
        try:
            # If online login is required (new Nepali month) and not in offline mode,
            # do not auto-restore; user must login.
            if (not Settings.OFFLINE_MODE) and self.date_validator.is_new_nepali_month():
                return

            user = self.local_db.get_last_session_user()
            if not user:
                return

            token = user.get("session_token")
            if not token:
                return

            self.session.set_session(user["id"], user["username"], token)

        except Exception as e:
            if Settings.DEBUG:
                print(f"[App] Session restore error: {e}")

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

        # Check for backup requests (silent; developer-controlled by app_settings)
        if self.sync_manager is not None:
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