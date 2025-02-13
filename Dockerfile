FROM python:3.12-slim

# Add a user to run the application and create a directory to store the downloaded files
RUN adduser download_worker && \
    mkdir /download

# Set the working directory
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxcb1 \
    wget \
    gnupg \
    ffmpeg \
    unzip \
    chromium-common \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Change the ownership of the /app directory to the download_worker user
RUN chown download_worker -R /app /download

# Set the user to run the application
USER download_worker

EXPOSE 8080

# Add a healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --spider --quiet http://127.0.0.1:8080 || exit 1

# Run the web.py when the container launches
CMD ["python", "web.py"]