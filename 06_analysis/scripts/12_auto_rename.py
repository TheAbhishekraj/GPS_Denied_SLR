"""Auto-rename downloaded PDFs to REC_XXXX.pdf by DOI match.
Uses PyMuPDF if available, else pypdf."""
import csv, pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
STAGING = ROOT/"08_docs/downloads_staging"
TARGET  = ROOT/"05_papers_fulltext"
CSV     = ROOT/"02_data_processed/screened_included_v2.csv"
LOG     = ROOT/"08_docs/rename_log.csv"

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)

def read_first_pages(path, max_pages=2):
    try:
        try:
            import pymupdf
            doc = pymupdf.open(str(path))
        except ImportError:
            import fitz
            doc = fitz.open(str(path))
        text = "".join(doc[i].get_text() for i in range(min(max_pages, len(doc))))
        doc.close()
        return text
    except ImportError:
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(path))
            text = ""
            for i, page in enumerate(reader.pages[:max_pages]):
                text += page.extract_text() or ""
            return text
        except Exception:
            return ""
    except Exception:
        return ""

def extract_doi(text):
    m = DOI_RE.search(text)
    return m.group(0).lower().rstrip(".,;)") if m else None

def extract_title(text):
    lines = [l.strip() for l in text.splitlines() if len(l.strip()) > 20]
    return lines[0][:120] if lines else None

def norm(s):
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())

def main():
    STAGING.mkdir(exist_ok=True)
    TARGET.mkdir(exist_ok=True)
    rows = list(csv.DictReader(CSV.open(encoding="utf-8-sig")))
    doi_to_id = {(r.get("doi") or "").lower(): (r.get("id") or r.get("paper_id"))
                 for r in rows if r.get("doi")}
    title_to_id = {norm(r.get("title") or ""): (r.get("id") or r.get("paper_id"))
                   for r in rows}

    log = []
    renamed = skipped = 0
    for f in STAGING.glob("*.pdf"):
        pid = None
        method = ""
        text = read_first_pages(f)
        doi = extract_doi(text)
        if doi and doi in doi_to_id:
            pid = doi_to_id[doi]; method = "doi"
        if not pid:
            t = extract_title(text)
            if t and norm(t) in title_to_id:
                pid = title_to_id[norm(t)]; method = "title"
        if not pid:
            log.append({"file": f.name, "result": "unmatched", "id": "", "method": ""})
            skipped += 1
            continue
        dest = TARGET / f"{pid}.pdf"
        if dest.exists():
            log.append({"file": f.name, "result": "already_exists", "id": pid, "method": method})
            skipped += 1
            continue
        shutil.move(str(f), str(dest))
        log.append({"file": f.name, "result": "renamed", "id": pid, "method": method})
        renamed += 1

    with LOG.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file","result","id","method"])
        w.writeheader(); w.writerows(log)

    print(f"Renamed: {renamed}  Skipped: {skipped}")
    print(f"Log: {LOG}")
    print(f"Final PDFs in 05_papers_fulltext: {len(list(TARGET.glob('*.pdf')))}")

if __name__ == "__main__": main()
