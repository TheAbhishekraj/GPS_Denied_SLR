"""Generate prioritized download list, year-stratified."""
import csv, pathlib, urllib.parse
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[2]
IN   = ROOT/"02_data_processed/screened_included_v2.csv"
PDF_DIR = ROOT/"05_papers_fulltext"
OUT  = ROOT/"08_docs/priority_300_download.csv"

have = {p.stem for p in PDF_DIR.glob("*.pdf")}
missing = [r for r in csv.DictReader(IN.open(encoding="utf-8-sig"))
           if (r.get("id") or r.get("paper_id")) not in have]

# Year-stratified: 100 recent, 100 mid, 100 classic
buckets = {"recent": [], "mid": [], "classic": []}
for r in missing:
    try: y = int(r.get("year") or 0)
    except: y = 0
    if y >= 2024:   buckets["recent"].append(r)
    elif y >= 2020: buckets["mid"].append(r)
    else:           buckets["classic"].append(r)

# Sort within each bucket: has DOI first, then newest
def bkey(r):
    has_doi = 1 if (r.get("doi") or "").strip() else 0
    try: y = int(r.get("year") or 0)
    except: y = 0
    return (-has_doi, -y)

for k in buckets: buckets[k].sort(key=bkey)

# Take 100 from each; backfill from others if a bucket is short
def take(lst, n):
    out = lst[:n]; rest = lst[n:]
    return out, rest

recent, r_extra = take(buckets["recent"], 100)
mid,    m_extra = take(buckets["mid"],    100)
classic, c_extra = take(buckets["classic"],100)

# Backfill shortfalls from whichever bucket has spares
deficit = 300 - (len(recent)+len(mid)+len(classic))
pool = r_extra + m_extra + c_extra
if deficit > 0:
    pool.sort(key=bkey)
    top_up = pool[:deficit]
    for r in top_up:
        try: y = int(r.get("year") or 0)
        except: y = 0
        if y >= 2024: recent.append(r)
        elif y >= 2020: mid.append(r)
        else: classic.append(r)

final = recent + mid + classic

def enc(s): return urllib.parse.quote_plus((s or "").strip())

with OUT.open("w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["priority","id","filename","title","year","source","doi",
                "bucket","ieee_link","doi_link","scholar_link",
                "done_Y_N","notes"])
    for i, r in enumerate(final, 1):
        pid = r.get("id") or r.get("paper_id")
        doi = (r.get("doi") or "").strip()
        title = (r.get("title") or "").strip()
        try: y = int(r.get("year") or 0)
        except: y = 0
        bucket = "recent" if y >= 2024 else ("mid" if y >= 2020 else "classic")
        w.writerow([
            i, pid, f"{pid}.pdf", title, r.get("year",""),
            r.get("source",""), doi, bucket,
            f"https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={enc(doi or title)}",
            f"https://doi.org/{doi}" if doi else "",
            f"https://scholar.google.com/scholar?q={enc(title)}",
            "", ""
        ])

print(f"Already have: {len(have)}")
print(f"Total missing: {len(missing)}")
print(f"Selected: {len(final)}")
print(f"  recent (2024+):  {len(recent)}")
print(f"  mid (2020-23):   {len(mid)}")
print(f"  classic (<2020): {len(classic)}")
print(f"Written: {OUT}")

