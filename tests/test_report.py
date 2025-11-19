import unittest
import os
import json
import pandas as pd
from datetime import datetime, timezone
from sp_secret_bot.report import ReportGenerator
from sp_secret_bot.scanner import SecretRisk

class TestReportGenerator(unittest.TestCase):
    
    def setUp(self):
        self.reporter = ReportGenerator()
        self.sample_risks = [
            SecretRisk(
                sp_name="Test SP",
                app_id="app-123",
                sp_object_id="obj-123",
                secret_id="key-123",
                secret_type="Password",
                expiry_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
                days_remaining=30,
                severity="CRITICAL"
            )
        ]
        self.test_file_csv = "test_report.csv"
        self.test_file_json = "test_report.json"
        self.test_file_md = "test_report.md"

    def tearDown(self):
        # Clean up test files
        for f in [self.test_file_csv, self.test_file_json, self.test_file_md]:
            if os.path.exists(f):
                os.remove(f)

    def test_export_csv(self):
        self.reporter.export_csv(self.sample_risks, self.test_file_csv)
        self.assertTrue(os.path.exists(self.test_file_csv))
        df = pd.read_csv(self.test_file_csv)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["Service Principal"], "Test SP")

    def test_export_json(self):
        self.reporter.export_json(self.sample_risks, self.test_file_json)
        self.assertTrue(os.path.exists(self.test_file_json))
        with open(self.test_file_json, 'r') as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["Severity"], "CRITICAL")

    def test_export_markdown(self):
        self.reporter.export_markdown(self.sample_risks, self.test_file_md)
        self.assertTrue(os.path.exists(self.test_file_md))
        with open(self.test_file_md, 'r') as f:
            content = f.read()
            self.assertIn("Test SP", content)
            self.assertIn("# Azure Service Principal Secret Expiry Report", content)

if __name__ == '__main__':
    unittest.main()
