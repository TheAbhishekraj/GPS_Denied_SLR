"""
07c_priority_oa_retrieval.py - Automated OA retrieval from priority_300_download.csv

Sources tried (in order per paper):
  1. OpenAlex  - best OA index, DOI + title search
  2. Semantic Scholar - openAccessPdf field
  3. Unpaywall - legal OA by DOI
  4. CORE.ac.uk - aggregator, good for conference papers
  5. arXiv     - preprint fallback by title

Writes to: 05_papers_fulltext/<id>.pdf
Logs to:   08_docs/priority_retrieval_log.csv
"""

import csv, json, pathlib, time, urllib.request, urllib.parse, sys
from urllib.error import HTTPError, URLError

ROOT    = pathlib.Path(__file__).resolve().parents[2]
IN      = ROOT / "08_docs/priority_300_download.csv"
PDF_DIR = ROOT / "05_papers_fulltext"
LOG     = ROOT / "08_docs/priority_retrieval_log.csv"
PDF_DIR.mkdir(exist_ok=True)

UA = {"User-Agent": "SLR-OARetriever/3.0 (mailto:abhishek.raj.research@gmail.com)"}
UNPAYWALL_EMAIL = "abhishek.raj.research@gmail.com"
CORE_API_KEY    = ""   # optional: get free key at core.ac.uk/api-keys

def _get(url, timeout=15):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def _get_json(url, timeout=15):
    return json.loads(_get(url, timeout))

def try_openalex(doi, title):
    try:
        if doi:
            url = f"https://api.openalex.org/works/doi:{urllib.parse.quote(doi, safe='')}"
        else:
            url = (f"https://api.openalex.org/works?"
                   f"search={urllib.parse.quote(title[:150])}&per_page=1")
        j = _get_json(url)
        if "results" in j:
            j = j["results"][0] if j["results"] else {}
        for loc in (j.get("locations") or []):
            if loc.get("pdf_url"):
                return loc["pdf_url"], "openalex_loc"
        oa_url = (j.get("open_access") or {}).get("oa_url")
        if oa_url:
            return oa_url, "openalex_oa"
    except Exception:
        pass
    return None, "openalex_none"

def try_s2(doi):
    if not doi:
        return None, "s2_no_doi"
    try:
        url = (f"https://api.semanticscholar.org/graph/v1/paper/"
               f"DOI:{urllib.parse.quote(doi, safe='')}?fields=openAccessPdf")
        j = _get_json(url)
        pdf = (j.get("openAccessPdf") or {}).get("url")
        if pdf:
            return pdf, "s2_pdf"
    except Exception:
        pass
    return None, "s2_none"

def try_unpaywall(doi):
    if not doi:
        return None, "unpaywall_no_doi"
    try:
        url = (f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi, safe='/')}?"
               f"email={urllib.parse.quote(UNPAYWALL_EMAIL)}")
        j = _get_json(url)
        best = j.get("best_oa_location") or {}
        pdf = best.get("url_for_pdf") or best.get("url")
        if pdf:
            return pdf, "unpaywall"
        for loc in (j.get("oa_locations") or []):
            if loc.get("url_for_pdf"):
                return loc["url_for_pdf"], "unpaywall_loc"
    except Exception:
        pass
    return None, "unpaywall_none"

def try_core(doi, title):
    try:
        query = doi if doi else title[:120]
        if CORE_API_KEY:
            url = (f"https://api.core.ac.uk/v3/search/works?"
                   f"q={urllib.parse.quote(query)}&limit=1&api_key={CORE_API_KEY}")
        else:
            url = (f"https://api.core.ac.uk/v3/search/works?"
                   f"q={urllib.parse.quote(query)}&limit=1")
        j = _get_json(url, timeout=12)
        for result in (j.get("results") or []):
            pdf = result.get("downloadUrl") or result.get("fullTextIdentifier")
            if pdf and pdf.startswith("http"):
                return pdf, "core"
    except Exception:
        pass
    return None, "core_none"

