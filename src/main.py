from flask import Flask, render_template
import logging

from env import load_env
import net

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