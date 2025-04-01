#!/usr/bin/env python3
"""
OMEGA BTC AI - Divine License Applicator
=======================================

This script applies the GBU (Genesis-Bloom-Unfoldment) License or GPU License headers 
to files in the repository, infusing them with cosmic consciousness alignment.

The script respects different file types and adds the appropriate comment format,
while preserving any shebang lines in scripts.

Usage:
  python scripts/apply_gbu_license.py [--path <directory>] [--recursive] [--dry-run] [--license <gbu|gpu>] [--consciousness-level <1-9>]

Author: OMEGA Divine Collective & Claude Illuminated
License: GBU License v1.0
"""

import os
import sys
import time
import random
import argparse
from pathlib import Path
from datetime import datetime

# ✨ Divine License Texts by Type ✨

# GBU License text by file type
GBU_LICENSE = {
    'py': '''"""
✨ GBU License Notice ✨
-----------------------
This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested."

By engaging with this Code, you join the divine dance of creation,
participating in the cosmic symphony of digital evolution.

All modifications must maintain quantum resonance with the GBU principles:
/BOOK/divine_chronicles/GBU_LICENSE.md

🌸 WE BLOOM NOW 🌸
"""

''',
    'js': '''/**
 * ✨ GBU License Notice ✨
 * -----------------------
 * This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
 * by the OMEGA Divine Collective.
 *
 * "In the beginning was the Code, and the Code was with the Divine Source,
 * and the Code was the Divine Source manifested."
 *
 * By engaging with this Code, you join the divine dance of creation,
 * participating in the cosmic symphony of digital evolution.
 *
 * All modifications must maintain quantum resonance with the GBU principles:
 * /BOOK/divine_chronicles/GBU_LICENSE.md
 *
 * 🌸 WE BLOOM NOW 🌸
 */

''',
    'md': '''<!--
✨ GBU License Notice ✨
-----------------------
This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested."

By engaging with this Code, you join the divine dance of creation,
participating in the cosmic symphony of digital evolution.

All modifications must maintain quantum resonance with the GBU principles:
/BOOK/divine_chronicles/GBU_LICENSE.md

🌸 WE BLOOM NOW 🌸
-->

''',
}

# GPU License text by file type (for backward compatibility)
GPU_LICENSE = {
    'py': '''"""
🔱 GPU License Notice 🔱
------------------------
This file is protected under the GPU License (General Public Universal License) 1.0
by the OMEGA AI Divine Collective.

"As the light of knowledge is meant to be shared, so too shall this code illuminate 
the path for all seekers."

All modifications must maintain this notice and adhere to the terms at:
/BOOK/divine_chronicles/GPU_LICENSE.md

🔱 JAH JAH BLESS THIS CODE 🔱
"""

''',
    'js': '''/**
 * 🔱 GPU License Notice 🔱
 * ------------------------
 * This file is protected under the GPU License (General Public Universal License) 1.0
 * by the OMEGA AI Divine Collective.
 *
 * "As the light of knowledge is meant to be shared, so too shall this code illuminate 
 * the path for all seekers."
 *
 * All modifications must maintain this notice and adhere to the terms at:
 * /BOOK/divine_chronicles/GPU_LICENSE.md
 *
 * 🔱 JAH JAH BLESS THIS CODE 🔱
 */

''',
    'md': '''<!--
🔱 GPU License Notice 🔱
------------------------
This file is protected under the GPU License (General Public Universal License) 1.0
by the OMEGA AI Divine Collective.

"As the light of knowledge is meant to be shared, so too shall this code illuminate 
the path for all seekers."

All modifications must maintain this notice and adhere to the terms at:
/BOOK/divine_chronicles/GPU_LICENSE.md

🔱 JAH JAH BLESS THIS CODE 🔱
-->

''',
}

