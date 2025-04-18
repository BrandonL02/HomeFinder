import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Access apartments.com

driver = webdriver.Chrome()
driver.get('https://www.apartments.com')

time.sleep(3)  # wait for page to load

# Search city in the searchbar

search_box = driver.find_element(By.XPATH, '//*[@id="quickSearchLookup"]')
search_box.send_keys('Tampa, FL', Keys.RETURN)

time.sleep(3)  # wait for page to load

# Set apartment criteria

# Price

driver.find_element(By.XPATH, '//*[@id="rentRangeLink"]').click()

min_price = driver.find_element(By.XPATH, '//*[@id="min-input"]')
min_price.send_keys('1000')

max_price = driver.find_element(By.XPATH, '//*[@id="max-input"]')
max_price.send_keys('1300')

time.sleep(2)

# Beds/Baths

driver.find_element(By.XPATH, '//*[@id="bedRangeLink"]').click()

for x in range(1, 5):
    if x != 2 and x != 3:
        continue
    # 2 = studio / 3 = one bedroom
    driver.find_element(By.XPATH,
                        f'/html/body/div[1]/main/section/header/div/span[3]/div/div/div/div[1]/div/button[{x}]').click()

time.sleep(2)

# Home type

driver.find_element(By.XPATH, '//*[@id="typeSelect"]')

driver.find_element(By.XPATH, '/html/body/div[1]/main/section/header/div/span[5]/div/div/div[1]/button[1]/i').click()

time.sleep(5)
