# -*- coding: utf-8 -*-
"""Template processing engine."""

from typing import Dict, Any
from config.constants import (
    DEFAULT_OFFICE_DECISION,
    DEFAULT_TAPSIL_POINTS,
    DOCUMENT_TOP_BLANK_LINES,
    TAB_SPACES
)
from config.settings import Settings


class TemplateEngine:
    """Processes document templates."""
    
    def __init__(self):
        """Initialize template engine."""
        self.default_district = Settings.DEFAULT_DISTRICT
    
    def get_empty_template(self) -> Dict[str, Any]:
        """Get empty template structure with defaults."""
        return {
            'district': self.default_district,
            'cdo_name': '',
            'wadi_content': '',
            'pratiwadi_content': '',
            'mudda': '',
            'mudda_number': '',
            'case_points': [''],  # One empty point by default
            'office_decision': DEFAULT_OFFICE_DECISION,
            'tapsil_points': DEFAULT_TAPSIL_POINTS.copy(),
            'typist_name': '',
            'footer_cdo_name': '',  # Auto-linked to cdo_name
            'document_date_year': None,
            'document_date_month': None,
            'document_date_day': None,
            'document_date_day_num': None
        }
    
    def generate_header(self, district: str, cdo_name: str) -> str:
        """Generate document header text."""
        blank_lines = '\n' * DOCUMENT_TOP_BLANK_LINES
        header = f"{blank_lines}जिल्ला प्रशासन कार्यालय, {district}का प्रमुख जिल्ला अधिकारी {cdo_name} को इजालासबाट भएको फैसला"
        return header
    
    def generate_footer(self, typist_name: str, cdo_name: str, date_info: Dict) -> str:
        """Generate document footer text."""
        from config.constants import NEPALI_MONTHS
        
        month_name = NEPALI_MONTHS[date_info['month'] - 1] if date_info['month'] else ''
        
        footer = f"""
टिपोट गर्ने ना.सु. {typist_name}\t\t\t\t................................
\t\t\t\t\t\t\t{cdo_name}
\t\t\t\t\t\t\tप्रमुख जिल्ला अधिकारी

ईति सम्वत {date_info['year']} साल {month_name} {date_info['day']} गते रोज {date_info['day_num']} शुभम्
"""
        return footer
    
    def add_indentation(self, text: str) -> str:
        """Add indentation to text."""
        indent = ' ' * TAB_SPACES
        lines = text.split('\n')
        indented_lines = [indent + line if line.strip() else line for line in lines]
        return '\n'.join(indented_lines)