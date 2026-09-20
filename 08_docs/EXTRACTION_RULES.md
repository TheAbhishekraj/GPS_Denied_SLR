# Extraction Rules — GPS_Denied_SLR

## Rule E1 — No fabrication
Every value must come from the PDF. If not found, write NOT_REPORTED.

## Rule E2 — Quote anchoring
Every QUOTE field contains a verbatim sentence plus page number.
Paraphrase is not allowed.

## Rule E3 — Page citation
Use the PDF's internal page numbering if printed, else the
physical page. Record which convention is used in _source_pages.

## Rule E4 — No interpolation
If a metric is given in a figure only, write FIGURE_ONLY [p.N] and
quote the caption.

## Rule E5 — Unit fidelity
Copy the unit exactly as printed (m, cm, %, dB, etc.).
Do not convert.

## Rule E6 — Author honesty
If authors report a range (e.g., "0.13-0.23 m"), copy the range.
Do not compute a midpoint.

## Rule E7 — Baseline honesty
If the paper reports no baseline, write NO_BASELINE.
Do not imply one.

## Rule E8 — Limitations fidelity
Copy the limitations section verbatim (up to 2 sentences) with page.
Do not summarize.

## Rule E9 — Multiple experiments
If the paper reports several experiments, extract the headline
result of the primary experiment and record the others in notes.

## Rule E10 — Taxonomy derivation
taxonomy_category is derived, not extracted. Apply the rule in the
schema. Record the decision in notes.

## Rule E11 — Consistency
Every batch uses the same rules. If a rule is unclear for one paper,
the human decides, and the decision is logged in _AUDIT/rules_log.md.

## Rule E12 — Quote length
Quotes may be 1 to 3 sentences. No longer. If the claim spans more,
cite the page and summarize in notes.
