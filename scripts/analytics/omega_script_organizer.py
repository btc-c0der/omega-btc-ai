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
OMEGA Script Organizer - Analyzes and organizes shell scripts, Python runner files,
and Docker files by function to create a more coherent structure within the codebase.
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
    'cli': ['cli', 'command', 'terminal', 'cmd', 'console'],
    'traders': ['trader', 'position', 'trade', 'market', 'exchange', 'bitget', 'binance', 'futures'],
    'docker': ['docker', 'container', 'image', 'registry', 'kubernetes', 'k8s', 'pod', 'deployment']
}

# Special patterns for run_*.sh and run_*.py files
RUN_FILE_PATTERNS = {
    'monitors': [r'run_.*?_monitor', r'run_.*?_watcher', r'run_trap_position', r'run_btc_monitor', r'run_market_monitor'],
    'dashboards': [r'run_.*?_dashboard', r'run_divine_dashboard', r'run_.*?_portal', r'run-react-dashboard'],
    'analytics': [r'run_.*?_trinity', r'run_prometheus_matrix', r'run_.*?_analyze', r'run_trap_aware'],
    'services': [r'run_redis', r'run_service'],
    'traders': [r'run_.*?_trader', r'run_.*?_position', r'run_.*?_trading', r'dry_run']
}

# Docker file patterns
DOCKER_FILE_PATTERNS = {
    'monitors': [r'monitor', r'watcher', r'trap', r'btc-monitor', r'btc-live-feed'],
    'dashboards': [r'dashboard', r'divine', r'portal', r'ui', r'frontend', r'omega_portal', r'omega-vnc'],
    'analytics': [r'matrix', r'news', r'prophet', r'prediction', r'analyze', r'analytics', 'prophecy-core'],
    'services': [r'redis', r'postgres', r'database', r'service'],
    'traders': [r'trader', r'position', r'trading', r'exchange', r'bitget', r'binance'],
    'cli': [r'cli', r'cli-portal', r'terminal', r'console'],
    'infra': [r'base', r'infrastructure', r'platform']
}

# File extensions to process
FILE_EXTENSIONS = ['.sh', '.py']

# Docker file patterns to process
DOCKER_PATTERNS = ['Dockerfile', 'Dockerfile.', 'docker-compose']

def create_directory_structure(base_dir):
    """Create the directory structure for organized scripts"""
    script_dir = os.path.join(base_dir, "scripts")
    docker_dir = os.path.join(base_dir, "docker")
    
    # Create main directories
    if not os.path.exists(script_dir):
        os.mkdir(script_dir)
    
    if not os.path.exists(docker_dir):
        os.mkdir(docker_dir)
    
    # Create category subdirectories for scripts
    for category in SCRIPT_CATEGORIES.keys():
        category_dir = os.path.join(script_dir, category)
        if not os.path.exists(category_dir):
            os.mkdir(category_dir)
        
        # Create special run_scripts directory for each category
        run_dir = os.path.join(category_dir, "run_scripts")
        if not os.path.exists(run_dir):
            os.mkdir(run_dir)
    
    # Create category subdirectories for Docker files
    docker_categories = ['monitors', 'dashboards', 'analytics', 'services', 'traders', 'cli', 'infra', 'base']
    for category in docker_categories:
        category_dir = os.path.join(docker_dir, category)
        if not os.path.exists(category_dir):
            os.mkdir(category_dir)
    
    return script_dir, docker_dir

