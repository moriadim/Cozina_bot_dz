# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot source code
COPY main.py ./
COPY recipes.json ./
COPY subscribers.json ./
COPY limits.json ./

# Optionally copy .env if you want to build with secrets (not recommended for production)
# COPY .env ./

# Run the bot
CMD ["python", "main.py"] 