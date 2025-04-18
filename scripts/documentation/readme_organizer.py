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
OMEGA README Organizer - Analyzes and organizes README markdown files
scattered across the root directory into a coherent documentation structure.
"""

import os
import sys
import shutil
import re
import json
from pathlib import Path
import argparse
from datetime import datetime
from collections import defaultdict

# Define README categories and their keywords
README_CATEGORIES = {
    'deployment': ['deploy', 'cloud', 'kubernetes', 'k8s', 'aws', 'scaleway', 'docker'],
    'services': ['service', 'redis', 'database', 'config'],
    'interfaces': ['dashboard', 'portal', 'ui', 'gui', 'vnc'],
    'monitors': ['monitor', 'trap', 'watch', 'market'],
    'analytics': ['analytics', 'matrix', 'predict', 'trader', 'trading'],
    'testing': ['test', 'coverage', 'qa', 'quality'],
    'cli': ['cli', 'command', 'terminal'],
    'trading': ['trader', 'position', 'trade', 'market', 'exchange'],
    'divine': ['divine', 'book', 'omega', 'cosmic', 'quantum'],
    'security': ['security', 'quantum', 'encryption'],
    'development': ['development', 'code', 'programming', 'refactor']
}

def create_directory_structure(base_dir):
    """Create the directory structure for organized README files"""
    docs_dir = os.path.join(base_dir, "docs")
    
    # Create main documentation directory
    if not os.path.exists(docs_dir):
        os.mkdir(docs_dir)
    
    # Create category subdirectories for documentation
    docs_categories = ['deployment', 'services', 'interfaces', 'monitors', 
                      'analytics', 'testing', 'cli', 'trading', 'divine', 
                      'security', 'development', 'general']
    for category in docs_categories:
        category_dir = os.path.join(docs_dir, category)
        if not os.path.exists(category_dir):
            os.mkdir(category_dir)
    
    return docs_dir

def determine_readme_category(readme_path):
    """Analyze a README and determine its category based on content and name"""
    readme_name = os.path.basename(readme_path).lower()
    
    # Check specific keywords in the filename
    for category, keywords in README_CATEGORIES.items():
        for keyword in keywords:
            if keyword in readme_name:
                return category
    
    # If filename doesn't match, check the content
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            
            # Check content against keywords with different weights
            category_scores = defaultdict(int)
            
            for category, keywords in README_CATEGORIES.items():
                for keyword in keywords:
                    # Check for keywords in the content
                    content_matches = len(re.findall(r'\b' + keyword + r'\b', content))
                    category_scores[category] += content_matches
            
            # Get the category with the highest score
            if category_scores:
                return max(category_scores.items(), key=lambda x: x[1])[0]
    
    except Exception as e:
        print(f"Error analyzing README file {readme_path}: {e}")
    
    # Default to general if no clear category
    return 'general'

def process_file_move(source_path, dest_path, dest_dir, cleanup=True):
    """Process the move of a file to its destination with proper error handling
    
    Args:
        source_path: Original file path
        dest_path: Destination file path
        dest_dir: Destination directory path
        cleanup: If True, remove the original file and create a symlink; otherwise, just copy
    """
    try:
        # Create destination directory if it doesn't exist
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)
        
        # Copy file to category directory
        shutil.copy2(source_path, dest_path)
        
        # Create symbolic link if cleanup is requested
        if cleanup:
            # We need to use relative paths for symlinks to work properly
            rel_path = os.path.relpath(dest_path, os.path.dirname(source_path))
            os.remove(source_path)
            os.symlink(rel_path, source_path)
            print(f"  ✓ Created symlink: {os.path.basename(source_path)} → {rel_path}")
        else:
            print(f"  ✓ Copied to: {dest_path} (original left intact)")
            
    except Exception as e:
        print(f"Error processing {os.path.basename(source_path)}: {e}")

def verify_symlinks(base_dir, docs_dir, remove_after_verification=True):
    """Verify all symlinks are correctly pointing to their organized destinations
    
    Args:
        base_dir: The base directory containing README symlinks
        docs_dir: The docs directory containing organized README files
        remove_after_verification: If True, remove symlinks after verification
    """
    print(f"\n{'=' * 80}")
    print("VERIFYING README SYMLINKS")
    print(f"{'=' * 80}")
    
    all_correct = True
    readme_files = []
    
    # Find README files in the root directory
    for file in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file)
        if os.path.isfile(file_path) and file.lower().endswith('.md') and 'readme' in file.lower():
            readme_files.append(file_path)
    
    # Check README symlinks
    for readme_path in readme_files:
        if not os.path.islink(readme_path):
            print(f"❌ ERROR: {readme_path} is not a symlink")
            all_correct = False
            continue
            
        # Get the target of the symlink
        target_path = os.readlink(readme_path)
        absolute_target = os.path.normpath(os.path.join(os.path.dirname(readme_path), target_path))
        
        # Check if the target exists
        if not os.path.exists(absolute_target):
            print(f"❌ ERROR: Symlink target does not exist: {absolute_target}")
            all_correct = False
            continue
            
        # Check if the target is under the docs directory
        if not absolute_target.startswith(docs_dir):
            print(f"❌ ERROR: Symlink target is not in docs directory: {absolute_target}")
            all_correct = False
            continue
            
        # Check if the target has the same content as the original
        try:
            with open(absolute_target, 'r', encoding='utf-8') as f:
                target_content = f.read()
            
            print(f"✓ Verified: {os.path.basename(readme_path)} → {os.path.relpath(absolute_target, base_dir)}")
            
            # Remove symlink after verification if requested
            if remove_after_verification:
                os.remove(readme_path)
                print(f"  ✓ Removed symlink: {os.path.basename(readme_path)}")
            
        except Exception as e:
            print(f"❌ ERROR: Could not verify {readme_path} content: {e}")
            all_correct = False
    
    if all_correct:
        print(f"\n✅ All README symlinks verified successfully!")
        if remove_after_verification:
            print(f"✅ All symlinks have been removed after verification!")
    else:
        print(f"\n⚠️ Some README symlinks could not be verified. Please check the errors above.")
    
    return all_correct

def organize_readme_files(base_dir, dry_run=False, verify_only=False, cleanup=True):
    """Organize README files into the appropriate directories
    
    Args:
        base_dir: The base directory containing README files
        dry_run: If True, only show what would be done without making changes
        verify_only: If True, only verify existing symlinks without organizing
        cleanup: If True, remove original files and replace with symlinks; otherwise just copy
    """
    # Create the docs directory structure
    docs_dir = create_directory_structure(base_dir)
    
    # If verify_only, just check existing symlinks
    if verify_only:
        return verify_symlinks(base_dir, docs_dir)
    
    # Find all README files in the base directory
    readme_files = []
    
    for file in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file)
        if os.path.isfile(file_path) and file.lower().endswith('.md') and 'readme' in file.lower():
            readme_files.append(file_path)
    
    # Track organization statistics
    readme_stats = {category: 0 for category in README_CATEGORIES.keys()}
    readme_stats['general'] = 0
    
    print(f"\n{'=' * 80}")
    print(f"OMEGA README ORGANIZER")
    print(f"{'=' * 80}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total README files found: {len(readme_files)}")
    print(f"Mode: {'Dry Run (no changes)' if dry_run else 'Actual Run'}")
    print(f"Cleanup: {'Yes (create symlinks)' if cleanup else 'No (keep originals)'}")
    
    # Organize each README file
    print("\nORGANIZING README FILES:")
    print(f"{'=' * 80}")
    
    for readme_path in readme_files:
        readme_name = os.path.basename(readme_path)
        category = determine_readme_category(readme_path)
        readme_stats[category] += 1
        
        dest_dir = os.path.join(docs_dir, category)
        dest_path = os.path.join(dest_dir, readme_name)
        
        # Ensure the source and destination are not the same file
        if os.path.abspath(readme_path) == os.path.abspath(dest_path):
            print(f"Warning: Source and destination are the same for {readme_name}. Skipping.")
            continue
        
        print(f"README file: {readme_name}")
        print(f"  Category: {category}")
        print(f"  Destination: {dest_path}")
        
        if not dry_run:
            process_file_move(readme_path, dest_path, dest_dir, cleanup)
        
        print()
    
    # Print statistics
    print(f"{'=' * 80}")
    print("Organization Statistics:")
    
    print("\nREADME Categories:")
    for category, count in readme_stats.items():
        if count > 0:
            print(f"  {category.capitalize()}: {count} README files")
    
    print(f"{'=' * 80}")
    
    if dry_run:
        print("\nThis was a dry run. No files were moved.")
        print("Run without --dry-run to perform the actual organization.")
    else:
        print("\nREADME file organization complete!")
        print(f"All README files have been organized into {docs_dir}/")
        if cleanup:
            print("Original file locations now contain symbolic links to their organized versions.")
            # Verify the symlinks
            verify_symlinks(base_dir, docs_dir)
        else:
            print("Original files were kept intact (no symlinks created).")

def create_readme_index(base_dir, dry_run=False):
    """Create an index file of all README files"""
    docs_dir = os.path.join(base_dir, "docs")
    
    if not os.path.exists(docs_dir):
        print("Docs directory not found. Please organize README files first.")
        return False
    
    # Dictionary to hold categorized READMEs
    readme_index = {}
    
    # Walk through the docs directory
    for root, dirs, files in os.walk(docs_dir):
        category = os.path.basename(root)
        if category not in readme_index and category != "docs":
            readme_index[category] = []
        
        for file in files:
            if file.lower().endswith('.md') and 'readme' in file.lower():
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, base_dir)
                
                # Extract title from file content
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Try to extract the title from a markdown heading
                        title_match = re.search(r'^#\s+(.*?)$', content, re.MULTILINE)
                        if title_match:
                            title = title_match.group(1).strip()
                        else:
                            # Use filename as title if no heading found
                            title = os.path.splitext(file)[0].replace('_', ' ').title()
                            
                        # Add to the appropriate category
                        if category != "docs":
                            readme_index[category].append({"title": title, "path": rel_path, "filename": file})
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    # Create the index file content
    index_content = f"""# OMEGA Documentation Index

