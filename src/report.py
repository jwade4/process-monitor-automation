import csv
from io import StringIO
import smtplib
from datetime import datetime
from email.message import EmailMessage

def make_csv_report(flagged_processes):
    """
    Generates a CSV string and filename from a list of flagged processes.

    Returns (csv_content, filename) or (None, None) if no data.
    """
    if not flagged_processes:
        return None, None

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"suspicious_processes_{timestamp}.csv"

    cleaned_data = []
    for proc in flagged_processes:
        proc_copy = proc.copy()
        # Convert list of reasons to a single string
        if isinstance(proc_copy.get("reason"), list):
            proc_copy["reason"] = "; ".join(proc_copy["reason"])
        cleaned_data.append(proc_copy)

    fieldnames = cleaned_data[0].keys()
    csv_buffer = StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cleaned_data)
    csv_content = csv_buffer.getvalue()

    return csv_content, filename


def send_report_via_gmail(csv_content, filename, recipient="it-support-team-test@googlegroups.com"):
    """
    Sends the given CSV content as an attachment via Gmail SMTP.
    """
    if not csv_content:
        print("No CSV content to send.")
        return None

    msg = EmailMessage()
    msg["Subject"] = "Suspicious Process Report"
    msg["From"] = "jordanwade.ftr@gmail.com"  # Replace with your Gmail
    msg["To"] = recipient
    msg.set_content("Attached is the latest suspicious process report.")
    msg.add_attachment(csv_content, subtype="csv", filename=filename)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("jordanwade.ftr@gmail.com", "xqod zvfy rypn hbsx")  # App Password
        server.send_message(msg)

    print("Report successfully emailed via Gmail service account.")
    return True


# ===== Optional convenience function to do both =====
def send_report(flagged_processes):
    csv_content, filename = make_csv_report(flagged_processes)
    if csv_content:
        return send_report_via_gmail(csv_content, filename)
    else:
        print("No suspicious processes found. No email sent.")
        return None