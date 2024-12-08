import requests
from pprint import pprint
from src.env import load_env
import paho.mqtt.client as mqtt
import random

current_print = {
    "filename": None,
    "metadata": None,
    "state": "complete"
}


def choose_message(type: str) -> str:
    return random.choices(
        [
            # Typed weirdly so the tts pronounces it correctly
            f"Print {type} on vore on",
            f"Print {type} on morr on",
            "Spaghetti detected on vore on",
            "Replicator reports job complete captain"
        ],
        weights=[
            0.7,
            0.1,
            0.1,
            0.1
        ],
        k=1
    )[0]


def handle_squawk(state):
    if state == "printing":
        current_print["state"] = state
    elif state == "paused" or state == "complete":
        if current_print["state"] != state:
            current_print["state"] = state
            # Connect here since we only need to connect once every few hours at most
            mqttc = mqtt.Client()
            mqttc.connect("mqtt.hacklab")
            mqttc.publish("sound/g1/speak", payload=choose_message(state))
            mqttc.disconnect()


def get(
    url: str,
    method: str,
    query=None,
    key=None
) -> requests.Response:
    # Construct base URL
    url = f"{url}/{method.lstrip('/')}"
    # Add query
    if type(query) == list:
        url += "?" + "&".join(query)
    elif type(query) == dict:
        url += "?" + "&".join(f"{k}={v}" for k, v in query.items())

    # Add api key
    headers = {}
    if key:
        headers["X-Api-Key"] = key

    # print(f"GET {url}")
    return requests.get(url, headers=headers)

def post(
    url: str,
    method: str,
    query=None,
    key=None
) -> requests.Response:
    # Construct base URL
    url = f"{url}/{method.lstrip('/')}"
    # Add query
    if type(query) == list:
        url += "?" + "&".join(query)
    elif type(query) == dict:
        url += "?" + "&".join(f"{k}={v}" for k, v in query.items())

    # Add api key
    headers = {}
    if key:
        headers["X-Api-Key"] = key

    # print(f"GET {url}")
    return requests.post(url, headers=headers)


def run():
    (printer_url, api_key) = load_env()

    pprint(get_packet(printer_url, api_key))


def get_cat(json, cat):
    return json.get("result").get("status").get(cat)


def get_state(json):
    return get_cat(json, "print_stats").get("state")


def get_file(json, printer_url, api_key):
    print_stats = get_cat(json, "print_stats")
    display = get_cat(json, "display_status")
    virtual_sdcard = get_cat(json, "virtual_sdcard")

    filename = print_stats.get("filename")

    if current_print["filename"] != filename:
        current_print["filename"] = filename
        try:
            current_print["metadata"] = get(
                "http://localhost", "server/files/metadata", query={"filename": filename}, key=api_key).json()
        except:
            pass

    return {
        "progress": display.get("progress"),
        "path": filename,
        "started": -1,
        "remaining": -1
    }


def get_thermals():
    return {}
    # return Thermals()


def get_packet(printer_url, api_key):

    try:
        res: requests.Response = get(printer_url, "printer/objects/query",
                                     ["virtual_sdcard", "print_stats", "display_status", "webhooks"], api_key)
    except Exception as e:
        return {
            "printer_state": "error",
            "message": f"{e}"
        }

    json = None
    try:
        json = res.json()
    except:
        print(res.text)

    webhooks = get_cat(json, "webhooks")

    if webhooks.get("state") == "error" or webhooks.get("state") == "shutdown":
        return {
            "printer_state": "error",
            "message": webhooks.get("state_message")
        }

    state = get_state(json)

    packet = {
        "printer_state": state
    }

    # print(f"State: {state}")
    # print(f"Persistent: {current_print}")

    if state == "standby":  # Ready to start printing
        pass
        # packet["limits"] = get_limits(json)
    elif state in ["printing", "paused", "complete", "cancelled"]:
        packet["file_info"] = get_file(json, printer_url, api_key)
        # packet["limits"] = get_limits(json)
        handle_squawk(state)
    elif state == "error":
        return {
            "printer_state": "error",
            "message": get_cat(json, "print_stats").get("message")
        }
    else:
        print(f"Unknown state {state}")

    return packet

    # return {
    #     "printer_state": state,
    #     "file_info": get_file(json),
    #     "limits": get_limits(),
    #     "thermals": get_thermals()
    # }
