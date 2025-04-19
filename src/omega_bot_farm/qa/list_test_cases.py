#!/usr/bin/env python3
"""
List Test Cases for CyBer1t4L QA Bot
------------------------------------

A utility script to list all available test cases from the CyBer1t4L QA Bot.
This script can be run from the command line or imported by the Discord bot.
"""
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
import json
import argparse
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# ANSI color codes for output
RESET = "\033[0m"
GREEN = "\033[38;5;82m"
RED = "\033[38;5;196m"
YELLOW = "\033[38;5;226m"
CYAN = "\033[38;5;51m"
BLUE = "\033[38;5;39m"
PURPLE = "\033[38;5;141m"
BOLD = "\033[1m"

def get_config_path() -> str:
    """Get the path to the testcases config file."""
    # First, try to find it in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check in the config directory
    config_path = os.path.join(script_dir, "../docker/cyber1t4l-qa-bot/config/testcases_config.json")
    if os.path.exists(config_path):
        return config_path
    
    # Try alternative locations
    alt_paths = [
        os.path.join(script_dir, "../config/testcases_config.json"),
        os.path.join(script_dir, "testcases_config.json")
    ]
    
    for path in alt_paths:
        if os.path.exists(path):
            return path
    
    # If we didn't find it, return the default path (even if it doesn't exist)
    return config_path

def load_test_cases_from_config() -> Dict[str, Any]:
    """Load test cases from the configuration file."""
    config_path = get_config_path()
    
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            print(f"{YELLOW}Warning: Config file not found at {config_path}{RESET}")
            return {"test_suites": {}, "categories": {}}
    except Exception as e:
        print(f"{RED}Error loading config: {str(e)}{RESET}")
        return {"test_suites": {}, "categories": {}}

