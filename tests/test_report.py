import unittest
from src.report import make_csv_report

class TestMakeCSVReport(unittest.TestCase):

    def test_csv_created(self):
        flagged = [
            {
                "pid": 123,
                "name": "malware.exe",
                "memory": 800,
                "cpu_percent": 95,
                "suspicious": True,
                "reason": ["High memory usage", "High CPU usage"]
            }
        ]

        csv_content, filename = make_csv_report(flagged)

        # CSV content should exist
        self.assertIsNotNone(csv_content)
        self.assertTrue(len(csv_content) > 0)

        # Filename should exist and end with .csv
        self.assertIsNotNone(filename)
        self.assertTrue(filename.endswith(".csv"))

        # CSV header includes all keys
        header = csv_content.strip().split("\n")[0]
        expected_keys = ["pid", "name", "memory", "cpu_percent", "suspicious", "reason"]
        for key in expected_keys:
            self.assertIn(key, header)

        # Check that reasons are joined properly
        self.assertIn("High memory usage; High CPU usage", csv_content)

    def test_csv_empty_list(self):
        csv_content, filename = make_csv_report([])
        self.assertIsNone(csv_content)
        self.assertIsNone(filename)


if __name__ == "__main__":
    unittest.main()