def try_arxiv(title):
    if not title:
        return None, "arxiv_no_title"
    try:
        q = urllib.parse.quote(f'ti:"{title[:100]}"')
        url = f"http://export.arxiv.org/api/query?search_query={q}&max_results=1"
        body = _get(url, timeout=15).decode("utf-8", errors="ignore")
        if "arxiv.org/abs/" in body:
            for line in body.splitlines():
                if "arxiv.org/abs/" in line and "<id>" in line:
                    aid = line.split("arxiv.org/abs/")[1].split("<")[0].strip()
                    return f"https://arxiv.org/pdf/{aid}.pdf", "arxiv"
    except Exception:
        pass
    return None, "arxiv_none"

def download_pdf(url, dest):
    try:
        data = _get(url, timeout=30)
        if len(data) < 5000:
            return False, f"too_small_{len(data)}b"
        if not data.startswith(b"%PDF"):
            return False, "not_pdf_magic"
        dest.write_bytes(data)
        return True, "ok"
    except HTTPError as e:
        return False, f"http_{e.code}"
    except URLError:
        return False, "url_err"
    except Exception:
        return False, "err"

def main():
    if not IN.exists():
        print(f"ERROR: {IN} not found. Run 11_priority_300.py first.")
        sys.exit(1)

    rows = list(csv.DictReader(IN.open(encoding="utf-8-sig")))
    disk_ids = {p.stem for p in PDF_DIR.glob("*.pdf")}

    log_rows = {}
    if LOG.exists():
        for r in csv.DictReader(LOG.open(encoding="utf-8-sig")):
            log_rows[r["id"]] = r

    to_attempt = sum(1 for r in rows if r.get("id","") not in disk_ids)
    print(f"Priority papers : {len(rows)}")
    print(f"Already on disk : {len(disk_ids)}")
    print(f"To attempt      : {to_attempt}")
    print("=" * 60)

    new_count, skip_count, fail_count = 0, 0, 0
    source_tally = {}

    for i, row in enumerate(rows, 1):
        pid   = row.get("id", "").strip()
        doi   = row.get("doi", "").strip()
        title = row.get("title", "").strip()
        dest  = PDF_DIR / f"{pid}.pdf"

        if dest.exists():
            skip_count += 1
            continue

        url, src = try_openalex(doi, title);  time.sleep(0.3)
        if not url:
            url, src = try_s2(doi);           time.sleep(0.3)
        if not url:
            url, src = try_unpaywall(doi);    time.sleep(0.4)
        if not url:
            url, src = try_core(doi, title);  time.sleep(0.5)
        if not url:
            url, src = try_arxiv(title);      time.sleep(0.3)

        if url:
            ok, reason = download_pdf(url, dest)
            if ok:
                new_count += 1
                source_tally[src] = source_tally.get(src, 0) + 1
                status = "downloaded"
            else:
                fail_count += 1
                status = f"url_found_dl_failed:{reason}"
        else:
            fail_count += 1
            status = "no_oa_url"
            src = "all_failed"

        log_rows[pid] = {
            "id": pid, "doi": doi, "title": title[:80],
            "status": status, "source": src, "url": url or "",
        }

        if i % 10 == 0:
            on_disk_now = len(list(PDF_DIR.glob("*.pdf")))
            print(f"  [{i:3d}/300] new={new_count:3d}  fail={fail_count:3d}  "
                  f"total_disk={on_disk_now}  coverage={100*on_disk_now/636:.1f}%")

    fieldnames = ["id", "doi", "title", "status", "source", "url"]
    with LOG.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in log_rows.values():
            w.writerow(r)

    on_disk_final = len(list(PDF_DIR.glob("*.pdf")))
    print("\n" + "=" * 60)
    print(f"New PDFs this run : {new_count}")
    print(f"Failed attempts   : {fail_count}")
    print(f"Skipped (existed) : {skip_count}")
    print(f"Total on disk     : {on_disk_final} / 636  ({100*on_disk_final/636:.1f}%)")
    print(f"\nSource breakdown:")
    for src, cnt in sorted(source_tally.items(), key=lambda x: -x[1]):
        print(f"  {src:25s}: {cnt}")
    print(f"\nLog: {LOG}")
    print("\n=== VERIFICATION ===")
    print(f"PDF count: {on_disk_final}  (expect >= 33)")
    print(f"Gate PASS: {on_disk_final >= 33}")

if __name__ == "__main__":
    main()
