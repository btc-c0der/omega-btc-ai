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
Docker files, JSON, HTML, and TXT files by function to create a more coherent 
structure within the codebase.
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

# Define script categories and their keywords
SCRIPT_CATEGORIES = {
    'deployment': ['deploy', 'build', 'setup', 'install', 'docker', 'container', 'image', 'scaleway', 'cloud'],
    'services': ['service', 'start', 'stop', 'restart', 'redis', 'postgres', 'database', 'config'],
    'dashboards': ['dashboard', 'divine', 'ui', 'gui', 'interface', 'web', 'display', 'visualize', 'portal'],
    'monitors': ['monitor', 'quad', 'dual', 'position', 'track', 'trap', 'watch', 'btc_monitor', 'market'],
    'analytics': ['analyze', 'gamon', 'trinity', 'prometheus', 'matrix', 'predict', 'trader', 'trading', 'exit', 'stats'],
    'debugging': ['debug', 'trace', 'log', 'diagnostic', 'troubleshoot', 'compile', 'fractal', 'mermaid', 'test'],
    'cli': ['cli', 'command', 'terminal', 'cmd', 'console'],
    'traders': ['trader', 'position', 'trade', 'market', 'exchange', 'bitget', 'binance', 'futures'],
    'docker': ['docker', 'container', 'image', 'registry', 'kubernetes', 'k8s', 'pod', 'deployment'],
    'documentation': ['readme', 'changelog', 'license', 'manifest', 'guide', 'book', 'doc', 'manual'],
    'data': ['data', 'price', 'history', 'json', 'btc_price', 'dump', 'statistics', 'coverage', 'prediction']
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

# JSON file patterns
JSON_FILE_PATTERNS = {
    'data': [r'btc_.*?\.json', r'price_.*?\.json', r'coverage\.json', r'coverage_.*?\.json', r'last_.*?\.json'],
    'configuration': [r'.*?config.*?\.json', r'.*?settings.*?\.json', r'package\.json', r'.*?\.config\.json'],
    'analysis': [r'.*?_analysis.*?\.json', r'.*?_prediction.*?\.json', r'.*?_report.*?\.json'],
    'models': [r'model_.*?\.json', r'.*?_model.*?\.json', r'.*?_weights.*?\.json']
}

# HTML file patterns
HTML_FILE_PATTERNS = {
    'dashboards': [r'.*?dashboard.*?\.html', r'.*?portal.*?\.html', r'.*?ui.*?\.html', r'.*?divine.*?\.html'],
    'reports': [r'.*?report.*?\.html', r'.*?coverage.*?\.html', r'.*?analysis.*?\.html'],
    'visualizations': [r'.*?chart.*?\.html', r'.*?graph.*?\.html', r'.*?plot.*?\.html', r'.*?heatmap.*?\.html'],
    'documentation': [r'docs?_.*?\.html', r'.*?_docs?\.html', r'.*?manual.*?\.html', r'.*?guide.*?\.html']
}

# TXT file patterns
TXT_FILE_PATTERNS = {
    'logs': [r'.*?log.*?\.txt', r'.*?output.*?\.txt', r'.*?error.*?\.txt'],
    'data': [r'btc_.*?\.txt', r'price_.*?\.txt', r'.*?data.*?\.txt'],
    'documentation': [r'readme.*?\.txt', r'.*?note.*?\.txt', r'.*?instruction.*?\.txt'],
    'prompts': [r'prompt.*?\.txt', r'.*?prompt.*?\.txt', r'.*?article.*?\.txt']
}

# File extensions to process
SCRIPT_EXTENSIONS = ['.sh', '.py']
DATA_EXTENSIONS = ['.json', '.html', '.txt']
FILE_EXTENSIONS = SCRIPT_EXTENSIONS + DATA_EXTENSIONS

# Docker file patterns to process
DOCKER_PATTERNS = ['Dockerfile', 'Dockerfile.', 'docker-compose']

def create_directory_structure(base_dir):
    """Create the directory structure for organized files"""
    script_dir = os.path.join(base_dir, "scripts")
    docker_dir = os.path.join(base_dir, "docker")
    data_dir = os.path.join(base_dir, "data")
    docs_dir = os.path.join(base_dir, "docs")
    web_dir = os.path.join(base_dir, "web")
    
    # Create main directories
    dirs_to_create = [script_dir, docker_dir, data_dir, docs_dir, web_dir]
    for dir_path in dirs_to_create:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    
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
    
    # Create category subdirectories for data files
    data_categories = ['json', 'text', 'logs', 'analysis', 'coverage', 'models', 'historical']
    for category in data_categories:
        category_dir = os.path.join(data_dir, category)
        if not os.path.exists(category_dir):
            os.mkdir(category_dir)
    
    # Create category subdirectories for docs
    docs_categories = ['markdown', 'specifications', 'book', 'reference', 'manuals', 'changelogs']
    for category in docs_categories:
        category_dir = os.path.join(docs_dir, category)
        if not os.path.exists(category_dir):
            os.mkdir(category_dir)
    
    # Create category subdirectories for web files
    web_categories = ['dashboards', 'reports', 'visualizations', 'components']
    for category in web_categories:
        category_dir = os.path.join(web_dir, category)
        if not os.path.exists(category_dir):
            os.mkdir(category_dir)
    
    return script_dir, docker_dir, data_dir, docs_dir, web_dir

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

def determine_json_category(json_path):
    """Analyze a JSON file and determine its category based on content and name"""
    json_name = os.path.basename(json_path).lower()
    
    # Check specific JSON patterns first
    for category, patterns in JSON_FILE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, json_name):
                return category
    
    # Check for keywords in the filename
    for category, keywords in SCRIPT_CATEGORIES.items():
        for keyword in keywords:
            if keyword in json_name:
                return category
    
    # If filename doesn't match, check the content
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            try:
                json_data = json.load(f)
                
                # Look for specific keys that might indicate the file's purpose
                json_keys = []
                if isinstance(json_data, dict):
                    json_keys = list(json_data.keys())
                
                # Check for common configuration keys
                config_keys = ['config', 'settings', 'parameters', 'options']
                if any(key in json_keys for key in config_keys):
                    return 'configuration'
                
                # Check for data collection keys
                data_keys = ['data', 'prices', 'values', 'records', 'history']
                if any(key in json_keys for key in data_keys):
                    return 'data'
                
                # Check for analysis or report keys
                analysis_keys = ['analysis', 'report', 'results', 'stats', 'predictions']
                if any(key in json_keys for key in analysis_keys):
                    return 'analysis'
                
                # Check for model related keys
                model_keys = ['model', 'weights', 'layers', 'network', 'hyperparameters']
                if any(key in json_keys for key in model_keys):
                    return 'models'
                
            except json.JSONDecodeError:
                # Not valid JSON or empty, continue with other checks
                pass
    
    except Exception as e:
        print(f"Error analyzing JSON file {json_path}: {e}")
    
    # If BTC or price in the name, it's likely data
    if 'btc' in json_name or 'price' in json_name:
        return 'data'
    
    # Default to data if no clear category
    return 'data'

