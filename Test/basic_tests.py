import os
import time
import unittest

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

BASE_URL = "https://clickup.com/"


class LoginTests(unittest.TestCase):
    driver = None

    def setUp(self) -> None:
        self.driver = webdriver.Chrome(service=Service("../Drivers/chromedriver.exe"))
        self.driver.implicitly_wait(60)

    def test_correct_login_page_header(self):
        driver = self.driver
        driver.get(BASE_URL)

        login_button = driver.find_element(By.XPATH, '//*[@id="header"]/div/nav/div/div/a')
        login_button.click()

        header = driver.find_element(By.XPATH, '//*[@id="app-root"]/cu-login/div/div[2]/div[2]/div[1]/cu-login-form/h1')

        expected_header = "Welcome back!"
        self.assertEqual(expected_header, header.text,
                         f"Expected login page header: {expected_header} "
                         f"is different from actual header: {header.text}")

    def test_correct_login(self):
        load_dotenv("clickup_test_environment.env")
        correct_login = os.getenv("CLICKUP_EMAIL")
        correct_password = os.getenv("CLICKUP_PASSWORD")
        driver = self.driver

        driver.get(BASE_URL)
        login_button = driver.find_element(By.XPATH, '//*[@id="header"]/div/nav/div/div/a')
        login_button.click()

        email_field = driver.find_element(By.ID, 'login-email-input')
        password_field = driver.find_element(By.ID, 'login-password-input')
        email_field.send_keys(correct_login)
        password_field.send_keys(correct_password, Keys.ENTER)

        home_navigation_bar = driver.find_element(By.XPATH, '//*[@id="app-root"]/cu-app-shell/cu-manager/div[1]/div/'
                                                            'div[2]/cu-simple-bar/div/div[3]/a[1]')
        expected_home_navigation_bar_text = "Home"

        self.assertEqual(expected_home_navigation_bar_text, home_navigation_bar.text,
                         f"Expected Home navigation bar text: {expected_home_navigation_bar_text} "
                         f"is different from actual: {home_navigation_bar.text}")

        # Log out from account
        avatar = driver.find_element(By.XPATH, '//*[@id="app-root"]/cu-app-shell/cu-manager/div[1]/div/div[2]/'
                                               'cu-simple-bar/div/div[4]/cu-user-settings-menu/div/div/cu-team-avatar')
        avatar.click()
        log_out_button = driver.find_element(By.XPATH, '//*[contains(text(), "Log out")]')

        log_out_button.click()
        time.sleep(10)

    def tearDown(self) -> None:
        self.driver.quit()
