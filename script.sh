#!/bin/bash

update() {
    git stash
    git pull
    pip install -r requirements.txt
    script_name="bot.py"
}

start_bot() {
    echo "Starting $script_name..."
    python3 "$script_name" &
}

stop_bot() {
    # Use pkill to send SIGTERM to the process with the specified name
    pkill -f "$script_name"
}

while true; do
    update
    start_bot

    # Sleep for 2 minutes
    sleep 120

    stop_bot
done
