import json
import os
import requests
from urllib.parse import urljoin, urlparse, unquote
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from tkinter import Tk, filedialog

# Function to download and save images
def download_image(url, folder):
    response = requests.get(url, verify=False)
    
    img = Image.open(BytesIO(response.content))
    
    # Extract the image file name, stripping out any query strings
    parsed_url = urlparse(url)
    img_name = os.path.basename(parsed_url.path)
    
    # Remove any query strings from the file name
    img_name = unquote(img_name.split('?')[0])
    
    # Determine the correct extension if missing or corrupted
    if not img_name.lower().endswith(('jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff')):
        img_format = img.format.lower()
        img_name += f".{img_format}"
    
    # Construct the full path to save the image
    img_path = os.path.join(folder, img_name)
    
    # Save the image
    img.save(img_path)
    
    return img_path, img

# Function to extract metadata
def extract_metadata(image):
    return image.info

# Function to scrape images from a single page and save metadata to JSON
def scrape_images(url, folder, metadata_file):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    metadata_list = []

    for img_tag in img_tags:
        img_url = img_tag.get('src')
        if img_url:
            img_url = urljoin(url, img_url)
            try:
                img_path, img = download_image(img_url, folder)
                metadata = extract_metadata(img)
                print(f"Image: {img_path}, Metadata: {metadata}")
                
                # Store the metadata in a list
                metadata_list.append({
                    "image_path": img_path,
                    "metadata": metadata
                })
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")
    
    # Save metadata to a JSON file
    with open(metadata_file, 'w') as f:
        json.dump(metadata_list, f, indent=4)

# Recursive function to scrape an entire site
def scrape_site(url, folder, visited=None):
    if visited is None:
        visited = set()

    if url in visited:
        return
    visited.add(url)

    # Create a metadata JSON file
    metadata_file = os.path.join(folder, "image_metadata.json")
    scrape_images(url, folder, metadata_file)

    base_domain = urlparse(url).netloc
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a', href=True):
        next_url = link['href']
        next_url = urljoin(url, next_url)

        if urlparse(next_url).netloc == base_domain:
            scrape_site(next_url, folder, visited)

# Allow user to input URL
user_url = input("Enter the URL of the website to scrape images from: ").strip()

# Ensure the URL is properly formatted
if not user_url.startswith(('http://', 'https://')):
    user_url = 'http://' + user_url

# Create a Tkinter root widget, which is necessary to use filedialog
root = Tk()
root.withdraw()

# Prompt the user to select a directory
folder_selected = filedialog.askdirectory(title="Select Folder to Save Images")

if folder_selected:
    scrape_site(user_url, folder_selected)
    # Success message
    print("\nScraping completed successfully! Images and metadata saved.")
else:
    print("No folder selected. Exiting...")
