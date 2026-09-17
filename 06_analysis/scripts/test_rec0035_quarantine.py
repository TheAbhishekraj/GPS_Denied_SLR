"""Regression check for quarantining the misattributed REC_0035 extraction."""
import csv
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
QUARANTINE = ROOT / '06_analysis/output/quarantine_REC_0035'
MASTER_SHA256 = 'f3e869be0bc3a818c649266eb4de18029e22f4781d12658dd86a1ecdd4399883'


class QuarantineCheck(unittest.TestCase):
    def test_active_evidence(self):
        with (ROOT / '02_data_processed/MASTER_EVIDENCE_V1.csv').open(
                encoding='utf-8-sig', newline='') as stream:
            reader = csv.DictReader(stream)
            fields, rows = reader.fieldnames, list(reader)
        self.assertEqual(len(fields), 63)
        self.assertEqual(len(set(fields)), 63)
        self.assertEqual(rows, [], 'The sole misattributed row must not remain active')
        with (QUARANTINE / 'MASTER_EVIDENCE_V1.csv').open(
                encoding='utf-8-sig', newline='') as stream:
            self.assertEqual(fields, next(csv.reader(stream)))
        self.assertFalse((ROOT / '03_extraction/per_paper/REC_0035.md').exists())
        self.assertFalse((ROOT / '06_analysis/output/extraction_inbox/REC_0035.json').exists())

    def test_preserved_record_and_provenance(self):
        record = json.loads((QUARANTINE / 'REC_0035.json').read_text(encoding='utf-8'))
        self.assertEqual(record['id'], 'REC_0035')
        self.assertEqual(record['best_ate_rmse'], '0.059')
        with (QUARANTINE / 'MASTER_EVIDENCE_V1.csv').open(
                encoding='utf-8-sig', newline='') as stream:
            self.assertEqual([r['id'] for r in csv.DictReader(stream)], ['REC_0035'])
        self.assertIn('REC_0035', (QUARANTINE / 'REC_0035.md').read_text(encoding='utf-8'))
        report = (QUARANTINE / 'README.md').read_text(encoding='utf-8')
        for text in ['State Estimation and Control', 'Robust Autonomous Flight',
                     'page 1', 'page 5', '0.059', '0.071', 'NOT_REPORTED']:
            self.assertIn(text, report)

    def test_audited_master_unchanged(self):
        data = (ROOT / '02_data_processed/extracted_master_v2.csv').read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), MASTER_SHA256)


if __name__ == '__main__':
    unittest.main(verbosity=2)
