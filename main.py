import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()
driver.get('https://www.apartments.com')
time.sleep(3)
search_box = driver.find_element(By.XPATH, '//*[@id="quickSearchLookup"]')
search_box.send_keys('Tampa, FL',Keys.RETURN)


time.sleep(3)

search_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/section[1]/div[1]/section/div/fieldset/div/div/button[2]')
search_button.click()

time.sleep(10) # Let the user actually see something!

#driver.quit()