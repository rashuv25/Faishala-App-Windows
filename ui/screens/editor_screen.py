# -*- coding: utf-8 -*-
"""Document editor screen UI."""

import customtkinter as ctk
from ui.components.scrollable_frame import ScrollableFrame
from typing import Callable, Dict, Any

from ui.theme import AppTheme
from ui.editor.field_district import DistrictField
from ui.editor.field_cdo_name import CDONameField
from ui.editor.field_wadi_pratiwadi import WadiPratiwadiField
from ui.editor.field_mudda import MuddaField
from ui.editor.field_case_points import CasePointsField
from ui.editor.field_office_decision import OfficeDecisionField
from ui.editor.field_tapsil import TapsilField
from ui.editor.field_footer import FooterField
from ui.editor.field_date import DateField

from core.document_manager import DocumentManager
from core.template_engine import TemplateEngine
from core.auto_save import AutoSaveManager
from core.undo_redo import UndoRedoManager
from export.docx_generator import DocxGenerator
from export.pdf_generator import PdfGenerator
from utils.file_handler import FileHandler


class EditorScreen(ctk.CTkFrame):
    """Document editor screen."""

    def __init__(
        self,
        parent,
        document_id: int,
        on_back: Callable
    ):
        """Initialize editor screen."""
        super().__init__(parent, fg_color=AppTheme.BACKGROUND_COLOR)

        self.document_id = document_id
        self.on_back = on_back

        self.doc_manager = DocumentManager()
        self.template_engine = TemplateEngine()
        self.docx_generator = DocxGenerator()
        self.pdf_generator = PdfGenerator()

        self.auto_save = AutoSaveManager(document_id, self._on_auto_save)
        self.undo_redo = UndoRedoManager()

        self.document_data: Dict[str, Any] = {}
        self.cdo_name_linked = True
        self._save_indicator_after_id = None

        self._load_document()
        self._create_widgets()
        self._bind_shortcuts()

    def _load_document(self):
        """Load document data."""
        doc = self.doc_manager.get_document(self.document_id)

        if doc:
            self.document_data = doc
            self.document_name = doc.get("document_name", "Untitled")
        else:
            self.document_data = self.template_engine.get_empty_template()
            self.document_name = "New Document"

    def _create_widgets(self):
        """Create editor widgets."""
        self._create_top_bar()

        # Scrollable content area
        self.scroll_frame = ScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        # Main editor card
        self.editor_card = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=AppTheme.CARD_COLOR,
            corner_radius=12,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR
        )
        self.editor_card.pack(fill="x", padx=8, pady=(4, 16))

        self._create_document_content()
        self._create_bottom_bar()

    def _create_top_bar(self):
        """Create top bar with back button and document name."""
        top_bar = ctk.CTkFrame(
            self,
            fg_color=AppTheme.CARD_COLOR,
            height=64,
            corner_radius=12,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR
        )
        top_bar.pack(fill="x", padx=20, pady=(16, 12))
        top_bar.pack_propagate(False)

        left = ctk.CTkFrame(top_bar, fg_color="transparent")
        left.pack(side="left", fill="y", padx=14)

        back_btn = ctk.CTkButton(
            left,
            text="← पछाडि",
            width=92,
            height=38,
            font=AppTheme.get_font("normal"),
            fg_color=AppTheme.BACKGROUND_COLOR,
            hover_color=AppTheme.HOVER_LIGHT,
            text_color=AppTheme.TEXT_PRIMARY,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR,
            corner_radius=AppTheme.BORDER_RADIUS,
            command=self._handle_back
        )
        back_btn.pack(side="left", pady=12)

        name_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        name_frame.pack(side="left", fill="both", expand=True, padx=(8, 10))

        title_row = ctk.CTkFrame(name_frame, fg_color="transparent")
        title_row.pack(anchor="w", pady=(10, 0))

        doc_icon = ctk.CTkLabel(
            title_row,
            text="📄",
            font=("Arial", 18)
        )
        doc_icon.pack(side="left", padx=(0, 6))

        self.name_label = ctk.CTkLabel(
            title_row,
            text=self.document_name,
            font=AppTheme.get_font("large", bold=True),
            text_color=AppTheme.TEXT_PRIMARY
        )
        self.name_label.pack(side="left")

        rename_btn = ctk.CTkButton(
            title_row,
            text="✏️",
            width=32,
            height=30,
            fg_color="transparent",
            hover_color=AppTheme.HOVER_LIGHT,
            text_color=AppTheme.TEXT_PRIMARY,
            corner_radius=6,
            command=self._handle_rename
        )
        rename_btn.pack(side="left", padx=(6, 0))

        subtitle = ctk.CTkLabel(
            name_frame,
            text="Auto-save enabled • Ctrl+S save • Ctrl+Z undo • Ctrl+Y redo",
            font=AppTheme.get_font("small"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        subtitle.pack(anchor="w", pady=(2, 8))

        right = ctk.CTkFrame(top_bar, fg_color="transparent")
        right.pack(side="right", padx=16)

        self.save_indicator = ctk.CTkLabel(
            right,
            text="✓ Auto-saved",
            font=AppTheme.get_font("small"),
            text_color=AppTheme.SUCCESS_COLOR
        )
        self.save_indicator.pack(pady=20)

    def _create_document_content(self):
        """Create document content fields."""
        content = self.editor_card

        inner = ctk.CTkFrame(content, fg_color="transparent")
        inner.pack(fill="x", padx=22, pady=22)

        # Header area
        header_frame = ctk.CTkFrame(inner, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 18))

        header_line = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_line.pack(fill="x")

        header_start = ctk.CTkLabel(
            header_line,
            text="जिल्ला प्रशासन कार्यालय,",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        header_start.pack(side="left", pady=4)

        self.district_field = DistrictField(
            header_line,
            default_value=self.document_data.get("district", "मोरङ"),
            on_change=lambda v: self._on_field_change("district", v)
        )
        self.district_field.pack(side="left", padx=6)

        header_mid = ctk.CTkLabel(
            header_line,
            text="का प्रमुख जिल्ला अधिकारी",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        header_mid.pack(side="left", pady=4)

        self.cdo_name_field = CDONameField(
            header_line,
            default_value=self.document_data.get("cdo_name", ""),
            on_change=self._on_cdo_name_change
        )
        self.cdo_name_field.pack(side="left", padx=6)

        header_end = ctk.CTkLabel(
            header_line,
            text="को इजालासबाट भएको फैसला",
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        header_end.pack(side="left", pady=4)

        separator = ctk.CTkLabel(
            inner,
            text="." * 70,
            font=AppTheme.get_font("normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        separator.pack(pady=(6, 14))

        # Sections
        self.wadi_pratiwadi_field = WadiPratiwadiField(
            inner,
            wadi_value=self.document_data.get("wadi_content", ""),
            pratiwadi_value=self.document_data.get("pratiwadi_content", ""),
            on_wadi_change=lambda v: self._on_field_change("wadi_content", v),
            on_pratiwadi_change=lambda v: self._on_field_change("pratiwadi_content", v)
        )
        self.wadi_pratiwadi_field.pack(fill="x", pady=(0, 16))

        self.mudda_field = MuddaField(
            inner,
            mudda_value=self.document_data.get("mudda", ""),
            mudda_number_value=self.document_data.get("mudda_number", ""),
            on_mudda_change=lambda v: self._on_field_change("mudda", v),
            on_number_change=lambda v: self._on_field_change("mudda_number", v)
        )
        self.mudda_field.pack(fill="x", pady=(0, 16))

        self.case_points_field = CasePointsField(
            inner,
            points=self.document_data.get("case_points", [""]),
            on_change=lambda v: self._on_field_change("case_points", v)
        )
        self.case_points_field.pack(fill="x", pady=(0, 16))

        self.office_decision_field = OfficeDecisionField(
            inner,
            value=self.document_data.get("office_decision", ""),
            on_change=lambda v: self._on_field_change("office_decision", v)
        )
        self.office_decision_field.pack(fill="x", pady=(0, 16))

        self.tapsil_field = TapsilField(
            inner,
            points=self.document_data.get("tapsil_points", []),
            on_change=lambda v: self._on_field_change("tapsil_points", v)
        )
        self.tapsil_field.pack(fill="x", pady=(0, 16))

        self.footer_field = FooterField(
            inner,
            typist_name=self.document_data.get("typist_name", ""),
            cdo_name=self.document_data.get("footer_cdo_name", "") or self.document_data.get("cdo_name", ""),
            on_typist_change=lambda v: self._on_field_change("typist_name", v),
            on_cdo_change=self._on_footer_cdo_change
        )
        self.footer_field.pack(fill="x", pady=(0, 16))

        self.date_field = DateField(
            inner,
            year=self.document_data.get("document_date_year"),
            month=self.document_data.get("document_date_month"),
            day=self.document_data.get("document_date_day"),
            day_num=self.document_data.get("document_date_day_num"),
            on_change=self._on_date_change
        )
        self.date_field.pack(fill="x", pady=(0, 6))

    def _create_bottom_bar(self):
        """Create bottom bar with action buttons."""
        bottom_bar = ctk.CTkFrame(
            self,
            fg_color=AppTheme.CARD_COLOR,
            height=68,
            corner_radius=12,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR
        )
        bottom_bar.pack(fill="x", padx=20, pady=(0, 16))
        bottom_bar.pack_propagate(False)

        left = ctk.CTkFrame(bottom_bar, fg_color="transparent")
        left.pack(side="left", padx=14, pady=12)

        info_label = ctk.CTkLabel(
            left,
            text="Final output will be correct in exported DOCX/PDF.",
            font=AppTheme.get_font("small"),
            text_color=AppTheme.TEXT_SECONDARY
        )
        info_label.pack(anchor="w")

        right = ctk.CTkFrame(bottom_bar, fg_color="transparent")
        right.pack(side="right", padx=14, pady=12)

        docx_btn = ctk.CTkButton(
            right,
            text="📄 Export DOCX",
            width=145,
            height=40,
            font=AppTheme.get_font("normal", bold=True),
            fg_color=AppTheme.PRIMARY_COLOR,
            hover_color=AppTheme.SECONDARY_COLOR,
            text_color=AppTheme.TEXT_LIGHT,
            corner_radius=AppTheme.BORDER_RADIUS,
            command=self._export_docx
        )
        docx_btn.pack(side="left", padx=(0, 8))

        pdf_btn = ctk.CTkButton(
            right,
            text="📑 Export PDF",
            width=145,
            height=40,
            font=AppTheme.get_font("normal", bold=True),
            fg_color=AppTheme.PRIMARY_COLOR,
            hover_color=AppTheme.SECONDARY_COLOR,
            text_color=AppTheme.TEXT_LIGHT,
            corner_radius=AppTheme.BORDER_RADIUS,
            command=self._export_pdf
        )
        pdf_btn.pack(side="left", padx=(0, 8))

        save_btn = ctk.CTkButton(
            right,
            text="💾 Save & Close",
            width=150,
            height=40,
            font=AppTheme.get_font("normal", bold=True),
            fg_color=AppTheme.BACKGROUND_COLOR,
            hover_color=AppTheme.HOVER_LIGHT,
            text_color=AppTheme.TEXT_PRIMARY,
            border_width=1,
            border_color=AppTheme.BORDER_COLOR,
            corner_radius=AppTheme.BORDER_RADIUS,
            command=self._save_and_close
        )
        save_btn.pack(side="left")

    def _bind_shortcuts(self):
        """Bind keyboard shortcuts."""
        root = self.winfo_toplevel()

        try:
            root.unbind("<Control-z>")
            root.unbind("<Control-y>")
            root.unbind("<Control-s>")
        except Exception:
            pass

        root.bind("<Control-z>", lambda e: self._undo())
        root.bind("<Control-y>", lambda e: self._redo())
        root.bind("<Control-s>", lambda e: self._save_document())

    def _on_field_change(self, field_name: str, value: Any):
        """Handle field value change."""
        self.document_data[field_name] = value
        self.auto_save.on_change(field_name, value)
        self.undo_redo.save_state(field_name, value)
        self._update_save_indicator("saving")

    def _on_cdo_name_change(self, value: str):
        """Handle CDO name change."""
        self.document_data["cdo_name"] = value

        if self.cdo_name_linked:
            self.document_data["footer_cdo_name"] = value
            self.footer_field.set_cdo_name(value)

        self.auto_save.on_change("cdo_name", value)
        self._update_save_indicator("saving")

    def _on_footer_cdo_change(self, value: str):
        """Handle footer CDO name change."""
        self.document_data["footer_cdo_name"] = value

        if value != self.document_data.get("cdo_name", ""):
            self.cdo_name_linked = False

        self.auto_save.on_change("footer_cdo_name", value)
        self._update_save_indicator("saving")

    def _on_date_change(self, year: int, month: int, day: int, day_num: int):
        """Handle date change."""
        self.document_data["document_date_year"] = year
        self.document_data["document_date_month"] = month
        self.document_data["document_date_day"] = day
        self.document_data["document_date_day_num"] = day_num

        self.auto_save.on_change("document_date", {
            "year": year,
            "month": month,
            "day": day,
            "day_num": day_num
        })
        self._update_save_indicator("saving")

    def _on_auto_save(self, state: Dict):
        """Called when auto-save completes."""
        self._save_to_database()
        self._update_save_indicator("saved")

    def _update_save_indicator(self, state="saved"):
        """Update save indicator safely."""
        if self._save_indicator_after_id:
            try:
                self.after_cancel(self._save_indicator_after_id)
            except Exception:
                pass
            self._save_indicator_after_id = None

        if state == "saving":
            self.save_indicator.configure(
                text="💾 Saving...",
                text_color=AppTheme.WARNING_COLOR
            )
            self._save_indicator_after_id = self.after(700, lambda: self._update_save_indicator("saved"))
        elif state == "exported":
            self.save_indicator.configure(
                text="✓ Export complete",
                text_color=AppTheme.SUCCESS_COLOR
            )
            self._save_indicator_after_id = self.after(1800, lambda: self._update_save_indicator("saved"))
        else:
            self.save_indicator.configure(
                text="✓ Auto-saved",
                text_color=AppTheme.SUCCESS_COLOR
            )

    def _save_document(self):
        """Save document to database."""
        self._save_to_database()
        self._update_save_indicator("saved")
        return "break"

    def _save_to_database(self):
        """Save current state to database."""
        self.doc_manager.save_document(self.document_id, self.document_data)

    def _handle_back(self):
        """Handle back button."""
        self._save_to_database()
        self._unbind_shortcuts()
        self.on_back()

    def _unbind_shortcuts(self):
        """Unbind keyboard shortcuts when leaving editor."""
        root = self.winfo_toplevel()
        try:
            root.unbind("<Control-z>")
            root.unbind("<Control-y>")
            root.unbind("<Control-s>")
        except Exception:
            pass

    def _handle_rename(self):
        """Handle rename document."""
        from ui.components.popup import RenamePopup

        RenamePopup(
            self,
            current_name=self.document_name,
            on_rename=self._do_rename
        )

    def _do_rename(self, new_name: str):
        """Perform rename."""
        self.document_name = new_name
        self.name_label.configure(text=new_name)
        self.doc_manager.rename_document(self.document_id, new_name)

    def _undo(self):
        """Undo last action."""
        state = self.undo_redo.undo()
        if state:
            self._apply_state(state)
        return "break"

    def _redo(self):
        """Redo last undone action."""
        state = self.undo_redo.redo()
        if state:
            self._apply_state(state)
        return "break"

    def _apply_state(self, state):
        """Apply state snapshot to fields."""
        # Future improvement: sync specific widgets with undo/redo state
        pass

    def _export_docx(self):
        """Export document as DOCX."""
        self._save_to_database()

        file_path = FileHandler.get_save_path(self.document_name, "docx")
        if file_path:
            success = self.docx_generator.generate(self.document_data, file_path)
            if success:
                self._show_export_success("DOCX")

    def _export_pdf(self):
        """Export document as PDF."""
        self._save_to_database()

        file_path = FileHandler.get_save_path(self.document_name, "pdf")
        if file_path:
            success = self.pdf_generator.generate(self.document_data, file_path)
            if success:
                self._show_export_success("PDF")

    def _show_export_success(self, format_type: str):
        """Show export success state."""
        self.save_indicator.configure(
            text=f"✓ {format_type} exported",
            text_color=AppTheme.SUCCESS_COLOR
        )
        self._update_save_indicator("exported")

    def _save_and_close(self):
        """Save and close editor."""
        self._save_to_database()
        self._unbind_shortcuts()
        self.on_back()