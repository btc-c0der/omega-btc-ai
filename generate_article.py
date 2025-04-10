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
OMEGA BTC AI - Scientific Article Generator

This script converts the README summaries into a scientific article format using an LLM.
"""

import os
import json
import argparse
import subprocess
import requests
import datetime
from pathlib import Path

# Default configuration
DEFAULT_CLAUDE_API_BASE = "https://api.anthropic.com/v1/messages"
DEFAULT_MODEL = "claude-3-sonnet-20240229"
DEFAULT_OUTPUT_FILE = "OMEGA_BTC_AI_Scientific_Article.md"

def run_readme_scanner():
    """Run the README scanner script to generate the summary file."""
    print("Generating README summaries...")
    try:
        subprocess.run(["python3", "list_readme_content.py"], check=True)
        if os.path.exists("README_SUMMARY.md"):
            print("README summary generated successfully.")
            return True
        else:
            print("Error: README_SUMMARY.md was not created.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error running list_readme_content.py: {e}")
        return False

def read_readme_summary():
    """Read the README summary file."""
    try:
        with open("README_SUMMARY.md", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading README_SUMMARY.md: {e}")
        return None

def get_prompt(readme_summary):
    """Create a scientific article prompt for the LLM."""
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    
    prompt = f"""
You are a computer science researcher specializing in artificial intelligence and cryptocurrency trading systems.
You are writing a scientific article for publication in a technical journal based on the following documentation from a project called OMEGA BTC AI.

The article should follow this structure:
1. Title (creative but academic)
2. Abstract (summarizing the innovation and findings)
3. Introduction (context of crypto trading and AI)
4. System Architecture (hierarchical breakdown of components)
5. Methodology (how the system operates)
6. Results & Discussion (theoretical performance and advantages)
7. Conclusion
8. References (invent appropriate academic references)

Here is the project documentation to base your article on:

{readme_summary}

Write the complete article in markdown format with appropriate sections, maintaining academic tone while highlighting the innovative aspects of this system.
The date of this article is {current_date}.
Include fictional but realistic performance metrics and statistics to support the system's effectiveness.
"""
    return prompt

def call_claude_api(prompt, api_key, model=DEFAULT_MODEL):
    """Call the Claude API to generate the article."""
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    data = {
        "model": model,
        "max_tokens": 4000,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(DEFAULT_CLAUDE_API_BASE, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["content"][0]["text"]
    except requests.exceptions.RequestException as e:
        print(f"Error calling Claude API: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def save_article(article, output_file):
    """Save the generated article to a file."""
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(article)
        print(f"Article saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error saving article: {e}")
        return False

def get_api_key():
    """Get the Claude API key from environment variable or prompt."""
    api_key = os.environ.get("CLAUDE_API_KEY")
    if not api_key:
        api_key = input("Enter your Claude API key: ")
    return api_key

def main():
    """Main function to generate the scientific article."""
    parser = argparse.ArgumentParser(description="Generate a scientific article from README summaries")
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT_FILE, 
                        help=f"Output file path (default: {DEFAULT_OUTPUT_FILE})")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, 
                        help=f"Claude model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--api-key", "-k", 
                        help="Claude API key (can also be set with CLAUDE_API_KEY environment variable)")
    args = parser.parse_args()
    
    # Run the README scanner
    if not run_readme_scanner():
        return
    
    # Read the README summary
    readme_summary = read_readme_summary()
    if not readme_summary:
        return
    
    # Get the API key
    api_key = args.api_key or get_api_key()
    if not api_key:
        print("Error: Claude API key is required.")
        return
    
    # Create the prompt
    prompt = get_prompt(readme_summary)
    
    # Call the Claude API
    print(f"Generating scientific article using {args.model}...")
    article = call_claude_api(prompt, api_key, args.model)
    if not article:
        return
    
    # Save the article
    save_article(article, args.output)
    
    print(f"\nScientific article generation complete!")
    print(f"Article saved to: {args.output}")

if __name__ == "__main__":
    main() 