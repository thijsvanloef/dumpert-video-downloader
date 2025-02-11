FROM python:3.12-slim

# Add a user to run the application and create a directory to store the downloaded files
RUN useradd download_worker \
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
    chromium-common=131.0.6778.139-1~deb12u1 \
    chromium=131.0.6778.139-1~deb12u1

# Download ChromeDriver
RUN if [ "$(uname -m)" = "aarch64" ]; then \
    wget -q -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.264/mac-arm64/chromedriver-mac-arm64.zip; \
    else \
    wget -q -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.264/linux64/chromedriver-linux64.zip; \
    fi \
    && unzip /tmp/chromedriver.zip -d /tmp \
    && mv /tmp/chromedriver-*/chromedriver /app \
    && chmod +x /app/chromedriver

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Change the ownership of the /app directory to the download_worker user
RUN chown -R download_worker /app /download

# Set the user to run the application
USER download_worker

EXPOSE 8080

# Run the download.py when the container launches
CMD ["python", "web.py"]