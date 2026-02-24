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

            process_dict = {
	        'pid': info['pid'],
		    'name': info['name'],
		    'memory_mb': memory_mb
	    }
	    
            all_processes.append(process_dict)
            #print(process_dict)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

scan_processes()
