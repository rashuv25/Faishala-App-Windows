# -*- coding: utf-8 -*-
"""Calculate and add dots for tapsil formatting."""

from config.constants import TAPSIL_MIN_DOTS


class DotCalculator:
    """Calculates dots for tapsil line formatting."""
    
    def __init__(self, line_width: int = 80):
        """Initialize dot calculator."""
        self.line_width = line_width
        self.min_dots = TAPSIL_MIN_DOTS
    
    def add_dots(self, content: str, number: str) -> str:
        """Add dots between content and number to fill line."""
        content = content.strip()
        number = str(number).strip()
        
        # Calculate available space for dots
        content_length = len(content)
        number_length = len(number)
        available_space = self.line_width - content_length - number_length
        
        # Ensure minimum dots
        num_dots = max(available_space, self.min_dots)
        
        dots = '.' * num_dots
        
        return f"{content}{dots}{number}"
    
    def calculate_dots_count(self, content: str, number: str) -> int:
        """Calculate number of dots needed."""
        content_length = len(content.strip())
        number_length = len(str(number).strip())
        available_space = self.line_width - content_length - number_length
        return max(available_space, self.min_dots)