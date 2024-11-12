import json
import requests
from bs4 import BeautifulSoup

# Load names from the JSON file
def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

# Fetch all speaker links from the BYU speeches website
def fetch_all_speaker_links(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    soup = BeautifulSoup(response.content, 'html.parser')

    speaker_links = []
    # Find all speaker links
    for link in soup.find_all('a', class_='archive-item__link'):
        speaker_links.append(link['href'])
    return speaker_links

# Fetch speaker name from their individual page
def fetch_speaker_name(speaker_url):
    response = requests.get(speaker_url)
    response.raise_for_status()  # Raise an error for bad responses
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the speaker's name
    name = soup.find('h1', class_='single-speaker__name').text.strip()
    return name

# Compare names from JSON with those fetched from the website
def compare_names(json_data, website_names):
    matches = []
    json_names = {item['name'] for item in json_data}  # Set for faster lookup

    for name in website_names:
        if name in json_names:
            matches.append({"name": name})  # Store as a dictionary with key "name"
    return matches

# Save the matching names to a new JSON file
def save_matches_to_json(matches, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(matches, f, ensure_ascii=False, indent=4)

def main():
    json_filepath = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\all_GAs.json"
    byu_speakers_url = 'https://speeches.byu.edu/speakers/'
    output_filepath = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\all_GAs_BYU.json"

    # Load the JSON data
    json_data = load_json_file(json_filepath)

    # Fetch all speaker links from BYU website
    speaker_links = fetch_all_speaker_links(byu_speakers_url)
    
    # Fetch names from individual speaker pages
    website_names = []
    for link in speaker_links:
        try:
            name = fetch_speaker_name(link)
            website_names.append(name)
            print(f"Fetched name: {name}")
        except Exception as e:
            print(f"Error fetching {link}: {e}")

    # Compare names
    matches = compare_names(json_data, website_names)

    # Save matching names to a new JSON file
    save_matches_to_json(matches, output_filepath)

    # Print the matches
    print("Matching Names saved to:", output_filepath)
    print("Matches Found:", matches)

if __name__ == "__main__":
    main()
