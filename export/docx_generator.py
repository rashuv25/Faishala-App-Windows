# -*- coding: utf-8 -*-
"""DOCX document generation."""

from pathlib import Path
from typing import Dict, Any

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
from utils.nepali_text import sanitize_document_data, sanitize_nepali_text


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
            cleaned_data = sanitize_document_data(document_data)

            # Set default font for document
            self._set_default_font(doc)

            # Add blank lines at top
            for _ in range(DOCUMENT_TOP_BLANK_LINES):
                doc.add_paragraph()

            # Add header
            self._add_header(doc, cleaned_data)

            # Add separator line
            sep = doc.add_paragraph()
            sep.alignment = WD_ALIGN_PARAGRAPH.CENTER
            self._add_text_run(sep, "." * 50, size=14)

            # Add Wadi/Pratiwadi section
            self._add_wadi_pratiwadi(doc, cleaned_data)

            # Add Mudda section
            self._add_mudda_section(doc, cleaned_data)

            # Add Case Points
            self._add_case_points(doc, cleaned_data)

            # Add Office Decision
            self._add_office_decision(doc, cleaned_data)

            # Add Tapsil
            self._add_tapsil(doc, cleaned_data)

            # Add Footer
            self._add_footer(doc, cleaned_data)

            # Save document
            doc.save(str(output_path))
            return True

        except Exception as e:
            print(f"DOCX generation error: {e}")
            return False

    def _set_default_font(self, doc: Document) -> None:
        """Set default font for document."""
        style = doc.styles["Normal"]
        font = style.font
        font.name = self.font_name
        font.size = Pt(14)

        r = style.element
        rPr = r.get_or_add_rPr()

        # Remove old font definitions if any
        for child in list(rPr):
            if child.tag == qn("w:rFonts"):
                rPr.remove(child)

        rFonts = OxmlElement("w:rFonts")
        rFonts.set(qn("w:ascii"), self.font_name)
        rFonts.set(qn("w:hAnsi"), self.font_name)
        rFonts.set(qn("w:cs"), self.font_name)
        rFonts.set(qn("w:eastAsia"), self.font_name)
        rPr.append(rFonts)

    def _apply_font_to_run(self, run, bold: bool = False, size: int = 14) -> None:
        """Apply export font to an individual run."""
        run.font.name = self.font_name
        run.font.size = Pt(size)
        run.bold = bold

        r = run._element
        rPr = r.get_or_add_rPr()

        for child in list(rPr):
            if child.tag == qn("w:rFonts"):
                rPr.remove(child)

        rFonts = OxmlElement("w:rFonts")
        rFonts.set(qn("w:ascii"), self.font_name)
        rFonts.set(qn("w:hAnsi"), self.font_name)
        rFonts.set(qn("w:cs"), self.font_name)
        rFonts.set(qn("w:eastAsia"), self.font_name)
        rPr.append(rFonts)

    def _add_text_run(self, paragraph, text: str, bold: bool = False, size: int = 14):
        """Add a sanitized text run to a paragraph."""
        run = paragraph.add_run(sanitize_nepali_text(text))
        self._apply_font_to_run(run, bold=bold, size=size)
        return run

    def _set_cell_margins(self, cell, top=80, start=80, bottom=80, end=80):
        """Set table cell margins."""
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()

        tcMar = None
        for child in tcPr:
            if child.tag == qn("w:tcMar"):
                tcMar = child
                break

        if tcMar is None:
            tcMar = OxmlElement("w:tcMar")
            tcPr.append(tcMar)

        for m, val in [("top", top), ("start", start), ("bottom", bottom), ("end", end)]:
            node = None
            for child in tcMar:
                if child.tag == qn(f"w:{m}"):
                    node = child
                    break
            if node is None:
                node = OxmlElement(f"w:{m}")
                tcMar.append(node)
            node.set(qn("w:w"), str(val))
            node.set(qn("w:type"), "dxa")

    def _add_header(self, doc: Document, data: Dict) -> None:
        """Add document header."""
        header_text_1 = (
            f"जिल्ला प्रशासन कार्यालय, {data.get('district', '')}का प्रमुख जिल्ला अधिकारी "
            f"{data.get('cdo_name', '')} को"
        )
        header_text_2 = "इजालासबाट भएको फैसला"

        p1 = doc.add_paragraph()
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        self._add_text_run(p1, header_text_1, bold=True, size=16)

        p2 = doc.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        self._add_text_run(p2, header_text_2, bold=True, size=16)

    def _add_wadi_pratiwadi(self, doc: Document, data: Dict) -> None:
        """Add Wadi and Pratiwadi section."""
        table = doc.add_table(rows=1, cols=2)
        table.autofit = True

        left_cell = table.cell(0, 0)
        right_cell = table.cell(0, 1)

        self._set_cell_margins(left_cell)
        self._set_cell_margins(right_cell)

        # Left side
        left_cell.text = ""
        p = left_cell.paragraphs[0]
        self._add_text_run(p, "वादी", bold=True, size=15)

        for line in str(data.get("wadi_content", "")).split("\n"):
            line = line.strip()
            if not line:
                continue
            lp = left_cell.add_paragraph()
            self._add_text_run(lp, line, size=14)

        # Right side
        right_cell.text = ""
        p = right_cell.paragraphs[0]
        self._add_text_run(p, "प्रतिवादी", bold=True, size=15)

        for line in str(data.get("pratiwadi_content", "")).split("\n"):
            line = line.strip()
            if not line:
                continue
            rp = right_cell.add_paragraph()
            self._add_text_run(rp, line, size=14)

    def _add_mudda_section(self, doc: Document, data: Dict) -> None:
        """Add Mudda section."""
        p1 = doc.add_paragraph()
        self._add_text_run(p1, "मुद्दा : ", bold=True, size=14)
        self._add_text_run(p1, data.get("mudda", ""), size=14)

        p2 = doc.add_paragraph()
        self._add_text_run(p2, "मु. द. नं. : ", bold=True, size=14)
        self._add_text_run(p2, data.get("mudda_number", ""), size=14)

    def _add_case_points(self, doc: Document, data: Dict) -> None:
        """Add case points section."""
        title = doc.add_paragraph()
        self._add_text_run(title, "केसको संक्षिप्त व्यहोरा", bold=True, size=15)

        case_points = data.get("case_points", [""])
        for i, point in enumerate(case_points, 1):
            nepali_num = self._to_nepali_number(i)
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.2)
            self._add_text_run(p, f"{nepali_num}. ", bold=True, size=14)
            self._add_text_run(p, point, size=14)

    def _add_office_decision(self, doc: Document, data: Dict) -> None:
        """Add office decision section."""
        title = doc.add_paragraph()
        self._add_text_run(title, "कार्यालयको ठहर", bold=True, size=15)

        decision = data.get("office_decision", "")
        for para in str(decision).split("\n"):
            para = para.strip()
            if not para:
                continue
            p = doc.add_paragraph()
            p.paragraph_format.first_line_indent = Inches(0.4)
            self._add_text_run(p, para, size=14)

    def _add_tapsil(self, doc: Document, data: Dict) -> None:
        """Add tapsil section."""
        title = doc.add_paragraph()
        self._add_text_run(title, "तपसिल", bold=True, size=15)

        tapsil_points = data.get("tapsil_points", DEFAULT_TAPSIL_POINTS)
        for i, point in enumerate(tapsil_points, 1):
            nepali_num = self._to_nepali_number(i)
            dotted_text = self.dot_calculator.add_dots(
                sanitize_nepali_text(point),
                nepali_num
            )
            p = doc.add_paragraph()
            self._add_text_run(p, dotted_text, size=14)

    def _add_footer(self, doc: Document, data: Dict) -> None:
        """Add document footer."""
        table = doc.add_table(rows=3, cols=2)
        table.autofit = True

        left_top = table.cell(0, 0)
        right_top = table.cell(0, 1)
        left_mid = table.cell(1, 0)
        right_mid = table.cell(1, 1)
        left_bot = table.cell(2, 0)
        right_bot = table.cell(2, 1)

        for cell in [left_top, right_top, left_mid, right_mid, left_bot, right_bot]:
            self._set_cell_margins(cell)

        left_top.text = ""
        p = left_top.paragraphs[0]
        self._add_text_run(p, f"टिपोट गर्ने ना.सु. {data.get('typist_name', '')}", size=14)

        right_top.text = ""
        p = right_top.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        self._add_text_run(p, "................................", size=14)

        left_mid.text = ""
        right_mid.text = ""
        p = right_mid.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        self._add_text_run(p, data.get("footer_cdo_name", data.get("cdo_name", "")), size=14)

        left_bot.text = ""
        right_bot.text = ""
        p = right_bot.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        self._add_text_run(p, "प्रमुख जिल्ला अधिकारी", size=14)

        date_info = {
            "year": data.get("document_date_year", ""),
            "month": data.get("document_date_month", ""),
            "day": data.get("document_date_day", ""),
            "day_num": data.get("document_date_day_num", "")
        }

        month_name = ""
        if isinstance(date_info["month"], int) and 1 <= date_info["month"] <= len(NEPALI_MONTHS):
            month_name = NEPALI_MONTHS[date_info["month"] - 1]
        elif date_info["month"]:
            month_name = date_info["month"]

        date_text = (
            f"ईति सम्वत {date_info['year']} साल {month_name} "
            f"{date_info['day']} गते रोज {date_info['day_num']} शुभम्"
        )

        p = doc.add_paragraph()
        self._add_text_run(p, date_text, size=14)

    def _to_nepali_number(self, num: int) -> str:
        """Convert integer to Nepali number string."""
        from config.constants import NEPALI_NUMBERS
        return "".join(NEPALI_NUMBERS.get(d, d) for d in str(num))