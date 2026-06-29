"""
report_generator.py  –  PDF Report Generator
=============================================
Produces a premium-formatted PDF diligence memorandum using ReportLab.
Designed to be inserted directly into an M&A due diligence report.

Sections
--------
1. Cover page (matter, company, date, risk score)
2. Executive Summary (one page)
3. Risk Score & Category
4. Heat Map Status Table
5. Issue-by-Issue Analysis (Issue / Regulation / Explanation / Why It Matters /
   Consequences / Documents / Management Questions / SPA Protections)
6. Due Diligence Document Request List
7. Disclaimer
"""

from __future__ import annotations

import io
from datetime import date
from typing import List

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    ListFlowable,
    ListItem,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

from config import APP_NAME, APP_TAGLINE, REGULATION_REFERENCE, COLORS
from models import AnalysisResult, DiligenceInput
from regulations_kb import REGULATIONS


# ─────────────────────────────────────────────────────────────────────────────
# COLOUR CONSTANTS  (ReportLab uses its own color objects)
# ─────────────────────────────────────────────────────────────────────────────

NAVY = colors.HexColor(COLORS["navy"])
NAVY_LIGHT = colors.HexColor(COLORS["navy_light"])
SLATE = colors.HexColor(COLORS["slate"])
GREY = colors.HexColor(COLORS["grey"])
GREY_LIGHT = colors.HexColor(COLORS["grey_light"])
GOLD = colors.HexColor(COLORS["gold"])
C_GREEN = colors.HexColor(COLORS["green"])
C_AMBER = colors.HexColor(COLORS["amber"])
C_RED = colors.HexColor(COLORS["red"])
WHITE = colors.white
BLACK = colors.black

_RISK_COLORS = {"green": C_GREEN, "amber": C_AMBER, "red": C_RED}
_STATUS_COLORS = {
    "green": colors.HexColor(COLORS["green_bg"]),
    "amber": colors.HexColor(COLORS["amber_bg"]),
    "red": colors.HexColor(COLORS["red_bg"]),
}


# ─────────────────────────────────────────────────────────────────────────────
# STYLE SHEET
# ─────────────────────────────────────────────────────────────────────────────

def _make_styles() -> dict:
    base = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "cover_title", fontName="Helvetica-Bold", fontSize=24,
            textColor=WHITE, spaceAfter=6, alignment=TA_LEFT,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub", fontName="Helvetica", fontSize=11,
            textColor=colors.HexColor("#B0BEC5"), spaceAfter=4, alignment=TA_LEFT,
        ),
        "cover_meta": ParagraphStyle(
            "cover_meta", fontName="Helvetica", fontSize=9,
            textColor=colors.HexColor("#90A4AE"), alignment=TA_LEFT,
        ),
        "h1": ParagraphStyle(
            "h1", fontName="Helvetica-Bold", fontSize=14,
            textColor=NAVY, spaceBefore=16, spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "h2", fontName="Helvetica-Bold", fontSize=11,
            textColor=NAVY_LIGHT, spaceBefore=12, spaceAfter=4,
        ),
        "h3": ParagraphStyle(
            "h3", fontName="Helvetica-Bold", fontSize=9,
            textColor=SLATE, spaceBefore=8, spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "body", fontName="Helvetica", fontSize=9,
            textColor=SLATE, spaceAfter=4, leading=14,
        ),
        "bullet": ParagraphStyle(
            "bullet", fontName="Helvetica", fontSize=9,
            textColor=SLATE, spaceAfter=2, leading=13,
            leftIndent=12, firstLineIndent=0,
        ),
        "label": ParagraphStyle(
            "label", fontName="Helvetica-Bold", fontSize=8,
            textColor=GREY, spaceAfter=2, letterSpacing=0.5,
        ),
        "caption": ParagraphStyle(
            "caption", fontName="Helvetica-Oblique", fontSize=8,
            textColor=GREY, spaceAfter=4,
        ),
        "footer": ParagraphStyle(
            "footer", fontName="Helvetica", fontSize=7,
            textColor=GREY, alignment=TA_CENTER,
        ),
    }