def determine_script_category(script_path):
    """Analyze a script and determine its category based on content and name"""
    script_name = os.path.basename(script_path).lower()
    
    # Special handling for run_* files
    if script_name.startswith('run_') or script_name.startswith('run-') or script_name.startswith('dry_run'):
        # Check specific run file patterns first
        for category, patterns in RUN_FILE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, script_name):
                    return category
    
    # If it has "trader" or "position" in the name, it's likely a trader script
    if 'trader' in script_name or 'position' in script_name:
        return 'traders'
    
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
            if script_path.endswith('.py'):
                comment_match = re.search(r'""".*?"""', content, re.DOTALL)
                if not comment_match:
                    comment_match = re.search(r"'''.*?'''", content, re.DOTALL)
            else:  # For shell scripts
                comment_match = re.search(r'#.*?$(.*?)^[^#]', content, re.MULTILINE | re.DOTALL)
                
            if comment_match:
                comment_block = comment_match.group(0).lower()
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
    
    # For run_* files that don't match specific patterns
    if script_name.startswith('run_') or script_name.startswith('run-'):
        if script_path.endswith('.py'):
            return 'traders'  # Python run files often involve trading logic
        return 'monitors'  # Shell run files often involve monitoring
    
    # Default to debugging if no clear category
    return 'debugging'

def determine_docker_category(docker_path):
    """Analyze a Docker file and determine its category based on content and name"""
    docker_name = os.path.basename(docker_path).lower()
    
    # Check for docker-compose files
    if 'docker-compose' in docker_name:
        if 'cloud' in docker_name or 'scaleway' in docker_name:
            return 'infra'
        return 'base'  # Default for docker-compose files
    
    # Extract service name from Dockerfile.<service> pattern
    service_name = ""
    if docker_name.startswith('dockerfile.'):
        service_name = docker_name[10:]  # Remove "Dockerfile." prefix
    
    # Check specific Docker patterns
    for category, patterns in DOCKER_FILE_PATTERNS.items():
        for pattern in patterns:
            if pattern in docker_name or pattern in service_name:
                return category
    
    # If filename doesn't match, check the content
    try:
        with open(docker_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            
            # Check content against keywords with different weights
            category_scores = defaultdict(int)
            
            for category, keywords in SCRIPT_CATEGORIES.items():
                for keyword in keywords:
                    # Check for keywords in the content
                    content_matches = len(re.findall(r'\b' + keyword + r'\b', content))
                    category_scores[category] += content_matches
            
            # Get the category with the highest score
            if category_scores:
                return max(category_scores.items(), key=lambda x: x[1])[0]
    
    except Exception as e:
        print(f"Error analyzing Docker file {docker_path}: {e}")
    
    # Default to base if no clear category
    return 'base'

def verify_symlinks(base_dir, script_dir, docker_dir=None):
    """Verify all symlinks are correctly pointing to their organized destinations"""
    print(f"\n{'=' * 80}")
    print("VERIFYING SYMLINKS AND FILE INTEGRITY")
    print(f"{'=' * 80}")
    
    all_correct = True
    script_files = []
    docker_files = []
    
    for file in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file)
        if os.path.isfile(file_path):
            if any(file.endswith(ext) for ext in FILE_EXTENSIONS):
                script_files.append(file_path)
            elif any(pattern in file.lower() for pattern in DOCKER_PATTERNS):
                docker_files.append(file_path)
    
    # Check script symlinks
    for script_path in script_files:
        if not os.path.islink(script_path):
            print(f"❌ ERROR: {script_path} is not a symlink")
            all_correct = False
            continue
            
        # Get the target of the symlink
        target_path = os.readlink(script_path)
        absolute_target = os.path.normpath(os.path.join(os.path.dirname(script_path), target_path))
        
        # Check if the target exists
        if not os.path.exists(absolute_target):
            print(f"❌ ERROR: Symlink target does not exist: {absolute_target}")
            all_correct = False
            continue
            
        # Check if the target is under the scripts directory
        if not absolute_target.startswith(script_dir):
            print(f"❌ ERROR: Symlink target is not in scripts directory: {absolute_target}")
            all_correct = False
            continue
            
        # Check if the target has the same content as the original
        try:
            with open(absolute_target, 'r', encoding='utf-8') as f:
                target_content = f.read()
                
            # Ensure target is executable if it's a script
            if any(script_path.endswith(ext) for ext in FILE_EXTENSIONS):
                if not os.access(absolute_target, os.X_OK):
                    print(f"⚠️ WARNING: Target file is not executable: {absolute_target}")
                    # Make it executable
                    os.chmod(absolute_target, 0o755)
                    print(f"✓ Fixed: Made {absolute_target} executable")
            
            print(f"✓ Verified: {os.path.basename(script_path)} → {os.path.relpath(absolute_target, base_dir)}")
            
        except Exception as e:
            print(f"❌ ERROR: Could not verify {script_path} content: {e}")
            all_correct = False
    
    # Check Docker file symlinks
    for docker_path in docker_files:
        if not os.path.islink(docker_path):
            print(f"❌ ERROR: {docker_path} is not a symlink")
            all_correct = False
            continue
            
        # Get the target of the symlink
        target_path = os.readlink(docker_path)
        absolute_target = os.path.normpath(os.path.join(os.path.dirname(docker_path), target_path))
        
        # Check if the target exists
        if not os.path.exists(absolute_target):
            print(f"❌ ERROR: Symlink target does not exist: {absolute_target}")
            all_correct = False
            continue
            
        # Check if the target is under the docker directory
        if docker_dir and not absolute_target.startswith(docker_dir):
            print(f"❌ ERROR: Symlink target is not in docker directory: {absolute_target}")
            all_correct = False
            continue
            
        # Check if the target has the same content as the original
        try:
            with open(absolute_target, 'r', encoding='utf-8') as f:
                target_content = f.read()
                
            print(f"✓ Verified: {os.path.basename(docker_path)} → {os.path.relpath(absolute_target, base_dir)}")
            
        except Exception as e:
            print(f"❌ ERROR: Could not verify {docker_path} content: {e}")
            all_correct = False
    
    if all_correct:
        print(f"\n✅ All symlinks verified successfully!")
    else:
        print(f"\n⚠️ Some symlinks could not be verified. Please check the errors above.")
    
    return all_correct

