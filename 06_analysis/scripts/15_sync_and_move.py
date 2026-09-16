"""
sync_and_move.py
Robust PDF matcher using PyMuPDF (fitz) to identify, rename, and move
all staged PDFs to 05_papers_fulltext/ as REC_XXXX.pdf, then update
priority_300_download.csv (done_Y_N = Y) and rename_log.csv.
"""
import csv
import difflib
import os
import pathlib
import re
import shutil
import pymupdf

ROOT = pathlib.Path(__file__).resolve().parents[2]
CSV_PRIORITY = ROOT / "08_docs/priority_300_download.csv"
CSV_SCREENED = ROOT / "02_data_processed/screened_included_v2.csv"
STAGING_DIR = ROOT / "08_docs/downloads_staging"
DEST_DIR = ROOT / "05_papers_fulltext"
LOG_FILE = ROOT / "08_docs/rename_log.csv"

# Load priority 300
priority_rows = list(csv.DictReader(CSV_PRIORITY.open(encoding="utf-8-sig")))
# Load screened 636
screened_rows = list(csv.DictReader(CSV_SCREENED.open(encoding="utf-8-sig")))

all_papers = {}
for r in screened_rows:
    all_papers[r["id"]] = {
        "id": r["id"],
        "title": r["title"],
        "doi": r.get("doi", "").strip(),
        "in_300": False,
    }
for r in priority_rows:
    if r["id"] in all_papers:
        all_papers[r["id"]]["in_300"] = True
    else:
        all_papers[r["id"]] = {
            "id": r["id"],
            "title": r["title"],
            "doi": r.get("doi", "").strip(),
            "in_300": True,
        }

staged_files = sorted(STAGING_DIR.glob("*.pdf"))
print(f"Total files in staging: {len(staged_files)}")

log_entries = []
moved_count = 0
dup_count = 0
unmatched_count = 0

for pdf in staged_files:
    # 1. Extract text from PDF using PyMuPDF
    text = ""
    try:
        doc = pymupdf.open(pdf)
        for pno in range(min(len(doc), 3)):
            t = doc[pno].get_text("text")
            text += " " + t
            # If we already have substantial text (> 400 chars), stop reading pages
            if len(text.strip()) > 400:
                break
        doc.close()
    except Exception as e:
        text = ""

    clean_text = " ".join(text.split()).lower()
    first_lines = " ".join(text.split()[:200]).lower()

    matched_id = None
    match_method = ""

    # Strategy A: DOI exact match in text
    for pid, pdata in all_papers.items():
        pdoi = pdata["doi"].lower()
        if pdoi and len(pdoi) > 6 and pdoi in clean_text:
            matched_id = pid
            match_method = f"DOI match ({pdoi})"
            break

    # Strategy B: Title phrase match (first 5-6 words of title in text)
    if not matched_id:
        for pid, pdata in all_papers.items():
            ptitle = pdata["title"].strip().lower()
            clean_title = re.sub(r"[^a-z0-9 ]", " ", ptitle)
            words = [w for w in clean_title.split() if len(w) > 3]
            if len(words) >= 4:
                phrase = " ".join(words[:6])
                if phrase in re.sub(r"[^a-z0-9 ]", " ", clean_text):
                    matched_id = pid
                    match_method = f"Title phrase: {ptitle[:40]}"
                    break

    # Strategy C: Fuzzy filename match against titles
    if not matched_id:
        stem = pdf.stem.replace("_", " ").replace("-", " ").lower()
        titles = [pdata["title"].lower() for pdata in all_papers.values()]
        close = difflib.get_close_matches(stem, titles, n=1, cutoff=0.55)
        if close:
            for pid, pdata in all_papers.items():
                if pdata["title"].lower() == close[0]:
                    matched_id = pid
                    match_method = f"Fuzzy filename: {close[0][:40]}"
                    break

    # Strategy D: High word overlap between paper title and PDF intro text
    if not matched_id:
        best_score = 0
        best_id = None
        text_words = set(re.findall(r"\b[a-z]{4,}\b", first_lines))
        for pid, pdata in all_papers.items():
            words = set(re.findall(r"\b[a-z]{4,}\b", pdata["title"].lower()))
            if len(words) < 4:
                continue
            overlap = len(words.intersection(text_words))
            score = overlap / len(words)
            if score > best_score and score >= 0.70:
                best_score = score
                best_id = pid
        if best_id:
            matched_id = best_id
            match_method = f"Word overlap ({best_score:.2f}): {all_papers[best_id]['title'][:40]}"

    # Process match outcome
    if matched_id:
        dest_pdf = DEST_DIR / f"{matched_id}.pdf"
        if dest_pdf.exists():
            dup_count += 1
            # Remove duplicate from staging
            pdf.unlink()
            log_entries.append({
                "original": pdf.name,
                "rec_id": matched_id,
                "status": "duplicate_removed",
            })
            print(f"[DUP] {pdf.name[:45]:45s} -> {matched_id} (already on disk, staging cleaned)")
        else:
            shutil.move(str(pdf), str(dest_pdf))
            moved_count += 1
            log_entries.append({
                "original": pdf.name,
                "rec_id": matched_id,
                "status": "moved",
            })
            print(f"[OK]  {pdf.name[:45]:45s} -> {matched_id} [{match_method}]")
    else:
        unmatched_count += 1
        log_entries.append({
            "original": pdf.name,
            "rec_id": "UNKNOWN",
            "status": "unmatched",
        })
        print(f"[XX]  {pdf.name[:45]:45s} -> UNMATCHED")

# Update rename_log.csv
existing_log = []
if LOG_FILE.exists():
    existing_log = list(csv.DictReader(LOG_FILE.open(encoding="utf-8-sig")))

combined_log = existing_log + log_entries
with LOG_FILE.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["original", "rec_id", "status"])
    writer.writeheader()
    for row in combined_log:
        writer.writerow(row)

# Update done_Y_N in priority_300_download.csv
disk_ids = {p.stem for p in DEST_DIR.glob("*.pdf")}
marked_y_count = 0
for r in priority_rows:
    if r["id"] in disk_ids:
        r["done_Y_N"] = "Y"
        marked_y_count += 1

with CSV_PRIORITY.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(priority_rows[0].keys()))
    writer.writeheader()
    for r in priority_rows:
        writer.writerow(r)

total_fulltext = len(list(DEST_DIR.glob("*.pdf")))
stg_remaining = len(list(STAGING_DIR.glob("*.pdf")))

print("\n" + "=" * 60)
print(f"Sync Results:")
print(f"  Moved new PDFs to 05_papers_fulltext/ : {moved_count}")
print(f"  Duplicate staged PDFs cleaned up     : {dup_count}")
print(f"  Unmatched files remaining             : {unmatched_count}")
print(f"  Staging folder remaining              : {stg_remaining}")
print(f"  Total fulltext PDFs on disk           : {total_fulltext} / 636 ({100*total_fulltext/636:.1f}%)")
print(f"  Priority 300 papers marked done (Y)   : {marked_y_count} / 300")
print("=" * 60)
