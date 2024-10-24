import argparse
import dotenv
import requests


def load_env() -> tuple[str, str | None]:
    env = dotenv.dotenv_values(".env")
    if env.get("PRINTER-URL") == None:
        print("ERROR: please set 'PRINTER-URL' in .env")
        exit(-1)

    printer_url: str = env.get("PRINTER-URL")  # type: ignore
    api_key = env.get("MOONRAKER-API-KEY")

    if printer_url[0:4] != "http":
        printer_url = "http://" + printer_url

    return (printer_url, api_key)


def get(url: str, method: str, key: str | None) -> requests.Response:
    url = f"{url}/{method}"

    print(f"GET {url}")

    return requests.get(url, headers={"X-Api-Key": key})

def run():
    parser = argparse.ArgumentParser(prog='klipper-get')
    parser.add_argument("-d", "--database", action='store_true',
                        help="Retrieve from the moonraker database instead")
    parser.add_argument("method")

    args = parser.parse_args()

    (printer_url, api_key) = load_env()
    print(f"Printer = {printer_url}")

    if args.database:
        # Get from the database <https://moonraker.readthedocs.io/en/latest/web_api/#database-apis>
        pass
    else:
        # Retrieve klipper object <https://moonraker.readthedocs.io/en/latest/web_api/#printer-status>
        pass


if __name__ == "__main__":
    run()
