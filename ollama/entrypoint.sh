#!/bin/sh
set -e

# Start Ollama server in the background
ollama serve &
pid=$!

# Wait for the server to be ready
echo "Waiting for Ollama server to start..."
sleep 300

# Pull models
echo "Pulling embedding model..."
ollama pull nomic-embed-text

echo "Pulling base model for morales1..."
ollama pull gemma3:4b-it-qat
sleep 5

# Create the custom model
echo "Creating morales1 model..."
ollama create morales1 -f /root/.ollama/Modelfile
sleep 5

echo "Listing models..."
ollama list

# Bring the server process to the foreground
wait $pid