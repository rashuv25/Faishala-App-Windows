# -*- coding: utf-8 -*-
"""Sidebar navigation component."""

import customtkinter as ctk
from typing import Callable, Optional

from ui.theme import AppTheme


class SidebarButton(ctk.CTkButton):
    """Custom sidebar button with proper hover states."""
    
    def __init__(self, parent, text: str, command: Callable, **kwargs):
        """Initialize sidebar button."""
        super().__init__(
            parent,
            text=text,
            font=AppTheme.get_font("normal"),
            fg_color="transparent",
            hover_color="#e8e8e8",
            text_color=AppTheme.TEXT_PRIMARY,
            anchor="w",
            height=45,
            corner_radius=8,
            command=command,
            **kwargs
        )
        
        self._is_active = False
        self._default_fg = "transparent"
        self._active_fg = AppTheme.PRIMARY_COLOR
        self._default_text_color = AppTheme.TEXT_PRIMARY
        self._active_text_color = AppTheme.TEXT_LIGHT
        self._hover_color = "#e8e8e8"
        self._active_hover_color = AppTheme.SECONDARY_COLOR
    
    def set_active(self, active: bool):
        """Set button active state."""
        self._is_active = active
        
        if active:
            self.configure(
                fg_color=self._active_fg,
                text_color=self._active_text_color,
                hover_color=self._active_hover_color
            )
        else:
            self.configure(
                fg_color=self._default_fg,
                text_color=self._default_text_color,
                hover_color=self._hover_color
            )


class Sidebar(ctk.CTkFrame):
    """Sidebar navigation widget."""
    
    def __init__(
        self,
        parent,
        username: str,
        on_dashboard: Callable,
        on_dictionary: Callable,
        on_trash: Callable,
        on_settings: Callable,
        on_logout: Callable
    ):
        """Initialize sidebar."""
        super().__init__(
            parent,
            fg_color=AppTheme.SIDEBAR_COLOR,
            width=AppTheme.SIDEBAR_WIDTH,
            corner_radius=0,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR
        )
        self.pack_propagate(False)
        
        self.on_dashboard = on_dashboard
        self.on_dictionary = on_dictionary
        self.on_trash = on_trash
        self.on_settings = on_settings
        self.on_logout = on_logout
        self.username = username
        
        self.buttons = {}
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create sidebar widgets."""
        # Top section with navigation
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="x", pady=(20, 10), padx=10)
        
        # Navigation label
        nav_label = ctk.CTkLabel(
            nav_frame,
            text="NAVIGATION",
            font=AppTheme.get_font("small"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        nav_label.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Dashboard button
        self.buttons["dashboard"] = SidebarButton(
            nav_frame,
            text="  📊  Dashboard",
            command=lambda: self._on_nav_click("dashboard", self.on_dashboard)
        )
        self.buttons["dashboard"].pack(fill="x", pady=2)
        
        # Dictionary button
        self.buttons["dictionary"] = SidebarButton(
            nav_frame,
            text="  📚  Dictionary",
            command=lambda: self._on_nav_click("dictionary", self.on_dictionary)
        )
        self.buttons["dictionary"].pack(fill="x", pady=2)
        
        # Trash button
        self.buttons["trash"] = SidebarButton(
            nav_frame,
            text="  🗑️  Trash",
            command=lambda: self._on_nav_click("trash", self.on_trash)
        )
        self.buttons["trash"].pack(fill="x", pady=2)
        
        # Settings button
        self.buttons["settings"] = SidebarButton(
            nav_frame,
            text="  ⚙️  Settings",
            command=lambda: self._on_nav_click("settings", self.on_settings)
        )
        self.buttons["settings"].pack(fill="x", pady=2)
        
        # Spacer
        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.pack(fill="both", expand=True)
        
        # Divider line
        divider = ctk.CTkFrame(
            self,
            fg_color=AppTheme.BORDER_COLOR,
            height=1
        )
        divider.pack(fill="x", padx=15, pady=10)
        
        # Bottom section
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        # User info card
        user_card = ctk.CTkFrame(
            bottom_frame,
            fg_color=AppTheme.BACKGROUND_COLOR,
            corner_radius=8
        )
        user_card.pack(fill="x", pady=(0, 10))
        
        user_inner = ctk.CTkFrame(user_card, fg_color="transparent")
        user_inner.pack(fill="x", padx=12, pady=12)
        
        user_icon = ctk.CTkLabel(
            user_inner,
            text="👤",
            font=("Arial", 20)
        )
        user_icon.pack(side="left", padx=(0, 10))
        
        user_label = ctk.CTkLabel(
            user_inner,
            text=self.username,
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        user_label.pack(side="left")
        
        # Logout button
        logout_btn = ctk.CTkButton(
            bottom_frame,
            text="🚪  Logout",
            font=AppTheme.get_font("normal"),
            fg_color="transparent",
            hover_color="#ffebee",
            text_color=AppTheme.ERROR_COLOR,
            anchor="w",
            height=40,
            corner_radius=8,
            border_width=1,
            border_color=AppTheme.ERROR_COLOR,
            command=self._handle_logout
        )
        logout_btn.pack(fill="x")
    
    def _on_nav_click(self, button_name: str, command: Callable):
        """Handle navigation button click."""
        self.set_active(button_name)
        command()
    
    def _handle_logout(self):
        """Handle logout with confirmation."""
        from ui.components.popup import ConfirmPopup
        
        popup = ConfirmPopup(
            self,
            title="Logout",
            message="के तपाईं लगआउट गर्न चाहनुहुन्छ?",
            on_confirm=self.on_logout,
            confirm_text="Logout",
            cancel_text="Cancel"
        )
    
    def set_active(self, button_name: Optional[str]):
        """Set active navigation button."""
        for name, btn in self.buttons.items():
            btn.set_active(name == button_name)