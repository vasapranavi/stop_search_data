# ---- Base ----
FROM python:3.10-slim

# System basics (optional but handy for SSL/CA & tzdata)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates tzdata && \
    rm -rf /var/lib/apt/lists/*

# ---- Workdir ----
WORKDIR /app

# ---- Copy app ----
# copy only what we need; keep data outside the image
COPY src/ ./src/
COPY config/ ./config/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ensure imports like `from src...` and `from config...` work
ENV PYTHONPATH=/app/src

# Data directory inside the container
RUN mkdir -p /app/data
VOLUME ["/app/data"]

# Default command: run updater (change to --init for first full pull)
CMD ["python", "-m", "src.main", "--update"]