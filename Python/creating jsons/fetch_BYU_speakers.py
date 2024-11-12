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

# Fetch speaker name and MP3 download links from their individual page
def fetch_speaker_name_and_mp3_links(speaker_url):
    response = requests.get(speaker_url)
    response.raise_for_status()  # Raise an error for bad responses
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the speaker's name
    name = soup.find('h1', class_='single-speaker__name').text.strip()
    
    # Find all MP3 download links (excluding PDF)
    mp3_links = soup.find_all('a', class_='download-links__option download-links__option--reduced download-links__option--available')
    
    # Count only MP3 links (exclude links that contain .pdf)
    mp3_count = sum(1 for link in mp3_links if '.mp3' in link['href'])
    
    return name, mp3_count

# Save all speaker names and MP3 counts to a new JSON file
def save_speakers_to_json(speakers, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(speakers, f, ensure_ascii=False, indent=4)

def main():
    byu_speakers_url = 'https://speeches.byu.edu/speakers/'
    output_filepath = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\all_speakers_with_byu_talks.json"

    # Fetch all speaker links from BYU website
    speaker_links = fetch_all_speaker_links(byu_speakers_url)
    
    # Fetch names and MP3 counts from individual speaker pages
    all_speakers = []
    for link in speaker_links:
        try:
            name, mp3_count = fetch_speaker_name_and_mp3_links(link)
            all_speakers.append({"name": name, "byu_talks": mp3_count})  # Store as a dictionary with "byu_talks" key
            print(f"Fetched name: {name}, BYU Talks: {mp3_count}")
        except Exception as e:
            print(f"Error fetching {link}: {e}")

    # Save all speaker names and MP3 counts to the JSON file
    save_speakers_to_json(all_speakers, output_filepath)

    # Print the total number of names saved
    print("All speaker names and BYU talks saved to:", output_filepath)
    print("Total Speakers Found:", len(all_speakers))

if __name__ == "__main__":
    main()
