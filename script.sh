#!/bin/bash

pip install -r requirements.txt

while true; do
    script_name="bot.py"

    # Run the Python script with a timeout of 2 minutes
    timeout 2m python3 "$script_name"

    # Sleep for a short duration before restarting (adjust as needed)
    sleep 2
done
