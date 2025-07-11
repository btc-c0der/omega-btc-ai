#!/usr/bin/env python3

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

"""
Display Organized Structure

This script finds and displays the most recently created BOOK_ORGANIZED directory
and its contents to help visualize the new organizational structure.
"""

import os
import sys
import datetime
import glob

def main():
    # First check main directory
    organized_dirs = glob.glob("BOOK_ORGANIZED_*")
    
    # If not found, check inside BOOK directory
    if not organized_dirs and os.path.isdir("BOOK"):
        book_dir = "BOOK"
        organized_dirs = [os.path.join(book_dir, d) for d in os.listdir(book_dir) 
                         if d.startswith("BOOK_ORGANIZED_") and 
                         os.path.isdir(os.path.join(book_dir, d))]
    
    if not organized_dirs:
        print("No BOOK_ORGANIZED directory found. Please run md_to_medium.py with --organize flag first.")
        return
    
    # Sort by creation time (newest first)
    organized_dirs.sort(key=lambda x: os.path.getctime(x), reverse=True)
    latest_dir = organized_dirs[0]
    
    # Get creation time
    creation_time = datetime.datetime.fromtimestamp(os.path.getctime(latest_dir))
    creation_str = creation_time.strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n{'='*80}")
    print(f"🌟 DIVINE ORGANIZATION STRUCTURE 🌟")
    print(f"{'='*80}")
    print(f"\nMost recent organization: {latest_dir} (created at {creation_str})\n")
    
    # Count files in each category
    categories = os.listdir(latest_dir)
    categories = [c for c in categories if os.path.isdir(os.path.join(latest_dir, c)) and not c.startswith('.')]
    
    print(f"{'='*80}")
    print(f"CATEGORY SUMMARY")
    print(f"{'='*80}")
    
    total_md = 0
    total_html = 0
    
    for category in sorted(categories):
        category_path = os.path.join(latest_dir, category)
        files = os.listdir(category_path)
        md_files = [f for f in files if f.lower().endswith('.md')]
        html_files = [f for f in files if f.lower().endswith('.html')]
        
        total_md += len(md_files)
        total_html += len(html_files)
        
        print(f"{category}: {len(md_files)} Markdown files, {len(html_files)} HTML files")
    
    print(f"\nTOTAL: {total_md} Markdown files, {total_html} HTML files")
    
    # Look for index.html
    index_path = os.path.join(latest_dir, "index.html")
    if os.path.exists(index_path):
        print(f"\n{'='*80}")
        print(f"INDEX FILE")
        print(f"{'='*80}")
        print(f"An index file was created at: {index_path}")
        print(f"Open this file in a web browser to navigate the organized manuscripts.")
    
    print(f"\n{'='*80}")
    print(f"SAMPLE CONTENT")
    print(f"{'='*80}")
    
    # Show a sample of files from each category (up to 5 per category)
    for category in sorted(categories):
        category_path = os.path.join(latest_dir, category)
        files = [f for f in os.listdir(category_path) if f.lower().endswith('.md')]
        
        if files:
            print(f"\n{category} (sample of {min(5, len(files))} files):")
            for f in sorted(files)[:5]:
                print(f"  - {f}")
    
    print(f"\n{'='*80}")
    print(f"✨ DIVINE HARMONY ACHIEVED ✨")
    print(f"{'='*80}\n")
    
    # Provide a command to open the index.html file
    if os.path.exists(index_path):
        if os.name == 'nt':  # Windows
            print(f"To view the organized manuscripts, run: start {index_path}")
        elif os.name == 'posix':  # macOS or Linux
            if 'darwin' in sys.platform:  # macOS
                print(f"To view the organized manuscripts, run: open {index_path}")
            else:  # Linux
                print(f"To view the organized manuscripts, run: xdg-open {index_path}")

if __name__ == "__main__":
    main() 