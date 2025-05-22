from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import datetime

STREAMLIT_APPS = ['https://homefinder-tampa.streamlit.app/']

# Set up Selenium webdriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)


# Iterate through each URL in the list
for url in STREAMLIT_APPS:
    try:
        # Navigate to the webpage
        driver.get(url)

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Check if the wake up button exists
        try:
            button = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//button[text()='Yes, get this app back up!']")))
            button.click()
        # Missing except or finally here causes SyntaxError
        except TimeoutException:
            print('error')

    except TimeoutException:
        print('error')
