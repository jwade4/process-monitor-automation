from process_logic import scan_processes, flag_processes
from report import send_report
from notify import notify_user

all_processes = scan_processes()
flagged = flag_processes(all_processes)
send_report(flagged)
# notify_user(report_path)
