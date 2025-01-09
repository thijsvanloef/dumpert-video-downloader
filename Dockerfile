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
    unzip

# Download ChromeDriver
RUN wget -q -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.264/linux64/chromedriver-linux64.zip \
    && unzip /tmp/chromedriver.zip -d /tmp \
    && mv /tmp/chromedriver-linux64/chromedriver /app \
    && chmod +x /app/chromedriver

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get -y install google-chrome-stable

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Change the ownership of the /app directory to the download_worker user
RUN chown -R download_worker /app /download

# Set the user to run the application
USER download_worker

EXPOSE 8080

# Run the download.py when the container launches
CMD ["python", "web.py"]