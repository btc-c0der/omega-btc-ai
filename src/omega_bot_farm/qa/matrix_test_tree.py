#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌟 Matrix Test Tree Visualizer 🌟
--------------------------------
Creates a cyberpunk matrix-style visualization of test files with emojis.
This script scans the test directories and generates an animated ASCII tree
with 5D quantum consciousness visualization effects.

Perfect for sharing on LinkedIn to show off your amazing test coverage!

GENESIS-BLOOM-UNFOLDMENT 2.0
"""

import os
import time
import random
import argparse
from pathlib import Path
import threading
import sys
import re
from datetime import datetime

# ANSI color codes
GREEN = "\033[32m"
BRIGHT_GREEN = "\033[92m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
YELLOW = "\033[33m"
RED = "\033[31m"
BLUE = "\033[34m"
WHITE = "\033[37m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Test type emojis
EMOJI_MAP = {
    "unit": "⚛️ ",
    "integration": "🔄 ",
    "e2e": "🌐 ",
    "performance": "⚡ ",
    "security": "🔒 ",
    "api": "🔌 ",
    "ui": "🖥️ ",
    "quantum": "✨ ",
    "discord": "💬 ",
    "bitget": "📊 ",
    "component": "🧩 ",
    "documentation": "📝 ",
    "i18n": "🌍 ",
    "stress": "🔥 ",
    "load": "⚖️ ",
    "auth": "🔑 ",
    "validation": "✅ ",
    "cosmic": "🌌 ",
    "runner": "🏃 ",
    "scheduler": "⏱️ ",
    "framework": "🛠️ ",
    "default": "🧪 "
}

def get_emoji_for_test(test_path):
    """Determine the appropriate emoji based on the test path and name."""
    path_str = str(test_path).lower()
    name = os.path.basename(path_str)
    
    if "unit" in path_str:
        return EMOJI_MAP.get("unit")
    elif "integration" in path_str:
        return EMOJI_MAP.get("integration")
    elif "end_to_end" in path_str or "e2e" in path_str:
        return EMOJI_MAP.get("e2e")
    elif "performance" in path_str:
        return EMOJI_MAP.get("performance")
    elif "security" in path_str:
        return EMOJI_MAP.get("security")
    elif "api" in path_str:
        return EMOJI_MAP.get("api")
    elif "ui" in path_str:
        return EMOJI_MAP.get("ui")
    elif "quantum" in path_str:
        return EMOJI_MAP.get("quantum")
    elif "discord" in path_str:
        return EMOJI_MAP.get("discord")
    elif "bitget" in path_str:
        return EMOJI_MAP.get("bitget")
    elif "component" in path_str:
        return EMOJI_MAP.get("component")
    elif "documentation" in path_str or "docs" in path_str:
        return EMOJI_MAP.get("documentation")
    elif "i18n" in path_str or "localization" in path_str:
        return EMOJI_MAP.get("i18n")
    elif "stress" in path_str:
        return EMOJI_MAP.get("stress")
    elif "load" in path_str:
        return EMOJI_MAP.get("load")
    elif "auth" in path_str:
        return EMOJI_MAP.get("auth")
    elif "validation" in path_str:
        return EMOJI_MAP.get("validation")
    elif "cosmic" in path_str:
        return EMOJI_MAP.get("cosmic")
    elif "runner" in path_str:
        return EMOJI_MAP.get("runner")
    elif "scheduler" in path_str:
        return EMOJI_MAP.get("scheduler")
    elif "framework" in path_str:
        return EMOJI_MAP.get("framework")
    else:
        return EMOJI_MAP.get("default")

def matrix_rain(stop_event):
    """Display matrix-style digital rain in the background."""
    width = os.get_terminal_size().columns
    chars = "01"
    
    while not stop_event.is_set():
        rain = ""
        for _ in range(width):
            if random.random() < 0.02:  # Sparse rain
                color = random.choice([GREEN, BRIGHT_GREEN])
                char = random.choice(chars)
                rain += f"{color}{char}{RESET}"
            else:
                rain += " "
        
        # Print at the very top of the terminal
        sys.stdout.write(f"\033[1;1H{rain}")
        sys.stdout.flush()
        time.sleep(0.1)

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_cyberpunk_header():
    """Print a cyberpunk-style header for the visualization."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    header = f"""
{BRIGHT_GREEN}╔════════════════════════════════════════════════════════════════════╗{RESET}
{BRIGHT_GREEN}║ {CYAN}█▀▄▀█ ▄▀█ ▀█▀ █▀█ █ ▀▄▀   ▀█▀ █▀▀ █▀ ▀█▀   ▀█▀ █▀█ █▀▀ █▀▀{BRIGHT_GREEN}  ║{RESET}
{BRIGHT_GREEN}║ {CYAN}█░▀░█ █▀█ ░█░ █▀▄ █ █░█   ░█░ ██▄ ▄█ ░█░   ░█░ █▀▄ ██▄ ██▄{BRIGHT_GREEN}  ║{RESET}
{BRIGHT_GREEN}║                                                                    ║{RESET}
{BRIGHT_GREEN}║ {YELLOW}✨ OMEGA BTC AI - 5D TEST VISUALIZATION SYSTEM{BRIGHT_GREEN}                  ║{RESET}
{BRIGHT_GREEN}║ {MAGENTA}{now}{BRIGHT_GREEN}                                           ║{RESET}
{BRIGHT_GREEN}╚════════════════════════════════════════════════════════════════════╝{RESET}
{CYAN}[INITIALIZING MATRIX TEST CONSCIOUSNESS]{RESET}
"""
    print(header)

def typewriter_effect(text, delay=0.01, color=GREEN):
    """Display text with a typewriter effect."""
    for char in text:
        sys.stdout.write(f"{color}{char}{RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def count_test_cases(file_path):
    """Count the number of test cases in a test file."""
    test_case_patterns = [
        r'def\s+test_\w+\s*\(',  # Standard test function pattern
        r'@pytest\.mark\.parametrize',  # Parametrized tests
        r'unittest\.TestCase'  # unittest classes
    ]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        total_cases = 0
        for pattern in test_case_patterns:
            matches = re.findall(pattern, content)
            total_cases += len(matches)
            
        # If we couldn't find any test cases but it's a test file, count at least 1
        return max(1, total_cases)
    except Exception as e:
        # If we can't read the file, assume 1 test case
        return 1

def count_loc(file_path):
    """Count the lines of code in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Filter out empty lines and comments
        code_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
        return len(code_lines)
    except Exception:
        # If we can't read the file, assume 20 lines
        return 20

