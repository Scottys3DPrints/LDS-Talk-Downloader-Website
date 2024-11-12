import json

# Load the JSON data from a file
def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

# Compare names and update byu_talks while keeping general_conference_talks
def compare_and_update(json_data_1, json_data_2):
    # Create a dictionary for easy lookup of byu_talks based on speaker name
    byu_talks_dict = {item['name']: item.get('byu_talks', '-') for item in json_data_2}
    
    updated_data = []
    
    for item in json_data_1:
        name = item['name']
        general_conference_talks = item.get('general_conference_talks', 0)
        
        # Check if the name is found in the byu_talks_dict
        byu_talks = byu_talks_dict.get(name, '-')  # Default to '-' if name is not found
        
        # Add the speaker with both general_conference_talks and byu_talks
        updated_data.append({
            "name": name,
            "general_conference_talks": general_conference_talks,
            "byu_talks": byu_talks
        })
    
    return updated_data

# Save the updated data to a new JSON file
def save_to_json(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    all_GAs_filepath = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\current.json"
    all_speakers_filepath = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\all_speakers_with_byu_talks.json"
    output_filepath = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\LDS Talk Downloader Website\json\current_with_byu.json"

    # Load the JSON data from the files
    all_GAs_data = load_json_file(all_GAs_filepath)
    all_speakers_data = load_json_file(all_speakers_filepath)
    
    # Compare and update the data
    updated_data = compare_and_update(all_GAs_data, all_speakers_data)
    
    # Save the updated data to the new JSON file
    save_to_json(updated_data, output_filepath)
    
    print("Updated data saved to:", output_filepath)

if __name__ == "__main__":
    main()