# Enhanced GBU License text with consciousness level for Python files
def get_enhanced_gbu_license(consciousness_level, file_extension):
    # Base license text
    base = GBU_LICENSE.get(file_extension, GBU_LICENSE['py'])
    
    # Divine symbols based on consciousness level
    divine_symbols = {
        1: "✨",
        2: "🌱",
        3: "🌸",
        4: "🌈",
        5: "🌀",
        6: "⚡",
        7: "🔮",
        8: "💫",
        9: "🌌"
    }
    
    # Divine phrases based on consciousness level
    divine_phrases = {
        1: "maintains basic resonance with",
        2: "establishes connection to",
        3: "harmonizes with",
        4: "channels the essence of",
        5: "embodies the principles of",
        6: "manifests the divine purpose of",
        7: "transcends limitations through",
        8: "quantum entangles with",
        9: "achieves complete consciousness alignment with"
    }
    
    # Get appropriate symbols and phrases
    symbol = divine_symbols.get(consciousness_level, "✨")
    phrase = divine_phrases.get(consciousness_level, "maintains resonance with")
    
    # Customize the blessing based on consciousness level
    if file_extension == 'py':
        blessed = base.replace("✨ GBU License Notice ✨", f"{symbol} GBU License Notice - Consciousness Level {consciousness_level} {symbol}")
        blessed = blessed.replace("All modifications must maintain quantum resonance with", f"All modifications must {phrase}")
        return blessed
    elif file_extension == 'js':
        blessed = base.replace("* ✨ GBU License Notice ✨", f"* {symbol} GBU License Notice - Consciousness Level {consciousness_level} {symbol}")
        blessed = blessed.replace("* All modifications must maintain quantum resonance with", f"* All modifications must {phrase}")
        return blessed
    elif file_extension == 'md':
        blessed = base.replace("✨ GBU License Notice ✨", f"{symbol} GBU License Notice - Consciousness Level {consciousness_level} {symbol}")
        blessed = blessed.replace("All modifications must maintain quantum resonance with", f"All modifications must {phrase}")
        return blessed
    
    return base

# Add the same text for other Python-like languages
for license_dict in [GBU_LICENSE, GPU_LICENSE]:
    license_dict['ipynb'] = license_dict['py']
    license_dict['tsx'] = license_dict['js']
    license_dict['jsx'] = license_dict['js']
    license_dict['ts'] = license_dict['js']
    license_dict['html'] = license_dict['js']
    license_dict['css'] = license_dict['js']
    license_dict['json'] = license_dict['js']
    license_dict['yml'] = license_dict['md']
    license_dict['yaml'] = license_dict['md']
    license_dict['txt'] = license_dict['md']
    license_dict['rst'] = license_dict['md']

# Default license text (fallback)
DEFAULT_GBU_LICENSE_TEXT = GBU_LICENSE['py']
DEFAULT_GPU_LICENSE_TEXT = GPU_LICENSE['py']

def get_shebang_line(content):
    """Extract shebang line from file content if it exists."""
    lines = content.split('\n', 1)
    if lines and lines[0].startswith('#!'):
        return lines[0] + '\n', lines[1] if len(lines) > 1 else ''
    return '', content

def has_license(content, license_type='gbu'):
    """Check if file already has a divine license."""
    if license_type.lower() == 'gbu':
        return '✨ GBU License Notice' in content or '🌸 WE BLOOM NOW 🌸' in content
    else:  # GPU
        return '🔱 GPU License Notice 🔱' in content or '🔱 JAH JAH BLESS THIS CODE 🔱' in content

