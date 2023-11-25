#!/bin/bash
pip install -r requirements.txt
while true; do
    script_name="bot.py"
    
    # Run the Python script
    python3 "$script_name" &
    # Sleep for 2 minutes before running the script again
    sleep 120
    existing_pid=$(pgrep -f "$script_name")

    if [ -n "$existing_pid" ]; then
        # Kill the existing bot.py process
        echo "Killing existing bot.py process with PID $existing_pid"
        kill "$existing_pid"
    fi
done
