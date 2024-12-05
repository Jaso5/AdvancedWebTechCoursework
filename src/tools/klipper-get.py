import argparse
import requests
from pprint import pprint
from src.env import load_env
from src.net import get


def run():
    parser = argparse.ArgumentParser(prog='klipper-get')
    parser.add_argument("-d", "--database", action='store_true',
                        help="Retrieve from the moonraker database instead")
    parser.add_argument("method", nargs='*')

    args = parser.parse_args()

    (printer_url, api_key) = load_env()
    print(f"Printer = {printer_url}")

    res: requests.Response

    if args.database:
        # Get from the database <https://moonraker.readthedocs.io/en/latest/web_api/#database-apis>
        if args.method[0] == "list":
            res = get(
                printer_url, f"server/database/{args.method[0]}", key=api_key)
        if args.method[0] == "item":
            arguments = {
                "namespace": "fluidd",  # args.method[1],
                # "key": args.method[2]
            }
            res = get(printer_url, f"server/database/item",
                      arguments, key=api_key)
        else:
            print(f"Unknown command {args.method}")
            exit(-1)
    else:
        # Retrieve klipper object <https://moonraker.readthedocs.io/en/latest/web_api/#printer-status>
        if args.method[0] == "query":
            res = get(printer_url, f"printer/objects/query",
                      args.method[1:], key=api_key)
        else:
            res = get(printer_url, f"{args.method[0]}", key=api_key)

    try:
        pprint(res.json())
    except:
        print(res.text)

if __name__ == "__main__":
    run()
