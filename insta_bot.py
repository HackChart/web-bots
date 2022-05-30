from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import os


class InstaBot:
    def __init__(self):
        # determine driver path
        if os.name == 'posix':
            self.chrome_driver_path = '../Development/chromedriver'
        else:
            self.chrome_driver_path = 'C:\Development\chromedriver.exe'

        # create driver
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path)

    def login(self):
        # get page
        self.driver.get('https://www.instagram.com/')
        # wait for page to load
        try:
            self.username_entry = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, 'username'))
            )
        except TimeoutException:
            print('Login elements could not be found')
            self.driver.quit()
        else:
            # get remaining entries
            self.password_entry = self.driver.find_element_by_name('password')
            # fill entries / login
            # TODO: ensure that environmental variables exist
            self.username_entry.send_keys(os.environ.get('INSTA_USER'))
            self.password_entry.send_keys(os.environ.get('INSTA_PASS'))
            self.password_entry.send_keys(Keys.ENTER)

    def find_user(self, user):
        try:
            self.search_bar = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search"]'))
            )
        except TimeoutException:
            print('Search element not found')
            self.driver.quit()
        else:
            self.driver.get(f'https://www.instagram.com/{user}')

    def follow(self):
        try:
            self.follow_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="Follow"]'))
            )
        except TimeoutException:
            print('Follow button not found')
            self.driver.quit()
        else:
            self.follow_btn.click()


if __name__ == '__main__':
    bot = InstaBot()
    bot.login()
    bot.find_user(os.environ.get('TARGET_USER'))
    bot.follow()
