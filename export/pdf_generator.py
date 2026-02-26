# -*- coding: utf-8 -*-
"""PDF document generation."""

from pathlib import Path
from typing import Optional
import platform

from .docx_generator import DocxGenerator


class PdfGenerator:
    """Generates PDF documents."""
    
    def __init__(self):
        """Initialize PDF generator."""
        self.docx_generator = DocxGenerator()
    
    def generate(self, document_data: dict, output_path: Path) -> bool:
        """Generate PDF file from document data."""
        try:
            # First generate DOCX
            temp_docx_path = output_path.with_suffix('.docx')
            
            if not self.docx_generator.generate(document_data, temp_docx_path):
                return False
            
            # Convert to PDF
            success = self._convert_to_pdf(temp_docx_path, output_path)
            
            # Clean up temp DOCX
            if temp_docx_path.exists():
                temp_docx_path.unlink()
            
            return success
            
        except Exception as e:
            print(f"PDF generation error: {e}")
            return False
    
    def _convert_to_pdf(self, docx_path: Path, pdf_path: Path) -> bool:
        """Convert DOCX to PDF."""
        system = platform.system()
        
        if system == "Windows":
            return self._convert_windows(docx_path, pdf_path)
        elif system == "Linux":
            return self._convert_linux(docx_path, pdf_path)
        else:
            print(f"Unsupported platform: {system}")
            return False
    
    def _convert_windows(self, docx_path: Path, pdf_path: Path) -> bool:
        """Convert using docx2pdf on Windows."""
        try:
            from docx2pdf import convert
            convert(str(docx_path), str(pdf_path))
            return True
        except Exception as e:
            print(f"Windows PDF conversion error: {e}")
            return False
    
    def _convert_linux(self, docx_path: Path, pdf_path: Path) -> bool:
        """Convert using LibreOffice on Linux."""
        try:
            import subprocess
            result = subprocess.run([
                'libreoffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', str(pdf_path.parent),
                str(docx_path)
            ], capture_output=True, text=True)
            
            return result.returncode == 0
        except Exception as e:
            print(f"Linux PDF conversion error: {e}")
            return False