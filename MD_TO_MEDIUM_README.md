# Markdown to Medium Converter

A Python utility that converts Markdown files to Medium-ready HTML format, with advanced organization features for large document collections.

## Features

- Converts Markdown to HTML optimized for Medium
- Preserves code blocks with language syntax highlighting
- Formats images with captions
- Properly styles headers, lists, and blockquotes
- Maintains table formatting
- Supports batch processing of multiple markdown files
- Includes Medium-friendly CSS styling
- **NEW**: Recursively scans directories for Markdown files
- **NEW**: Smart content analysis and categorization
- **NEW**: Organizes content into a structured directory
- **NEW**: Generates a beautiful index.html for organized content

## Requirements

- Python 3.6+
- markdown library
- beautifulsoup4 library

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install markdown beautifulsoup4
```

3. Make the script executable (optional):

```bash
chmod +x md_to_medium.py
```

## Usage

### Convert a single Markdown file

```bash
python md_to_medium.py input.md [output.html]
```

If you don't specify an output file, the script will use the input filename with an .html extension.

### Batch convert all Markdown files in a directory

```bash
python md_to_medium.py directory_path/ --batch
```

This will convert all .md files in the specified directory, creating corresponding .html files.

### Recursively scan and convert Markdown files

```bash
python md_to_medium.py directory_path/ --recursive
```

Scans the specified directory and all subdirectories for Markdown files and converts them to Medium-ready HTML.

### Analyze and organize content by category

```bash
python md_to_medium.py directory_path/ --recursive --organize
```

This will:

1. Recursively scan the directory for Markdown files
2. Convert them to Medium-ready HTML
3. Analyze the content to determine the most appropriate category
4. Recommend a new organizational structure
5. If approved, create the new structure and copy all files
6. Generate an index.html file to browse the organized content

## Content Categories

The script analyzes content and organizes files into these categories:

- **Quantum**: Content related to quantum computing, qubits, entanglement
- **Divine**: Spiritual, sacred, blessing, or ritual content
- **Cosmic**: Content about cosmic patterns, matrix systems, oracles
- **Technical**: Deployment, architecture, infrastructure, Kubernetes, Docker
- **Trading**: Content about trading, markets, prices, cryptocurrency, positions
- **Documentation**: Manuals, guides, readme files, catalogs, installation instructions
- **Uncategorized**: Content that doesn't match any specific category

## Medium Import Instructions

After converting your Markdown file(s), you can import the content to Medium:

1. Open the generated HTML file in a web browser
2. Copy everything below the yellow instructions box
3. In Medium, click on your profile picture and select "Stories"
4. Click "Import a story"
5. Paste the copied content into a new Medium story

Alternatively, if you host the HTML file on a web server:

1. In Medium, click on your profile picture and select "Stories"
2. Click "Import a story"
3. Enter the URL where your HTML file is hosted

## Customization

The script includes CSS styling that mimics Medium's appearance. You can customize the styling by modifying the `MEDIUM_CSS` variable in the script.

## Advanced Features

### Code Block Language Support

The script automatically detects language specifications in code blocks and adds appropriate syntax highlighting indicators for Medium.

Example markdown:

```markdown
```python
def hello_world():
    print("Hello, Medium!")
```

```

This will be converted to HTML with language indicators that Medium can interpret.

### Image Captions

To add captions to images, use the alt text attribute in your Markdown:

```markdown
![This is the caption for the image](path/to/image.jpg)
```

The script will convert this to HTML with proper `<figure>` and `<figcaption>` tags.

### Smart Directory Organization

When using the `--organize` flag, the script creates a new directory structure with:

- A main directory named "BOOK_ORGANIZED_[timestamp]"
- Subdirectories for each content category
- Files copied to their appropriate category directories
- An index.html file that provides easy navigation of all content
- Both the original Markdown and converted HTML files preserved

## Troubleshooting

If you encounter any issues:

- Make sure you have all the required dependencies installed
- Check that your Markdown syntax is valid
- For complex Markdown features, review the generated HTML to ensure proper conversion
- If organizing content, ensure you have write permissions in the parent directory

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The Python Markdown library
- BeautifulSoup for HTML parsing and manipulation
