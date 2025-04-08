import os
import sys
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

def find_largest_files(root_dir, num_files=10):
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
        recommendations.append(emoji.emojize(":frame_with_picture:") + " Consider using image optimization tools (e.g., ImageOptim, TinyPNG) to reduce image file sizes without significant quality loss.")
    elif ext in ['.mp4', '.mov', '.avi', '.mkv']:
        recommendations.append(emoji.emojize(":clapper_board:") + " Explore video compression techniques or encoding at a lower bitrate using tools like HandBrake.")
    elif ext in ['.mp3', '.wav', '.aac']:
        recommendations.append(emoji.emojize(":musical_note:") + " Consider converting audio files to a compressed format (e.g., MP3 with a reasonable bitrate) or using lossless compression where appropriate.")
    elif ext in ['.zip', '.tar.gz', '.dmg']:
        recommendations.append(emoji.emojize(":package:") + " This file is already a compressed archive.")
    elif ext in ['.log', '.txt', '.csv']:
        recommendations.append(emoji.emojize(":memo:") + " For text-based files, consider reviewing the content for unnecessary verbosity or using compression tools if they are large.")
    elif ext in ['.pdf']:
        recommendations.append(emoji.emojize(":scroll:") + " Optimize PDFs using tools available in Adobe Acrobat or online PDF optimizers.")
    elif ext in ['.psd', '.ai', '.sketch']:
        recommendations.append(emoji.emojize(":artist_palette:") + " For design files, ensure layers are flattened where possible and unnecessary data is removed before saving.")
    elif ext in ['.doc', '.docx', '.odt']:
        recommendations.append(emoji.emojize(":page_with_curl:") + " Review document content and remove unnecessary formatting or embedded objects.")
    elif ext in ['.xls', '.xlsx', '.ods']:
        recommendations.append(emoji.emojize(":bar_chart:") + " Review spreadsheet data and remove unnecessary formulas or formatting.")
    else:
        recommendations.append(emoji.emojize(":question_mark:") + " No specific compression recommendations readily available for this file type.")
    return recommendations

def fdisk_recommendations():
    """Provides recommendations for fdisk usage on macOS."""
    recommendations = [
        emoji.emojize(":warning:") + " **Caution with `diskutil` (macOS equivalent of `fdisk`):** Incorrect usage can lead to permanent data loss. Always double-check commands before execution.",
        emoji.emojize(":information_source:") + " **Identify your disks:** Use `diskutil list` to clearly identify the disk identifiers (e.g., disk0, disk1).",
        emoji.emojize(":partition_globe:") + " **Partitioning:** Use `diskutil partitionDisk` to create, resize, or delete partitions. Understand the different partition schemes (e.g., GPT, APM).",
        emoji.emojize(":mount:") + " **Mounting/Unmounting:** Use `diskutil mount` and `diskutil unmount` to access and detach volumes.",
        emoji.emojize(":check_mark_button:") + " **File System Considerations:** Choose the appropriate file system (APFS is the default and recommended for macOS).",
        emoji.emojize(":rescue_worker_helmet:") + " **Backup Before Changes:** Always back up your important data before making any changes to disk partitions.",
        emoji.emojize(":magnifying_glass_tilted_left:") + " **Verify Operations:** Use `diskutil verifyDisk` and `diskutil verifyVolume` to check for errors after partitioning or other disk operations.",
        emoji.emojize(":eject_button:") + " **External Drives:** Use `diskutil eject` to safely remove external drives.",
        emoji.emojize(":books:") + " **Consult Documentation:** Refer to the `man diskutil` page for comprehensive information and options.",
        emoji.emojize(":gear:") + " **Graphical Tools:** For less experienced users, consider using Disk Utility (Applications > Utilities > Disk Utility) for a safer visual interface.",
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

    print("\n" + emoji.emojize(":floppy_disk:") + " **Recommendations for `fdisk`-like Operations on macOS (`diskutil`):**")
    for rec in fdisk_recommendations():
        print(f"- {rec}")

    print("\n" + emoji.emojize(":stopwatch:") + f" Scan completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")