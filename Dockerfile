# Stage 1: Build stage
FROM python:3.11-slim AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Final stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /root/.local /root/.local
COPY . .

# Ensure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Expose the port Django runs on
EXPOSE 8000

# Run database migrations, collect static files, and start the app
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn configs.wsgi:application --bind 0.0.0.0:8000"]