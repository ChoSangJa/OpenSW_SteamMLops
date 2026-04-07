# Stage 1: Build requirements
FROM python:3.11-slim as requirements-stage

# Set environment variables for pip
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /tmp

# Copy only the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Build wheels for dependencies
RUN pip wheel --no-deps --wheel-dir /tmp/wheels -r requirements.txt


# Stage 2: Final minimal image
FROM python:3.11-slim

# Set python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-root system user and group for security
RUN addgroup --system appgroup && adduser --system --group appuser

# Copy the built wheels from the requirements stage
COPY --from=requirements-stage /tmp/wheels /wheels

# Install the wheels
RUN pip install --no-cache-dir /wheels/* \
    && rm -rf /wheels

# Copy the application code
COPY ./app ./app

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose the API port
EXPOSE 8000

# Start the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
