
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

import os
import sys
import time
from datetime import datetime
import emoji

def get_file_size(filepath):
    """Gets the size of a file in bytes."""
    try:
        return os.path.getsize(filepath)
    except OSError:
        return 0

def convert_bytes(size):
    """Converts bytes to a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def find_largest_files(root_dir, num_files=5):  # Reduced to 5 for loop example
    """Finds the largest files within a directory."""
    largest_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            size = get_file_size(filepath)
            largest_files.append((filepath, size))

    largest_files.sort(key=lambda item: item[1], reverse=True)
    return largest_files[:num_files]

def recommend_compression(filepath):
    """Provides recommendations for decreasing file size."""
    name, ext = os.path.splitext(filepath.lower())
    recommendations = []
    if ext in ['.jpg', '.jpeg', '.png']:
        recommendations.append(emoji.emojize(":frame_with_picture:") + " Consider image optimization.")
    elif ext in ['.mp4', '.mov', '.avi', '.mkv']:
        recommendations.append(emoji.emojize(":clapper_board:") + " Explore video compression.")
    elif ext in ['.mp3', '.wav', '.aac']:
        recommendations.append(emoji.emojize(":musical_note:") + " Consider audio compression.")
    elif ext in ['.zip', '.tar.gz', '.dmg']:
        recommendations.append(emoji.emojize(":package:") + " Already compressed.")
    elif ext in ['.log', '.txt', '.csv']:
        recommendations.append(emoji.emojize(":memo:") + " Review content or compress.")
    elif ext in ['.pdf']:
        recommendations.append(emoji.emojize(":scroll:") + " Optimize PDF.")
    elif ext in ['.psd', '.ai', '.sketch']:
        recommendations.append(emoji.emojize(":artist_palette:") + " Optimize design files.")
    elif ext in ['.doc', '.docx', '.odt']:
        recommendations.append(emoji.emojize(":page_with_curl:") + " Review document content.")
    elif ext in ['.xls', '.xlsx', '.ods']:
        recommendations.append(emoji.emojize(":bar_chart:") + " Review spreadsheet data.")
    else:
        recommendations.append(emoji.emojize(":question_mark:") + " No specific recommendations.")
    return recommendations

def fdisk_recommendations():
    """Provides recommendations for fdisk usage on macOS."""
    recommendations = [
        emoji.emojize(":warning:") + " **Caution with `diskutil`.**",
        emoji.emojize(":information_source:") + " **Identify disks:** `diskutil list`.",
        emoji.emojize(":partition_globe:") + " **Partitioning:** `diskutil partitionDisk`.",
        emoji.emojize(":mount:") + " **Mounting/Unmounting:** `diskutil mount`/`unmount`.",
        emoji.emojize(":check_mark_button:") + " **File System:** Consider APFS.",
        emoji.emojize(":rescue_worker_helmet:") + " **Backup Before Changes!**",
        emoji.emojize(":magnifying_glass_tilted_left:") + " **Verify:** `diskutil verify*`.",
        emoji.emojize(":eject_button:") + " **Eject:** `diskutil eject`.",
        emoji.emojize(":books:") + " **`man diskutil` for details.**",
        emoji.emojize(":gear:") + " **Consider Disk Utility GUI.**",
    ]
    return recommendations

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(emoji.emojize(":file_folder:") + " Usage: python script_name.py <directory_to_scan>")
        sys.exit(1)

    target_directory = sys.argv[1]

    if not os.path.isdir(target_directory):
        print(emoji.emojize(":no_entry_sign:") + f" Error: Directory '{target_directory}' not found.")
        sys.exit(1)

    scan_interval = 3600  # Scan every hour (in seconds)

    while True:
        print(emoji.emojize(":repeat:") + f" Starting scan at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(emoji.emojize(":magnifying_glass:") + f" Scanning directory: {target_directory}...")
        print("-" * 40)

        largest_files = find_largest_files(target_directory)

        if largest_files:
            print(emoji.emojize(":trophy:") + " **Top Largest Files:**")
            for filepath, size in largest_files:
                print(f"- {emoji.emojize(':file:')} {filepath}: {convert_bytes(size)}")
                recommendations = recommend_compression(filepath)
                if recommendations:
                    print(emoji.emojize(":light_bulb:") + " Recommendations:")
                    for rec in recommendations:
                        print(f"  - {rec}")
                print("-" * 20)
        else:
            print(emoji.emojize(":check_mark_button:") + " No large files found in this directory.")

        print("\n" + emoji.emojize(":floppy_disk:") + " **Recommendations for `diskutil` (macOS `fdisk`):**")
        for rec in fdisk_recommendations():
            print(f"- {rec}")

        print("-" * 40)
        print(emoji.emojize(":hourglass_flowing_sand:") + f" Next scan will occur at: {(datetime.now() + timedelta(seconds=scan_interval)).strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(scan_interval)