#!/bin/bash

script_name="bot.py"
update() {
    git stash
    git pull
    pip install -r requirements.txt
}

start_bot() {
    echo "Starting $script_name..."
    { python3 "$script_name" 2>&1; } | tee /dev/tty &
}
}

stop_bot() {
    # Use pkill to send SIGTERM to the process with the specified name
    pkill -9 -f "$script_name"
}

while true; do
    update
    stop_bot
    clear
    start_bot

    # Sleep for 5 minutes
    sleep 300

    stop_bot
done
