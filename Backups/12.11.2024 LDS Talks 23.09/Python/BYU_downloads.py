import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = "C:\\_Download Talk Test Folder"

# Ensure the download folder exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Function to reformat the speaker's name
def reformat_name(name):
    try:
        parts = name.split()
        if len(parts) > 1:
            last_name = parts[-1]
            rest_of_name = " ".join(parts[:-1])
            formatted_name = f"{last_name}, {rest_of_name}"
            print(f"[DEBUG] Reformatted name: {formatted_name}")
            return formatted_name
        else:
            print("[DEBUG] Name has only one part, no reformatting needed.")
            return name
    except Exception as e:
        print(f"[ERROR] Error while reformatting name: {e}")
        return name

# Function to extract the year and month from the date span for each talk
def extract_year_month(date_tag):
    date_text = date_tag.get_text(strip=True)
    match = re.search(r'([A-Za-z]+) (\d{1,2}), (\d{4})', date_text)
    if match:
        month_str, _, year = match.groups()
        month_map = {
            "January": "01", "February": "02", "March": "03", "April": "04",
            "May": "05", "June": "06", "July": "07", "August": "08",
            "September": "09", "October": "10", "November": "11", "December": "12"
        }
        month = month_map.get(month_str, 'unknown')
        return year, month
    return 'unknown', 'unknown'

# Function to search for the speaker on the BYU website and download MP3 files
def search_and_download_mp3_files(formatted_name):
    try:
        url = "https://speeches.byu.edu/speakers/"
        print(f"[DEBUG] Sending request to {url}")
        response = requests.get(url)

        if response.status_code == 200:
            print("[DEBUG] Successfully received response from BYU website")
            soup = BeautifulSoup(response.content, "html.parser")
            speakers = soup.find_all("a", class_="archive-item__link")

            for speaker in speakers:
                speaker_name = speaker.get_text(strip=True)
                if formatted_name in speaker_name:
                    speaker_url = urljoin(url, speaker['href'])
                    print(f"[DEBUG] Match found: {speaker_name}, visiting {speaker_url}")

                    # Visit the speaker's page to get MP3 download links
                    speaker_response = requests.get(speaker_url)
                    if speaker_response.status_code == 200:
                        print("[DEBUG] Successfully reached the speaker's page")
                        speaker_soup = BeautifulSoup(speaker_response.content, "html.parser")

                        # Find all article elements for each talk
                        talks = speaker_soup.find_all('article', class_="card card--reduced")

                        for talk in talks:
                            # Extract the talk title
                            talk_title_tag = talk.find('h2', class_="card__header")
                            talk_title = talk_title_tag.get_text(strip=True) if talk_title_tag else "Unknown Title"

                            # Extract the MP3 download link
                            mp3_link_tag = talk.find('a', class_="download-links__option--available", string=lambda text: "MP3" in text)
                            if not mp3_link_tag:
                                print(f"No MP3 link found for talk: {talk_title}")
                                continue

                            mp3_link = urljoin(speaker_url, mp3_link_tag['href'])

                            # Extract the date for the talk
                            date_tag = talk.find('span', class_="card__speech-date")
                            if date_tag:
                                year, month = extract_year_month(date_tag)
                            else:
                                year, month = 'unknown', 'unknown'

                            # Generate the filename
                            file_name = f"{year}_{month}_BYU_{talk_title}_{formatted_name}.mp3"
                            file_name = re.sub(r'[^\w\s-]', '', file_name) + ".mp3"  # Ensure .mp3 extension
                            file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

                            # Download the MP3 file
                            print(f"[DEBUG] Downloading {mp3_link} to {file_path}")
                            mp3_response = requests.get(mp3_link)
                            if mp3_response.status_code == 200:
                                with open(file_path, "wb") as file:
                                    file.write(mp3_response.content)
                                print(f"[DEBUG] Successfully downloaded {file_path}")
                            else:
                                print(f"[ERROR] Failed to download {mp3_link}. Status code: {mp3_response.status_code}")

                        return f"Downloaded talks for {formatted_name}."
                    else:
                        print(f"[ERROR] Failed to load speaker's page. Status code: {speaker_response.status_code}")
                        return f"Failed to load speaker's page for {formatted_name}."
            print("[DEBUG] No match found for the speaker.")
        else:
            print(f"[ERROR] Failed to fetch BYU website. Status code: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Error while searching for speaker and downloading MP3 files: {e}")
    return f"{formatted_name} not found on BYU website."

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        print(f"[DEBUG] Received data: {data}")

        name = data.get('name', '')
        if not name:
            print("[ERROR] No name provided in the request.")
            return jsonify({"error": "No name provided"}), 400

        # Reformat the name
        formatted_name = reformat_name(name)

        # Search for the speaker and download MP3 files
        result = search_and_download_mp3_files(formatted_name)
        print(f"[DEBUG] Download result: {result}")

        return jsonify({"message": result})
    except Exception as e:
        print(f"[ERROR] Error in /download route: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == "__main__":
    print("[DEBUG] Starting Flask server...")
    app.run(debug=True)
