import ctypes
import requests
from datetime import datetime, timedelta
import os
from icalendar import Calendar

def check_internet_connection(url='https://www.google.com/', timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

def show_message_box(message, title, style):
    ctypes.windll.user32.MessageBoxW(0, message, title, style)

def read_ics(file_path):
    with open(file_path, "rb") as f:
        return Calendar.from_ical(f.read())

def wait_for_download(download_dir, filename, timeout=60):
    new_file = os.path.join(download_dir, filename)
    end_time = time.time() + timeout
    while time.time() < end_time:
        if os.path.exists(new_file):
            modified_time = datetime.fromtimestamp(os.path.getmtime(new_file))
            if datetime.now() - modified_time < timedelta(seconds=60):
                return new_file
        time.sleep(1)
    return None