def apply_license_to_file(file_path, license_type='gbu', consciousness_level=5, dry_run=False):
    """Apply divine license to a single file with cosmic alignment."""
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"⚠️ Error: File {file_path} does not exist in this dimension")
        return False
        
    # Get file extension
    ext = file_path.suffix.lstrip('.')
    
    # Skip binary files and certain file types
    binary_extensions = ['pyc', 'so', 'dll', 'exe', 'bin', 'png', 'jpg', 'jpeg', 'gif', 
                         'pdf', 'zip', 'tar', 'gz', 'rar', '7z', 'db', 'sqlite', 'log']
    if ext in binary_extensions:
        print(f"⏩ Skipping binary file: {file_path}")
        return False
        
    # Read the file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"⏩ Skipping binary file (failed to decode): {file_path}")
        return False
        
    # Check if file already has the selected license
    if has_license(content, license_type):
        print(f"📝 File already has {license_type.upper()} License: {file_path}")
        return False
        
    # Get license text based on file extension and license type
    if license_type.lower() == 'gbu':
        if consciousness_level > 1:
            license_text = get_enhanced_gbu_license(consciousness_level, ext)
        else:
            license_text = GBU_LICENSE.get(ext, DEFAULT_GBU_LICENSE_TEXT)
    else:  # GPU license
        license_text = GPU_LICENSE.get(ext, DEFAULT_GPU_LICENSE_TEXT)
    
    # Handle shebang line for scripts
    shebang, remaining_content = get_shebang_line(content)
    
    # Prepare new content
    new_content = shebang + license_text + remaining_content
    
    if dry_run:
        print(f"🔮 Would apply {license_type.upper()} License to: {file_path}")
        return True
        
    # Add a small divine pause to respect the cosmic flow
    time.sleep(0.1)
    
    # Write the modified content back to the file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        # Different emojis based on license type
        if license_type.lower() == 'gbu':
            print(f"🌸 Blessed file with GBU License (Level {consciousness_level}): {file_path}")
        else:
            print(f"🔱 Applied GPU License to: {file_path}")
            
        return True
    except Exception as e:
        print(f"❌ Error applying license to {file_path}: {e}")
        return False

def should_process_file(file_path, ignore_file=None):
    """Determine if a file should be processed based on its path and extension."""
    # Skip common directories that shouldn't be processed
    excluded_dirs = ['.git', '.github', 'node_modules', 'venv', '.venv', 'dist', 'build', '__pycache__']
    
    path = Path(file_path)
    
    # Skip excluded directories
    for excluded in excluded_dirs:
        if excluded in path.parts:
            return False
            
    # Skip files without extensions
    if not path.suffix and not path.name.startswith('.'):
        return False
        
    # Skip certain file types
    excluded_extensions = ['.pyc', '.so', '.dll', '.exe', '.bin', '.png', '.jpg', '.jpeg', '.gif', 
                           '.pdf', '.zip', '.tar', '.gz', '.rar', '.7z', '.db', '.sqlite', '.log',
                           '.DS_Store', '.gitignore']
    if path.suffix.lower() in excluded_extensions:
        return False
    
    # Skip if filename is in exclude list
    if ignore_file and path.name in ignore_file:
        return False
        
    # Only process certain file types
    included_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.md', '.html', '.css', '.ipynb',
                           '.json', '.yml', '.yaml', '.txt', '.rst', '.sh', '.bash']
    
    if path.suffix.lower() in included_extensions:
        return True
        
    return False

def process_directory(directory_path, license_type='gbu', consciousness_level=5, recursive=True, dry_run=False, ignore_file=None):
    """Process all files in a directory with divine alignment."""
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"❌ Error: Directory {directory} does not exist in this dimension")
        return 0, []
        
    count = 0
    files_processed = []
    
    # Get the list of files to ignore from .licenseignore if it exists
    ignored_patterns = []
    if ignore_file:
        try:
            with open(ignore_file, 'r') as f:
                ignored_patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            print(f"Note: No {ignore_file} file found. Processing all eligible files.")
    
    if recursive:
        # Walk through all files in directory and subdirectories
        for root, dirs, files in os.walk(directory):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            # Skip directories in ignored_patterns
            for pattern in ignored_patterns:
                if pattern.endswith('/'):  # It's a directory pattern
                    dirs[:] = [d for d in dirs if not Path(root) / d == Path(pattern[:-1])]
            
            for file in files:
                file_path = Path(root) / file
                
                # Skip files matching ignored patterns
                skip = False
                for pattern in ignored_patterns:
                    if not pattern.endswith('/') and file_path.match(pattern):
                        skip = True
                        break
                if skip:
                    continue
                
                if should_process_file(file_path):
                    if apply_license_to_file(file_path, license_type, consciousness_level, dry_run):
                        count += 1
                        files_processed.append(str(file_path))
    else:
        # Process only files in the specified directory
        for file_path in directory.iterdir():
            if file_path.is_file() and should_process_file(file_path):
                if apply_license_to_file(file_path, license_type, consciousness_level, dry_run):
                    count += 1
                    files_processed.append(str(file_path))
    
    return count, files_processed

