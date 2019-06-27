import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

chrome_options = Options()
chrome_options.add_argument("--headless")
qa_host = os.getenv("QA_HOST")

# i'm a comment
class TestUIElements(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.driver = webdriver.Chrome(options=chrome_options, executable_path="/usr/bin/chromedriver")

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def test_special_checkbox(self):
        self.driver.get(qa_host)
        special = self.driver.find_element_by_id("special")
        assert special.get_attribute("type") == "checkbox"

    def test_digit_checkbox(self):
        self.driver.get(qa_host)
        digits = self.driver.find_element_by_id("numbers")
        assert digits.get_attribute("type") == "checkbox"

    def test_upper_checkbox(self):
        self.driver.get(qa_host)
        upper = self.driver.find_element_by_id("uppercase")
        assert upper.get_attribute("type") == "checkbox"
