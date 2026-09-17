# PDF_EXTRACTION_AUDIT_PROTOCOL.md
# Verification standard for Phase 7 PDF extraction

**Purpose:** Detect shallow, stubbed, or fabricated extraction.
**Applies to:** `06_analysis/scripts/16_execute_phase7_extraction.py` output.
**Frequency:** After every re-extraction run.
**Author:** Abhishek Raj
**Date:** 2026-09-17
**Referenced by:** MASTER_SLR_WRITING_SOP_V2.md §13

---

## WHY THIS EXISTS

Phase 7 extraction ran at 2 minutes for 171 papers. That is only possible
with keyword/regex extraction, not LLM semantic reading. This is a valid
methodology IF documented. It becomes a problem IF the manuscript claims
"full-text analysis" without stating the keyword method.

This protocol enforces three things:
1. Every PDF is actually opened (not just filename-checked)
2. Every extracted value correlates with something in the text
3. Every QA score is justified by a specific phrase in the PDF

---

## THE FIVE CHECKS

### CHECK 1 — PDF Open Verification

**Proves:** the script actually opened and parsed each PDF.

**Method:** For each of N papers, open `05_papers_fulltext/{id}.pdf` with
PyMuPDF. Extract first-page text. Compare to `notes` field in
`extracted_master_v2.csv`.

**PASS:** ≥ 95% of papers have a distinctive text snippet in `notes`
OR a word count consistent with the PDF page count.

**FAIL action:** Script is not reading PDF content. Rewrite.

---

### CHECK 2 — Field-Text Correlation

**Proves:** categorical labels match actual PDF text.

**Method:** Sample 20 papers (seed 42). For each, read first 3 pages.
Check whether assigned `method_category` and `sensor_list` are supported
by keywords in the text.

**PASS:** ≥ 90% of sampled papers have consistent field-text.

**FAIL action:** Extraction logic produces wrong labels. Fix keywords.

---

### CHECK 3 — QA Score Justification

**Proves:** each qa_* score is backed by a specific phrase.

**Method:** For each paper with qa_rigor >= 3, find the ground-truth phrase
that triggered the +2 (e.g., "Vicon" or "mocap").
For each paper with qa_baseline >= 1, find the named baseline.

**PASS:** Every scored field has a matching trigger.

**FAIL action:** Scoring is random or defaulted. Fix.

---

### CHECK 4 — Distribution Sanity

**Proves:** the QA distribution is realistic.

**Method:** Compute Q-high %, Q-low %, Core %. Compare to bounds.

**Bounds:**
- Q-high: 15–25%
- Q-low: 20–35%
- Core: 15–25%
- No single value > 60% of any field

**PASS:** All four bounds met.

**FAIL action:** Re-tune thresholds, re-run.

---

### CHECK 5 — Manual 5-Paper Spot Check

**Proves:** you personally confirm extraction on 5 papers.

**Method:** Sample 5 papers randomly. For each:
1. Open `05_papers_fulltext/{id}.pdf`
2. Read abstract + methods section
3. Verify CSV `method_category` matches the paper
4. Verify `qa_total` reflects the paper's experimental rigor

**PASS:** ≥ 4 of 5 papers match your read.

**FAIL action:** Systematic errors. Stop and rebuild.

---

## AUDIT REPORT TEMPLATE

After running checks 1–4 and manually doing check 5, produce
`08_docs/extraction_audit_report.md`:

```
# Extraction Audit Report
Date: YYYY-MM-DD
Corpus version: V1 / V2
Papers: N

## Check 1 — PDF Open
Result: PASS / FAIL
Percentage with distinctive notes: __%
Flagged papers: <list>

## Check 2 — Field-Text Correlation
Sample size: 20
Consistent: __ / 20
Flagged: <list>

## Check 3 — QA Justification
Papers with unscored Q-high: __
Papers with scored field but no trigger: __
Flagged: <list>

## Check 4 — Distribution
Q-high: __%  (bound 15-25%)
Q-low:  __%  (bound 20-35%)
Core:   __%  (bound 15-25%)
Result: PASS / FAIL

## Check 5 — Manual Spot Check
Papers: <list>
Match: __ / 5
Notes: <any discrepancies>

## Overall Verdict
PASS / FAIL
If FAIL, blocking issue: <specific>
```

---

## WARNING SIGNS OF SHALLOW EXTRACTION

| Signal | Meaning |
|--------|---------|
| Runtime < 10 min for 171 papers | No LLM or PDF parsing |
| notes = "Parsed from N-page PDF" for all | Generic template |
| qa_* uniform (all "5") | Defaulted |
| Distribution all Q-high or all Q-low | Threshold broken |
| Zero UNKNOWN in any field | Fields force-filled |
| Same method_category for > 70% papers | Regex too narrow |
| sensor_list = "" for many papers | Parse failure not flagged |

If you see any of these, run the audit and roll back.

---

## THE AUDIT SCRIPT

Location: `06_analysis/scripts/17_audit_extraction.py`

Interface:
```
python 06_analysis/scripts/17_audit_extraction.py --check=open|fields|qa|dist|all
```

Reads:
- `02_data_processed/extracted_master_v2.csv`
- `05_papers_fulltext/*.pdf`

Writes:
- `08_docs/extraction_audit_report.md`

Exit code:
- 0 if PASS
- 1 if FAIL

---

## WHEN TO RUN THIS

| Trigger | Action |
|---------|--------|
| After every extraction run | `--check=all` |
| After adding PDFs (171→330) | `--check=all` |
| Before manuscript freeze | `--check=all` + manual 5-paper spot check |
| Before submission | Full report in supplementary S10 |

---

## RELATIONSHIP TO HUMAN VALIDATION

| Audit (this file) | Human validation |
|-------------------|------------------|
| Automatic, script-driven | Manual, human reviewers |
| Verifies PDFs are read | Verifies labels correct |
| Detects fabrication | Detects systematic bias |
| Runs in 2 min | Runs in 45 min |

Both are required for publication. This protocol does not replace
the 20-paper human validation.

---

## HOW TO IMPLEMENT A NEW AUDIT SCRIPT

If `17_audit_extraction.py` doesn't exist yet:

1. Write it to implement Checks 1–4 programmatically
2. Accept `--check=open|fields|qa|dist|all`
3. Use PyMuPDF for PDF text extraction (already installed)
4. Handle missing PDFs gracefully
5. Emit `08_docs/extraction_audit_report.md`
6. Exit 0 for PASS, 1 for FAIL
7. No hardcoded paths

Check 5 is manual (see protocol).

End of PDF_EXTRACTION_AUDIT_PROTOCOL.md
