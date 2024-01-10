#!/bin/bash

echo "Checking if /root/.ollama exists and it's not a symlink..."

if [ ! -e "/root/.ollama" ]; then
    echo "/root/.ollama does not exist. Creating a symlink..."
    ln -s /runpod-volume/ /root/.ollama
    echo "Symlink created."
fi

check_server_is_running() {
    # Send a GET request to the /api/tags endpoint and check the HTTP status code
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:11434/api/tags | grep -q "200"; then
        echo "Server is running."
        return 0 # Success
    else
        echo "Server is not running yet."
        return 1 # Failure
    fi
}

# Wait for the server to start
echo "Waiting for server to start..."
while ! check_server_is_running; do
    sleep 1
done

echo "Running runpod_wrapper.py..."
python -u runpod_wrapper.py $1