def load_test_cases_from_framework() -> Dict[str, Any]:
    """Load test cases from the test automation framework."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    framework_path = os.path.join(script_dir, "test_automation_framework.py")
    
    try:
        if not os.path.exists(framework_path):
            print(f"{YELLOW}Warning: Framework not found at {framework_path}{RESET}")
            return {}
            
        # Try to import the module dynamically
        spec = importlib.util.spec_from_file_location("test_automation_framework", framework_path)
        if spec is None:
            print(f"{YELLOW}Warning: Could not create module spec for framework{RESET}")
            return {}
            
        framework = importlib.util.module_from_spec(spec)
        if spec.loader is None:
            print(f"{YELLOW}Warning: Module spec has no loader{RESET}")
            return {}
            
        spec.loader.exec_module(framework)
        
        # Get test suites
        suites = {}
        
        try:
            discord_suite = framework.define_discord_bot_tests()
            suites[discord_suite.name] = {
                "description": discord_suite.description,
                "tests": [
                    {"name": test["name"], "description": test["description"]}
                    for test in discord_suite.tests
                ]
            }
        except Exception as e:
            print(f"{YELLOW}Warning: Could not load Discord tests: {str(e)}{RESET}")
        
        try:
            network_suite = framework.define_network_tests()
            suites[network_suite.name] = {
                "description": network_suite.description,
                "tests": [
                    {"name": test["name"], "description": test["description"]}
                    for test in network_suite.tests
                ]
            }
        except Exception as e:
            print(f"{YELLOW}Warning: Could not load Network tests: {str(e)}{RESET}")
        
        try:
            system_suite = framework.define_system_tests()
            suites[system_suite.name] = {
                "description": system_suite.description,
                "tests": [
                    {"name": test["name"], "description": test["description"]}
                    for test in system_suite.tests
                ]
            }
        except Exception as e:
            print(f"{YELLOW}Warning: Could not load System tests: {str(e)}{RESET}")
        
        return suites
    except Exception as e:
        print(f"{RED}Error loading framework: {str(e)}{RESET}")
        return {}

def format_test_cases_plain(test_suites: Dict[str, Any], categories: Optional[Dict[str, Any]] = None) -> str:
    """Format test cases as plain text."""
    output = []
    output.append("CyBer1t4L QA Bot Test Cases")
    output.append("===========================\n")
    
    for suite_name, suite in test_suites.items():
        output.append(f"{suite_name}")
        output.append("-" * len(suite_name))
        output.append(f"{suite.get('description', '')}\n")
        
        for i, test in enumerate(suite.get('tests', [])):
            test_name = test.get('name', f"Test {i+1}")
            test_desc = test.get('description', 'No description available')
            test_category = test.get('category', '')
            
            # Add category icon if available
            category_icon = ""
            if categories and test_category and test_category in categories:
                category_icon = f" {categories[test_category].get('icon', '')}"
            
            output.append(f"{i+1}. {test_name}{category_icon}")
            output.append(f"   {test_desc}\n")
    
    return "\n".join(output)

def format_test_cases_markdown(test_suites: Dict[str, Any], categories: Optional[Dict[str, Any]] = None) -> str:
    """Format test cases as markdown."""
    output = []
    output.append("# 🔮 CyBer1t4L QA Bot Test Cases\n")
    
    for suite_name, suite in test_suites.items():
        output.append(f"## {suite_name}")
        output.append(f"*{suite.get('description', '')}*\n")
        
        for i, test in enumerate(suite.get('tests', [])):
            test_name = test.get('name', f"Test {i+1}")
            test_desc = test.get('description', 'No description available')
            test_category = test.get('category', '')
            
            # Add category info if available
            category_info = ""
            if categories and test_category and test_category in categories:
                category_icon = categories[test_category].get('icon', '')
                category_name = categories[test_category].get('description', test_category)
                category_info = f" | {category_icon} {category_name}"
            
            output.append(f"### {i+1}. {test_name}{category_info}")
            output.append(f"{test_desc}\n")
    
    return "\n".join(output)

def format_test_cases_json(test_suites: Dict[str, Any]) -> str:
    """Format test cases as JSON."""
    return json.dumps(test_suites, indent=2)

def get_all_test_cases(format_type: str = "markdown") -> str:
    """Get all test cases formatted according to the specified format."""
    # Load test cases from config
    config = load_test_cases_from_config()
    test_suites = config.get("test_suites", {})
    categories = config.get("categories", {})
    
    # Load test cases from framework if config is empty
    if not test_suites:
        framework_suites = load_test_cases_from_framework()
        if framework_suites:
            test_suites = framework_suites
    
    # Format according to the specified format
    if format_type.lower() == "plain":
        return format_test_cases_plain(test_suites, categories)
    elif format_type.lower() == "json":
        return format_test_cases_json(test_suites)
    else:  # Default to markdown
        return format_test_cases_markdown(test_suites, categories)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="List all test cases for CyBer1t4L QA Bot")
    parser.add_argument(
        "--format", "-f", 
        choices=["plain", "markdown", "json"], 
        default="plain",
        help="Output format"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file to write to (default: stdout)"
    )
    
    args = parser.parse_args()
    
    # Get formatted test cases
    output = get_all_test_cases(args.format)
    
    # Write to file or stdout
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"{GREEN}Test cases written to {args.output}{RESET}")
        except Exception as e:
            print(f"{RED}Error writing to file: {str(e)}{RESET}")
            sys.exit(1)
    else:
        # Add ANSI colors for terminal if using plain format
        if args.format.lower() == "plain":
            output = (
                output
                .replace("CyBer1t4L QA Bot Test Cases", f"{BOLD}{CYAN}CyBer1t4L QA Bot Test Cases{RESET}")
                .replace("===========================", f"{BOLD}{CYAN}==========================={RESET}")
            )
            
            # Color suite names and descriptions
            lines = output.split("\n")
            for i, line in enumerate(lines):
                if i > 2 and line and all(c == "-" for c in line):  # Suite underline
                    lines[i-1] = f"{BOLD}{PURPLE}{lines[i-1]}{RESET}"  # Suite name
                    lines[i] = f"{PURPLE}{line}{RESET}"  # Suite underline
            
            output = "\n".join(lines)
        
        print(output)

if __name__ == "__main__":
    main() 