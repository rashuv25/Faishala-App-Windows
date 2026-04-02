# -*- coding: utf-8 -*-
"""PDF document generation.

On Linux we use WeasyPrint (HTML -> PDF).
On Windows we use docx2pdf (Word -> PDF) because WeasyPrint native dependencies
are not always available.
"""

from pathlib import Path
from typing import Dict, Any, List
import platform
import tempfile
import html

from PIL import ImageFont
from config.settings import Settings
from config.constants import DEFAULT_TAPSIL_POINTS, NEPALI_MONTHS
from utils.nepali_text import sanitize_document_data
from export.docx_generator import DocxGenerator


class PdfGenerator:
    """Generates PDF documents."""

    def __init__(self):
        """Initialize PDF generator."""
        self.font_path = Settings.EXPORT_FONT_PATH

        if not self.font_path.exists():
            raise FileNotFoundError(
                f"Required PDF font not found: {self.font_path}"
            )

    def generate(self, document_data: Dict[str, Any], output_path: Path) -> bool:
        """Generate PDF file."""
        output_path = Path(output_path)

        try:
            if platform.system() == "Windows":
                return self._generate_pdf_with_docx2pdf(document_data, output_path)
            return self._generate_pdf_with_weasyprint(document_data, output_path)
        except Exception as e:
            print(f"PDF generation error: {e}")
            return False

    def _generate_pdf_with_docx2pdf(self, document_data: Dict[str, Any], output_path: Path) -> bool:
        """Generate PDF on Windows using DOCX -> PDF conversion (Word)."""
        try:
            from docx2pdf import convert
        except Exception as e:
            print(f"docx2pdf import error: {e}")
            return False

        tmp_dir = Path(tempfile.gettempdir()) / "mudda_phaisala_export"
        tmp_dir.mkdir(parents=True, exist_ok=True)
        tmp_docx_path = tmp_dir / f"{output_path.stem}.docx"

        try:
            # 1) Generate DOCX first (same template logic as DOCX export)
            docx_generator = DocxGenerator()
            if not docx_generator.generate(document_data, tmp_docx_path):
                return False

            # 2) Convert to PDF using Word (client PC must have Word installed)
            convert(str(tmp_docx_path), str(output_path.parent))

            return output_path.exists()
        finally:
            try:
                tmp_docx_path.unlink(missing_ok=True)
            except Exception:
                pass

    def _generate_pdf_with_weasyprint(self, document_data: Dict[str, Any], output_path: Path) -> bool:
        """Generate PDF on non-Windows using WeasyPrint (HTML -> PDF)."""
        try:
            import importlib

            # Use dynamic import so PyInstaller doesn't try to import weasyprint
            # at build time on systems where native deps are missing.
            weasyprint = importlib.import_module("weasyprint")
            HTML = weasyprint.HTML
            CSS = weasyprint.CSS
        except Exception as e:
            print(f"WeasyPrint import error: {e}")
            return False

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

    def _build_html(self, data: Dict[str, Any]) -> str:
        """Build full HTML document."""
        district = self._escape(data.get("district", ""))
        cdo_name = self._escape(data.get("cdo_name", ""))

        header_line_1 = (
            f'जिल्ला प्रशासन कार्यालय, {district}का प्रमुख जिल्ला अधिकारी '
            f'<span class="cdo-name">{cdo_name}</span> को'
        )

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
            <div class="header-line header-line-1">{header_line_1}</div>
            <div class="header-line header-line-2">
                <span class="header-title">इजालासबाट भएको फैसला</span>
                <span class="header-dots"></span>
            </div>
        </div>

        <div class="party-wrap">
            <div class="party-block party-left">
                <div class="section-heading">वादी</div>
                <div class="party-content">{wadi_html}</div>
            </div>

            <div class="party-block party-right">
                <div class="section-heading">प्रतिवादी</div>
                <div class="party-content">{pratiwadi_html}</div>
            </div>
        </div>

        <div class="label-line centered-label-line">
            <span class="label">मुद्दा :</span> <span class="value">{mudda}</span>
        </div>
        <div class="label-line centered-label-line">
            <span class="label">मु. द. नं. :</span> <span class="value">{mudda_number}</span>
        </div>

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

        <div class="footer-gap"></div>

        <div class="footer">
            <div class="footer-left">
                <div>टिपोट गर्ने ना.सु. {footer_typist}</div>
            </div>

            <div class="footer-right">
                <div class="sign-line">................................</div>
                <div class="footer-cdo-name">{footer_cdo}</div>
                <div class="footer-cdo-title">प्रमुख जिल्ला अधिकारी</div>
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
        """Build HTML for tapsil section with proper trailing dots and point numbers."""
        if not tapsil_points:
            tapsil_points = DEFAULT_TAPSIL_POINTS

        items = []
        for i, point in enumerate(tapsil_points, 1):
            nep_num = self._to_nepali_number(i)
            items.append(
                self._build_single_tapsil_point_html(str(point or ""), nep_num)
            )
        return "\n".join(items)

    def _measure_text_width(self, text: str, font_size_pt: float = 14.0) -> float:
        """Measure rendered text width in pixels using the export font."""
        if not text:
            return 0.0

        px_size = max(1, int(round(font_size_pt * 96 / 72)))  # pt -> px
        font = ImageFont.truetype(str(self.font_path), px_size)
        return float(font.getlength(text))

    def _wrap_text_to_width(
        self,
        text: str,
        max_width_px: float,
        font_size_pt: float = 14.0
    ) -> List[str]:
        """Wrap text into lines according to rendered font width."""
        text = " ".join(str(text).split())
        if not text:
            return [""]

        words = text.split(" ")
        lines: List[str] = []
        current = words[0]

        for word in words[1:]:
            trial = current + " " + word
            if self._measure_text_width(trial, font_size_pt) <= max_width_px:
                current = trial
            else:
                lines.append(current)
                current = word

        lines.append(current)
        return lines

    def _build_single_tapsil_point_html(self, point_text: str, point_num: str) -> str:
        """Build one tapsil point so that only the last line gets dots + number."""
        point_text = " ".join(str(point_text).split())

        # A4 width = 21cm
        # Page margins = left 2.5cm, right 0.8cm => usable = 17.7cm
        # tapsil-list padding-left = 0.85cm => inner usable approx = 16.85cm
        total_width_px = (16.85 / 2.54) * 96

        font_size_pt = 14.0
        num_width = self._measure_text_width(point_num, font_size_pt)
        dot_width = max(self._measure_text_width(".", font_size_pt), 1.0)
        gap_width = self._measure_text_width("  ", font_size_pt)
        min_dots_width = dot_width * 10

        normal_line_width = total_width_px
        final_line_text_width = max(
            120.0,
            total_width_px - num_width - min_dots_width - gap_width
        )

        lines = self._wrap_text_to_width(point_text, normal_line_width, font_size_pt)

        # Ensure final line has room for dots + number
        while lines and self._measure_text_width(lines[-1], font_size_pt) > final_line_text_width:
            last_words = lines[-1].split()
            if len(last_words) <= 1:
                break

            moved_word = last_words.pop()
            lines[-1] = " ".join(last_words).strip()

            if len(lines) == 1:
                lines.append(moved_word)
            else:
                lines.append(moved_word)

        lines = [ln for ln in lines if ln.strip()]
        if not lines:
            lines = [""]

        final_text = lines[-1]
        final_text_width = self._measure_text_width(final_text, font_size_pt)

        remaining_width = total_width_px - final_text_width - num_width - gap_width
        dot_count = max(6, int(remaining_width / dot_width))
        dots = "." * dot_count

        body_lines = []
        for line in lines[:-1]:
            body_lines.append(
                f'<div class="tapsil-subline">{self._escape(line)}</div>'
            )

        body_lines.append(
            f'''
            <div class="tapsil-final-line">
                <span class="tapsil-final-text">{self._escape(final_text)}</span>
                <span class="tapsil-final-dots">{self._escape(dots)}</span>
                <span class="tapsil-final-num">{self._escape(point_num)}</span>
            </div>
            '''
        )

        return f'<div class="tapsil-item">{"".join(body_lines)}</div>'

    def _build_date_text(self, data: Dict[str, Any]) -> str:
        """Build date text."""
        year = self._to_nepali_number(data.get("document_date_year", ""))
        month = data.get("document_date_month", "")
        day = self._to_nepali_number(data.get("document_date_day", ""))
        day_num = self._to_nepali_number(data.get("document_date_day_num", ""))

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

    def _to_nepali_number(self, num: Any) -> str:
        """Convert integer/string to Nepali digits."""
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
    margin: 2cm 0.8cm 2cm 2.5cm;
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
    margin-top: 0.8cm;
    margin-bottom: 0.7cm;
}}

