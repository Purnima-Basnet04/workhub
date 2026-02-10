# Use official Python base image
FROM python:3.13-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project, including templates
COPY . /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Collect static files (optional)
RUN python manage.py collectstatic --noinput

# Expose the port (Railway uses 8080)
EXPOSE 8080

# Start Gunicorn server
CMD ["gunicorn", "workhub.wsgi:application", "--bind", "0.0.0.0:8080"]
