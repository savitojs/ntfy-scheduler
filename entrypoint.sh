#!/bin/bash

# Initialize the database
python /app/database.py

# Function to handle SIGTERM and stop child processes
terminate() {
    echo "Terminating..."
    kill -TERM "$flask_pid" 2>/dev/null
    kill -TERM "$scheduler_pid" 2>/dev/null
    wait "$flask_pid"
    wait "$scheduler_pid"
    exit 0
}

# Start the Flask app in the background
python /app/main.py &
flask_pid=$!

# Start the scheduler in the background
python /app/scheduler.py &
scheduler_pid=$!

# Trap SIGTERM signal and call the terminate function
trap terminate SIGTERM

# Wait for child processes to finish
wait "$flask_pid"
wait "$scheduler_pid"
