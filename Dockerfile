# Pinned Debian Bookworm Python runtime
 FROM python:3.11.8-slim-bookworm
# Pinned to the exact immutable bitstream of the image on Docker Hub
#FROM python:3.11.8-slim-bookworm@sha256:90f8795536170fd08236d2ceb74fe7065dbf74f738d8b84bfbf263656654dc9b

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Pinned system runtime dependencies for OpenCASCADE & X11 headless rendering
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglu1-mesa \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install pinned Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application assets
COPY app.py .
COPY fonts/ ./fonts/
COPY templates/ ./templates/
COPY static/ ./static/

EXPOSE 8000

# Direct exec form entrypoint without shell wrapping
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]