# ─────────────────────────────────────────────────────────────────────────────
# PAGE TEMPLATES
# ─────────────────────────────────────────────────────────────────────────────

class _FooterCanvas:
    """Mixin so every page gets a rule + footer line."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _draw_footer(self, doc, is_cover: bool = False):
        self.saveState()
        w, h = A4
        # Bottom rule
        self.setStrokeColor(GREY_LIGHT)
        self.setLineWidth(0.5)
        self.line(2 * cm, 1.6 * cm, w - 2 * cm, 1.6 * cm)
        # Footer text
        self.setFont("Helvetica", 7)
        self.setFillColor(GREY)
        if not is_cover:
            self.drawString(2 * cm, 1.2 * cm,
                f"{APP_NAME}  |  PRIVILEGED & CONFIDENTIAL — FOR M&A DUE DILIGENCE USE ONLY")
            self.drawRightString(w - 2 * cm, 1.2 * cm, f"Page {doc.page}")
        else:
            self.drawString(2 * cm, 1.2 * cm,
                "PRIVILEGED & CONFIDENTIAL — FOR M&A DUE DILIGENCE USE ONLY")
        self.restoreState()


def _header_footer(canvas, doc):
    """Called by ReportLab for every page after the cover."""
    w, h = A4
    canvas.saveState()

    # Top rule
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(1.5)
    canvas.line(2 * cm, h - 1.5 * cm, w - 2 * cm, h - 1.5 * cm)

    # App name top-left
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(NAVY)
    canvas.drawString(2 * cm, h - 1.2 * cm, APP_NAME.upper())

    # Page number top-right
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GREY)
    canvas.drawRightString(w - 2 * cm, h - 1.2 * cm, f"Page {doc.page}")

    # Bottom rule + footer
    canvas.setStrokeColor(GREY_LIGHT)
    canvas.setLineWidth(0.5)
    canvas.line(2 * cm, 1.6 * cm, w - 2 * cm, 1.6 * cm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GREY)
    canvas.drawString(2 * cm, 1.2 * cm,
        "PRIVILEGED & CONFIDENTIAL — FOR M&A DUE DILIGENCE USE ONLY")
    canvas.restoreState()


def _cover_template(canvas, doc):
    """Cover page: full navy background."""
    w, h = A4
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    # Gold accent bar
    canvas.setFillColor(GOLD)
    canvas.rect(0, h - 0.8 * cm, w, 0.8 * cm, fill=1, stroke=0)
    # Bottom footer
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#607D8B"))
    canvas.drawString(2 * cm, 1.2 * cm,
        "PRIVILEGED & CONFIDENTIAL — FOR M&A DUE DILIGENCE USE ONLY")
    canvas.restoreState()


# ─────────────────────────────────────────────────────────────────────────────
# BUILDING BLOCKS
# ─────────────────────────────────────────────────────────────────────────────

def _bullet_list(items: List[str], S: dict) -> ListFlowable:
    return ListFlowable(
        [ListItem(Paragraph(item, S["bullet"]), bulletColor=NAVY, leftIndent=16)
         for item in items],
        bulletType="bullet", leftIndent=4,
    )


def _rule(color=GREY_LIGHT, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=8)


def _section_header(text: str, S: dict):
    return [Paragraph(text.upper(), S["label"]), _rule(GREY_LIGHT, 0.5)]


def _risk_badge_table(label: str, color_key: str, score: int, S: dict) -> Table:
    """A small coloured badge showing Risk Category and score."""
    clr = _RISK_COLORS.get(color_key, C_RED)
    data = [[
        Paragraph(f"<b>{score}/100</b>", ParagraphStyle(
            "badge_score", fontName="Helvetica-Bold", fontSize=22,
            textColor=WHITE, alignment=TA_CENTER)),
        Paragraph(f"<b>{label}</b>", ParagraphStyle(
            "badge_label", fontName="Helvetica-Bold", fontSize=13,
            textColor=WHITE, alignment=TA_LEFT)),
    ]]
    t = Table(data, colWidths=[3 * cm, 8 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), clr),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return t


def _heatmap_table(heatmap: dict, S: dict) -> Table:
    header = [
        Paragraph("WORKSTREAM", S["label"]),
        Paragraph("STATUS", S["label"]),
        Paragraph("SCORE", S["label"]),
    ]
    rows = [header]
    for cat, info in heatmap.items():
        status = info["status"]
        pts = info["points"]
        label_text = status.upper()
        bg = _STATUS_COLORS.get(status, colors.white)
        fg = _RISK_COLORS.get(status, BLACK)
        rows.append([
            Paragraph(cat, S["body"]),
            Paragraph(f"<b>{label_text}</b>", ParagraphStyle(
                "hm_status", fontName="Helvetica-Bold", fontSize=9,
                textColor=fg, alignment=TA_CENTER)),
            Paragraph(str(pts), ParagraphStyle(
                "hm_pts", fontName="Helvetica-Bold", fontSize=9,
                textColor=SLATE, alignment=TA_CENTER)),
        ])

    col_w = [9 * cm, 3.5 * cm, 2.5 * cm]
    t = Table(rows, colWidths=col_w, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, colors.HexColor("#F7F8FA")]),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]
    # Colour status cells
    for row_idx, (cat, info) in enumerate(heatmap.items(), start=1):
        bg = _STATUS_COLORS.get(info["status"], WHITE)
        style.append(("BACKGROUND", (1, row_idx), (1, row_idx), bg))
    t.setStyle(TableStyle(style))
    return t


def _issue_block(issue, S: dict) -> list:
    """Return a list of flowables for a single RiskIssue."""
    severity_colors = {
        "Critical": C_RED, "High": C_AMBER,
        "Medium": NAVY_LIGHT, "Low": SLATE, "Informational": GREY,
    }
    clr = severity_colors.get(issue.severity, SLATE)

    reg_text = "; ".join(
        f"{REGULATIONS[r].number}" for r in issue.regulations if r in REGULATIONS
    )

    flows = []
    # Issue title bar
    title_data = [[
        Paragraph(f"<b>{issue.title}</b>", ParagraphStyle(
            "issue_title", fontName="Helvetica-Bold", fontSize=10,
            textColor=WHITE)),
        Paragraph(f"<b>{issue.severity.upper()}</b>", ParagraphStyle(
            "issue_sev", fontName="Helvetica-Bold", fontSize=8,
            textColor=WHITE, alignment=TA_RIGHT)),
    ]]
    t = Table(title_data, colWidths=[13 * cm, 3 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), clr),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, 0), 10),
        ("RIGHTPADDING", (-1, 0), (-1, 0), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    flows.append(t)

    # Regulation badge + transaction impact
    meta_data = [[
        Paragraph(f"<b>Regulations:</b> {reg_text}", S["caption"]),
        Paragraph(f"<b>Transaction Impact:</b> {issue.transaction_impact_label}",
                  ParagraphStyle("ti", fontName="Helvetica-Bold", fontSize=8,
                                 textColor=clr, alignment=TA_RIGHT)),
    ]]
    mt = Table(meta_data, colWidths=[9 * cm, 7 * cm])
    mt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F7F8FA")),
        ("LEFTPADDING", (0, 0), (0, 0), 10),
        ("RIGHTPADDING", (-1, 0), (-1, 0), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, GREY_LIGHT),
    ]))
    flows.append(mt)

    # Explanation
    flows.append(Spacer(1, 4))
    flows.append(Paragraph(issue.explanation, S["body"]))

    # Why It Matters
    flows.append(Paragraph("WHY THIS MATTERS IN M&A", S["label"]))
    flows.append(_bullet_list(issue.why_it_matters, S))

    # Potential Consequences
    flows.append(Paragraph("POTENTIAL CONSEQUENCES", S["label"]))
    flows.append(_bullet_list(issue.potential_consequences, S))

    # Documents
    flows.append(Paragraph("DOCUMENTS TO REQUEST", S["label"]))
    flows.append(_bullet_list(issue.documents_to_review, S))

    # Management Questions
    flows.append(Paragraph("MANAGEMENT QUESTIONS", S["label"]))
    flows.append(_bullet_list(issue.management_questions, S))

    # SPA Protections
    flows.append(Paragraph("RECOMMENDED SPA PROTECTIONS", S["label"]))
    flows.append(_bullet_list(issue.spa_protections, S))

    flows.append(Spacer(1, 12))
    flows.append(_rule())
    return flows


# ─────────────────────────────────────────────────────────────────────────────
# DILIGENCE DOCUMENT CHECKLIST
# ─────────────────────────────────────────────────────────────────────────────

_STANDARD_DOCS = [
    # Export
    "Export invoices (last 3 financial years)",
    "Shipping bills / EDF copies (EDI and non-EDI port exports)",
    "EDPMS extract as at the latest practicable date",
    "Invoice-wise ageing analysis of export receivables",
    "AD Bank extension approvals for delayed realisation",
    "Write-off / reduction approvals from the AD Bank",
    "Set-off agreement documentation",
    # Import
    "Import contracts / purchase orders (last 3 financial years)",
    "Bills of entry and import invoices",
    "IDPMS extract as at the latest practicable date",
    "Ageing analysis of import payables cross-referenced to contract terms",
    "AD Bank extension approvals for delayed import payments",
    # Advance payments
    "Advance import payment records with corresponding realisation / repatriation evidence",
    "Gold / silver import contracts and payment records",
    # MTT
    "Merchanting Trade Transaction register",
    "Commercial invoices, bills of lading, and contracts for all MTT transactions",
    "AD Bank approvals for third-party MTT flows and timing extensions",
    # Reporting
    "Complete EDPMS and IDPMS extracts (all outstanding entries)",
    "FETERS reporting confirmations for the last 3 years",
    "AD Bank correspondence (compliance queries, extensions, approvals) — last 3 years",
    # Approvals
    "Board resolutions authorising export / import activities and banking arrangements",
    "Any RBI compounding orders or correspondence",
    "Any RBI / FEMA Show Cause Notices",
]


def _checklist_section(result: AnalysisResult, S: dict) -> list:
    """Compile standard + issue-specific document requests."""
    flows = [Paragraph("DUE DILIGENCE DOCUMENT REQUEST LIST", S["h1"]), _rule(NAVY, 1)]

    # Aggregate all issue-specific document requests (deduplicated)
    issue_docs: list[str] = []
    seen = set()
    for issue in result.scored_issues:
        for doc in issue.documents_to_review:
            if doc not in seen:
                seen.add(doc)
                issue_docs.append(doc)

    flows.append(Paragraph("Issue-Specific Document Requests", S["h2"]))
    flows.append(_bullet_list(issue_docs or ["No additional issue-specific documents flagged."], S))
    flows.append(Spacer(1, 8))
    flows.append(Paragraph("Standard FEMA Export-Import Diligence Documents", S["h2"]))
    flows.append(_bullet_list(_STANDARD_DOCS, S))
    return flows


# ─────────────────────────────────────────────────────────────────────────────
# EXECUTIVE SUMMARY
# ─────────────────────────────────────────────────────────────────────────────

def _executive_summary(data: DiligenceInput, result: AnalysisResult, S: dict) -> list:
    flows = [Paragraph("EXECUTIVE SUMMARY", S["h1"]), _rule(NAVY, 1)]

    # Overall
    flows.append(Paragraph("Overall FEMA Risk Assessment", S["h2"]))
    flows.append(_risk_badge_table(result.risk_category, result.risk_color_key,
                                   result.total_score, S))
    flows.append(Spacer(1, 12))

    # Key findings
    flows.append(Paragraph("Key Findings", S["h2"]))
    company = data.company_name or "The Target"
    roles = [r for r, flag in [
        ("goods exporter", data.exporter),
        ("importer", data.importer),
        ("software exporter", data.software_exporter),
        ("service exporter", data.service_exporter),
        ("merchanting trader", data.merchanting_trader),
    ] if flag]
    role_str = ", ".join(roles) if roles else "cross-border trader"
    flows.append(Paragraph(
        f"{company} is a {role_str} with annual turnover of "
        f"₹{data.annual_turnover_cr:.1f} crore (export: "
        f"₹{data.export_turnover_cr:.1f} crore; import: "
        f"₹{data.import_turnover_cr:.1f} crore). "
        f"The FEMA diligence review has identified <b>{len(result.scored_issues)}</b> "
        f"compliance issue(s) contributing to a total risk score of "
        f"<b>{result.total_score}/100</b> ({result.risk_category}).",
        S["body"]
    ))
    flows.append(Spacer(1, 8))

    # Top concerns
    top = result.scored_issues[:5]
    if top:
        flows.append(Paragraph("Critical Issues / Top Concerns", S["h2"]))
        for i, issue in enumerate(top, 1):
            flows.append(Paragraph(
                f"{i}. <b>{issue.title}</b> — {issue.severity} Risk "
                f"({issue.score_points} pts) | Impact: {issue.transaction_impact_label}",
                S["bullet"]
            ))
        flows.append(Spacer(1, 8))

    # Recommended actions
    flows.append(Paragraph("Recommended Actions", S["h2"]))
    action_items = [
        "Obtain and review full EDPMS and IDPMS extracts before completion.",
        "Request invoice-wise ageing of export receivables and import payables.",
        "Confirm AD Bank extension status for all overdue entries.",
        "Request copies of all compounding applications and RBI correspondence.",
        "Conduct focused management Q&A session on identified issues.",
        "Instruct FEMA specialist counsel to advise on compounding exposure quantification.",
    ]
    flows.append(_bullet_list(action_items, S))
    flows.append(Spacer(1, 8))

    # Transaction concerns
    flows.append(Paragraph("Potential Transaction Concerns", S["h2"]))
    concerns = []
    for issue in result.scored_issues:
        concerns.append(
            f"{issue.title}: {issue.transaction_impact_label} — "
            f"{issue.transaction_impact_detail[:120]}..."
        )
    if concerns:
        flows.append(_bullet_list(concerns, S))
    else:
        flows.append(Paragraph("No material transaction concerns identified.", S["body"]))

    return flows


# ─────────────────────────────────────────────────────────────────────────────
# MAIN EXPORT FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

def generate_pdf(data: DiligenceInput, result: AnalysisResult) -> bytes:
    """
    Generate a complete PDF diligence memorandum and return the bytes.
    Caller can stream these bytes to st.download_button().
    """
    buf = io.BytesIO()
    S = _make_styles()

    doc = BaseDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
        title=f"{APP_NAME} — {data.company_name}",
        author=APP_NAME,
    )

    # Two page templates: cover (full navy) and body (with header/footer)
    cover_frame = Frame(0, 0, A4[0], A4[1], leftPadding=2*cm,
                        rightPadding=2*cm, topPadding=3*cm, bottomPadding=3*cm)
    body_frame = Frame(
        2 * cm, 2 * cm,
        A4[0] - 4 * cm, A4[1] - 4.5 * cm,
    )
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=_cover_template),
        PageTemplate(id="body", frames=[body_frame], onPage=_header_footer),
    ])

    story = []

    # ── COVER ─────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 4 * cm))
    story.append(Paragraph(APP_NAME.upper(), S["cover_title"]))
    story.append(Paragraph(APP_TAGLINE, S["cover_sub"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(HRFlowable(width="60%", thickness=1, color=GOLD, spaceAfter=12))
    story.append(Paragraph(f"Target Company: <b>{data.company_name or 'Undisclosed'}</b>",
                            S["cover_sub"]))
    story.append(Paragraph(f"Industry: {data.industry or 'Not specified'}", S["cover_sub"]))
    story.append(Paragraph(f"Review Date: {date.today().strftime('%d %B %Y')}", S["cover_sub"]))
    story.append(Spacer(1, 1.5 * cm))

    # Risk score on cover
    risk_clr_hex = COLORS.get(result.risk_color_key, COLORS["red"])
    score_label = (
        f"<font color='{risk_clr_hex}'><b>{result.total_score}/100 — "
        f"{result.risk_category}</b></font>"
    )
    story.append(Paragraph(f"Overall FEMA Risk: {score_label}", S["cover_sub"]))
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph(
        "This memorandum is prepared for internal use by the M&A diligence team. "
        "It is privileged and confidential and does not constitute legal advice.",
        S["cover_meta"]
    ))

    # Switch to body template
    story.append(PageBreak())
    from reportlab.platypus import NextPageTemplate
    story.insert(story.index(story[-1]), NextPageTemplate("body"))

    # ── EXECUTIVE SUMMARY ─────────────────────────────────────────────────────
    story.extend(_executive_summary(data, result, S))
    story.append(PageBreak())

    # ── HEAT MAP ──────────────────────────────────────────────────────────────
    story.append(Paragraph("COMPLIANCE HEAT MAP", S["h1"]))
    story.append(_rule(NAVY, 1))
    story.append(Paragraph(
        "The table below shows the aggregate risk score and traffic-light "
        "status for each of the eight FEMA compliance workstreams assessed "
        "in this review.", S["body"]
    ))
    story.append(Spacer(1, 8))
    story.append(_heatmap_table(result.heatmap, S))
    story.append(Spacer(1, 20))

    # ── APPLICABLE REGULATIONS ─────────────────────────────────────────────
    story.append(Paragraph("APPLICABLE REGULATIONS", S["h1"]))
    story.append(_rule(NAVY, 1))
    seen_regs = set()
    for issue in result.issues:
        for r in issue.regulations:
            seen_regs.add(r)
    reg_items = []
    for key in sorted(seen_regs):
        reg = REGULATIONS.get(key)
        if reg:
            reg_items.append(f"<b>{reg.number} — {reg.title}:</b> {reg.summary}")
    if reg_items:
        story.append(_bullet_list(reg_items, S))
    story.append(PageBreak())

    # ── ISSUE ANALYSIS ────────────────────────────────────────────────────────
    story.append(Paragraph("DETAILED ISSUE ANALYSIS", S["h1"]))
    story.append(_rule(NAVY, 1))
    if result.scored_issues:
        for issue in result.scored_issues:
            story.extend(_issue_block(issue, S))
    else:
        story.append(Paragraph("No material FEMA issues identified based on the "
                               "information provided.", S["body"]))
    story.append(PageBreak())

    # ── DOCUMENT CHECKLIST ────────────────────────────────────────────────────
    story.extend(_checklist_section(result, S))
    story.append(PageBreak())

    # ── DISCLAIMER ────────────────────────────────────────────────────────────
    story.append(Paragraph("DISCLAIMER", S["h1"]))
    story.append(_rule(NAVY, 1))
    story.append(Paragraph(
        "This report has been generated by the FEMA Diligence Analyzer, an internal "
        "M&A knowledge tool, based solely on the information provided in the intake "
        "form. It is intended to assist qualified lawyers in identifying areas for "
        "further investigation and does not constitute legal advice. The findings "
        "in this report are based on information provided by the user and have not "
        "been independently verified. This report should not be relied upon as a "
        "complete or authoritative statement of the target's FEMA compliance profile. "
        "Qualified legal counsel should review the underlying documents and advise "
        "on the specific facts of the transaction.",
        S["body"]
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        f"Regulatory Reference: {REGULATION_REFERENCE}",
        S["caption"]
    ))

    doc.build(story)
    return buf.getvalue()
