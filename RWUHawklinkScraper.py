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
# Shared helpers (same pattern as 25Live)
# --------------------------------------------------

def fetch_rss(url: str, headers=DEFAULT_HEADERS, timeout=10) -> ET.Element:
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return ET.fromstring(response.content)

def strip_namespaces(root: ET.Element) -> None:
    for el in root.iter():
        if "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]

def clean_html(text: str) -> str:
    if not text:
        return ""
    text = unescape(text)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<.*?>", "", text)
    return text.strip()

# --------------------------------------------------
# HawkLink-specific scraper
# --------------------------------------------------

def fetch_hawklink_events(
    rss_urls: List[str],
    source_name: str = "HawkLink",
    timeout: int = 10
) -> List[Dict]:
    """
    Fetch and parse events from HawkLink RSS feeds.

    Returns a list of normalized event dictionaries suitable
    for database insertion and downstream analysis.
    """

    events: List[Dict] = []

    for url in rss_urls:
        root = fetch_rss(url, timeout=timeout)
        strip_namespaces(root)

        for item in root.findall(".//item"):
            raw_description = item.findtext("description", "")
            description = clean_html(raw_description)

            event = {
                # --- provenance ---
                "source": source_name,
                "source_url": url,
                "external_id": item.findtext("guid", "").strip(),

                # --- core fields ---
                "title": item.findtext("title", "").strip(),
                "link": item.findtext("link", "").strip(),
                "published_at": item.findtext("pubDate", "").strip(),
                "category": item.findtext("category", "").strip(),

                # --- HawkLink-specific structured data ---
                "start_time": item.findtext("start", "").strip(),
                "end_time": item.findtext("end", "").strip(),
                "location": item.findtext("location", "").strip(),
                "host": item.findtext("host", "").strip(),
                "author": item.findtext("author", "").strip(),

                # --- text fields ---
                "description": description,
                "raw_description": raw_description
            }

            events.append(event)

    return events