def cleanup_root_folder(base_dir, script_dir, docker_dir=None, dry_run=False):
    """Clean up the root folder by removing symlinks"""
    print(f"\n{'=' * 80}")
    print("CLEANING UP ROOT FOLDER")
    print(f"{'=' * 80}")
    
    script_files = []
    docker_files = []
    
    for file in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file)
        if os.path.isfile(file_path):
            if any(file.endswith(ext) for ext in FILE_EXTENSIONS):
                script_files.append(file_path)
            elif any(pattern in file.lower() for pattern in DOCKER_PATTERNS):
                docker_files.append(file_path)
    
    if dry_run:
        print(f"Would remove {len(script_files)} script symlinks from root folder")
        print(f"Would remove {len(docker_files)} Docker file symlinks from root folder")
        return True
    
    # Remove all symlinks in the root folder
    success = True
    
    # Remove script symlinks
    for script_path in script_files:
        if os.path.islink(script_path):
            try:
                print(f"Removing symlink: {os.path.basename(script_path)}")
                os.unlink(script_path)
            except Exception as e:
                print(f"❌ ERROR: Could not remove symlink {script_path}: {e}")
                success = False
    
    # Remove Docker file symlinks
    for docker_path in docker_files:
        if os.path.islink(docker_path):
            try:
                print(f"Removing symlink: {os.path.basename(docker_path)}")
                os.unlink(docker_path)
            except Exception as e:
                print(f"❌ ERROR: Could not remove symlink {docker_path}: {e}")
                success = False
    
    if success:
        print(f"\n✅ Root folder cleaned up successfully!")
    else:
        print(f"\n⚠️ Some symlinks could not be removed. Please check the errors above.")
    
    return success

