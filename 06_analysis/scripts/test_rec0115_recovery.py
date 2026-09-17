"""Regression tests for conservative REC_0115 text recovery."""
import csv
from importlib import import_module
from pathlib import Path
import unittest

builder = import_module("09_build_evidence_workbooks")
ROOT = Path(__file__).resolve().parents[2]


class RecoveryCheck(unittest.TestCase):
    def test_encoded_title_and_punctuation(self):
        self.assertEqual(builder.recover_rec0115_span('/RZ\x03&RPSXWDWLRQDO'),
                         'Low Computational')
        self.assertEqual(builder.recover_rec0115_span('\x03\x0b8$9\x0c\x03'),
                         ' (UAV) ')

    def test_readable_spans_unchanged(self):
        for text in ['Abstract', 'Keywords—data fusion',
                     'DOI 10.1109/PDCAT.2019.00080', 'East', 'തതതത']:
            self.assertEqual(builder.recover_rec0115_span(text), text)

    def test_pdf_title_matches_master(self):
        pages = builder.build_pages(ROOT / '05_papers_fulltext/REC_0115.pdf')
        title = ' '.join(pages[0].split('Xiaoying', 1)[0].split())
        title = title.replace('GPS- Denied', 'GPS-Denied')
        with (ROOT / '02_data_processed/extracted_master_v2.csv').open(
                encoding='utf-8', newline='') as stream:
            record = next(r for r in csv.DictReader(stream) if r['id'] == 'REC_0115')
        self.assertEqual(title, record['title'])
        self.assertIn('DOI 10.1109/PDCAT.2019.00080', pages[0])
        with builder.fitz.open(ROOT / '05_papers_fulltext/REC_0115.pdf') as doc:
            self.assertEqual(len(pages), doc.page_count)

    def test_other_pdf_unchanged(self):
        pdf = ROOT / '05_papers_fulltext/REC_0001.pdf'
        with builder.fitz.open(pdf) as doc:
            expected = [page.get_text() for page in doc]
        self.assertEqual(builder.build_pages(pdf), expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