.header-line {{
    font-size: 13pt;
    line-height: 1.45;
}}

.header-line-1 {{
    text-align: left;
    padding-left: 1cm;
    margin-bottom: 0.12cm;
}}

.cdo-name {{
    font-weight: 700;
}}

.header-line-2 {{
    display: flex;
    align-items: baseline;
    gap: 0.15cm;
    padding-left: 1cm;
}}

.header-title {{
    font-weight: 700;
    white-space: nowrap;
}}

.header-dots {{
    flex: 1;
    border-bottom: 2px dotted #111111;
    transform: translateY(-0.08cm);
}}

.party-wrap {{
    display: flex;
    width: 100%;
    gap: 1.2cm;
    margin-bottom: 0.7cm;
    align-items: flex-start;
}}

.party-block {{
    min-width: 0;
}}

.party-left {{
    flex: 0 0 42%;
    max-width: 42%;
}}

.party-right {{
    flex: 0 0 52%;
    max-width: 52%;
    margin-left: auto;
}}

.section-heading {{
    font-size: 16pt;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.18cm;
}}

.party-content {{
    font-size: 14pt;
    line-height: 1.75;
    text-align: justify;
    word-break: break-word;
    overflow-wrap: anywhere;
}}

.party-left .party-content {{
    padding-right: 0.15cm;
}}

