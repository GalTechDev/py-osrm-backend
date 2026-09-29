# py-osrm-backend Docker Image
# Multi-stage build for optimized image size

FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY setup.py pyproject.toml README.md ./

# Install the package
RUN pip install --no-cache-dir --user .

# Production image
FROM python:3.11-slim

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Create data directory for OSM files
RUN mkdir -p /app/data

# Copy source for running server
COPY src/ ./src/

# Expose the API port
EXPOSE 5000

# Server configuration (see osrm.server.api)
ENV OSRM_FILE=/app/data/map.osm \
    OSRM_HOST=0.0.0.0 \
    OSRM_PORT=5000

# Health check (the slim image has no curl)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Default command: run the API server
# Users should mount their OSM file to /app/data/map.osm
CMD ["python", "-m", "osrm.server.api"]
