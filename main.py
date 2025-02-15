import os
import sys
import json
import requests
import ctypes
from pathlib import Path
from scraper import download_calendar
from calendar_processor import update_calendar

# User's home directory on Windows
USER_HOME = Path.home()

# Downloads directory path for current user
DOWNLOAD_DIR = USER_HOME / "Downloads"

# Path to save config.json
CONFIG_FILE = USER_HOME / "calendar_config.json"

def check_internet():
    """Checks for an active internet connection."""
    try:
        requests.get("https://www.google.com/", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def save_credentials(username, password):
    """Saves credentials to config.json."""
    credentials = {"username": username, "password": password}
    with open(CONFIG_FILE, "w") as file:
        json.dump(credentials, file)

def load_credentials():
    """Loads credentials from config.json or asks for them."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    
    save_credentials(username, password)
    return {"username": username, "password": password}

# Check internet connection before proceeding
if not check_internet():
    ctypes.windll.user32.MessageBoxW(0, "No internet connection. Please check your connection and try again.", "Connection Error", 0x10 | 0x1)
    exit()

# Load user credentials
credentials = load_credentials()
USERNAME = credentials.get("username")
PASSWORD = credentials.get("password")

# Validate credentials
if not USERNAME or not PASSWORD:
    print("⚠ Invalid credentials!")
    exit()

# Download and update calendar
new_file = download_calendar(USERNAME, PASSWORD, DOWNLOAD_DIR)
if new_file:
    update_calendar(new_file, CONFIG_FILE)
else:
    print("⚠ Failed to download the calendar.")