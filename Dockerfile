# Use Python slim image as base for smaller size
FROM python:3.10-slim

# Set environment variables
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Install minimal dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install requirements first (for better caching)
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

# Copy the application
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Set default command
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
