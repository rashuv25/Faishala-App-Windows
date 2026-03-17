# -*- coding: utf-8 -*-
"""Application settings and configuration."""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Settings:
    """Application settings."""

    # Application Info
    APP_NAME = "मुद्दा फैसला"
    APP_NAME_ENGLISH = "Mudda Phaisala"
    APP_VERSION = "1.0.0"

    # Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    ASSETS_DIR = BASE_DIR / "assets"
    FONTS_DIR = ASSETS_DIR / "fonts"
    IMAGES_DIR = ASSETS_DIR / "images"

    # Database
    DATABASE_NAME = "mudda_phaisala.db"
    DATABASE_PATH = DATA_DIR / DATABASE_NAME

    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

    # Export Font (used in DOCX/PDF only)
    EXPORT_FONT_NAME = "Noto Sans Devanagari"
    EXPORT_FONT_FILE = "NotoSansDevanagari-Regular.ttf"
    EXPORT_FONT_PATH = FONTS_DIR / EXPORT_FONT_FILE

    # UI Font (used inside desktop application)
    UI_FONT_NAME = "Noto Sans Devanagari"
    UI_FONT_FILE = "NotoSansDevanagari-Regular.ttf"
    UI_FONT_PATH = FONTS_DIR / UI_FONT_FILE
    UI_FONT_FALLBACK = "Arial"

    # UI Settings
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    MIN_WINDOW_WIDTH = 1000
    MIN_WINDOW_HEIGHT = 600

    # Auto-save
    AUTO_SAVE_ENABLED = True

    # Default District
    DEFAULT_DISTRICT = "मोरङ"

    # Environment
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Offline Mode - bypasses online login check
    OFFLINE_MODE = os.getenv("OFFLINE_MODE", "False").lower() == "true"

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)

    def __init__(self):
        """Initialize settings."""
        self.ensure_directories()