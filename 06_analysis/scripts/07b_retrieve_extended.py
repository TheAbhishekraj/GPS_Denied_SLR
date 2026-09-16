"""Extended full-text retrieval: OpenAlex + S2 + DOAJ + arXiv."""
import csv, json, pathlib, time, urllib.request, urllib.parse
from urllib.error import HTTPError, URLError

ROOT = pathlib.Path(__file__).resolve().parents[2]
IN   = ROOT/"02_data_processed/screened_included_v2.csv"
LOG  = ROOT/"08_docs/fulltext_retrieval_log.csv"
PDF_DIR = ROOT/"05_papers_fulltext"
PDF_DIR.mkdir(exist_ok=True)
UA = {"User-Agent": "SLR-Retriever/2.0 (mailto:abhishek.raj.research@gmail.com)"}

def _get(url, timeout=12):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def try_openalex(doi, title):
    url = (f"https://api.openalex.org/works/doi:{urllib.parse.quote(doi)}"
           if doi else
           f"https://api.openalex.org/works?search={urllib.parse.quote(title[:150])}&per_page=1")
    try:
        j = json.loads(_get(url))
        if "results" in j: j = j["results"][0] if j["results"] else {}
        for loc in (j.get("locations") or []):
            if loc.get("pdf_url"): return loc["pdf_url"], "openalex"
        oa = (j.get("open_access") or {}).get("oa_url")
        if oa: return oa, "openalex_oa"
    except Exception: pass
    return None, "openalex_none"

def try_s2(doi):
    if not doi: return None, "s2_no_doi"
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{urllib.parse.quote(doi)}?fields=openAccessPdf"
    try:
        j = json.loads(_get(url))
        pdf = (j.get("openAccessPdf") or {}).get("url")
        if pdf: return pdf, "s2_pdf"
    except Exception: pass
    return None, "s2_none"

def try_doaj(title):
    if not title: return None, "doaj_no_title"
    url = f"https://doaj.org/api/search/articles/{urllib.parse.quote(title[:120])}"
    try:
        j = json.loads(_get(url))
        for hit in j.get("results", [])[:1]:
            for link in hit.get("bibjson", {}).get("link", []):
                if link.get("type") == "fulltext": return link.get("url"), "doaj"
    except Exception: pass
    return None, "doaj_none"

def try_arxiv(title):
    if not title: return None, "arxiv_no_title"
    q = urllib.parse.quote(f'ti:"{title[:100]}"')
    url = f"http://export.arxiv.org/api/query?search_query={q}&max_results=1"
    try:
        body = _get(url).decode("utf-8", errors="ignore")
        if "arxiv.org/abs/" in body:
            for line in body.splitlines():
                if "arxiv.org/abs/" in line and "<id>" in line:
                    aid = line.split("arxiv.org/abs/")[1].split("<")[0].strip()
                    return f"https://arxiv.org/pdf/{aid}.pdf", "arxiv"
    except Exception: pass
    return None, "arxiv_none"

def download_pdf(url, dest):
    try:
        data = _get(url, timeout=25)
        if len(data) < 5000 or not data.startswith(b"%PDF"): return False
        dest.write_bytes(data)
        return True
    except Exception: return False

def main():
    rows = list(csv.DictReader(IN.open(encoding="utf-8-sig")))
    log  = {r["id"]: r for r in csv.DictReader(LOG.open(encoding="utf-8-sig"))}
    disk_ids = {p.stem for p in PDF_DIR.glob("*.pdf")}
    for pid, r in log.items():
        on_disk = pid in disk_ids
        if on_disk and r.get("fulltext_available") != "True":
            r["status"] = "downloaded"; r["fulltext_available"] = "True"
            r["retrieval_status"] = "reconciled"
        elif not on_disk and r.get("fulltext_available") == "True":
            r["status"] = "failed"; r["fulltext_available"] = "False"
            r["retrieval_status"] = "reconciled_missing"
    new_count = 0
    print(f"Processing {len(rows)} papers...", flush=True)
    for i, row in enumerate(rows, 1):
        pid   = row.get("id") or row.get("paper_id")
        doi   = (row.get("doi") or "").strip()
        title = (row.get("title") or "").strip()
        dest  = PDF_DIR / f"{pid}.pdf"
        if dest.exists(): continue
        url, src = try_openalex(doi, title)
        if not url: url, src = try_s2(doi)
        if not url: url, src = try_doaj(title)
        if not url: url, src = try_arxiv(title)
        if url and download_pdf(url, dest):
            new_count += 1
            if pid in log:
                log[pid].update({"status":"downloaded","fulltext_available":"True",
                                 "retrieval_status":f"ext_{src}","reason":""})
        if i % 25 == 0:
            print(f"  {i}/{len(rows)}  new={new_count}", flush=True)
        time.sleep(0.4)
    with LOG.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id","doi","status","reason",
                                          "fulltext_available","retrieval_status"])
        w.writeheader()
        for pid in log: w.writerow(log[pid])
    on_disk = len(list(PDF_DIR.glob("*.pdf")))
    print(f"\nNew this run: {new_count}", flush=True)
    print(f"Total on disk: {on_disk} / {len(rows)} ({100*on_disk/len(rows):.1f}%)", flush=True)

if __name__ == "__main__": main()

