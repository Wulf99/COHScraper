# runner.py

from typing import List
from datetime import datetime, timezone

import mysql.connector

from normalizer import normalize_event
from RWU25liveScraper import fetch_25live_events
from RWUHawklinkScraper import fetch_hawklink_events
from RWU_AthleticsScraper import fetch_athletics_events


# ----------------------------
# Database configuration
# ----------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Community430*",
    "database": "rwu_events",
}


# ----------------------------
# Scraper runner
# ----------------------------
def run_all_scrapers() -> List[dict]:
    all_events: List[dict] = []

    # -------- 25Live --------
    try:
        feeds_25live = [
            "https://25livepub.collegenet.com/calendars/community-events-6.rss",
            "https://25livepub.collegenet.com/calendars/alumni-events-6.rss",
            "https://25livepub.collegenet.com/calendars/parents-family-events.rss",
            "https://25livepub.collegenet.com/calendars/student-events-6.rss",
            "https://25livepub.collegenet.com/calendars/featured-events-10.rss",
            "https://25livepub.collegenet.com/calendars/faculty-staff-events-1.rss",
        ]

        events = fetch_25live_events(feeds_25live)
        all_events.extend(events)
        print(f"[OK] 25Live: {len(events)} events")

    except Exception as e:
        print(f"[ERROR] 25Live scraper failed: {e}")

    # -------- HawkLink --------
    try:
        hawklink_feeds = [
            "https://hawklink.rwu.edu/events.rss"
        ]

        events = fetch_hawklink_events(hawklink_feeds)
        all_events.extend(events)
        print(f"[OK] HawkLink: {len(events)} events")

    except Exception as e:
        print(f"[ERROR] HawkLink scraper failed: {e}")

    # -------- Athletics --------
    try:
        events = fetch_athletics_events()
        all_events.extend(events)
        print(f"[OK] Athletics: {len(events)} events")

    except Exception as e:
        print(f"[ERROR] Athletics scraper failed: {e}")

    return all_events


# ----------------------------
# Database insertion
# ----------------------------
def insert_events(events: List[dict]) -> None:
    if not events:
        print("[DB] No events to insert")
        return

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    sql = """
    INSERT INTO events (
        source, source_url, external_id,
        title, description, link,
        published_at, event_start, event_end, event_date_text,
        location, organization, host,
        sport, opponent, is_conference, status,
        ingested_at
    ) VALUES (
        %(source)s, %(source_url)s, %(external_id)s,
        %(title)s, %(description)s, %(link)s,
        %(published_at)s, %(event_start)s, %(event_end)s, %(event_date_text)s,
        %(location)s, %(organization)s, %(host)s,
        %(sport)s, %(opponent)s, %(is_conference)s, %(status)s,
        %(ingested_at)s
    )
    ON DUPLICATE KEY UPDATE
        title = VALUES(title),
        description = VALUES(description),
        link = VALUES(link),
        published_at = VALUES(published_at),
        event_start = VALUES(event_start),
        event_end = VALUES(event_end),
        event_date_text = VALUES(event_date_text),
        location = VALUES(location),
        organization = VALUES(organization),
        host = VALUES(host),
        sport = VALUES(sport),
        opponent = VALUES(opponent),
        is_conference = VALUES(is_conference),
        status = VALUES(status)
    """

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    rows = []
    for e in events:
        row = e.copy()

        # override ingested_at with a MySQL-safe datetime
        row["ingested_at"] = now

        rows.append(row)

    cursor.executemany(sql, rows)
    conn.commit()

    print(f"[DB] Inserted/updated {cursor.rowcount} rows")

    cursor.close()
    conn.close()


# ----------------------------
# Main
# ----------------------------
def main():
    raw_events = run_all_scrapers()

    normalized_events = [
        normalize_event(e) for e in raw_events
    ]

    print(f"\nTotal normalized events: {len(normalized_events)}")

    # sanity check
    if normalized_events:
        from pprint import pprint
        pprint(normalized_events[0])

    insert_events(normalized_events)


if __name__ == "__main__":
    main()
