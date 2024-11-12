import json
import requests
from bs4 import BeautifulSoup

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

# Save all speaker names to a new JSON file
def save_speakers_to_json(speakers, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(speakers, f, ensure_ascii=False, indent=4)

def main():
    byu_speakers_url = 'https://speeches.byu.edu/speakers/'
    output_filepath = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\all_speakers_BYU.json"

    # Fetch all speaker links from BYU website
    speaker_links = fetch_all_speaker_links(byu_speakers_url)
    
    # Fetch names from individual speaker pages
    all_speakers = []
    for link in speaker_links:
        try:
            name = fetch_speaker_name(link)
            all_speakers.append({"name": name})  # Store as a dictionary with key "name"
            print(f"Fetched name: {name}")
        except Exception as e:
            print(f"Error fetching {link}: {e}")

    # Save all speaker names to the JSON file
    save_speakers_to_json(all_speakers, output_filepath)

    # Print the total number of names saved
    print("All speaker names saved to:", output_filepath)
    print("Total Speakers Found:", len(all_speakers))

if __name__ == "__main__":
    main()
