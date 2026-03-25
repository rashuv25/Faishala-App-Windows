# -*- coding: utf-8 -*-
"""
Script to create a test user for development.
Run this once to set up initial user.
"""

import sys
import os
import hashlib

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager


def create_test_user(username: str, password: str):
    """Create a test user in the database."""
    
    # Initialize database
    db = DatabaseManager()
    db.initialize()
    
    # Hash password
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Check if user already exists
    existing = db.fetch_one(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    
    if existing:
        print(f"User '{username}' already exists!")
        return
    
    # Create user
    query = """
        INSERT INTO users (username, password_hash, last_login_nepali_year, last_login_nepali_month)
        VALUES (?, ?, ?, ?)
    """
    
    db.execute(query, (username, password_hash, 2081, 1))
    
    print("Test user created successfully!")
    print(f"   Username: {username}")
    print(f"   Password: {password}")


if __name__ == "__main__":
    # Default test credentials
    USERNAME = "testuser"
    PASSWORD = "test123"
    
    # Allow custom credentials via command line
    if len(sys.argv) >= 3:
        USERNAME = sys.argv[1]
        PASSWORD = sys.argv[2]
    
    create_test_user(USERNAME, PASSWORD)