import requests
import xml.etree.ElementTree as ET
import re
from html import unescape
from typing import List, Dict

# --------------------------------------------------
# Configuration
# --------------------------------------------------

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# --------------------------------------------------
# Helpers
# --------------------------------------------------

def strip_namespaces(root: ET.Element) -> None:
    """Remove XML namespaces to simplify tag lookup."""
    for el in root.iter():
        if "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]

def clean_html(text: str) -> str:
    """Strip HTML tags and normalize whitespace."""
    if not text:
        return ""

    text = unescape(text)
    text = text.replace("<br/>", "\n")
    text = re.sub(r"<.*?>", "", text)
    return text.strip()

def extract_field(text: str, label: str) -> str:
    """Extract labeled fields from description text."""
    match = re.search(rf"{label}:\s*(.+)", text)
    return match.group(1).strip() if match else ""

# --------------------------------------------------
# Core scraper
# --------------------------------------------------

def fetch_25live_events(
    rss_urls: List[str],
    source_name: str = "RWU 25Live",
    headers: Dict[str, str] = DEFAULT_HEADERS,
    timeout: int = 10
) -> List[Dict]:
    """
    Fetch and parse events from one or more 25Live RSS feeds.

    Returns a list of normalized event dictionaries suitable
    for database insertion.
    """

    events: List[Dict] = []

    for url in rss_urls:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        strip_namespaces(root)

        for item in root.findall(".//item"):
            raw_description = item.findtext("description", "")
            description = clean_html(raw_description)

            event = {
                # --- identity / provenance ---
                "source": source_name,
                "source_url": url,
                "external_id": item.findtext("guid", "").strip(),

                # --- core event data ---
                "title": item.findtext("title", "").strip(),
                "link": item.findtext("link", "").strip(),
                "published_at": item.findtext("pubDate", "").strip(),
                "event_date_raw": item.findtext("category", "").strip(),

                # --- extracted metadata ---
                "organization": extract_field(description, "Organization"),
                "event_locator": extract_field(description, "Event Locator"),

                # --- raw + cleaned text ---
                "description": description,
                "raw_description": raw_description
            }

            events.append(event)

    return events
