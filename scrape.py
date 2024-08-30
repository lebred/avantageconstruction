import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


# Function to download an image
def download_image(url, folder):
    try:
        # Send a HTTP request to the image
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Extract the image filename from the URL
        filename = os.path.basename(urlparse(url).path)
        file_path = os.path.join(folder, filename)

        # Save the image to the specified folder
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"Downloaded: {url}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")


# Main function to scrape images
def scrape_images(url, folder="images"):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Send a HTTP request to the URL
    response = requests.get(url)
    response.raise_for_status()
    headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)


    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all image tags
    img_tags = soup.find_all("img")

    # Extract the image URLs
    img_urls = [urljoin(url, img["src"]) for img in img_tags if "src" in img.attrs]

    # Download each image
    for img_url in img_urls:
        download_image(img_url, folder)


# Replace with the URL you want to scrape
url_to_scrape = "https://www.avantagejmr.com/"

# Call the function to scrape images
scrape_images(url_to_scrape)
