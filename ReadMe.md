# Purpose
This project was created as part of the COH Listens project to scrape Data from RWU events. This is to be later reviewed and used to inform decisions about gaps in DEI opportunities on campus

# Technical Information
- This project has 3 scrapers a normalizer and the runner.
- it imports the data into a mysql database which checks for uniqueness
- It scrapes all RWU events, athletics events and Hawklink events
  
  
# Testing Code (If issues arise)
# HawkLinkScraper Testing code

```python

# --------------------------------------------------
# Standalone test runner (DEV ONLY)
# --------------------------------------------------

if __name__ == "__main__":

    TEST_FEEDS = [
        "https://hawklink.rwu.edu/events.rss"
    ]

    events = fetch_hawklink_events(TEST_FEEDS)
    print(f"Fetched {len(events)} HawkLink events")

    if events:
        from pprint import pprint
        print("\nSample event:\n")
        pprint(events[0])
```

  
  

# Rwu25LiveScraper Testing Code
  
```python
# --------------------------------------------------
# Optional standalone test runner
# --------------------------------------------------
  
if __name__ == "__main__":
    TEST_FEEDS = [
            "https://25livepub.collegenet.com/calendars/community-events-6.rss",
    "https://25livepub.collegenet.com/calendars/alumni-events-6.rss",
    "https://25livepub.collegenet.com/calendars/parents-family-events.rss",
    "https://25livepub.collegenet.com/calendars/student-events-6.rss",
    "https://25livepub.collegenet.com/calendars/featured-events-10.rss",
    "https://25livepub.collegenet.com/calendars/faculty-staff-events-1.rss",
    # Add more RSS links here
    ]
  
    events = fetch_25live_events(TEST_FEEDS)
    print(f"Fetched {len(events)} events")

    # Preview one event for sanity check
    if events:
        from pprint import pprint
        pprint(events[0])

```
  
# Rwu_AthleticsScraper Testing code
 
```python

# --------------------------------------------------
# Standalone testing / dev mode
# --------------------------------------------------

if __name__ == "__main__":
    # Example: fetch the current month’s events
    sample_events = fetch_athletics_events()
    print(f"Fetched {len(sample_events)} RWU Athletics events")

    if sample_events:
        from pprint import pprint
        pprint(sample_events[0])

```

