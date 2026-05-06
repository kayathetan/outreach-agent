"""
Hourglass AI Outreach Agent
----------------------------
Researches a target company, writes a personalised cold email from Hourglass AI,
and sends it via Gmail.

Usage:
    python main.py --url https://example.com --to contact@example.com
    python main.py --url https://example.com --to contact@example.com --dry-run
    python main.py --log
"""

import argparse
import os
from dotenv import load_dotenv

from researcher import research_company
from writer import write_outreach_email
from sender import send_email
from tracker import log_email, print_log

load_dotenv()


def run(url: str, to_address: str, dry_run: bool = False):
    print(f"\n🔍 Researching {url}...")
    company_info = research_company(url)

    if company_info.get("error"):
        print(f"⚠️  Could not fetch site: {company_info['error']}")

    print("✍️  Writing personalised email with Claude...")
    email = write_outreach_email(company_info)

    print(f"\n📧 Subject: {email['subject']}")
    print(f"\n{email['body']}\n")

    success = send_email(
        to_address=to_address,
        subject=email["subject"],
        body=email["body"],
        dry_run=dry_run,
    )

    status = "sent" if (success and not dry_run) else "dry_run"
    log_email(url, to_address, email["subject"], email["body"], status)

    if not dry_run:
        print(f"✅ Sent to {to_address}")
    print(f"📋 Logged to sent_emails.csv")


def main():
    parser = argparse.ArgumentParser(description="Hourglass AI Outreach Agent")
    parser.add_argument("--url", help="Target company website URL")
    parser.add_argument("--to", help="Recipient email address")
    parser.add_argument("--dry-run", action="store_true", help="Preview email without sending")
    parser.add_argument("--log", action="store_true", help="Print sent email log")
    args = parser.parse_args()

    if args.log:
        print_log()
        return

    if not args.url or not args.to:
        parser.error("--url and --to are required (or use --log)")

    run(url=args.url, to_address=args.to, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
