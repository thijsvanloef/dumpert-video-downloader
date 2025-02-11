FROM python:3.12-slim

# Add a user to run the application and create a directory to store the downloaded files
RUN adduser download_worker \
    && mkdir /download

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

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

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Change the ownership of the /app directory to the download_worker user
RUN chown -R download_worker /app /download

# Set the user to run the application
USER download_worker

EXPOSE 8080

# Run the download.py when the container launches
CMD ["python", "web.py"]