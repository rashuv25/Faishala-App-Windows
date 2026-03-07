#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
मुद्दा फैसला - Court Judgement Document Creator
Main Application Entry Point
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.app import MuddaPhaisalaApp
from database.db_manager import DatabaseManager
from config.settings import Settings
from utils.font_manager import FontManager


def main():
    """Main entry point for the application."""
    # Initialize settings
    settings = Settings()

    # Register fonts before UI starts
    font_manager = FontManager()
    font_status = font_manager.register_fonts()

    if Settings.DEBUG:
        print(f"[Startup] UI font registered: {font_status['ui_font_registered']}")
        print(f"[Startup] Export font registered: {font_status['export_font_registered']}")
        print(f"[Startup] Selected UI font: {font_manager.get_best_ui_font()}")
        print(f"[Startup] Export font: {font_manager.get_export_font()}")

    # Initialize database
    db_manager = DatabaseManager()
    db_manager.initialize()

    # Create and run application
    app = MuddaPhaisalaApp()
    app.run()


if __name__ == "__main__":
    main()