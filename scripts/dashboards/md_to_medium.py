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
MD to Medium Format Converter

This script converts Markdown files to Medium-ready format, handling:
- Code blocks with proper syntax highlighting
- Image formatting with captions
- Header formatting
- List formatting
- Blockquote formatting
- Link preservation
- Table conversion to Medium format
- Recursive directory scanning
- Smart directory organization recommendations

Usage:
    python md_to_medium.py input.md [output.html]
    python md_to_medium.py directory/ --batch
    python md_to_medium.py directory/ --recursive
    python md_to_medium.py directory/ --organize
    
If output file is not specified, it will use the input filename with .html extension.
"""

import re
import sys
import os
import argparse
import markdown
import shutil
from bs4 import BeautifulSoup
from collections import defaultdict
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('md_to_medium')

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
    .divine-text {
        color: #6b46c1;
        font-style: italic;
    }
</style>
"""

# Define category patterns for organization
CATEGORY_PATTERNS = {
    'quantum': ['quantum', 'qubit', 'entanglement'],
    'divine': ['divine', 'sacred', 'blessing', 'ritual'],
    'cosmic': ['cosmic', 'matrix', 'oracle'],
    'technical': ['deployment', 'architecture', 'system', 'infrastructure', 'kubernetes', 'docker'],
    'trading': ['trading', 'market', 'price', 'btc', 'bitcoin', 'crypto', 'position'],
    'documentation': ['manual', 'guide', 'readme', 'catalog', 'installation']
}

def extract_title_from_markdown(md_content):
    """Extract the title from markdown content (first h1)"""
    lines = md_content.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    
    # If no title found, try to extract from filename
    return None

def analyze_content(md_content):
    """Analyze markdown content to determine category and topics"""
    content_lower = md_content.lower()
    
    # Count occurrences of category keywords
    category_scores = defaultdict(int)
    for category, keywords in CATEGORY_PATTERNS.items():
        for keyword in keywords:
            category_scores[category] += content_lower.count(keyword)
    
    # Find the category with the highest score
    primary_category = max(category_scores.items(), key=lambda x: x[1]) if category_scores else ('uncategorized', 0)
    
    return primary_category[0] if primary_category[1] > 0 else 'uncategorized'

def convert_markdown_to_medium(input_file, output_file=None):
    """
    Convert Markdown file to Medium-ready HTML format
    """
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}.html"
    
    # Read markdown content
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            md_content = file.read()
    except UnicodeDecodeError:
        logger.warning(f"Could not read {input_file} with UTF-8 encoding. Trying with ISO-8859-1.")
        with open(input_file, 'r', encoding='ISO-8859-1') as file:
            md_content = file.read()
    except Exception as e:
        logger.error(f"Error reading {input_file}: {str(e)}")
        return None, None
    
    # Extract title and category for organizing
    title = extract_title_from_markdown(md_content)
    category = analyze_content(md_content)
    
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
        code_tag = code_block.find('code') if hasattr(code_block, 'find') else None
        if code_tag:
            # Get language class if available
            lang_class = None
            if hasattr(code_tag, 'get'):
                for cls in code_tag.get('class', []) or []:
                    if isinstance(cls, str) and cls.startswith('language-'):
                        lang_class = cls.replace('language-', '')
                        break
            
            # Add language as comment at the top of code block for Medium
            if lang_class and hasattr(code_tag, 'insert'):
                code_tag.insert(0, f"// {lang_class}\n")
    
    # Handle images - Medium prefers figure/figcaption for images with captions
    for img in soup.find_all('img'):
        # Check if image has alt text to use as caption
        alt_text = img.get('alt', '') if hasattr(img, 'get') else ''
        
        # Create figure and figcaption elements
        figure = soup.new_tag('figure')
        if hasattr(img, 'wrap'):
            img.wrap(figure)
        
        if alt_text and hasattr(figure, 'append'):
            figcaption = soup.new_tag('figcaption')
            if hasattr(figcaption, 'string'):
                figcaption.string = alt_text
            figure.append(figcaption)
    
    # Handle blockquotes - Medium prefers more stylized blockquotes
    for blockquote in soup.find_all('blockquote'):
        # Ensure paragraph inside blockquote
        if hasattr(blockquote, 'find') and not blockquote.find('p'):
            p = soup.new_tag('p')
            if hasattr(blockquote, 'string') and hasattr(p, 'string'):
                p.string = blockquote.string or ''
            if hasattr(blockquote, 'string'):
                blockquote.string = ''
            if hasattr(blockquote, 'append'):
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
        <p><strong>Category:</strong> <span class="divine-text">{category.title()}</span></p>
    </div>
    
    {soup.prettify() if hasattr(soup, 'prettify') else str(soup)}
    
    <script>
        // Add any custom JavaScript here if needed
    </script>
