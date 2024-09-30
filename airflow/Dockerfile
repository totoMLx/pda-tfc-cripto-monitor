# Use the official Airflow image as a parent image
FROM apache/airflow:2.10.2

# Set the working directory in the container
WORKDIR /opt/airflow

# Install additional necessary packages
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to the airflow user
USER airflow

# Copy the requirements file into the container at /opt/airflow
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt