import requests
from bs4 import BeautifulSoup
import json
import os

# Define the path to your JSON file
json_file_path = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\presidents_w_imgs.json"

# Load the existing JSON data
with open(json_file_path, 'r') as file:
    presidents_data = json.load(file)

# Define the base URL for the images
base_url = "https://newsroom.churchofjesuschrist.org"

# Function to fetch images for each president
def fetch_images():
    for president in presidents_data:
        name = president['Name']
        # Fetch the webpage for church presidents
        search_url = f"https://newsroom.churchofjesuschrist.org/article/church-presidents"
        response = requests.get(search_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the strong tag with the president's name
            strong_tag = soup.find('strong', string=name)
            if strong_tag:
                # Get the parent of the strong tag to find the corresponding image
                img_tag = strong_tag.find_next('img')
                if img_tag and 'src' in img_tag.attrs:
                    # Extract the image source and create the full URL
                    img_src = img_tag['src']
                    full_image_url = base_url + img_src.replace('192x256', '640x853')  # Replace with a higher resolution
                    
                    # Add the image URL to the president's data
                    president['image'] = full_image_url
                    print(f"Added image for {name}: {full_image_url}")
                else:
                    print(f"No image found for {name}")
            else:
                print(f"{name} not found on the page")
        else:
            print(f"Failed to fetch the page for {name}")

    # Save the updated data back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(presidents_data, file, indent=4)

    print(f"Updated JSON file saved at {json_file_path}")

if __name__ == "__main__":
    fetch_images()
