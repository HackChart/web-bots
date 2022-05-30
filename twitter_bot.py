from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import re
import os

# DESIGNED TO COMPLAIN ABOUT YOUR INTERNET SPEED

class wait_for_text_to_match(object):
    def __init__(self, locator, pattern):
        self.locator = locator
        self.pattern = re.compile(pattern)

    def __call__(self, driver):
        try:
            element_text = EC._find_element(driver, self.locator).text
            return self.pattern.search(element_text)
        except StaleElementReferenceException:
            return False


class TwitterBot:
    def __init__(self):
        # create driver
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.chrome_driver_path = "C:\Development\chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path, options=self.options)

    def internet_speedtest(self):
        # sets consts for paid speeds
        self.MAX_DOWN = 1000
        self.MAX_UP = 40
        # set threshold level (currently 30% advertised speed)
        self.THRESHOLD = .30

        # determine threshold values
        self.down_threshold = self.MAX_DOWN * self.THRESHOLD
        self.up_threshold = self.MAX_UP * self.THRESHOLD

        # get speedtest
        self.driver.get('https://www.speedtest.net/')
        # start test
        self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a').click()

        # wait for speedtest to finish
        try:
            self.upload = WebDriverWait(self.driver, 120).until(wait_for_text_to_match((By.CSS_SELECTOR, '.upload-speed'), r'\d+\.\d+'))
        except TimeoutException:
            print('Could not locate element: WebDriver Timeout')
            self.driver.quit()
        else:
            # get results
            self.download = float(self.driver.find_element_by_css_selector('.download-speed').text)
            self.upload = float(self.upload.group(0))  # get string from regex match object
            print(f'Download: {self.download} {type(self.download)}')
            print(f'Upload: {self.upload} {type(self.upload)}')

        # determine whether to tweet or not
        if self.download <= self.down_threshold \
            or self.upload <= self.up_threshold:
            self.twitter_login()
            self.send_tweet()

    def twitter_login(self):
        # get page
        self.driver.get('https://twitter.com/login')
        # wait for login entries to load
        try:
            self.username_entry = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'session[username_or_email]'))
            )
        except TimeoutException:
            print('Login page has timed out')
            self.driver.quit()
        else:
            self.password_entry = self.driver.find_element_by_name('session[password]')
            self.username_entry.send_keys(os.environ.get('TWITTER_USERNAME'))
            self.password_entry.send_keys(os.environ.get('TWITTER_PASS'))
            self.password_entry.send_keys(Keys.ENTER)

    def send_tweet(self):
        try:
            self.tweet_editor = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'public-DraftEditor-content'))
        )
        except TimeoutException:
            print('Home page has timed out')
            self.driver.quit()
        else:
            self.tweet_editor.send_keys(f'Hey Comcast, why is my internet speed {self.download} down/{self.upload} up '
                                        f'when I pay for {self.MAX_DOWN} down/{self.MAX_UP} up')
            self.tweet_btn = self.driver.find_element_by_xpath('//div[@data-testid="tweetButtonInline"]')
            self.tweet_btn.click()


if __name__ == '__main__':
    twitter_bot = TwitterBot()
    twitter_bot.internet_speedtest()
