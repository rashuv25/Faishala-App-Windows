# -*- coding: utf-8 -*-
"""Custom scrollable frame with proper mouse wheel support."""

import customtkinter as ctk
import platform


class ScrollableFrame(ctk.CTkScrollableFrame):
    """Scrollable frame with fixed mouse wheel scrolling for Linux."""
    
    def __init__(self, parent, **kwargs):
        """Initialize scrollable frame."""
        super().__init__(parent, **kwargs)
        
        # Bind mouse wheel events
        self._bind_mouse_wheel()
    
    def _bind_mouse_wheel(self):
        """Bind mouse wheel events for scrolling."""
        # Bind to the frame itself
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event):
        """When mouse enters the frame, bind scroll events."""
        system = platform.system()
        
        if system == "Linux":
            # Linux uses Button-4 and Button-5 for scroll
            self.bind_all("<Button-4>", self._on_scroll_up)
            self.bind_all("<Button-5>", self._on_scroll_down)
        else:
            # Windows and Mac use MouseWheel
            self.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _on_leave(self, event):
        """When mouse leaves the frame, unbind scroll events."""
        system = platform.system()
        
        if system == "Linux":
            try:
                self.unbind_all("<Button-4>")
                self.unbind_all("<Button-5>")
            except Exception:
                pass
        else:
            try:
                self.unbind_all("<MouseWheel>")
            except Exception:
                pass
    
    def _on_scroll_up(self, event):
        """Handle scroll up on Linux."""
        self._parent_canvas.yview_scroll(-1, "units")
        return "break"
    
    def _on_scroll_down(self, event):
        """Handle scroll down on Linux."""
        self._parent_canvas.yview_scroll(1, "units")
        return "break"
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel on Windows/Mac."""
        self._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"