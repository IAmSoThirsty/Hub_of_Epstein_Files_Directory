# Dockerfile for Epstein Files Hub
# Multi-stage build for optimized image size

FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies including Tesseract OCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p \
    data/public_files/fbi_vault \
    data/wikipedia \
    data/processed/text \
    data/processed/metadata \
    data/processed/indexed \
    logs \
    cache \
    tmp

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command
CMD ["python", "--version"]

# Development stage
FROM base as development

USER root
RUN pip install --no-cache-dir pytest pytest-cov ipython
USER appuser

CMD ["/bin/bash"]

# Production stage
FROM base as production

# Run as non-root user
USER appuser

# Entry point for production
CMD ["python", "scripts/generate-search-index.py"]
