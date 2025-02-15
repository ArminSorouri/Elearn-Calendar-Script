from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time
import os

def download_calendar(username, password, download_dir):
    """Logs in to the website and downloads the calendar file."""
    
    # Configure Firefox options
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", str(download_dir))  # Change download path to given directory
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    options.set_preference("browser.safebrowsing.enabled", True)

    # Initialize Firefox driver with configured options
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    
    try:
        # Navigate to calendar export page
        driver.get("https://elearn.ut.ac.ir/calendar/export.php?")
        
        # Find login form elements
        username_input = driver.find_element(By.ID, "Username")
        password_input = driver.find_element(By.ID, "password")

        # Enter credentials and submit
        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        # Wait for login to complete
        time.sleep(3)

        # Navigate to export page again after login
        driver.get("https://elearn.ut.ac.ir/calendar/export.php?")

        # Find and click export options
        checkbox1 = driver.find_element(By.ID, "id_events_exportevents_all")
        checkbox2 = driver.find_element(By.ID, "id_period_timeperiod_weeknow")

        checkbox1.click()
        checkbox2.click()

        # Click download button
        download_button = driver.find_element(By.ID, "id_export")
        download_button.click()

        # Check if file has been downloaded
        new_file = os.path.join(download_dir, "icalexport(1).ics")
        download_wait_time = 60
        end_time = time.time() + download_wait_time

        # Wait for file to appear in download directory
        while time.time() < end_time:
            if os.path.exists(new_file):
                return new_file
            time.sleep(1)

        print("⚠ Download did not complete in the expected time.")
        return None

    finally:
        # Clean up browser instance
        driver.quit()