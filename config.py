"""
config.py
=========
Central configuration for the application.

Everything a firm would want to change before "white-labelling" this tool for
a different engagement lives here: the product name, the colour palette, the
risk-scoring weights and the risk-category thresholds.

Nothing in this file contains business logic — it is a settings surface only,
so that a non-developer (e.g. a knowledge-management lawyer) can tune the
tool's behaviour without touching the analysis engine.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# 1. BRANDING / REBRANDING
# ---------------------------------------------------------------------------
# Alternative names considered for this tool (kept here for reference so the
# product can be re-skinned quickly for a different client or practice group):
#   - FEMA Diligence Analyzer
#   - Cross-Border Compliance Risk Engine
#   - FEMA Transaction Risk Dashboard
#   - M&A FEMA Review Tool
#   - Export-Import Due Diligence Engine
#
# To rebrand the tool, change the three constants below. Nothing else needs
# to change.
APP_NAME = "FEMA Diligence Analyzer"
APP_TAGLINE = "Cross-Border Export / Import Compliance Review for M&A Transactions"
FIRM_NAME = "Internal M&A Knowledge Tools"

# Short reference to the regulation this tool is built around. Shown in the
# footer / disclaimer of generated reports.
REGULATION_REFERENCE = (
    "Foreign Exchange Management (Export and Import of Goods and Services) "
    "Regulations, 2026 (Notification No. FEMA 23(R)/2026-RB dated "
    "January 13, 2026), effective October 1, 2026."
)

# ---------------------------------------------------------------------------
# 2. COLOUR PALETTE  (Dark blue / white / grey — premium law-firm aesthetic)
# ---------------------------------------------------------------------------
# These tokens are consumed by ui/styling.py to generate the CSS injected
# into the Streamlit app. Keeping them here means the whole visual identity
# can be adjusted from a single location.
COLORS = {
    "navy":        "#0B1F3A",   # primary brand colour — headers, sidebar
    "navy_light":  "#16335E",   # secondary panels, hover states
    "slate":       "#3D4A5C",   # body text on light backgrounds
    "grey":        "#6B7280",   # muted text / captions
    "grey_light":  "#E7E9ED",   # borders, dividers, table lines
    "paper":       "#F7F8FA",   # page background
    "white":       "#FFFFFF",   # cards / surfaces
    "gold":        "#B68D40",   # restrained accent (use sparingly)
    # Traffic-light risk colours
    "green":       "#2E7D52",
    "amber":       "#C68A1E",
    "red":         "#B3261E",
    "green_bg":    "#E8F3ED",
    "amber_bg":    "#FBF1DE",
    "red_bg":      "#FBEAE9",
}

# Typography: a characterful serif for headings (the "letterhead" feel of a
# law-firm memorandum) paired with a clean, highly legible sans-serif for
# body copy and data.
FONT_DISPLAY = "'Source Serif 4', Georgia, 'Times New Roman', serif"
FONT_BODY = "'Inter', 'Helvetica Neue', Arial, sans-serif"
FONT_MONO = "'IBM Plex Mono', 'Courier New', monospace"

# ---------------------------------------------------------------------------
# 3. RISK SCORING ENGINE — WEIGHTS
# ---------------------------------------------------------------------------
# Every entry below corresponds to one rule in risk_engine.py. Points are
# additive; the total is capped at MAX_SCORE. A firm can recalibrate the
# model for a particular sector, deal size, or client risk appetite simply by
# editing the numbers in this dictionary — no other file needs to change.
RISK_WEIGHTS = {
    # --- Export realisation -------------------------------------------------
    "export_realisation_delay": 20,      # Outstanding export proceeds beyond permitted FEMA timelines (Reg 5)
    "unrealised_export_reg13": 25,       # Export proceeds unrealised > 1 year past due date (Reg 13 consequence)
    "export_value_reduction_writeoff": 10,  # Export value reduced / written off (Reg 6)
    "set_off_arrangement": 5,            # Set-off of export receivables vs import payables (Reg 7)
    "advance_export_receipt_routing": 5,  # Advance export receipts — AD-routing diligence (Reg 10(1))
    "warehouse_export_timeline": 5,      # Warehouse exports — different realisation trigger date (Reg 5(1)(b))

    # --- Import payments ------------------------------------------------------
    "import_payment_delay": 15,          # Imports unpaid beyond contractual period (Reg 9)
    "reduced_value_settlement_import": 10,  # Import settled at reduced value (Reg 18(1)(k))

    # --- Advance remittances ---------------------------------------------------
    "advance_import_not_materialised": 20,  # Advance import payment, import not materialised, not repatriated (Reg 12)
    "gold_silver_advance_breach": 25,    # Advance remittance against gold/silver imports (Reg 11 prohibition)

    # --- Merchanting trade --------------------------------------------------
    "merchanting_timing_breach": 15,     # MTT legs not completed within prescribed period (Reg 16(1)(a))
    "merchanting_third_party": 10,       # MTT third-party receipts/payments (Reg 16(1)(b))
    "merchanting_documentation": 10,     # MTT supporting documents not available (Reg 16(1)(c))

    # --- Third-party transactions (general) ---------------------------------
    "third_party_receipts_export": 10,   # Third-party receipts for exports (Reg 8)
    "third_party_payments_import": 10,   # Third-party payments for imports (Reg 8)

    # --- Reporting & documentation -------------------------------------------
    "edpms_unreconciled": 15,            # EDPMS entries not reconciled (Reg 18)
    "idpms_unreconciled": 15,            # IDPMS entries not reconciled (Reg 18)
    "outstanding_entries": 10,           # Outstanding EDPMS/IDPMS entries pending closure (Reg 18(1)(f))
    "missing_edfs": 10,                  # Missing Export Declaration Forms (Reg 3)
    "missing_supporting_documentation": 10,  # General supporting documentation gaps
    "ad_bank_queries_pending": 10,       # Unresolved AD bank queries
}

# Informational items below carry zero score impact but still surface as
# diligence notes on the dashboard / executive summary (they describe
# structural facts about the target rather than compliance failures).
INFORMATIONAL_WEIGHT = 0

# ---------------------------------------------------------------------------
# 4. RISK CATEGORY THRESHOLDS
# ---------------------------------------------------------------------------
MAX_SCORE = 100

RISK_CATEGORY_THRESHOLDS = [
    # (upper bound inclusive, label, color key)
    (25, "Low Risk", "green"),
    (50, "Moderate Risk", "amber"),
    (75, "High Risk", "amber"),
    (100, "Critical Risk", "red"),
]


def get_risk_category(score: int) -> tuple[str, str]:
    """Return (label, color_key) for a given total risk score."""
    for upper, label, color_key in RISK_CATEGORY_THRESHOLDS:
        if score <= upper:
            return label, color_key
    return "Critical Risk", "red"


# ---------------------------------------------------------------------------
# 5. HEAT MAP CATEGORIES & THRESHOLDS
# ---------------------------------------------------------------------------
# The eight diligence workstreams shown on the heat map. Order is preserved
# wherever the categories are displayed.
HEATMAP_CATEGORIES = [
    "Export Realisation",
    "Import Payments",
    "Advance Remittances",
    "Merchanting Trade",
    "Reporting Compliance",
    "Documentation",
    "Third Party Transactions",
    "AD Bank Approvals",
]

# Sum of issue scores mapped to a category -> traffic-light status.
HEATMAP_THRESHOLDS = {
    "green_max": 0,    # 0 points  -> Green  (no flags raised)
    "amber_max": 19,   # 1-19      -> Amber  (some diligence required)
    # >= 20                       -> Red    (material exposure)
}


def get_heatmap_status(points: int) -> str:
    """Map a category's aggregated points to Green / Amber / Red."""
    if points <= HEATMAP_THRESHOLDS["green_max"]:
        return "green"
    if points <= HEATMAP_THRESHOLDS["amber_max"]:
        return "amber"
    return "red"


