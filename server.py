#!/Users/alex/Code/clock-in-bot/venv/bin

import clock_in_bot
from flask import Flask


app = Flask(__name__)
bot = clock_in_bot.ClockInBot()

@app.route("/clock-in")
def clock_in():
    try:
        print("Clocking in...")
        bot.login()
        bot.driver.implicitly_wait(10)
        bot.clock_in()
        bot.driver.implicitly_wait(10)
        bot.get_screenshot()
        resp = bot.send_notification()
        if not resp: raise Exception("resp is undefined for some reason..")
    except NewConnectionError:
        return "Could not connect. Check server logs."
    finally:
        print("Done.")
        return resp.reason

@app.route("/status")
def get_status():
    return bot.is_clocked_in


@app.route("/")
def send_request():
    try:
        print("Sending request...")
        resp = bot.send_request()
    finally:
        print("Done.")
        return resp.reason


