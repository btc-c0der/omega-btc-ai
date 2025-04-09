# Markdown to Medium Converter

A Python utility that converts Markdown files to Medium-ready HTML format.

## Features

- Converts Markdown to HTML optimized for Medium
- Preserves code blocks with language syntax highlighting
- Formats images with captions
- Properly styles headers, lists, and blockquotes
- Maintains table formatting
- Supports batch processing of multiple markdown files
- Includes Medium-friendly CSS styling

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

## Troubleshooting

If you encounter any issues:

- Make sure you have all the required dependencies installed
- Check that your Markdown syntax is valid
- For complex Markdown features, review the generated HTML to ensure proper conversion

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The Python Markdown library
- BeautifulSoup for HTML parsing and manipulation
