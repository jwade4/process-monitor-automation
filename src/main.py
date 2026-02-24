import psutil
from datetime import datetime
import os
import csv


def scan_processes():
    all_processes = []

    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            info = proc.info
            memory_mb = info['memory_info'].rss / (1024 * 1024)
            cpu_percent = proc.cpu_percent(interval=0.1)

            process_dict = {
	        'pid': info['pid'],
		    'name': info['name'],
		    'memory_mb': memory_mb,
            'cpu_percent' : cpu_percent
	    }
	    
            all_processes.append(process_dict)
            #print(process_dict)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return all_processes


def evaluate_process(proc):
    reasons = []

    if proc.get("memory_mb", 0) > 500:
        reasons.append("High memory usage")

    if proc.get("cpu_percent", 0) > 80:
        reasons.append("High CPU usage")
    
    return reasons

def test_evaluate_process():
    proc = {"memory_mb": 600, "cpu_percent": 90}
    reasons = evaluate_process(proc)
    assert "High memory usage" in reasons
    assert "High CPU usage" in reasons

    print("All evaluate_process tests passed!")

    return

def flag_processes(process_list):
   flagged = []

   for proc in process_list:
       name = proc.get("name")
       reasons = evaluate_process(proc)
    
       if reasons:
           proc["suspicious"] = True
           proc["reasons"] = reasons
           flagged.append(proc)
    
   return flagged

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

     print("All flag_processes tests passed!")

     return

#test_flag_processes()
#test_evaluate_process()
#all_processes = scan_processes()
#flagged = flag_processes(all_processes)
#for p in flagged:
#    print(p)