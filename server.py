#!/Users/alex/Code/clock-in-bot/venv/bin

from flask import Flask
import ast
import clock_in_bot


app = Flask(__name__)
bot = clock_in_bot.ClockInBot()
resp = None
log = []

@app.route("/clock-in")
def clock_in():
    try:
        print("Clocking in...")
        global resp
        if get_log_request(resp) not in log: raise Exception("Link expired.")
        bot.login()
        bot.driver.implicitly_wait(10)
        bot.clock_in()
        bot.driver.implicitly_wait(10)
        bot.get_screenshot()
        respClock = bot.send_notification()
        if not respClock: raise Exception("resp is undefined for some reason..")
    except NewConnectionError:
        return "Could not connect. Check server logs."
    finally:
        print("Done.")
        if resp.ok: log.remove(get_log_request(resp))
        return respClock.reason

@app.route("/status")
def get_status():
    print(log)
    return "Currently clocked {}".format("in" if bot.is_clocked_in else "out")


@app.route("/")
def send_request():
    try:
        print("Sending request...")
        global resp
        resp = bot.send_request()
        log.append(get_log_request(resp))
    finally:
        print("Done.")
        print(log)
        return resp.reason

def get_log_request(resp):
    return ast.literal_eval(resp.content.decode('utf8'))['request']
