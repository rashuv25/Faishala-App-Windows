# # -*- coding: utf-8 -*-
# """Remote database operations (Supabase)."""

# from typing import Optional, Dict, List
# from config.settings import Settings

# try:
#     from supabase import create_client, Client
#     SUPABASE_AVAILABLE = True
# except ImportError:
#     SUPABASE_AVAILABLE = False


# class RemoteDatabase:
#     """Handles Supabase remote database operations."""
    
#     _instance: Optional['RemoteDatabase'] = None
#     _client: Optional['Client'] = None
    
#     def __new__(cls):
#         """Singleton pattern."""
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#         return cls._instance
    
#     def __init__(self):
#         """Initialize remote database connection."""
#         if not SUPABASE_AVAILABLE:
#             self._client = None
#             return
            
#         if self._client is None and Settings.SUPABASE_URL and Settings.SUPABASE_KEY:
#             try:
#                 self._client = create_client(Settings.SUPABASE_URL, Settings.SUPABASE_KEY)
#             except Exception as e:
#                 print(f"Failed to connect to Supabase: {e}")
#                 self._client = None
    
#     def is_connected(self) -> bool:
#         """Check if connected to remote database."""
#         return self._client is not None
    
#     # ==================== AUTHENTICATION ====================
    
#     def verify_credentials(self, username: str, password_hash: str) -> Optional[Dict]:
#         """Verify user credentials against remote database."""
#         if not self.is_connected():
#             return None
        
#         try:
#             response = self._client.table('users').select('*').eq(
#                 'username', username
#             ).eq('password_hash', password_hash).execute()
            
#             if response.data and len(response.data) > 0:
#                 return response.data[0]
#             return None
#         except Exception as e:
#             print(f"Remote auth error: {e}")
#             return None
    
#     # ==================== BACKUP OPERATIONS ====================
    
#     def check_backup_request(self, user_id: int) -> Optional[Dict]:
#         """Check if there's a pending backup request for user."""
#         if not self.is_connected():
#             return None
        
#         try:
#             response = self._client.table('backup_requests').select('*').eq(
#                 'target_user_id', user_id
#             ).eq('status', 'pending').execute()
            
#             if response.data and len(response.data) > 0:
#                 return response.data[0]
#             return None
#         except Exception as e:
#             print(f"Backup check error: {e}")
#             return None
    
#     def upload_backup(self, user_id: int, document_id: int, file_content: bytes, filename: str) -> bool:
#         """Upload document backup to remote storage."""
#         if not self.is_connected():
#             return False
        
#         try:
#             # Upload to Supabase storage
#             path = f"backups/{user_id}/{filename}"
#             self._client.storage.from_('documents').upload(path, file_content)
            
#             # Log backup
#             self._client.table('backups').insert({
#                 'user_id': user_id,
#                 'document_id': document_id,
#                 'file_path': path
#             }).execute()
            
#             return True
#         except Exception as e:
#             print(f"Backup upload error: {e}")
#             return False
    
#     def mark_backup_complete(self, request_id: int) -> None:
#         """Mark backup request as completed."""
#         if not self.is_connected():
#             return
        
#         try:
#             self._client.table('backup_requests').update({
#                 'status': 'completed'
#             }).eq('id', request_id).execute()
#         except Exception as e:
#             print(f"Backup status update error: {e}")






# -*- coding: utf-8 -*-
"""Remote database operations (Supabase)."""

from typing import Optional, Dict
from config.settings import Settings

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False


class RemoteDatabase:
    """Handles Supabase remote database operations."""

    _instance: Optional["RemoteDatabase"] = None
    _client: Optional["Client"] = None

    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize remote database connection."""
        if not SUPABASE_AVAILABLE:
            self._client = None
            return

        if self._client is None and Settings.SUPABASE_URL and Settings.SUPABASE_KEY:
            try:
                self._client = create_client(Settings.SUPABASE_URL, Settings.SUPABASE_KEY)
            except Exception as e:
                if Settings.DEBUG:
                    print(f"Failed to connect to Supabase: {e}")
                self._client = None

    def is_connected(self) -> bool:
        """Check if connected to remote database."""
        return self._client is not None

    # ==================== AUTHENTICATION ====================

    def verify_credentials(self, username: str, password_hash: str) -> Optional[Dict]:
        """Verify user credentials against remote database."""
        if not self.is_connected():
            return None

        try:
            response = (
                self._client.table("users")
                .select("*")
                .eq("username", username)
                .eq("password_hash", password_hash)
                .execute()
            )

            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            if Settings.DEBUG:
                print(f"Remote auth error: {e}")
            return None

    # ==================== BACKUP OPERATIONS ====================

    def check_backup_request(self, user_id: int) -> Optional[Dict]:
        """Check if there's a pending backup request for user."""
        if not self.is_connected():
            return None

        try:
            response = (
                self._client.table("backup_requests")
                .select("*")
                .eq("target_user_id", user_id)
                .eq("status", "pending")
                .execute()
            )

            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            if Settings.DEBUG:
                print(f"Backup check error: {e}")
            return None

    def upload_backup(self, user_id: int, document_id: int, file_content: bytes, filename: str) -> bool:
        """Upload document backup to remote storage."""
        if not self.is_connected():
            return False

        try:
            # Upload to Supabase storage
            path = f"backups/{user_id}/{filename}"
            self._client.storage.from_("documents").upload(path, file_content)

            # Log backup
            self._client.table("backups").insert(
                {"user_id": user_id, "document_id": document_id, "file_path": path}
            ).execute()

            return True
        except Exception as e:
            if Settings.DEBUG:
                print(f"Backup upload error: {e}")
            return False

    def mark_backup_complete(self, request_id: int) -> None:
        """Mark backup request as completed."""
        if not self.is_connected():
            return

        try:
            self._client.table("backup_requests").update({"status": "completed"}).eq(
                "id", request_id
            ).execute()
        except Exception as e:
            if Settings.DEBUG:
                print(f"Backup status update error: {e}")