# Use Python 3.10 as the base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Playwright and Chromium
# This ensures the browser runs smoothly in the cloud
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium
RUN playwright install-deps

# Copy your application code
COPY . .

# Create downloads directory with write permissions
RUN mkdir -p /app/downloads && chmod 777 /app/downloads

# Expose port 7860 (Hugging Face specific port)
EXPOSE 7860

# Run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]