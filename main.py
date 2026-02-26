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


def main():
    """Main entry point for the application."""

    # Initialize settings
    settings = Settings()

    # Initialize database
    db_manager = DatabaseManager()
    db_manager.initialize()

    # Create and run application
    app = MuddaPhaisalaApp()
    app.run()


if __name__ == "__main__":
    main()
