from selenium import webdriver
from time import sleep
import os

# TODO: FIND A WAIT METHOD FOR PAGE LOAD THAT DOESNT USE SLEEP

class JobFinder:
    def __init__(self):
        self.LOAD_TIME = 1
        self.chrome_driver_path = "C:\Development\chromedriver.exe"
        # create driver
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path)

    def login(self):
        # get  page
        self.driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
        # get entries
        self.username_entry = self.driver.find_element_by_id('username')
        self.password_entry = self.driver.find_element_by_id('password')
        # fill entries
        # TODO: ensure that login credentials exist
        self.username_entry.send_keys('USERNAME')
        sleep(.3)
        self.password_entry.send_keys(os.environ.get('LINKEDIN_PASS'))
        sleep(.6)
        # get login btn
        self.login_btn = self.driver.find_element_by_xpath('/html/body/div/main/div[2]/div[1]/form/div[3]/button')
        # login
        self.login_btn.click()
        sleep(self.LOAD_TIME)

    def find_jobs(self):
        # load job search page
        self.jobs_btn = self.driver.find_element_by_id('ember27')
        self.jobs_btn.click()
        sleep(self.LOAD_TIME)
        # get job search entries
        self.job_entry = self.driver.find_element_by_xpath('//input[starts-with(@id, "jobs-search-box-keyword-id")]')
        self.location_entry = self.driver.find_element_by_xpath('//input[starts-with(@id, "jobs-search-box-location-id")]')
        # fill entries
        # TODO: make sure keywords exist
        self.job_entry.send_keys(os.environ.get('JOB_TITLE'))
        self.location_entry.send_keys(os.environ.get('LOCATION'))
        # get button
        self.job_search_btn = self.driver.find_element_by_css_selector('.jobs-search-box__submit-button')
        # search
        self.job_search_btn.click()
        sleep(self.LOAD_TIME)


    def save_job(self):
        self.apply_button = self.driver.find_element_by_xpath('//button[contains(@class, "jobs-apply-button")]')
        self.apply_button.click()
        print('Job saved')


if __name__ == '__main__':
    finder = JobFinder()
    finder.login()
    finder.find_jobs()
    sleep(1)
    finder.save_job()
