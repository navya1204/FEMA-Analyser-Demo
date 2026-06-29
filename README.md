# FEMA Diligence Analyzer
### Cross-Border Export / Import Compliance Review for M&A Transactions

> **Regulatory basis:** Foreign Exchange Management (Export and Import of Goods and Services) Regulations, 2026 — Notification No. FEMA 23(R)/2026-RB dated 13 January 2026, effective 1 October 2026.

---

## What It Does

An internal M&A knowledge tool that analyses a target company's FEMA export-import compliance profile and generates:

- **Risk Score** (0–100) and **Risk Category** (Low / Moderate / High / Critical)
- **Compliance Heat Map** across eight workstreams
- **Detailed Issue Analysis** — each issue presented the way a senior M&A lawyer would frame it: why an acquirer should care, potential consequences, documents to request, management questions, and SPA protections
- **Deal Impact Simulator** — slider showing how severity maps from "monitor" through to "potential deal-stopper"
- **Diligence Checklist** — standard + issue-specific document requests
- **Executive Summary** — one-page output ready for insertion into a DD report
- **Downloadable PDF Report** — full formatted memorandum

---

## Quick Start (Local)

```bash
# 1. Clone / copy the project folder
cd fema_diligence_app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

The app opens at `http://localhost:8501`.

Click **"▶ Load Demo Profile"** in the sidebar to instantly populate a sample target (Meridian Exports & Trading Pvt. Ltd.) and see all features.

---

## Deploy to Streamlit Cloud

1. Push the entire `fema_diligence_app/` folder to a GitHub repository (public or private).
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Select your repository, set the **Main file path** to `app.py`.
4. Click **Deploy**. Streamlit Cloud reads `requirements.txt` automatically.

No environment variables or secrets are required.

---

## Architecture

```
fema_diligence_app/
├── app.py                  Main Streamlit application (UI only — no business logic)
├── config.py               Branding, colours, scoring weights, risk thresholds
│                           ← Edit here to recalibrate the scoring model
├── models.py               Typed dataclasses: DiligenceInput, RiskIssue, AnalysisResult
├── regulations_kb.py       Structured summaries of every operative Regulation
│                           (FEMA 23(R)/2026-RB, Regulations 2–19)
├── content_library.py      M&A lawyer analysis templates for every issue type
│                           ← Edit here to refine the diligence playbook
├── risk_engine.py          Scoring engine: DiligenceInput → AnalysisResult
├── report_generator.py     PDF export via ReportLab
└── requirements.txt
```

### Separation of concerns

| File | What to change there |
|------|---------------------|
| `config.py` | Rebrand the tool; adjust scoring weights; change risk-category thresholds |
| `content_library.py` | Refine "why it matters", management questions, SPA protections, document requests |
| `risk_engine.py` | Add new issue families; change triggering logic |
| `regulations_kb.py` | Update regulation summaries if future RBI amendments change the Regulations |
| `app.py` | UI layout, tab structure, styling tweaks |

---

## Rebranding

To rebrand the tool for a client or different practice group, change three constants at the top of `config.py`:

```python
APP_NAME    = "FEMA Diligence Analyzer"       # → e.g. "Cross-Border Risk Engine"
APP_TAGLINE = "Cross-Border Export / Import…" # → your preferred subtitle
FIRM_NAME   = "Internal M&A Knowledge Tools"  # → your firm name
```

No other file needs to change.

---

## Scoring Model

All weights are in `config.RISK_WEIGHTS`. Current values:

| Issue | Points |
|-------|--------|
| Unrealised exports (Reg 13 trigger) | 25 |
| Export realisation delay (Reg 5) | 20 |
| Advance import not repatriated (Reg 12) | 20 |
| Gold/silver advance remittance (Reg 11) | 25 |
| Import payment delay (Reg 9) | 15 |
| Merchanting trade timing breach (Reg 16) | 15 |
| EDPMS unreconciled (Reg 18) | 15 |
| IDPMS unreconciled (Reg 18) | 15 |
| Export value reduced/written off (Reg 6) | 10 |
| Third-party receipts — export (Reg 8) | 10 |
| Third-party payments — import (Reg 8) | 10 |
| Reduced value settlement import (Reg 18) | 10 |
| Merchanting trade — third party (Reg 16) | 10 |
| Merchanting trade — documentation (Reg 16) | 10 |
| Outstanding EDPMS/IDPMS entries (Reg 18) | 10 |
| Missing EDFs (Reg 3) | 10 |
| Missing supporting documentation (Reg 18) | 10 |
| AD bank queries pending (Reg 18–19) | 10 |
| Set-off arrangement (Reg 7) | 5 |
| Advance export receipt routing (Reg 10) | 5 |
| Warehouse export timeline (Reg 5) | 5 |

Total is capped at 100. Risk categories: Low (0–25), Moderate (26–50), High (51–75), Critical (76–100).

---

## Disclaimer

This tool is designed for use by qualified lawyers as a diligence aid only. It does not constitute legal advice. All findings should be reviewed by FEMA and transaction counsel in the context of the specific facts of each transaction. The tool's output is only as reliable as the information entered into the intake form.

---

*FEMA 23(R)/2026-RB — effective 1 October 2026*
