import requests
from pprint import pprint
from src.env import load_env
import paho.mqtt.client as mqtt

current_print = {
    "filename": None,
    "metadata": None
}


mqttc = mqtt.Client()
mqttc.connect("mqtt.hacklab")

print_state = "complete"


def handle_squawk(state):
    match state:
        case "printing" as s:
            print_state = s
        case ("paused" | "complete") as s:
            if print_state != s:
                print_state = s
                mqttc.publish("sound/g1/speak", f"Print {s} on Voron")

def get(
    url: str,
    method: str,
    query = None,
    key = None
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
                printer_url, "server/files/metadata", query={"filename": filename}, key=api_key).json()
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

    match state:
        case "standby":  # Ready to start printing
            pass
            # packet["limits"] = get_limits(json)
        case "printing" | "paused" | "complete":
            packet["file_info"] = get_file(json, printer_url, api_key)
            # packet["limits"] = get_limits(json)
            handle_squawk(state)
        case "error":
            return {
                "printer_state": "error",
                "message": get_cat(json, "print_stats").get("message")
            }
        case _:
            print(f"Unknown state {state}")

    return packet

    # return {
    #     "printer_state": state,
    #     "file_info": get_file(json),
    #     "limits": get_limits(),
    #     "thermals": get_thermals()
    # }
