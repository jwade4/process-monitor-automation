import os
import tempfile

from src.report import save_report

def test_save_report_csv_created():
    flagged = [
        {
            "pid": 123,
            "name": "malware.exe",
            "memory_mb": 800,
            "cpu_percent": 95,
            "suspicious": True,
            "reason": ["High memory usage", "High CPU usage"]
        }
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = save_report(flagged, output_dir=temp_dir)

        assert filepath is not None
        assert os.path.exists(filepath)

        assert os.path.getsize(filepath) > 0

def test_save_report_empty():
    result = save_report([])
    assert result is None