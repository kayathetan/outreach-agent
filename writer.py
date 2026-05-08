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
- Proper greeting on its own line: "Hi [First Name]," if you can infer a contact, otherwise "Hi [Company Name] team,"
- 3 short paragraphs with a blank line between each
- Paragraph 1: strong, confident opening — a sharp observation about their business that shows you've done your homework. No generic compliments. Reference something specific: their model, their scale, their industry position, a likely operational pain point.
- Paragraph 2: what Hourglass AI does for companies like them — use "we" not "I". One or two sentences, concrete and specific. Mention the 30-day guarantee and 5+ hours saved.
- Paragraph 3: soft CTA — "We'd love to explore whether there's a fit. Would you be open to a brief call this week?" Keep it low pressure.
- Professional sign-off: "Best regards," then a blank line, then sender name, role, and email on separate lines
- Use "we" and "our" throughout — never "I"
- Tone: high-end, polished, confident. Like a top-tier consulting firm reaching out. Not salesy, not casual, not corporate-robotic.
- Do NOT use placeholders like [Company Name] — infer it from the URL/title
- Subject line: sharp and specific, not generic. Reference the company or their industry.

The body must use actual newlines (\\n) between sections, not run-on paragraphs.

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

    # Extract subject and body directly via regex to avoid JSON newline issues
    subject_match = re.search(r'"subject"\s*:\s*"(.*?)"', raw, re.DOTALL)
    body_match = re.search(r'"body"\s*:\s*"(.*?)"\s*\}', raw, re.DOTALL)

    if not subject_match or not body_match:
        raise ValueError(f"Could not parse email from response:\n{raw}")

    email = {
        "subject": subject_match.group(1),
        "body": body_match.group(1).replace("\\n", "\n"),
    }
    return {
        "subject": email["subject"],
        "body": email["body"],
        "sender_name": SENDER_NAME,
        "sender_role": SENDER_ROLE,
        "sender_signature": SENDER_EMAIL_SIGNATURE,
    }
