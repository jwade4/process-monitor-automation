from process_logic import scan_processes, flag_processes
from report import send_report
from logger import log_info, log_error

def main():
    log_info("Application started.")

    try:
        all_processes = scan_processes()
    except Exception:
        log_error("Error in scan_processes()", exc_info=True, terminate=True)

    try:
        flagged = flag_processes(all_processes)
    except Exception:
        log_error("Error in flag_processes()", exc_info=True, terminate=True)

    try:
        send_report(flagged)
        log_info("Report successfully sent.")
    except Exception:
        log_error("Error in send_report()", exc_info=True, terminate=True)

if __name__ == "__main__":
    main()