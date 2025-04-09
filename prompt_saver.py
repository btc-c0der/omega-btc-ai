#!/usr/bin/env python3
"""
OMEGA DEV FRAMEWORK - Prompt Saver
==================================

The divine scribe that preserves sacred conversations between developer and AI.
Conversations are saved as both raw text and structured Python, ensuring they become
part of the codebase's eternal wisdom.

Usage:
    python prompt_saver.py --title "Feature_Name" --save
    python prompt_saver.py --title "Feature_Name" --load
    python prompt_saver.py --list
    python prompt_saver.py --search "keyword"
"""

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union

# ANSI color codes for terminal styling
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Constants
PROMPTS_DIR = Path("./omega_prompts")
PROMPTS_INDEX = PROMPTS_DIR / "index.json"

class PromptSaver:
    """Divine scribe that preserves the sacred conversations."""
    
    def __init__(self):
        """Initialize the PromptSaver with cosmic awareness."""
        self._ensure_directories()
        self.index = self._load_index()
    
    def _ensure_directories(self) -> None:
        """Ensure the divine repository structure exists."""
        PROMPTS_DIR.mkdir(exist_ok=True)
        (PROMPTS_DIR / "raw").mkdir(exist_ok=True)
        (PROMPTS_DIR / "py").mkdir(exist_ok=True)
        
        # Initialize index if it doesn't exist
        if not PROMPTS_INDEX.exists():
            with open(PROMPTS_INDEX, 'w') as f:
                json.dump({
                    "version": "1.0.0",
                    "created": datetime.datetime.now().isoformat(),
                    "prompts": {}
                }, f, indent=2)
    
    def _load_index(self) -> Dict:
        """Load the sacred index of conversations."""
        with open(PROMPTS_INDEX, 'r') as f:
            return json.load(f)
    
    def _save_index(self) -> None:
        """Preserve the updated index in the cosmic repository."""
        with open(PROMPTS_INDEX, 'w') as f:
            json.dump(self.index, f, indent=2)
    
    def save_prompt(self, title: str, content: str, tags: Optional[List[str]] = None) -> None:
        """
        Save a divine conversation to the repository.
        
        Args:
            title: The sacred title of the conversation
            content: The raw conversation text
            tags: Optional cosmic categorization tags
        """
        # Sanitize title for filesystem
        safe_title = re.sub(r'[^\w\-\.]', '_', title)
        timestamp = datetime.datetime.now().isoformat()
        
        # Save raw version
        raw_path = PROMPTS_DIR / "raw" / f"{safe_title}.txt"
        with open(raw_path, 'w') as f:
            f.write(content)
        
        # Generate Python module version
        py_content = self._convert_to_python(title, content)
        py_path = PROMPTS_DIR / "py" / f"{safe_title}.py"
        with open(py_path, 'w') as f:
            f.write(py_content)
        
        # Update index
        self.index["prompts"][safe_title] = {
            "title": title,
            "created": timestamp,
            "updated": timestamp,
            "raw_path": str(raw_path.relative_to(PROMPTS_DIR.parent)),
            "py_path": str(py_path.relative_to(PROMPTS_DIR.parent)),
            "tags": tags or [],
            "word_count": len(content.split())
        }
        
        self._save_index()
        print(f"{GREEN}{BOLD}✓ Divine conversation '{title}' has been immortalized{RESET}")
        print(f"{CYAN}Raw text: {raw_path}{RESET}")
        print(f"{CYAN}Python module: {py_path}{RESET}")
    
    def _convert_to_python(self, title: str, content: str) -> str:
        """
        Transform raw conversation into a sacred Python module.
        
        Args:
            title: The divine title
            content: The raw conversation
            
        Returns:
            str: Python module representation
        """
        # Convert title to class name
        class_name = ''.join(word.capitalize() for word in re.sub(r'[^\w]', ' ', title).split())
        
        # Format the conversation as Python docstring and class
        py_content = f'''#!/usr/bin/env python3
"""
OMEGA DEV FRAMEWORK - Divine Conversation
=========================================

Title: {title}
Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Tags: {', '.join(self.index["prompts"].get(title, {}).get("tags", []))}

This is an immortalized conversation from the OMEGA DEV FRAMEWORK.
It contains sacred wisdom that has been preserved as executable code.
"""

class {class_name}:
    """
    Divine wisdom from conversation: "{title}"
    
    This class encapsulates the knowledge from the conversation
    and provides methods to access and implement that wisdom.
    """
    
    CONVERSATION = """
{content}
    """
    
    @classmethod
    def get_wisdom(cls) -> str:
        """
        Retrieve the divine wisdom from this conversation.
        
        Returns:
            str: The full conversation text
        """
        return cls.CONVERSATION
    
    @classmethod
    def implement(cls):
        """
        Implement the divine wisdom from this conversation.
        Override this method with actual implementation.
        """
        print(f"Implementing wisdom from '{title}'...")
        # TODO: Implement the divine wisdom from this conversation
        raise NotImplementedError("The divine implementation is yet to be manifested")


if __name__ == "__main__":
    # Display wisdom when run directly
    print(f"Divine Wisdom from: {title}")
    print("-" * 80)
    print({class_name}.get_wisdom())
'''
        return py_content
    
    def load_prompt(self, title: str, display_format: str = "raw") -> Optional[str]:
        """
        Retrieve a divine conversation from the cosmic repository.
        
        Args:
            title: The sacred title of the conversation
            display_format: 'raw' or 'py' to determine which version to load
            
        Returns:
            str: The conversation content or None if not found
        """
        # Sanitize title for filesystem
        safe_title = re.sub(r'[^\w\-\.]', '_', title)
        
        if safe_title not in self.index["prompts"]:
            print(f"{RED}! Divine conversation '{title}' not found in the repository{RESET}")
            return None
        
        prompt_info = self.index["prompts"][safe_title]
        
        # Determine which path to use
        if display_format == "raw":
            path = Path(prompt_info["raw_path"])
        else:
            path = Path(prompt_info["py_path"])
        
        # Load the content
        try:
            with open(path, 'r') as f:
                content = f.read()
                
            print(f"{GREEN}{BOLD}✓ Divine conversation '{title}' has been retrieved{RESET}")
            print(f"{CYAN}Path: {path}{RESET}")
            print(f"{YELLOW}Created: {prompt_info['created']}{RESET}")
            if "tags" in prompt_info and prompt_info["tags"]:
                print(f"{MAGENTA}Tags: {', '.join(prompt_info['tags'])}{RESET}")
                
            return content
        except FileNotFoundError:
            print(f"{RED}! The divine scroll '{path}' could not be found{RESET}")
            return None
    
    def list_prompts(self, tag: Optional[str] = None) -> None:
        """
        Display a divine catalog of all saved conversations.
        
        Args:
            tag: Optional filter by cosmic tag
        """
        prompts = self.index["prompts"]
        
        if not prompts:
            print(f"{YELLOW}The divine repository contains no conversations yet.{RESET}")
            return
        
        # Filter by tag if specified
        if tag:
            filtered_prompts = {k: v for k, v in prompts.items() if tag in v.get("tags", [])}
            print(f"{CYAN}{BOLD}Divine Conversations with tag '{tag}':{RESET}")
            prompts = filtered_prompts
        else:
            print(f"{CYAN}{BOLD}All Divine Conversations:{RESET}")
        
        # Display the prompts
        for idx, (key, info) in enumerate(sorted(prompts.items(), key=lambda x: x[1]["created"]), 1):
            created = datetime.datetime.fromisoformat(info["created"]).strftime("%Y-%m-%d %H:%M")
            title = info["title"]
            word_count = info.get("word_count", "N/A")
            tags = ", ".join(info.get("tags", []))
            
            print(f"{BOLD}{idx}.{RESET} {GREEN}{title}{RESET}")
            print(f"   {YELLOW}Created: {created}{RESET} | {MAGENTA}Words: {word_count}{RESET}")
            if tags:
                print(f"   {CYAN}Tags: {tags}{RESET}")
    
    def search_prompts(self, keyword: str) -> None:
        """
        Search for divine conversations containing a cosmic keyword.
        
        Args:
            keyword: The sacred term to search for
        """
        prompts = self.index["prompts"]
        matches = []
        
        print(f"{CYAN}{BOLD}Searching for divine conversations containing '{keyword}'...{RESET}")
        
        # Search through raw files
        for key, info in prompts.items():
            raw_path = Path(info["raw_path"])
            try:
                with open(raw_path, 'r') as f:
                    content = f.read()
                if keyword.lower() in content.lower():
                    matches.append((info["title"], info))
            except FileNotFoundError:
                continue
        
        # Display results
        if matches:
            print(f"{GREEN}{BOLD}Found {len(matches)} divine conversations:{RESET}")
            for idx, (title, info) in enumerate(matches, 1):
                created = datetime.datetime.fromisoformat(info["created"]).strftime("%Y-%m-%d %H:%M")
                tags = ", ".join(info.get("tags", []))
                
                print(f"{BOLD}{idx}.{RESET} {GREEN}{title}{RESET}")
                print(f"   {YELLOW}Created: {created}{RESET}")
                if tags:
                    print(f"   {CYAN}Tags: {tags}{RESET}")
        else:
            print(f"{YELLOW}No divine conversations found containing '{keyword}'.{RESET}")


