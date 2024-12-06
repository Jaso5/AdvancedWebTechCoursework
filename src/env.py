import dotenv

def load_env():
    env = dotenv.dotenv_values(".env")
    if env.get("PRINTER-URL") == None:
        print("ERROR: please set 'PRINTER-URL' in .env")
        exit(-1)

    printer_url: str = env.get("PRINTER-URL")  # type: ignore
    api_key = env.get("MOONRAKER-API-KEY")

    if printer_url[0:4] != "http":
        printer_url = "http://" + printer_url

    return (printer_url, api_key)