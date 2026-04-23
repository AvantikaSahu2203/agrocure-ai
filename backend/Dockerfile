FROM python:3.9-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libgl1 \
    libglib2.0-0 \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application ZIP and extract it 
# This handles the "app" folder correctly in Cloud environments
# Note: we allow exit code 1 from unzip to handle Windows backslash warnings
COPY app.zip .
RUN unzip -q app.zip || [ $? -eq 1 ] && rm app.zip

# Copy other root files (like the .pth model)
COPY . .

# Use dynamic port for Hugging Face (Port 7860)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
