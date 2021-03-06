#!/usr/local/bin/python

from selenium import webdriver
from datetime import datetime
import requests
import sys
import os

import config


class ClockInBot():

    def __init__(self, headless=True):
        options = webdriver.ChromeOptions()
        if (headless):
            options.add_argument('headless')

        self.is_clocked_in = False
        self.last_activity = datetime.now().strftime("%H:%M:%S")
        self.pushover_url = "https://api.pushover.net/1/messages.json"

        self.driver = webdriver.Chrome(options=options)

        self.driver.get(config.URL_TARGET)
        self.driver.implicitly_wait(10)

    def update_state(self):
        status = self.driver.find_element_by_xpath('//*[@id="current_ebundy_status"]')
        self.last_activity = datetime.now().strftime("%H:%M:%S")
        self.is_clocked_in = status.get_attribute('value') == "TIME IN"

    def login(self):
        email_el = self.driver.find_element_by_xpath('//*[@name="email"]')
        email_el.send_keys(config.USERNAME)

        pw_el = self.driver.find_element_by_xpath('//*[@name="password"]')
        pw_el.send_keys(config.PASSWORD)

        login_btn = self.driver.find_element_by_xpath('//*[@type="submit"]')
        login_btn.click()
        self.driver.implicitly_wait(10)
        self.update_state()

    def clock_in(self):
        clock_in_btn = self.driver.find_element_by_xpath('//*[@id="time_btn"]')
        clock_in_btn.click()
        self.driver.implicitly_wait(10)
        self.update_state()

    def get_screenshot(self):
        self.driver.get_screenshot_as_file(os.path.join(os.environ['HOME'], "salarium.png"))

    def get_state(self):
        state = "out" if self.is_clocked_in else "in"
        return "You are currently clocked {0} at {1]".format(state, self.last_activity)

    def send_notification(self):
        state = "out" if self.is_clocked_in else "in"
        message = "You clocked {0} at {1}!".format(state, datetime.now().strftime("%H:%M:%S"))
        body = {
            'token': config.PUSHOVER_TOKEN,
            'user': config.PUSHOVER_USER,
            'message': message
        }
        screenshot= {
            "attachment": ("salarium.png", open(os.path.join(os.environ['HOME'], "salarium.png"), "rb"), "image/png")
        }
        return requests.post(self.pushover_url, data=body, files=screenshot)

    def send_request(self):
        state = "out" if self.is_clocked_in else "in"
        message = "Ready to clock {}?".format(state)
        link_title = "Click here to clock {}".format(state)
        body = {
            'token': config.PUSHOVER_TOKEN,
            'user': config.PUSHOVER_USER,
            'message': message,
            'url': config.CALLBACK_URL,
            'url_title': link_title
        }
        return requests.post(self.pushover_url, body)

    def quit(self):
        self.driver.quit()


if __name__ == '__main__':

    bot = ClockInBot(len(sys.argv) < 2)

    try:
        bot.login()
        bot.driver.implicitly_wait(10)
        bot.clock_in()
        bot.driver.implicitly_wait(10)
        bot.get_screenshot()
        bot.send_notification()
    finally:
        bot.quit()
        print('Done.')
