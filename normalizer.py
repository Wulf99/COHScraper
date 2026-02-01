# normalizer.py

from datetime import datetime, timezone
from typing import Dict
from email.utils import parsedate_to_datetime
# --------------------------------------------------

UNIVERSAL_SCHEMA = {
    # provenance
    "source": None,
    "source_url": None,
    "external_id": None,

    # core display
    "title": None,
    "description": None,
    "link": None,

    # time
    "published_at": None,
    "event_start": None,
    "event_end": None,
    "event_date_text": None,

    # location / org
    "location": None,
    "organization": None,
    "host": None,

    # athletics-specific (nullable)
    "sport": None,
    "opponent": None,
    "is_conference": None,
    "status": None,

    # metadata
    "ingested_at": None,
}


def normalize_event(raw: Dict) -> Dict:
    event = UNIVERSAL_SCHEMA.copy()

    field_map = {
        "start_time": "event_start",
        "end_time": "event_end",
        "event_date_raw": "event_date_text",
        "sport_abbr": "sport",
        "opponent_name": "opponent",
    }

    for key, value in raw.items():
        target_key = field_map.get(key, key)

        if target_key not in event or value is None:
            continue

        # ---- DATE PARSING ----
        if target_key in ("published_at", "event_start", "event_end"):
            if isinstance(value, str):
                try:
                    dt = parsedate_to_datetime(value)
                    event[target_key] = dt.replace(tzinfo=None)
                except Exception:
                    event[target_key] = None
            else:
                event[target_key] = value
        else:
            event[target_key] = value

    # ingested_at handled by runner
    event["ingested_at"] = None

    return event
