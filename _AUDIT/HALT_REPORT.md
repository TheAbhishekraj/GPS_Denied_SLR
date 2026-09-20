# HALT REPORT — Interpretive Pass Capacity Limit

Generated: 2026-09-19T21:10:00Z
Scope: Full-run authorization for 274 per-PDF summaries
Status: HALTED — capacity constraint; no fabrication possible at required scale

## Condition (rule triggered)
Rule 6 (stop-and-report) + no-fabrication policy. The task requires reading
each paper's archived text (~17-85 KB) and writing an 18-section summary with
verbatim quotes. Measured pilot throughput: ~23 KB read + ~10 KB written +
~4-6 tool calls per paper. Remaining: 274 papers -> ~6+ MB read, ~2.7 MB
written, ~1,100+ tool calls. This exceeds a single session's context capacity.
Attempting it would end in either (a) unreported partial delivery, or
(b) summaries generated without reading the papers = fabricated quotes.

## Completed so far
- Pilot: 5 of 279 (REC_0001, REC_0003, REC_0006, REC_0008, REC_0010) —
  human-approved.
- 274 remain: BATCH_B01 remainder (REC_0013, REC_0017, REC_0022, REC_0025,
  REC_0028) and all of B02-B28.

## No files were harmed
- No summary beyond the pilot was written.
- No frozen file touched. MASTER_EVIDENCE.csv untouched (279 rows).
- No figures, no synthesis regeneration, no manuscript regeneration.

## Options (human decision required)
A. CHUNKED SESSIONS — continue as-is, ~20-25 summaries per session,
   human issues "continue" each time. ~11-14 sessions. Zero new approvals.
B. HYBRID MECHANICAL + CURATED (needs Rule 9 spec + approval) — a read-only
   pre-extractor script (06_analysis/scripts/prepare_summary_input.py) that,
   per paper, emits a compact work-file (~3-5 KB): YAML bibliographic fields,
   located section headers, and candidate verbatim sentences (with [p.N]) for
   limitations / future work / metrics / baselines, flagged curated=false.
   I then read the work-file + skim the page text and write the final summary.
   Cuts per-paper context dramatically; estimated 25-40 summaries per session.
   The summary remains human-curated; the script never writes a summary.
C. TIERED TEMPLATE — full 18-section summaries only for papers reporting
   quantitative results; reduced template (sections 1-7, 10-17) for purely
   qualitative papers. Reduces volume ~30-40%. Needs human approval of the
   reduced template.

## Recommendation
Option B (with the Rule 9 spec presented for approval), then Option A's
chunking. This preserves the no-fabrication guarantee while making the
279-paper target reachable.

## Current state
- 5 summaries exist and are approved.
- OVERNIGHT_PROGRESS.md and action_log.md carry the pilot record.
- Nothing pending write.
