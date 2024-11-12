from flask import Flask, request, jsonify, send_from_directory
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
from flask import render_template

app = Flask(__name__)
CORS(app)

BASE_URL = "https://www.churchofjesuschrist.org"
BYU_BASE_URL = "https://speeches.byu.edu/speakers/"

# Set the path to save downloaded audio files
DOWNLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

speaker_folder = None  # Global variable for the speaker folder


# Define a route for the home page
@app.route('/')
def home():
    return render_template('index.html')


# Function to create a folder for the speaker in the Downloads directory
def create_speaker_folder(speaker_name):
    global speaker_folder
    speaker_folder = os.path.join(DOWNLOAD_FOLDER, speaker_name)
    if not os.path.exists(speaker_folder):
        os.makedirs(speaker_folder)


# Function to download and save audio
def download_audio(audio_url, filename):
    try:
        file_path = os.path.join(speaker_folder, filename)
        response = requests.get(audio_url)
        response.raise_for_status()
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded and saved: {file_path}")
        return file_path  # Return the file path to serve it later
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None


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
def process_general_conference_talk(driver, talk_url, speaker_name):
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
            filename = f"{year}_{month}_{sanitized_talk_title}_{speaker_name}.mp3"
            return download_audio(audio_url, filename)
        else:
            print("Audio link not found.")
            return None
    except Exception as e:
        print(f"Error occurred while processing talk: {e}")
        return None


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


# Route for downloading the file
@app.route('/download_file/<filename>', methods=['GET'])
def download_file(filename):
    try:
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            return send_from_directory(directory=DOWNLOAD_FOLDER, filename=filename)
        else:
            return jsonify({"error": "File not found!"}), 404
    except Exception as e:
        print(f"Error in download_file: {e}")
        return jsonify({"error": str(e)}), 500


# Route for BYU downloads
@app.route('/byu_download', methods=['POST'])
def byu_download():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"error": "No name provided"}), 400

    create_speaker_folder(name)  # Create the folder once
    formatted_name = reformat_name(name)
    file_path = process_general_conference_talk(None, "", formatted_name)

    if file_path:
        return jsonify({
            "message": "Download completed.",
            "download_link": f"/download_file/{os.path.basename(file_path)}"  # Link to download the file
        })
    else:
        return jsonify({"error": "Failed to download file"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
