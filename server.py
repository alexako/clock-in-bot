#!/Users/alex/Code/clock-in-bot/venv/bin

import clock_in_bot
from flask import Flask


app = Flask(__name__)

@app.route("/")
def clock_in():
    try:
        print("Sending request...")
        bot = clock_in_bot.ClockInBot()
        bot.send_request()
    finally:
        bot.quit()
        print("Done.")
        return "Done."


