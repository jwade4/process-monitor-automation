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

all_processes = scan_processes()
flagged = flag_processes(all_processes)
for p in flagged:
    print(p)