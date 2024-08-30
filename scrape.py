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


# Function to get the highest resolution image URL
def get_high_res_image(img_tag, base_url):
    # Check for common lazy loading attributes
    potential_urls = [
        img_tag.get("src"),
        img_tag.get("data-src"),
        img_tag.get("data-lazy"),
        img_tag.get("data-srcset"),
        img_tag.get("srcset"),
    ]

    # Filter out None values
    potential_urls = [url for url in potential_urls if url]

    # Process srcset if present
    for url in potential_urls:
        if "srcset" in img_tag.attrs:
            srcset = img_tag["srcset"]
            urls = [u.split(" ")[0] for u in srcset.split(",")]
            potential_urls.extend(urls)

    # Choose the highest resolution image
    high_res_url = max(potential_urls, key=lambda url: len(url))

    # Join relative URL with the base URL
    return urljoin(base_url, high_res_url)


# Main function to scrape images
def scrape_images(url, folder="images"):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Send a HTTP request to the URL
    response = requests.get(url)
    response.raise_for_status()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all image tags
    img_tags = soup.find_all("img")

    # Download each image
    for img_tag in img_tags:
        img_url = get_high_res_image(img_tag, url)
        download_image(img_url, folder)


# Replace with the URL you want to scrape
url_to_scrape = "https://www.avantagejmr.com/"

# Call the function to scrape images
scrape_images(url_to_scrape)