def determine_html_category(html_path):
    """Analyze an HTML file and determine its category based on content and name"""
    html_name = os.path.basename(html_path).lower()
    
    # Check specific HTML patterns first
    for category, patterns in HTML_FILE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, html_name):
                return category
    
    # Check for keywords in the filename
    if 'dashboard' in html_name or 'ui' in html_name or 'divine' in html_name:
        return 'dashboards'
    elif 'report' in html_name or 'coverage' in html_name:
        return 'reports'
    elif 'chart' in html_name or 'plot' in html_name or 'graph' in html_name or 'map' in html_name:
        return 'visualizations'
    
    # If filename doesn't match, check the content
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            
            # Look for specific HTML tags that might indicate the file's purpose
            if '<canvas' in content or '<svg' in content or '<plot' in content or 'd3' in content:
                return 'visualizations'
            elif '<table' in content and ('report' in content or 'coverage' in content or 'test' in content):
                return 'reports'
            elif '<div' in content and ('dashboard' in content or 'portal' in content):
                return 'dashboards'
            elif '<h1' in content and ('documentation' in content or 'guide' in content or 'manual' in content):
                return 'documentation'
    
    except Exception as e:
        print(f"Error analyzing HTML file {html_path}: {e}")
    
    # Default to visualizations if no clear category
    return 'visualizations'

