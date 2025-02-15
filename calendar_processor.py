import os
from icalendar import Calendar
from pathlib import Path

def update_calendar(new_file, config_file):
    """Updates the calendar file by keeping only new events."""
    
    # Get user's home directory on Windows
    HOME = Path.home()
    
    # Path to the old file (existing calendar file in system)
    #old_file = config_file.with_name("calendar.ics")
    old_file = HOME / "Downloads" / "icalexport.ics"

    # If old file doesn't exist, just rename the new file
    if not os.path.exists(old_file):
        os.rename(new_file, old_file)
        print("✅ New calendar file saved.")
        return
    
    # Read old and new calendar data
    def read_ics(file_path):
        with open(file_path, "rb") as f:
            return Calendar.from_ical(f.read())

    old_calendar = read_ics(old_file)
    new_calendar = read_ics(new_file)

    # Get UIDs of existing events
    old_uids = {event.get("UID") for event in old_calendar.subcomponents if event.name == "VEVENT"}

    # Create new calendar with filtered events
    filtered_calendar = Calendar()
    filtered_calendar.add("VERSION", "2.0")
    filtered_calendar.add("PRODID", "-//Filtered Calendar//EN")

    # Add only new events (events not in old calendar)
    for event in new_calendar.subcomponents:
        if event.name == "VEVENT" and event.get("UID") not in old_uids:
            filtered_calendar.add_component(event)

    # Save updated calendar and cleanup
    with open(old_file, "wb") as f:
        f.write(filtered_calendar.to_ical())

    os.remove(new_file)
    print("✅ Calendar updated: only new events are kept, and the old file is replaced.")