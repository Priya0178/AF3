#!/bin/bash

script_name="bot.py"

update() {
    git stash
    git pull
    pip install -r requirements.txt
}

start_bot() {
    echo "Starting $script_name..."
    python3 "$script_name" 2>&1 | tee /dev/tty &
}

stop_bot() {
    echo "Stopping $script_name..."
    pkill -9 -f "$script_name"
    wait $!
    echo "$script_name stopped."
}

while true; do
    update
    stop_bot
    clear
    start_bot

    # Sleep for 10 minutes
    sleep 120

    stop_bot
done