.party-right .party-content {{
    padding-left: 0.25cm;
    padding-right: 0;
}}

.line {{
    margin-bottom: 0.08cm;
}}

.label-line {{
    font-size: 15pt;
    margin-bottom: 0.28cm;
}}

.centered-label-line {{
    text-align: center;
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
    margin-bottom: 0.28cm;
}}

.case-points {{
    margin-bottom: 0.42cm;
}}

.case-point {{
    display: table;
    width: 100%;
    margin-bottom: 0.18cm;
}}

.case-num {{
    display: table-cell;
    width: 1.2cm;
    vertical-align: top;
}}

.case-text {{
    display: table-cell;
    vertical-align: top;
    text-align: justify;
    padding-left: 0.45cm;
}}

.office-decision {{
    margin-bottom: 0.45cm;
}}

.decision-para {{
    text-indent: 1.2cm;
    margin: 0 0 0.18cm 1cm;
    text-align: justify;
}}

.tapsil-list {{
    margin-bottom: 0;
    padding-left: 0.85cm;
}}

.tapsil-item {{
    margin-bottom: 0.18cm;
    font-size: 14pt;
    line-height: 1.9;
}}

.tapsil-subline {{
    display: block;
    text-align: left;
}}

.tapsil-final-line {{
    display: flex;
    align-items: baseline;
    white-space: nowrap;
}}

.tapsil-final-text {{
    flex: 0 0 auto;
    white-space: nowrap;
}}

.tapsil-final-dots {{
    flex: 1 1 auto;
    overflow: hidden;
    white-space: nowrap;
    margin-left: 0.08cm;
    margin-right: 0.08cm;
    letter-spacing: 0.01em;
}}

.tapsil-final-num {{
    flex: 0 0 auto;
    white-space: nowrap;
}}

.footer-gap {{
    height: 1cm;
}}

.footer {{
    width: 100%;
    display: table;
    margin-top: 0;
}}

.footer-left {{
    display: table-cell;
    width: 45%;
    vertical-align: top;
    font-size: 14pt;
}}

.footer-right {{
    display: table-cell;
    width: 55%;
    vertical-align: top;
    text-align: right;
    font-size: 14pt;
}}

.sign-line {{
    margin-bottom: 0;
    line-height: 1.1;
}}

.footer-cdo-name {{
    margin-top: 0.05cm;
    margin-bottom: 0.02cm;
    line-height: 1.1;
}}

.footer-cdo-title {{
    margin-top: 0;
    line-height: 1.1;
}}

.date-line {{
    margin-top: 0.7cm;
    font-size: 14pt;
}}
"""