def determine_txt_category(txt_path):
    """Analyze a TXT file and determine its category based on content and name"""
    txt_name = os.path.basename(txt_path).lower()
    
    # Check specific TXT patterns first
    for category, patterns in TXT_FILE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, txt_name):
                return category
    
    # Check for keywords in the filename
    if 'log' in txt_name or 'output' in txt_name or 'error' in txt_name:
        return 'logs'
    elif 'readme' in txt_name or 'note' in txt_name or 'instruction' in txt_name:
        return 'documentation'
    elif 'btc' in txt_name or 'price' in txt_name or 'data' in txt_name:
        return 'data'
    elif 'prompt' in txt_name or 'article' in txt_name:
        return 'prompts'
    
    # If filename doesn't match, check the first few lines
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            # Read first 10 lines or the whole file if it's shorter
            first_lines = ''.join([next(f, '').lower() for _ in range(10)])
            
            if 'log' in first_lines or 'error' in first_lines or 'warning' in first_lines:
                return 'logs'
            elif 'readme' in first_lines or 'instruction' in first_lines or 'guide' in first_lines:
                return 'documentation'
            elif 'btc' in first_lines or 'bitcoin' in first_lines or 'price' in first_lines:
                return 'data'
            elif 'prompt' in first_lines or 'article' in first_lines or 'writing' in first_lines:
                return 'prompts'
    
    except Exception as e:
        print(f"Error analyzing TXT file {txt_path}: {e}")
    
    # Default to documentation if no clear category
    return 'documentation'

def verify_symlinks(base_dir, script_dir, docker_dir, data_dir, docs_dir, web_dir):
    """Verify all symlinks are correctly pointing to their organized destinations"""
    print(f"\n{'=' * 80}")
    print("VERIFYING SYMLINKS AND FILE INTEGRITY")
    print(f"{'=' * 80}")
    
    all_correct = True
    script_files = []
    docker_files = []
    json_files = []
    html_files = []
    txt_files = []
    
    for file in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file)
        if os.path.isfile(file_path):
            if any(file.endswith(ext) for ext in SCRIPT_EXTENSIONS):
                script_files.append(file_path)
            elif any(pattern in file.lower() for pattern in DOCKER_PATTERNS):
                docker_files.append(file_path)
            elif file.lower().endswith('.json'):
                json_files.append(file_path)
            elif file.lower().endswith('.html'):
                html_files.append(file_path)
            elif file.lower().endswith('.txt'):
                txt_files.append(file_path)
    
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
            if any(script_path.endswith(ext) for ext in SCRIPT_EXTENSIONS):
                if not os.access(absolute_target, os.X_OK):
                    print(f"⚠️ WARNING: Target file is not executable: {absolute_target}")
                    # Make it executable
                    os.chmod(absolute_target, 0o755)
                    print(f"✓ Fixed: Made {absolute_target} executable")
            
            print(f"✓ Verified: {os.path.basename(script_path)} → {os.path.relpath(absolute_target, base_dir)}")
            
        except Exception as e:
            print(f"❌ ERROR: Could not verify {script_path} content: {e}")
            all_correct = False
    
    # Check Docker file symlinks using the same pattern
    all_correct = verify_file_symlinks(docker_files, docker_dir, base_dir, all_correct, "Docker file")
    
    # Check JSON file symlinks
    all_correct = verify_file_symlinks(json_files, data_dir, base_dir, all_correct, "JSON file")
    
    # Check HTML file symlinks
    all_correct = verify_file_symlinks(html_files, web_dir, base_dir, all_correct, "HTML file")
    
    # Check TXT file symlinks
    all_correct = verify_file_symlinks(txt_files, data_dir, base_dir, all_correct, "TXT file")
    
    if all_correct:
        print(f"\n✅ All symlinks verified successfully!")
    else:
        print(f"\n⚠️ Some symlinks could not be verified. Please check the errors above.")
    
    return all_correct

def verify_file_symlinks(files, target_dir, base_dir, all_correct, file_type):
    """Verify symlinks for a specific file type"""
    for file_path in files:
        if not os.path.islink(file_path):
            print(f"❌ ERROR: {file_path} is not a symlink")
            all_correct = False
            continue
            
        # Get the target of the symlink
        target_path = os.readlink(file_path)
        absolute_target = os.path.normpath(os.path.join(os.path.dirname(file_path), target_path))
        
        # Check if the target exists
        if not os.path.exists(absolute_target):
            print(f"❌ ERROR: Symlink target does not exist: {absolute_target}")
            all_correct = False
            continue
            
        # Check if the target is under the target directory
        if not absolute_target.startswith(target_dir):
            print(f"❌ ERROR: Symlink target is not in the appropriate directory: {absolute_target}")
            all_correct = False
            continue
            
        # Check if the target has the same content as the original
        try:
            with open(absolute_target, 'r', encoding='utf-8') as f:
                target_content = f.read()
                
            print(f"✓ Verified: {os.path.basename(file_path)} → {os.path.relpath(absolute_target, base_dir)}")
            
        except Exception as e:
            print(f"❌ ERROR: Could not verify {file_path} content: {e}")
            all_correct = False
    
    return all_correct

