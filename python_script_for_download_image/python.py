from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import urllib.request
from selenium import webdriver

# Function to create directory if it does not exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to download images
def download_images(search_term, images_count):
    # Locate the search box and input the search term
    search_box = driver.find_element(By.NAME, "q")
    search_box.clear()
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.RETURN)

    # Wait for some time for the search results to load
    time.sleep(3)

    # Click on the Images tab
    images_tab = driver.find_element(By.XPATH, '//a[contains(@href, "tbm=isch")]')
    images_tab.click()

    # Wait for some time for the images to load
    time.sleep(3)

    # Scroll down the page to load more images
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Find and extract image URLs
    image_elements = driver.find_elements(By.XPATH, '//img[@class="rg_i Q4LuWd"]')
    image_urls = []
    for element in image_elements:
        src = element.get_attribute('src')
        alt = element.get_attribute('alt')
        if 'fracture' in alt.lower():
            image_urls.append(src)

    # Create directory for the search term
    search_directory = os.path.join('bone_non_fracture_data', search_term)
    create_directory(search_directory)

    # Download images
    count = 0
    for url in image_urls:
        if count >= images_count:
            break
        try:
            file_path = os.path.join(search_directory, f'{count+1}.png')
            urllib.request.urlretrieve(url, file_path)
            count += 1
        except Exception as e:
            print(f"Error downloading image {count+1}: {e}")

# Main script
driver = webdriver.Chrome()
driver.get("https://www.google.com")

search_terms = [
    'forearm bone x-ray fractured',
]
images_count = 200

# Create main directory for bone non-fracture data
create_directory('bone_fracture_data')

for term in search_terms:
    print(f"Downloading images for '{term}'...")
    download_images(term, images_count)

driver.quit()