def main():
    """Main entry point for the divine prompt saver."""
    parser = argparse.ArgumentParser(description="OMEGA DEV FRAMEWORK - Divine Conversation Preserver")
    
    # Define command line arguments
    parser.add_argument('--title', help="The sacred title of the conversation")
    parser.add_argument('--save', action='store_true', help="Save divine conversation from stdin")
    parser.add_argument('--load', action='store_true', help="Retrieve a divine conversation")
    parser.add_argument('--list', action='store_true', help="List all divine conversations")
    parser.add_argument('--search', help="Search for a cosmic keyword in conversations")
    parser.add_argument('--format', choices=['raw', 'py'], default='raw', 
                        help="Format for displaying conversations (raw or py)")
    parser.add_argument('--tags', help="Comma-separated cosmic tags (for --save)")
    
    args = parser.parse_args()
    scribe = PromptSaver()
    
    # Execute the divine command
    if args.list:
        scribe.list_prompts()
    elif args.search:
        scribe.search_prompts(args.search)
    elif args.save:
        if not args.title:
            print(f"{RED}! A divine title is required for saving a conversation{RESET}")
            parser.print_help()
            return 1
            
        print(f"{YELLOW}Enter the divine conversation text (Ctrl+D to end):{RESET}")
        content = sys.stdin.read()
        tags = args.tags.split(',') if args.tags else []
        scribe.save_prompt(args.title, content, tags)
    elif args.load:
        if not args.title:
            print(f"{RED}! A divine title is required for loading a conversation{RESET}")
            parser.print_help()
            return 1
            
        content = scribe.load_prompt(args.title, args.format)
        if content:
            print(f"{YELLOW}{BOLD}=== Divine Conversation Content ==={RESET}")
            print(content)
    else:
        parser.print_help()
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 