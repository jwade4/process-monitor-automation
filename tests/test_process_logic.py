from src.process_logic import scan_processes, flag_processes, evaluate_process

def test_evaluate_process():
    proc = {"memory_mb": 600, "cpu_percent": 90}
    reasons = evaluate_process(proc)
    assert "High memory usage" in reasons
    assert "High CPU usage" in reasons

def test_flag_processes():
     processes = [
        {"pid": 1, "name": "safe.exe", "memory_mb": 100, "cpu_percent": 10},
        {"pid": 2, "name": "bigmem.exe", "memory_mb": 600, "cpu_percent": 10},
        {"pid": 3, "name": "cpuhog.exe", "memory_mb": 100, "cpu_percent": 90},
        {"pid": 4, "name": "both.exe", "memory_mb": 800, "cpu_percent": 95}
    ] 
     flagged = flag_processes(processes)

     assert len(flagged) == 3

     for proc in flagged:
        assert proc["suspicious"] is True
        assert isinstance(proc["reasons"], list)
        assert len(proc["reasons"]) >= 1
    
     reasons_dict = {proc["name"]: proc["reasons"] for proc in flagged}
     assert "High memory usage" in reasons_dict["bigmem.exe"]
     assert "High CPU usage" in reasons_dict["cpuhog.exe"]
     assert "High memory usage" in reasons_dict["both.exe"]
     assert "High CPU usage" in reasons_dict["both.exe"]

def test_scan_processes():
    all_processes = scan_processes()
    assert isinstance(all_processes, list)