# ---------------------------------------------------------------------------
# 6. TRANSACTION IMPACT TIERS (used by the Deal Impact Simulator & issue cards)
# ---------------------------------------------------------------------------
# Each tier maps a severity score (0-100) to the buy-side response a senior
# M&A lawyer would typically reach for. Used both for individual issues and
# for the standalone "Deal Impact Simulator".
TRANSACTION_IMPACT_TIERS = [
    (10, "Monitor",
         "No immediate action. Note in the diligence working file for "
         "completeness; revisit if related issues emerge elsewhere."),
    (35, "Additional Diligence Required",
         "Request further documents and management explanation before "
         "forming a view. Not yet disclosure-worthy on its own."),
    (60, "Disclosure Schedule Item",
         "Sufficiently material that it should be carved out as a specific "
         "disclosure against the relevant warranty in the transaction "
         "documents."),
    (80, "Specific Indemnity Recommended",
         "Generic warranty coverage is unlikely to be adequate. Consider a "
         "standalone indemnity addressing this exposure, drafted to cover "
         "any RBI compounding fees, penalties or restrictions on future "
         "remittances."),
    (95, "Escrow Holdback Advisable",
         "Quantifiable contingent liability. Consider a completion holdback "
         "or escrow sized to the likely compounding exposure, released on "
         "satisfactory regularisation or expiry of the limitation period."),
    (100, "Potential Deal-Stopper",
         "Exposure of this nature could affect the target's ability to "
         "operate its export/import business as presently conducted (e.g. "
         "loss of future advance-payment facility, AD bank relationship "
         "risk). Warrants escalation to the deal team and senior management "
         "before proceeding further."),
]


def get_transaction_impact(severity: int) -> tuple[str, str]:
    """Return (tier_label, tier_description) for a 0-100 severity score."""
    for upper, label, description in TRANSACTION_IMPACT_TIERS:
        if severity <= upper:
            return label, description
    return TRANSACTION_IMPACT_TIERS[-1][1], TRANSACTION_IMPACT_TIERS[-1][2]


# Mapping from an issue's raw score points to a 0-100 "severity" for the
# transaction-impact tiers above (issue points run 0-25; we rescale to the
# simulator's 0-100 range so both speak the same language).
def issue_points_to_severity(points: int) -> int:
    """Rescale a 0-25 issue weight onto the 0-100 transaction-impact scale."""
    return min(100, round(points * 4))
