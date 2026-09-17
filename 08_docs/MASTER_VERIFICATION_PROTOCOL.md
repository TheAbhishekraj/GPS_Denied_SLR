# MASTER_VERIFICATION_PROTOCOL.md
# Manual verification of MASTER_EVIDENCE_V1.csv and per-paper MDs

Run this after the extraction agent reports completion. Do not write the
manuscript until all checks below pass.

Working directory: E:\GPS_Denied_SLR

## Check V1 — Row count and ID integrity

```powershell
$ev = Import-Csv 02_data_processed\MASTER_EVIDENCE_V1.csv
$ms = Import-Csv 02_data_processed\extracted_master_v2.csv

"evidence rows: $($ev.Count)"
"master rows:   $($ms.Count)"

$orphan = $ev | Where-Object { $_.id -notin $ms.id }
"orphan ids: $($orphan.Count)"
$orphan | Format-Table id, title
```
PASS: evidence rows = 171, orphan ids = 0.

## Check V2 — Per-paper MD coverage

```powershell
$md = Get-ChildItem 03_extraction\per_paper\*.md
"md files: $($md.Count)"
$missing = $ms | Where-Object { "$($_.id).md" -notin $md.Name }
"missing md: $($missing.Count)"
$missing | Format-Table id
```
PASS: 171 md files, missing = 0.

## Check V3 — NOT_REPORTED density (sanity, not a pass/fail)

```powershell
$ev = Import-Csv 02_data_processed\MASTER_EVIDENCE_V1.csv
$metrics = 'best_ate_rmse','best_rpe','drift_rate_pct','success_rate_pct',
           'improvement_vs_baseline_pct','baseline_compared',
           'hardware_platform','compute_onboard','ground_truth_method'
foreach ($m in $metrics) {
  $nr = ($ev | Where-Object { $_.$m -eq 'NOT_REPORTED' }).Count
  "{0,-32} NOT_REPORTED: {1}/171" -f $m, $nr
}
```
If a field is NOT_REPORTED in >90% of rows, treat it as a real corpus limitation
and say so in the manuscript. Do not try to fill it by guessing.

## Check V4 — Forbidden numbers

```powershell
$files = Get-ChildItem 02_data_processed,03_extraction,08_docs -Recurse -Include *.csv,*.md |
         Where-Object { $_.FullName -notmatch 'MASTER_SLR_WRITING_SOP_V2' }
$bad = Select-String -Path $files.FullName -Pattern '1,692|1,700|1,719|2,000|1,332|495|98\.4%'
"forbidden matches: $(@($bad).Count)"
$bad | Select-Object Path, LineNumber, Line | Format-Table
```
PASS: 0 matches in new artifacts.

## Check V5 — QA reconciliation

```powershell
$ev = Import-Csv 02_data_processed\MASTER_EVIDENCE_V1.csv
$ms = Import-Csv 02_data_processed\extracted_master_v2.csv
$map = @{}; $ms | ForEach-Object { $map[$_.id] = $_ }
$mismatch = $ev | Where-Object { $map[$_.id].qa_total -ne $_.qa_total }
"qa_total mismatches: $($mismatch.Count)"
$mismatch | Select-Object id, qa_total | Format-Table
```
PASS: 0 mismatches.

## Check V6 — Human verification sample (34 rows)

`08_docs/MASTER_EVIDENCE_VERIFY_SAMPLE.csv` was produced by the agent. You must
fill it manually.

For each of the 34 sampled rows:
1. Open the PDF at `05_papers_fulltext/<id>.pdf`.
2. For each of these CSV fields, compare to the paper:
   - `abstract_summary`
   - `approach_family`
   - `sensors_used`
   - `best_ate_rmse` and `best_ate_rmse_unit`
   - `baseline_compared`
   - `claimed_novelty`
   - `environment_category`
   - `real_or_sim`
3. Add two columns to the sample CSV:
   - `human_verdict` = `MATCH` / `MISMATCH` / `PARTIAL`
   - `human_notes` = one line per mismatch explaining what was wrong
4. Save the updated file as `08_docs/MASTER_EVIDENCE_VERIFY_SAMPLE_DONE.csv`.

Then:

```powershell
$v = Import-Csv 08_docs\MASTER_EVIDENCE_VERIFY_SAMPLE_DONE.csv
"MATCH:   $(($v | ? human_verdict -eq 'MATCH').Count) / 34"
"MISMATCH:$(($v | ? human_verdict -eq 'MISMATCH').Count) / 34"
"PARTIAL: $(($v | ? human_verdict -eq 'PARTIAL').Count) / 34"
```
PASS criterion: MATCH + PARTIAL ≥ 30/34 (≥ 88%).

If below 30, the AI extraction is not reliable enough. Fix the prompt's
extraction rules, re-run Step 2 of the master prompt, then re-sample.

## Check V7 — Cross-tab sanity (distribution must match canonical vectors)

```powershell
$ev = Import-Csv 02_data_processed\MASTER_EVIDENCE_V1.csv
"qa_tier:";      $ev | Group-Object qa_tier | Select-Object Name,Count
"citation_tier:";$ev | Group-Object citation_tier | Select-Object Name,Count
"real_or_sim:";  $ev | Group-Object real_or_sim | Select-Object Name,Count
```
PASS: identical to canonical vectors (Q-high 38 / Q-medium 84 / Q-low 49;
Core 35 / Important 87 / Peripheral 49; Real_World 22 / Simulation 78 / Both 71).

## Check V8 — Spot-read 3 per-paper MDs

Pick three at random:

```powershell
Get-Random -InputObject (Get-ChildItem 03_extraction\per_paper\*.md) -Count 3
```

Open each. Confirm:
- All 15 sections of the template are present.
- No field is blank (must be `NOT_REPORTED` or `NOT_STATED` if missing).
- `extraction_source` cites a real page / table / figure.
- The abstract summary is in the extractor's own words, not the paper's abstract
  copied verbatim.

PASS: all three pass.

## Check V9 — Derived inference tables can be built

Confirm the CSV is analytically usable:

```powershell
$ev = Import-Csv 02_data_processed\MASTER_EVIDENCE_V1.csv
$ev | Group-Object approach_family |
  ForEach-Object {
    $ate = $_.Group | Where-Object { $_.best_ate_rmse -ne 'NOT_REPORTED' -and $_.best_ate_rmse -match '^\d' }
    [pscustomobject]@{
      Family        = $_.Name
      Papers        = $_.Count
      With_ATE      = $ate.Count
      Best_ATE_m    = ($ate | ForEach-Object {[double]$_.best_ate_rmse} | Measure-Object -Minimum).Minimum
    }
  } | Sort-Object Papers -Descending | Format-Table
```
PASS: at least 5 families return a numeric Best_ATE_m.

If fewer than 5 families return numeric ATE, the corpus cannot support an
accuracy-comparison review. Reframe the manuscript as an architectural /
thematic SLR and note the limitation explicitly. Do NOT fabricate values.

## Sign-off

Record in `08_docs/MASTER_VERIFICATION_REPORT.md`:

| Check | Result | Notes |
|---|---|---|
| V1 row/ID integrity | | |
| V2 MD coverage | | |
| V3 NOT_REPORTED density | | |
| V4 forbidden numbers | | |
| V5 QA reconciliation | | |
| V6 human sample | | |
| V7 canonical vectors | | |
| V8 spot-read 3 MDs | | |
| V9 inference viability | | |

Auditor: __________________  Date: ______________  Commit: ______________

Only when V1–V9 pass do you proceed to rewrite the manuscript V1_171_EVIDENCE.md.

End of MASTER_VERIFICATION_PROTOCOL.md