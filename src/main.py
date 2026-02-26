from process_logic import scan_processes, flag_processes
from report import save_report
from notify import notify_user

all_processes = scan_processes()
flagged = flag_processes(all_processes)
report_path = save_report(flagged)
notify_user(report_path)
