import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to_address: str, subject: str, body: str, dry_run: bool = False) -> bool:
    """Send an email via Gmail SMTP. Set dry_run=True to preview without sending."""
    gmail_address = os.environ["GMAIL_ADDRESS"]
    gmail_app_password = os.environ["GMAIL_APP_PASSWORD"].replace(" ", "")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = gmail_address
    msg["To"] = to_address
    msg.attach(MIMEText(body, "plain"))

    if dry_run:
        print("\n--- DRY RUN (not sent) ---")
        print(f"To: {to_address}")
        print(f"Subject: {subject}")
        print(f"Body:\n{body}")
        print("--------------------------\n")
        return True

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_address, gmail_app_password)
        server.sendmail(gmail_address, to_address, msg.as_string())

    return True
