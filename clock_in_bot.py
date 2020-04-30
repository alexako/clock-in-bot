#!/usr/local/bin/python

from selenium import webdriver
from datetime import datetime
import requests
import sys

import config


class ClockInBot():

    def __init__(self, headless=True):
        options = webdriver.ChromeOptions()
        if (headless):
            options.add_argument('headless')

        self.is_clocked_in = False
        self.pushover_url = "https://api.pushover.net/1/messages.json"

        self.driver = webdriver.Chrome(options=options)

        self.driver.get(config.URL_TARGET)
        self.driver.implicitly_wait(10)

    def update_state(self):
        status = self.driver.find_element_by_xpath('//*[@id="current_ebundy_status"]')
        self.is_clocked_in = status.get_attribute('value') == "TIME IN"

    def login(self):
        base_window = self.driver.window_handles[0]

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
        date = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        self.driver.get_screenshot_as_file("/Users/alex/salarium_{0}.png".format(date))

    def send_notification(self):
        state = "out" if self.is_clocked_in else "in"
        message = "You clocked {0} at {1}!".format(state, datetime.now().strftime("%H:%M:%S"))
        body = {
            'token': config.PUSHOVER_TOKEN,
            'user': config.PUSHOVER_USER,
            'message': message
        }
        return requests.post(self.pushover_url, body)

    def send_request(self):
        message = "Ready to clock {}?".format("out" if self.is_clocked_in else "in")
        link_title = "Click here to clock {}".format("out" if self.is_clocked_in else "in")
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
