# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.10-alpine
EXPOSE 8000

WORKDIR /app

# Install system dependencies
RUN apk update && \
    apk add --no-cache \
    bash \
    sqlite-dev \
    gcc \
    musl-dev

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Run server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
