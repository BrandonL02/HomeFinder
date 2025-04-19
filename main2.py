import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Access apartments.com

driver = webdriver.Chrome()


def scrape_apartments(driver):
    apartment_list = []

    for page in range(1, 19):
        driver.get(f'https://www.apartments.com/tampa-fl/{page}/')
        time.sleep(3)

        # extract data for that page
        data = driver.find_elements(By.CLASS_NAME, 'placard')

        for apartment in data:
            try:
                apartment_title = apartment.find_element(By.CLASS_NAME, 'property-title').text
            except NoSuchElementException:
                break  # No name means it is no longer apartments

            try:
                apartment_address = apartment.find_element(By.CLASS_NAME, 'property-address').text
            except NoSuchElementException:
                break

            try:
                apartment_pricing = apartment.find_element(By.CLASS_NAME, 'property-pricing').text
            except NoSuchElementException:
                apartment_pricing = 'None'

            try:
                apartment_beds = apartment.find_element(By.CLASS_NAME, 'property-beds').text
            except NoSuchElementException:
                apartment_beds = 'None'

            apartment_amenities_list = []
            try:
                apartment_amenities = apartment.find_element(By.CLASS_NAME, 'property-amenities')
                amenities = apartment_amenities.find_elements(By.TAG_NAME, 'span')
                for x in amenities:
                    if x.text != '':
                        apartment_amenities_list.append(x.text)
            except NoSuchElementException:
                try:
                    # add steps here to find amenities
                except NoSuchElementException:
                    pass  # fallback if element doesn't exist

            apartment_list.append({
                'Apartment': apartment_title,
                'Address': apartment_address,
                'Price': apartment_pricing,
                'Beds': apartment_beds,
                'Amenities': apartment_amenities_list
            })

    return pd.DataFrame(apartment_list)


# Set options to display all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 0)  # Adjust to your console width if needed
pd.set_option('display.max_colwidth', None)

df = scrape_apartments(driver)

print(df)
