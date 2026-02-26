# -*- coding: utf-8 -*-
"""Font management utilities."""

import platform
from pathlib import Path
from typing import Optional

from config.settings import Settings


class FontManager:
    """Manages Kalimati font installation and usage."""
    
    def __init__(self):
        """Initialize font manager."""
        self.font_path = Settings.FONT_PATH
        self.font_name = Settings.FONT_NAME
    
    def is_font_available(self) -> bool:
        """Check if Kalimati font file exists."""
        return self.font_path.exists()
    
    def get_font_path(self) -> Optional[Path]:
        """Get path to font file."""
        if self.is_font_available():
            return self.font_path
        return None
    
    def register_font(self) -> bool:
        """Register font for use in the application."""
        if not self.is_font_available():
            print(f"Font file not found: {self.font_path}")
            return False
        
        system = platform.system()
        
        try:
            if system == "Windows":
                return self._register_windows()
            elif system == "Linux":
                return self._register_linux()
            else:
                print(f"Unsupported platform: {system}")
                return False
        except Exception as e:
            print(f"Font registration error: {e}")
            return False
    
    def _register_windows(self) -> bool:
        """Register font on Windows."""
        # CustomTkinter should handle this automatically
        # if font is in system or app fonts folder
        return True
    
    def _register_linux(self) -> bool:
        """Register font on Linux."""
        # Copy font to user fonts directory
        import shutil
        user_fonts = Path.home() / ".local" / "share" / "fonts"
        user_fonts.mkdir(parents=True, exist_ok=True)
        
        dest = user_fonts / self.font_path.name
        if not dest.exists():
            shutil.copy(self.font_path, dest)
        
        # Rebuild font cache
        import subprocess
        subprocess.run(['fc-cache', '-f'], capture_output=True)
        
        return True