def cleanup_root_folder(base_dir, script_dir, docker_dir, data_dir, docs_dir, web_dir, dry_run=False):
    """Clean up the root folder by removing symlinks"""
    print(f"\n{'=' * 80}")
    print("CLEANING UP ROOT FOLDER")
    print(f"{'=' * 80}")
    
    script_files = []
    docker_files = []
    json_files = []
    html_files = []
    txt_files = []
    
    for file in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file)
        if os.path.isfile(file_path):
            if any(file.endswith(ext) for ext in SCRIPT_EXTENSIONS):
                script_files.append(file_path)
            elif any(pattern in file.lower() for pattern in DOCKER_PATTERNS):
                docker_files.append(file_path)
            elif file.lower().endswith('.json'):
                json_files.append(file_path)
            elif file.lower().endswith('.html'):
                html_files.append(file_path)
            elif file.lower().endswith('.txt'):
                txt_files.append(file_path)
    
    if dry_run:
        print(f"Would remove {len(script_files)} script symlinks from root folder")
        print(f"Would remove {len(docker_files)} Docker file symlinks from root folder")
        print(f"Would remove {len(json_files)} JSON file symlinks from root folder")
        print(f"Would remove {len(html_files)} HTML file symlinks from root folder")
        print(f"Would remove {len(txt_files)} TXT file symlinks from root folder")
        return True
    
    # Remove all symlinks in the root folder
    success = True
    
    # Remove script symlinks
    success = remove_symlinks(script_files, success)
    
    # Remove Docker file symlinks
    success = remove_symlinks(docker_files, success)
    
    # Remove JSON file symlinks
    success = remove_symlinks(json_files, success)
    
    # Remove HTML file symlinks
    success = remove_symlinks(html_files, success)
    
    # Remove TXT file symlinks
    success = remove_symlinks(txt_files, success)
    
    if success:
        print(f"\n✅ Root folder cleaned up successfully!")
    else:
        print(f"\n⚠️ Some symlinks could not be removed. Please check the errors above.")
    
    return success

def remove_symlinks(file_paths, success):
    """Remove symlinks for specified file paths"""
    for file_path in file_paths:
        if os.path.islink(file_path):
            try:
                print(f"Removing symlink: {os.path.basename(file_path)}")
                os.unlink(file_path)
            except Exception as e:
                print(f"❌ ERROR: Could not remove symlink {file_path}: {e}")
                success = False
    return success

