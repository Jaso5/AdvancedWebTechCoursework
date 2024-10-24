# Printer Status V2

This is the second iteration of the printer status display inside the Edinburgh hacklab. We use <https://github.com/dylan-thinnes/hacklab-status-screen> for our display, however any browser should work.

## Installing
This project was created for use with Poetry, please use `poetry install` to setup the dependencies and scripts to run

### Configuration
Please create a .env file in this project's root folder populated with these values:
```toml
PRINTER-URL = "URL to printer"
MOONRAKER-API-KEY = "Moonraker API key if needed"
```

## Running
Invoke `poetry run server`

## Tools

### klipper-get

A tool for quickly retriving things from moonraker, invoke with `poetry run klipper-get <args>`