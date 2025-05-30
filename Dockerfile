# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install uv package manager
RUN pip install uv

# Copy project files
COPY pyproject.toml ./
COPY main.py ./
COPY server.py ./
COPY README.md ./

# Copy .env file if it exists (optional)
COPY .env* ./

# Install dependencies using uv
RUN uv sync

# Expose the port your server runs on
EXPOSE 6969

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Command to run the server
CMD ["uv", "run", "server.py"]