def organize_files(base_dir, dry_run=False, verify_only=False, cleanup=False):
    """Organize files into the appropriate directories"""
    # Create the directory structure
    script_dir, docker_dir, data_dir, docs_dir, web_dir = create_directory_structure(base_dir)
    
    # If verify_only, just check existing symlinks
    if verify_only:
        return verify_symlinks(base_dir, script_dir, docker_dir, data_dir, docs_dir, web_dir)
        
    # If cleanup, just remove symlinks from root folder
    if cleanup:
        return cleanup_root_folder(base_dir, script_dir, docker_dir, data_dir, docs_dir, web_dir, dry_run)
    
    # Find all relevant files in base directory
    script_files = []
    docker_files = []
    json_files = []
    html_files = []
    txt_files = []
    
    for file in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file)
        if os.path.isfile(file_path):
            if any(file.endswith(ext) for ext in SCRIPT_EXTENSIONS):
                script_files.append(file_path)
            elif any(pattern in file.lower() for pattern in DOCKER_PATTERNS):
                docker_files.append(file_path)
            elif file.lower().endswith('.json'):
                json_files.append(file_path)
            elif file.lower().endswith('.html'):
                html_files.append(file_path)
            elif file.lower().endswith('.txt'):
                txt_files.append(file_path)
    
    # Track organization statistics
    script_stats = {category: 0 for category in SCRIPT_CATEGORIES.keys()}
    docker_stats = {category: 0 for category in ['monitors', 'dashboards', 'analytics', 'services', 'traders', 'cli', 'infra', 'base']}
    json_stats = {category: 0 for category in ['data', 'configuration', 'analysis', 'models', 'analytics', 'monitors']}
    html_stats = {category: 0 for category in ['dashboards', 'reports', 'visualizations', 'documentation']}
    txt_stats = {category: 0 for category in ['logs', 'data', 'documentation', 'prompts']}
    extension_stats = {ext: 0 for ext in FILE_EXTENSIONS}
    
    # Count files
    run_scripts_count = len([s for s in script_files if (os.path.basename(s).startswith(('run_', 'run-', 'dry_run')))])
    docker_count = len(docker_files)
    json_count = len(json_files)
    html_count = len(html_files)
    txt_count = len(txt_files)
    
    print(f"\n{'=' * 80}")
    print(f"OMEGA FILE ORGANIZER")
    print(f"{'=' * 80}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total script files found: {len(script_files)}")
    print(f"Run scripts found: {run_scripts_count}")
    print(f"Docker files found: {docker_count}")
    print(f"JSON files found: {json_count}")
    print(f"HTML files found: {html_count}")
    print(f"TXT files found: {txt_count}")
    
    # Count by extension
    for ext in FILE_EXTENSIONS:
        if ext in SCRIPT_EXTENSIONS:
            count = len([s for s in script_files if s.endswith(ext)])
        elif ext == '.json':
            count = json_count
        elif ext == '.html':
            count = html_count
        elif ext == '.txt':
            count = txt_count
        else:
            count = 0
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
        if os.path.abspath(script_path) == os.path.abspath(dest_path):
            print(f"Warning: Source and destination are the same for {script_name}. Skipping.")
            continue
        
        print(f"Script: {script_name}")
        print(f"  Category: {category}")
        print(f"  Type: {'Run script' if is_run_script else 'Standard script'}")
        print(f"  Extension: {os.path.splitext(script_path)[1]}")
        print(f"  Destination: {dest_path}")
        
        if not dry_run:
            process_file_move(script_path, dest_path, dest_dir, True)  # True for executable scripts
        
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
            process_file_move(docker_path, dest_path, dest_dir)
        
        print()
    
    # Organize JSON files
    print(f"\n{'=' * 80}")
    print("ORGANIZING JSON FILES:")
    print(f"{'=' * 80}")
    
    for json_path in json_files:
        json_name = os.path.basename(json_path)
        category = determine_json_category(json_path)
        json_stats[category] += 1
        
        dest_dir = os.path.join(data_dir, 'json', category)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)
            
        dest_path = os.path.join(dest_dir, json_name)
        
        # Ensure the source and destination are not the same file
        if os.path.abspath(json_path) == os.path.abspath(dest_path):
            print(f"Warning: Source and destination are the same for {json_name}. Skipping.")
            continue
        
        print(f"JSON file: {json_name}")
        print(f"  Category: {category}")
        print(f"  Destination: {dest_path}")
        
        if not dry_run:
            process_file_move(json_path, dest_path, dest_dir)
        
        print()
    
    # Organize HTML files
    print(f"\n{'=' * 80}")
    print("ORGANIZING HTML FILES:")
    print(f"{'=' * 80}")
    
    for html_path in html_files:
        html_name = os.path.basename(html_path)
        category = determine_html_category(html_path)
        html_stats[category] += 1
        
        dest_dir = os.path.join(web_dir, category)
        dest_path = os.path.join(dest_dir, html_name)
        
        # Ensure the source and destination are not the same file
        if os.path.abspath(html_path) == os.path.abspath(dest_path):
            print(f"Warning: Source and destination are the same for {html_name}. Skipping.")
            continue
        
        print(f"HTML file: {html_name}")
        print(f"  Category: {category}")
        print(f"  Destination: {dest_path}")
        
        if not dry_run:
            process_file_move(html_path, dest_path, dest_dir)
        
        print()
    
    # Organize TXT files
    print(f"\n{'=' * 80}")
    print("ORGANIZING TXT FILES:")
    print(f"{'=' * 80}")
    
    for txt_path in txt_files:
        txt_name = os.path.basename(txt_path)
        category = determine_txt_category(txt_path)
        txt_stats[category] += 1
        
        # Determine appropriate destination directory based on category
        if category == 'documentation':
            dest_dir = os.path.join(docs_dir, 'text')
        else:
            dest_dir = os.path.join(data_dir, 'text', category)
        
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)
            
        dest_path = os.path.join(dest_dir, txt_name)
        
        # Ensure the source and destination are not the same file
        if os.path.abspath(txt_path) == os.path.abspath(dest_path):
            print(f"Warning: Source and destination are the same for {txt_name}. Skipping.")
            continue
        
        print(f"TXT file: {txt_name}")
        print(f"  Category: {category}")
        print(f"  Destination: {dest_path}")
        
        if not dry_run:
            process_file_move(txt_path, dest_path, dest_dir)
        
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
    
    print("\nJSON File Categories:")
    for category, count in json_stats.items():
        if count > 0:
            print(f"  {category.capitalize()}: {count} JSON files")
    
    print("\nHTML File Categories:")
    for category, count in html_stats.items():
        if count > 0:
            print(f"  {category.capitalize()}: {count} HTML files")
    
    print("\nTXT File Categories:")
    for category, count in txt_stats.items():
        if count > 0:
            print(f"  {category.capitalize()}: {count} TXT files")
    
    print(f"\nExtension Statistics:")
    for ext, count in extension_stats.items():
        if count > 0:
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
        print("\nFile organization complete!")
        print(f"All scripts have been organized into {script_dir}/")
        print(f"All Docker files have been organized into {docker_dir}/")
        print(f"All JSON files have been organized into {data_dir}/json/")
        print(f"All HTML files have been organized into {web_dir}/")
        print(f"All TXT files have been organized into {data_dir}/text/ or {docs_dir}/text/")
        print("Original file locations now contain symbolic links to their organized versions.")
        
        # Verify the symlinks
        verify_symlinks(base_dir, script_dir, docker_dir, data_dir, docs_dir, web_dir)
        
        # Remind about cleanup
        print("\nTo complete the organization and remove symlinks from root folder:")
        print(f"  python {os.path.basename(__file__)} --cleanup")