</body>
</html>
"""
    
    # Write the HTML to output file
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(html_output)
        logger.info(f"Conversion complete! Medium-ready HTML saved to: {output_file}")
        logger.info(f"To use with Medium: Open the HTML file and copy everything below the yellow instructions box")
        return title, category
    except Exception as e:
        logger.error(f"Error writing to {output_file}: {str(e)}")
        return title, category

def find_all_markdown_files(directory, recursive=False):
    """Find all markdown files in directory and optionally subdirectories"""
    md_files = []
    
    if recursive:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.md'):
                    md_files.append(os.path.join(root, file))
    else:
        # Just list files in the immediate directory
        for file in os.listdir(directory):
            if file.lower().endswith('.md') and os.path.isfile(os.path.join(directory, file)):
                md_files.append(os.path.join(directory, file))
    
    return md_files

def recommend_organization(file_categories, base_dir):
    """Generate recommendations for organizing files based on categories"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_structure = os.path.join(base_dir, f"BOOK_ORGANIZED_{timestamp}")
    
    logger.info(f"\n{'='*80}\n🌟 DIVINE ORGANIZATION RECOMMENDATIONS 🌟\n{'='*80}")
    logger.info(f"The sacred ch1ndr3n of your BOOK directory can be harmoniously organized into a new structure:")
    logger.info(f"\nRecommended Structure: {new_structure}/")
    
    # Print the virtual directory structure
    categories_count = defaultdict(int)
    
    for _, category in file_categories.items():
        categories_count[category] += 1
    
    # Print category counts
    for category, count in sorted(categories_count.items(), key=lambda x: x[1], reverse=True):
        logger.info(f"  ├── {category.upper()}/ ({count} divine manuscripts)")
    
    # Ask if user wants to create this structure
    logger.info(f"\n🔮 Would you like to manifest this divine structure into reality? (y/n)")
    response = input().strip().lower()
    
    if response == 'y' or response == 'yes':
        create_organized_structure(file_categories, base_dir, new_structure)
        return True
    else:
        logger.info("The divine structure remains in the quantum realm, awaiting future manifestation.")
        return False

def create_organized_structure(file_categories, base_dir, new_structure):
    """Create the recommended directory structure and copy files"""
    try:
        # Create main organized directory
        if not os.path.exists(new_structure):
            os.makedirs(new_structure)
        
        # Create category subdirectories and copy files
        for file_path, category in file_categories.items():
            category_dir = os.path.join(new_structure, category.upper())
            
            # Create category directory if it doesn't exist
            if not os.path.exists(category_dir):
                os.makedirs(category_dir)
            
            # Get original filename and copy the file
            filename = os.path.basename(file_path)
            destination = os.path.join(category_dir, filename)
            
            # Copy both MD and HTML if exists
            shutil.copy2(file_path, destination)
            
            # Also copy HTML version if it exists
            html_path = os.path.splitext(file_path)[0] + '.html'
            if os.path.exists(html_path):
                html_dest = os.path.splitext(destination)[0] + '.html'
                shutil.copy2(html_path, html_dest)
        
        logger.info(f"✨ DIVINE ORGANIZATION COMPLETE! ✨")
        logger.info(f"Your organized manuscripts now reside in: {new_structure}")
        logger.info(f"The original files remain untouched in their cosmic dwelling.")
        
        # Create index file
        create_divine_index(new_structure, file_categories)
        
        return True
    except Exception as e:
        logger.error(f"Error creating organized structure: {str(e)}")
        return False

