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
OMEGA Script Organizer - Analyzes and organizes shell scripts by function
to create a more coherent structure within the codebase.
"""

import os
import sys
import shutil
import re
from pathlib import Path
import argparse
from datetime import datetime
from collections import defaultdict

# Define script categories and their keywords
SCRIPT_CATEGORIES = {
    'deployment': ['deploy', 'build', 'setup', 'install', 'docker', 'container', 'image', 'scaleway', 'cloud'],
    'services': ['service', 'start', 'stop', 'restart', 'redis', 'postgres', 'database', 'config'],
    'dashboards': ['dashboard', 'divine', 'ui', 'gui', 'interface', 'web', 'display', 'visualize', 'portal'],
    'monitors': ['monitor', 'quad', 'dual', 'position', 'track', 'trap', 'watch', 'btc_monitor', 'market'],
    'analytics': ['analyze', 'gamon', 'trinity', 'prometheus', 'matrix', 'predict', 'trader', 'trading', 'exit'],
    'debugging': ['debug', 'trace', 'log', 'diagnostic', 'troubleshoot', 'compile', 'fractal', 'mermaid', 'test'],
    'cli': ['cli', 'command', 'terminal', 'cmd', 'console']
}

# Special patterns for run_*.sh files
RUN_FILE_PATTERNS = {
    'monitors': [r'run_.*?_monitor', r'run_.*?_watcher', r'run_trap_position', r'run_btc_monitor', r'run_market_monitor'],
    'dashboards': [r'run_.*?_dashboard', r'run_divine_dashboard', r'run_.*?_portal', r'run-react-dashboard'],
    'analytics': [r'run_gamon_trinity', r'run_prometheus_matrix', r'run_.*?_trader', r'run_trap_aware'],
    'services': [r'run_redis']
}

def create_directory_structure(base_dir):
    """Create the directory structure for organized scripts"""
    script_dir = os.path.join(base_dir, "scripts")
    
    # Create main scripts directory
    if not os.path.exists(script_dir):
        os.mkdir(script_dir)
    
    # Create category subdirectories
    for category in SCRIPT_CATEGORIES.keys():
        category_dir = os.path.join(script_dir, category)
        if not os.path.exists(category_dir):
            os.mkdir(category_dir)
    
    return script_dir

def determine_script_category(script_path):
    """Analyze a shell script and determine its category based on content and name"""
    script_name = os.path.basename(script_path).lower()
    
    # Special handling for run_*.sh files
    if script_name.startswith('run_') or script_name.startswith('run-'):
        # Check specific run file patterns first
        for category, patterns in RUN_FILE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, script_name):
                    return category
    
    # First check the filename itself against keywords
    for category, keywords in SCRIPT_CATEGORIES.items():
        for keyword in keywords:
            if keyword in script_name:
                return category
    
    # If filename doesn't match, check the content
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            
            # Get the first comment block which often describes purpose
            comment_match = re.search(r'#.*?$(.*?)^[^#]', content, re.MULTILINE | re.DOTALL)
            if comment_match:
                comment_block = comment_match.group(1).lower()
            else:
                comment_block = ""
            
            # Check content against keywords with different weights
            category_scores = defaultdict(int)
            
            for category, keywords in SCRIPT_CATEGORIES.items():
                for keyword in keywords:
                    # Higher weight for keywords in the comment block
                    comment_matches = len(re.findall(r'\b' + keyword + r'\b', comment_block))
                    category_scores[category] += comment_matches * 3
                    
                    # Lower weight for keywords in the full content
                    content_matches = len(re.findall(r'\b' + keyword + r'\b', content))
                    category_scores[category] += content_matches
            
            # Get the category with the highest score
            if category_scores:
                return max(category_scores.items(), key=lambda x: x[1])[0]
    
    except Exception as e:
        print(f"Error analyzing {script_path}: {e}")
    
    # For run_*.sh files that don't match specific patterns, default to monitors
    if script_name.startswith('run_') or script_name.startswith('run-'):
        return 'monitors'
        
    # Default to debugging if no clear category
    return 'debugging'

def organize_scripts(base_dir, dry_run=False):
    """Organize shell scripts into the appropriate directories"""
    # Create the directory structure
    script_dir = create_directory_structure(base_dir)
    
    # Find all shell scripts in base directory
    shell_scripts = []
    for file in os.listdir(base_dir):
        if file.endswith('.sh') and os.path.isfile(os.path.join(base_dir, file)):
            shell_scripts.append(os.path.join(base_dir, file))
    
    # Track organization statistics
    stats = {category: 0 for category in SCRIPT_CATEGORIES.keys()}
    run_scripts_count = len([s for s in shell_scripts if os.path.basename(s).startswith(('run_', 'run-'))])
    
    print(f"\n{'=' * 80}")
    print(f"OMEGA SCRIPT ORGANIZER")
    print(f"{'=' * 80}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total shell scripts found: {len(shell_scripts)}")
    print(f"Run scripts (run_*.sh) found: {run_scripts_count}")
    print(f"{'=' * 80}\n")
    
    # Create special subdirectories for run scripts
    run_script_dirs = {}
    for category in SCRIPT_CATEGORIES.keys():
        run_dir = os.path.join(script_dir, category, "run_scripts")
        if not os.path.exists(run_dir):
            os.mkdir(run_dir)
        run_script_dirs[category] = run_dir
    
    # Organize each script
    for script_path in shell_scripts:
        script_name = os.path.basename(script_path)
        category = determine_script_category(script_path)
        stats[category] += 1
        
        # Determine destination based on whether it's a run script
        if script_name.startswith(('run_', 'run-')):
            dest_dir = run_script_dirs[category]
            is_run_script = True
        else:
            dest_dir = os.path.join(script_dir, category)
            is_run_script = False
            
        dest_path = os.path.join(dest_dir, script_name)
        
        print(f"Script: {script_name}")
        print(f"  Category: {category}")
        print(f"  Type: {'Run script' if is_run_script else 'Standard script'}")
        print(f"  Destination: {dest_path}")
        
        if not dry_run:
            # Copy script to category directory
            shutil.copy2(script_path, dest_path)
            
            # Create symbolic link in original location
            symlink_path = script_path + ".symlink"
            os.symlink(dest_path, symlink_path)
            
            # Replace original with symlink
            os.remove(script_path)
            os.rename(symlink_path, script_path)
            
            # Set executable permissions
            os.chmod(dest_path, 0o755)
        
        print()
    
    # Print statistics
    print(f"{'=' * 80}")
    print("Organization Statistics:")
    for category, count in stats.items():
        print(f"  {category.capitalize()}: {count} scripts")
    
    print(f"\nRun Scripts (run_*.sh) Distribution:")
    for category in SCRIPT_CATEGORIES.keys():
        category_run_scripts = [s for s in shell_scripts if os.path.basename(s).startswith(('run_', 'run-')) and determine_script_category(s) == category]
        print(f"  {category.capitalize()}: {len(category_run_scripts)} run scripts")
    
    print(f"{'=' * 80}")
    
    if dry_run:
        print("\nThis was a dry run. No files were moved.")
        print("Run without --dry-run to perform the actual organization.")
    else:
        print("\nScript organization complete!")
        print(f"All scripts have been organized into {script_dir}/")
        print("Original script locations now contain symbolic links to their organized versions.")
        print("\nRun scripts are now properly entangled in their respective category directories.")
    
def main():
    parser = argparse.ArgumentParser(description='Organize shell scripts by function')
    parser.add_argument('--dir', type=str, default='.', help='Base directory containing shell scripts')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    
    args = parser.parse_args()
    
    # Get absolute path of the directory
    base_dir = os.path.abspath(args.dir)
    
    # Organize scripts
    organize_scripts(base_dir, args.dry_run)

if __name__ == '__main__':
    main()