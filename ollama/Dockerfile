# ollama/Dockerfile

# Use the official Ollama image as a base
FROM ollama/ollama

# Copy the Modelfile into the image
COPY Modelfile /root/.ollama/Modelfile

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]
