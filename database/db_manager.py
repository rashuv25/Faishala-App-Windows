# -*- coding: utf-8 -*-
"""Database connection manager."""

import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

from config.settings import Settings
from .models import ALL_TABLES


class DatabaseManager:
    """Manages SQLite database connections and initialization."""
    
    _instance: Optional['DatabaseManager'] = None
    _connection: Optional[sqlite3.Connection] = None
    
    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize database manager."""
        self.db_path = Settings.DATABASE_PATH
    
    def initialize(self) -> None:
        """Initialize database and create tables."""
        Settings.ensure_directories()
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for table_sql in ALL_TABLES:
                cursor.execute(table_sql)
            
            # Run migrations
            self._run_migrations(cursor)
            
            conn.commit()
    
    def _run_migrations(self, cursor):
        """Run database migrations."""
        # Check and add is_deleted column
        try:
            cursor.execute("SELECT is_deleted FROM documents LIMIT 1")
        except sqlite3.OperationalError:
            try:
                cursor.execute("ALTER TABLE documents ADD COLUMN is_deleted INTEGER DEFAULT 0")
            except Exception:
                pass
        
        # Check and add deleted_date column
        try:
            cursor.execute("SELECT deleted_date FROM documents LIMIT 1")
        except sqlite3.OperationalError:
            try:
                cursor.execute("ALTER TABLE documents ADD COLUMN deleted_date TEXT")
            except Exception:
                pass
    
    @contextmanager
    def get_connection(self):
        """Get database connection context manager."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a query and return cursor."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[dict]:
        """Fetch single row."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def fetch_all(self, query: str, params: tuple = ()) -> list:
        """Fetch all rows."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]