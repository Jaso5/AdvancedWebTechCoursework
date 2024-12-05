#!/usr/bin/bash

# Activate venv
source .venv/bin/activate

# Start server
python3.10 -m flask --app src/main run