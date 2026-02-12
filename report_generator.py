from collections import defaultdict
from datetime import datetime
import mysql.connector

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

# ----------------------------
# Report Name Generator
# ----------------------------
from datetime import datetime


def generate_report_filename(prefix="justice_report"):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{prefix}_{timestamp}.pdf"


# ----------------------------
# Database config (reuse yours)
# ----------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Community430*",
    "database": "rwu_events",
}


# ----------------------------
# Justice Categories + Keywords
# ----------------------------
JUSTICE_KEYWORDS = {
    "Latino Justice": [
        "latino", "latina", "latinx", "hispanic"
    ],

    "Asian Justice": [
        "asian", "aapi", "pacific islander"
    ],

    "Black Justice": [
        "black", "african american", "blm"
    ],

    "Indigenous Justice": [
        "indigenous", "native american", "tribal"
    ],

    "Immigrant Justice": [
        "immigrant", "immigration", "refugee"
    ],

    "LGBTQ+ Justice": [
        "lgbt", "lgbtq", "pride", "transgender", "queer"
    ],
}


# ----------------------------
# Fetch events from DB
# ----------------------------
def fetch_all_events():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT title, description, event_start, event_end
        FROM events
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


# ----------------------------
# Categorization Logic
# ----------------------------
def categorize_events(events):
    categorized = defaultdict(list)

    for event in events:
        text_blob = (
            (event["title"] or "") +
            " " +
            (event["description"] or "")
        ).lower()

        for category, keywords in JUSTICE_KEYWORDS.items():
            if any(keyword in text_blob for keyword in keywords):
                categorized[category].append(event)

    return categorized


# ----------------------------
# PDF Generation
# ----------------------------
def generate_pdf_report(categorized_events, output_file="justice_report.pdf"):
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    title = Paragraph("COH Justice Event Report", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 20))

    for category, events in categorized_events.items():

        elements.append(
            Paragraph(f"{category} ({len(events)} events)", styles["Heading1"])
        )
        elements.append(Spacer(1, 12))

        for e in events:
            start = e["event_start"]
            end = e["event_end"]

            start_str = start.strftime("%Y-%m-%d %H:%M") if start else "N/A"
            end_str = end.strftime("%Y-%m-%d %H:%M") if end else "N/A"

            elements.append(Paragraph(f"<b>{e['title']}</b>", styles["Heading3"]))
            elements.append(Paragraph(e["description"] or "No description", styles["BodyText"]))
            elements.append(
                Paragraph(f"Start: {start_str} | End: {end_str}", styles["Italic"])
            )

            elements.append(Spacer(1, 15))

    doc.build(elements)

    print(f"[REPORT] PDF generated: {output_file}")


# ----------------------------
# Main Reporting Runner
# ----------------------------
def main():
    print("[REPORT] Fetching events from DB...")
    events = fetch_all_events()

    print(f"[REPORT] {len(events)} events loaded")

    categorized = categorize_events(events)

    output_file = generate_report_filename()
    generate_pdf_report(categorized, output_file)



if __name__ == "__main__":
    main()
