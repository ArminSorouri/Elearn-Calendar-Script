from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time

# تنظیمات برای اجرای مرورگر
options = webdriver.FirefoxOptions()
#options.add_argument("--headless")  # اجرای مرورگر در حالت مخفی
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.dir", r"C:\Users\YourUser\Downloads")
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
options.set_preference("browser.safebrowsing.enabled", True)

# اجرای WebDriver
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

# باز کردن سایت
driver.get("https://calendar.google.com")

