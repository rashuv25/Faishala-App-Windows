# -*- coding: utf-8 -*-
"""PDF document generation using WeasyPrint (HTML -> PDF)."""

from pathlib import Path
from typing import Dict, Any, List
import html

from weasyprint import HTML, CSS
from config.settings import Settings
from config.constants import DEFAULT_TAPSIL_POINTS, NEPALI_MONTHS
from utils.nepali_text import sanitize_document_data


class PdfGenerator:
    """Generates PDF documents using WeasyPrint with embedded fonts."""

    def __init__(self):
        """Initialize PDF generator."""
        self.font_path = Settings.EXPORT_FONT_PATH

        if not self.font_path.exists():
            raise FileNotFoundError(
                f"Required PDF font not found: {self.font_path}"
            )

    def generate(self, document_data: Dict[str, Any], output_path: Path) -> bool:
        """Generate PDF file directly from HTML."""
        try:
            output_path = Path(output_path)
            cleaned_data = sanitize_document_data(document_data)

            html_content = self._build_html(cleaned_data)
            css_content = self._build_css()

            HTML(
                string=html_content,
                base_url=str(Settings.BASE_DIR)
            ).write_pdf(
                str(output_path),
                stylesheets=[CSS(string=css_content)]
            )

            return True

        except Exception as e:
            print(f"PDF generation error: {e}")
            return False

    def _build_html(self, data: Dict[str, Any]) -> str:
        """Build full HTML document."""
        district = self._escape(data.get("district", ""))
        cdo_name = self._escape(data.get("cdo_name", ""))

        header_line_1 = f"जिल्ला प्रशासन कार्यालय, {district}का प्रमुख जिल्ला अधिकारी {cdo_name} को"
        header_line_2 = "इजालासबाट भएको फैसला"

        wadi_html = self._paragraph_lines(data.get("wadi_content", ""))
        pratiwadi_html = self._paragraph_lines(data.get("pratiwadi_content", ""))

        mudda = self._escape(data.get("mudda", ""))
        mudda_number = self._escape(data.get("mudda_number", ""))

        case_points_html = self._build_case_points_html(data.get("case_points", [""]))
        office_decision_html = self._build_office_decision_html(data.get("office_decision", ""))
        tapsil_html = self._build_tapsil_html(data.get("tapsil_points", DEFAULT_TAPSIL_POINTS))

        footer_typist = self._escape(data.get("typist_name", ""))
        footer_cdo = self._escape(data.get("footer_cdo_name", data.get("cdo_name", "")))
        date_text = self._build_date_text(data)

        return f"""<!DOCTYPE html>
<html lang="ne">
<head>
    <meta charset="utf-8">
    <title>मुद्दा फैसला</title>
</head>
<body>
    <div class="page">

        <div class="header">
            <div class="header-line">{header_line_1}</div>
            <div class="header-line">{header_line_2}</div>
        </div>

        <div class="separator">............................................</div>

        <table class="party-table">
            <tr>
                <td class="party-col">
                    <div class="section-heading">वादी</div>
                    <div class="party-content">{wadi_html}</div>
                </td>
                <td class="party-col">
                    <div class="section-heading">प्रतिवादी</div>
                    <div class="party-content">{pratiwadi_html}</div>
                </td>
            </tr>
        </table>

        <div class="label-line"><span class="label">मुद्दा :</span> <span class="value">{mudda}</span></div>
        <div class="label-line"><span class="label">मु. द. नं. :</span> <span class="value">{mudda_number}</span></div>

        <div class="section-title">केसको संक्षिप्त व्यहोरा</div>
        <div class="case-points">
            {case_points_html}
        </div>

        <div class="section-title">कार्यालयको ठहर</div>
        <div class="office-decision">
            {office_decision_html}
        </div>

        <div class="section-title">तपसिल</div>
        <div class="tapsil-list">
            {tapsil_html}
        </div>

        <div class="footer">
            <div class="footer-left">
                <div>टिपोट गर्ने ना.सु. {footer_typist}</div>
            </div>

            <div class="footer-right">
                <div>................................</div>
                <div class="footer-cdo-name">{footer_cdo}</div>
                <div>प्रमुख जिल्ला अधिकारी</div>
            </div>
        </div>

        <div class="date-line">{date_text}</div>

    </div>
</body>
</html>
"""

    def _build_case_points_html(self, points: List[str]) -> str:
        """Build HTML for case points."""
        if not points:
            points = [""]

        items = []
        for i, point in enumerate(points, 1):
            nep_num = self._to_nepali_number(i)
            point = self._escape(point or "")
            items.append(
                f"""
                <div class="case-point">
                    <div class="case-num">{nep_num}.</div>
                    <div class="case-text">{point}</div>
                </div>
                """
            )
        return "\n".join(items)

    def _build_office_decision_html(self, decision: str) -> str:
        """Build HTML for office decision paragraphs."""
        if not decision:
            return '<p class="decision-para"></p>'

        paras = []
        for para in str(decision).split("\n"):
            para = para.strip()
            if para:
                paras.append(f'<p class="decision-para">{self._escape(para)}</p>')
        return "\n".join(paras) if paras else '<p class="decision-para"></p>'

    def _build_tapsil_html(self, tapsil_points: List[str]) -> str:
        """Build HTML for tapsil section."""
        if not tapsil_points:
            tapsil_points = DEFAULT_TAPSIL_POINTS

        items = []
        for i, point in enumerate(tapsil_points, 1):
            nep_num = self._to_nepali_number(i)
            point = self._escape(point or "")
            items.append(
                f"""
                <div class="tapsil-item">
                    <div class="tapsil-text">{point}</div>
                    <div class="tapsil-num">...{nep_num}</div>
                </div>
                """
            )
        return "\n".join(items)

    def _build_date_text(self, data: Dict[str, Any]) -> str:
        """Build date text."""
        year = self._escape(data.get("document_date_year", ""))
        month = data.get("document_date_month", "")
        day = self._escape(data.get("document_date_day", ""))
        day_num = self._escape(data.get("document_date_day_num", ""))

        month_name = ""
        if isinstance(month, int) and 1 <= month <= len(NEPALI_MONTHS):
            month_name = NEPALI_MONTHS[month - 1]
        elif month:
            month_name = str(month)

        month_name = self._escape(month_name)
        return f"ईति सम्वत {year} साल {month_name} {day} गते रोज {day_num} शुभम्"

    def _paragraph_lines(self, text: str) -> str:
        """Convert multi-line text into HTML paragraphs."""
        if not text:
            return ""

        lines = []
        for line in str(text).split("\n"):
            line = line.strip()
            if line:
                lines.append(f'<div class="line">{self._escape(line)}</div>')
        return "\n".join(lines)

    def _escape(self, value: Any) -> str:
        """Escape HTML safely."""
        return html.escape("" if value is None else str(value))

    def _to_nepali_number(self, num: int) -> str:
        """Convert integer to Nepali digits."""
        from config.constants import NEPALI_NUMBERS
        return "".join(NEPALI_NUMBERS.get(ch, ch) for ch in str(num))

    def _build_css(self) -> str:
        """Build CSS for PDF."""
        font_url = self.font_path.resolve().as_uri()

        return f"""
@font-face {{
    font-family: "MuddaPdfFont";
    src: url("{font_url}");
}}

@page {{
    size: A4;
    margin: 2cm 2.2cm 2cm 2.2cm;
}}

body {{
    font-family: "MuddaPdfFont", "Noto Sans Devanagari", sans-serif;
    font-size: 14pt;
    line-height: 1.75;
    color: #111111;
    font-kerning: normal;
}}

.page {{
    width: 100%;
}}

.header {{
    text-align: center;
    margin-top: 0.8cm;
    margin-bottom: 1cm;
}}

.header-line {{
    font-size: 17pt;
    font-weight: 700;
    line-height: 1.6;
}}

.separator {{
    text-align: center;
    font-size: 15pt;
    margin-bottom: 1cm;
}}

.party-table {{
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
    margin-bottom: 0.8cm;
}}

.party-col {{
    width: 50%;
    vertical-align: top;
    padding-right: 1.2cm;
}}

.party-col:last-child {{
    padding-right: 0;
    padding-left: 0.6cm;
}}

.section-heading {{
    font-size: 16pt;
    font-weight: 700;
    margin-bottom: 0.2cm;
}}

.party-content {{
    font-size: 14pt;
    line-height: 1.8;
}}

.line {{
    margin-bottom: 0.08cm;
}}

.label-line {{
    font-size: 15pt;
    margin-bottom: 0.35cm;
}}

.label {{
    font-weight: 700;
}}

.value {{
    font-weight: 400;
}}

.section-title {{
    font-size: 16pt;
    font-weight: 700;
    margin-top: 0.55cm;
    margin-bottom: 0.35cm;
}}

.case-points {{
    margin-bottom: 0.45cm;
}}

.case-point {{
    display: table;
    width: 100%;
    margin-bottom: 0.2cm;
}}

.case-num {{
    display: table-cell;
    width: 1cm;
    vertical-align: top;
    font-weight: 700;
}}

.case-text {{
    display: table-cell;
    vertical-align: top;
    text-align: justify;
}}

.office-decision {{
    margin-bottom: 0.45cm;
}}

.decision-para {{
    text-indent: 1cm;
    margin: 0 0 0.2cm 0;
    text-align: justify;
}}

.tapsil-list {{
    margin-bottom: 0.7cm;
}}

.tapsil-item {{
    display: table;
    width: 100%;
    margin-bottom: 0.18cm;
}}

.tapsil-text {{
    display: table-cell;
    vertical-align: top;
    text-align: justify;
    padding-right: 0.4cm;
}}

.tapsil-num {{
    display: table-cell;
    width: 1.8cm;
    text-align: right;
    vertical-align: top;
    font-weight: 700;
}}

.footer {{
    width: 100%;
    margin-top: 1cm;
    display: table;
}}

.footer-left {{
    display: table-cell;
    width: 50%;
    vertical-align: top;
    font-size: 14pt;
}}

.footer-right {{
    display: table-cell;
    width: 50%;
    vertical-align: top;
    text-align: right;
    font-size: 14pt;
}}

.footer-cdo-name {{
    margin-top: 0.15cm;
    margin-bottom: 0.1cm;
}}

.date-line {{
    margin-top: 0.9cm;
    font-size: 14pt;
}}
"""