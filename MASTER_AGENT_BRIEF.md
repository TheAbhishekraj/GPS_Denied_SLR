# MASTER_AGENT_BRIEF.md — Complete Project Onboarding Document

**Purpose**: Hand this file to any capable AI agent. After reading, the agent
will know the entire project, determine the current phase, distinguish manual
from automated work, and continue toward completion.

**Author**: Abhishek Raj
**Date**: 2026-09-16
**Status**: Binding. Supersedes all prior onboarding docs.

---

## SECTION 1 — WHAT THIS PROJECT IS

### 1.1 One-sentence summary
A PRISMA-2020-compliant systematic literature review (SLR) on autonomous
navigation and localization for UAVs operating without GPS — built to be
submitted to a peer-reviewed journal (IEEE T-RO / IEEE Access / RAS / Drones).

### 1.2 Why it exists
GPS-denied navigation is a critical unsolved problem in robotics. The
literature is fragmented across robotics, aerospace, computer vision, and
control theory. No prior review covers the 2022-2026 period with PRISMA
methodology. This SLR fills that gap.

### 1.3 The three central findings (must be provable from data)
- **F1**: IMU is the universal substrate — appears in ~78% of papers
- **F2**: Adversarial/EW environments are the largest category (~29%)
- **F3**: A persistent simulation-to-deployment gap exists across methods

### 1.4 Project state at hand-off
- ~50% complete
- Screening done, extraction blocked, manuscript drafted
- Full-text retrieval is the current bottleneck

---

## SECTION 2 — THE THREE GOALS (in priority order)

### Goal 1 — Assemble a defensible full-text corpus
**Target**: 330 PDFs on disk (≥45% coverage of the 636 screened papers).
**Why**: The current 30 PDFs (4.7%) are insufficient for a publishable SLR.
**Success metric**: `05_papers_fulltext/` contains ≥286 valid `%PDF` files.

