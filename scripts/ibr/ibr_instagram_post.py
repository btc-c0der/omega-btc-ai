#!/usr/bin/env python3
"""
IBR España Instagram Automation Script
This script automates posting content to the @ibrespana Instagram account.

JAH JAH BLESS THE DIVINE FLOW OF CONTENT TO IBR ESPAÑA!
"""

import os
import sys
import time
import argparse
import json
import logging
from datetime import datetime
from textwrap import dedent

try:
    from instagrapi import Client
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Required packages not found. Install with:")
    print("pip install instagrapi pillow")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ibr_instagram.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ibr_instagram")

# Content templates for different post types
TEMPLATES = {
    'sermon': dedent("""\
        {title}
        
        {scripture_ref}
        
        "{scripture_text}"
        
        {description}
        
        #IBREspaña #IGlesiaReformada #Barcelona #Catalonia
    """),
    
    'event': dedent("""\
        {title}
        
        {date_formatted}
        {location}
        
        {description}
        
        #IBREspaña #Barcelona #Evento
    """),
    
    'scripture': dedent("""\
        Versículo del día:
        
        "{text}"
        
        {reference}
        
        #VersiculoDelDia #IBREspaña #Biblia
    """),
}

def login_to_instagram(username, password):
    """Login to Instagram using provided credentials"""
    logger.info(f"Logging in as {username}")
    client = Client()
    
    try:
        client.login(username, password)
        logger.info("Login successful")
        return client
    except Exception as e:
        logger.error(f"Login failed: {e}")
        return None

def create_scripture_image(text, reference, output_path):
    """Create a scripture image with text and reference"""
    # Image dimensions
    width, height = 1080, 1080
    
    # Create a new image with white background
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
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
        outline=(30, 80, 162),  # IBR blue
        width=5
    )
    
    # Add a subtle background pattern
    for i in range(0, width, 20):
        draw.line([(i, 0), (i, height)], fill=(240, 240, 240), width=1)
    
    # Draw the title
    title = "Versículo del Día"
    title_width = draw.textlength(title, font=title_font)
    draw.text(
        ((width - title_width) / 2, 120),
        title,
        font=title_font,
        fill=(30, 80, 162)  # IBR blue
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
            fill=(0, 0, 0)
        )
        y_position += 70
    
    # Draw the reference
    ref_width = draw.textlength(reference, font=reference_font)
    draw.text(
        ((width - ref_width) / 2, height - 180),
        reference,
        font=reference_font,
        fill=(30, 80, 162)  # IBR blue
    )
    
    # Add church logo or name
    church_name = "IBR España"
    church_width = draw.textlength(church_name, font=reference_font)
    draw.text(
        ((width - church_width) / 2, height - 100),
        church_name,
        font=reference_font,
        fill=(0, 0, 0)
    )
    
    # Save the image
    image.save(output_path)
    logger.info(f"Created scripture image: {output_path}")
    return output_path

def post_to_instagram(client, post_type, content, image_path=None):
    """Post content to Instagram based on post type"""
    if post_type not in TEMPLATES:
        logger.error(f"Unknown post type: {post_type}")
        return False
    
    # Format the caption based on the template and content
    caption = TEMPLATES[post_type].format(**content)
    
    if image_path:
        # Image post
        try:
            if os.path.exists(image_path):
                logger.info(f"Uploading image: {image_path}")
                media = client.photo_upload(
                    image_path,
                    caption=caption
                )
                logger.info(f"Posted successfully with ID: {media.id}")
                return True
            else:
                logger.error(f"Image file not found: {image_path}")
                return False
        except Exception as e:
            logger.error(f"Failed to upload image: {e}")
            return False
    else:
        # Text-only post (not supported by Instagram, need at least an image)
        logger.error("Instagram requires at least an image for posting")
        return False

def post_scripture(client, text, reference):
    """Post a scripture verse to Instagram"""
    # Create content dictionary
    content = {
        'text': text,
        'reference': reference
    }
    
    # Create a scripture image
    temp_image_path = "temp_scripture.jpg"
    create_scripture_image(text, reference, temp_image_path)
    
    # Post to Instagram
    result = post_to_instagram(client, 'scripture', content, temp_image_path)
    
    # Clean up
    if os.path.exists(temp_image_path):
        os.remove(temp_image_path)
    
    return result

def main():
    """Main function to handle command line arguments and execute posting"""
    parser = argparse.ArgumentParser(description='IBR España Instagram Posting Tool')
    parser.add_argument('--username', help='Instagram username')
    parser.add_argument('--password', help='Instagram password')
    parser.add_argument('--config', help='Path to config file with credentials')
    parser.add_argument('--type', choices=['sermon', 'event', 'scripture'], 
                        help='Type of content to post')
    parser.add_argument('--content', help='Path to JSON file with content')
    parser.add_argument('--image', help='Path to image file to upload')
    
    args = parser.parse_args()
    
    # Load credentials
    username = args.username
    password = args.password
    
    if args.config:
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)
                username = config.get('username', username)
                password = config.get('password', password)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
    
    if not username or not password:
        logger.error("Username and password are required")
        return 1
    
    # Login to Instagram
    client = login_to_instagram(username, password)
    if not client:
        return 1
    
    # Load content
    if args.content:
        try:
            with open(args.content, 'r') as f:
                content = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load content: {e}")
            return 1
    else:
        content = {}
    
    # Post based on type
    if args.type == 'scripture':
        if 'text' in content and 'reference' in content:
            if post_scripture(client, content['text'], content['reference']):
                logger.info("Scripture posted successfully")
                return 0
        else:
            logger.error("Scripture content must include 'text' and 'reference'")
    elif args.image and args.type in ['sermon', 'event']:
        if post_to_instagram(client, args.type, content, args.image):
            logger.info(f"{args.type.capitalize()} posted successfully")
            return 0
    else:
        logger.error("Invalid combination of arguments")
    
    return 1

if __name__ == "__main__":
    sys.exit(main()) 