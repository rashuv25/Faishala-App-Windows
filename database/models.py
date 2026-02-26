# -*- coding: utf-8 -*-
"""Database table definitions."""

# SQL Statements for table creation

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    last_login_date TEXT,
    last_login_nepali_month INTEGER,
    last_login_nepali_year INTEGER,
    session_token TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
)
"""

CREATE_DOCUMENTS_TABLE = """
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    document_name TEXT NOT NULL,
    district TEXT DEFAULT 'मोरङ',
    cdo_name TEXT,
    wadi_content TEXT,
    pratiwadi_content TEXT,
    mudda TEXT,
    mudda_number TEXT,
    case_points TEXT,
    office_decision TEXT,
    tapsil_points TEXT,
    typist_name TEXT,
    footer_cdo_name TEXT,
    document_date_year INTEGER,
    document_date_month TEXT,
    document_date_day INTEGER,
    document_date_day_num INTEGER,
    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
    modified_date TEXT DEFAULT CURRENT_TIMESTAMP,
    nepali_created_date TEXT,
    is_synced INTEGER DEFAULT 0,
    is_deleted INTEGER DEFAULT 0,
    deleted_date TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
"""

CREATE_DICTIONARY_TABLE = """
CREATE TABLE IF NOT EXISTS dictionary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    value TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(category, value)
)
"""

CREATE_AUTO_SAVE_TABLE = """
CREATE TABLE IF NOT EXISTS auto_save (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER,
    save_state TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents (id)
)
"""

CREATE_SETTINGS_TABLE = """
CREATE TABLE IF NOT EXISTS app_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    value TEXT,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
)
"""

CREATE_BACKUP_LOG_TABLE = """
CREATE TABLE IF NOT EXISTS backup_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER,
    backup_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT,
    FOREIGN KEY (document_id) REFERENCES documents (id)
)
"""

# Migration to add is_deleted column if not exists
ADD_IS_DELETED_COLUMN = """
ALTER TABLE documents ADD COLUMN is_deleted INTEGER DEFAULT 0
"""

ADD_DELETED_DATE_COLUMN = """
ALTER TABLE documents ADD COLUMN deleted_date TEXT
"""

# List of all tables
ALL_TABLES = [
    CREATE_USERS_TABLE,
    CREATE_DOCUMENTS_TABLE,
    CREATE_DICTIONARY_TABLE,
    CREATE_AUTO_SAVE_TABLE,
    CREATE_SETTINGS_TABLE,
    CREATE_BACKUP_LOG_TABLE
]