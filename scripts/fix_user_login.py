# -*- coding: utf-8 -*-
"""
Script to fix user login date for offline testing.
"""

import sys
import os
import sqlite3

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Settings

def fix_user_login():
    """Update user's last login to allow offline access."""
    
    db_path = Settings.DATABASE_PATH
    
    if not db_path.exists():
        print("❌ Database not found! Run create_test_user.py first.")
        return
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Get current Nepali date
    try:
        import nepali_datetime
        today = nepali_datetime.date.today()
        current_year = today.year
        current_month = today.month
    except ImportError:
        # Fallback - use approximate values
        current_year = 2081
        current_month = 10
    
    # Update user's login date and add session token
    cursor.execute("""
        UPDATE users 
        SET last_login_nepali_year = ?,
            last_login_nepali_month = ?,
            session_token = 'offline_session_token_12345',
            last_login_date = datetime('now')
        WHERE username = 'testuser'
    """, (current_year, current_month))
    
    # Also update app_settings table
    cursor.execute("""
        INSERT OR REPLACE INTO app_settings (key, value, updated_at)
        VALUES ('last_login_nepali_year', ?, datetime('now'))
    """, (str(current_year),))
    
    cursor.execute("""
        INSERT OR REPLACE INTO app_settings (key, value, updated_at)
        VALUES ('last_login_nepali_month', ?, datetime('now'))
    """, (str(current_month),))
    
    conn.commit()
    conn.close()
    
    print(f"✅ User login fixed!")
    print(f"   Nepali Year: {current_year}")
    print(f"   Nepali Month: {current_month}")
    print(f"")
    print(f"   Now try logging in with:")
    print(f"   Username: testuser")
    print(f"   Password: test123")


if __name__ == "__main__":
    fix_user_login()