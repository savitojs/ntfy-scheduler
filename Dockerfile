# Use the Red Hat UBI minimal base image
FROM registry.access.redhat.com/ubi9/python-39

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app /app

# Copy the entrypoint script and set the correct permissions
COPY entrypoint.sh /entrypoint.sh

# Switch to root user
USER root

# Add the exec perm
RUN chmod +x /entrypoint.sh

# Create the database file with appropriate permissions
RUN touch /app/messages.db && chmod 666 /app/messages.db && chown 1001:0 /app/messages.db

# Expose port 5000 for the Flask application
EXPOSE 5000

# Set the entrypoint script to start both the Flask app and the scheduler
ENTRYPOINT ["/entrypoint.sh"]