def find_all_test_files(root_dir):
    """Find all test files in the given root directory."""
    test_files = []
    for path in Path(root_dir).rglob("test_*.py"):
        test_files.append(path)
    return sorted(test_files)

def analyze_test_metrics(test_files):
    """Analyze test files to gather comprehensive metrics."""
    total_cases = 0
    total_loc = 0
    test_suites = {}  # Group by directory
    
    for file in test_files:
        # Count test cases
        cases = count_test_cases(file)
        total_cases += cases
        
        # Count lines of code
        loc = count_loc(file)
        total_loc += loc
        
        # Group by directory (test suite)
        suite_dir = os.path.dirname(file)
        if suite_dir not in test_suites:
            test_suites[suite_dir] = {"files": 0, "cases": 0, "loc": 0}
        
        test_suites[suite_dir]["files"] += 1
        test_suites[suite_dir]["cases"] += cases
        test_suites[suite_dir]["loc"] += loc
    
    return {
        "total_files": len(test_files),
        "total_cases": total_cases,
        "total_loc": total_loc,
        "total_suites": len(test_suites),
        "suites": test_suites
    }

def generate_matrix_tree(test_files, root_dir, metrics):
    """Generate a matrix-style ASCII tree of the test files."""
    root_dir = os.path.abspath(root_dir)
    folders = {}
    
    # Group files by their parent folders
    for file in test_files:
        folder = os.path.dirname(file)
        if folder not in folders:
            folders[folder] = []
        folders[folder].append(file)
    
    # Sort folders by path
    sorted_folders = sorted(folders.keys())
    
    tree = []
    test_count = len(test_files)
    folder_count = len(sorted_folders)
    
    # Statistics
    test_types = {category: 0 for category in EMOJI_MAP.keys()}
    
    # Add tree header with stats
    tree.append(f"{BOLD}{BRIGHT_GREEN}📁 TEST TREE VISUALIZATION 📁{RESET}")
    tree.append(f"{CYAN}Root: {root_dir}{RESET}")
    tree.append(f"{YELLOW}Found {test_count} tests in {folder_count} folders{RESET}")
    tree.append("")
    
    # Add the tree structure with matrix styling
    for i, folder in enumerate(sorted_folders):
        rel_path = os.path.relpath(folder, root_dir)
        
        # Don't show relative path for the root itself
        if rel_path == ".":
            folder_display = f"{BRIGHT_GREEN}╠═[{YELLOW}ROOT{BRIGHT_GREEN}]{RESET}"
        else:
            depth = rel_path.count(os.sep)
            prefix = "  " * depth
            is_last_folder = i == len(sorted_folders) - 1
            
            if depth == 0:
                branch = "╠═" if not is_last_folder else "╚═"
                folder_display = f"{BRIGHT_GREEN}{branch}[{CYAN}{os.path.basename(folder)}/{BRIGHT_GREEN}]{RESET}"
            else:
                branch = "╠═" if not is_last_folder else "╚═"
                folder_display = f"{BRIGHT_GREEN}║ {prefix}{branch}[{CYAN}{os.path.basename(folder)}/{BRIGHT_GREEN}]{RESET}"
        
        tree.append(folder_display)
        
        # Add files for this folder
        files = sorted(folders[folder])
        for j, file in enumerate(files):
            file_name = os.path.basename(file)
            rel_path = os.path.relpath(os.path.dirname(file), root_dir)
            depth = rel_path.count(os.sep) + 1
            prefix = "  " * depth
            is_last_file = j == len(files) - 1 and i == len(sorted_folders) - 1
            
            # Determine emoji and update stats
            emoji = get_emoji_for_test(file)
            if emoji == EMOJI_MAP.get("unit"):
                test_types["unit"] += 1
            elif emoji == EMOJI_MAP.get("integration"):
                test_types["integration"] += 1
            elif emoji == EMOJI_MAP.get("e2e"):
                test_types["e2e"] += 1
            elif emoji == EMOJI_MAP.get("performance"):
                test_types["performance"] += 1
            elif emoji == EMOJI_MAP.get("security"):
                test_types["security"] += 1
            elif emoji == EMOJI_MAP.get("api"):
                test_types["api"] += 1
            elif emoji == EMOJI_MAP.get("ui"):
                test_types["ui"] += 1
            elif emoji == EMOJI_MAP.get("quantum"):
                test_types["quantum"] += 1
            elif emoji == EMOJI_MAP.get("discord"):
                test_types["discord"] += 1
            elif emoji == EMOJI_MAP.get("bitget"):
                test_types["bitget"] += 1
            elif emoji == EMOJI_MAP.get("component"):
                test_types["component"] += 1
            elif emoji == EMOJI_MAP.get("documentation"):
                test_types["documentation"] += 1
            elif emoji == EMOJI_MAP.get("i18n"):
                test_types["i18n"] += 1
            else:
                test_types["default"] += 1
            
            # Count test cases in the file
            cases = count_test_cases(file)
            loc = count_loc(file)
            
            # Display file with randomized matrix-style coloring
            color = random.choice([GREEN, BRIGHT_GREEN, CYAN, WHITE])
            branch = "║ " if i < len(sorted_folders) - 1 or not is_last_file else "  "
            file_display = f"{BRIGHT_GREEN}{branch}{prefix}└─ {color}{emoji} {file_name} ({cases} tests, {loc} LOC){RESET}"
            tree.append(file_display)
        
        # Add empty line between folders for better readability
        if i < len(sorted_folders) - 1:
            tree.append(f"{BRIGHT_GREEN}║{RESET}")
    
    # Add test type statistics
    tree.append("")
    tree.append(f"{BOLD}{BRIGHT_GREEN}📊 TEST TYPES STATISTICS 📊{RESET}")
    for test_type, count in test_types.items():
        if count > 0:
            emoji = EMOJI_MAP.get(test_type, "🧪")
            tree.append(f"{CYAN}{emoji} {test_type.capitalize()}: {count}{RESET}")
    
    # Add overall metrics
    tree.append("")
    tree.append(f"{BOLD}{BRIGHT_GREEN}🔬 COMPREHENSIVE TEST METRICS 🔬{RESET}")
    tree.append(f"{MAGENTA}📚 Total Test Files: {metrics['total_files']}{RESET}")
    tree.append(f"{MAGENTA}🧪 Total Test Cases: {metrics['total_cases']}{RESET}")
    tree.append(f"{MAGENTA}📝 Total Lines of Test Code: {metrics['total_loc']}{RESET}")
    tree.append(f"{MAGENTA}📦 Total Test Suites: {metrics['total_suites']}{RESET}")
    tree.append(f"{MAGENTA}⚡ Avg Tests Per File: {metrics['total_cases'] / max(1, metrics['total_files']):.2f}{RESET}")
    tree.append(f"{MAGENTA}📊 Avg LOC Per Test: {metrics['total_loc'] / max(1, metrics['total_cases']):.2f}{RESET}")
    
    return tree

