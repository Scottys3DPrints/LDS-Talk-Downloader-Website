import json

# File paths for current.json and all_GAs.json
current_file_path = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\current.json"
all_GAs_file_path = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\all_GAs.json"

# Load data from both JSON files
with open(current_file_path, "r") as file:
    current_data = json.load(file)

with open(all_GAs_file_path, "r") as file:
    all_GAs_data = json.load(file)

# Create a dictionary from all_GAs.json for quick lookup of talk counts
all_GAs_dict = {item["name"]: item["general_conference_talks"] for item in all_GAs_data}

# Update current.json with the general conference talk counts
for member in current_data:
    if member["name"] in all_GAs_dict:
        member["general_conference_talks"] = all_GAs_dict[member["name"]]

# Save the updated current.json
with open(current_file_path, "w") as file:
    json.dump(current_data, file, indent=4)

print("current.json has been updated with general conference talk counts.")
