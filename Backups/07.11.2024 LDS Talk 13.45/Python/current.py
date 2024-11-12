import requests
from bs4 import BeautifulSoup
import json

# URL of the website containing the list of church leaders
URL = "https://www.churchofjesuschrist.org/learn/quorum-of-the-twelve-apostles?lang=eng"  # Replace with the actual URL

def scrape_members():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all elements with the class that contains "Biography"
    bio_tags = soup.find_all("div", class_="sc-12qnjz9-0 dVlPOA ListTile__PrimaryMeta-webcon__sc-2dk18t-4 koRXWz")

    members = []
    for bio in bio_tags:
        # Find the next <h4> tag that contains the member's name
        name_tag = bio.find_next("h4", class_="sc-12mz36o-0 jSCFto ListTile__Title-webcon__sc-2dk18t-8 bhHzmh")
        if name_tag:
            name = name_tag.text.strip()  # Extract and clean the name text
            members.append(name)

    # Specify the file save location
    save_path = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\members.json"
    with open(save_path, "w") as file:
        json.dump(members, file, indent=4)

    print(f"Saved members to {save_path}")

if __name__ == "__main__":
    scrape_members()
