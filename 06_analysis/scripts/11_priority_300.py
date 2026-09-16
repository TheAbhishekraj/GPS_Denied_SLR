"""Generate prioritized 300-paper download list."""
import csv, pathlib, urllib.parse
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[2]
IN   = ROOT/"02_data_processed/screened_included_v2.csv"
PDF_DIR = ROOT/"05_papers_fulltext"
OUT  = ROOT/"08_docs/priority_300_download.csv"

have = {p.stem for p in PDF_DIR.glob("*.pdf")}
rows = [r for r in csv.DictReader(IN.open(encoding="utf-8-sig"))
        if (r.get("id") or r.get("paper_id")) not in have]

cat_counts = Counter(r.get("method_category", "unknown") for r in rows)
small_cats = {c for c, n in cat_counts.items() if n <= 15}

def score(r):
    s = 0
    if (r.get("qa_tier") or "").upper() == "Q-MEDIUM": s += 10000
    try: s += int(r.get("year") or 0) * 10
    except: pass
    if (r.get("doi") or "").strip(): s += 100
    if r.get("method_category", "") in small_cats: s += 500
    return s

rows.sort(key=score, reverse=True)
top = rows[:300]

def enc(s): return urllib.parse.quote_plus((s or "").strip())

with OUT.open("w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["priority","id","filename","title","year","source","doi",
                "method_category","qa_tier","ieee_link","doi_link",
                "scholar_link","done_Y_N","notes"])
    for i, r in enumerate(top, 1):
        pid = r.get("id") or r.get("paper_id")
        doi = (r.get("doi") or "").strip()
        title = (r.get("title") or "").strip()
        w.writerow([
            i, pid, f"{pid}.pdf", title, r.get("year",""),
            r.get("source",""), doi,
            r.get("method_category",""), r.get("qa_tier",""),
            f"https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={enc(doi or title)}",
            f"https://doi.org/{doi}" if doi else "",
            f"https://scholar.google.com/scholar?q={enc(title)}",
            "", ""
        ])

print(f"Already have: {len(have)}")
print(f"Total missing: {len(rows)}")
print(f"Small categories boosted: {sorted(small_cats)}")
print(f"Top 300 selected")
print(f"Written: {OUT}")
