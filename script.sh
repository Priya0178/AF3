#!/bin/bash

git stash
git pull
chmod +x your_script.sh
pip install -r requirements.txt
script_name="bot.py"

start_bot() {
    echo "Starting $script_name..."
    python3 "$script_name" &
}

stop_bot() {
    # Get the process ID of the existing bot.py process
    existing_pid=$(pgrep -f "$script_name")

    if [ -n "$existing_pid" ]; then
        echo "Killing existing $script_name process with PID $existing_pid"
        kill "$existing_pid"
    fi
}

while true; do
    # Start the bot
    start_bot

    sleep 120

    stop_bot
done