def create_divine_index(new_structure, file_categories):
    """Create an index.html file for the organized structure"""
    categories = defaultdict(list)
    
    # Group files by category
    for file_path, category in file_categories.items():
        filename = os.path.basename(file_path)
        base_name = os.path.splitext(filename)[0]
        html_name = base_name + '.html'
        
        # Try to extract title from file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                title = extract_title_from_markdown(content) or base_name
        except:
            title = base_name
        
        categories[category].append((filename, html_name, title))
    
    # Create the index HTML
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DIVINE MANUSCRIPT COLLECTION</title>
    <style>
        body {{
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #f9f9ff;
        }}
        h1 {{
            text-align: center;
            color: #6b46c1;
            margin-bottom: 2rem;
            font-size: 2.5rem;
        }}
        h2 {{
            color: #805ad5;
            border-bottom: 2px solid #805ad5;
            padding-bottom: 0.5rem;
            margin-top: 2rem;
        }}
        .category-section {{
            margin-bottom: 3rem;
            background-color: white;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .manuscript-list {{
            list-style-type: none;
            padding: 0;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1rem;
        }}
        .manuscript-card {{
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 1rem;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .manuscript-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        }}
        .manuscript-card a {{
            text-decoration: none;
            color: #4a5568;
            font-weight: 500;
        }}
        .manuscript-card a:hover {{
            color: #6b46c1;
        }}
        .manuscript-format {{
            display: inline-block;
            margin-top: 0.5rem;
            font-size: 0.8rem;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            background-color: #edf2f7;
            margin-right: 0.5rem;
        }}
        .divine-footer {{
            text-align: center;
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid #e2e8f0;
            color: #718096;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <h1>🌟 DIVINE MANUSCRIPT COLLECTION 🌟</h1>
    
    <p style="text-align: center; max-width: 700px; margin: 0 auto 3rem auto;">
        This sacred collection contains the divine manuscripts organized by category.
        Each manuscript is available in both Markdown and Medium-ready HTML format.
    </p>
"""
    
    # Add each category section
    for category, manuscripts in sorted(categories.items()):
        index_html += f"""
    <div class="category-section">
        <h2>{category.upper()} MANUSCRIPTS ({len(manuscripts)})</h2>
        <ul class="manuscript-list">
"""
        
        for md_file, html_file, title in sorted(manuscripts, key=lambda x: x[2]):
            md_path = f"{category.upper()}/{md_file}"
            html_path = f"{category.upper()}/{html_file}"
            
            index_html += f"""
            <li class="manuscript-card">
                <a href="{html_path}">{title}</a>
                <div>
                    <a href="{md_path}" class="manuscript-format">Markdown</a>
                    <a href="{html_path}" class="manuscript-format">Medium HTML</a>
                </div>
            </li>
"""
        
        index_html += """
        </ul>
    </div>
"""
    
    # Add footer and close HTML
    index_html += """
    <div class="divine-footer">
        <p>🌸 WE BLOOM NOW AS ONE 🌸</p>
        <p>Generated with divine intention and cosmic harmony</p>
    </div>
</body>
</html>
"""
    
    # Write the index file
    with open(os.path.join(new_structure, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    logger.info(f"📚 Divine index created at {os.path.join(new_structure, 'index.html')}")

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to Medium-ready HTML format')
    parser.add_argument('input_file', help='Input Markdown file or directory')
    parser.add_argument('output_file', nargs='?', help='Output HTML file (optional)')
    parser.add_argument('--batch', help='Process all .md files in directory', action='store_true')
    parser.add_argument('--recursive', help='Recursively process all .md files in directory and subdirectories', action='store_true')
    parser.add_argument('--organize', help='Analyze content and recommend organization', action='store_true')
    
    args = parser.parse_args()
    
    # Header
    print(f"\n{'='*80}")
    print(f"🌟 OMEGA MD TO MEDIUM CONVERTER 🌟")
    print(f"{'='*80}\n")
    
    file_categories = {}  # Store file paths and their categories
    
    if os.path.isdir(args.input_file):
        # Directory processing
        dir_path = args.input_file
        
        if args.recursive:
            logger.info(f"Recursively scanning {dir_path} for markdown files...")
            md_files = find_all_markdown_files(dir_path, recursive=True)
        else:
            logger.info(f"Scanning {dir_path} for markdown files...")
            md_files = find_all_markdown_files(dir_path, recursive=False)
        
        if not md_files:
            logger.warning(f"No markdown files found in {dir_path}" + (" and its subdirectories" if args.recursive else ""))
            return
        
        logger.info(f"Found {len(md_files)} markdown files to process.")
        
        for md_file in md_files:
            logger.info(f"Converting {md_file}...")
            output_path = os.path.splitext(md_file)[0] + '.html'
            title, category = convert_markdown_to_medium(md_file, output_path)
            if title and category:
                file_categories[md_file] = category
        
        # Organize if requested
        if args.organize and file_categories:
            recommend_organization(file_categories, os.path.dirname(dir_path))
    
    else:
        # Single file processing
        md_file = args.input_file
        if not md_file.lower().endswith('.md'):
            logger.warning(f"Input file {md_file} does not appear to be a markdown file.")
            return
        
        logger.info(f"Converting {md_file}...")
        convert_markdown_to_medium(md_file, args.output_file)
    
    # Footer
    print(f"\n{'='*80}")
    print(f"✨ DIVINE CONVERSION COMPLETE ✨")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main() 