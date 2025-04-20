import time
import sqlite3
import re

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

from amenity_separator import clean_amenity_data

con = sqlite3.connect('apartment_data.db')
cur = con.cursor()

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode

# Access apartments.com
driver = webdriver.Chrome()

temp_driver = webdriver.Chrome()


def clean_price_range(price_str):
    if "Call for Rent" in price_str:
        return None, None
    prices = re.findall(r'\$([\d,]+)', price_str)
    prices = [int(p.replace(',', '')) for p in prices]
    if len(prices) == 1:
        return prices[0], prices[0]
    elif len(prices) == 2:
        return prices[0], prices[1]
    return None, None


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
                try:
                    apartment_pricing = apartment.find_element(By.CLASS_NAME, 'property-rents').text
                except NoSuchElementException:
                    apartment_pricing = 'None'

            min_price, max_price = clean_price_range(apartment_pricing)

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
                apartment_url = apartment.get_attribute("data-url")
                temp_driver.get(apartment_url)
                amenities = temp_driver.find_elements(By.CLASS_NAME, 'amenityLabel')
                for x in amenities:
                    if x.text != '':
                        apartment_amenities_list.append(x.text)

            apartment_list.append({
                'Apartment': apartment_title,
                'Address': apartment_address,
                'MinPrice': min_price,
                'MaxPrice': max_price,
                'Beds': apartment_beds,
                'Amenities': str(apartment_amenities_list)
            })

    return pd.DataFrame(apartment_list)


# Set options to display all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 0)  # Adjust to your console width if needed
pd.set_option('display.max_colwidth', None)

df = scrape_apartments(driver)

amenity_df = clean_amenity_data(df)

df.to_sql(name='apartments', con=con, if_exists='replace', index=False)

amenity_df.to_sql(name='amenities', con=con, if_exists='replace', index=False)

# Confirm desired output
#print(df)
#print(amenity_df)