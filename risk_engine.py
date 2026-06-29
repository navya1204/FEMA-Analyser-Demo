"""
risk_engine.py  –  FEMA Diligence Scoring Engine
==================================================
Takes a DiligenceInput and produces a fully-populated AnalysisResult.

Design principles
-----------------
* One function per issue family (export, import, advance, MTT, reporting).
* Each function returns a list[RiskIssue]—zero issues if nothing triggered.
* The orchestrator `analyse()` calls all families, sums scores (capped at
  MAX_SCORE), assembles the heat map, and returns the AnalysisResult.
* All scoring weights and risk thresholds live in config.py so a partner
  can recalibrate without touching this file.
"""

from __future__ import annotations

from typing import List

from config import (
    RISK_WEIGHTS,
    MAX_SCORE,
    HEATMAP_CATEGORIES,
    get_risk_category,
    get_heatmap_status,
    get_transaction_impact,
    issue_points_to_severity,
)
from content_library import ISSUE_LIBRARY
from models import DiligenceInput, RiskIssue, AnalysisResult


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _severity_label(points: int) -> str:
    """Map score contribution to a display severity label."""
    if points == 0:
        return "Informational"
    if points <= 10:
        return "Low"
    if points <= 15:
        return "Medium"
    if points <= 20:
        return "High"
    return "Critical"


def _build_issue(issue_id: str, fmt_kwargs: dict | None = None) -> RiskIssue:
    """
    Build a RiskIssue from the content library entry for `issue_id`.

    `fmt_kwargs` is passed to str.format() on the explanation template so
    runtime data (amounts, delay months, etc.) can be interpolated.
    """
    tmpl = ISSUE_LIBRARY[issue_id]
    weight_key = tmpl.get("weight_key")
    points = RISK_WEIGHTS.get(weight_key, 0) if weight_key else 0
    severity = _severity_label(points)

    explanation = tmpl["explanation"]
    if fmt_kwargs:
        try:
            explanation = explanation.format(**fmt_kwargs)
        except (KeyError, ValueError):
            pass  # Leave un-interpolated placeholder in place rather than crash

    severity_score = issue_points_to_severity(points)
    impact_label, impact_detail = get_transaction_impact(severity_score)

    return RiskIssue(
        issue_id=issue_id,
        title=tmpl["title"],
        severity=severity,
        score_points=points,
        regulations=tmpl["regulations"],
        heatmap_categories=tmpl["heatmap_categories"],
        explanation=explanation,
        why_it_matters=tmpl["why_it_matters"],
        potential_consequences=tmpl["potential_consequences"],
        documents_to_review=tmpl["documents_to_review"],
        management_questions=tmpl["management_questions"],
        spa_protections=tmpl["spa_protections"],
        transaction_impact_label=impact_label,
        transaction_impact_detail=impact_detail,
    )


# ─────────────────────────────────────────────────────────────────────────────
# ISSUE FAMILIES
# ─────────────────────────────────────────────────────────────────────────────

def _export_issues(d: DiligenceInput) -> List[RiskIssue]:
    issues: List[RiskIssue] = []

    if not (d.exporter or d.software_exporter or d.service_exporter):
        return issues

    # --- Outstanding receivables / Reg 5 breach ---
    if d.outstanding_export_receivables and not d.export_proceeds_realised_within_fema_timelines:
        ext_note = (
            "AD Bank extension has been obtained for this delay."
            if d.ad_extensions_obtained
            else "No AD Bank extension appears to have been obtained for this delay."
        )
        issues.append(_build_issue("export_realisation_delay", {
            "amount_outstanding_cr": d.amount_outstanding_cr,
            "num_invoices": d.num_invoices_outstanding,
            "max_delay": d.max_delay_months,
            "extension_note": ext_note,
        }))

        # --- Reg 13 trigger: > 12 months beyond due date ---
        # The permissible period is 15 months + any extension.  We flag
        # Regulation 13 risk if the maximum delay is more than 27 months
        # from shipment (15 months base + 12 months of "unrealised" window).
        if d.max_delay_months and d.max_delay_months > 27:
            issues.append(_build_issue("unrealised_export_reg13", {
                "max_delay": d.max_delay_months,
            }))

    # --- Export value reduced / written off ---
    if d.export_value_reduced_written_off:
        issues.append(_build_issue("export_value_reduction_writeoff"))

    # --- Set-off arrangements ---
    if d.set_off_arrangements_used:
        issues.append(_build_issue("set_off_arrangement"))

    # --- Third-party receipts ---
    if d.third_party_receipts:
        issues.append(_build_issue("third_party_receipts_export"))

    # --- Advance export receipts ---
    if d.advance_export_receipts:
        issues.append(_build_issue("advance_export_receipt_routing"))

    # --- Warehouse exports ---
    if d.warehouse_exports:
        issues.append(_build_issue("warehouse_export_timeline"))

    # --- INR-invoiced exports (informational) ---
    if d.exports_invoiced_in_inr:
        issues.append(_build_issue("exports_invoiced_in_inr"))

    # --- Project exports (informational) ---
    if d.project_exports:
        issues.append(_build_issue("project_exports"))

    return issues


