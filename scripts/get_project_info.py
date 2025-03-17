import os
import json

def get_folder_structure(root_dir):
    """Recursively scans the folder structure and returns a dictionary."""
    folder_structure = {}

    for item in sorted(os.listdir(root_dir)):  # Sorted for consistency
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            folder_structure[item] = get_folder_structure(item_path)  # Recursive call for directories
        else:
            folder_structure[item] = "file"  # Mark files distinctly

    return folder_structure

def save_to_json(structure, output_file="folder_structure.json"):
    """Save the folder structure to a JSON file."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=4)
    print(f"✅ Folder structure saved to {output_file}")

if __name__ == "__main__":
    root_directory = "."  # Scans the current directory
    print(f"🔍 Scanning directory: {os.path.abspath(root_directory)}")

    structure = get_folder_structure(root_directory)
    save_to_json(structure)

    print("🚀 Folder structure successfully extracted!")
