# Use official Python image
FROM python:3.12.4

# Install system dependencies
RUN apt-get update -y && \
    apt-get install -y awscli libgl1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application code
COPY . /app

# Upgrade pip and install Python dependencies
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m pip install gunicorn

# Expose Flask port
EXPOSE 8080

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "application:app"]