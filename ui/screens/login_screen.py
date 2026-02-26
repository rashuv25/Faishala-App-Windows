# -*- coding: utf-8 -*-
"""Login screen UI."""

import customtkinter as ctk
from typing import Callable, Optional
from PIL import Image
from pathlib import Path

from config.settings import Settings
from ui.theme import AppTheme
from auth.authenticator import Authenticator
from database.remote_db import RemoteDatabase


class LoginScreen(ctk.CTkFrame):
    """Login screen widget."""
    
    def __init__(self, parent, on_login_success: Callable):
        """Initialize login screen."""
        super().__init__(parent, fg_color=AppTheme.BACKGROUND_COLOR)
        
        self.on_login_success = on_login_success
        self.authenticator = Authenticator()
        self.remote_db = RemoteDatabase()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create login screen widgets."""
        # Center container
        center_frame = ctk.CTkFrame(self, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Nepal Emblem
        self._add_emblem(center_frame)
        
        # App Title
        title_label = ctk.CTkLabel(
            center_frame,
            text=Settings.APP_NAME,
            font=AppTheme.get_font("header", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        title_label.pack(pady=(20, 5))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            center_frame,
            text="Court Judgement Document Creator",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Login Card - FIXED: Increased size and padding
        login_card = ctk.CTkFrame(
            center_frame,
            fg_color=AppTheme.CARD_COLOR,
            corner_radius=12,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR
        )
        login_card.pack(padx=20, pady=20)
        
        # Inner container for proper padding
        inner_container = ctk.CTkFrame(login_card, fg_color="transparent")
        inner_container.pack(padx=50, pady=40)
        
        # Username label
        username_label = ctk.CTkLabel(
            inner_container,
            text="प्रयोगकर्ता नाम (Username)",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        username_label.pack(anchor="w", pady=(0, 8))
        
        # Username entry
        self.username_entry = ctk.CTkEntry(
            inner_container,
            width=350,
            height=45,
            placeholder_text="Enter username",
            font=AppTheme.get_font("normal"),
            corner_radius=8
        )
        self.username_entry.pack(pady=(0, 20))
        
        # Password label
        password_label = ctk.CTkLabel(
            inner_container,
            text="पासवर्ड (Password)",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        password_label.pack(anchor="w", pady=(0, 8))
        
        # Password entry
        self.password_entry = ctk.CTkEntry(
            inner_container,
            width=350,
            height=45,
            placeholder_text="Enter password",
            show="•",
            font=AppTheme.get_font("normal"),
            corner_radius=8
        )
        self.password_entry.pack(pady=(0, 15))
        
        # Error message label
        self.error_label = ctk.CTkLabel(
            inner_container,
            text="",
            font=AppTheme.get_font("small"),
            text_color=AppTheme.ERROR_COLOR,
            wraplength=340
        )
        self.error_label.pack(pady=(0, 10))
        
        # Login Button
        login_button = ctk.CTkButton(
            inner_container,
            text="लगइन गर्नुहोस् (Login)",
            width=350,
            height=45,
            font=AppTheme.get_font("normal", bold=True),
            fg_color=AppTheme.PRIMARY_COLOR,
            hover_color=AppTheme.SECONDARY_COLOR,
            text_color=AppTheme.TEXT_LIGHT,
            corner_radius=8,
            command=self._handle_login
        )
        login_button.pack(pady=(5, 15))
        
        # Forgot Password Link
        forgot_password = ctk.CTkLabel(
            inner_container,
            text="पासवर्ड बिर्सनुभयो? (Forgot Password?)",
            font=AppTheme.get_font("small"),
            text_color=AppTheme.PRIMARY_COLOR,
            cursor="hand2"
        )
        forgot_password.pack(pady=(0, 5))
        forgot_password.bind("<Button-1>", self._on_forgot_password)
        forgot_password.bind("<Enter>", lambda e: forgot_password.configure(font=AppTheme.get_font("small", bold=False)))
        forgot_password.bind("<Leave>", lambda e: forgot_password.configure(font=AppTheme.get_font("small")))
        
        # Status indicator
        status_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        status_frame.pack(pady=20)
        
        status_color = AppTheme.SUCCESS_COLOR if self.remote_db.is_connected() else AppTheme.ERROR_COLOR
        self.status_indicator = ctk.CTkLabel(
            status_frame,
            text="●",
            font=AppTheme.get_font("small"),
            text_color=status_color
        )
        self.status_indicator.pack(side="left", padx=(0, 5))
        
        status_text = "Online" if self.remote_db.is_connected() else "Offline"
        status_label = ctk.CTkLabel(
            status_frame,
            text=status_text,
            font=AppTheme.get_font("small"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        status_label.pack(side="left")
        
        # Bind Enter key
        self.password_entry.bind("<Return>", lambda e: self._handle_login())
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        
        # Focus on username entry
        self.after(100, lambda: self.username_entry.focus())
    
    def _add_emblem(self, parent):
        """Add Nepal emblem image."""
        emblem_path = Settings.IMAGES_DIR / "nepal_emblem.png"
        
        if emblem_path.exists():
            try:
                image = Image.open(emblem_path)
                image = image.resize((100, 100), Image.LANCZOS)
                photo = ctk.CTkImage(light_image=image, size=(100, 100))
                
                emblem_label = ctk.CTkLabel(parent, image=photo, text="")
                emblem_label.pack(pady=(0, 10))
            except Exception as e:
                print(f"Error loading emblem: {e}")
                self._add_placeholder_emblem(parent)
        else:
            self._add_placeholder_emblem(parent)
    
    def _add_placeholder_emblem(self, parent):
        """Add placeholder for emblem."""
        placeholder = ctk.CTkLabel(
            parent,
            text="🏛️",
            font=("Arial", 60),
            text_color=AppTheme.PRIMARY_COLOR
        )
        placeholder.pack(pady=(0, 10))
    
    def _handle_login(self):
        """Handle login button click."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validate input
        if not username or not password:
            self.error_label.configure(text="कृपया प्रयोगकर्ता नाम र पासवर्ड प्रविष्ट गर्नुहोस्")
            return
        
        # Clear previous error
        self.error_label.configure(text="")
        
        # Attempt login
        success, message, user = self.authenticator.login(username, password)
        
        if success:
            self.on_login_success()
        else:
            self.error_label.configure(text=message)
    
    def _on_forgot_password(self, event):
        """Handle forgot password click."""
        from ui.components.popup import ForgotPasswordPopup
        
        try:
            popup = ForgotPasswordPopup(self)
        except Exception:
            # If popup class doesn't exist, show simple message
            self.error_label.configure(
                text="कृपया प्रशासकलाई सम्पर्क गर्नुहोस्। (Please contact administrator.)"
            )