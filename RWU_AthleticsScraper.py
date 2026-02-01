import requests
from typing import List, Dict
import re
from html import unescape

# --------------------------------------------------
# Shared helpers (can reuse from other scrapers)
# --------------------------------------------------

def clean_html(text: str) -> str:
    """Remove HTML tags and unescape HTML entities."""
    if not text:
        return ""
    text = unescape(text)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<.*?>", "", text)
    return text.strip()

# --------------------------------------------------
# Athletics scraper (Sidearm)
# --------------------------------------------------

def fetch_athletics_events(
    url: str = "https://rwuhawks.com/services/responsive-calendar.ashx",
    date: str = "1/25/2026 12:00:00 AM",
    sport: int = 0,
    location: str = "all",
    headers: Dict = None,
    timeout: int = 10
) -> List[Dict]:
    """
    Fetch RWU Athletics events from Sidearm responsive-calendar endpoint.
    Returns a list of normalized event dictionaries ready for DB insertion.
    """
    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://rwuhawks.com/calendar"
        }

    params = {
        "type": "month",
        "sport": sport,
        "location": location,
        "date": date
    }

    resp = requests.get(url, params=params, headers=headers, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()

    events: List[Dict] = []

    for day in data:
        day_events = day.get("events")
        if not day_events:
            continue  # skip days with no events

        for evt in day_events:
            sport_title = evt.get("sport", {}).get("title", "").strip()
            opponent_title = evt.get("opponent", {}).get("title", "").strip()

            event = {
                "source": "RWU Athletics",
                "external_id": str(evt.get("id", "")),
                "title": f"{sport_title} vs {opponent_title}" if opponent_title else sport_title,
                "link": evt.get("opponent", {}).get("website", ""),
                "description": f"{sport_title} game against {opponent_title} at {evt.get('location','')}" if opponent_title else f"{sport_title} event at {evt.get('location','')}",
                "start_time": evt.get("date", ""),
                "location": evt.get("location", ""),
                "status": evt.get("status", ""),
                "sport_abbr": evt.get("sport", {}).get("abbreviation", ""),
                "opponent_name": opponent_title,
                "opponent_location": evt.get("opponent", {}).get("location", ""),
                "is_conference": evt.get("conference", False),
                "type": evt.get("type", ""),
            }
            events.append(event)

    return events
