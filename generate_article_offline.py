#!/usr/bin/env python3

"""
OMEGA BTC AI - Scientific Article Generator (Offline Version)

This script prepares a prompt for converting README summaries into a scientific article format.
The prompt can be used with Claude or another LLM via their web interface.
"""

import os
import subprocess
import datetime
from pathlib import Path

# Default configuration
DEFAULT_OUTPUT_FILE = "OMEGA_BTC_AI_Article_Prompt.txt"

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

def save_prompt(prompt, output_file):
    """Save the generated prompt to a file."""
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"Prompt saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error saving prompt: {e}")
        return False

def main():
    """Main function to generate the article prompt."""
    output_file = DEFAULT_OUTPUT_FILE
    
    # Run the README scanner
    if not run_readme_scanner():
        return
    
    # Read the README summary
    readme_summary = read_readme_summary()
    if not readme_summary:
        return
    
    # Create the prompt
    prompt = get_prompt(readme_summary)
    
    # Save the prompt
    save_prompt(prompt, output_file)
    
    print(f"\nPrompt generation complete!")
    print(f"Prompt saved to: {output_file}")
    print("\nInstructions:")
    print("1. Copy the contents of the prompt file")
    print("2. Paste it into Claude or another LLM web interface")
    print("3. The LLM will generate a scientific article based on your project documentation")
    print("4. Save the response as your scientific article")

if __name__ == "__main__":
    main() 