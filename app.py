"""
app.py  -  FEMA Diligence Analyzer
Run:  streamlit run app.py
"""
from __future__ import annotations
import streamlit as st
from models import DiligenceInput, AnalysisResult
from regulations_kb import format_regulation_list
from risk_engine import analyse
from config import APP_NAME, APP_TAGLINE, TRANSACTION_IMPACT_TIERS, get_transaction_impact

st.set_page_config(page_title=APP_NAME, page_icon=None, layout="wide",
                   initial_sidebar_state="collapsed")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&display=swap');

*, *::before, *::after { box-sizing: border-box; }
section[data-testid="stSidebar"] { display: none !important; }
.stApp { background: #ffffff; }
.main .block-container { max-width: 1100px; padding: 3rem 2.5rem 6rem 2.5rem; margin: 0 auto; }

html, body, p, li, label, div, span, input, select, textarea, button {
  font-family: 'EB Garamond', 'Times New Roman', Georgia, Times, serif !important;
  color: #111111;
}
h1, h2, h3, h4, h5, h6 {
  font-family: 'EB Garamond', 'Times New Roman', Georgia, Times, serif !important;
  color: #111111 !important;
}
h1 { font-size: 2.2rem !important; font-weight: 600 !important; letter-spacing: -0.02em; line-height: 1.2; }
h2 { font-size: 1.6rem !important; font-weight: 600 !important; letter-spacing: -0.01em; margin-top: 2.5rem !important; }
h3 { font-size: 1.25rem !important; font-weight: 600 !important; }

/* tabs */
.stTabs [data-baseweb="tab-list"] { background: transparent; border-bottom: 1px solid #d0d0d0; gap: 0; padding: 0; }
.stTabs [data-baseweb="tab"] {
  font-family: 'EB Garamond', 'Times New Roman', serif !important;
  font-size: 0.95rem; font-weight: 500; color: #999;
  padding: 0.65rem 1.4rem; border-bottom: 2px solid transparent;
  margin-bottom: -1px; background: transparent; letter-spacing: 0.01em;
}
.stTabs [aria-selected="true"] { color: #111 !important; border-bottom: 2px solid #111 !important; font-weight: 600 !important; }

/* buttons */
.stButton > button {
  background-color: #111111 !important; color: #ffffff !important;
  -webkit-text-fill-color: #ffffff !important; border: 1px solid #111111 !important;
  border-radius: 2px !important;
  font-family: 'EB Garamond', 'Times New Roman', serif !important;
  font-size: 1rem !important; font-weight: 500 !important;
  padding: 0.5rem 1.6rem !important; transition: opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.7 !important; background-color: #111111 !important; -webkit-text-fill-color: #ffffff !important; }
.btn-secondary .stButton > button {
  background-color: #ffffff !important; color: #111111 !important;
  -webkit-text-fill-color: #111111 !important; border: 1px solid #cccccc !important;
}
.btn-secondary .stButton > button:hover { background-color: #f5f5f5 !important; opacity: 1 !important; }

/* inputs */
.stTextInput input, .stNumberInput input {
  background-color: #ffffff !important; color: #111111 !important;
  -webkit-text-fill-color: #111111 !important; border: 1px solid #cccccc !important;
  border-radius: 2px !important;
  font-family: 'EB Garamond', 'Times New Roman', serif !important;
  font-size: 1rem !important; padding: 0.45rem 0.75rem !important; box-shadow: none !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
  border: 1px solid #111111 !important; box-shadow: none !important;
  background-color: #ffffff !important; -webkit-text-fill-color: #111111 !important;
}
.stNumberInput > div > div { background-color: #ffffff !important; border: 1px solid #cccccc !important; border-radius: 2px !important; }
.stNumberInput button { background-color: #f5f5f5 !important; color: #111111 !important; border-left: 1px solid #cccccc !important; }
input, textarea { background-color: #ffffff !important; color: #111111 !important; -webkit-text-fill-color: #111111 !important; }

/* checkboxes */
.stCheckbox label { font-family: 'EB Garamond', 'Times New Roman', serif !important; font-size: 1rem !important; color: #222222 !important; line-height: 1.6 !important; }
.stCheckbox [data-baseweb="checkbox"] { background-color: #ffffff !important; border-color: #999999 !important; }

/* metrics */
[data-testid="metric-container"] { background: #fafafa; border: 1px solid #e8e8e8; border-radius: 2px; padding: 1.2rem 1.4rem; }
[data-testid="stMetricLabel"] { font-family: 'EB Garamond', 'Times New Roman', serif !important; font-size: 0.85rem !important; letter-spacing: 0.04em !important; text-transform: uppercase !important; color: #888 !important; }
[data-testid="stMetricValue"] { font-family: 'EB Garamond', 'Times New Roman', serif !important; font-size: 2.2rem !important; color: #111 !important; font-weight: 600 !important; }

/* slider */
[data-testid="stSlider"] .rc-slider-track { background: #111 !important; }
[data-testid="stSlider"] .rc-slider-handle { background: #111 !important; border-color: #111 !important; }

/* divider */
hr { border: none; border-top: 1px solid #e0e0e0 !important; margin: 2rem 0 !important; }

/* section heading — bold with underline rule */
.section-heading {
  font-family: 'EB Garamond', 'Times New Roman', serif;
  font-size: 1.1rem; font-weight: 700; color: #111111;
  letter-spacing: 0.01em; margin-top: 2rem; margin-bottom: 0.6rem;
  padding-bottom: 0.4rem; border-bottom: 2px solid #111111;
}

/* issue blocks */
.issue-block { border-top: 1px solid #e0e0e0; padding: 1.8rem 0 0.8rem 0; }
.issue-block:last-of-type { border-bottom: 1px solid #e0e0e0; }
.issue-title { font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 1.2rem; font-weight: 600; color: #111; margin-bottom: 0.25rem; line-height: 1.35; }
.issue-meta  { font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 0.85rem; color: #888; margin-bottom: 0.7rem; }
.issue-body  { font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 1.05rem; color: #333; line-height: 1.75; }
.reg-ref { font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 0.82rem; color: #555; background: #f2f2f2; padding: 2px 8px; border-radius: 2px; margin-right: 4px; border: 1px solid #e0e0e0; }

/* numbered analysis table */
.analysis-table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 1rem; }
.analysis-table td { font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 1rem; color: #222; border-bottom: 1px solid #eeeeee; padding: 0.6rem 1rem 0.6rem 0; vertical-align: top; line-height: 1.65; }
.analysis-table td.num { font-size: 0.78rem; color: #ccc; width: 26px; padding-right: 0.5rem; }
.analysis-table tr:last-child td { border-bottom: none; }

/* sub-section label inside analysis */
.sub-label { font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #888; margin: 1.2rem 0 0.3rem 0; }

/* heatmap */
.hm-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; margin-top: 0.5rem; }
.hm-cell { padding: 0.9rem 0.5rem 0.9rem 0; border-top: 1px solid #e8e8e8; border-bottom: 1px solid #e8e8e8; }
.hm-label { font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 1rem; color: #111; margin-bottom: 0.15rem; font-weight: 500; }
.hm-status { font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 0.85rem; font-weight: 600; letter-spacing: 0.02em; }
.hm-green { color: #2d6a4f; } .hm-amber { color: #b45309; } .hm-red { color: #991b1b; }

/* score */
.score-display { font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 5.5rem; font-weight: 600; line-height: 1; letter-spacing: -0.04em; color: #111; }
.score-cat { font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 1rem; color: #777; margin-top: 0.4rem; }

/* deal impact tiers */
.tier-row { display: flex; align-items: flex-start; gap: 1.2rem; padding: 1rem 0; border-top: 1px solid #e8e8e8; }
.tier-num { font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 1.6rem; color: #ddd; min-width: 36px; line-height: 1; padding-top: 2px; }
.tier-label { font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 1.05rem; font-weight: 600; }
.tier-detail { font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 1rem; color: #555; line-height: 1.7; margin-top: 0.3rem; }

/* checklist */
.cl-row { display: flex; gap: 0.75rem; padding: 0.65rem 0; border-bottom: 1px solid #f0f0f0; font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 1rem; color: #333; line-height: 1.55; }
.cl-num { font-size: 0.78rem; color: #ccc; min-width: 22px; padding-top: 3px; }

/* transaction impact block */
.impact-block { margin-top: 1.2rem; padding: 1rem 1.2rem; background: #fafafa; border-left: 3px solid #111; }
.impact-label-cap { font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.09em; text-transform: uppercase; color: #888; margin-bottom: 0.3rem; }
.impact-tier { font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 1.05rem; font-weight: 700; margin-bottom: 0.3rem; }
.impact-detail { font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 1rem; color: #444; line-height: 1.65; }

/* footer */
.page-footer { font-family: 'EB Garamond', 'Times New Roman', serif; font-size: 0.82rem; color: #ccc; line-height: 1.7; border-top: 1px solid #eee; padding-top: 1rem; margin-top: 3rem; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def sub_label(text: str) -> str:
    return f"<div class='sub-label'>{text}</div>"

def num_table(items: list) -> str:
    rows = "".join(f"<tr><td class='num'>{i:02d}</td><td>{item}</td></tr>"
                   for i, item in enumerate(items, 1))
    return f"<table class='analysis-table'><tbody>{rows}</tbody></table>"

FOOTER_HTML = ""

# ── Sample data ───────────────────────────────────────────────────────────────
SAMPLE = DiligenceInput(
    company_name="Magnolia Bakery",
    industry="Food & Beverage / Consumer Retail",
    exporter=True, importer=True, service_exporter=False,
    software_exporter=False, merchanting_trader=True,
    sez_unit=False, eou=False,
    annual_turnover_cr=485.0, export_turnover_cr=310.0, import_turnover_cr=120.0,
    outstanding_export_receivables=True,
    amount_outstanding_cr=18.5, num_invoices_outstanding=11, max_delay_months=28.0,
    export_proceeds_realised_within_fema_timelines=False,
    ad_extensions_obtained=False, export_value_reduced_written_off=True,
    set_off_arrangements_used=False, third_party_receipts=True,
    exports_invoiced_in_inr=True, warehouse_exports=False,
    project_exports=False, advance_export_receipts=True,
    outstanding_import_payables=True, import_max_delay_months=9.0,
    advance_import_payments=True, imports_not_materialised=True,
    advance_payments_repatriated=False, gold_silver_imports=False,
    third_party_payments=False, reduced_value_settlements=True,
    merchanting_trade_conducted=True, both_legs_completed=True,
    within_six_months=False, mtt_third_party=False,
    mtt_supporting_documents_available=True,
    edpms_reconciled=False, idpms_reconciled=True,
    outstanding_entries=True, missing_edfs=True,
    supporting_documentation_available=True, ad_bank_queries_pending=True,
)

ALL_WIDGET_KEYS = [
    "inp_co","inp_ind","n_ann","n_exp","n_imp",
    "c_exp","c_imp","c_sw","c_svc","c_mtt",
    "c_or","c_ro","c_ae","c_ev","c_so","c_tp","c_inr","c_wh","c_pe","c_ae2",
    "n_ao","n_ni","n_md",
    "c_oi","c_ai","c_in","c_rp","c_gs","c_tpp","c_rv","n_id",
    "c_mt","c_ld","c_6m","c_mtp","c_md2",
    "c_ep","c_ip","c_oe","c_me","c_sd","c_aq",
]

# ── Session state ─────────────────────────────────────────────────────────────
if "result" not in st.session_state: st.session_state.result = None
if "data"   not in st.session_state: st.session_state.data   = DiligenceInput()

# ── Header ────────────────────────────────────────────────────────────────────
co = st.session_state.data.company_name
co_str = f" \u2014 {co}" if co else ""
st.markdown(f"""
<div style='padding:2rem 0 1.5rem 0; border-bottom:1px solid #e0e0e0; margin-bottom:2rem;'>
  <div style='font-family:EB Garamond,"Times New Roman",serif; font-size:1.15rem; font-weight:600; color:#111;'>
    FEMA Diligence Analyzer{co_str}
  </div>
  <div style='font-family:EB Garamond,"Times New Roman",serif; font-size:0.95rem; color:#999; margin-top:0.25rem;'>
    Cross-border export / import compliance review for M&amp;A transactions
  </div>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs(["Company Profile", "Risk Dashboard", "Deal Impact", "Summary"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 0 — COMPANY PROFILE
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    d = st.session_state.data

    # Action buttons
    a1, a2, _ = st.columns([1, 1, 5])
    if a1.button("Load demo", key="btn_demo"):
        st.session_state.data   = SAMPLE
        st.session_state.result = analyse(SAMPLE)
        # Write all widget keys directly so Streamlit re-renders with correct values
        st.session_state["inp_co"]  = SAMPLE.company_name
        st.session_state["inp_ind"] = SAMPLE.industry
        st.session_state["n_ann"]   = float(SAMPLE.annual_turnover_cr)
        st.session_state["n_exp"]   = float(SAMPLE.export_turnover_cr)
        st.session_state["n_imp"]   = float(SAMPLE.import_turnover_cr)
        st.session_state["c_exp"]   = SAMPLE.exporter
        st.session_state["c_imp"]   = SAMPLE.importer
        st.session_state["c_sw"]    = SAMPLE.software_exporter
        st.session_state["c_svc"]   = SAMPLE.service_exporter
        st.session_state["c_mtt"]   = SAMPLE.merchanting_trader
        st.session_state["c_or"]    = SAMPLE.outstanding_export_receivables
        st.session_state["c_ro"]    = SAMPLE.export_proceeds_realised_within_fema_timelines
        st.session_state["c_ae"]    = SAMPLE.ad_extensions_obtained
        st.session_state["c_ev"]    = SAMPLE.export_value_reduced_written_off
        st.session_state["c_so"]    = SAMPLE.set_off_arrangements_used
        st.session_state["c_tp"]    = SAMPLE.third_party_receipts
        st.session_state["c_inr"]   = SAMPLE.exports_invoiced_in_inr
        st.session_state["c_wh"]    = SAMPLE.warehouse_exports
        st.session_state["c_pe"]    = SAMPLE.project_exports
        st.session_state["c_ae2"]   = SAMPLE.advance_export_receipts
        st.session_state["n_ao"]    = float(SAMPLE.amount_outstanding_cr)
        st.session_state["n_ni"]    = int(SAMPLE.num_invoices_outstanding)
        st.session_state["n_md"]    = float(SAMPLE.max_delay_months)
        st.session_state["c_oi"]    = SAMPLE.outstanding_import_payables
        st.session_state["c_ai"]    = SAMPLE.advance_import_payments
        st.session_state["c_in"]    = SAMPLE.imports_not_materialised
        st.session_state["c_rp"]    = SAMPLE.advance_payments_repatriated
        st.session_state["c_gs"]    = SAMPLE.gold_silver_imports
        st.session_state["c_tpp"]   = SAMPLE.third_party_payments
        st.session_state["c_rv"]    = SAMPLE.reduced_value_settlements
        st.session_state["n_id"]    = float(SAMPLE.import_max_delay_months)
        st.session_state["c_mt"]    = SAMPLE.merchanting_trade_conducted
        st.session_state["c_ld"]    = SAMPLE.both_legs_completed
        st.session_state["c_6m"]    = SAMPLE.within_six_months
        st.session_state["c_mtp"]   = SAMPLE.mtt_third_party
        st.session_state["c_md2"]   = SAMPLE.mtt_supporting_documents_available
        st.session_state["c_ep"]    = SAMPLE.edpms_reconciled
        st.session_state["c_ip"]    = SAMPLE.idpms_reconciled
        st.session_state["c_oe"]    = SAMPLE.outstanding_entries
        st.session_state["c_me"]    = SAMPLE.missing_edfs
        st.session_state["c_sd"]    = SAMPLE.supporting_documentation_available
        st.session_state["c_aq"]    = SAMPLE.ad_bank_queries_pending
        st.rerun()

    with a2:
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("Clear", key="btn_clear"):
            st.session_state.data   = DiligenceInput()
            st.session_state.result = None
            for k in ALL_WIDGET_KEYS:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("## Company Profile")
    c1, c2 = st.columns(2)
    company_name = c1.text_input("Company name",    value=d.company_name, key="inp_co")
    industry     = c2.text_input("Industry / sector", value=d.industry,   key="inp_ind")

    st.markdown('<div class="section-heading">Business Activities &mdash; Select All That Apply</div>', unsafe_allow_html=True)
    bc = st.columns(5)
    exporter = bc[0].checkbox("Goods exporter",    value=d.exporter,           key="c_exp")
    importer = bc[1].checkbox("Goods importer",    value=d.importer,           key="c_imp")
    sw_exp   = bc[2].checkbox("Software exporter", value=d.software_exporter,  key="c_sw")
    svc_exp  = bc[3].checkbox("Service exporter",  value=d.service_exporter,   key="c_svc")
    mtt      = bc[4].checkbox("Merchanting trade", value=d.merchanting_trader, key="c_mtt")

    st.markdown('<div class="section-heading">Annual Turnover (\u20b9 Crore)</div>', unsafe_allow_html=True)
    st.markdown("<p style='font-family:EB Garamond,Times New Roman,serif; font-size:0.9rem; color:#999; margin-top:-0.4rem; margin-bottom:0.6rem;'>Not directly referenced in FEMA 23(R)/2026-RB, but relevant for M&amp;A context: helps size compounding exposure relative to business scale and assess working capital impact.</p>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    annual_t = t1.number_input("Total turnover",  min_value=0.0, value=float(d.annual_turnover_cr), step=10.0, key="n_ann")
    export_t = t2.number_input("Export turnover", min_value=0.0, value=float(d.export_turnover_cr), step=10.0, key="n_exp")
    import_t = t3.number_input("Import turnover", min_value=0.0, value=float(d.import_turnover_cr), step=10.0, key="n_imp")

    # ── Export ────────────────────────────────────────────────────────────────
    if exporter or sw_exp or svc_exp:
        st.markdown("## Export Compliance")
        st.markdown('<div class="section-heading">Regulations 3 \u2013 8 and 13</div>', unsafe_allow_html=True)
        e1, e2 = st.columns(2)
        out_recv    = e1.checkbox("The target has export invoices for which payment from the overseas buyer has not yet been received.", value=d.outstanding_export_receivables, key="c_or")
        realised_ok = e2.checkbox("All export proceeds have been received within the FEMA time limit (15 months from shipment / invoice; 18 months for INR exports).", value=d.export_proceeds_realised_within_fema_timelines, key="c_ro")
        ad_ext      = e1.checkbox("The target has obtained formal AD bank extensions for any overdue export receivables.", value=d.ad_extensions_obtained, key="c_ae")
        ev_reduce   = e2.checkbox("The target has accepted less than the invoiced amount from an overseas buyer (reduced or written-off export receivable).", value=d.export_value_reduced_written_off, key="c_ev")
        setoff      = e1.checkbox("The target has netted off export receivables against import payables owed to the same overseas party (set-off).", value=d.set_off_arrangements_used, key="c_so")
        tp_recv     = e2.checkbox("The target has received export payment from a party other than the named overseas buyer (third-party receipt).", value=d.third_party_receipts, key="c_tp")
        inr_inv     = e1.checkbox("The target invoices or settles some export transactions in Indian Rupees rather than foreign currency.", value=d.exports_invoiced_in_inr, key="c_inr")
        wh_exp      = e2.checkbox("The target exports goods to an overseas warehouse before finding a buyer (consignment / warehouse export).", value=d.warehouse_exports, key="c_wh")
        proj_exp    = e1.checkbox("The target undertakes project exports (e.g. turnkey contracts, construction, or supply-and-install projects abroad).", value=d.project_exports, key="c_pe")
        adv_exp     = e2.checkbox("The target receives advance payments from overseas buyers before goods are shipped or services delivered.", value=d.advance_export_receipts, key="c_ae2")
        if out_recv:
            st.markdown('<div class="section-heading">Outstanding Receivables \u2014 Details</div>', unsafe_allow_html=True)
            ea, eb, ec = st.columns(3)
            amt_out = ea.number_input("Amount outstanding (\u20b9 crore)",   min_value=0.0, value=float(d.amount_outstanding_cr),      step=0.5, key="n_ao")
            num_inv = eb.number_input("Number of invoices outstanding",      min_value=0,   value=int(d.num_invoices_outstanding),     step=1,   key="n_ni")
            max_dly = ec.number_input("Longest delay beyond due date (months)", min_value=0.0, value=float(d.max_delay_months),        step=1.0, key="n_md")
        else:
            amt_out, num_inv, max_dly = 0.0, 0, 0.0
    else:
        out_recv = realised_ok = ad_ext = ev_reduce = setoff = tp_recv = False
        inr_inv = wh_exp = proj_exp = adv_exp = False
        amt_out = num_inv = max_dly = 0.0

    # ── Import ────────────────────────────────────────────────────────────────
    if importer:
        st.markdown("## Import Compliance")
        st.markdown('<div class="section-heading">Regulations 9 \u2013 12</div>', unsafe_allow_html=True)
        i1, i2 = st.columns(2)
        out_imp = i1.checkbox("The target has import invoices that remain unpaid to overseas suppliers beyond the contractual payment date.", value=d.outstanding_import_payables, key="c_oi")
        adv_imp = i2.checkbox("The target has made advance payments to overseas suppliers before receiving the goods or services.", value=d.advance_import_payments, key="c_ai")
        imp_nm  = i1.checkbox("There are cases where an advance was paid for an import but the goods or services were never received.", value=d.imports_not_materialised, key="c_in")
        rep_ok  = i2.checkbox("Where imports did not materialise, the advance payment has been repatriated back to India.", value=d.advance_payments_repatriated, key="c_rp")
        gold    = i1.checkbox("The target imports gold or silver.", value=d.gold_silver_imports, key="c_gs")
        tp_pay  = i2.checkbox("The target has made import payments to a party other than the named overseas supplier (third-party payment).", value=d.third_party_payments, key="c_tpp")
        red_val = i1.checkbox("The target has settled an import invoice for less than the original invoiced amount (reduced value settlement).", value=d.reduced_value_settlements, key="c_rv")
        if out_imp:
            imp_dly = i2.number_input("Longest delay beyond contractual due date (months)", min_value=0.0, value=float(d.import_max_delay_months), step=1.0, key="n_id")
        else:
            imp_dly = 0.0
    else:
        out_imp = adv_imp = imp_nm = rep_ok = gold = tp_pay = red_val = False
        imp_dly = 0.0

    # ── Merchanting ───────────────────────────────────────────────────────────
    if mtt:
        st.markdown("## Merchanting Trade")
        st.markdown('<div class="section-heading">Regulation 16</div>', unsafe_allow_html=True)
        m1, m2 = st.columns(2)
        mtt_done  = m1.checkbox("The target has conducted Merchanting Trade Transactions (buying from an overseas supplier and selling to an overseas buyer, without goods entering India).", value=d.merchanting_trade_conducted, key="c_mt")
        legs_done = m2.checkbox("Both legs of each MTT (outward payment to supplier; inward receipt from buyer) have been completed.", value=d.both_legs_completed, key="c_ld")
        in_6m     = m1.checkbox("Both legs of every MTT were completed within 6 months of each other, as required by FEMA.", value=d.within_six_months, key="c_6m")
        mtt_tp    = m2.checkbox("In some MTTs, payment was received from or made to a party other than the named buyer or supplier.", value=d.mtt_third_party, key="c_mtp")
        mtt_docs  = m1.checkbox("The target holds complete documentation for all MTTs (contracts, invoices, bills of lading) for submission to the AD bank.", value=d.mtt_supporting_documents_available, key="c_md2")
    else:
        mtt_done = legs_done = in_6m = mtt_docs = True
        mtt_tp = False

    # ── Reporting ─────────────────────────────────────────────────────────────
    st.markdown("## Reporting & Documentation")
    st.markdown('<div class="section-heading">Regulations 3 \u2013 4 and 18</div>', unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)
    edpms_ok  = r1.checkbox("The target's export records in RBI's EDPMS are fully up to date and reconciled.", value=d.edpms_reconciled,                      key="c_ep")
    idpms_ok  = r2.checkbox("The target's import records in RBI's IDPMS are fully up to date and reconciled.", value=d.idpms_reconciled,                      key="c_ip")
    out_ent   = r3.checkbox("There are entries in EDPMS or IDPMS that remain open and unresolved.", value=d.outstanding_entries,                              key="c_oe")
    miss_edf  = r1.checkbox("There are export transactions for which the required Export Declaration Form (EDF) was not filed with the AD bank.", value=d.missing_edfs, key="c_me")
    supp_docs = r2.checkbox("The target has complete supporting documentation for all export and import transactions.", value=d.supporting_documentation_available, key="c_sd")
    ad_q      = r3.checkbox("There are unanswered queries or pending correspondence from the target's AD bank.", value=d.ad_bank_queries_pending,              key="c_aq")

    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
    if st.button("Run analysis", key="btn_run"):
        nd = DiligenceInput(
            company_name=company_name, industry=industry,
            exporter=exporter, importer=importer,
            software_exporter=sw_exp, service_exporter=svc_exp,
            merchanting_trader=mtt, sez_unit=False, eou=False,
            annual_turnover_cr=float(annual_t), export_turnover_cr=float(export_t),
            import_turnover_cr=float(import_t),
            outstanding_export_receivables=out_recv,
            amount_outstanding_cr=float(amt_out),
            num_invoices_outstanding=int(num_inv), max_delay_months=float(max_dly),
            export_proceeds_realised_within_fema_timelines=realised_ok,
            ad_extensions_obtained=ad_ext, export_value_reduced_written_off=ev_reduce,
            set_off_arrangements_used=setoff, third_party_receipts=tp_recv,
            exports_invoiced_in_inr=inr_inv, warehouse_exports=wh_exp,
            project_exports=proj_exp, advance_export_receipts=adv_exp,
            outstanding_import_payables=out_imp, import_max_delay_months=float(imp_dly),
            advance_import_payments=adv_imp, imports_not_materialised=imp_nm,
            advance_payments_repatriated=rep_ok, gold_silver_imports=gold,
            third_party_payments=tp_pay, reduced_value_settlements=red_val,
            merchanting_trade_conducted=mtt_done, both_legs_completed=legs_done,
            within_six_months=in_6m, mtt_third_party=mtt_tp,
            mtt_supporting_documents_available=mtt_docs,
            edpms_reconciled=edpms_ok, idpms_reconciled=idpms_ok,
            outstanding_entries=out_ent, missing_edfs=miss_edf,
            supporting_documentation_available=supp_docs, ad_bank_queries_pending=ad_q,
        )
        st.session_state.data   = nd
        st.session_state.result = analyse(nd)
        st.success("Analysis complete. Open the Risk Dashboard tab.")

    st.markdown(FOOTER_HTML, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — RISK DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    if not st.session_state.result:
        st.info("Complete the intake form and click Run analysis.")
    else:
        r: AnalysisResult = st.session_state.result
        d: DiligenceInput = st.session_state.data

        # Score + metrics
        sc1, sc2 = st.columns([1, 3])
        with sc1:
            st.markdown(f"<div class='score-display'>{r.total_score}</div><div class='score-cat'>{r.risk_category}</div>", unsafe_allow_html=True)
        with sc2:
            m1, m2, m3 = st.columns(3)
            m1.metric("Issues identified", len(r.scored_issues))
            m2.metric("Critical / High",   sum(1 for i in r.scored_issues if i.severity in ("Critical","High")))
            m3.metric("Risk score",        f"{r.total_score} / 100")

        st.markdown("---")

        # Heat map — rendered as a CSS grid so all 8 cells have consistent borders
        st.markdown("## Compliance Overview")
        hm_label = {"green":"Clear","amber":"Review required","red":"Material risk"}
        hm_cls   = {"green":"hm-green","amber":"hm-amber","red":"hm-red"}
        cells_html = ""
        for cat, info in r.heatmap.items():
            s = info["status"]; css = hm_cls.get(s,""); lbl = hm_label.get(s,"")
            cells_html += f"<div class='hm-cell'><div class='hm-label'>{cat}</div><div class='hm-status {css}'>{lbl}</div></div>"
        st.markdown("<div class='hm-grid'>" + cells_html + "</div>", unsafe_allow_html=True)

        st.markdown("---")

        # Issue list
        if not r.scored_issues:
            st.markdown("<p style='font-family:EB Garamond,Times New Roman,serif; font-size:1.05rem;'>No material FEMA issues identified based on the information provided.</p>", unsafe_allow_html=True)
        else:
            n = len(r.scored_issues)
            st.markdown(f"## Risk Issues ({n} identified)")
            st.markdown("<p style='font-family:EB Garamond,Times New Roman,serif; font-size:1rem; color:#777; margin-top:-0.5rem; margin-bottom:2rem;'>Each issue is mapped to the applicable FEMA regulation. Click \"Show analysis\" to expand the full due diligence detail.</p>", unsafe_allow_html=True)

            sev_note = {"Critical":"Critical","High":"High risk","Medium":"Medium risk","Low":"Low risk"}
            ti_col_map = {
                "Monitor":"#2d6a4f",
                "Additional Diligence Required":"#b45309",
                "Disclosure Schedule Item":"#b45309",
                "Specific Indemnity Recommended":"#991b1b",
                "Escrow Holdback Advisable":"#991b1b",
                "Potential Deal-Stopper":"#991b1b",
            }

            for idx, issue in enumerate(r.scored_issues, 1):
                reg_labels = format_regulation_list(issue.regulations)
                reg_html   = "".join(f"<span class='reg-ref'>{rl}</span>" for rl in reg_labels)
                sev_txt    = sev_note.get(issue.severity, issue.severity)
                ti_col     = ti_col_map.get(issue.transaction_impact_label, "#555")

                st.markdown(f"""
                <div class='issue-block'>
                  <div style='display:flex; justify-content:space-between; align-items:baseline; flex-wrap:wrap; gap:0.5rem; margin-bottom:0.25rem;'>
                    <div class='issue-title'>{idx:02d}. {issue.title}</div>
                    <div style='font-family:EB Garamond,"Times New Roman",serif; font-size:0.9rem; color:#999; white-space:nowrap;'>{sev_txt} &middot; {issue.score_points} pts</div>
                  </div>
                  <div class='issue-meta'>{reg_html}</div>
                  <div class='issue-body'>{issue.explanation}</div>
                </div>""", unsafe_allow_html=True)

                show_detail = st.checkbox(f"Show analysis for issue {idx:02d}", key=f"show_{idx}")
                if show_detail:
                    st.markdown(sub_label("Why This Matters in M&A"), unsafe_allow_html=True)
                    st.markdown(num_table(issue.why_it_matters), unsafe_allow_html=True)

                    col_l, col_r = st.columns(2)
                    with col_l:
                        st.markdown(sub_label("Potential Consequences"), unsafe_allow_html=True)
                        st.markdown(num_table(issue.potential_consequences), unsafe_allow_html=True)
                        st.markdown(sub_label("Recommended SPA Protections"), unsafe_allow_html=True)
                        st.markdown(num_table(issue.spa_protections), unsafe_allow_html=True)
                    with col_r:
                        st.markdown(sub_label("Documents to Request"), unsafe_allow_html=True)
                        st.markdown(num_table(issue.documents_to_review), unsafe_allow_html=True)
                        st.markdown(sub_label("Questions for Management"), unsafe_allow_html=True)
                        st.markdown(num_table(issue.management_questions), unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class='impact-block' style='border-left-color:{ti_col};'>
                      <div class='impact-label-cap'>Transaction Impact</div>
                      <div class='impact-tier' style='color:{ti_col};'>{issue.transaction_impact_label}</div>
                      <div class='impact-detail'>{issue.transaction_impact_detail}</div>
                    </div>
                    <div style='height:1rem;'></div>""", unsafe_allow_html=True)

        # Standard diligence checklist
        st.markdown("---")
        st.markdown("## Standard Diligence Checklist")
        st.markdown("<p style='font-family:EB Garamond,Times New Roman,serif; font-size:1rem; color:#777; margin-bottom:1.2rem;'>Standard documents to request in addition to the issue-specific items above.</p>", unsafe_allow_html=True)
        checklist = [
            ("Export invoices (last 3 financial years)", "Export Realisation"),
            ("Shipping bills and Export Declaration Forms, EDI and non-EDI", "Reg 3"),
            ("EDPMS extract as at the latest practicable date", "Reg 18"),
            ("Invoice-wise ageing analysis of all export receivables", "Reg 5"),
            ("AD bank extension approvals for any delayed export realisation", "Reg 5"),
            ("AD bank approvals for any export value reductions or write-offs", "Reg 6"),
            ("Set-off arrangement agreements with overseas counterparties", "Reg 7"),
            ("Import contracts and purchase orders (last 3 financial years)", "Reg 9"),
            ("Bills of entry and import invoices", "Import Payments"),
            ("IDPMS extract as at the latest practicable date", "Reg 18"),
            ("Ageing analysis of import payables vs contractual due dates", "Reg 9"),
            ("AD bank extension approvals for delayed import payments", "Reg 9"),
            ("Advance import payment records with repatriation or materialisation evidence", "Reg 12"),
            ("Gold / silver import contracts and payment records", "Reg 11"),
            ("Merchanting Trade Transaction register and underlying contracts", "Reg 16"),
            ("AD bank approvals for third-party MTT flows or timing extensions", "Reg 16"),
            ("All AD bank correspondence on compliance queries (last 3 years)", "Reg 18-19"),
            ("RBI compounding orders, Show Cause Notices, or related correspondence", "Regulatory"),
            ("Board resolutions authorising export / import activities and banking arrangements", "Corporate"),
        ]
        for i, (doc, ref) in enumerate(checklist, 1):
            st.markdown(f"<div class='cl-row'><div class='cl-num'>{i:02d}</div><div>{doc} <span style='font-size:0.82rem; color:#ccc;'>{ref}</span></div></div>", unsafe_allow_html=True)

        st.markdown(FOOTER_HTML, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DEAL IMPACT SIMULATOR
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("## Deal Impact Simulator")
    st.markdown("<p style='font-family:EB Garamond,Times New Roman,serif; font-size:1.05rem; color:#666; margin-bottom:2rem;'>Adjust the severity score to see how a FEMA issue maps to the appropriate M&amp;A transaction response — from a minor diligence note through to a potential deal-stopper.</p>", unsafe_allow_html=True)

    sev = st.slider("Severity score (0 = negligible \u00b7 100 = maximum exposure)",
                    min_value=0, max_value=100, value=40, step=5, key="sim")
    current_tier, current_detail = get_transaction_impact(sev)

    st.markdown("---")

    tc_map = {
        "Monitor":"#2d6a4f",
        "Additional Diligence Required":"#b45309",
        "Disclosure Schedule Item":"#b45309",
        "Specific Indemnity Recommended":"#991b1b",
        "Escrow Holdback Advisable":"#991b1b",
        "Potential Deal-Stopper":"#991b1b",
    }
    for i2, (upper, label, detail) in enumerate(TRANSACTION_IMPACT_TIERS, 1):
        is_active = (label == current_tier)
        tc = tc_map.get(label, "#555")
        if is_active:
            st.markdown(f"""
            <div class='tier-row'>
              <div class='tier-num' style='color:{tc};'>{i2:02d}</div>
              <div>
                <div class='tier-label' style='color:{tc};'>{label}</div>
                <div class='tier-detail'>{detail}</div>
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='tier-row' style='opacity:0.28;'>
              <div class='tier-num'>{i2:02d}</div>
              <div><div class='tier-label' style='color:#999;'>{label}</div></div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**What would a buy-side lawyer do?**")
    guidance = {
        "Monitor": [
            "Note the finding in the diligence working file.",
            "Include a standard FEMA compliance warranty in the SPA.",
            "Flag for post-completion monitoring by the target's finance team.",
        ],
        "Additional Diligence Required": [
            "Issue a supplementary document request focused on this issue.",
            "Schedule a dedicated management Q&A session on this specific topic.",
            "Instruct FEMA specialist counsel to advise on the facts.",
            "Hold the SPA negotiation open on the relevant warranty pending the outcome.",
        ],
        "Disclosure Schedule Item": [
            "Require a specific, particularised disclosure against the FEMA compliance warranty — not a general sweep-up.",
            "Confirm the disclosure does not inadvertently reduce warranty coverage without adequate compensation.",
            "Assess whether additional protection elsewhere in the SPA is required.",
        ],
        "Specific Indemnity Recommended": [
            "Draft a standalone FEMA indemnity in the SPA covering this specific contravention.",
            "The indemnity should cover: RBI compounding fees, penalties, professional fees for regularisation, and consequential losses.",
            "Negotiate without a de minimis threshold or liability basket, with a survival period beyond the general warranty period.",
            "Consider making a compounding application by the target a condition precedent to completion.",
        ],
        "Escrow Holdback Advisable": [
            "Estimate the compounding exposure using RBI's published matrix for the contravention category and duration.",
            "Negotiate a completion holdback or post-completion escrow sized to that estimate.",
            "Define clear release conditions tied to satisfactory regularisation or expiry of the RBI limitation period.",
            "Engage FEMA specialist counsel to map the regularisation pathway and timeline.",
        ],
        "Potential Deal-Stopper": [
            "Escalate immediately to deal team partners and senior client management.",
            "Assess whether this exposure affects the target's ability to continue its export / import business on current terms.",
            "Obtain an urgent independent opinion from FEMA specialist external counsel.",
            "Consider whether the transaction can be restructured (deferred completion, price reduction) or should be paused entirely.",
            "Review the MAC clause to determine whether this constitutes a material adverse change.",
        ],
    }
    items = guidance.get(current_tier, [])
    st.markdown(num_table(items), unsafe_allow_html=True)
    st.markdown(FOOTER_HTML, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    if not st.session_state.result:
        st.info("Run the analysis first.")
    else:
        r: AnalysisResult = st.session_state.result
        d: DiligenceInput = st.session_state.data

        st.markdown("## Executive Summary")
        st.markdown("<p style='font-family:EB Garamond,Times New Roman,serif; font-size:1rem; color:#777; margin-bottom:2rem;'>For insertion into an M&amp;A due diligence report or circulation to the deal team.</p>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style='border-top:3px solid #111; padding:1.5rem 0 1.5rem 0; margin-bottom:2rem;'>
          <div style='font-family:EB Garamond,"Times New Roman",serif; font-size:0.78rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#999; margin-bottom:0.5rem;'>FEMA Risk Assessment</div>
          <div style='font-family:EB Garamond,"Times New Roman",serif; font-size:4rem; font-weight:600; line-height:1; letter-spacing:-0.03em; color:#111;'>{r.total_score}<span style='font-size:1.5rem; color:#bbb; font-weight:400;'>/100</span></div>
          <div style='font-family:EB Garamond,"Times New Roman",serif; font-size:1.1rem; color:#555; margin-top:0.5rem;'>{r.risk_category}</div>
        </div>""", unsafe_allow_html=True)

        roles = [n for n, f in [
            ("goods exporter", d.exporter), ("importer", d.importer),
            ("software exporter", d.software_exporter),
            ("service exporter", d.service_exporter),
            ("merchanting trader", d.merchanting_trader),
        ] if f]
        role_str = ", ".join(roles) if roles else "cross-border trader"
        turnover_str = ""
        if d.annual_turnover_cr > 0:
            turnover_str = f" with annual turnover of \u20b9{d.annual_turnover_cr:.1f}\u00a0crore (export: \u20b9{d.export_turnover_cr:.1f}\u00a0crore; import: \u20b9{d.import_turnover_cr:.1f}\u00a0crore)"

        st.markdown(f"<p style='font-family:EB Garamond,Times New Roman,serif; font-size:1.05rem; color:#222; line-height:1.8;'><b>{d.company_name or 'The Target'}</b> is a {role_str}{turnover_str}. This FEMA diligence review has identified <b>{len(r.scored_issues)} compliance issue(s)</b>, producing an overall risk score of <b>{r.total_score}/100</b> ({r.risk_category}).</p>", unsafe_allow_html=True)

        if r.scored_issues:
            st.markdown("---")
            st.markdown('<div class="section-heading">Issues Identified</div>', unsafe_allow_html=True)
            # Show all issues, not just top 5
            for i2, issue in enumerate(r.scored_issues, 1):
                regs = ", ".join(format_regulation_list(issue.regulations))
                expl = issue.explanation[:300] + ("..." if len(issue.explanation) > 300 else "")
                st.markdown(f"<p style='font-family:EB Garamond,Times New Roman,serif; font-size:1.05rem; color:#222; margin-bottom:0.15rem;'><b>{i2}. {issue.title}</b> &mdash; {issue.severity} ({regs})</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-family:EB Garamond,Times New Roman,serif; font-size:1rem; color:#555; margin-top:0; margin-bottom:1rem; line-height:1.75;'>{expl} <em>Transaction impact: {issue.transaction_impact_label}.</em></p>", unsafe_allow_html=True)

        red_c   = [c for c, i in r.heatmap.items() if i["status"] == "red"]
        amber_c = [c for c, i in r.heatmap.items() if i["status"] == "amber"]
        if red_c or amber_c:
            st.markdown("---")
            st.markdown('<div class="section-heading">Priority Review Areas</div>', unsafe_allow_html=True)
            if red_c:
                st.markdown(f"<p style='font-family:EB Garamond,Times New Roman,serif; font-size:1.05rem; color:#991b1b;'><b>Material risk:</b> {', '.join(red_c)}</p>", unsafe_allow_html=True)
            if amber_c:
                st.markdown(f"<p style='font-family:EB Garamond,Times New Roman,serif; font-size:1.05rem; color:#b45309;'><b>Elevated review required:</b> {', '.join(amber_c)}</p>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="section-heading">Recommended Next Steps</div>', unsafe_allow_html=True)
        steps = [
            "Obtain full EDPMS and IDPMS extracts before completion.",
            "Request invoice-wise ageing of all export receivables and import payables.",
            "Confirm AD bank extension and compounding status for all overdue entries.",
            "Request all compounding applications and RBI / AD bank correspondence.",
            "Conduct a focused management Q&A session on each identified issue.",
            "Instruct FEMA specialist counsel to quantify compounding exposure and advise on regularisation pathways.",
            "Negotiate appropriate FEMA representations, warranties, indemnities, and disclosure schedule items in the SPA.",
        ]
        st.markdown(num_table(steps), unsafe_allow_html=True)

        st.markdown(FOOTER_HTML, unsafe_allow_html=True)
