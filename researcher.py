import requests
from bs4 import BeautifulSoup


def research_company(url: str) -> dict:
    """Scrape a company website and extract key info."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; OutreachAgent/1.0)"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        return {"url": url, "error": str(e), "raw_text": ""}

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove noise
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    # Extract title
    title = soup.title.string.strip() if soup.title else ""

    # Extract meta description
    meta = soup.find("meta", attrs={"name": "description"}) or \
           soup.find("meta", attrs={"property": "og:description"})
    description = meta["content"].strip() if meta and meta.get("content") else ""

    # Extract main body text (capped to avoid token overflow)
    raw_text = " ".join(soup.get_text(separator=" ").split())[:4000]

    return {
        "url": url,
        "title": title,
        "description": description,
        "raw_text": raw_text,
    }
