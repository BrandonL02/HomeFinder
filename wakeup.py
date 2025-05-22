from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from streamlit_app import STREAMLIT_APPS
import datetime

# Setup headless Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

# Log file setup
with open("wakeup_log.txt", "a") as log_file:
    log_file.write(f"\n=== Execution started at: {datetime.datetime.now()} ===\n")

    for url in STREAMLIT_APPS:
        try:
            driver.get(url)

            # Wait for body to ensure page loaded
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            try:
                # Try to find the "wake up" button by text
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Yes, get this app back up!']"))
                )
                button.click()
                log_file.write(f"[{datetime.datetime.now()}] ✅ App at {url} was successfully woken up.\n")
            except TimeoutException:
                log_file.write(f"[{datetime.datetime.now()}] ℹ️ No wake-up button found at: {url} — likely already awake.\n")

        except Exception as e:
            log_file.write(f"[{datetime.datetime.now()}] ❌ Error with {url}: {str(e)}\n")

driver.quit()
