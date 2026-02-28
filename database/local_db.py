# -*- coding: utf-8 -*-
"""Local database CRUD operations."""

import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

from .db_manager import DatabaseManager


class LocalDatabase:
    """Handles all local database operations."""
    
    def __init__(self):
        """Initialize local database handler."""
        self.db = DatabaseManager()
    
    # ==================== USER OPERATIONS ====================
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username."""
        query = "SELECT * FROM users WHERE username = ?"
        return self.db.fetch_one(query, (username,))
    
    def get_last_session_user(self) -> Optional[Dict]:
        """Get the most recently updated user who has a session token."""
        query = """
            SELECT * FROM users
            WHERE session_token IS NOT NULL AND session_token != ''
            ORDER BY updated_at DESC
            LIMIT 1
        """
        return self.db.fetch_one(query, ())

    def set_user_session_token(self, user_id: int, token: Optional[str]):
        query = "UPDATE users SET session_token = ?, updated_at = ? WHERE id = ?"
        now = datetime.now().isoformat()
        self.db.execute(query, (token, now, user_id))


    
    def update_user_login(self, user_id: int, nepali_year: int, nepali_month: int, token: str) -> None:
        """Update user's last login info."""
        query = """
            UPDATE users 
            SET last_login_date = ?, 
                last_login_nepali_year = ?,
                last_login_nepali_month = ?, 
                session_token = ?,
                updated_at = ?
            WHERE id = ?
        """
        now = datetime.now().isoformat()
        self.db.execute(query, (now, nepali_year, nepali_month, token, now, user_id))
    
    # ==================== DOCUMENT OPERATIONS ====================
    
    def create_document(self, user_id: int, document_name: str, nepali_date: str) -> int:
        """Create new document and return its ID."""
        query = """
            INSERT INTO documents (user_id, document_name, nepali_created_date, is_deleted)
            VALUES (?, ?, ?, 0)
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id, document_name, nepali_date))
            conn.commit()
            return cursor.lastrowid
    
    def get_document(self, document_id: int) -> Optional[Dict]:
        """Get document by ID."""
        query = "SELECT * FROM documents WHERE id = ? AND is_deleted = 0"
        return self.db.fetch_one(query, (document_id,))
    
    def get_user_documents(self, user_id: int) -> List[Dict]:
        """Get all active documents for a user, ordered by date."""
        query = """
            SELECT * FROM documents 
            WHERE user_id = ? AND is_deleted = 0
            ORDER BY modified_date DESC
        """
        return self.db.fetch_all(query, (user_id,))
    
    def document_name_exists(self, user_id: int, document_name: str, exclude_id: int = None) -> bool:
        """Check if document name already exists for user."""
        if exclude_id:
            query = """
                SELECT COUNT(*) as count FROM documents 
                WHERE user_id = ? AND document_name = ? AND is_deleted = 0 AND id != ?
            """
            result = self.db.fetch_one(query, (user_id, document_name, exclude_id))
        else:
            query = """
                SELECT COUNT(*) as count FROM documents 
                WHERE user_id = ? AND document_name = ? AND is_deleted = 0
            """
            result = self.db.fetch_one(query, (user_id, document_name))
        
        return result and result['count'] > 0
    
    def update_document(self, document_id: int, data: Dict[str, Any]) -> None:
        """Update document fields."""
        fields = []
        values = []
        
        for key, value in data.items():
            if key in ['case_points', 'tapsil_points']:
                value = json.dumps(value, ensure_ascii=False)
            fields.append(f"{key} = ?")
            values.append(value)
        
        fields.append("modified_date = ?")
        values.append(datetime.now().isoformat())
        values.append(document_id)
        
        query = f"UPDATE documents SET {', '.join(fields)} WHERE id = ?"
        self.db.execute(query, tuple(values))
    
    def soft_delete_document(self, document_id: int) -> None:
        """Soft delete document (move to trash)."""
        query = """
            UPDATE documents 
            SET is_deleted = 1, deleted_date = ?
            WHERE id = ?
        """
        self.db.execute(query, (datetime.now().isoformat(), document_id))
    
    def restore_document(self, document_id: int) -> None:
        """Restore document from trash."""
        query = """
            UPDATE documents 
            SET is_deleted = 0, deleted_date = NULL
            WHERE id = ?
        """
        self.db.execute(query, (document_id,))
    
    def permanent_delete_document(self, document_id: int) -> None:
        """Permanently delete document."""
        # Delete auto-save first
        self.db.execute("DELETE FROM auto_save WHERE document_id = ?", (document_id,))
        # Delete document
        self.db.execute("DELETE FROM documents WHERE id = ?", (document_id,))
    
    def get_trash_documents(self, user_id: int) -> List[Dict]:
        """Get all documents in trash for a user."""
        query = """
            SELECT * FROM documents 
            WHERE user_id = ? AND is_deleted = 1
            ORDER BY deleted_date DESC
        """
        return self.db.fetch_all(query, (user_id,))
    
    def empty_trash(self, user_id: int) -> None:
        """Permanently delete all documents in trash for a user."""
        # Get all trash document IDs
        docs = self.get_trash_documents(user_id)
        for doc in docs:
            self.permanent_delete_document(doc['id'])
    
    def auto_delete_old_trash(self, user_id: int, days: int = 30) -> int:
        """Automatically delete documents older than specified days. Returns count of deleted."""
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        query = """
            SELECT id FROM documents 
            WHERE user_id = ? AND is_deleted = 1 AND deleted_date < ?
        """
        old_docs = self.db.fetch_all(query, (user_id, cutoff_date))
        
        for doc in old_docs:
            self.permanent_delete_document(doc['id'])
        
        return len(old_docs)
    
    def rename_document(self, document_id: int, new_name: str) -> None:
        """Rename document."""
        query = "UPDATE documents SET document_name = ?, modified_date = ? WHERE id = ?"
        self.db.execute(query, (new_name, datetime.now().isoformat(), document_id))
    
    def search_documents(self, user_id: int, search_term: str) -> List[Dict]:
        """Search documents by name."""
        query = """
            SELECT * FROM documents 
            WHERE user_id = ? AND document_name LIKE ? AND is_deleted = 0
            ORDER BY modified_date DESC
        """
        return self.db.fetch_all(query, (user_id, f"%{search_term}%"))
    
    def filter_documents_by_date(self, user_id: int, nepali_date: str) -> List[Dict]:
        """Filter documents by Nepali date."""
        query = """
            SELECT * FROM documents 
            WHERE user_id = ? AND nepali_created_date LIKE ? AND is_deleted = 0
            ORDER BY modified_date DESC
        """
        return self.db.fetch_all(query, (user_id, f"%{nepali_date}%"))
    
    # ==================== DICTIONARY OPERATIONS ====================
    
    def get_dictionary_items(self, category: str) -> List[str]:
        """Get all items in a dictionary category."""
        query = "SELECT value FROM dictionary WHERE category = ? ORDER BY value"
        rows = self.db.fetch_all(query, (category,))
        return [row['value'] for row in rows]
    
    def add_dictionary_item(self, category: str, value: str) -> bool:
        """Add item to dictionary. Returns False if already exists."""
        try:
            query = "INSERT INTO dictionary (category, value) VALUES (?, ?)"
            self.db.execute(query, (category, value))
            return True
        except Exception:
            return False
    
    def delete_dictionary_item(self, category: str, value: str) -> None:
        """Delete item from dictionary."""
        query = "DELETE FROM dictionary WHERE category = ? AND value = ?"
        self.db.execute(query, (category, value))
    
    # ==================== AUTO-SAVE OPERATIONS ====================
    
    def save_auto_save(self, document_id: int, state: Dict) -> None:
        """Save auto-save state."""
        delete_query = "DELETE FROM auto_save WHERE document_id = ?"
        self.db.execute(delete_query, (document_id,))
        
        insert_query = "INSERT INTO auto_save (document_id, save_state) VALUES (?, ?)"
        self.db.execute(insert_query, (document_id, json.dumps(state, ensure_ascii=False)))
    
    def get_auto_save(self, document_id: int) -> Optional[Dict]:
        """Get auto-save state."""
        query = "SELECT save_state FROM auto_save WHERE document_id = ?"
        row = self.db.fetch_one(query, (document_id,))
        if row:
            return json.loads(row['save_state'])
        return None
    
     # ==================== SETTINGS OPERATIONS ====================

    def get_setting(self, key: str) -> Optional[str]:
        """Get app setting."""
        query = "SELECT value FROM app_settings WHERE key = ?"
        row = self.db.fetch_one(query, (key,))
        return row["value"] if row else None

    def get_bool_setting(self, key: str, default: bool = False) -> bool:
        """Get a boolean setting from app_settings.

        Accepts common truthy values: true/1/yes/on (case-insensitive).
        """
        value = self.get_setting(key)
        if value is None:
            return default
        return str(value).strip().lower() in ("true", "1", "yes", "on")

    def set_setting(self, key: str, value: str) -> None:
        """Set app setting."""
        query = """
            INSERT INTO app_settings (key, value, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET value = ?, updated_at = ?
        """
        now = datetime.now().isoformat()
        self.db.execute(query, (key, value, now, value, now))

    # ==================== BACKUP LOG ====================

    def log_backup_status(self, document_id: Optional[int], status: str) -> None:
        """Write a silent backup status entry to backup_log."""
        query = "INSERT INTO backup_log (document_id, status) VALUES (?, ?)"
        self.db.execute(query, (document_id, status))

    def get_all_settings(self) -> Dict[str, str]:
        """Get all settings as a dictionary."""
        query = "SELECT key, value FROM app_settings"
        rows = self.db.fetch_all(query, ())
        return {row["key"]: row["value"] for row in rows}