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

    def test_can_add_a_new_video(self):
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

        # User wants to download a new video. Only the video should be downloaded no audio files be extracted.
        # User clicks the Add Video navigation link.
        # https://stackoverflow.com/a/59505017
        self.browser.find_element("link text", "Add Video").click()
        time.sleep(1)

        # User is greeted with the formular to add a new video.
        header_text = self.browser.find_element("tag name", "h1").text
        self.assertIn("Add a video to be downloaded", header_text)
        time.sleep(1)

        # User fills out the owners video title field.
        inputbox = self.browser.find_element("id", "id_title")
        inputbox.send_keys("test add video")
        time.sleep(1)

        # User fills out url field.
        inputbox = self.browser.find_element("id", "id_url")
        inputbox.send_keys("https://www.youtube.com/watch?v=hS5CfP8n_js")
        time.sleep(1)

        # User fills out the tags field.
        inputbox = self.browser.find_element("id", "id_tags")
        inputbox.send_keys("test-tag")
        time.sleep(1)

        # User clicks the submit button.
        # https://stackoverflow.com/a/59505017
        submit_button = 'button[class="btn btn-primary"]'
        self.browser.find_element("css selector", submit_button).click()
        time.sleep(1)

        # User is send back to the Your Videos page.
        header_text = self.browser.find_element("tag name", "h1").text
        self.assertIn("Your Videos", header_text)
        time.sleep(1)

        card_titles_selector = 'h5[class="card-title list-title truncate"]'
        card_titles = self.browser.find_elements("css selector", card_titles_selector)
        self.assertIn("test add video", [card_title.text for card_title in card_titles])


if __name__ == "__main__":
    unittest.main()