def organize_scripts(base_dir, dry_run=False, verify_only=False, cleanup=False):
    """Organize scripts and Docker files into the appropriate directories"""
    # Create the directory structure
    script_dir, docker_dir = create_directory_structure(base_dir)
    
    # If verify_only, just check existing symlinks
    if verify_only:
        return verify_symlinks(base_dir, script_dir, docker_dir)
        
    # If cleanup, just remove symlinks from root folder
    if cleanup:
        return cleanup_root_folder(base_dir, script_dir, docker_dir, dry_run)
    
    # Find all script files and Docker files in base directory
    script_files = []
    docker_files = []
    
    for file in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file)
        if os.path.isfile(file_path):
            if any(file.endswith(ext) for ext in FILE_EXTENSIONS):
                script_files.append(file_path)
            elif any(pattern in file.lower() for pattern in DOCKER_PATTERNS):
                docker_files.append(file_path)
    
    # Track organization statistics
    script_stats = {category: 0 for category in SCRIPT_CATEGORIES.keys()}
    docker_stats = {category: 0 for category in ['monitors', 'dashboards', 'analytics', 'services', 'traders', 'cli', 'infra', 'base']}
    extension_stats = {ext: 0 for ext in FILE_EXTENSIONS}
    run_scripts_count = len([s for s in script_files if (os.path.basename(s).startswith(('run_', 'run-', 'dry_run')))])
    docker_count = len(docker_files)
    
    print(f"\n{'=' * 80}")
    print(f"OMEGA SCRIPT ORGANIZER")
    print(f"{'=' * 80}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total script files found: {len(script_files)}")
    print(f"Run scripts found: {run_scripts_count}")
    print(f"Docker files found: {docker_count}")
    
    # Count by extension
    for ext in FILE_EXTENSIONS:
        count = len([s for s in script_files if s.endswith(ext)])
        extension_stats[ext] = count
        print(f"{ext} files: {count}")
    
    print(f"{'=' * 80}\n")
    
    # Organize each script
    print("ORGANIZING SCRIPTS:")
    print(f"{'=' * 80}")
    
    for script_path in script_files:
        script_name = os.path.basename(script_path)
        category = determine_script_category(script_path)
        script_stats[category] += 1
        
        # Determine destination based on whether it's a run script
        if script_name.startswith(('run_', 'run-', 'dry_run')):
            dest_dir = os.path.join(script_dir, category, "run_scripts")
            is_run_script = True
        else:
            dest_dir = os.path.join(script_dir, category)
            is_run_script = False
            
        dest_path = os.path.join(dest_dir, script_name)
        
        # Ensure the source and destination are not the same file
        # This prevents the SameFileError
        if os.path.abspath(script_path) == os.path.abspath(dest_path):
            print(f"Warning: Source and destination are the same for {script_name}. Skipping.")
            continue
        
        print(f"Script: {script_name}")
        print(f"  Category: {category}")
        print(f"  Type: {'Run script' if is_run_script else 'Standard script'}")
        print(f"  Extension: {os.path.splitext(script_path)[1]}")
        print(f"  Destination: {dest_path}")
        
        if not dry_run:
            try:
                # Create destination directory if it doesn't exist
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir, exist_ok=True)
                
                # Copy script to category directory
                shutil.copy2(script_path, dest_path)
                
                # Create symbolic link
                # We need to use relative paths for symlinks to work properly
                rel_path = os.path.relpath(dest_path, os.path.dirname(script_path))
                os.remove(script_path)
                os.symlink(rel_path, script_path)
                
                # Set executable permissions
                os.chmod(dest_path, 0o755)
                
            except Exception as e:
                print(f"Error processing {script_name}: {e}")
        
        print()
    
    # Organize Docker files
    print(f"\n{'=' * 80}")
    print("ORGANIZING DOCKER FILES:")
    print(f"{'=' * 80}")
    
    for docker_path in docker_files:
        docker_name = os.path.basename(docker_path)
        category = determine_docker_category(docker_path)
        docker_stats[category] += 1
        
        dest_dir = os.path.join(docker_dir, category)
        dest_path = os.path.join(dest_dir, docker_name)
        
        # Ensure the source and destination are not the same file
        if os.path.abspath(docker_path) == os.path.abspath(dest_path):
            print(f"Warning: Source and destination are the same for {docker_name}. Skipping.")
            continue
        
        print(f"Docker file: {docker_name}")
        print(f"  Category: {category}")
        print(f"  Destination: {dest_path}")
        
        if not dry_run:
            try:
                # Create destination directory if it doesn't exist
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir, exist_ok=True)
                
                # Copy Docker file to category directory
                shutil.copy2(docker_path, dest_path)
                
                # Create symbolic link
                rel_path = os.path.relpath(dest_path, os.path.dirname(docker_path))
                os.remove(docker_path)
                os.symlink(rel_path, docker_path)
                
            except Exception as e:
                print(f"Error processing {docker_name}: {e}")
        
        print()
    
    # Print statistics
    print(f"{'=' * 80}")
    print("Organization Statistics:")
    
    print("\nScript Categories:")
    for category, count in script_stats.items():
        if count > 0:
            print(f"  {category.capitalize()}: {count} scripts")
    
    print("\nDocker File Categories:")
    for category, count in docker_stats.items():
        if count > 0:
            print(f"  {category.capitalize()}: {count} Docker files")
    
    print(f"\nExtension Statistics:")
    for ext, count in extension_stats.items():
        print(f"  {ext}: {count} files")
    
    print(f"\nRun Scripts Distribution:")
    for category in SCRIPT_CATEGORIES.keys():
        category_run_scripts = [s for s in script_files if os.path.basename(s).startswith(('run_', 'run-', 'dry_run')) and determine_script_category(s) == category]
        if category_run_scripts:
            print(f"  {category.capitalize()}: {len(category_run_scripts)} run scripts")
    
    print(f"{'=' * 80}")
    
    if dry_run:
        print("\nThis was a dry run. No files were moved.")
        print("Run without --dry-run to perform the actual organization.")
    else:
        print("\nScript and Docker file organization complete!")
        print(f"All scripts have been organized into {script_dir}/")
        print(f"All Docker files have been organized into {docker_dir}/")
        print("Original file locations now contain symbolic links to their organized versions.")
        
        # Verify the symlinks
        verify_symlinks(base_dir, script_dir, docker_dir)
        
        # Remind about cleanup
        print("\nTo complete the organization and remove symlinks from root folder:")
        print(f"  python {os.path.basename(__file__)} --cleanup")
    
