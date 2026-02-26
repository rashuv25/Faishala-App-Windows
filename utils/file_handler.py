# -*- coding: utf-8 -*-
"""File handling utilities."""

from pathlib import Path
from typing import Optional
import os


class FileHandler:
    """Handles file operations."""
    
    @staticmethod
    def get_save_path(default_name: str, file_type: str = "docx") -> Optional[Path]:
        """Open save file dialog and return selected path."""
        try:
            import tkinter as tk
            from tkinter import filedialog
            
            root = tk.Tk()
            root.withdraw()
            
            if file_type == "docx":
                filetypes = [("Word Document", "*.docx"), ("All Files", "*.*")]
                default_ext = ".docx"
            else:
                filetypes = [("PDF Document", "*.pdf"), ("All Files", "*.*")]
                default_ext = ".pdf"
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=default_ext,
                filetypes=filetypes,
                initialfile=default_name
            )
            
            root.destroy()
            
            if file_path:
                return Path(file_path)
            return None
            
        except Exception as e:
            print(f"File dialog error: {e}")
            return None
    
    @staticmethod
    def ensure_directory(path: Path) -> None:
        """Ensure directory exists."""
        path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def get_unique_filename(directory: Path, base_name: str, extension: str) -> Path:
        """Get unique filename in directory."""
        path = directory / f"{base_name}.{extension}"
        counter = 1
        
        while path.exists():
            path = directory / f"{base_name}_{counter}.{extension}"
            counter += 1
        
        return path