from datetime import datetime
import os
import csv

def save_report(flagged_processes, output_dir=os.path.join(os.path.expanduser("~"), "Downloads")):
    if not flagged_processes:
        print("No suspicious processes found. No report created.")
        return None
    
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"suspicious_processes_{timestamp}.csv"
    filepath = os.path.join(output_dir, filename)

    cleaned_data = []
    for proc in flagged_processes:
        proc_copy = proc.copy()

        if isinstance(proc_copy.get("reason"), list):
            proc_copy["reason"] = "; ".join(proc_copy["reason"])

        cleaned_data.append(proc_copy)
        
    fieldnames = cleaned_data[0].keys()

    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_data)
    
    print(f"Report sucessfully saved to: {filepath}")
    return filepath