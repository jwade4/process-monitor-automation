import csv
from io import StringIO
import smtplib
from datetime import datetime
from email.message import EmailMessage

def send_report(flagged_processes):
    """
    Sends a CSV report of flagged processes to a Google Group using Gmail.

    flagged_processes: List of dictionaries containing process info.
    """

    if not flagged_processes:
        print("No suspicious processes found. No email sent.")
        return None

    # ===== 1️⃣ Create CSV in memory =====
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

    # ===== 2️⃣ Create the email =====
    msg = EmailMessage()
    msg["Subject"] = "Suspicious Process Report"
    msg["From"] = "jordanwade.ftr@gmail.com"  # Replace with your Gmail
    msg["To"] = "it-support-team-test@googlegroups.com"  # Replace with your group email
    msg.set_content("Attached is the latest suspicious process report.")
    msg.add_attachment(csv_content, subtype="csv", filename=filename)

    # ===== 3️⃣ Send the email via Gmail SMTP =====
    # Gmail SMTP server with SSL
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("jordanwade.ftr@gmail.com", "xqod zvfy rypn hbsx")  # Use App Password
        server.send_message(msg)

    print("Report successfully emailed via Gmail service account.")
    return True
