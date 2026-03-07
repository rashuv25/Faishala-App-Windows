# -*- coding: utf-8 -*-
"""DOCX document generation."""

from pathlib import Path
from typing import Dict, Any, Optional
from docx import Document
from docx.shared import Pt, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from config.settings import Settings
from config.constants import (
    DOCUMENT_TOP_BLANK_LINES,
    NEPALI_MONTHS,
    DEFAULT_TAPSIL_POINTS
)
from .dot_calculator import DotCalculator


class DocxGenerator:
    """Generates DOCX documents."""
    
    def __init__(self):
        """Initialize DOCX generator."""
        self.font_name = Settings.EXPORT_FONT_NAME
        self.dot_calculator = DotCalculator()
    
    def generate(self, document_data: Dict[str, Any], output_path: Path) -> bool:
        """Generate DOCX file from document data."""
        try:
            doc = Document()
            
            # Set default font for document
            self._set_default_font(doc)
            
            # Add blank lines at top
            for _ in range(DOCUMENT_TOP_BLANK_LINES):
                doc.add_paragraph()
            
            # Add header
            self._add_header(doc, document_data)
            
            # Add separator line
            doc.add_paragraph("." * 50)
            
            # Add Wadi/Pratiwadi section
            self._add_wadi_pratiwadi(doc, document_data)
            
            # Add Mudda section
            self._add_mudda_section(doc, document_data)
            
            # Add Case Points
            self._add_case_points(doc, document_data)
            
            # Add Office Decision
            self._add_office_decision(doc, document_data)
            
            # Add Tapsil
            self._add_tapsil(doc, document_data)
            
            # Add Footer
            self._add_footer(doc, document_data)
            
            # Save document
            doc.save(str(output_path))
            return True
            
        except Exception as e:
            print(f"DOCX generation error: {e}")
            return False
    
    def _set_default_font(self, doc: Document) -> None:
        """Set default font for document."""
        style = doc.styles['Normal']
        font = style.font
        font.name = self.font_name
        font.size = Pt(12)
        
        # Set font for Nepali
        r = style.element
        rPr = r.get_or_add_rPr()
        rFonts = OxmlElement('w:rFonts')
        rFonts.set(qn('w:ascii'), self.font_name)
        rFonts.set(qn('w:hAnsi'), self.font_name)
        rFonts.set(qn('w:cs'), self.font_name)
        rPr.append(rFonts)
    
    def _add_header(self, doc: Document, data: Dict) -> None:
        """Add document header."""
        header_text = f"जिल्ला प्रशासन कार्यालय, {data.get('district', '')}का प्रमुख जिल्ला अधिकारी {data.get('cdo_name', '')} को इजालासबाट भएको फैसला"
        p = doc.add_paragraph(header_text)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    def _add_wadi_pratiwadi(self, doc: Document, data: Dict) -> None:
        """Add Wadi and Pratiwadi section."""
        # Create table for side-by-side layout
        table = doc.add_table(rows=1, cols=2)
        table.autofit = True
        
        # Wadi (left)
        wadi_cell = table.cell(0, 0)
        wadi_cell.text = f"वादी\n{data.get('wadi_content', '')}"
        
        # Pratiwadi (right)
        pratiwadi_cell = table.cell(0, 1)
        pratiwadi_cell.text = f"प्रतिवादी\n{data.get('pratiwadi_content', '')}"
    
    def _add_mudda_section(self, doc: Document, data: Dict) -> None:
        """Add Mudda section."""
        doc.add_paragraph(f"मुद्दा : {data.get('mudda', '')}")
        doc.add_paragraph(f"मु. द. नं. : {data.get('mudda_number', '')}")
    
    def _add_case_points(self, doc: Document, data: Dict) -> None:
        """Add case points section."""
        doc.add_paragraph("केसको संक्षिप्त व्यहोरा")
        
        case_points = data.get('case_points', [''])
        for i, point in enumerate(case_points, 1):
            nepali_num = self._to_nepali_number(i)
            doc.add_paragraph(f"{nepali_num}.\t{point}")
    
    def _add_office_decision(self, doc: Document, data: Dict) -> None:
        """Add office decision section."""
        doc.add_paragraph("कार्यालयको ठहर")
        
        decision = data.get('office_decision', '')
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(0.5)
        p.add_run(decision)
    
    def _add_tapsil(self, doc: Document, data: Dict) -> None:
        """Add tapsil section."""
        doc.add_paragraph("तपसिल")
        
        tapsil_points = data.get('tapsil_points', DEFAULT_TAPSIL_POINTS)
        for i, point in enumerate(tapsil_points, 1):
            nepali_num = self._to_nepali_number(i)
            dotted_text = self.dot_calculator.add_dots(point, nepali_num)
            doc.add_paragraph(dotted_text)
    
    def _add_footer(self, doc: Document, data: Dict) -> None:
        """Add document footer."""
        # Typist and CDO signature table
        table = doc.add_table(rows=3, cols=2)
        
        # Row 1: Typist name | Dots for signature
        table.cell(0, 0).text = f"टिपोट गर्ने ना.सु. {data.get('typist_name', '')}"
        table.cell(0, 1).text = "................................"
        
        # Row 2: Empty | CDO Name
        table.cell(1, 0).text = ""
        table.cell(1, 1).text = data.get('footer_cdo_name', data.get('cdo_name', ''))
        
        # Row 3: Empty | Designation
        table.cell(2, 0).text = ""
        table.cell(2, 1).text = "प्रमुख जिल्ला अधिकारी"
        
        # Date
        date_info = {
            'year': data.get('document_date_year', ''),
            'month': data.get('document_date_month', ''),
            'day': data.get('document_date_day', ''),
            'day_num': data.get('document_date_day_num', '')
        }
        
        month_name = ''
        if date_info['month'] and isinstance(date_info['month'], int):
            month_name = NEPALI_MONTHS[date_info['month'] - 1]
        elif date_info['month']:
            month_name = date_info['month']
        
        date_text = f"ईति सम्वत {date_info['year']} साल {month_name} {date_info['day']} गते रोज {date_info['day_num']} शुभम्"
        doc.add_paragraph(date_text)
    
    def _to_nepali_number(self, num: int) -> str:
        """Convert integer to Nepali number string."""
        from config.constants import NEPALI_NUMBERS
        return ''.join(NEPALI_NUMBERS.get(d, d) for d in str(num))