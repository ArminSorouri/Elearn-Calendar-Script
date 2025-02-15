import os
from icalendar import Calendar

# File paths
old_file = r"C:\Users\Armin\Downloads\icalexport.ics"
new_file = r"C:\Users\Armin\Downloads\icalexport(1).ics"

# Check if old file exists
if not os.path.exists(old_file):
    print("⚠ Old file does not exist, renaming new file.")
    if os.path.exists(new_file):
        os.rename(new_file, old_file)
        print("✅ New file has been renamed to old file.")
    else:
        print("⚠ New file does not exist either.")
else:
    if not os.path.exists(new_file):
        print("⚠ New file does not exist.")
    else:
        # Function to read ICS file
        def read_ics(file_path):
            with open(file_path, "rb") as f:
                return Calendar.from_ical(f.read())

        old_calendar = read_ics(old_file)
        new_calendar = read_ics(new_file)

        # Extract UIDs from old file
        old_uids = {event.get("UID") for event in old_calendar.subcomponents if event.name == "VEVENT"}

        # Filter only new events
        filtered_calendar = Calendar()
        filtered_calendar.add("VERSION", "2.0")
        filtered_calendar.add("PRODID", "-//Filtered Calendar//EN")

        for event in new_calendar.subcomponents:
            if event.name == "VEVENT" and event.get("UID") not in old_uids:
                filtered_calendar.add_component(event)

        # Save filtered events to the new old_file
        with open(old_file, "wb") as f:
            f.write(filtered_calendar.to_ical())

        # Remove new_file
        os.remove(new_file)
        
        print("✅ Calendar updated: only new events are kept, and the old file is replaced.")
