#!/Users/alex/Code/clock-in-bot/venv/bin

import clock_in_bot
from flask import Flask


app = Flask(__name__)

@app.route("/clock-in")
def clock_in():
    try:
        print("Clocking in...")
        bot = clock_in_bot.ClockInBot()
        bot.login()
        bot.driver.implicitly_wait(10)
        bot.clock_in()
        bot.driver.implicitly_wait(10)
        bot.get_screenshot()
        resp = bot.send_notification()
    finally:
        bot.quit()
        print("Done.")
        return resp.reason

@app.route("/")
def send_request():
    try:
        print("Sending request...")
        bot = clock_in_bot.ClockInBot()
        resp = bot.send_request()
    finally:
        bot.quit()
        print("Done.")
        return resp.reason

