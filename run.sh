#!/usr/bin/bash

# Activate venv
source .venv/bin/activate

# Start server
python -m flask --app src/main run