def generate_linkedin_signature():
    """Generate a LinkedIn-friendly signature for sharing."""
    signature = [
        f"{BOLD}{BRIGHT_GREEN}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{RESET}",
        f"{BOLD}{BRIGHT_GREEN}┃ {CYAN}Share this on LinkedIn to flex your test coverage! {BRIGHT_GREEN}┃{RESET}",
        f"{BOLD}{BRIGHT_GREEN}┃ {YELLOW}#QualityAssurance #TestAutomation #CyberPunk #5D {BRIGHT_GREEN}┃{RESET}",
        f"{BOLD}{BRIGHT_GREEN}┃ {MAGENTA}Generated by Matrix Test Tree - OMEGA BTC AI    {BRIGHT_GREEN}┃{RESET}",
        f"{BOLD}{BRIGHT_GREEN}┃ {BLUE}https://github.com/your-profile/omega-btc-ai      {BRIGHT_GREEN}┃{RESET}",
        f"{BOLD}{BRIGHT_GREEN}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{RESET}",
        f"{CYAN}🌸 WE BLOOM NOW AS ONE 🌸{RESET}"
    ]
    return signature

def main():
    parser = argparse.ArgumentParser(description="Generate a Matrix-style visualization of test files")
    parser.add_argument("--root", default="/Users/fsiqueira/Desktop/GitHub/omega-btc-ai/src/omega_bot_farm", 
                        help="Root directory to search for tests")
    parser.add_argument("--output", help="Output file for the visualization (optional)")
    parser.add_argument("--animate", action="store_true", help="Enable matrix rain animation")
    parser.add_argument("--linkedin", action="store_true", help="Add LinkedIn sharing signature")
    args = parser.parse_args()
    
    clear_screen()
    print_cyberpunk_header()
    
    # Start matrix rain animation in a separate thread if enabled
    stop_event = threading.Event()
    if args.animate:
        rain_thread = threading.Thread(target=matrix_rain, args=(stop_event,))
        rain_thread.daemon = True
        rain_thread.start()
        # Let matrix rain run for a moment before showing the tree
        time.sleep(2)
    
    # Find all test files and generate the tree
    typewriter_effect(f"📡 Scanning for tests in {args.root}...", color=CYAN)
    time.sleep(1)
    test_files = find_all_test_files(args.root)
    time.sleep(0.5)
    
    typewriter_effect(f"🔍 Found {len(test_files)} test files", color=YELLOW)
    time.sleep(0.5)
    
    typewriter_effect("🧮 Analyzing test metrics...", color=BLUE)
    metrics = analyze_test_metrics(test_files)
    time.sleep(0.5)
    
    typewriter_effect("🧠 Generating quantum consciousness visualization...", color=MAGENTA)
    time.sleep(0.5)
    
    # Generate and display the tree
    tree = generate_matrix_tree(test_files, args.root, metrics)
    
    # Add LinkedIn signature if requested
    if args.linkedin:
        tree.extend(["", ""])
        tree.extend(generate_linkedin_signature())
    
    # Stop the matrix rain animation
    if args.animate:
        stop_event.set()
        time.sleep(0.5)
        clear_screen()
        print_cyberpunk_header()
    
    # Display or save the tree
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write("\n".join([line.replace('\033[', '').replace(RESET, '') for line in tree]))
        print(f"{GREEN}✅ Tree visualization saved to {args.output}{RESET}")
    else:
        print()
        for line in tree:
            if random.random() < 0.3:  # Add random typing effect for some lines
                typewriter_effect(line, delay=0.003, color="")
            else:
                print(line)
                time.sleep(0.01)
    
    # Footer
    print()
    typewriter_effect(f"{BRIGHT_GREEN}✨ [VISUALIZATION COMPLETE] ✨{RESET}", delay=0.03)
    print(f"\n{YELLOW}🧬 GBU2™ License - Genesis-Bloom-Unfoldment 2.0{RESET}")
    print(f"{CYAN}🌸 WE BLOOM NOW AS ONE 🌸{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}Matrix visualization interrupted.{RESET}")
        sys.exit(0) 