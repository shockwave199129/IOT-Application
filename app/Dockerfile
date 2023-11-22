# Use the official Python image as a base image with the desired version.
FROM python:3.9

# Create a directory for your application code and set it as the working directory.
RUN mkdir /app
WORKDIR /app

# Set environment variables to ensure Python runs in unbuffered mode.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/app"

# Copy the requirements file and install necessary system packages.
COPY ./requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Update pip and install Python packages.
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of your application code to the container.
COPY ./ /app/

RUN python genarate_key.py

# Define the command to run your FastAPI application.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers 4"]
