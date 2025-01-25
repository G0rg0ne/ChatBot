# Use NVIDIA PyTorch container which comes with Python 3.10
FROM nvcr.io/nvidia/pytorch:23.12-py3

# Set environment variables for Python
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

# Install additional system dependencies if needed
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Set the Langflow port
ENV LANGFLOW_PORT=7860

EXPOSE 7860
EXPOSE 11434

# Run Langflow (if you're using CMD)
CMD ["langflow", "--port", "7860"]