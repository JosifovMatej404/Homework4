# Use Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies, including SQLite
RUN apt-get update && apt-get install -y \
    sqlite3 \
    libsqlite3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . /app/

ENV PYTHONPATH=/app

# Expose the port your Flask app will run on
EXPOSE 8050

# Command to run the application
CMD ["python", "app/server.py"]
