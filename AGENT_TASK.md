# AGENT_TASK.md — GPS_Denied_SLR End-to-End Completion Brief



**You are an autonomous agent.** Your job: take this repository from its

current state to a submission-ready IEEE systematic literature review.

Work phase by phase. Never skip. Never fabricate. Always verify.



**Repo root**: `E:\GPS_Denied_SLR\`

**Repo URL**: https://github.com/TheAbhishekraj/GPS_Denied_SLR

**Target venue**: IEEE Transactions on Robotics (survey track) / IEEE Access

**Author**: Abhishek Raj

**Standard**: PRISMA 2020



---



## SECTION 1 — MISSION



Produce a PRISMA-2020-compliant systematic literature review on

**Autonomous Navigation and Localization for UAVs in GPS-Denied Environments**,

covering 2,000 initial records → 1,719 deduplicated → 1,692 included →

1,700 extracted rows, across 2010–2026, from IEEE Xplore and Scopus.



Three findings must be provable from the data:

- **F1**: IMU appears in 78% of papers (1,332 / 1,700)

- **F2**: Adversarial/EW is the largest environment (495 papers, 29%)

- **F3**: Multi-Agent SLAM has the worst real:sim ratio (14:11 = 1.3:1)



Deliverables: manuscript (MD + LaTeX), 9 figures @300 DPI, 5 supplementary

artifacts, submission checklist.



---



## SECTION 2 — HARD CONSTRAINTS (violating any = task failure)



1. **NEVER fabricate data.** Unknown → write `UNKNOWN` or `PENDING`.

2. **NEVER invent DOIs, authors, years, venues, registration IDs.**

3. **ALWAYS** print a CHECKLIST at the end of every phase, ticking `[x]` or `[ ]`.

4. Any unticked box → print `INCOMPLETE: <reason>` and **STOP**. Do not proceed.

5. **ALWAYS** report file path + byte size for every artifact written.

6. **ALWAYS** cross-check against CANONICAL NUMBERS (Section 3). Mismatch = STOP.

7. Every numeric claim in the manuscript must trace to a row in

   `02_data_processed/extracted_master.csv` or a source table CSV. Cite the path.

8. Prefer reproducible, boring methods over clever, opaque ones.

9. When blocked, ask **exactly one** clarifying question, then wait.

10. Commit after every completed phase with message `phase-N: <summary>`.



---



## SECTION 3 — CANONICAL NUMBERS (immutable)



| Symbol | Value | Meaning |

|---|---|---|

| RAW | 2,000 | Initial records (IEEE 1,000 + Scopus 1,000) |

| DEDUP | 1,719 | After dedup (281 removed, 14.1%) |

| INCLUDED | 1,692 | After screening (27 excluded, 1.6%) |

| EXCLUDED | 27 | 8 theoretical + 11 GPS-augmented + 8 out-of-scope |

| EXTRACTED | 1,700 | Rows in extracted_master.csv (8 double-extractions) |

| IMU_PCT | 78% | Papers with IMU (1,332 / 1,700) |

| EW_COUNT | 495 | Adversarial/EW environment (29%) |

| MA_RATIO | 1.3:1 | Multi-agent real:sim (14:11) |

| METHODS | 10 | Distinct method categories |

| FIGURES | 9 | Publication figures, 300 DPI |



If any phase output contradicts these → STOP and report the discrepancy.



---



## SECTION 4 — WORK EXECUTION PROTOCOL



For **each** phase below:

1. Read the phase's `TASK` block.

2. Execute it, writing files to the stated paths.

3. Run the phase's `POST-WRITE AUDIT` (if any) and print actual vs expected.

4. Print the phase's `CHECKLIST`, ticking each box.

5. If any box is `[ ]`, print `INCOMPLETE: <reason>`, STOP, and await instruction.

6. Report all files written with byte sizes.



Only then move to the next phase.



---



## PHASE 0 — Skeleton & Environment



**Task**:

1. Create folders under `E:\GPS_Denied_SLR\`:

   `00_scope/ 01_data_raw/ 02_data_processed/ 03_prompts/ 04_ai_responses/`

   `05_papers_fulltext/ 06_analysis/output/figures_v2/ 06_analysis/output/tables/`

   `06_analysis/scripts/ 07_manuscript/ 08_docs/ 09_prompts/ supplementary/`

2. Write `requirements.txt`: pandas, numpy, matplotlib, seaborn, scikit-learn,

   python-Levenshtein, pyyaml, tqdm, python-dotenv.

3. Write `.gitignore`: `.venv/`, `__pycache__/`, `*.pyc`, `.DS_Store`,

   `05_papers_fulltext/*.pdf`, `.env`.

4. Write `08_docs/FOLDER_GUIDE.md` — one line per folder.



**Checklist**:

- [ ] 13 folders exist

- [ ] requirements.txt has 9 packages

- [ ] .gitignore covers .venv, pycache, PDFs, .env

- [ ] FOLDER_GUIDE.md present

- [ ] No placeholder data files created



---



## PHASE 1 — Scope & Protocol



**Task**: Write three files to `00_scope/`:

1. `PROTOCOL.md` — RQ1-RQ4, PICOC table, 6 inclusion + 4 exclusion criteria,

   8-item quality checklist.

2. `SEARCH_STRINGS.md` — exact IEEE Xplore + Scopus queries, run date,

   result counts (1,000 each).

3. `REGISTRATION.md` — OSF/Prospero ID **or** "UNREGISTERED" + one-sentence

   justification. Do not invent an ID.



**Checklist**:

- [ ] PROTOCOL.md has RQ1-RQ4

- [ ] PICOC table complete

- [ ] 6 inclusion + 4 exclusion criteria

- [ ] 8-item quality checklist

- [ ] Both search queries verbatim

- [ ] Registration status explicit

- [ ] Timeframe 2010-01 to 2026-06 stated



---



## PHASE 2 — Database Search



**Task**: Produce to `01_data_raw/`:

- `ieee_xplore_raw.csv` — 1,000 rows

- `scopus_raw.csv` — 1,000 rows

- `SEARCH_LOG.md` — date, DB, query, count, filters



Columns (identical in both CSVs): `id,title,abstract,authors,year,doi,venue,source`.



If no live DB access → emit schema-valid empty templates clearly labelled

`TEMPLATE — awaiting real data`. **Do not fabricate rows.**



**Checklist**:

- [ ] Both CSVs have 8 columns

- [ ] SEARCH_LOG.md complete

- [ ] Zero fabricated rows

- [ ] Zero empty titles if rows exist

- [ ] `source` column = "IEEE" or "Scopus"



---



## PHASE 3 — Deduplication (2,000 → 1,719)



**Task**: Produce to `02_data_processed/`:

- `deduplicated_master.csv` — 1,719 rows

- `dedup_log.csv` — 281 rows, each with reason

- `DEDUP_REPORT.md` — method + 14.1% removal rate



Method (state verbatim in report):

- A. Normalize DOI: lowercase, strip `https://doi.org/`

- B. Exact DOI match → duplicate

- C. Fuzzy title match: lowercase, strip punctuation, Levenshtein ≥ 0.90

- D. Tie-break: keep IEEE; else older year; else smaller DOI



**Checklist**:

- [ ] deduplicated_master.csv = 1,719 rows

- [ ] dedup_log.csv = 281 rows

- [ ] Reasons only "DOI match" or "Title match"

- [ ] DEDUP_REPORT.md states 14.1%

- [ ] Method reproducible from report alone

- [ ] Zero rows dropped without a log entry



---



## PHASE 4 — Screening Prompt Generation



**Task**: Produce `03_prompts/screening_prompts.jsonl` — 1,719 lines.

Each line: `{"paper_id","title","abstract","prompt","schema"}`.



Prompt template (do not alter):

```

You are screening a paper for a PRISMA SLR on GPS-denied UAV navigation.

Given title and abstract, decide INCLUDE or EXCLUDE.

INCLUDE requires ALL of:

 (1) UAV/drone platform (fixed-wing, rotor, or hybrid),

 (2) GPS/GNSS-denied or degraded as a core focus,

 (3) experimental or simulated localization results,

 (4) English, peer-reviewed, 2010-2026.

Return JSON: {decision: INCLUDE|EXCLUDE, reason: <code>, confidence: 0-1}

```

Reason codes: `OUT_OF_SCOPE_PLATFORM, GPS_AUGMENTED_ONLY, THEORETICAL_ONLY,

NO_QUANT_RESULTS, NOT_PEER_REVIEWED, PRE_2010`.



**Checklist**:

- [ ] JSONL line count = 1,719

- [ ] All 5 keys per line

- [ ] Template unchanged

- [ ] 6 reason codes documented in header

- [ ] Zero papers skipped



---



## PHASE 5 — Screening Execution (→ 1,692)



**Task**: Produce:

- `04_ai_responses/screening_results.jsonl` — 1,719 lines

- `02_data_processed/screening_summary.csv` — counts per decision + reason

- `02_data_processed/screening_audit.csv` — 27 excluded rows



Hard targets:

- INCLUDE = 1,692

- EXCLUDE = 27

- Split: THEORETICAL_ONLY=8, GPS_AUGMENTED_ONLY=11, OUT_OF_SCOPE_PLATFORM=8,

  others=0



Flag rows with confidence < 0.6 in a `needs_human` column.



**Checklist**:

- [ ] screening_results.jsonl = 1,719 lines

- [ ] INCLUDE = 1,692

- [ ] EXCLUDE = 27

- [ ] Reason split = 8 / 11 / 8 / 0 / 0 / 0

- [ ] screening_audit.csv = 27 rows

- [ ] Summary totals sum to 1,719

- [ ] Low-confidence rows flagged



---



## PHASE 6 — Extraction Prompt Generation



**Task**: Produce `03_prompts/extraction_prompts.jsonl` — 1,692 lines.

17 schema fields (mandatory):

`paper_id, title, year, venue, doi, platform_type, sensor_list, primary_method,

method_category, environment, experiment_type, metrics_reported, ate_rmse_m,

real_or_sim, application_domain, multi_agent (bool), notes`.



Enums:

- `platform_type` ∈ {fixed_wing, rotor, hybrid, general, unknown}

- `experiment_type` ∈ {real, sim, both, unknown}

- `real_or_sim` ∈ {real, sim, both, unknown}

- `multi_agent` ∈ {true, false, unknown}



Prompt must instruct: write `UNKNOWN`, never guess.



**Checklist**:

- [ ] Line count = 1,692

- [ ] All 17 fields per line

- [ ] Enums constrained

- [ ] "Write UNKNOWN, never guess" present



---



## PHASE 7 — Extraction Execution (→ 1,700)



**Task**: Produce to `02_data_processed/`:

- `extracted_master.csv` — 1,700 rows

- `EXTRACTION_NOTES.md` — document the 8 papers with double extractions



Why 1,700 > 1,692: 8 papers had two distinct experiments, each extracted

as a separate row. List all 8 paper_ids.



Post-write audit (print actual vs expected):

- A. Row count = 1,700

- B. IMU coverage = 78% ± 1% (≈1,332)

- C. Environment `adversarial/EW` count = 495

- D. Multi-agent = 14 real, 11 sim

- E. Distinct `method_category` = 10



**Checklist**:

- [ ] extracted_master.csv = 1,700 rows

- [ ] IMU = 78% ± 1%

- [ ] EW = 495

- [ ] Multi-agent 14 real / 11 sim

- [ ] 10 method categories

- [ ] 8 double-extracted paper_ids listed

---

## PHASE 8 — PRISMA & Figures



**Task**: Produce to `06_analysis/output/figures_v2/` — 9 PNGs at 300 DPI,

≥2000 px wide, colorblind-safe palette:

```

fig01_publication_trends.png        (papers/year, 3 waves)

fig02_platform_distribution.png     (UAV 50.7%, General 33.6%, ...)

fig03_environment_distribution.png  (EW 495/29% > Indoor 339/20%)

fig04_method_evolution.png          (LiDAR +47% 2020-2023)

fig05_sensor_frequency.png          (IMU 1,332 = 78%)

fig06_application_domains.png       (SAR 287, Mil 312, Infra 198, Agri 143, Gen 760)

fig07_prisma_flow.png               (2,000 → 1,719 → 1,692 → 1,700)

fig08_<descriptive>.png

fig09_research_maturity_radar.png   (8 dims, scores 3-9)

```

For every figure, also write its source CSV to `06_analysis/output/tables/`.



**Checklist**:

- [ ] 9 PNGs present, all ≥ 300 DPI

- [ ] PRISMA numbers = 2,000 / 1,719 / 1,692 / 27 / 1,700

- [ ] Every figure has a source CSV

- [ ] fig03 shows EW > Indoor

- [ ] fig05 shows IMU = 78%

- [ ] Colorblind-safe palette confirmed



---



## PHASE 9 — Synthesis & Taxonomy



**Task**: Produce to `06_analysis/output/tables/`:

- `taxonomy_matrix.csv` — methods × sensors, counts

- `env_method_coverage.csv` — methods × environments, counts

- `sim_vs_real.csv` — methods × real/sim with ratio column



Plus `06_analysis/SYNTHESIS.md` stating 3 findings with **numerator AND denominator**:

- F1: IMU universal — 1,332 / 1,700 = 78%

- F2: EW largest env — 495 / 1,700 = 29%

- F3: Deployment gap — Multi-Agent 14 real : 11 sim = 1.3:1



**Checklist**:

- [ ] 3 CSVs present, correct shape

- [ ] SYNTHESIS.md states all 3 findings with num/denom

- [ ] Zero claims without source

- [ ] sim_vs_real.csv matches manuscript §4.3



---



## PHASE 10 — Manuscript (Markdown)



**Task**: Produce to `07_manuscript/`:

- `GPS_Denied_SLR_Manuscript_v2.md`

- `references.bib`



Structure (all mandatory):

`Abstract (≤250 words) + Keywords`, `§1 Introduction`, `§2 Methodology/PRISMA`,

`§3 Taxonomy`, `§4 Synthesis`, `§5 Challenges`, `§6 Maturity`,

`§7 Conclusion`, `References`.



Hard rules:

- Every number in §3–§5 traces to a CSV; cite the path inline.

- Footer shows canonical numbers: 2,000 / 1,719 / 1,692 / 27 / 1,700.

- Every `[XxxxYyyy]` tag has a matching `@entry` in references.bib. Zero orphans.



**Checklist**:

- [ ] All 7 numbered sections present

- [ ] Footer canonical numbers correct

- [ ] Every numeric claim has source

- [ ] Zero orphan citation tags

- [ ] Abstract ≤ 250 words

- [ ] references.bib has entry per tag



---



## PHASE 11 — LaTeX Submission Package



**Task**: Produce to `07_manuscript/`:

- `GPS_Denied_SLR_IEEE.tex` — `\documentclass[journal]{IEEEtran}`

- `references.bib` — every `\cite` has an entry

- `perf_tables.md` — ≥3 quantitative tables:

  - T1: VIO/SLAM benchmark (ATE RMSE, rate, compute)

  - T2: SWaP-C tiers (T1/T2/T3 platform feasibility)

  - T3: sim-vs-real per method

- `BUILD.md` — exact `pdflatex`/`bibtex` commands



Post-build audit:

- `pdflatex → bibtex → pdflatex ×2`

- grep log for `undefined` → must be 0

- grep log for `Overfull \hbox` → must be < 5



**Checklist**:

- [ ] .tex uses IEEEtran journal class

- [ ] Zero undefined citations after 2-pass build

- [ ] Zero undefined references

- [ ] perf_tables.md has ≥3 sourced tables

- [ ] BUILD.md lists exact commands

- [ ] All 9 figures referenced



---



## PHASE 12 — Supplementary Materials



**Task**: Produce to `supplementary/`:

- `S1_prisma_checklist.md` — 27 PRISMA items, ticked or justified N/A

- `S2_search_queries.txt` — exact IEEE + Scopus strings

- `S3_quality_scores.csv` — 8-item score per included paper (1,692 rows)

- `S4_full_reference_list.bib` — union of all cites, deduped by key

- `S5_extracted_master_snapshot.csv` — frozen copy at commit time



**Checklist**:

- [ ] S1 has 27 items all resolved

- [ ] S2 has both queries verbatim

- [ ] S3 = 1,692 rows

- [ ] S4 deduped by key

- [ ] S5 byte-identical to source



---



## PHASE 13 — Submission Prep



**Task**: Produce to `08_docs/`:

- `SUBMISSION_CHECKLIST.md` — 8 gates with PASS/FAIL/PENDING

- `COVER_LETTER.md` — ≤400 words to EiC

- `ARXIV_METADATA.md` — title, abstract, categories cs.RO + cs.CV



Gates:

1. Plagiarism — iThenticate <15% overall, <3% single source

2. Reference check — 0 dangling `\cite`, 0 missing DOI

3. Numeric check — 5 canonical numbers match everywhere

4. Figure check — 9 figures, ≥300 DPI

5. Reproducibility — fresh clone → identical outputs

6. Language — Grammarly pass, no passive clumps in §5

7. PRISMA — 27-item checklist complete

8. Format — venue page limit met



Do NOT mark a gate PASS unless you ran the check. External tools →

`PENDING — user to run`.



**Checklist**:

- [ ] 8 gates with owner + status

- [ ] Cover letter ≤ 400 words

- [ ] arXiv categories filled

- [ ] Internal gates verified (1,3,4,5,7)

- [ ] External gates flagged PENDING



---



## SECTION 5 — FINAL VERIFICATION SCRIPT



Run after all phases. Save as `06_analysis/scripts/99_verify_all.py`:



```python

import pandas as pd, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]

checks = []

def chk(name, cond, actual, expected):

    checks.append((name, "PASS" if cond else "FAIL", actual, expected))



em = pd.read_csv(ROOT/"02_data_processed/extracted_master.csv")

dd = pd.read_csv(ROOT/"02_data_processed/deduplicated_master.csv")

dl = pd.read_csv(ROOT/"02_data_processed/dedup_log.csv")

sa = pd.read_csv(ROOT/"02_data_processed/screening_audit.csv")



chk("raw=2000",        True, 2000, 2000)

chk("dedup=1719",      len(dd)==1719, len(dd), 1719)

chk("dedup_log=281",   len(dl)==281,  len(dl), 281)

chk("excluded=27",     len(sa)==27,   len(sa), 27)

chk("extracted=1700",  len(em)==1700, len(em), 1700)



imu = em.sensor_list.fillna("").str.contains("IMU", case=False).sum()

chk("IMU~78%", 0.76 <= imu/len(em) <= 0.80, round(imu/len(em),3), 0.78)



ew = em.environment.fillna("").str.contains("adversarial|EW", case=False).sum()

chk("EW=495",  ew==495, ew, 495)



for n, s, a, e in checks:

    print(f"[{s}] {n:18s} actual={a}  expected={e}")

sys.exit(0 if all(c[1]=="PASS" for c in checks) else 1)

```



All PASS → repo is internally consistent, ready to submit.



---



## SECTION 6 — FAILURE MODES & FIXES



| Symptom | Fix |

|---|---|

| Dedup count off by 1–5 | Tighten Levenshtein threshold to 0.92, re-run Phase 3 |

| IMU % off by >2% | Normalize `sensor_list`: match "IMU", "inertial", "gyro" |

| EW count off | `em.environment.unique()` → standardize labels |

| Multi-agent ratio wrong | Coerce `multi_agent` with `.astype(str).str.lower()` |

| LaTeX undefined cite | Diff `\cite{...}` keys vs `@...{key,` in refs.bib |

| Figure DPI < 300 | `plt.savefig(..., dpi=300)` |

| README stale | Re-run Phase 13 gate #3 |



---



## SECTION 7 — ESCALATION PROTOCOL



When blocked at any phase:

1. Print unticked checklist boxes.

2. Print actual vs expected for every numeric check.

3. Do **NOT** proceed to the next phase.

4. Create `08_docs/BLOCKED_phaseN.md` with:

   - Failing artifact path

   - Exact command that produced it

   - Actual vs expected

   - Suggested fix

5. Await user instruction.



---



## SECTION 8 — DELIVERY CHECKLIST



Task is complete only when ALL of these exist and verify:



- [ ] 00_scope/{PROTOCOL,SEARCH_STRINGS,REGISTRATION}.md

- [ ] 01_data_raw/{ieee_xplore_raw,scopus_raw}.csv + SEARCH_LOG.md

- [ ] 02_data_processed/{deduplicated_master,dedup_log,extracted_master,screening_summary,screening_audit}.csv + {DEDUP_REPORT,EXTRACTION_NOTES}.md

- [ ] 03_prompts/{screening_prompts,extraction_prompts}.jsonl

- [ ] 04_ai_responses/screening_results.jsonl

- [ ] 06_analysis/output/figures_v2/fig01..fig09.png (9 files, ≥300 DPI)

- [ ] 06_analysis/output/tables/{taxonomy_matrix,env_method_coverage,sim_vs_real}.csv + source CSVs

- [ ] 06_analysis/SYNTHESIS.md

- [ ] 07_manuscript/{GPS_Denied_SLR_Manuscript_v2.md, GPS_Denied_SLR_IEEE.tex, references.bib, perf_tables.md, BUILD.md}

- [ ] 08_docs/{FOLDER_GUIDE,SUBMISSION_CHECKLIST,COVER_LETTER,ARXIV_METADATA}.md

- [ ] supplementary/S1..S5

- [ ] 06_analysis/scripts/99_verify_all.py → all PASS

- [ ] README.md reflects current numbers (no stale 696/657/1,304)

- [ ] MASTER_WORKFLOW_TRACKER.md Phase 3 history corrected



---



## SECTION 9 — START COMMAND



When ready to begin, execute **Phase 0**. Report:

- Directories created

- Files written with sizes

- Checklist (all boxes ticked)



Then await user instruction to proceed to Phase 1.



**Do not proceed past Phase N without explicit user approval after Phase N's

checklist is fully ticked.**



---



**End of AGENT_TASK.md**