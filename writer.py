from groq import Groq

HOURGLASS_CONTEXT = """
Hourglass AI is a Melbourne-based startup that builds custom AI agents for growing businesses.
They automate repetitive admin workflows — things like email triage, invoice chasing, weekly
reporting, order processing, and customer support — deployed directly into existing tools like
Xero, HubSpot, Slack, and Salesforce.

Their core promise: "5+ hours saved per person per week, guaranteed in 30 days."
They build, they don't just advise. No new platforms required.
Target customers: professional services, SaaS, retail, manufacturing, healthcare.
"""

SENDER_NAME = "Alex"
SENDER_ROLE = "Growth, Hourglass AI"
SENDER_EMAIL_SIGNATURE = "alex@thehourglass.ai"


def write_outreach_email(company_info: dict) -> dict:
    """Use Claude to write a personalised cold email from Hourglass AI."""
    import os
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    prompt = f"""You are writing a cold outreach email on behalf of Hourglass AI to a potential client.

## About Hourglass AI (the sender)
{HOURGLASS_CONTEXT}

## About the target company (the recipient)
URL: {company_info['url']}
Title: {company_info.get('title', '')}
Description: {company_info.get('description', '')}
Website content: {company_info.get('raw_text', '')}

## Your task
Write a short, personalised cold email from {SENDER_NAME} at Hourglass AI to this company.

Rules:
- 3-4 sentences max. No fluff.
- Reference ONE specific thing you observed about their business (what they do, their industry, a pain point they likely have)
- Connect it naturally to what Hourglass AI can do for them
- End with a soft CTA: offer a 20-min call, no pressure
- Tone: confident, direct, human. Not salesy or corporate.
- Do NOT use placeholders like [Company Name] — infer the company name from the URL/title
- Subject line included

Return JSON with exactly these fields:
{{
  "subject": "...",
  "body": "..."
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )

    import json, re
    raw = response.choices[0].message.content
    # Extract JSON even if wrapped in markdown code block
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"Could not parse email JSON from Claude response:\n{raw}")

    email = json.loads(match.group())
    return {
        "subject": email["subject"],
        "body": email["body"],
        "sender_name": SENDER_NAME,
        "sender_role": SENDER_ROLE,
        "sender_signature": SENDER_EMAIL_SIGNATURE,
    }