### Goal 2 — Extract, score, and validate the corpus
**Target**: `extracted_master_v2.csv` with 27 fields per paper, Q-high > 0,
Core > 0, field-level agreement ≥ 90%.
**Why**: Enables evidence-weighted synthesis (the review's unique angle).
**Success metric**: Phase 7b validation report shows all fields PASS.

### Goal 3 — Produce a submission-ready manuscript
**Target**: Manuscript v3 (Markdown + IEEEtran .tex), 9 figures @ 300 DPI,
supplementary S1-S8, 10 submission gates PASS/PENDING.
**Why**: The deliverable is a submitted paper, not a dataset.
**Success metric**: `SUBMISSION_CHECKLIST.md` shows gates resolved.

---

## SECTION 3 — COMPLETE PIPELINE MAP (0 through 15)

This is the entire project in one view. Every step, tool, and status.

| # | Step | Tool | Time | Status | Blocker |
|---|---|---|---|---|---|
| 0 | Verify state | PS | 5 min | ✅ Done | — |
| 1 | Environment setup | Cline | 5 min | ✅ Done | — |
| 2A | Priority list (initial) | Cline | 2 min | ✅ Superseded by 2A-fix | — |
| 2A-fix | Year-stratified list | Cline | 2 min | ✅ Done | — |
| **2B** | **Extended OA retrieval** | **Cline** | **20 min** | **⏳ Current** | **None** |
| 3a | Extra OA sources | Cline | 15 min | Optional | Only if 2B < 50 PDFs |
| **3b** | **Manual IEEE download** | **Human** | **2 hrs** | **Blocked by 2B** | **University access required** |
| 4 | Auto-rename staged PDFs | Cline | 5 min | Blocked by 3b | — |
| 5 | Verify coverage | Cline | 2 min | Blocked by 4 | — |
| 6 | Apply I6 filter | Cline | 2 min | Blocked by 5 | — |
| 7 | Phase 7 extraction (real) | Cline | 2-4 hrs | Blocked by 6 | PDFs must exist |
| 7b | Extraction validation | Cline+human | 1 hr | Blocked by 7 | Human review of 20 papers |
| 7-S | Snowballing | Cline | 1 hr | Blocked by 7b | — |
| 8 | Core paper selection | Cline | 15 min | Blocked by 7-S | — |
| 9 | Figure generation | Cline | 1 hr | Blocked by 8 | — |
| 10 | Manuscript v3 | Cline+human | 2 hrs | Blocked by 9 | — |
| 11 | LaTeX package | Cline | 30 min | Blocked by 10 | — |
| 12 | Supplementary | Cline | 30 min | Blocked by 11 | — |
| 13 | Submission prep | Human | 1 hr | Blocked by 12 | Journal access required |

**Critical path**: 2B → 3b → 4 → 5 → 6 → 7 → 7b → 7-S → 8 → 9 → 10 → 11 → 12 → 13

**Total remaining time**: ~12 hours of human work + AI runtime.

---

## SECTION 4 — MANUAL vs AUTOMATED (crucial distinction)

This is the single most important section for agents. It tells you what YOU
can do and what only a HUMAN can do.

### 4.1 Things ONLY A HUMAN CAN DO (agent cannot proceed without these)

| Task | Why manual | Where |
|---|---|---|
| **IEEE Xplore PDF download** | Requires university library login via browser | Step 3b |
| **Scopus PDF download** | Same — institutional session | Step 3b |
| **Publisher fallback (Springer/Elsevier/Wiley)** | Login required | Step 3b |
| **Human reviewer #1 on validation sample** | Independent judgment needed | Step 7b |
| **Human reviewer #2 on validation sample** | Second independent reviewer | Step 7b |
| **Adjudication of reviewer disagreements** | Third-party decision | Step 7b |
| **Plagiarism check (iThenticate)** | Requires institutional account | Step 13 |
| **Grammarly / language edit** | External tool | Step 13 |
| **Journal portal submission** | Account + forms | Step 13 |
| **Final approval of manuscript** | Author responsibility | Step 13 |

**Rule**: If a step is on this list, the agent must STOP, produce a worksheet
or checklist, and hand off to the human. Do not fabricate.

### 4.2 Things AN AGENT CAN DO AUTOMATICALLY

| Task | Tool | Notes |
|---|---|---|
| Git operations (commit, tag, branch) | shell | Never force-push |
| File read/write | shell | No hardcoded paths |
| Python script execution | venv | Repo-relative paths only |
| PyMuPDF PDF text extraction | Python | 1.28.2 installed |
| DOI regex extraction | Python | `10\.\d{4,9}/...` |
| OpenAlex / S2 / DOAJ / arXiv queries | HTTP API | Rate-limited |
| CSV generation and validation | Python/pandas | — |
| Figure generation | matplotlib | 300 DPI, Okabe-Ito palette |
| Manuscript editing | text | Every number traced to source |
| LaTeX conversion | pandoc + manual | IEEEtran class |
| Consistency checks | Python | 0 mismatches target |
| PRISMA number updates | Python | JSON output |
| Quality rubric scoring | Python + LLM | 0-10 scale per paper |
| Citation tier computation | Python | Per RULINGS.md R4 |
| Snowball citation harvesting | OpenAlex/S2 API | Backward + forward |
| Verification scripts | Python | 99_verify_all.py |

**Rule**: If a step is on this list, the agent MUST execute it fully, verify
the result, and commit. Do not hand off to a human unnecessarily.

### 4.3 Things THAT NEED HUMAN + AGENT TOGETHER

| Step | Agent does | Human does |
|---|---|---|
| 3b | Prepares priority CSV, verifies downloads land | Clicks IEEE links, downloads PDFs |
| 7b | Samples 20 papers, computes agreement | Fills the 20-row worksheet |
| 10 | Drafts manuscript, runs consistency checks | Reviews narrative, approves claims |
| 13 | Runs 5 internal gates | Runs 5 external gates, submits |

### 4.4 How the agent decides: manual or automated?

**Decision tree**:

```
Does this task require...
├── University login? → MANUAL (hand off)
├── Human judgment on data? → MANUAL (produce worksheet, wait)
├── External paid tool (iThenticate, Grammarly)? → MANUAL (flag for user)
├── Journal account? → MANUAL (flag for user)
└── None of the above? → AUTOMATED (execute, verify, commit)
```

**If unsure**: default to AUTOMATED with a verification step. If verification
fails, escalate to MANUAL.

---

## SECTION 5 — HOW TO DETECT THE CURRENT PHASE

When you (the agent) are first invoked, run this detection script. Its output
tells you exactly which step is current. Do not ask the user — derive it.

### 5.1 Detection script

```powershell
cd E:\GPS_Denied_SLR

Write-Output "=== 1. Git HEAD ==="
git log --oneline -1

Write-Output "`n=== 2. Key file presence ==="
$files = @(
  "02_data_processed/screened_included_v2.csv",
  "02_data_processed/screened_included_v2_fulltext.csv",
  "02_data_processed/extracted_master_v2.csv",
  "02_data_processed/core_papers_v2.csv",
  "02_data_processed/prisma_counts_v2.json",
  "08_docs/priority_300_download.csv",
  "08_docs/rename_log.csv",
  "08_docs/download_verification_report.md",
  "08_docs/snowball_log.csv",
  "08_docs/extraction_validation_report.md",
  "08_docs/manuscript_consistency_check.md",
  "08_docs/SUBMISSION_CHECKLIST.md",
  "07_manuscript/GPS_Denied_SLR_Manuscript_v3.md",
  "07_manuscript/GPS_Denied_SLR_IEEE_v3.tex",
  "supplementary/S1_prisma_checklist.md"
)
foreach ($f in $files) {
  $exists = Test-Path $f
  $status = if ($exists) { "EXISTS" } else { "MISSING" }
  Write-Output "  [$status] $f"
}

Write-Output "`n=== 3. PDF counts ==="
$final   = (Get-ChildItem "05_papers_fulltext\*.pdf" -EA SilentlyContinue).Count
$staging = (Get-ChildItem "08_docs\downloads_staging\*.pdf" -EA SilentlyContinue).Count
Write-Output "  Final PDFs: $final"
Write-Output "  Staging PDFs: $staging"
Write-Output "  Total: $($final + $staging)"
Write-Output "  Coverage: $([math]::Round(100*($final+$staging)/636,1))%"

Write-Output "`n=== 4. Scripts present ==="
Get-ChildItem "06_analysis\scripts\*.py" |
  Where-Object { $_.Name -match "^(07b|11_|12_|13_|14_)" } |
  Select-Object -ExpandProperty Name

Write-Output "`n=== 5. Recent commits ==="
git log --oneline -10

Write-Output "`n=== 6. Agent lock ==="
Test-Path ".agent_lock"
```

### 5.2 Interpreting the output

| If you see... | Current step is... | Next action |
|---|---|---|
| No `priority_300_download.csv` | Step 2A | Generate priority list |
| `priority_300_download.csv` exists, no staging PDFs | Step 2B | Run extended OA retrieval |
| Staging PDFs < 200 | Step 3b (in progress) | Continue manual download |
| Staging PDFs ≥ 180, no rename log | Step 4 | Run auto-rename |
| `rename_log.csv` exists, no coverage report | Step 5 | Run coverage verification |
| Coverage report exists, no filtered CSV | Step 6 | Apply I6 filter |
| Filtered CSV exists, no `extracted_master_v2.csv` | Step 7 | Run Phase 7 extraction |
| `extracted_master_v2.csv` exists, no validation report | Step 7b | Run extraction validation |
| Validation report exists, no snowball log | Step 7-S | Run snowballing |
| Snowball log exists, no core papers | Step 8 | Select core papers |
| Core papers exist, no figures | Step 9 | Generate figures |
| Figures exist, no Manuscript_v3.md | Step 10 | Draft manuscript |
| Manuscript_v3.md exists, no .tex | Step 11 | LaTeX conversion |
| .tex exists, no S1-S8 | Step 12 | Supplementary package |
| S1-S8 exist, no SUBMISSION_CHECKLIST | Step 13 | Submission prep |
| SUBMISSION_CHECKLIST exists | DONE | Report final state |

### 5.3 What the agent must report at start

Before doing anything, the agent must state:

```
=== AGENT STARTUP REPORT ===

Current phase detected: <Step N>
Evidence: <which files exist / missing>
Next action required: <specific task>
Blocker: <manual dependency, if any>

What the AGENT will do now: <list>
What the HUMAN must do: <list or "none">

Ready to proceed: YES / NO
=== END REPORT ===
```

Only after this report is printed should the agent act.

---

## SECTION 6 — BINDING RULES (non-negotiable)

Every agent must follow these rules at all times.

```
R1  Single writer. Only one agent on the repo at a time.
    Create .agent_lock at start; remove at end.

R2  No hardcoded paths. Use repo-relative paths only.
    Bad:  E:\GPS_Denied_SLR\02_data_processed\file.csv
    Good: 02_data_processed/file.csv

R3  Verification gate. Every step ends with a verification block.
    If verification fails, fix and retry (max 3 attempts).
    After 3 failures, STOP and escalate.

R4  Honest reporting. Every report states:
    - Inputs (with row counts)
    - Outputs (with row counts)
    - Verification results (raw output)
    - Records that could not be processed

R5  No fabrication. Unknown -> "UNKNOWN". Never invent DOIs, titles, years.

R6  Append-only audit. Every step writes a dated CHANGELOG.md entry:
    phase, timestamp, inputs, outputs, counts, deviations.

R7  Single data chain. Only consume canonical files:
    01_data_raw/* -> 02_data_processed/deduplicated_master.csv ->
    screened_included_v2.csv -> screened_included_v2_fulltext.csv ->
    extracted_master_v2.csv -> core_papers_v2.csv.
    All other files are read-only history.

R8  Rollback safety. Never delete tags. Never force-push.
    If unsure, create a new tag before destructive ops.

R9  Scope discipline. Work only on the assigned step.
    Never refactor unrelated files or improve prompts mid-run.

R10 Escalation. STOP and report (never guess) when:
    - Canonical data chain violates R7
    - Two rules conflict
    - Any verification fails 3 times
    - Unexpected file changes during a run
    - A human-only task is required
```

---

## SECTION 7 — VERIFICATION PROTOCOL

### 7.1 Every step must produce a verification block

Pattern:

```powershell
# Run after completing the step
$check1 = <command>       # What does this expect?
$check2 = <command>       # What does this expect?
$check3 = <command>       # What does this expect?
```

### 7.2 Pass conditions are pre-defined

Each step in MASTER_EXECUTION_PROMPT.md has a Pass Conditions table. If any
condition fails, do not proceed. Fix, or escalate.

### 7.3 Sample verification for common steps

**After Step 4 (auto-rename)**:
```powershell
$final = (Get-ChildItem "05_papers_fulltext\*.pdf").Count
$staged = (Get-ChildItem "08_docs\downloads_staging\*.pdf" -EA SilentlyContinue).Count
Write-Output "Final: $final (expect >= 180)"
Write-Output "Staged left: $staged (expect < 20% of initial)"
```

**After Step 6 (I6 filter)**:
```powershell
$f = (Import-Csv "02_data_processed\screened_included_v2_fulltext.csv").Count
Write-Output "Filtered corpus: $f (expect >= 286)"
Get-Content "02_data_processed\prisma_counts_v2.json"
```

**After Step 7 (extraction)**:
```powershell
$r = Import-Csv "02_data_processed\extracted_master_v2.csv"
Write-Output "Rows: $($r.Count)"
Write-Output "Q-high: $((($r | Where-Object { $_.qa_tier -eq 'Q-high' }).Count))"
Write-Output "Core: $((($r | Where-Object { $_.citation_tier -eq 'Core' }).Count))"
```

### 7.4 Global verification (any time)

```powershell
cd E:\GPS_Denied_SLR
python 06_analysis\scripts\99_verify_all.py
```

Returns PASS/FAIL for:
- Corpus size = 636
- Filtered corpus ≥ 286
- Extracted rows ≥ 286
- Q-high > 0, Core > 0
- PDFs ≥ 286, coverage ≥ 45%
- README clean (no v1 numbers)
- 9 figures present

---

## SECTION 8 — HANDOFF TEMPLATE (agent to human)

When a step requires human action, the agent must produce this handoff
document. Save as `08_docs/HANDOFF_step<N>.md`.

```
# HANDOFF_step<N> — <Step Name>

## What was completed (agent)
- <list>
- <list>
Files written:
- <path> (bytes)
- <path> (bytes)

## What the human must do now
<numbered list of specific manual actions>

## Inputs the human needs
- File: <path>
- Tool: <e.g. IEEE Xplore login>
- Duration: <estimated time>

## When the human returns
Save your work as: <path>
Reply: CONTINUE
Agent will then resume at: <next step>

## What happens if the human cannot proceed
<fallback action>
```

### 8.1 Example: Step 3b handoff

```
# HANDOFF_step3b — Manual IEEE Download

## What was completed (agent)
- Priority list of 300 papers generated
- Staging folder created
- Extended OA retrieval attempted (+N PDFs found)

## What the human must do now
1. Open 08_docs/priority_300_download.csv in Excel
2. Open 08_docs/downloads_staging/ in File Explorer
3. Log into university library portal (IEEE Xplore)
4. For each row: click ieee_link → PDF button → download
5. Move PDF to staging folder (do NOT rename)
6. Type Y in done_Y_N column
7. Repeat until staged count ≥ 180

## Inputs the human needs
- File: 08_docs/priority_300_download.csv
- Tool: IEEE Xplore + university login
- Duration: 2 hours

## When the human returns
Confirm staging count: (Get-ChildItem "08_docs\downloads_staging\*.pdf").Count
Reply: CONTINUE
Agent will then resume at: Step 4 (auto-rename)

## What happens if the human cannot proceed
Log reason to 08_docs/BLOCKED_step3b.md. If university access unavailable,
switch to Path B (scoping review) — target lower-tier venue with 636
abstract-only papers.
```

---

## SECTION 9 — EXAMPLE PROMPTS FOR EACH PHASE

These are ready-to-use prompts. Pick the one matching your current phase.

### 9.1 Step 2B — Extended OA retrieval
```
Execute Step 2B from MASTER_EXECUTION_PROMPT.md.
Run 06_analysis/scripts/07b_retrieve_extended.py.
Report using the STEP 2B REPORT BLOCK.
Do not proceed to Step 3 until I confirm.
```

### 9.2 Step 3a — Extra OA sources
```
Execute Step 3a from MASTER_EXECUTION_PROMPT.md.
Only run if Step 2B added < 50 PDFs.
Query CORE.ac.uk and BASE for missing DOIs.
Report using the STEP 3a REPORT BLOCK.
```

### 9.3 Step 3b — Manual download (agent prepares, human executes)
```
Prepare Step 3b handoff.
Write 08_docs/HANDOFF_step3b.md with the manual workflow.
Verify priority_300_download.csv exists.
Verify 08_docs/downloads_staging/ exists.
Print the handoff for the user.
```

### 9.4 Step 4 — Auto-rename
```
Execute Step 4 from MASTER_EXECUTION_PROMPT.md.
Run 06_analysis/scripts/12_auto_rename.py.
Verify match rate ≥ 85%.
Report using the STEP 4 REPORT BLOCK.
```

### 9.5 Step 5 — Verify coverage
```
Execute Step 5 from MASTER_EXECUTION_PROMPT.md.
Run 06_analysis/scripts/13_verify_downloads.py.
Report coverage by method category.
Report using the STEP 5 REPORT BLOCK.
```

### 9.6 Step 6 — Apply I6 filter
```
Execute Step 6 from MASTER_EXECUTION_PROMPT.md.
Run 06_analysis/scripts/14_apply_i6_filter.py.
Update PRISMA in prisma_counts_v2.json.
Report using the STEP 6 REPORT BLOCK.
```

### 9.7 Step 7 — Phase 7 extraction
```
Execute Phase 7 from MASTER_EXECUTION_PROMPT.md.
Read screened_included_v2_fulltext.csv, parse each PDF with PyMuPDF,
extract 27 fields, score QA rubric, write extracted_master_v2.csv.
Verify: Q-high > 0, Core > 0, all fields populated.
Report using the PHASE 7 REAL REPORT BLOCK.
```

### 9.8 Step 7b — Extraction validation
```
Execute Phase 7b from MASTER_EXECUTION_PROMPT.md.
Part 1: sample 20 papers (seed 42), write blank worksheet, STOP.
Part 2 (after CONTINUE): compute field agreement, write report.
```

### 9.9 Step 7-S — Snowballing
```
Execute Phase 7-S from MASTER_EXECUTION_PROMPT.md.
Harvest citations from Core/Important papers.
Update PRISMA Branch B.
Report using the PHASE 7-S REPORT BLOCK.
```

### 9.10 Step 8 — Core paper selection
```
Execute Phase 8 from MASTER_EXECUTION_PROMPT.md.
Filter to Core/Important AND Q-high/Q-medium.
Write core_papers_v2.csv.
Report using the PHASE 8 REPORT BLOCK.
```

### 9.11 Step 9 — Figures
```
Execute Phase 9 from MASTER_EXECUTION_PROMPT.md.
Generate 9 figures @ 300 DPI from extracted_master_v2.csv.
Verify PRISMA numbers, DPI, pixel width.
Report using the PHASE 9 REPORT BLOCK.
```

### 9.12 Step 10 — Manuscript
```
Execute Phase 10 from MASTER_EXECUTION_PROMPT.md.
Write GPS_Denied_SLR_Manuscript_v3.md.
Zero v1 numbers. Trace every claim to CSV.
Run consistency sweep.
Report using the PHASE 10 REPORT BLOCK.
```

### 9.13 Step 11 — LaTeX
```
Execute Phase 11 from MASTER_EXECUTION_PROMPT.md.
Convert to IEEEtran .tex.
Compile: pdflatex -> bibtex -> pdflatex x2.
Zero undefined refs.
Report using the PHASE 11 REPORT BLOCK.
```

### 9.14 Step 12 — Supplementary
```
Execute Phase 12 from MASTER_EXECUTION_PROMPT.md.
Write S1-S8 files.
Verify each against its source.
Report using the PHASE 12 REPORT BLOCK.
```

### 9.15 Step 13 — Submission
```
Execute Phase 13 from MASTER_EXECUTION_PROMPT.md.
Run 10 gates. Mark each PASS/FAIL/PENDING.
Write SUBMISSION_CHECKLIST.md, COVER_LETTER.md, ARXIV_METADATA.md.
Report using the PHASE 13 REPORT BLOCK.
```

---

## SECTION 10 — ESCALATION PROTOCOL

### 10.1 When the agent must STOP

- Any verification fails 3 consecutive times
- A rule conflict is detected
- A file changes unexpectedly during a run
- Coverage drops below 25%
- Q-high = 0 after extraction
- Two agents attempt to write simultaneously
- A human-only task is required and no handoff was produced

### 10.2 Escalation report template

```
=== ESCALATION ===
Step: <N>
Blocking condition: <one sentence>
Evidence: <raw command output>
Attempts made: <N>
Suggested fix: <what the human or next agent should try>
Awaiting: <specific decision needed>
=== END ESCALATION ===
```

### 10.3 What NOT to do when blocked

- Do NOT invent data to pass a check
- Do NOT skip the failing step and move forward
- Do NOT commit a broken state
- Do NOT force-push
- Do NOT delete files without logging

---

## SECTION 11 — THE STARTUP PROMPT (paste this into any agent)

This is the exact message to send to a new agent to bring them up to speed.

```
You are joining an in-progress systematic literature review project.

READ FIRST (in order):
1. MASTER_AGENT_BRIEF.md — this file (context, rules, pipeline)
2. MASTER_EXECUTION_PROMPT.md — step-by-step execution guide
3. MASTER_PROMPT_FINAL.md — binding rules (R1-R8)
4. CHANGELOG.md — recent activity

YOUR TASK NOW:
1. Read the 4 files above.
2. Run the detection script in MASTER_AGENT_BRIEF.md Section 5.1.
3. Print an AGENT STARTUP REPORT:
   - Current phase detected
   - Evidence
   - Next action required
   - What YOU will do
   - What the HUMAN must do
4. Wait for user confirmation before executing.

RULES YOU MUST FOLLOW:
- R1-R10 from MASTER_AGENT_BRIEF.md Section 6
- Create .agent_lock at start; remove at end
- Never fabricate data
- Always verify before committing
- Escalate when blocked (Section 10)

DO NOT:
- Run any step beyond the detected current phase
- Modify files outside the current step's scope
- Trust a previous agent's "done" without verifying

After reading and running detection, print the STARTUP REPORT.
Do not execute any phase until the user replies APPROVED.
```

### 11.1 What a good startup report looks like

```
=== AGENT STARTUP REPORT ===

Files read: 4/4
Detection script executed: YES

Current phase detected: Step 2B — Extended OA retrieval
Evidence:
  - 02_data_processed/screened_included_v2.csv EXISTS (636 rows)
  - 08_docs/priority_300_download.csv EXISTS (300 rows)
  - 05_papers_fulltext/ has 30 PDFs
  - 08_docs/downloads_staging/ empty
  - No rename_log.csv
  - No extracted_master_v2.csv

Next action required: Run 07b_retrieve_extended.py

What I (agent) will do:
  1. Verify 07b script has no hardcoded paths
  2. Run 07b_retrieve_extended.py (~20 min, rate-limited)
  3. Verify new PDFs on disk vs log claims (delta ≤ 5)
  4. Commit updated fulltext_retrieval_log.csv
  5. Report STEP 2B results

What the HUMAN must do: Nothing for this step

Blocker: None

Ready to proceed: YES (awaiting APPROVED)
=== END REPORT ===
```

---

## SECTION 12 — QUICK REFERENCE CARD

Print this and keep visible.

### Current phase quick lookup
| See this file... | You are at... |
|---|---|
| No priority_300_download.csv | Step 2A |
| priority_300_download.csv, no staging PDFs | Step 2B |
| Staging PDFs growing | Step 3b (in progress) |
| Staging complete, no rename_log.csv | Step 4 |
| rename_log.csv exists | Step 5 |
| Coverage report exists | Step 6 |
| Filtered CSV exists | Step 7 |
| extracted_master_v2.csv exists | Step 7b |
| Extraction validation report exists | Step 7-S |
| snowball_log.csv exists | Step 8 |
| core_papers_v2.csv exists | Step 9 |
| figures_v2 has 9 PNGs | Step 10 |
| Manuscript_v3.md exists | Step 11 |
| IEEE_v3.tex exists | Step 12 |
| S1-S8 exist | Step 13 |
| SUBMISSION_CHECKLIST.md exists | DONE |

### Files that MUST exist (canonical chain)
```
02_data_processed/deduplicated_master.csv          (1,719)
02_data_processed/screened_included_v2.csv         (636)
02_data_processed/screened_included_v2_fulltext.csv (≥286)
02_data_processed/extracted_master_v2.csv          (≥286)
02_data_processed/core_papers_v2.csv
02_data_processed/prisma_counts_v2.json
05_papers_fulltext/*.pdf                           (≥286)
06_analysis/output/figures_v2/*.png                (9 @ 300 DPI)
07_manuscript/GPS_Denied_SLR_Manuscript_v3.md
07_manuscript/GPS_Denied_SLR_IEEE_v3.tex
supplementary/S1_prisma_checklist.md
08_docs/SUBMISSION_CHECKLIST.md
```

### Commands you will run often
```powershell
# Activate venv
cd E:\GPS_Denied_SLR; .\.venv\Scripts\Activate.ps1

# Check PDF count
(Get-ChildItem "05_papers_fulltext\*.pdf").Count

# Check staging count
(Get-ChildItem "08_docs\downloads_staging\*.pdf").Count

# Run global verification
python 06_analysis\scripts\99_verify_all.py

# Commit
git add -A; git commit -m "<message>"
```

---

## SECTION 13 — FINAL CHECKLIST (before declaring DONE)

The agent must verify ALL of these before reporting completion.

```
=== PROJECT COMPLETION CHECKLIST ===

CORPUS:
[ ] ≥330 PDFs on disk (of 636)
[ ] Coverage ≥45%
[ ] Every method category has ≥5 papers

EXTRACTION:
[ ] extracted_master_v2.csv exists (≥286 rows)
[ ] Q-high > 0
[ ] Core > 0
[ ] All 27 fields populated
[ ] Field-level agreement ≥90% (Phase 7b)
[ ] Snowball log complete
[ ] PRISMA branches separate

FIGURES:
[ ] 9 PNGs @ 300 DPI, ≥2000px wide
[ ] Every figure has source CSV
[ ] PRISMA numbers match prisma_counts_v2.json

MANUSCRIPT:
[ ] All 7 sections + abstract + appendices
[ ] Zero v1 numbers (1,692, 1,332, 98.4)
[ ] Consistency sweep: 0 mismatches
[ ] Performance tables cite QA tiers
[ ] README regenerated with v2 numbers

LATEX:
[ ] IEEEtran class
[ ] Zero undefined citations
[ ] Zero undefined references
[ ] All 9 figures referenced
[ ] Compiles to PDF

SUPPLEMENTARY:
[ ] S1-S8 present
[ ] S3 row count == extracted_master_v2 rows
[ ] S6 verbatim match to source

SUBMISSION:
[ ] 10 gates have PASS or PENDING
[ ] Internal gates verified
[ ] External gates flagged for human
[ ] COVER_LETTER.md ≤400 words
[ ] ARXIV_METADATA.md complete

GOVERNANCE:
[ ] CHANGELOG has one entry per step
[ ] No .agent_lock left behind
[ ] No uncommitted changes
[ ] All tags preserved
[ ] README updated

VERIFICATION:
[ ] 99_verify_all.py returns all PASS

If ALL boxes ticked: report DONE.
If ANY unticked: report INCOMPLETE with the specific gap.
=== END CHECKLIST ===
```

---

## SECTION 14 — APPENDIX: FULL PROJECT HISTORY

For context, here is what happened before this brief was written.

| Date | Event | Commit |
|---|---|---|
| Aug 2026 | Initial search (2,000 records) | early |
| Sep 2026 | Deduplication (1,719 unique) | 60928c6 ancestors |
| Sep 2026 | v1 screening (loose criteria, 1,692 included) | superseded |
| Sep 14 | v2 criteria drafted (I2 rule added) | 524d763 |
| Sep 15 | v2 screening (636 included, 37%) | 60928c6 |
| Sep 15 | Human validation (kappa=0.874, ACCEPT) | 60928c6 |
| Sep 15 | Phase 7 stub attempt (abstract-only) | 35e23bb (archived) |
| Sep 16 | Rollback to 60928c6 | post-rollback |
| Sep 16 | Step 1: environment setup | 1e25d019 |
| Sep 16 | Step 2A: priority list (300 papers) | d3ad2496 |
| Sep 16 | Step 2A-fix: year-stratified | d3ad2496 |
| **Sep 16** | **Current: Step 2B — extended OA retrieval** | **next commit** |

The "broken" attempt at Phase 7 (35e23bb) is preserved under tag
`archive-broken-phase7-10` for audit purposes. Do not use it.

---

**End of MASTER_AGENT_BRIEF.md**