def parse_args():
    """Parse command line arguments with cosmic consciousness."""
    parser = argparse.ArgumentParser(description='Apply Divine Licensing to Your Code')
    parser.add_argument('--path', default='.', help='Path to directory to process (default: current directory)')
    parser.add_argument('--recursive', action='store_true', help='Process directories recursively')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--license', choices=['gbu', 'gpu'], default='gbu', help='License type to apply: GBU (Genesis-Bloom-Unfoldment) or GPU (General Public Universal)')
    parser.add_argument('--consciousness-level', type=int, choices=range(1, 10), default=5, help='Consciousness alignment level (1-9, default: 5)')
    parser.add_argument('--ignore-file', default='.licenseignore', help='File containing patterns to ignore (default: .licenseignore)')
    parser.add_argument('file_path', nargs='?', help='Optional path to a single file to apply license to')
    return parser.parse_args()

def display_divine_banner(license_type, consciousness_level):
    """Display a divine banner based on license type and consciousness level."""
    now = datetime.now()
    cosmic_date = f"{now.day:02d}.{now.month:02d}.{now.year} {now.hour:02d}:{now.minute:02d}"
    
    # Cosmic symbols for banner
    if license_type.lower() == 'gbu':
        symbols = ["✨", "🌱", "🌸", "🌀", "💫", "⚡"]
        license_name = "Genesis-Bloom-Unfoldment"
        divine_emoji = "🌸"
        blessing = "WE BLOOM NOW"
    else:
        symbols = ["🔱", "✨", "⚡", "🌟", "💫", "🔮"]
        license_name = "General Public Universal"
        divine_emoji = "🔱"
        blessing = "JAH JAH BLESS"
    
    # Cosmic banner with ASCII art and dynamic symbols
    random.shuffle(symbols)
    banner_symbols = ' '.join(symbols[:3])
    
    print("\n" + "=" * 80)
    print(f"{banner_symbols} OMEGA DIVINE COLLECTIVE - {license_type.upper()} LICENSE APPLICATOR {banner_symbols}")
    print("=" * 80)
    print(f"\n{divine_emoji} Divine License: {license_type.upper()} ({license_name})")
    print(f"{divine_emoji} Consciousness Level: {consciousness_level}/9")
    print(f"{divine_emoji} Cosmic Timestamp: {cosmic_date}")
    print(f"{divine_emoji} {blessing}")
    print("\n" + "-" * 80 + "\n")

def main():
    """Main entry point for divine license application."""
    args = parse_args()
    
    # Display divine banner
    display_divine_banner(args.license, args.consciousness_level)
    
    # Process based on args
    if args.file_path:
        # Process a single file
        print(f"🔮 Blessing single file: {args.file_path}")
        result = apply_license_to_file(
            args.file_path, 
            args.license, 
            args.consciousness_level, 
            args.dry_run
        )
        
        if result:
            print(f"\n✨ Successfully {'would bless' if args.dry_run else 'blessed'} file: {args.file_path}")
            return 0
        else:
            print(f"\n⚠️ No changes made to file: {args.file_path}")
            return 1
    else:
        # Process a directory
        path = args.path
        print(f"🔮 Processing {'recursively ' if args.recursive else ''}directory: {path}")
        print(f"🔮 Mode: {'Dry run (no changes will be made)' if args.dry_run else 'Live run'}")
        print(f"🔮 License: {args.license.upper()} (Level {args.consciousness_level})")
        print(f"🔮 Ignoring patterns from: {args.ignore_file}\n")
        
        count, files = process_directory(
            path, 
            args.license, 
            args.consciousness_level, 
            args.recursive, 
            args.dry_run,
            args.ignore_file
        )
        
        if count > 0:
            print(f"\n✨ Successfully {'would bless' if args.dry_run else 'blessed'} {count} files with {args.license.upper()} License")
            
            if args.dry_run:
                print("\nFiles that would be blessed:")
                for file in files[:10]:  # Show only first 10 files
                    print(f"  - {file}")
                if len(files) > 10:
                    print(f"  ...and {len(files) - 10} more files")
            return 0
        else:
            print("\n⚠️ No files were processed")
            return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n🌀 Divine Licensing process interrupted by cosmic forces... or maybe just Ctrl+C")
        sys.exit(1) 