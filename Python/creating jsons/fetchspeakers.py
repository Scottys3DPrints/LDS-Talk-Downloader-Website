import requests
from bs4 import BeautifulSoup
import json

# URLs for the First Presidency and Quorum of the Twelve Apostles
current_urls = [
    "https://www.churchofjesuschrist.org/learn/first-presidency?lang=eng",
    "https://www.churchofjesuschrist.org/learn/quorum-of-the-twelve-apostles?lang=eng"
]

# URL for all General Authorities
all_GAs_url = "https://www.churchofjesuschrist.org/study/general-conference/speakers?lang=eng"
base_url = "https://www.churchofjesuschrist.org"

def scrape_current_members():
    members = []

    for url in current_urls:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {url}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")

        # Find all <h4> tags for names and image tags with specific classes
        name_tags = soup.find_all("h4", string=True)
        image_tags = soup.find_all("img", alt=True, class_=lambda x: x and "ListTile__StyledImage" in x)

        if not name_tags or not image_tags:
            print(f"No name or image tags found on {url}")
            continue

        for name_tag, image_tag in zip(name_tags, image_tags):
            name = name_tag.text.strip()

            # Extract high-resolution image URL from srcset
            if 'srcset' in image_tag.attrs:
                srcset = image_tag['srcset']
                high_res_url = srcset.split(",")[-1].split(" ")[0]
            else:
                high_res_url = image_tag["src"]

            members.append({"name": name, "image": high_res_url})

    # Save to current.json
    save_path_current = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\current.json"
    with open(save_path_current, "w") as file:
        json.dump(members, file, indent=4)

    print(f"Saved current members to {save_path_current}")

def scrape_all_general_authorities():
    response = requests.get(all_GAs_url)
    if response.status_code != 200:
        print(f"Failed to fetch {all_GAs_url}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    all_general_authorities = []

    # Find all <a> tags with the specific link and name class
    speaker_links = soup.find_all("a", class_="sc-omeqik-0 ewktus tile-P903U listTile-WHLxI")

    for link in speaker_links:
        name_tag = link.find("h4", class_="sc-12mz36o-0 jSCFto sc-omeqik-9 dbmmCm")
        if name_tag:
            name = name_tag.text.strip()
            speaker_url = base_url + link["href"]

            # Fetch the speaker's page and count the number of General Conference talks
            speaker_response = requests.get(speaker_url)
            if speaker_response.status_code == 200:
                speaker_soup = BeautifulSoup(speaker_response.content, "html.parser")
                talk_count = len(speaker_soup.find_all("h4", class_="sc-12mz36o-0 jSCFto sc-omeqik-9 dbmmCm"))
            else:
                talk_count = 0  # If the page fails to load, set count to 0

            all_general_authorities.append({
                "name": name,
                "general_conference_talks": talk_count
            })

    # Save to all_GAs.json
    save_path_all_GAs = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\all_GAs.json"
    with open(save_path_all_GAs, "w") as file:
        json.dump(all_general_authorities, file, indent=4)

    print(f"Saved all general authorities to {save_path_all_GAs}")

if __name__ == "__main__":
    scrape_current_members()
    scrape_all_general_authorities()
