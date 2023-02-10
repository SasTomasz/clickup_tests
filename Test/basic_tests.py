import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from Test import constant


class LoginTests(unittest.TestCase):
    login = constant.LOGIN
    password = constant.PASSWORD
    driver = webdriver.Chrome(service=Service("../Drivers/chromedriver.exe"))

    def test_correct_login_website(self):
        driver = self.driver
        driver.get("https://clickup.com")
        button = driver.find_element(By.XPATH, '//*[@id="header"]/div/nav/div/div/a')
        button.click()

        time.sleep(10)

        header = driver.find_element(By.XPATH, '//*[@id="app-root"]/cu-login/div/div[2]/div[2]/div[1]/cu-login-form/h1')

        self.assertEqual("Welcome back!", header.text)

    def tearDown(self) -> None:
        self.driver.quit()
