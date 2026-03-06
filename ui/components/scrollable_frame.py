# -*- coding: utf-8 -*-
"""Custom scrollable frame with stronger child-wheel support."""

import customtkinter as ctk
import platform


class ScrollableFrame(ctk.CTkScrollableFrame):
    """Scrollable frame with reliable mouse wheel scrolling."""

    def __init__(self, parent, **kwargs):
        """Initialize scrollable frame."""
        super().__init__(parent, **kwargs)

        self._system = platform.system()
        self._scroll_speed = 2
        self._binding_scheduled = False

        self._setup_scroll_support()

    def _setup_scroll_support(self):
        """Bind scrolling support for self and child widgets."""
        self.bind("<Configure>", self._schedule_rebind, add="+")
        self.bind("<Map>", self._schedule_rebind, add="+")
        self.bind("<Enter>", self._on_enter, add="+")
        self.bind("<Leave>", self._on_leave, add="+")
        self._schedule_rebind()

    def _schedule_rebind(self, event=None):
        """Schedule rebinding once after layout updates."""
        if self._binding_scheduled:
            return
        self._binding_scheduled = True
        self.after(20, self._do_rebind)

    def _do_rebind(self):
        """Bind scrolling and hover handlers to self and all descendants."""
        self._binding_scheduled = False
        try:
            self._bind_widget_and_children(self)
        except Exception:
            pass

    def _bind_widget_and_children(self, widget):
        """Recursively bind hover + wheel events to widget and children."""
        try:
            widget.bind("<Enter>", self._on_enter, add="+")
            widget.bind("<Leave>", self._on_leave, add="+")
        except Exception:
            pass

        # Bind wheel directly on each widget so textboxes don't swallow it
        try:
            if self._system == "Linux":
                widget.bind("<Button-4>", self._on_scroll_up, add="+")
                widget.bind("<Button-5>", self._on_scroll_down, add="+")
                widget.bind("<MouseWheel>", self._on_mousewheel, add="+")
            else:
                widget.bind("<MouseWheel>", self._on_mousewheel, add="+")
        except Exception:
            pass

        try:
            children = widget.winfo_children()
        except Exception:
            children = []

        for child in children:
            self._bind_widget_and_children(child)

    def _on_enter(self, event=None):
        """Activate wheel scrolling while mouse is over this scrollable area."""
        try:
            if self._system == "Linux":
                self.bind_all("<Button-4>", self._on_scroll_up, add="+")
                self.bind_all("<Button-5>", self._on_scroll_down, add="+")
                self.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
            else:
                self.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
        except Exception:
            pass

    def _on_leave(self, event=None):
        """Deactivate global wheel bindings when pointer leaves the frame."""
        try:
            x, y = self.winfo_pointerxy()
            widget_x = self.winfo_rootx()
            widget_y = self.winfo_rooty()
            widget_w = self.winfo_width()
            widget_h = self.winfo_height()

            inside = (
                widget_x <= x <= widget_x + widget_w and
                widget_y <= y <= widget_y + widget_h
            )
            if inside:
                return
        except Exception:
            pass

        try:
            if self._system == "Linux":
                self.unbind_all("<Button-4>")
                self.unbind_all("<Button-5>")
                self.unbind_all("<MouseWheel>")
            else:
                self.unbind_all("<MouseWheel>")
        except Exception:
            pass

    def _scroll_canvas(self, amount: int):
        """Scroll the parent canvas safely."""
        try:
            self._parent_canvas.yview_scroll(amount, "units")
        except Exception:
            pass
        return "break"

    def _on_scroll_up(self, event=None):
        """Linux scroll up."""
        return self._scroll_canvas(-self._scroll_speed)

    def _on_scroll_down(self, event=None):
        """Linux scroll down."""
        return self._scroll_canvas(self._scroll_speed)

    def _on_mousewheel(self, event):
        """Mouse wheel handler."""
        try:
            delta = getattr(event, "delta", 0)

            if delta != 0:
                step = int(-delta / 120)
                if step == 0:
                    step = -1 if delta > 0 else 1
            else:
                step = 0

            if step != 0:
                return self._scroll_canvas(step * self._scroll_speed)
        except Exception:
            pass

        return "break"