> *"Order is the shape upon which beauty depends."* — Pearl Buck

## Overview

This document serves as a master index for all README files in the OMEGA BTC AI project. 
The documentation is organized into categories to help you find the information you need more efficiently.

Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Categories

"""

    # Add each category
    for category, readmes in sorted(readme_index.items()):
        if readmes:
            index_content += f"### {category.capitalize()}\n\n"
            for readme in sorted(readmes, key=lambda x: x["title"]):
                index_content += f"- [{readme['title']}]({readme['path']})\n"
            index_content += "\n"
    
    # Add footer
    index_content += """
## Usage Tips

- Click on any document title to navigate to that README
- All documentation is maintained in markdown format
- The documentation structure mirrors the organization of the project
- For the most current information, always refer to this index

🌸 WE BLOOM NOW AS ONE 🌸
"""
    
    index_path = os.path.join(base_dir, "DOCUMENTATION_INDEX.md")
    
    if dry_run:
        print("\nWould create documentation index at:")
        print(index_path)
        print("\nSample content:")
        print("-------------")
        print(index_content[:500] + "...")  # Show just a preview
    else:
        try:
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)
            print(f"\n✅ Documentation index created at: {index_path}")
        except Exception as e:
            print(f"Error creating index file: {e}")
            return False
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description='Organize README markdown files into a coherent documentation structure'
    )
    parser.add_argument('--dir', type=str, default='.', help='Base directory containing README files')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--verify', action='store_true', help='Verify existing symlinks are correctly set up')
    parser.add_argument('--keep-symlinks', action='store_true', help='Keep symlinks after verification (default is to remove them)')
    parser.add_argument('--create-index', action='store_true', help='Create a documentation index file')
    parser.add_argument('--no-cleanup', action='store_true', help='Keep original files instead of replacing with symlinks')
    
    args = parser.parse_args()
    
    # Get absolute path of the directory
    base_dir = os.path.abspath(args.dir)
    
    # Process based on arguments
    if args.verify:
        # Pass the opposite of keep-symlinks to remove_after_verification
        docs_dir = os.path.join(base_dir, "docs")
        verify_symlinks(base_dir, docs_dir, not args.keep_symlinks)
    elif args.create_index:
        create_readme_index(base_dir, args.dry_run)
    else:
        organize_readme_files(base_dir, args.dry_run, cleanup=(not args.no_cleanup))
        if not args.dry_run:  # Also create the index if we're actually organizing
            create_readme_index(base_dir, args.dry_run)

if __name__ == '__main__':
    main()