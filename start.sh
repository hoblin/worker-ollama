#!/bin/bash

echo "Killing any running ollama processes..."
pgrep ollama | xargs kill

echo "Checking if /root/.ollama exists and it's not a symlink..."

if [ ! -e "/root/.ollama" ]; then
    echo "/root/.ollama does not exist. Creating a symlink..."
    ln -s /runpod-volume/ /root/.ollama
    echo "Symlink created."
fi

echo "Starting ollama server..."
ollama serve 2>&1 | tee ollama.server.log &
# Store the process ID (PID) of the background command

check_server_is_running() {
    # Replace "Listening" with the actual expected output
    if tail -n 1 ollama.server.log | grep -q "Listening"; then
        echo "Server is running."
        return 0 # Success
    else
        echo "Server is not running yet."
        return 1 # Failure
    fi
}

# Wait for the process to print "Listening"
echo "Waiting for server to start..."
while ! check_server_is_running; do
    sleep 1
done

echo "Pulling data with ollama..."
ollama pull $1

echo "Running runpod_wrapper.py..."
python -u runpod_wrapper.py $1
