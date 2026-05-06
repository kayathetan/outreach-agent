# Hourglass AI Outreach Agent

An autonomous AI agent that researches target companies and sends personalised cold emails on behalf of Hourglass AI — fully automated from research to send.

## What it does

1. **Researches** a target company by scraping their website
2. **Writes** a personalised cold email using Llama 3.3 (via Groq) — referencing specific details about the company
3. **Sends** the email via Gmail
4. **Logs** every sent email to a CSV tracker

## Demo

```bash
python3 main.py --url https://www.legalvision.com.au --to contact@legalvision.com.au
```

Output:
```
🔍 Researching https://www.legalvision.com.au...
✍️  Writing personalised email...
📧 Subject: Simplifying Legal Operations at LegalVision
✅ Sent to contact@legalvision.com.au
📋 Logged to sent_emails.csv
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Fill in your keys in .env
```

### Required environment variables

| Variable | Where to get it |
|----------|----------------|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) — free |
| `GMAIL_ADDRESS` | Your Gmail address |
| `GMAIL_APP_PASSWORD` | Google Account → Security → App Passwords |

## Usage

```bash
# Send a real email
python3 main.py --url https://company.com --to contact@company.com

# Preview without sending
python3 main.py --url https://company.com --to contact@company.com --dry-run

# View sent email log
python3 main.py --log
```

## Stack

- **LLM:** Llama 3.3 70B via [Groq](https://groq.com) (free tier)
- **Web research:** requests + BeautifulSoup
- **Email:** Gmail SMTP
- **Language:** Python 3.11
