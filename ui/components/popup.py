# -*- coding: utf-8 -*-
"""Popup dialog components."""

import customtkinter as ctk
from typing import Callable, Optional

from ui.theme import AppTheme


class BasePopup(ctk.CTkToplevel):
    """Base popup dialog."""
    
    def __init__(self, parent, title: str, width: int = 400, height: int = 200):
        """Initialize popup."""
        super().__init__(parent)
        
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        
        self.configure(fg_color=AppTheme.CARD_COLOR)
        self.transient(parent)
        
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        self.after(100, self._make_modal)
    
    def _make_modal(self):
        """Make the window modal after it's visible."""
        try:
            self.grab_set()
            self.focus_force()
        except Exception:
            self.after(100, self._try_grab_again)
    
    def _try_grab_again(self):
        """Try to grab focus again."""
        try:
            self.grab_set()
            self.focus_force()
        except Exception:
            pass


class ConfirmPopup(BasePopup):
    """Confirmation popup dialog."""
    
    def __init__(
        self,
        parent,
        title: str,
        message: str,
        on_confirm: Callable,
        confirm_text: str = "Confirm",
        cancel_text: str = "Cancel"
    ):
        """Initialize confirm popup."""
        super().__init__(parent, title, 420, 200)
        
        self.on_confirm = on_confirm
        self._create_widgets(message, confirm_text, cancel_text)
    
    def _create_widgets(self, message: str, confirm_text: str, cancel_text: str):
        """Create popup widgets."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=20)
        
        msg_label = ctk.CTkLabel(
            container,
            text=message,
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY,
            wraplength=360,
            justify="center"
        )
        msg_label.pack(pady=(20, 30))
        
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack()
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text=cancel_text,
            width=100,
            height=36,
            font=AppTheme.get_font("normal"),
            fg_color=AppTheme.BACKGROUND_COLOR,
            hover_color=AppTheme.BORDER_COLOR,
            text_color=AppTheme.TEXT_PRIMARY,
            corner_radius=8,
            command=self.destroy
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        confirm_btn = ctk.CTkButton(
            btn_frame,
            text=confirm_text,
            width=100,
            height=36,
            font=AppTheme.get_font("normal"),
            fg_color=AppTheme.ERROR_COLOR,
            hover_color="#d33426",
            text_color=AppTheme.TEXT_LIGHT,
            corner_radius=8,
            command=self._do_confirm
        )
        confirm_btn.pack(side="left")
    
    def _do_confirm(self):
        """Handle confirm."""
        self.destroy()
        self.on_confirm()


class CreateDocumentPopup(BasePopup):
    """Create document popup dialog."""
    
    def __init__(self, parent, on_create: Callable[[str], None], validate_name: Callable[[str], bool] = None):
        """Initialize create document popup."""
        super().__init__(parent, "नयाँ कागजात (New Document)", 480, 240)
        
        self.on_create = on_create
        self.validate_name = validate_name
        self._create_widgets()
    
    def _create_widgets(self):
        """Create popup widgets."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=25)
        
        label = ctk.CTkLabel(
            container,
            text="कागजातको नाम प्रविष्ट गर्नुहोस्:",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        label.pack(anchor="w", pady=(5, 10))
        
        self.entry = ctk.CTkEntry(
            container,
            width=400,
            height=42,
            placeholder_text="Document name...",
            font=AppTheme.get_font("normal"),
            corner_radius=8
        )
        self.entry.pack(pady=(0, 8))
        
        # Error label
        self.error_label = ctk.CTkLabel(
            container,
            text="",
            font=AppTheme.get_font("small"),
            text_color=AppTheme.ERROR_COLOR
        )
        self.error_label.pack(pady=(0, 10))
        
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack()
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=100,
            height=38,
            font=AppTheme.get_font("normal"),
            fg_color=AppTheme.BACKGROUND_COLOR,
            hover_color=AppTheme.BORDER_COLOR,
            text_color=AppTheme.TEXT_PRIMARY,
            corner_radius=8,
            command=self.destroy
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        create_btn = ctk.CTkButton(
            btn_frame,
            text="Create",
            width=100,
            height=38,
            font=AppTheme.get_font("normal"),
            fg_color=AppTheme.PRIMARY_COLOR,
            hover_color=AppTheme.SECONDARY_COLOR,
            text_color=AppTheme.TEXT_LIGHT,
            corner_radius=8,
            command=self._do_create
        )
        create_btn.pack(side="left")
        
        self.entry.bind("<Return>", lambda e: self._do_create())
        self.after(150, lambda: self.entry.focus())
    
    def _do_create(self):
        """Handle create."""
        name = self.entry.get().strip()
        
        if not name:
            self.error_label.configure(text="कृपया नाम प्रविष्ट गर्नुहोस् (Please enter a name)")
            return
        
        if self.validate_name and self.validate_name(name):
            self.error_label.configure(text="यो नाम पहिले नै छ (This name already exists)")
            return
        
        self.destroy()
        self.on_create(name)


class RenamePopup(BasePopup):
    """Rename document popup dialog."""
    
    def __init__(self, parent, current_name: str, on_rename: Callable[[str], None], validate_name: Callable[[str], bool] = None):
        """Initialize rename popup."""
        super().__init__(parent, "नाम परिवर्तन (Rename)", 480, 240)
        
        self.on_rename = on_rename
        self.validate_name = validate_name
        self.current_name = current_name
        self._create_widgets()
    
    def _create_widgets(self):
        """Create popup widgets."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=25)
        
        label = ctk.CTkLabel(
            container,
            text="नयाँ नाम प्रविष्ट गर्नुहोस्:",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        label.pack(anchor="w", pady=(5, 10))
        
        self.entry = ctk.CTkEntry(
            container,
            width=400,
            height=42,
            font=AppTheme.get_font("normal"),
            corner_radius=8
        )
        self.entry.pack(pady=(0, 8))
        self.entry.insert(0, self.current_name)
        
        # Error label
        self.error_label = ctk.CTkLabel(
            container,
            text="",
            font=AppTheme.get_font("small"),
            text_color=AppTheme.ERROR_COLOR
        )
        self.error_label.pack(pady=(0, 10))
        
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack()
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=100,
            height=38,
            font=AppTheme.get_font("normal"),
            fg_color=AppTheme.BACKGROUND_COLOR,
            hover_color=AppTheme.BORDER_COLOR,
            text_color=AppTheme.TEXT_PRIMARY,
            corner_radius=8,
            command=self.destroy
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        rename_btn = ctk.CTkButton(
            btn_frame,
            text="Rename",
            width=100,
            height=38,
            font=AppTheme.get_font("normal"),
            fg_color=AppTheme.PRIMARY_COLOR,
            hover_color=AppTheme.SECONDARY_COLOR,
            text_color=AppTheme.TEXT_LIGHT,
            corner_radius=8,
            command=self._do_rename
        )
        rename_btn.pack(side="left")
        
        self.entry.bind("<Return>", lambda e: self._do_rename())
        self.after(150, self._focus_entry)
    
    def _focus_entry(self):
        """Focus entry and select text."""
        self.entry.focus()
        self.entry.select_range(0, "end")
    
    def _do_rename(self):
        """Handle rename."""
        name = self.entry.get().strip()
        
        if not name:
            self.error_label.configure(text="कृपया नाम प्रविष्ट गर्नुहोस् (Please enter a name)")
            return
        
        if name == self.current_name:
            self.destroy()
            return
        
        if self.validate_name and self.validate_name(name):
            self.error_label.configure(text="यो नाम पहिले नै छ (This name already exists)")
            return
        
        self.destroy()
        self.on_rename(name)


class ForgotPasswordPopup(BasePopup):
    """Forgot password popup dialog."""
    
    def __init__(self, parent):
        """Initialize forgot password popup."""
        super().__init__(parent, "पासवर्ड बिर्सनुभयो (Forgot Password)", 450, 220)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create popup widgets."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=20)
        
        icon_label = ctk.CTkLabel(
            container,
            text="🔐",
            font=("Arial", 40)
        )
        icon_label.pack(pady=(10, 15))
        
        msg_label = ctk.CTkLabel(
            container,
            text="कृपया आफ्नो प्रशासकलाई सम्पर्क गर्नुहोस्।\n(Please contact your administrator.)",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY,
            justify="center"
        )
        msg_label.pack(pady=(0, 20))
        
        ok_btn = ctk.CTkButton(
            container,
            text="OK",
            width=100,
            height=36,
            font=AppTheme.get_font("normal"),
            fg_color=AppTheme.PRIMARY_COLOR,
            hover_color=AppTheme.SECONDARY_COLOR,
            text_color=AppTheme.TEXT_LIGHT,
            corner_radius=8,
            command=self.destroy
        )
        ok_btn.pack()


class DuplicateDocumentPopup(BasePopup):
    """Duplicate document popup dialog."""
    
    def __init__(self, parent, original_name: str, on_duplicate: Callable[[str], None], validate_name: Callable[[str], bool] = None):
        """Initialize duplicate document popup."""
        super().__init__(parent, "कागजात नक्कल गर्नुहोस् (Duplicate Document)", 480, 260)
        
        self.on_duplicate = on_duplicate
        self.validate_name = validate_name
        self.original_name = original_name
        self._create_widgets()
    
    def _create_widgets(self):
        """Create popup widgets."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=20)
        
        title_frame = ctk.CTkFrame(container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(5, 15))
        
        icon_label = ctk.CTkLabel(
            title_frame,
            text="📋",
            font=("Arial", 28)
        )
        icon_label.pack(side="left", padx=(0, 12))
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="नयाँ कागजातको नाम प्रविष्ट गर्नुहोस्:",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        title_label.pack(side="left")
        
        self.entry = ctk.CTkEntry(
            container,
            width=400,
            height=42,
            font=AppTheme.get_font("normal"),
            corner_radius=8
        )
        self.entry.pack(pady=(0, 8))
        
        default_name = self._generate_duplicate_name()
        self.entry.insert(0, default_name)
        
        # Error label
        self.error_label = ctk.CTkLabel(
            container,
            text="",
            font=AppTheme.get_font("small"),
            text_color=AppTheme.ERROR_COLOR
        )
        self.error_label.pack(pady=(0, 15))
        
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack()
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=100,
            height=38,
            font=AppTheme.get_font("normal"),
            fg_color=AppTheme.BACKGROUND_COLOR,
            hover_color=AppTheme.BORDER_COLOR,
            text_color=AppTheme.TEXT_PRIMARY,
            corner_radius=8,
            command=self.destroy
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        create_btn = ctk.CTkButton(
            btn_frame,
            text="Create",
            width=100,
            height=38,
            font=AppTheme.get_font("normal"),
            fg_color=AppTheme.PRIMARY_COLOR,
            hover_color=AppTheme.SECONDARY_COLOR,
            text_color=AppTheme.TEXT_LIGHT,
            corner_radius=8,
            command=self._do_duplicate
        )
        create_btn.pack(side="left")
        
        self.entry.bind("<Return>", lambda e: self._do_duplicate())
        self.after(150, self._focus_entry)
    
    def _generate_duplicate_name(self) -> str:
        """Generate a default name for the duplicate."""
        import re
        base_name = self.original_name
        
        match = re.match(r'^(.+?)(\d+)$', base_name)
        
        if match:
            name_part = match.group(1)
            num_part = int(match.group(2))
            return f"{name_part}{num_part + 1}"
        else:
            return f"{base_name}1"
    
    def _focus_entry(self):
        """Focus entry and select text."""
        self.entry.focus()
        self.entry.select_range(0, "end")
    
    def _do_duplicate(self):
        """Handle duplicate."""
        name = self.entry.get().strip()
        
        if not name:
            self.error_label.configure(text="कृपया नाम प्रविष्ट गर्नुहोस् (Please enter a name)")
            return
        
        if self.validate_name and self.validate_name(name):
            self.error_label.configure(text="यो नाम पहिले नै छ (This name already exists)")
            return
        
        self.destroy()
        self.on_duplicate(name)


class ExportDocumentPopup(BasePopup):
    """Export document popup dialog."""
    
    def __init__(self, parent, document_name: str, on_export: Callable[[str], None]):
        """Initialize export document popup."""
        super().__init__(parent, "कागजात निर्यात गर्नुहोस् (Export Document)", 420, 320)
        
        self.on_export = on_export
        self.document_name = document_name
        self.export_format = ctk.StringVar(value="docx")
        self._create_widgets()
    
    def _create_widgets(self):
        """Create popup widgets."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=25)
        
        # Icon
        icon_label = ctk.CTkLabel(
            container,
            text="📤",
            font=("Arial", 40)
        )
        icon_label.pack(pady=(5, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            container,
            text=f"Export: {self.document_name}",
            font=AppTheme.get_font("normal", bold=True),
            text_color=AppTheme.TEXT_PRIMARY,
            wraplength=350
        )
        title_label.pack(pady=(0, 20))
        
        # Format selection
        format_label = ctk.CTkLabel(
            container,
            text="Format छान्नुहोस् (Choose format):",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        format_label.pack(anchor="w", pady=(0, 12))
        
        # Radio buttons
        radio_frame = ctk.CTkFrame(container, fg_color="transparent")
        radio_frame.pack(fill="x", pady=(0, 25))
        
        docx_radio = ctk.CTkRadioButton(
            radio_frame,
            text="📄 DOCX (Word Document)",
            variable=self.export_format,
            value="docx",
            font=AppTheme.get_font("normal"),
            radiobutton_width=20,
            radiobutton_height=20
        )
        docx_radio.pack(anchor="w", pady=6)
        
        pdf_radio = ctk.CTkRadioButton(
            radio_frame,
            text="📑 PDF (PDF Document)",
            variable=self.export_format,
            value="pdf",
            font=AppTheme.get_font("normal"),
            radiobutton_width=20,
            radiobutton_height=20
        )
        pdf_radio.pack(anchor="w", pady=6)
        
        # Buttons
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack()
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=100,
            height=38,
            font=AppTheme.get_font("normal"),
            fg_color=AppTheme.BACKGROUND_COLOR,
            hover_color=AppTheme.BORDER_COLOR,
            text_color=AppTheme.TEXT_PRIMARY,
            corner_radius=8,
            command=self.destroy
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        export_btn = ctk.CTkButton(
            btn_frame,
            text="Export",
            width=100,
            height=38,
            font=AppTheme.get_font("normal"),
            fg_color=AppTheme.SUCCESS_COLOR,
            hover_color="#2d9348",
            text_color=AppTheme.TEXT_LIGHT,
            corner_radius=8,
            command=self._do_export
        )
        export_btn.pack(side="left")
    
    def _do_export(self):
        """Handle export."""
        format_type = self.export_format.get()
        self.destroy()
        self.on_export(format_type)