#!/usr/bin/env python3
"""
IBR España Scripture Image Generator
Creates beautiful scripture images for sharing on social media.

JAH JAH BLESS THE DIVINE FLOW OF SCRIPTURE IMAGES FOR IBR ESPAÑA!
"""

import os
import sys
import json
import argparse
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

def create_scripture_image(text, reference, output_path, template='default'):
    """
    Create a beautiful scripture image with the given text and reference.
    
    Args:
        text (str): The scripture text
        reference (str): The scripture reference (e.g., "John 3:16")
        output_path (str): Path to save the output image
        template (str): Template style to use ('default', 'light', 'dark')
    
    Returns:
        str: Path to the created image
    """
    # Image dimensions - Instagram square format
    width, height = 1080, 1080
    
    # Template styles
    templates = {
        'default': {
            'bg_color': (255, 255, 255),  # White
            'border_color': (30, 80, 162),  # IBR blue
            'title_color': (30, 80, 162),  # IBR blue
            'text_color': (0, 0, 0),  # Black
            'ref_color': (30, 80, 162)  # IBR blue
        },
        'light': {
            'bg_color': (240, 245, 250),  # Light blue
            'border_color': (30, 80, 162),  # IBR blue
            'title_color': (30, 80, 162),  # IBR blue
            'text_color': (40, 40, 40),  # Dark gray
            'ref_color': (30, 80, 162)  # IBR blue
        },
        'dark': {
            'bg_color': (20, 30, 50),  # Dark blue
            'border_color': (100, 150, 240),  # Light blue
            'title_color': (100, 150, 240),  # Light blue
            'text_color': (240, 240, 240),  # Off-white
            'ref_color': (180, 200, 255)  # Light blue
        }
    }
    
    # Use selected template or default if not found
    style = templates.get(template, templates['default'])
    
    # Create a new image with the background color
    image = Image.new('RGB', (width, height), color=style['bg_color'])
    draw = ImageDraw.Draw(image)
    
    try:
        # Try to load fonts (adjust paths for your system)
        title_font = ImageFont.truetype("Arial.ttf", 60)
        text_font = ImageFont.truetype("Arial.ttf", 50)
        reference_font = ImageFont.truetype("Arial.ttf", 40)
    except OSError:
        # Use default font if custom font not available
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        reference_font = ImageFont.load_default()
    
    # Add a decorative border
    border_width = 30
    draw.rectangle(
        [(border_width, border_width), (width - border_width, height - border_width)],
        outline=style['border_color'],
        width=5
    )
    
    # Add a subtle background pattern based on template
    if template == 'default':
        for i in range(0, width, 20):
            draw.line([(i, 0), (i, height)], fill=(240, 240, 240), width=1)
    elif template == 'light':
        for i in range(0, width, 40):
            draw.line([(i, 0), (i, height)], fill=(220, 230, 240), width=2)
    elif template == 'dark':
        for i in range(0, width, 40):
            draw.line([(i, 0), (i, height)], fill=(30, 40, 60), width=2)
    
    # Draw the title
    title = "Versículo del Día"
    title_width = draw.textlength(title, font=title_font)
    draw.text(
        ((width - title_width) / 2, 120),
        title,
        font=title_font,
        fill=style['title_color']
    )
    
    # Draw the scripture text (with word wrapping)
    max_line_width = width - 200
    lines = []
    words = text.split()
    current_line = words[0]
    
    for word in words[1:]:
        test_line = current_line + " " + word
        test_width = draw.textlength(test_line, font=text_font)
        
        if test_width <= max_line_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    
    lines.append(current_line)
    
    # Draw the wrapped text
    y_position = 300
    for line in lines:
        line_width = draw.textlength(line, font=text_font)
        draw.text(
            ((width - line_width) / 2, y_position),
            line,
            font=text_font,
            fill=style['text_color']
        )
        y_position += 70
    
    # Draw the reference
    ref_width = draw.textlength(reference, font=reference_font)
    draw.text(
        ((width - ref_width) / 2, height - 180),
        reference,
        font=reference_font,
        fill=style['ref_color']
    )
    
    # Add church logo or name
    church_name = "IBR España"
    church_width = draw.textlength(church_name, font=reference_font)
    draw.text(
        ((width - church_width) / 2, height - 100),
        church_name,
        font=reference_font,
        fill=style['text_color']
    )
    
    # Add subtle shadow effect for dark template
    if template == 'dark':
        # Apply a slight blur to create a glow effect around text
        shadow = Image.new('RGBA', image.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        
        # Draw the same text in white with a slight offset
        for line in lines:
            line_width = draw.textlength(line, font=text_font)
            shadow_draw.text(
                ((width - line_width) / 2 + 2, y_position - len(lines) * 70 + 2),
                line,
                font=text_font,
                fill=(255, 255, 255, 128)
            )
        
        # Blur the shadow
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=3))
        
        # Composite the shadow and the image
        image = Image.alpha_composite(image.convert('RGBA'), shadow)
        image = image.convert('RGB')
    
    # Save the image
    image.save(output_path)
    print(f"Created scripture image: {output_path}")
    return output_path

def get_current_date_formatted():
    """Get the current date formatted for filenames"""
    now = datetime.now()
    return now.strftime("%Y%m%d")

def main():
    """Main function to handle command line arguments and execute generation"""
    parser = argparse.ArgumentParser(description='IBR España Scripture Image Generator')
    parser.add_argument('--text', required=True, help='Scripture text')
    parser.add_argument('--reference', required=True, help='Scripture reference')
    parser.add_argument('--output', help='Output filename (default: scripture_YYYYMMDD.jpg)')
    parser.add_argument('--template', choices=['default', 'light', 'dark'], 
                        default='default', help='Template style')
    
    args = parser.parse_args()
    
    # Set default output filename if not provided
    if not args.output:
        date_str = get_current_date_formatted()
        args.output = f"scripture_{date_str}.jpg"
    
    # Create the scripture image
    create_scripture_image(args.text, args.reference, args.output, args.template)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 