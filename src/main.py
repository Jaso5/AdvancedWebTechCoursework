from flask import Flask, render_template
import logging

from src.env import load_env
import src.net as net

logging.getLogger(__name__)

app = Flask(__name__, static_url_path="", static_folder="static")

(printer_url, api_key) = load_env()


@app.route("/")
def main():
    return render_template("index.html", url=printer_url)
    # return send_from_directory(app.static_folder, "index.html") # type: ignore


@app.route("/api/update")
def api():
    return net.get_packet(printer_url, api_key)


@app.route("/api/lights/on")
def light_on():
    net.post(printer_url, "printer/gcode/script", {"script": "SET_FAN_SPEED FAN=caselight SPEED=0.5"}, key=api_key)
    return {"result": "Success"}


@app.route("/api/lights/off")
def light_off():
    net.post(printer_url, "printer/gcode/script", {"script": "SET_FAN_SPEED FAN=caselight SPEED=0"}, key=api_key)
    return {"result": "Success"}