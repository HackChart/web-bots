from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class TinderBot:
    def __init__(self):
        # create webdriver
        self.chrome_driver_path = 'C:\Development\chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path)
