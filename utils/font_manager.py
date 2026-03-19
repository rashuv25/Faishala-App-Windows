# -*- coding: utf-8 -*-
"""Font management utilities."""

import platform
import subprocess
from pathlib import Path

from config.settings import Settings


class FontManager:
    """Manages export font and UI font registration."""

    def __init__(self):
        """Initialize font manager."""
        self.export_font_path = Settings.EXPORT_FONT_PATH
        self.export_font_name = Settings.EXPORT_FONT_NAME

        self.ui_font_path = Settings.UI_FONT_PATH
        self.ui_font_name = Settings.UI_FONT_NAME

    def is_font_installed(self, font_name: str) -> bool:
        """Check whether a font is available on the system."""
        system = platform.system()

        try:
            if system == "Linux":
                result = subprocess.run(
                    ["fc-list", ":", "family"],
                    capture_output=True,
                    text=True
                )
                return font_name.lower() in result.stdout.lower()

            elif system == "Windows":
                fonts_dir = Path("C:/Windows/Fonts")
                if not fonts_dir.exists():
                    return False

                for item in fonts_dir.iterdir():
                    if font_name.lower() in item.name.lower():
                        return True
                return False

            return False

        except Exception:
            return False

    def _register_linux_font_file(self, source_path: Path) -> bool:
        """Register a font file on Linux."""
        try:
            import shutil

            if not source_path.exists():
                return False

            user_fonts = Path.home() / ".local" / "share" / "fonts"
            user_fonts.mkdir(parents=True, exist_ok=True)

            dest = user_fonts / source_path.name
            if not dest.exists():
                shutil.copy(source_path, dest)

            subprocess.run(["fc-cache", "-f"], capture_output=True)
            return True
        except Exception:
            return False

    def _register_windows_font_file(self, source_path: Path) -> bool:
        """Register a font file on Windows for the current session."""
        try:
            import ctypes

            if not source_path.exists():
                return False

            FR_PRIVATE = 0x10
            path_str = str(source_path)

            added = ctypes.windll.gdi32.AddFontResourceExW(path_str, FR_PRIVATE, 0)
            return added > 0
        except Exception:
            return False

    def register_font_file(self, source_path: Path) -> bool:
        """Register a specific font file."""
        system = platform.system()

        if not source_path.exists():
            return False

        if system == "Linux":
            return self._register_linux_font_file(source_path)
        elif system == "Windows":
            return self._register_windows_font_file(source_path)

        return False

    def register_fonts(self) -> dict:
        """Register both UI and export fonts."""
        ui_ok = self.is_font_installed(self.ui_font_name)
        export_ok = self.is_font_installed(self.export_font_name)

        if not ui_ok:
            self.register_font_file(self.ui_font_path)
            ui_ok = self.is_font_installed(self.ui_font_name)

        if not export_ok:
            self.register_font_file(self.export_font_path)
            export_ok = self.is_font_installed(self.export_font_name)

        return {
            "ui_font_registered": ui_ok,
            "export_font_registered": export_ok
        }

    def get_best_ui_font(self) -> str:
        """Return the best available UI font."""
        candidates = [
            self.ui_font_name,
            "Kalimati",
            "Noto Sans Devanagari",
            "Mangal",
            Settings.UI_FONT_FALLBACK,
        ]

        for font_name in candidates:
            if font_name and self.is_font_installed(font_name):
                return font_name

        return Settings.UI_FONT_FALLBACK

    def get_export_font(self) -> str:
        """Return export font name."""
        return self.export_font_name