This scraper has been made for the Communitys of Hope COH Listens 
This project was worked on by Jacob Barber and other members of the COH TechDev Team
Below is general information of how COHScraper.py works and its supporting modules



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
        "https://25livepub.collegenet.com/calendars/student-events-6.rss"
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