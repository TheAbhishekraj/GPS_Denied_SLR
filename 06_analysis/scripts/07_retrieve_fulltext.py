"""
Phase 7 Step 1 — Real full-text retrieval (Fast Concurrent Multi-Source OA Retriever).
Sources (in order): OpenAlex → Semantic Scholar → Unpaywall → PubMed Central → arXiv.
Concurrent ThreadPool (12 workers) completes all 636 papers in ~1-2 minutes.
Logs every outcome cleanly to 08_docs/fulltext_retrieval_log.csv.
"""
import csv, json, pathlib, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = pathlib.Path(__file__).resolve().parents[2]
IN   = ROOT/"02_data_processed/screened_included_v2.csv"
OUT  = ROOT/"08_docs/fulltext_retrieval_log.csv"
PDF_DIR = ROOT/"05_papers_fulltext"
PDF_DIR.mkdir(exist_ok=True)

EMAIL = "abhishek.raj.research@gmail.com"
USER_AGENT = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) SLR-Retriever/3.0 ({EMAIL})"

def try_openalex(doi):
    if not doi: return None, "no_doi"
    url = f"https://api.openalex.org/works/https://doi.org/{urllib.parse.quote(doi)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=4) as r:
            j = json.load(r)
        best_oa = j.get("best_oa_location") or {}
        pdf_url = best_oa.get("pdf_url") or best_oa.get("landing_page_url")
        if pdf_url:
            return pdf_url, "openalex"
    except Exception:
        pass
    return None, "openalex_none"

def try_semanticscholar(doi):
    if not doi: return None, "no_doi"
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{urllib.parse.quote(doi)}?fields=openAccessPdf"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=4) as r:
            j = json.load(r)
        oa_pdf = j.get("openAccessPdf") or {}
        pdf_url = oa_pdf.get("url")
        if pdf_url:
            return pdf_url, "semanticscholar"
    except Exception:
        pass
    return None, "semanticscholar_none"

def try_unpaywall(doi):
    if not doi: return None, "no_doi"
    url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={EMAIL}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=4) as r:
            j = json.load(r)
        loc = j.get("best_oa_location") or {}
        pdf_url = loc.get("url_for_pdf") or loc.get("url")
        if pdf_url:
            return pdf_url, "unpaywall"
    except Exception:
        pass
    return None, "unpaywall_none"

def try_pmc(doi):
    if not doi: return None, "no_doi"
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:{urllib.parse.quote(doi)}&format=json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=4) as r:
            j = json.load(r)
        hits = j.get("resultList", {}).get("result", [])
        if hits and hits[0].get("pmcid"):
            return f"https://www.ebi.ac.uk/europepmc/webservices/rest/{hits[0]['pmcid']}/fullTextXML", "pmc"
    except Exception:
        pass
    return None, "pmc_none"

def try_arxiv(title):
    if not title: return None, "no_title"
    words = [w for w in title.split() if w.isalnum()][:6]
    clean_q = " ".join(words)
    if not clean_q: return None, "no_title"
    q = urllib.parse.quote(f'ti:"{clean_q}"')
    url = f"http://export.arxiv.org/api/query?search_query={q}&max_results=1"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=4) as r:
            body = r.read().decode("utf-8", errors="ignore")
        if "<entry>" in body:
            for line in body.splitlines():
                if "<id>http" in line and "arxiv.org/abs/" in line:
                    abs_url = line.split("<id>")[1].split("</id>")[0].strip()
                    return abs_url.replace("/abs/", "/pdf/") + ".pdf", "arxiv"
    except Exception:
        pass
    return None, "arxiv_none"




def download(url, dest):
    if not url: return False
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = r.read()
            if len(data) > 5000:
                dest.write_bytes(data)
                return True
    except Exception:
        pass
    return False

def process_paper(row):
    pid = row.get("id") or row.get("paper_id")
    doi = (row.get("doi") or "").strip()
    title = (row.get("title") or "").strip()
    pdf_path = PDF_DIR / f"{pid}.pdf"

    if pdf_path.exists() and pdf_path.stat().st_size > 5000:
        return {"id": pid, "doi": doi, "status": "cached",
                "reason": "", "fulltext_available": "True",
                "retrieval_status": "cached"}

    url, src = try_openalex(doi)
    if not url:
        url, src = try_semanticscholar(doi)
    if not url:
        url, src = try_unpaywall(doi)
    if not url:
        url, src = try_pmc(doi)
    if not url:
        url, src = try_arxiv(title)

    if url and download(url, pdf_path):
        return {"id": pid, "doi": doi, "status": "downloaded",
                "reason": "", "fulltext_available": "True",
                "retrieval_status": src}

    return {"id": pid, "doi": doi, "status": "failed",
            "reason": src, "fulltext_available": "False",
            "retrieval_status": src}

def main():
    rows = list(csv.DictReader(IN.open(encoding="utf-8-sig")))
    print(f"Retrieving {len(rows)} papers using 12 concurrent workers...", flush=True)
    t0 = time.time()

    results = {}
    with ThreadPoolExecutor(max_workers=12) as executor:
        future_to_id = {executor.submit(process_paper, row): (row.get("id") or row.get("paper_id")) for row in rows}
        done_count = 0
        for future in as_completed(future_to_id):
            pid = future_to_id[future]
            try:
                res = future.result()
            except Exception as e:
                res = {"id": pid, "doi": "", "status": "error", "reason": str(e),
                       "fulltext_available": "False", "retrieval_status": "error"}
            results[pid] = res
            done_count += 1
            if done_count % 25 == 0 or done_count == len(rows):
                ok = sum(1 for r in results.values() if r["fulltext_available"] == "True")
                print(f"  {done_count}/{len(rows)} done  ok={ok} ({100*ok/done_count:.1f}%)", flush=True)

    ordered_log = [results[row.get("id") or row.get("paper_id")] for row in rows]
    fieldnames = ["id", "doi", "status", "reason", "fulltext_available", "retrieval_status"]
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(ordered_log)

    ok = sum(1 for x in ordered_log if x["fulltext_available"] == "True")
    elapsed = time.time() - t0
    print(f"\nDONE in {elapsed:.1f}s: {ok}/{len(rows)} retrieved ({100*ok/len(rows):.1f}%)", flush=True)
    print(f"Log saved to: {OUT}", flush=True)

if __name__ == "__main__":
    main()



