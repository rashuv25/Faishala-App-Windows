# # -*- coding: utf-8 -*-
# """Silent backup synchronization manager."""

# import threading
# from typing import Optional, List
# from pathlib import Path
# import tempfile

# from database.local_db import LocalDatabase
# from database.remote_db import RemoteDatabase
# from export.docx_generator import DocxGenerator
# from auth.session_manager import SessionManager


# class SyncManager:
#     """Manages silent backup synchronization."""
    
#     def __init__(self):
#         """Initialize sync manager."""
#         self.local_db = LocalDatabase()
#         self.remote_db = RemoteDatabase()
#         self.docx_generator = DocxGenerator()
#         self.session = SessionManager()
#         self._sync_thread: Optional[threading.Thread] = None
#         self._is_syncing = False
    
#     def check_and_sync(self) -> None:
#         """Check for backup requests and sync if needed."""
#         if not self.remote_db.is_connected():
#             return
        
#         if self._is_syncing:
#             return
        
#         # Run sync in background thread
#         self._sync_thread = threading.Thread(target=self._perform_sync, daemon=True)
#         self._sync_thread.start()
    
#     def _perform_sync(self) -> None:
#         """Perform synchronization (runs in background)."""
#         self._is_syncing = True
        
#         try:
#             user_id = self.session.user_id
#             if not user_id:
#                 return
            
#             # Check for pending backup request
#             request = self.remote_db.check_backup_request(user_id)
#             if not request:
#                 return
            
#             # Get documents to backup
#             documents = self.local_db.get_user_documents(user_id)
            
#             # Upload each document
#             for doc in documents:
#                 self._backup_document(doc)
            
#             # Mark request as complete
#             self.remote_db.mark_backup_complete(request['id'])
            
#         except Exception as e:
#             print(f"Sync error: {e}")
#         finally:
#             self._is_syncing = False
    
#     def _backup_document(self, document: dict) -> bool:
#         """Backup single document."""
#         try:
#             # Create temp DOCX file
#             with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
#                 temp_path = Path(tmp.name)
            
#             # Generate DOCX
#             if not self.docx_generator.generate(document, temp_path):
#                 return False
            
#             # Read file content
#             with open(temp_path, 'rb') as f:
#                 content = f.read()
            
#             # Upload to remote
#             filename = f"{document['document_name']}_{document['id']}.docx"
#             success = self.remote_db.upload_backup(
#                 self.session.user_id,
#                 document['id'],
#                 content,
#                 filename
#             )
            
#             # Clean up temp file
#             temp_path.unlink()
            
#             return success
            
#         except Exception as e:
#             print(f"Document backup error: {e}")
#             return False










# -*- coding: utf-8 -*-
"""Silent backup synchronization manager.

Remote backup is intentionally **developer-controlled**:
- It runs only when Supabase is configured AND a local setting enables it.
- It is silent for end-users (no UI popups). Status is written to local backup_log.
"""

import threading
from typing import Optional
from pathlib import Path
import tempfile

from config.settings import Settings
from database.local_db import LocalDatabase
from database.remote_db import RemoteDatabase
from export.docx_generator import DocxGenerator
from auth.session_manager import SessionManager


class SyncManager:
    """Manages silent backup synchronization."""

    def __init__(self):
        """Initialize sync manager."""
        self.local_db = LocalDatabase()
        self.remote_db = RemoteDatabase()
        self.docx_generator = DocxGenerator()
        self.session = SessionManager()
        self._sync_thread: Optional[threading.Thread] = None
        self._is_syncing = False

    def check_and_sync(self) -> None:
        """Check for backup requests and sync if needed (silent).

        Backup will run ONLY when:
        - Supabase is connected
        - app_settings.remote_backup_enabled is True
        - a pending backup request exists for the logged-in user
        """
        # Gate 1: developer-controlled local setting
        if not self.local_db.get_bool_setting("remote_backup_enabled", default=False):
            return

        # Gate 2: Supabase configured/connected
        if not self.remote_db.is_connected():
            return

        if self._is_syncing:
            return

        # Run sync in background thread
        self._sync_thread = threading.Thread(target=self._perform_sync, daemon=True)
        self._sync_thread.start()

    def _perform_sync(self) -> None:
        """Perform synchronization (runs in background)."""
        self._is_syncing = True

        try:
            user_id = self.session.user_id
            if not user_id:
                return

            # Check for pending backup request
            request = self.remote_db.check_backup_request(user_id)
            if not request:
                return

            # Get documents to backup
            documents = self.local_db.get_user_documents(user_id)

            # Upload each document
            for doc in documents:
                success = self._backup_document(doc)
                self.local_db.log_backup_status(
                    document_id=doc.get("id"),
                    status="success" if success else "failed"
                )

            # Mark request as complete
            self.remote_db.mark_backup_complete(request["id"])

        except Exception as e:
            # Silent by default; print only in DEBUG
            if Settings.DEBUG:
                print(f"[SyncManager] Sync error: {e}")
        finally:
            self._is_syncing = False

    def _backup_document(self, document: dict) -> bool:
        """Backup single document."""
        temp_path: Optional[Path] = None
        try:
            # Create temp DOCX file
            with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
                temp_path = Path(tmp.name)

            # Generate DOCX
            if not self.docx_generator.generate(document, temp_path):
                return False

            # Read file content
            with open(temp_path, "rb") as f:
                content = f.read()

            # Upload to remote
            filename = f"{document.get('document_name', 'document')}_{document.get('id', '')}.docx"
            success = self.remote_db.upload_backup(
                self.session.user_id,
                document.get("id"),
                content,
                filename
            )

            return bool(success)

        except Exception as e:
            if Settings.DEBUG:
                print(f"[SyncManager] Document backup error: {e}")
            return False
        finally:
            # Clean up temp file
            try:
                if temp_path and temp_path.exists():
                    temp_path.unlink()
            except Exception:
                pass