def process_file_move(source_path, dest_path, dest_dir, make_executable=False):
    """Process the move of a file to its destination with proper error handling"""
    try:
        # Create destination directory if it doesn't exist
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)
        
        # Copy file to category directory
        shutil.copy2(source_path, dest_path)
        
        # Create symbolic link
        # We need to use relative paths for symlinks to work properly
        rel_path = os.path.relpath(dest_path, os.path.dirname(source_path))
        os.remove(source_path)
        os.symlink(rel_path, source_path)
        
        # Set executable permissions if needed (for scripts)
        if make_executable:
            os.chmod(dest_path, 0o755)
            
    except Exception as e:
        print(f"Error processing {os.path.basename(source_path)}: {e}")
    
def main():
    parser = argparse.ArgumentParser(
        description='Organize shell scripts, Python scripts, Docker files, JSON, HTML, and TXT files by function'
    )
    parser.add_argument('--dir', type=str, default='.', help='Base directory containing files')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--analyze-only', action='store_true', help='Only analyze the files without reorganizing')
    parser.add_argument('--verify', action='store_true', help='Verify existing symlinks are correctly set up')
    parser.add_argument('--cleanup', action='store_true', help='Remove symlinks from root folder after organization')
    parser.add_argument('--extensions', type=str, default='.sh,.py,.json,.html,.txt', 
                      help='Comma-separated list of file extensions to process')
    parser.add_argument('--no-docker', action='store_true', help='Skip Docker file organization')
    parser.add_argument('--no-json', action='store_true', help='Skip JSON file organization')
    parser.add_argument('--no-html', action='store_true', help='Skip HTML file organization')
    parser.add_argument('--no-txt', action='store_true', help='Skip TXT file organization')
    
    args = parser.parse_args()
    
    # Update file extensions if specified
    global FILE_EXTENSIONS
    if args.extensions:
        FILE_EXTENSIONS = args.extensions.split(',')
    
    # Get absolute path of the directory
    base_dir = os.path.abspath(args.dir)
    
    # Process based on arguments
    if args.verify:
        organize_files(base_dir, verify_only=True)
    elif args.cleanup:
        organize_files(base_dir, cleanup=True, dry_run=args.dry_run)
    else:
        organize_files(base_dir, args.dry_run or args.analyze_only)

if __name__ == '__main__':
    main()