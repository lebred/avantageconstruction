from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Setup Selenium WebDriver
driver = webdriver.Chrome()  # Make sure to have the correct driver installed


def scrape_images_with_selenium(url, folder="images"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    driver.get(url)
    time.sleep(5)  # Wait for images to load

    # Parse the fully rendered page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    img_tags = soup.find_all("img")

    for img_tag in img_tags:
        img_url = get_high_res_image(img_tag, url)
        download_image(img_url, folder)

    driver.quit()


url_to_scrape = "https://www.avantagejmr.com/"
scrape_images_with_selenium(url_to_scrape)
