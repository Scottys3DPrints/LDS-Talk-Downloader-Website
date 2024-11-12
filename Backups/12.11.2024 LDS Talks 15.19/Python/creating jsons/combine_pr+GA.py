import json

# Define the file paths for the new JSON files
all_GAs_with_BYU_file_path = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\all_GAs_with_BYU.json"
all_apostles_with_BYU_file_path = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\all_apostles_with_BYU.json"
all_prophets_with_BYU_file_path = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\all_prophets_with_BYU.json"

# Read the data from all three files
with open(all_GAs_with_BYU_file_path, "r", encoding="utf-8") as file:
    all_GAs_with_BYU = json.load(file)

with open(all_apostles_with_BYU_file_path, "r", encoding="utf-8") as file:
    all_apostles_with_BYU = json.load(file)

with open(all_prophets_with_BYU_file_path, "r", encoding="utf-8") as file:
    all_prophets_with_BYU = json.load(file)

# Create a dictionary for quick lookup of GAs by name
ga_dict = {ga['name']: ga for ga in all_GAs_with_BYU}

# Combine the data
combined_data = []

# Add the GAs data into the combined list
for ga in all_GAs_with_BYU:
    combined_data.append({
        "name": ga['name'],
        "general_conference_talks": ga.get("general_conference_talks", "-"),
        "byu_talks": ga["byu_talks"]
    })

# Add the apostles data to the combined list
for apostle in all_apostles_with_BYU:
    if apostle['name'] in ga_dict:
        # If the name exists in GAs, combine the data
        ga = ga_dict[apostle['name']]
        ga["byu_talks"] += apostle["byu_talks"]  # Combine the BYU talks count
        if 'general_conference_talks' not in ga:
            ga["general_conference_talks"] = "-"  # Ensure general_conference_talks is included
    else:
        # If the name doesn't exist in GAs, add it with general_conference_talks as "-"
        combined_data.append({
            "name": apostle['name'],
            "general_conference_talks": "-",
            "byu_talks": apostle["byu_talks"]
        })

# Add the prophets data to the combined list
for prophet in all_prophets_with_BYU:
    if prophet['name'] in ga_dict:
        # If the name exists in GAs, combine the data
        ga = ga_dict[prophet['name']]
        ga["byu_talks"] += prophet["byu_talks"]  # Combine the BYU talks count
        if 'general_conference_talks' not in ga:
            ga["general_conference_talks"] = "-"  # Ensure general_conference_talks is included
    else:
        # If the name doesn't exist in GAs, add it with general_conference_talks as "-"
        combined_data.append({
            "name": prophet['name'],
            "general_conference_talks": "-",
            "byu_talks": prophet["byu_talks"]
        })

# Define the path for the new combined JSON file
output_file_path = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\all2_GAs+ap+pr_with_BYU.json"

# Write the combined data to the new JSON file
with open(output_file_path, "w", encoding="utf-8") as file:
    json.dump(combined_data, file, indent=4, ensure_ascii=False)

print("The combined file has been saved as all2_GAs+ap+pr_with_BYU.json.")