def _import_issues(d: DiligenceInput) -> List[RiskIssue]:
    issues: List[RiskIssue] = []

    if not d.importer:
        return issues

    # --- Outstanding import payables beyond contract period ---
    if d.outstanding_import_payables:
        issues.append(_build_issue("import_payment_delay", {
            "import_max_delay": d.import_max_delay_months,
        }))

    # --- Gold / silver imports with advance remittance ---
    if d.gold_silver_imports and d.advance_import_payments:
        issues.append(_build_issue("gold_silver_advance_breach"))

    # --- Third-party payments for imports ---
    if d.third_party_payments:
        issues.append(_build_issue("third_party_payments_import"))

    # --- Reduced value settlements ---
    if d.reduced_value_settlements:
        issues.append(_build_issue("reduced_value_settlement_import"))

    return issues


def _advance_issues(d: DiligenceInput) -> List[RiskIssue]:
    issues: List[RiskIssue] = []

    # --- Advance import: import not materialised and not repatriated ---
    if d.advance_import_payments and d.imports_not_materialised and not d.advance_payments_repatriated:
        issues.append(_build_issue("advance_import_not_materialised"))

    return issues


def _mtt_issues(d: DiligenceInput) -> List[RiskIssue]:
    issues: List[RiskIssue] = []

    if not d.merchanting_trade_conducted:
        return issues

    # --- Timing breach: both legs not completed within 6 months ---
    if not d.both_legs_completed or not d.within_six_months:
        issues.append(_build_issue("merchanting_timing_breach"))

    # --- Third-party flows ---
    if d.mtt_third_party:
        issues.append(_build_issue("merchanting_third_party"))

    # --- Documentation gaps ---
    if not d.mtt_supporting_documents_available:
        issues.append(_build_issue("merchanting_documentation"))

    return issues


def _reporting_issues(d: DiligenceInput) -> List[RiskIssue]:
    issues: List[RiskIssue] = []

    if not d.edpms_reconciled:
        issues.append(_build_issue("edpms_unreconciled"))

    if not d.idpms_reconciled:
        issues.append(_build_issue("idpms_unreconciled"))

    if d.outstanding_entries:
        issues.append(_build_issue("outstanding_entries"))

    if d.missing_edfs:
        issues.append(_build_issue("missing_edfs"))

    if not d.supporting_documentation_available:
        issues.append(_build_issue("missing_supporting_documentation"))

    if d.ad_bank_queries_pending:
        issues.append(_build_issue("ad_bank_queries_pending"))

    return issues


# ─────────────────────────────────────────────────────────────────────────────
# HEAT MAP BUILDER
# ─────────────────────────────────────────────────────────────────────────────

def _build_heatmap(issues: List[RiskIssue]) -> dict:
    """
    Aggregate issue score-points by heatmap category and return a dict of
    { category: { "points": int, "status": "green"|"amber"|"red" } }
    """
    totals: dict[str, int] = {cat: 0 for cat in HEATMAP_CATEGORIES}

    for issue in issues:
        for cat in issue.heatmap_categories:
            if cat in totals:
                totals[cat] += issue.score_points

    return {
        cat: {"points": pts, "status": get_heatmap_status(pts)}
        for cat, pts in totals.items()
    }


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def analyse(data: DiligenceInput) -> AnalysisResult:
    """
    Run all issue-family functions, sum scores, build the heat map, and
    return a fully-populated AnalysisResult.
    """
    all_issues: List[RiskIssue] = []
    all_issues.extend(_export_issues(data))
    all_issues.extend(_import_issues(data))
    all_issues.extend(_advance_issues(data))
    all_issues.extend(_mtt_issues(data))
    all_issues.extend(_reporting_issues(data))

    raw_score = sum(i.score_points for i in all_issues)
    total_score = min(raw_score, MAX_SCORE)

    risk_category, risk_color_key = get_risk_category(total_score)
    heatmap = _build_heatmap(all_issues)

    return AnalysisResult(
        total_score=total_score,
        risk_category=risk_category,
        risk_color_key=risk_color_key,
        issues=all_issues,
        heatmap=heatmap,
    )
