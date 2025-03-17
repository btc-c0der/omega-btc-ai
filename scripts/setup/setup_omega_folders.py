import os

# ✅ Define the directory structure
folders = [
    "omega_ai",
    "omega_ai/logs",
    "omega_ai/data"
]

files = {
    "omega_ai/__init__.py": "",
    "omega_ai/omega_main.py": "# Main AI script\n",
    "omega_ai/mm_trap_detector.py": "# Microservice for MM Trap Detection\n",
    "omega_ai/db_manager.py": "# Handles database interactions\n",
    "omega_ai/config.py": "# API keys & global settings\n",
    "omega_ai/logs/.gitkeep": "",
    "omega_ai/data/.gitkeep": ""
}

# ✅ Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# ✅ Create files with default content
for file_path, content in files.items():
    with open(file_path, "w") as f:
        f.write(content)

print("✅ OMEGA BTC AI Folder Structure Created Successfully!")
