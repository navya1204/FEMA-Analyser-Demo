"""
content_library.py  –  M&A Lawyer Analysis Templates for Every FEMA Issue
==========================================================================
One dict entry per issue_id.  Each entry drives a RiskIssue object created
by risk_engine.py.  Narrative text uses {placeholders} for runtime data.
"""

ISSUE_LIBRARY: dict = {

    # ─────────────────────────────────────────────────────────────────────────
    # EXPORT REALISATION
    # ─────────────────────────────────────────────────────────────────────────
    "export_realisation_delay": {
        "weight_key": "export_realisation_delay",
        "title": "Outstanding Export Proceeds Beyond FEMA Realisation Timelines",
        "regulations": ["reg_5"],
        "heatmap_categories": ["Export Realisation"],
        "explanation": (
            "The target has outstanding export receivables of approximately "
            "₹{amount_outstanding_cr:.2f} crore across {num_invoices} invoice(s), "
            "with a maximum reported delay of {max_delay} month(s). "
            "Regulation 5 requires realisation within 15 months from shipment / "
            "invoice date (18 months for INR-invoiced exports). {extension_note}"
        ),
        "why_it_matters": [
            "Persistent non-realisation beyond the prescribed period is a FEMA "
            "contravention capable of attracting compounding proceedings, "
            "independent of any commercial dispute over the receivable.",
            "The outstanding quantum represents a potential bad-debt exposure "
            "affecting working capital and the basis on which receivables were "
            "presented in management accounts.",
            "A pattern of delayed realisation may indicate weak collections "
            "discipline or recurring disputes with key customers—relevant to "
            "post-acquisition revenue assurance.",
            "Delayed realisation may also warrant scrutiny of revenue recognition "
            "policies if proceeds are booked as income before cash collection.",
        ],
        "potential_consequences": [
            "Compounding application to RBI / AD Bank, with fees calculated by "
            "reference to amount and duration of the contravention.",
            "Restriction on future exports to advance-payment / irrevocable LC "
            "terms if the one-year threshold under Regulation 13 is crossed.",
            "Possible reclassification of receivable as doubtful for accounting "
            "and tax purposes.",
        ],
        "documents_to_review": [
            "Invoice-wise ageing analysis of export receivables (with "
            "shipment/invoice dates)",
            "EDPMS extracts showing outstanding entries",
            "AD Bank extension approvals obtained under Regulation 5",
            "Customer correspondence evidencing collection efforts or disputes",
            "Board / management minutes discussing outstanding receivables",
        ],
        "management_questions": [
            "What is the root cause of delay for each material invoice—commercial "
            "dispute, customer distress, or administrative failure?",
            "Has an AD Bank extension been sought and granted for each outstanding "
            "entry, and for what period?",
            "Has any compounding application been filed or contemplated?",
            "What recovery or write-off steps have been taken?",
        ],
        "spa_protections": [
            "Specific representation that all export proceeds have been realised "
            "within prescribed periods, or that non-compliance is fully disclosed.",
            "Specific indemnity for compounding fees, penalties, and interest "
            "arising from disclosed delays.",
            "Disclosure schedule entry identifying each outstanding invoice, "
            "amount, delay duration, and status.",
            "Post-completion covenant requiring the target to pursue pending "
            "extension or compounding applications.",
        ],
    },

    "unrealised_export_reg13": {
        "weight_key": "unrealised_export_reg13",
        "title": "Regulation 13 Risk — Export Proceeds Unrealised Beyond One Year",
        "regulations": ["reg_13", "reg_5"],
        "heatmap_categories": ["Export Realisation", "AD Bank Approvals"],
        "explanation": (
            "Based on the maximum delay of {max_delay} month(s) reported, at "
            "least one export receivable appears to have remained unrealised "
            "for more than one year beyond its due date of realisation "
            "(including any AD-extended due date). Regulation 13 provides that "
            "in such circumstances the exporter may undertake further exports "
            "only against full advance payment or an irrevocable Letter of Credit."
        ),
        "why_it_matters": [
            "This is a forward-looking trading restriction—not merely a historic "
            "reporting issue—and can directly impair the target's ability to "
            "trade with the affected customer on open-account terms.",
            "A buyer must understand whether this restriction is already being "
            "applied, and if not, the risk that the AD Bank imposes it once the "
            "position is reviewed post-completion.",
            "If the restriction affects a material customer relationship, it has "
            "a direct and quantifiable revenue / cash-flow impact on Day 1.",
            "A Regulation 13 trigger is also a strong indicator that the underlying "
            "contravention is serious in both quantum and duration, increasing "
            "the likelihood of a material compounding exposure.",
        ],
        "potential_consequences": [
            "AD Bank may require full advance payment or irrevocable LC for future "
            "shipments to the relevant buyer until regularised.",
            "Higher compounding fee exposure given the extended duration.",
            "AD Bank may escalate scrutiny of all the target's export transactions.",
        ],
        "documents_to_review": [
            "Invoice-level ageing showing due dates of realisation and elapsed periods",
            "AD Bank communications regarding Regulation 13 trading restrictions",
            "Evidence of subsequent shipments to affected buyers and payment terms applied",
            "Compounding application (if filed) and RBI / AD correspondence",
        ],
        "management_questions": [
            "Has the AD Bank formally communicated that future exports must be "
            "against advance payment or irrevocable LC?",
            "Have any shipments been made to the affected buyer since the one-year "
            "threshold was crossed, and on what terms?",
            "What is the realistic prospect and timeline for recovery?",
            "Has a compounding application been filed, and if not, why not?",
        ],
        "spa_protections": [
            "Specific indemnity covering (i) compounding fees and (ii) any revenue "
            "loss attributable to advance-payment / LC-only trading terms.",
            "Warranty that no AD Bank or RBI has imposed, or threatened, "
            "restrictions on the target's export trading terms.",
            "Disclosure schedule entry with full particulars of affected "
            "receivables and all AD Bank communications.",
            "Consider an escrow holdback sized to the estimated compounding "
            "exposure, released on satisfactory regularisation.",
        ],
    },

    "export_value_reduction_writeoff": {
        "weight_key": "export_value_reduction_writeoff",
        "title": "Export Value Reduced or Written Off",
        "regulations": ["reg_6"],
        "heatmap_categories": ["Export Realisation", "AD Bank Approvals"],
        "explanation": (
            "The target has reduced or written off export value on one or more "
            "shipments / invoices. Regulation 6 permits this only on a reasoned "
            "request and with AD Bank satisfaction (or self-declaration for "
            "amounts up to ₹10 lakh per shipping bill / invoice)."
        ),
        "why_it_matters": [
            "Recurring reductions may indicate pricing disputes, quality claims, "
            "or collection difficulties with specific customers—relevant to "
            "revenue quality and customer concentration risk.",
            "Reductions above the ₹10 lakh self-declaration threshold without "
            "AD approval are themselves compliance gaps.",
            "Aggregated write-offs are a measure of historic revenue that did not "
            "convert to cash—relevant to EBITDA and working capital normalisation "
            "for valuation purposes.",
        ],
        "potential_consequences": [
            "Compounding exposure if reductions above the self-declaration threshold "
            "proceeded without AD approval.",
            "EBITDA / working capital normalisation adjustments in the valuation model.",
        ],
        "documents_to_review": [
            "Invoice-wise listing of all export value reductions / write-offs, "
            "amounts, and reasons",
            "AD Bank approvals for reductions above the ₹10 lakh threshold",
            "Customer correspondence evidencing the commercial basis for each reduction",
        ],
        "management_questions": [
            "What proportion of reductions relate to a small number of customers "
            "or recurring issues?",
            "For reductions above ₹10 lakh, is the AD approval documentation available?",
            "Are reductions reflected in revenue or as bad-debt expense?",
        ],
        "spa_protections": [
            "Disclosure schedule entry quantifying historic reductions by customer.",
            "Compliance representation regarding AD approvals for above-threshold reductions.",
            "Financial work-stream flag: consider EBITDA normalisation adjustment.",
        ],
    },

    "set_off_arrangement": {
        "weight_key": "set_off_arrangement",
        "title": "Set-Off of Export Receivables Against Import Payables",
        "regulations": ["reg_7"],
        "heatmap_categories": ["Export Realisation", "AD Bank Approvals"],
        "explanation": (
            "The target uses set-off arrangements under Regulation 7, netting "
            "export receivables against import payables owed to / from the same "
            "overseas counterparty or its group companies. AD approval and "
            "completion within the stipulated realisation period are required."
        ),
        "why_it_matters": [
            "Set-off reduces transparency of gross export / import flows—a buyer "
            "should confirm set-off amounts are properly reflected in both "
            "export-realisation and import-payment analyses.",
            "Where the counterparty is a group company of the overseas buyer, "
            "the arrangement intersects with related-party and transfer-pricing "
            "considerations.",
        ],
        "potential_consequences": [
            "If set-off occurred outside the stipulated / extended period, it "
            "could crystallise a Regulation 5 or 13 exposure on the export leg.",
            "Reconciliation complexity for completion accounts if amounts are not "
            "clearly tracked.",
        ],
        "documents_to_review": [
            "Set-off agreements with overseas counterparties",
            "AD Bank approval for set-off arrangements",
            "Reconciliation showing how set-off amounts are reflected in both ledgers",
        ],
        "management_questions": [
            "Were all set-off transactions completed within the stipulated / "
            "extended realisation period?",
            "Is the overseas counterparty a related party of the target?",
            "How are set-off amounts tracked to avoid double-counting?",
        ],
        "spa_protections": [
            "Compliance representation regarding AD approval and timing.",
            "Disclosure schedule entry if any mismatches identified.",
            "Related-party disclosure if applicable.",
        ],
    },

    "advance_export_receipt_routing": {
        "weight_key": "advance_export_receipt_routing",
        "title": "Advance Export Receipts — AD Bank Routing Compliance",
        "regulations": ["reg_10"],
        "heatmap_categories": ["Advance Remittances", "AD Bank Approvals"],
        "explanation": (
            "The target receives advance payments against export orders. "
            "Regulation 10(1) requires the advance receipt and subsequent "
            "realisation for the same order to be routed through the same AD "
            "Bank, unless both ADs have been formally notified of a change."
        ),
        "why_it_matters": [
            "AD Bank routing mismatches can leave EDPMS entries unreconciled "
            "and complicate future compliance reporting.",
            "Where advances carry interest, the Regulation 10(4) all-in-cost "
            "ceiling applies—a separate Borrowing & Lending Regulations issue if breached.",
            "Material advance receipts indicate reliance on pre-payment terms "
            "that a buyer should assess for customer concentration risk.",
        ],
        "potential_consequences": [
            "EDPMS reconciliation issues if advance and realisation are routed "
            "through different ADs without notification.",
            "Borrowing & Lending Regulations breach if interest on advances "
            "exceeds the all-in-cost ceiling.",
        ],
        "documents_to_review": [
            "Listing of advance export receipts with AD Bank details and "
            "corresponding realisation entries",
            "Any AD-change notifications issued under Regulation 10(1)",
            "Terms of interest-bearing advance arrangements",
        ],
        "management_questions": [
            "Does the target's treasury process track AD routing for advances?",
            "Are any advances interest-bearing, and how is the all-in-cost "
            "ceiling monitored?",
        ],
        "spa_protections": [
            "Compliance representation regarding AD routing of advances.",
            "Disclosure schedule entry if routing mismatches identified.",
        ],
    },

    "warehouse_export_timeline": {
        "weight_key": "warehouse_export_timeline",
        "title": "Warehouse Exports — Realisation Period Runs From Date of Sale",
        "regulations": ["reg_5"],
        "heatmap_categories": ["Export Realisation"],
        "explanation": (
            "The target exports goods to an overseas warehouse. Under "
            "Regulation 5(1)(b) the 15-month realisation period begins "
            "from the date of sale from the warehouse—not the shipment date. "
            "This distinction is commonly miscalculated and can materially "
            "alter which receivables are overdue."
        ),
        "why_it_matters": [
            "Applying the wrong trigger date could cause the finance team to "
            "either over- or under-state the population of overdue receivables.",
            "The longer, less transparent chain of custody for warehouse exports "
            "increases the documentation burden to evidence the actual sale date.",
        ],
        "potential_consequences": [
            "Mis-stated realisation timelines (in either direction), affecting "
            "the accuracy of the Export Realisation findings in this review.",
        ],
        "documents_to_review": [
            "Warehouse export transactions with both shipment dates and dates "
            "of sale from the overseas warehouse",
            "Warehousing / consignment agreements with the overseas warehouse operator",
        ],
        "management_questions": [
            "How does the target track the actual date of sale from the overseas "
            "warehouse for realisation-period monitoring?",
        ],
        "spa_protections": [
            "Disclosure schedule entry describing the warehouse export arrangement.",
            "Compliance representation regarding correct application of Regulation 5(1)(b).",
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # IMPORT PAYMENTS
    # ─────────────────────────────────────────────────────────────────────────
    "import_payment_delay": {
        "weight_key": "import_payment_delay",
        "title": "Outstanding Import Payables Beyond Contractual Period",
        "regulations": ["reg_9"],
        "heatmap_categories": ["Import Payments"],
        "explanation": (
            "The target has outstanding import payables with a maximum "
            "reported delay of {import_max_delay} month(s) beyond the period "
            "specified in the underlying import contract(s). Regulation 9 "
            "requires the AD Bank to monitor IDPMS entries and follow up for "
            "payment within the contracted period, with extensions available "
            "on a reasoned request."
        ),
        "why_it_matters": [
            "Delayed payment to overseas suppliers can strain key supply "
            "relationships—relevant where the target depends on continuity "
            "of imported inputs.",
            "Unexplained delay without a corresponding AD extension is a "
            "compliance gap requiring regularisation.",
            "Outstanding payables may understate the target's true liabilities, "
            "affecting completion accounts and working capital.",
            "Persistent delay may signal liquidity pressure relevant to "
            "post-completion funding requirements.",
        ],
        "potential_consequences": [
            "AD Bank may decline to process further outward remittances to the "
            "same supplier pending regularisation.",
            "Compounding exposure if delay is not covered by an AD extension.",
            "Strained supplier relationships affecting continuity of supply.",
        ],
        "documents_to_review": [
            "Ageing analysis of import payables cross-referenced to contractual "
            "payment terms",
            "IDPMS extracts evidencing outstanding entries",
            "AD Bank extension approvals for delayed payments",
            "Supplier correspondence regarding the delay",
        ],
        "management_questions": [
            "What is the reason for delay in each material case, and has the "
            "AD Bank been approached for an extension?",
            "Are any suppliers threatening to suspend supply as a result?",
            "What is the plan and funding source to clear outstanding payables?",
        ],
        "spa_protections": [
            "Working capital adjustment to reflect the true quantum of "
            "outstanding payables at completion.",
            "Disclosure schedule entry identifying outstanding payables by "
            "supplier, amount, and delay.",
            "Indemnity for compounding exposure arising from unregularised delays.",
        ],
    },

    "reduced_value_settlement_import": {
        "weight_key": "reduced_value_settlement_import",
        "title": "Imports Settled at Reduced Value",
        "regulations": ["reg_18"],
        "heatmap_categories": ["Import Payments", "AD Bank Approvals"],
        "explanation": (
            "The target has settled one or more import transactions at a "
            "value lower than the originally invoiced amount. Regulation 18(1)(k) "
            "permits AD Bank closure of the IDPMS entry only after the AD is "
            "satisfied of the genuineness of the reasons cited."
        ),
        "why_it_matters": [
            "Reduced-value settlements can reflect legitimate commercial "
            "adjustments (quality claims, price renegotiation) but can also "
            "disguise related-party pricing adjustments.",
            "If AD satisfaction was not documented, the IDPMS entry may remain "
            "technically open notwithstanding commercial settlement.",
        ],
        "potential_consequences": [
            "IDPMS entries remaining open if AD satisfaction was not documented.",
            "Transfer-pricing or customs-valuation queries if the reduction "
            "relates to a related-party import.",
        ],
        "documents_to_review": [
            "Listing of reduced-value import settlements with original and "
            "settled values and reasons",
            "AD Bank correspondence confirming IDPMS closure under Regulation 18(1)(k)",
            "Related-party disclosures for the relevant suppliers",
        ],
        "management_questions": [
            "What is the commercial reason for each reduced-value settlement, "
            "and is the supplier a related party?",
            "Has the AD Bank confirmed closure of corresponding IDPMS entries?",
        ],
        "spa_protections": [
            "Disclosure schedule entry describing reduced-value settlements.",
            "Compliance representation regarding IDPMS closure.",
            "Related-party / transfer-pricing representation if applicable.",
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # ADVANCE REMITTANCES
    # ─────────────────────────────────────────────────────────────────────────
    "advance_import_not_materialised": {
        "weight_key": "advance_import_not_materialised",
        "title": "Advance Import Payments — Imports Not Materialised, Amounts Not Repatriated",
        "regulations": ["reg_12"],
        "heatmap_categories": ["Advance Remittances", "AD Bank Approvals"],
        "explanation": (
            "The target has made advance payments for imports that have not "
            "materialised within the contract period (or any AD-extended period), "
            "and the corresponding amounts have not been repatriated. Under "
            "Regulation 12 this triggers a forward-looking restriction: any future "
            "advance import payment by the target requires an unconditional "
            "irrevocable standby LC or guarantee from an international bank of "
            "repute (or an AD Bank guarantee counter-guaranteed by such a bank)."
        ),
        "why_it_matters": [
            "The Regulation 12 restriction materially increases the cost and "
            "operational friction of future import procurement on an advance-"
            "payment basis—a structural issue, not merely a historic footnote.",
            "Non-repatriation may indicate a recoverability issue with the overseas "
            "counterparty—a potential balance-sheet write-off risk.",
            "The LC / guarantee requirement under Regulation 12 will need to be "
            "factored into working capital and treasury planning post-completion.",
        ],
        "potential_consequences": [
            "All future advance import payments require an unconditional irrevocable "
            "LC or international bank guarantee until regularised.",
            "Unrecoverable advance payments may require provision or write-off.",
            "Compounding exposure for non-repatriation.",
        ],
        "documents_to_review": [
            "Details of advance import payments where the import has not materialised",
            "Repatriation evidence (or confirmation that repatriation has not occurred)",
            "AD Bank communications regarding the outstanding IDPMS entries",
            "Correspondence with the overseas supplier regarding status of supply",
        ],
        "management_questions": [
            "Why did the import not materialise, and what is the recovery plan "
            "for the advance payment?",
            "Has the AD Bank formally communicated the Regulation 12 LC / "
            "guarantee requirement for future advance payments?",
            "Has a compounding application been filed for the non-repatriation?",
        ],
        "spa_protections": [
            "Specific indemnity for (i) any unrecoverable advance amount and "
            "(ii) compounding fees for non-repatriation.",
            "Disclosure schedule entry with full particulars.",
            "Consider purchase price adjustment if advance is likely unrecoverable.",
            "Post-completion covenant to regularise the IDPMS entry and, if "
            "applicable, to file a compounding application.",
        ],
    },

    "gold_silver_advance_breach": {
        "weight_key": "gold_silver_advance_breach",
        "title": "Gold / Silver Imports — Absolute Prohibition on Advance Remittance",
        "regulations": ["reg_11"],
        "heatmap_categories": ["Advance Remittances", "Import Payments"],
        "explanation": (
            "The target imports gold or silver. Regulation 11 contains an "
            "absolute prohibition on advance remittances for gold or silver "
            "imports—notwithstanding any other provision of the Regulations. "
            "If the target has made any advance remittances in connection with "
            "such imports, this represents a serious FEMA contravention."
        ),
        "why_it_matters": [
            "The prohibition is absolute—there is no documentation pathway, "
            "AD approval mechanism, or self-declaration route that renders an "
            "advance remittance for gold / silver imports compliant.",
            "Any advance remittance for gold / silver is a standalone FEMA "
            "contravention of the highest severity, and the compounding exposure "
            "is likely to be calculated on the full remittance amount.",
            "A buyer in a regulated sector (banking, jewellery, manufacturing) "
            "needs to factor this into its regulatory due diligence as well as "
            "its FEMA analysis.",
        ],
        "potential_consequences": [
            "Compounding application on the full advance remittance amount—no "
            "mitigating documentation pathway available.",
            "Potential impact on the target's future import permissions if "
            "the contravention is serious.",
        ],
        "documents_to_review": [
            "All import contracts / documentation relating to gold or silver imports",
            "Payment records evidencing whether any advance remittances were made",
            "AD Bank correspondence regarding mode of payment for gold / silver imports",
        ],
        "management_questions": [
            "Were any advance remittances made in connection with gold or silver "
            "imports at any time?",
            "If so, what was the quantum and when was the remittance made?",
            "Has a compounding application been filed?",
        ],
        "spa_protections": [
            "Specific indemnity for the full compounding exposure.",
            "Disclosure schedule entry with full particulars.",
            "Warranty that no advance remittances for gold / silver imports were "
            "made at any time.",
            "Consider escrow holdback pending resolution of any compounding "
            "proceedings.",
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # THIRD-PARTY TRANSACTIONS
    # ─────────────────────────────────────────────────────────────────────────
    "third_party_receipts_export": {
        "weight_key": "third_party_receipts_export",
        "title": "Third-Party Receipts for Export Transactions",
        "regulations": ["reg_8"],
        "heatmap_categories": ["Third Party Transactions", "Export Realisation"],
        "explanation": (
            "The target receives export proceeds from a party other than the "
            "overseas buyer named in the underlying export contract. Regulation 8 "
            "permits such arrangements only where the AD Bank is satisfied as to "
            "the bona fides of the transaction."
        ),
        "why_it_matters": [
            "Third-party receipt structures are permissible but require AD "
            "satisfaction and supporting documentation—if this was not obtained, "
            "the EDPMS entries may not be properly closed.",
            "Third-party payment flows can complicate AML / KYC analysis—a buyer "
            "should understand the commercial rationale and the identity of the "
            "third-party payer.",
            "Where the third party is a group company of the overseas buyer, "
            "the arrangement also intersects with related-party and transfer-"
            "pricing considerations.",
        ],
        "potential_consequences": [
            "EDPMS reconciliation issues if AD satisfaction was not documented.",
            "AML / KYC exposure if the identity or basis for involvement of the "
            "third-party payer was not properly established.",
        ],
        "documents_to_review": [
            "Export contracts identifying the overseas buyer",
            "Bank statements / SWIFT messages evidencing third-party receipts",
            "AD Bank approval / satisfaction documentation",
            "Underlying agreement or arrangement with the third-party payer",
        ],
        "management_questions": [
            "Who is the third-party payer and what is its relationship to the "
            "overseas buyer?",
            "Was AD satisfaction obtained for each third-party receipt?",
            "Is the third-party payer a related party of the target?",
        ],
        "spa_protections": [
            "Compliance representation regarding AD approval for third-party receipts.",
            "AML / KYC representation regarding the identity of third-party payers.",
            "Disclosure schedule entry describing the arrangement.",
        ],
    },

    "third_party_payments_import": {
        "weight_key": "third_party_payments_import",
        "title": "Third-Party Payments for Import Transactions",
        "regulations": ["reg_8"],
        "heatmap_categories": ["Third Party Transactions", "Import Payments"],
        "explanation": (
            "The target makes import payments to a party other than the overseas "
            "supplier named in the underlying import contract. Regulation 8 "
            "permits this only where the AD Bank is satisfied as to the bona "
            "fides of the transaction."
        ),
        "why_it_matters": [
            "Third-party payment flows can complicate AML / KYC analysis and "
            "may indicate that the underlying commercial arrangement is more "
            "complex than disclosed.",
            "If AD satisfaction was not documented, the IDPMS entry may not "
            "be properly closed.",
        ],
        "potential_consequences": [
            "IDPMS reconciliation issues if AD satisfaction was not documented.",
            "AML / KYC exposure as above.",
        ],
        "documents_to_review": [
            "Import contracts identifying the overseas supplier",
            "Bank statements evidencing third-party payments",
            "AD Bank approval / satisfaction documentation",
        ],
        "management_questions": [
            "Who is the third-party payee and what is its relationship to the "
            "overseas supplier?",
            "Was AD satisfaction obtained for each third-party payment?",
        ],
        "spa_protections": [
            "Compliance representation regarding AD approval for third-party payments.",
            "AML / KYC representation.",
            "Disclosure schedule entry.",
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # MERCHANTING TRADE
    # ─────────────────────────────────────────────────────────────────────────
    "merchanting_timing_breach": {
        "weight_key": "merchanting_timing_breach",
        "title": "Merchanting Trade — Both Legs Not Completed Within Six Months",
        "regulations": ["reg_16"],
        "heatmap_categories": ["Merchanting Trade"],
        "explanation": (
            "The target conducts Merchanting Trade Transactions (MTT) but has "
            "not completed both the outward remittance (to the overseas seller) "
            "and inward remittance (from the overseas buyer) legs within the "
            "six-month window prescribed by Regulation 16(1)(a), without a "
            "corresponding AD Bank extension."
        ),
        "why_it_matters": [
            "The six-month timing requirement is one of the defining conditions "
            "of a permissible MTT under Regulation 16—breach could cause the "
            "transaction to be re-characterised as a non-compliant arrangement.",
            "The AD Bank is required to monitor both legs of each MTT—evidence "
            "of timing breaches may also indicate EDPMS / IDPMS closure failures.",
            "MTT-related FEMA exposure is often underestimated because the "
            "transactions sit between export and import compliance workstreams "
            "and are missed in general diligence.",
        ],
        "potential_consequences": [
            "Compounding exposure for each MTT where the six-month window was "
            "exceeded without extension.",
            "AD Bank may decline to process future MTT remittances pending "
            "regularisation.",
            "Re-characterisation risk if transactions are found to be outside "
            "the FEMA definition of MTT.",
        ],
        "documents_to_review": [
            "MTT transaction listing with both outward and inward remittance dates",
            "AD Bank extension approvals for any MTTs exceeding six months",
            "EDPMS and IDPMS extracts for MTT entries",
            "Underlying commercial contracts with overseas buyer and seller",
        ],
        "management_questions": [
            "For MTTs where the six-month window was exceeded, was an AD Bank "
            "extension sought and granted?",
            "How many MTTs are outstanding (i.e., only one leg complete), "
            "and what is their aggregate value?",
            "Does the target maintain a separate register of MTT transactions "
            "for monitoring purposes?",
        ],
        "spa_protections": [
            "Specific indemnity for compounding fees referable to MTT timing breaches.",
            "Disclosure schedule entry identifying affected MTTs.",
            "Post-completion covenant to regularise outstanding MTT entries.",
        ],
    },

    "merchanting_third_party": {
        "weight_key": "merchanting_third_party",
        "title": "Merchanting Trade — Third-Party Receipts or Payments",
        "regulations": ["reg_16"],
        "heatmap_categories": ["Merchanting Trade", "Third Party Transactions"],
        "explanation": (
            "The target's MTT structure involves receipt from a party other than "
            "the overseas buyer, or payment to a party other than the overseas "
            "seller. Regulation 16(1)(b) requires that inward remittances be "
            "received only from the overseas buyer and outward remittances paid "
            "only to the overseas seller, unless the AD Bank has specifically "
            "approved third-party exceptions."
        ),
        "why_it_matters": [
            "Third-party MTT flows—if without AD approval—are a strict breach of "
            "Regulation 16(1)(b), irrespective of the commercial rationale.",
            "Such structures can also raise AML / KYC concerns given the inherent "
            "complexity of back-to-back trade flows.",
        ],
        "potential_consequences": [
            "Compounding exposure for unapproved third-party MTT flows.",
            "AML / KYC exposure.",
            "AD Bank may scrutinise all MTT transactions if this issue surfaces.",
        ],
        "documents_to_review": [
            "MTT payment records identifying remitting / receiving parties vs "
            "contractual buyer / seller",
            "AD Bank approval for any third-party MTT flows",
            "AML / KYC records for third-party payers / payees",
        ],
        "management_questions": [
            "Were any third-party MTT receipts / payments made, and if so, was "
            "AD Bank approval obtained for each?",
            "What is the identity and commercial role of the third party?",
        ],
        "spa_protections": [
            "Compliance representation regarding AD approval for third-party MTT flows.",
            "AML / KYC representation.",
            "Disclosure schedule entry.",
        ],
    },

    "merchanting_documentation": {
        "weight_key": "merchanting_documentation",
        "title": "Merchanting Trade — Supporting Documentation Gaps",
        "regulations": ["reg_16"],
        "heatmap_categories": ["Merchanting Trade", "Documentation"],
        "explanation": (
            "The target is unable to provide complete documentation evidencing "
            "its MTT transactions for submission to the AD Bank as required by "
            "Regulation 16(1)(c). The AD Bank is required to be satisfied as "
            "to the genuineness of the transaction before crediting / debiting "
            "the customer's account."
        ),
        "why_it_matters": [
            "Documentation gaps mean the AD Bank cannot properly close EDPMS / "
            "IDPMS entries for MTTs, leaving outstanding entries on the system.",
            "In the absence of documentation, the genuineness of the underlying "
            "MTT may itself be questioned—relevant to AML / sanctions diligence.",
        ],
        "potential_consequences": [
            "EDPMS / IDPMS entries remaining open pending documentation.",
            "AD Bank scrutiny of the genuineness of the MTT.",
        ],
        "documents_to_review": [
            "MTT documentation checklist against Regulation 16 requirements",
            "Copies of available MTT documents (commercial invoices, bills of lading, "
            "contracts with overseas buyer and seller)",
        ],
        "management_questions": [
            "What specific documents are missing and why?",
            "Has the AD Bank raised queries about documentation for any MTT?",
        ],
        "spa_protections": [
            "Compliance representation regarding MTT documentation.",
            "Disclosure schedule entry identifying documentation gaps.",
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # REPORTING & DOCUMENTATION
    # ─────────────────────────────────────────────────────────────────────────
    "edpms_unreconciled": {
        "weight_key": "edpms_unreconciled",
        "title": "EDPMS Entries Not Reconciled",
        "regulations": ["reg_4", "reg_18"],
        "heatmap_categories": ["Reporting Compliance", "Documentation"],
        "explanation": (
            "The target's Export Data Processing and Monitoring System (EDPMS) "
            "entries are not fully reconciled. Regulation 4 requires the AD Bank "
            "to update EDPMS simultaneously with each receipt, and Regulation 18 "
            "requires ongoing monitoring and closure of outstanding entries."
        ),
        "why_it_matters": [
            "Unreconciled EDPMS is one of the most reliable indicators of "
            "systemic compliance weakness in a target's export operations—it "
            "suggests the finance / treasury function is not actively managing "
            "FEMA obligations.",
            "Outstanding EDPMS entries represent a population of export "
            "transactions with uncertain realisation status—the buyer cannot "
            "assess its export-realisation exposure without first reconciling "
            "the system.",
            "AD Bank queries arising from unreconciled entries can create "
            "disruption to the target's banking relationships post-completion.",
        ],
        "potential_consequences": [
            "AD Bank may escalate unreconciled entries to RBI, triggering a "
            "formal review of the target's export compliance.",
            "Compounding exposure for each unreconciled entry where the "
            "realisation period has expired.",
            "Disruption to export banking arrangements pending reconciliation.",
        ],
        "documents_to_review": [
            "Full EDPMS extract as at the latest practicable date",
            "Reconciliation schedule produced by the target's finance team",
            "AD Bank correspondence regarding outstanding EDPMS entries",
        ],
        "management_questions": [
            "What is the total number and aggregate value of unreconciled "
            "EDPMS entries, and over what period do they span?",
            "What is the reason for the reconciliation failure—system gap, "
            "process failure, or substantive non-realisation?",
            "Has the AD Bank raised the outstanding entries with the target?",
        ],
        "spa_protections": [
            "Representation that EDPMS entries are current and reconciled as "
            "at completion (or at a specified pre-completion date).",
            "Indemnity for compounding exposure arising from entries where "
            "realisation has not in fact occurred.",
            "Pre-completion covenant to reconcile EDPMS and deliver a "
            "reconciliation schedule to the buyer.",
        ],
    },

    "idpms_unreconciled": {
        "weight_key": "idpms_unreconciled",
        "title": "IDPMS Entries Not Reconciled",
        "regulations": ["reg_4", "reg_18"],
        "heatmap_categories": ["Reporting Compliance", "Documentation"],
        "explanation": (
            "The target's Import Data Processing and Monitoring System (IDPMS) "
            "entries are not fully reconciled. As with EDPMS, Regulations 4 and 18 "
            "require the AD Bank to update IDPMS simultaneously with each payment "
            "and to monitor and close outstanding entries."
        ),
        "why_it_matters": [
            "Unreconciled IDPMS entries represent a population of import "
            "transactions with uncertain payment status—the buyer cannot fully "
            "assess its import-payment exposure without reconciling the system.",
            "Similar to EDPMS gaps, this is an indicator of systemic compliance "
            "weakness in the import operations.",
        ],
        "potential_consequences": [
            "AD Bank escalation and formal review of import compliance.",
            "Compounding exposure for entries where payment obligations have "
            "not been met.",
        ],
        "documents_to_review": [
            "Full IDPMS extract as at the latest practicable date",
            "Reconciliation schedule produced by the target's finance team",
            "AD Bank correspondence regarding outstanding IDPMS entries",
        ],
        "management_questions": [
            "What is the total number and aggregate value of unreconciled "
            "IDPMS entries?",
            "What is the root cause of the reconciliation failure?",
        ],
        "spa_protections": [
            "Representation that IDPMS entries are current and reconciled as "
            "at completion.",
            "Indemnity for compounding exposure from unreconciled entries.",
            "Pre-completion covenant to reconcile IDPMS.",
        ],
    },

    "outstanding_entries": {
        "weight_key": "outstanding_entries",
        "title": "Outstanding EDPMS / IDPMS Entries Pending Closure",
        "regulations": ["reg_18"],
        "heatmap_categories": ["Reporting Compliance"],
        "explanation": (
            "The target has outstanding entries in EDPMS and / or IDPMS that "
            "have not been marked off / closed. Regulation 18(1)(f) requires "
            "the AD Bank to monitor all transactions for closure and follow up "
            "actively for submission of closing documents."
        ),
        "why_it_matters": [
            "Outstanding entries are a primary focus of AD Bank compliance reviews "
            "and RBI inspections—a buyer inherits the AD's monitoring obligation "
            "in respect of these entries.",
            "Each outstanding entry is a potential unresolved compliance exposure "
            "whose severity depends on the elapsed time and the underlying facts.",
        ],
        "potential_consequences": [
            "AD Bank follow-up and potential escalation to RBI.",
            "Compounding exposure proportional to the duration and amount of "
            "each outstanding entry.",
        ],
        "documents_to_review": [
            "Full listing of outstanding EDPMS / IDPMS entries with ages",
            "Evidence of AD Bank follow-up communications",
            "Closing documents (if partially available) for each outstanding entry",
        ],
        "management_questions": [
            "What is the aggregate value and age profile of outstanding entries?",
            "For each outstanding entry, what document or action is required "
            "to effect closure?",
        ],
        "spa_protections": [
            "Pre-completion covenant to prepare and deliver a complete outstanding "
            "entries schedule.",
            "Indemnity for compounding exposure referable to outstanding entries.",
        ],
    },

    "missing_edfs": {
        "weight_key": "missing_edfs",
        "title": "Missing Export Declaration Forms (EDFs)",
        "regulations": ["reg_3"],
        "heatmap_categories": ["Documentation", "Reporting Compliance"],
        "explanation": (
            "One or more Export Declaration Forms (EDFs) required under "
            "Regulation 3 are missing from the target's records. For goods "
            "exports through EDI ports the EDF is embedded in the shipping bill, "
            "but for non-EDI goods and all service/software exports a separate "
            "EDF must be filed within the prescribed period."
        ),
        "why_it_matters": [
            "A missing EDF means the corresponding export transaction was not "
            "properly declared to the specified authority—a standalone FEMA "
            "compliance gap independent of whether proceeds were realised.",
            "Missing EDFs make it impossible to close the corresponding EDPMS "
            "entry, contributing to the outstanding-entries issue.",
        ],
        "potential_consequences": [
            "Compounding exposure for each missing EDF.",
            "EDPMS entries remaining open pending EDF submission.",
        ],
        "documents_to_review": [
            "Export register cross-referenced to EDPMS and EDF records",
            "Shipping bills (for EDI port goods exports) confirming deemed EDF",
            "Service export invoices and corresponding EDF submissions",
        ],
        "management_questions": [
            "For which transactions are EDFs missing, and what is the reason "
            "for non-filing in each case?",
            "For service exports, is the 30-day filing deadline being tracked?",
        ],
        "spa_protections": [
            "Compliance representation regarding EDF filing.",
            "Pre-completion covenant to file outstanding EDFs.",
            "Indemnity for compounding exposure from missing EDFs.",
        ],
    },

    "missing_supporting_documentation": {
        "weight_key": "missing_supporting_documentation",
        "title": "General Supporting Documentation Gaps",
        "regulations": ["reg_18"],
        "heatmap_categories": ["Documentation"],
        "explanation": (
            "The target is unable to produce complete supporting documentation "
            "for one or more categories of export / import / MTT transactions. "
            "Complete documentation is required both to close EDPMS / IDPMS "
            "entries (Regulation 18) and to establish the genuineness of "
            "transactions for AD Bank purposes (Regulation 4)."
        ),
        "why_it_matters": [
            "Documentation gaps impede a buyer's ability to verify the accuracy "
            "of the target's compliance representations—a gap in diligence "
            "coverage rather than a confirmed contravention.",
            "They also make it harder to assess or quantify the compounding "
            "exposure from underlying substantive issues.",
        ],
        "potential_consequences": [
            "Inability to close EDPMS / IDPMS entries.",
            "Ad hoc AD Bank queries.",
        ],
        "documents_to_review": [
            "Documentation inventory produced by the target's finance team",
            "Correspondence with the AD Bank regarding missing documents",
        ],
        "management_questions": [
            "For which transaction categories is documentation missing, and "
            "what is the reason?",
            "Can substitute or reconstructed documentation be produced?",
        ],
        "spa_protections": [
            "Document-delivery covenant requiring the target to produce, "
            "before completion, all documentation required for EDPMS / IDPMS closure.",
            "General FEMA compliance indemnity sized to cover exposure from "
            "unverified transactions.",
        ],
    },

    "ad_bank_queries_pending": {
        "weight_key": "ad_bank_queries_pending",
        "title": "Pending AD Bank Queries — Unresolved",
        "regulations": ["reg_18", "reg_19"],
        "heatmap_categories": ["AD Bank Approvals", "Reporting Compliance"],
        "explanation": (
            "The target has unresolved queries raised by its AD Bank in "
            "connection with its export, import, or MTT transactions. Under "
            "Regulation 19 the AD Bank is required to maintain an SOP and "
            "escalation mechanism for such queries; unresolved queries can "
            "indicate either substantive compliance issues or systemic process "
            "failures."
        ),
        "why_it_matters": [
            "Outstanding AD Bank queries are a direct window into the AD's "
            "concerns about the target's compliance profile—the nature of the "
            "queries can itself be diagnostic.",
            "A buyer needs to understand whether pending queries may escalate "
            "to formal AD compliance action or RBI referral post-completion.",
            "AD Bank relationship risk: if the AD is already in a heightened "
            "scrutiny posture regarding the target, this can affect the target's "
            "banking arrangements post-completion.",
        ],
        "potential_consequences": [
            "AD Bank may escalate queries to formal compliance action or RBI referral.",
            "Pending queries may delay or complicate the target's ability to "
            "execute routine export / import transactions.",
        ],
        "documents_to_review": [
            "All correspondence between the target and its AD Bank regarding "
            "compliance queries (last 3 years)",
            "Responses filed by the target to each AD Bank query",
            "Any AD Bank letters indicating a heightened scrutiny posture",
        ],
        "management_questions": [
            "What is the nature and status of each pending AD Bank query?",
            "Has the target engaged external counsel to respond to any query?",
            "Has the AD Bank indicated any intention to escalate any pending "
            "query to RBI?",
        ],
        "spa_protections": [
            "Warranty that there are no pending or threatened AD Bank or RBI "
            "actions, proceedings, or enquiries in connection with FEMA "
            "compliance.",
            "Specific indemnity for any liability, fine, or penalty arising "
            "from resolution of pending AD Bank queries.",
            "Pre-completion covenant requiring the target to keep the buyer "
            "informed of any developments regarding pending queries.",
        ],
    },
}

ISSUE_LIBRARY["exports_invoiced_in_inr"] = {
    "weight_key": None,
    "title": "Exports Invoiced / Settled in INR — Extended Realisation Period Applies",
    "regulations": ["reg_5", "reg_17"],
    "heatmap_categories": ["Export Realisation"],
    "explanation": (
        "The target invoices and/or settles certain export transactions in Indian Rupees. "
        "Under the proviso to Regulation 5, where exports are invoiced and/or settled in INR, "
        "the realisation period extends to 18 months (rather than the standard 15 months). "
        "This changes the benchmark against which any outstanding-receivable analysis should "
        "be assessed for INR-invoiced transactions."
    ),
    "why_it_matters": [
        "Applying the wrong benchmark (15 vs 18 months) could cause the team to overstate "
        "or understate the population of overdue receivables.",
        "The target's finance team and AD Bank should apply the correct benchmark on a "
        "transaction-by-transaction basis — worth confirming in the management Q&A.",
    ],
    "potential_consequences": [
        "No direct compliance consequence — this is a timeline-calibration point relevant "
        "to interpreting the Export Realisation findings in this review.",
    ],
    "documents_to_review": [
        "Listing of export transactions invoiced/settled in INR (to allow correct "
        "15-month or 18-month benchmark to be applied per transaction)",
    ],
    "management_questions": [
        "What proportion of export turnover is invoiced/settled in INR, and is this "
        "tracked separately for realisation-monitoring purposes?",
        "Does the AD Bank automatically apply the 18-month period in EDPMS monitoring "
        "for INR-invoiced transactions?",
    ],
    "spa_protections": [
        "No standalone protection required — relevant as interpretive context for the "
        "Export Realisation findings only.",
    ],
}

ISSUE_LIBRARY["project_exports"] = {
    "weight_key": None,
    "title": "Project Exports — Contract-Based Realisation Terms Apply",
    "regulations": ["reg_5", "reg_15"],
    "heatmap_categories": ["Export Realisation"],
    "explanation": (
        "The target undertakes project exports. Under Regulation 5(1)(c) and Regulation 15, "
        "realisation and repatriation for project exports follow the payment terms of the "
        "underlying contract (not the standard 15/18-month period), subject to AD Bank "
        "satisfaction as to the genuineness of the project. Regulation 15(2) also permits, "
        "subject to AD monitoring, deployment of temporary cash surpluses generated outside "
        "India into short-term instruments abroad (maturity ≤ one year)."
    ),
    "why_it_matters": [
        "The Export Realisation findings should be cross-checked against actual project "
        "contract payment milestones for project-export receivables — a different (potentially "
        "longer) benchmark may apply.",
        "Any offshore cash surpluses from project exports should be disclosed as assets; "
        "their deployment into short-term instruments should be AD-monitored per Regulation 15(2).",
    ],
    "potential_consequences": [
        "Mis-application of the standard realisation period to project-export receivables "
        "could produce a false positive or negative in the Export Realisation analysis.",
        "Undisclosed offshore cash surpluses would be a balance-sheet completeness issue.",
    ],
    "documents_to_review": [
        "Project export contracts setting out payment milestones and terms",
        "AD Bank genuineness approval for the project export(s)",
        "Details of any offshore cash surpluses and their deployment",
    ],
    "management_questions": [
        "What are the payment terms under the project export contract(s), and how do they "
        "compare to realisation periods assumed in this review?",
        "Does the target hold any cash surpluses generated outside India from project "
        "exports, and how are these deployed and disclosed?",
    ],
    "spa_protections": [
        "Disclosure schedule entry describing project export contracts and payment terms.",
        "Balance-sheet / asset disclosure covering any offshore cash surpluses.",
    ],
}
