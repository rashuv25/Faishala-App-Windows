# -*- coding: utf-8 -*-
"""Document management operations."""

import json
from typing import Optional, List, Dict, Any

from database.local_db import LocalDatabase
from auth.session_manager import SessionManager
from auth.nepali_date_validator import NepaliDateValidator


class DocumentManager:
    """Manages document operations."""
    
    def __init__(self):
        """Initialize document manager."""
        self.local_db = LocalDatabase()
        self.session = SessionManager()
        self.date_validator = NepaliDateValidator()
    
    def create_document(self, name: str) -> int:
        """Create new document and return its ID."""
        nepali_date = self._get_nepali_date_string()
        return self.local_db.create_document(
            self.session.user_id,
            name,
            nepali_date
        )
    
    def document_name_exists(self, name: str, exclude_id: int = None) -> bool:
        """Check if document name already exists."""
        return self.local_db.document_name_exists(
            self.session.user_id,
            name,
            exclude_id
        )
    
    def get_document(self, document_id: int) -> Optional[Dict]:
        """Get document by ID with parsed JSON fields."""
        doc = self.local_db.get_document(document_id)
        if doc:
            if doc.get('case_points'):
                try:
                    doc['case_points'] = json.loads(doc['case_points'])
                except (json.JSONDecodeError, TypeError):
                    doc['case_points'] = [""]
            else:
                doc['case_points'] = [""]
            
            if doc.get('tapsil_points'):
                try:
                    doc['tapsil_points'] = json.loads(doc['tapsil_points'])
                except (json.JSONDecodeError, TypeError):
                    doc['tapsil_points'] = self._get_default_tapsil()
            else:
                doc['tapsil_points'] = self._get_default_tapsil()
        
        return doc
    
    def get_all_documents(self) -> List[Dict]:
        """Get all documents for current user."""
        # Auto-delete old trash items
        self.local_db.auto_delete_old_trash(self.session.user_id, 30)
        
        return self.local_db.get_user_documents(self.session.user_id)
    
    def save_document(self, document_id: int, data: Dict[str, Any]) -> None:
        """Save document data."""
        self.local_db.update_document(document_id, data)
    
    def delete_document(self, document_id: int) -> None:
        """Soft delete document (move to trash)."""
        self.local_db.soft_delete_document(document_id)
    
    def restore_document(self, document_id: int) -> None:
        """Restore document from trash."""
        self.local_db.restore_document(document_id)
    
    def permanent_delete_document(self, document_id: int) -> None:
        """Permanently delete document."""
        self.local_db.permanent_delete_document(document_id)
    
    def get_trash_documents(self) -> List[Dict]:
        """Get all documents in trash."""
        return self.local_db.get_trash_documents(self.session.user_id)
    
    def empty_trash(self) -> None:
        """Empty trash - permanently delete all trash documents."""
        self.local_db.empty_trash(self.session.user_id)
    
    def rename_document(self, document_id: int, new_name: str) -> None:
        """Rename document."""
        self.local_db.rename_document(document_id, new_name)
    
    def search_documents(self, search_term: str) -> List[Dict]:
        """Search documents by name."""
        return self.local_db.search_documents(self.session.user_id, search_term)
    
    def filter_by_date(self, date_str: str) -> List[Dict]:
        """Filter documents by date."""
        return self.local_db.filter_documents_by_date(self.session.user_id, date_str)
    
    def _get_nepali_date_string(self) -> str:
        """Get current Nepali date as string."""
        date_info = self.date_validator.get_current_nepali_date()
        return f"{date_info['year']}-{date_info['month']:02d}-{date_info['day']:02d}"
    
    def _get_default_tapsil(self) -> List[str]:
        """Get default tapsil points."""
        from config.constants import DEFAULT_TAPSIL_POINTS
        return DEFAULT_TAPSIL_POINTS.copy()