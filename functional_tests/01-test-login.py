import os
import time
import unittest

from selenium import webdriver


class ReturningUser(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.url = os.environ.get("PYTEST_URL")
        self.username = os.environ.get("PYTEST_USERNAME")
        self.password = os.environ.get("PYTEST_PASSWORD")

    def tearDown(self):
        self.browser.quit()

    def test_can_login_with_registered_username(self):
        # User has heard about a cool new online service to archive videos and tag them.
        # User decides to visit its homepage.
        self.browser.get(self.url)

        # User checks the browser window for the correct title.
        self.assertIn("ViddlWS", self.browser.title)

        # User checks the displayed header text for the Sing In page.
        header_text = self.browser.find_element("tag name", "h1").text
        self.assertIn("Sign In", header_text)
        time.sleep(1)

        # The user already signed up earlier and wants to use the account again.
        # User fills out username (#id_login) field.
        inputbox = self.browser.find_element("id", "id_login")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Username")
        inputbox.send_keys(self.username)
        time.sleep(1)

        # User fills out password (#id_password) field.
        inputbox = self.browser.find_element("id", "id_password")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Password")
        inputbox.send_keys(self.password)
        time.sleep(1)

        # User clicks the login button.
        # https://stackoverflow.com/a/59505017
        login_button = 'button[class="primaryAction btn btn-primary"]'
        self.browser.find_element("css selector", login_button).click()
        time.sleep(1)

        # User is greeted with Your Videos page.
        header_text = self.browser.find_element("tag name", "h1").text
        self.assertIn("Your Videos", header_text)
        time.sleep(1)


if __name__ == "__main__":
    unittest.main()
