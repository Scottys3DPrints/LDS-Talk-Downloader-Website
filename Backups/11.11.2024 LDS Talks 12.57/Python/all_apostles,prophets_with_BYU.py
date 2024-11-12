import json

# Define the file paths for both JSON files
speakers_file_path = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\all_speakers_with_byu_talks.json"
presidents_file_path = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\presidents_w_imgs.json"

# Read the data from both files using utf-8 encoding
with open(speakers_file_path, "r", encoding="utf-8") as file:
    all_speakers_data = json.load(file)

with open(presidents_file_path, "r", encoding="utf-8") as file:
    presidents_data = json.load(file)

# Find the names that are in both lists
presidents_names = [president['name'] for president in presidents_data]
common_names = [speaker['name'] for speaker in all_speakers_data if speaker['name'] in presidents_names]

# Prepare the data for the new JSON file
all_prophets_with_byu = []
for speaker in all_speakers_data:
    if speaker['name'] in common_names:
        byu_talks_count = speaker['byu_talks']
        
        # If 'byu_talks' is a list, count its length, otherwise use the integer value
        if isinstance(byu_talks_count, list):
            byu_talks_count = len(byu_talks_count)
        
        # Add the speaker and the byu_talks count to the result list
        all_prophets_with_byu.append({
            "name": speaker['name'],
            "byu_talks": byu_talks_count
        })

# Define the path for the new JSON file
output_file_path = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\all_prophets_with_BYU.json"

# Write the results to the new JSON file using utf-8 encoding
with open(output_file_path, "w", encoding="utf-8") as file:
    json.dump(all_prophets_with_byu, file, indent=4, ensure_ascii=False)

print("File saved as all_prophets_with_BYU.json")
