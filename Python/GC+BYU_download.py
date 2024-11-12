from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
CORS(app)

BASE_URL = "https://www.churchofjesuschrist.org"
BYU_BASE_URL = "https://speeches.byu.edu/speakers/"
DOWNLOAD_FOLDER = "C:\\_Download Talk Test Folder"

# Ensure the download folder exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Function to download and save audio
def download_audio(audio_url, filename):
    try:
        response = requests.get(audio_url)
        response.raise_for_status()
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded and saved: {file_path}")
    except Exception as e:
        print(f"Error downloading audio: {e}")

# Function to extract year and month from the page
def extract_year_and_month(driver):
    try:
        date_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sc-1r3sor6-0'))
        )
        date_text = date_element.text.strip()
        match = re.search(r'(\w+)\s(\d{4})', date_text)
        if match:
            month = match.group(1)
            year = match.group(2)
            month_numeric = time.strptime(month, '%B').tm_mon
            month_str = f"{month_numeric:02d}"
            return year, month_str
        else:
            return "Unknown_Year", "Unknown_Month"
    except Exception as e:
        print(f"Error extracting year and month: {e}")
        return "Unknown_Year", "Unknown_Month"

# Function to process each General Conference talk
def process_general_conference_talk(driver, talk_url, speaker):
    try:
        driver.get(talk_url)
        time.sleep(2)
        try:
            consent_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'truste-consent-required'))
            )
            time.sleep(1)
            consent_button.click()
            print("Consent banner closed")
        except:
            print("No consent banner found")

        audio_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'AudioPlayer__AudioIconButton-sc-2r2ugr-0'))
        )
        time.sleep(1)
        audio_button.click()
        print("Audio button clicked successfully!")

        audio_source = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//source[@type="audio/mpeg"]'))
        )
        audio_url = audio_source.get_attribute('src')

        talk_title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )
        talk_title = talk_title_element.text.strip()
        print(f"Talk title: {talk_title}")

        if audio_url:
            print(f"Found audio link: {audio_url}")
            year, month = extract_year_and_month(driver)
            sanitized_talk_title = re.sub(r'[\\/*?:"<>|]', "", talk_title.replace(" ", "_"))
            filename = f"{year}_{month}_{sanitized_talk_title}_{speaker}.mp3"
            download_audio(audio_url, filename)
        else:
            print("Audio link not found.")
    except Exception as e:
        print(f"Error occurred while processing talk: {e}")

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

# Function to extract the year and month from the date span for each BYU talk
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
def search_and_download_byu_mp3_files(formatted_name):
    try:
        print(f"[DEBUG] Sending request to {BYU_BASE_URL}")
        response = requests.get(BYU_BASE_URL)

        if response.status_code == 200:
            print("[DEBUG] Successfully received response from BYU website")
            soup = BeautifulSoup(response.content, "html.parser")
            speakers = soup.find_all("a", class_="archive-item__link")

            for speaker in speakers:
                speaker_name = speaker.get_text(strip=True)
                if formatted_name in speaker_name:
                    speaker_url = urljoin(BYU_BASE_URL, speaker['href'])
                    print(f"[DEBUG] Match found: {speaker_name}, visiting {speaker_url}")

                    speaker_response = requests.get(speaker_url)
                    if speaker_response.status_code == 200:
                        print("[DEBUG] Successfully reached the speaker's page")
                        speaker_soup = BeautifulSoup(speaker_response.content, "html.parser")

                        talks = speaker_soup.find_all('article', class_="card card--reduced")

                        for talk in talks:
                            talk_title_tag = talk.find('h2', class_="card__header")
                            talk_title = talk_title_tag.get_text(strip=True) if talk_title_tag else "Unknown Title"

                            mp3_link_tag = talk.find('a', class_="download-links__option--available", string=lambda text: "MP3" in text)
                            if not mp3_link_tag:
                                print(f"No MP3 link found for talk: {talk_title}")
                                continue

                            mp3_link = urljoin(speaker_url, mp3_link_tag['href'])

                            date_tag = talk.find('span', class_="card__speech-date")
                            if date_tag:
                                year, month = extract_year_month(date_tag)
                            else:
                                year, month = 'unknown', 'unknown'

                            file_name = f"{year}_{month}_BYU_{talk_title}_{formatted_name}.mp3"
                            file_name = re.sub(r'[^\w\s-]', '', file_name) + ".mp3"
                            file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

                            print(f"[DEBUG] Downloading {mp3_link} to {file_path}")
                            mp3_response = requests.get(mp3_link)
                            if mp3_response.status_code == 200:
                                with open(file_path, "wb") as file:
                                    file.write(mp3_response.content)
                                print(f"[DEBUG] Successfully downloaded {file_path}")
                            else:
                                print(f"[ERROR] Failed to download {mp3_link}. Status code: {mp3_response.status_code}")

                        return f"Downloaded BYU talks for {formatted_name}."
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

        # Download General Conference talks
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920x1080")
        driver = webdriver.Firefox(options=options)

        try:
            search_url = f"{BASE_URL}/study/general-conference/speakers?lang=eng"
            response = requests.get(search_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            speaker_links = soup.find_all('a', href=True, class_=re.compile(r'sc-omeqik-0'))

            normalized_name = ' '.join(name.split()).lower()
            profile_url = None
            for link in speaker_links:
                h4_tag = link.find('h4', class_=re.compile(r'sc-12mz36o-0'))
                if h4_tag and h4_tag.text.strip().lower() == normalized_name:
                    profile_url = urljoin(BASE_URL, link['href'])
                    print(f"Speaker profile URL found: {profile_url}")
                    break

            if profile_url:
                response = requests.get(profile_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                talk_links = soup.find_all('a', class_=re.compile(r'sc-omeqik-0'))

                talk_names = []
                for talk_link in talk_links:
                    talk_url = urljoin(BASE_URL, talk_link['href'])
                    talk_title = talk_link.text.strip()
                    talk_names.append(talk_title)
                    process_general_conference_talk(driver, talk_url, name)

            else:
                print(f"Speaker '{name}' not found.")
                return jsonify({"error": f"Speaker '{name}' not found in General Conference talks."}), 404
        finally:
            driver.quit()

        # Download BYU talks
        formatted_name = reformat_name(name)
        byu_result = search_and_download_byu_mp3_files(formatted_name)

        return jsonify({
            "general_conference_talks": "Downloaded General Conference talks.",
            "byu_talks": byu_result
        })

    except Exception as e:
        print(f"[ERROR] Error in /download route: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == "__main__":
    print("[DEBUG] Starting Flask server...")
    app.run(debug=True)
