from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import os
from time import sleep


class PriceFinder:
    def __init__(self):
        # determine driver path
        # TODO: create path setup for non-original user
        if os.name == 'posix':
            self.chrome_driver_path = '../Development/chromedriver'
        else:
            self.chrome_driver_path = r'C:\Development\chromedriver.exe'

        # create driver
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path)

    def get_prices(self, location: str, max_price: float, beds: str = 'any', baths: str = 'any', min_price: float = 1):
        self.driver.get('https://www.zillow.com/homes/for_rent/')
        try:
            self.search_bar = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Address, neighborhood, or ZIP"]'))
            )
        except TimeoutException:
            print('Search bar could not be located within timeout period')
            self.driver.quit()
        else:
            # make sure that search bar is clear of location data
            self.search_bar.send_keys(Keys.CONTROL + 'a')
            self.search_bar.send_keys(Keys.DELETE)
            # fill location data
            self.search_bar.send_keys(location)

            # get buttons
            self.price_btn = self.driver.find_element_by_id('price')
            self.beds_btn = self.driver.find_element_by_id('beds')

            # set price range
            self.price_btn.click()
            self.min_price_entry = self.driver.find_element_by_id('price-exposed-min')
            self.max_price_entry = self.driver.find_element_by_id('price-exposed-max')
            self.min_price_entry.send_keys(min_price)
            self.max_price_entry.send_keys(max_price)

            # set number of beds
            # ONLY TAKES 'ANY' OR NUMERICAL VALUE
            self.beds_btn.click()
            if beds.lower() == 'any':
                self.driver.find_element_by_xpath('//fieldset[@class="filter_beds"]/div/button[@value="0"]').click()
            else:
                try:
                    beds = int(beds)
                    if beds == 0:
                        raise ValueError
                except ValueError:
                    print('Not a valid number of beds\nOnly "Any" or numerical values accepted')
                else:
                    if beds >= 5:
                        self.driver.find_element_by_xpath(
                            '//fieldset[@class="filter_beds"]/div/button[@value="5"]').click()
                    else:
                        self.driver.find_element_by_xpath(
                            f'//fieldset[@class="filter_beds"]/div/button[@value="{beds}"]').click()

            # set number of baths
            if baths.lower() == 'any':
                self.driver.find_element_by_xpath('//fieldset[@class="filter_baths"]/div/button[@value="0"]').click()
            else:
                try:
                    baths = float(baths)
                    if baths == 0:
                        raise ValueError
                except ValueError:
                    print('Not a valid number of baths\nOnly "Any" or numerical values accepted')
                else:
                    if baths >= 4:
                        self.driver.find_element_by_xpath(
                            '//fieldset[@class="filter_baths"]/div/button[@value="4"]').click()
                    else:
                        self.driver.find_element_by_xpath(
                            f'//fieldset[@class="filter_baths"]/div/button[@value="{baths}"]').click()

            # get search results
            self.search_bar.click()
            self.search_bar.send_keys(Keys.ENTER)

            # get links
            sleep(10)  # used generic wait because list has already prefilled/cannot reliably check for delta
            self.links = self.driver.find_elements_by_class_name('list-card-link')
            self.prices = self.driver.find_elements_by_class_name('list-card-price')
            self.addresses = self.driver.find_elements_by_class_name('list-card-addr')
            print(self.links)
            print(self.prices)
            print(self.addresses)

            # create list of listings
            self.listings = [
                {'Address': self.addresses[i].text,
                 'Price': self.prices[i].text,
                 'Link': self.links[i].get_attribute('href')}
                for i in range(len(self.links))
            ]

    def export_locations_to_sheety(self):
        # TODO: create handle to ensure environmental variables exist for user
        for listing in self.listings:
            # convert listing to json
            self.payload = {
                'location': {
                    'address': listing['Address'],
                    'price': listing['Price'],
                    'link': listing['Link']
                }
            }
            # post to google sheet
            response = requests.post(
                url=os.environ.get('SHEETY_ENDPOINT'),
                json=self.payload,
            )
            # get response code
            response.raise_for_status()
            print(response)


if __name__ == '__main__':
    price_finder = PriceFinder()
    price_finder.get_prices('Seattle, WA')
    price_finder.export_locations_to_sheety()