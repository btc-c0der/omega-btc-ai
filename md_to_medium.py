#!/usr/bin/env python3
"""
MD to Medium Format Converter

This script converts Markdown files to Medium-ready format, handling:
- Code blocks with proper syntax highlighting
- Image formatting with captions
- Header formatting
- List formatting
- Blockquote formatting
- Link preservation
- Table conversion to Medium format

Usage:
    python md_to_medium.py input.md [output.html]
    
If output file is not specified, it will use the input filename with .html extension.
"""

import re
import sys
import os
import argparse
import markdown
from bs4 import BeautifulSoup

MEDIUM_CSS = """
<style>
    body {
        font-family: 'Charter', 'Georgia', serif;
        line-height: 1.8;
        font-size: 18px;
        color: rgba(0, 0, 0, 0.84);
        margin: 0 auto;
        max-width: 740px;
        padding: 20px;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        margin-top: 36px;
        margin-bottom: 12px;
        font-weight: 600;
    }
    h1 {
        font-size: 32px;
    }
    h2 {
        font-size: 28px;
    }
    h3 {
        font-size: 24px;
    }
    h4 {
        font-size: 20px;
    }
    p, ul, ol {
        margin-bottom: 30px;
    }
    img {
        max-width: 100%;
        margin: 0 auto;
        display: block;
    }
    figcaption {
        text-align: center;
        font-size: 14px;
        color: rgba(0, 0, 0, 0.68);
        margin-top: 5px;
    }
    pre {
        background-color: rgba(0, 0, 0, 0.05);
        padding: 16px;
        overflow: auto;
        border-radius: 3px;
        margin: 20px 0;
    }
    code {
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
        font-size: 14px;
        padding: 2px 4px;
        background-color: rgba(0, 0, 0, 0.05);
        border-radius: 3px;
    }
    pre code {
        background-color: transparent;
        padding: 0;
    }
    blockquote {
        border-left: 3px solid rgba(0, 0, 0, 0.84);
        padding-left: 20px;
        margin-left: 0;
        margin-right: 0;
        font-style: italic;
    }
    a {
        color: #1a8917;
        text-decoration: none;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }
    th, td {
        border: 1px solid rgba(0, 0, 0, 0.15);
        padding: 8px 16px;
        text-align: left;
    }
    th {
        background-color: rgba(0, 0, 0, 0.05);
    }
    hr {
        border: none;
        border-bottom: 1px solid rgba(0, 0, 0, 0.15);
        margin: 30px 0;
    }
    .gist {
        margin: 20px 0;
    }
    .medium-instructions {
        background-color: #ffffd1;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 30px;
    }
</style>
"""

def convert_markdown_to_medium(input_file, output_file=None):
    """
    Convert Markdown file to Medium-ready HTML format
    """
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}.html"
    
    # Read markdown content
    with open(input_file, 'r', encoding='utf-8') as file:
        md_content = file.read()
    
    # Convert Markdown to HTML using the Python Markdown library
    html_content = markdown.markdown(
        md_content,
        extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.smarty',
            'markdown.extensions.codehilite',
        ]
    )
    
    # Create BeautifulSoup object for easy HTML manipulation
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Handle code blocks
    for code_block in soup.find_all('pre'):
        code_tag = code_block.find('code')
        if code_tag:
            # Get language class if available
            lang_class = None
            for cls in code_tag.get('class', []):
                if cls.startswith('language-'):
                    lang_class = cls.replace('language-', '')
                    break
            
            # Add language as comment at the top of code block for Medium
            if lang_class:
                code_tag.insert(0, f"// {lang_class}\n")
    
    # Handle images - Medium prefers figure/figcaption for images with captions
    for img in soup.find_all('img'):
        # Check if image has alt text to use as caption
        alt_text = img.get('alt', '')
        
        # Create figure and figcaption elements
        figure = soup.new_tag('figure')
        img.wrap(figure)
        
        if alt_text:
            figcaption = soup.new_tag('figcaption')
            figcaption.string = alt_text
            figure.append(figcaption)
    
    # Handle blockquotes - Medium prefers more stylized blockquotes
    for blockquote in soup.find_all('blockquote'):
        # Ensure paragraph inside blockquote
        if not blockquote.find('p'):
            p = soup.new_tag('p')
            p.string = blockquote.string
            blockquote.string = ''
            blockquote.append(p)
    
    # Create the final HTML document
    html_output = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medium-Ready Article</title>
    {MEDIUM_CSS}
</head>
<body>
    <div class="medium-instructions">
        <strong>Medium Import Instructions:</strong>
        <ol>
            <li>In Medium, click on your profile picture and select "Stories"</li>
            <li>Click "Import a story"</li>
            <li>Enter the URL of where this HTML is hosted, or</li>
            <li>Copy everything below this yellow box and paste into a Medium story</li>
        </ol>
    </div>
    
    {soup.prettify()}
    
    <script>
        // Add any custom JavaScript here if needed
    </script>
</body>
</html>
"""
    
    # Write the HTML to output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_output)
    
    print(f"Conversion complete! Medium-ready HTML saved to: {output_file}")
    print(f"To use with Medium: Open the HTML file and copy everything below the yellow instructions box")

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to Medium-ready HTML format')
    parser.add_argument('input_file', help='Input Markdown file')
    parser.add_argument('output_file', nargs='?', help='Output HTML file (optional)')
    parser.add_argument('--batch', help='Process all .md files in directory', action='store_true')
    
    args = parser.parse_args()
    
    if args.batch:
        # Process all markdown files in directory
        dir_path = args.input_file if os.path.isdir(args.input_file) else os.path.dirname(args.input_file) or '.'
        md_files = [f for f in os.listdir(dir_path) if f.endswith('.md')]
        
        if not md_files:
            print(f"No markdown files found in {dir_path}")
            return
        
        for md_file in md_files:
            input_path = os.path.join(dir_path, md_file)
            output_path = os.path.splitext(input_path)[0] + '.html'
            print(f"Converting {md_file}...")
            convert_markdown_to_medium(input_path, output_path)
    else:
        # Process single file
        convert_markdown_to_medium(args.input_file, args.output_file)

if __name__ == "__main__":
    main() 