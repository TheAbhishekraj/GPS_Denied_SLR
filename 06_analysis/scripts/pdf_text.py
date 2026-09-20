#!/usr/bin/env python3
"""pdf_text.py v1.0 — read-only single-PDF text extractor (Phase 6 aid).

LIBRARY SUBSTITUTION (human-approved 2026-09-19, Option 1):
  Uses PyMuPDF via `import fitz` instead of the originally-specified
  pypdf / pdfplumber, because neither pypdf nor pdfplumber is installed
  in the project venv and no new packages were to be installed.
  fitz (PyMuPDF v1.28.2) is already present and is read-only-safe.
  Recorded in _AUDIT/action_log.md.

Behavior (human-approved spec):
  1. Accepts exactly ONE CLI argument: absolute path to one PDF.
     Zero or >1 argument, or any write flag (--output/--write/etc.)
     -> usage to stderr, exit 2. No write-capable flag exists.
  2. Output: UTF-8 stdout ONLY. Page markers [p.1], [p.2], ... one per
     physical page, printed before that page's text.
  3. Header block printed before the first page:
         === pdf_text.py v1.0 ===
         file: <input path>
         sha256: <sha256 of input PDF>
         library: pymupdf (fitz) v<version>
         pages: <page count>
         === BEGIN ===
  4. Footer block after the last page:  === END ===
  5. Errors (encrypted / corrupt / missing / no extractable text)
     -> message to stderr, exit 1.
  6. Writes NOTHING: no files, no logs, no network, no state.
     Encoding UTF-8 with errors='replace' on stdout. Idempotent.
"""
import hashlib
import os
import sys

try:
    import fitz  # PyMuPDF
except Exception as exc:  # pragma: no cover
    sys.stderr.write("pdf_text.py: PyMuPDF (fitz) is not importable: %s\n" % exc)
    sys.exit(1)

VERSION = "1.0"

# Flags that would imply writing; none are supported by design.
REJECTED_FLAGS = ("--output", "--write", "--out", "-o", "--save", "--dump")

USAGE = (
    "usage: python pdf_text.py <absolute_path_to_one_pdf>\n"
    "  Prints the PDF's text to stdout with [p.N] page markers.\n"
    "  Writes nothing. No output/write flags are supported.\n"
)


def _usage_exit(msg=None):
    if msg:
        sys.stderr.write("pdf_text.py: %s\n" % msg)
    sys.stderr.write(USAGE)
    sys.exit(2)


def main():
    args = sys.argv[1:]

    # Argument guard: exactly one argument, and it must not be a write flag.
    if len(args) != 1:
        _usage_exit("expected exactly 1 argument (the PDF path), got %d" % len(args))
    target = args[0]
    if target.startswith("-") or target.lower() in REJECTED_FLAGS:
        _usage_exit("flags are not supported (read-only tool): %r" % target)

    if not os.path.isfile(target):
        sys.stderr.write("pdf_text.py: file not found: %s\n" % target)
        sys.exit(1)

    # SHA256 of the exact input PDF (traceability).
    h = hashlib.sha256()
    with open(target, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    digest = h.hexdigest().upper()

    # Open the PDF read-only.
    try:
        doc = fitz.open(target)
    except Exception as exc:
        sys.stderr.write("pdf_text.py: cannot open PDF (%s): %s\n" % (type(exc).__name__, exc))
        sys.exit(1)

    try:
        if doc.needs_pass or doc.is_encrypted:
            sys.stderr.write("pdf_text.py: PDF is encrypted/password-protected: %s\n" % target)
            sys.exit(1)

        page_count = doc.page_count
        if page_count <= 0:
            sys.stderr.write("pdf_text.py: PDF has no pages: %s\n" % target)
            sys.exit(1)

        lib_ver = getattr(fitz, "__doc__", "") or ""
        # fitz exposes version via fitz.version tuple in PyMuPDF.
        try:
            lib_ver = "pymupdf (fitz) v%s" % fitz.version[0]
        except Exception:
            lib_ver = "pymupdf (fitz)"

        out = sys.stdout
        try:
            out.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

        out.write("=== pdf_text.py v%s ===\n" % VERSION)
        out.write("file: %s\n" % target)
        out.write("sha256: %s\n" % digest)
        out.write("library: %s\n" % lib_ver)
        out.write("pages: %d\n" % page_count)
        out.write("=== BEGIN ===\n")

        any_text = False
        for i in range(page_count):
            page = doc.load_page(i)
            text = page.get_text("text") or ""
            if text.strip():
                any_text = True
            out.write("[p.%d]\n" % (i + 1))
            out.write(text)
            if not text.endswith("\n"):
                out.write("\n")

        out.write("=== END ===\n")
        out.flush()

        if not any_text:
            sys.stderr.write(
                "pdf_text.py: no extractable text layer (possible scanned image): %s\n" % target
            )
            sys.exit(1)
    finally:
        doc.close()

    sys.exit(0)


if __name__ == "__main__":
    main()
