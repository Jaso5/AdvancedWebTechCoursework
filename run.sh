#!/usr/bin/bash

# Activate venv
source .venv/bin/activate

# Start server
python -m gunicorn -b 0.0.0.0:5000 -w 1 src.main:app
