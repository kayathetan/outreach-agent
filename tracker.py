import csv
import os
from datetime import datetime

LOG_FILE = "sent_emails.csv"
FIELDS = ["timestamp", "company_url", "to_address", "subject", "body", "status"]


def log_email(company_url: str, to_address: str, subject: str, body: str, status: str):
    file_exists = os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now().isoformat(),
            "company_url": company_url,
            "to_address": to_address,
            "subject": subject,
            "body": body,
            "status": status,
        })


def print_log():
    if not os.path.exists(LOG_FILE):
        print("No emails logged yet.")
        return
    with open(LOG_FILE, newline="") as f:
        for row in csv.DictReader(f):
            print(f"[{row['timestamp']}] → {row['to_address']} | {row['subject']} | {row['status']}")