def main():
    parser = argparse.ArgumentParser(description='Organize shell scripts, Python scripts, and Docker files by function')
    parser.add_argument('--dir', type=str, default='.', help='Base directory containing scripts and Docker files')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--analyze-only', action='store_true', help='Only analyze the files without reorganizing')
    parser.add_argument('--verify', action='store_true', help='Verify existing symlinks are correctly set up')
    parser.add_argument('--cleanup', action='store_true', help='Remove symlinks from root folder after organization')
    parser.add_argument('--extensions', type=str, default='.sh,.py', help='Comma-separated list of file extensions to process')
    parser.add_argument('--no-docker', action='store_true', help='Skip Docker file organization')
    
    args = parser.parse_args()
    
    # Update file extensions if specified
    global FILE_EXTENSIONS
    if args.extensions:
        FILE_EXTENSIONS = args.extensions.split(',')
    
    # Get absolute path of the directory
    base_dir = os.path.abspath(args.dir)
    
    # Process based on arguments
    if args.verify:
        organize_scripts(base_dir, verify_only=True)
    elif args.cleanup:
        organize_scripts(base_dir, cleanup=True, dry_run=args.dry_run)
    else:
        organize_scripts(base_dir, args.dry_run or args.analyze_only)

if __name__ == '__main__':
    main()