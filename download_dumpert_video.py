import requests
import subprocess
import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import argparse
import logging
import sys
from colorlog import ColoredFormatter


# Set up logging
# Create a formatter with colors
formatter = ColoredFormatter(
    "%(log_color)s%(levelname)s:%(name)s:%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'white',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)

# Set up the logger
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# # Set up argument parser
# parser = argparse.ArgumentParser(description='Download video from Dumpert')
# parser.add_argument('url', type=str, help='URL of the Dumpert video page')
# args = parser.parse_args()

def download_video(url):
# Use the provided URL
    dumpert_url = url

    # Send a GET request to the URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(dumpert_url, headers=headers)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the video tag
    video_tag = soup.find('video')

    # Extract the source URL from the video tag
    if video_tag:
        source_tag = video_tag.find('source')
        if source_tag:
            video_url = source_tag['src']
            logging.info(f"Video URL: {video_url}")
        else:
            logging.warning("No source tag found in the video tag.")
    else:
        logging.warning("No video tag found in the HTML content.")
        # Set up Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument('log-level=3')

        # Enable performance logging
        perf_log_prefs = {
            'enableNetwork': True,
        }
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

        service = Service('/app/chromedriver')  # Update with the path to your chromedriver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            # Load the page
            driver.get(dumpert_url)

            # Wait for the video element to be present
            video_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )

            # Start video playback
            driver.execute_script("arguments[0].play();", video_element)

            # Wait for a few seconds to ensure .ts files are loaded
            time.sleep(5)

            # Get the network logs
            logs = driver.get_log("performance")

            # Extract .ts file URLs from the logs
            ts_urls = []
            for log in logs:
                if ".ts" in log["message"]:
                    message_parts = log["message"].split('"url":"')
                    if len(message_parts) > 1:
                        ts_url = message_parts[1].split('"')[0]
                        ts_urls.append(ts_url)
                    ts_urls.append(ts_url)

            if ts_urls:
                ts_urls = [url for url in ts_urls if not url.endswith('.js')]
                logging.debug("Filtered .ts URLs:", ts_urls)
                ts_url_output = ts_urls[0].replace('000.ts', '{index:03d}.ts')
            else:
                logging.error("No .ts files found in the network logs.")

        finally:
            driver.quit()

    logging.info(ts_url_output)

    # Generate a unique ID using the current timestamp
    unique_id = str(int(time.time()))

    # Directory to save the .ts files with a unique ID
    ts_dir = f"ts_files_{unique_id}"
    os.makedirs(ts_dir, exist_ok=True)

    ts_file_paths = []
    index = 1

    # Extract the quality from the ts_url
    quality = ts_url.split('/')[-2]
    # Find the highest quality available
    qualities = set()
    for ts_url in ts_urls:
        quality = ts_url.split('/')[-2]
        qualities.add(quality)

    highest_quality = max(qualities, key=lambda q: int(q.replace('p', '')))

    logging.info(f"Highest quality available: {highest_quality}")

    # Update ts_url_output to use the highest quality
    ts_url_output = ts_url_output.replace(quality, highest_quality)

    while True:
        ts_url = ts_url_output.format(index=index)
        response = requests.get(ts_url, stream=True)
        
        if response.status_code == 200:
            ts_file_path = os.path.join(ts_dir, f"video_{index:03d}.ts")
            with open(ts_file_path, "wb") as ts_file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        ts_file.write(chunk)
            ts_file_paths.append(ts_file_path)
            logging.info(f"TS file {ts_url} downloaded successfully!")
            index += 1
        else:
            logging.info(f"No more TS files found after index {index-1}.")
            break

    # Stitch the .ts files together
    with open("file_list.txt", "w") as file_list:
        for ts_file_path in ts_file_paths:
            file_list.write(f"file '{ts_file_path}'\n")

    # Convert the stitched .ts files to .mp4 using ffmpeg
    mp4_file_path = f"/download/video_{dumpert_url.split('=')[1]}.mp4"
    logging.info("Starting TS files stitch and conversion")
    subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "file_list.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-y", mp4_file_path])
    logging.info("TS files stitched and converted to MP4 successfully!")

    # Clean up the .ts files, the file list, and the folder
    for ts_file_path in ts_file_paths:
        os.remove(ts_file_path)
    os.remove("file_list.txt")
    os.rmdir(ts_dir)
    logging.info("Temporary TS files, file list, and folder cleaned up successfully!")

    return mp4_file_path

if __name__ == '__main__':
    # test1.py executed as script
    # do something
    download_video(url)