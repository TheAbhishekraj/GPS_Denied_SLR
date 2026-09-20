# Screening Independence Statement — GPS_Denied_SLR

> Status: RESOLVED — Case C selected by Abhishek Raj on 2026-09-19.

## PRISMA 2020 requirement
PRISMA 2020 items 8 (selection process) and 13a (synthesis
certainty assessment context) require the manuscript to state:
- how many reviewers screened each record,
- whether reviewers worked independently,
- how disagreements were resolved.

## What is currently documented on disk
- screening_results.csv contains one decision per record with no
  reviewer column.
- 00_scope/SCOPE.md Q7 defines a dual-appraiser procedure for
  QUALITY APPRAISAL only (two appraisers independently score 20%
  of papers; ICC(2,1) or weighted Cohen's kappa >= 0.75 before one
  appraiser proceeds solo). No equivalent statement exists for
  title/abstract or full-text screening.

## Disclosure policy for the manuscript
The human must confirm which of the following is true, and the
manuscript Methods section must state it verbatim:

Case A — Single-reviewer screening:
  "All records were screened by a single reviewer. This is
  reported as a limitation in the Limitations section."
  PRISMA 2020 permits single-reviewer screening provided it is
  disclosed.

Case B — Dual-reviewer screening:
  "Two reviewers independently screened [N] records. Disagreements
  were resolved by [consensus / third reviewer]. Agreement was
  [statistic] = [value]."
  Requires evidence on disk of the two decision sets and the
  agreement computation. If that evidence does not exist,
  Case B cannot be claimed.

Case C — Single-reviewer screening with AI assistance:
  "All records were screened by a single human reviewer assisted
  by an AI tool (decision + confidence + criteria + justification
  per record in screening_results.csv). The human verified all AI
  decisions. This is reported as a limitation in the Limitations
  section."
  Evidence on disk: screening_results.csv columns ai_decision,
  ai_confidence, criteria_triggered, justification, decision, rule.
  PRISMA 2020 permits single-reviewer screening with automation
  assistance provided it is disclosed (item 8 and PRISMA-A).

## SELECTED: Case C
Selected by: Abhishek Raj
Date: 2026-09-19

## Rule
Screening independence is resolved as Case C. Manuscript Methods
must state the Case C disclosure verbatim. No marker remains.
