#!/bin/bash

pip install -r requirements.txt

while true; do
    script_name="bot.py"

    # Run the Python script in the foreground
    python3 "$script_name"

    # Sleep for 2 minutes
    sleep 120

    # Get the process ID of the existing bot.py process
    existing_pid=$(pgrep -f "$script_name")

    if [ -n "$existing_pid" ]; then
        # Kill the existing bot.py process
        echo "Killing existing bot.py process with PID $existing_pid"
        kill "$existing_pid"
    fi
done
