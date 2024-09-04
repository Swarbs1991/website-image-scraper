import os
import requests
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from tkinter import Tk
from tkinter import filedialog

# Function to download and save images
def download_image(url, folder):
    response = requests.get(url, verify=False)  # Disable SSL verification here
    img = Image.open(BytesIO(response.content))
    img_name = os.path.join(folder, url.split('/')[-1])
    img.save(img_name)
    return img_name

# Function to extract metadata
def extract_metadata(image_path):
    img = Image.open(image_path)
    metadata = img.info
    return metadata

# Main function to scrape images
def scrape_images(url, folder='images'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    response = requests.get(url, verify=False)  # Disable SSL verification here
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    
    for img_tag in img_tags:
        img_url = img_tag.get('src')
        if img_url:
            # Handle relative URLs
            img_url = urljoin(url, img_url)
            img_path = download_image(img_url, folder)
            metadata = extract_metadata(img_path)
            print(f"Image: {img_path}, Metadata: {metadata}")

# Allow user to input URL
user_url = input("Enter the URL of the website to scrape images from: ").strip()

# Ensure the URL is properly formatted
if not user_url.startswith(('http://', 'https://')):
    user_url = 'http://' + user_url

# Create a Tkinter root widget, which is necessary to use filedialog
root = Tk()
root.withdraw()  # Hide the root window

# Prompt the user to select a directory
folder_selected = filedialog.askdirectory(title="Select Folder to Save Images")

if folder_selected:
    scrape_images(user_url, folder_selected)
else:
    print("No folder selected. Exiting...")
