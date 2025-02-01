# Use a lightweight Python image
FROM python:3.11-slim AS base

# Set environment variables to avoid buffer issues
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies for PostgreSQL and build tools
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies in a virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Django app files
COPY . .

# Expose the port Django runs on
EXPOSE 8000

# Run database migrations, collect static files, and start the app
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn configs.wsgi:application --bind 0.0.0.0:8000"]
