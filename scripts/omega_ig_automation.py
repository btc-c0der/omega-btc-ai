#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔱 OMEGA BTC AI - Divine Instagram Automation 🔱

This script automates the creation and posting of content to Instagram
for the OMEGA BTC AI project, including image generation, caption creation,
hashtag optimization, and posting scheduling.

JAH JAH BLESS THE DIVINE SOCIAL FLOW!

Copyright (C) 2024 OMEGA BTC AI Team
License: GNU General Public License v3.0
"""

import os
import sys
import time
import json
import random
import argparse
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union

# Third-party imports (install via requirements.txt)
try:
    import requests
    from PIL import Image, ImageDraw, ImageFont
    from instagrapi import Client
    from instagrapi.exceptions import ClientError, ClientLoginRequired
except ImportError as e:
    print(f"Error: Missing required package - {e}")
    print("Please install required packages: pip install requests pillow instagrapi")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("omega_ig_automation.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("omega_ig_automation")

# ANSI color codes for divine terminal output
COLORS = {
    "GOLD": "\033[38;5;220m",
    "CYAN": "\033[36m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "RED": "\033[31m",
    "RESET": "\033[0m",
    "BOLD": "\033[1m"
}

# Instagram credentials and configuration
class InstagramConfig:
    """Configuration for Instagram API access and posting settings."""
    
    def __init__(self, config_file: str = "config/instagram_config.json"):
        """Initialize Instagram configuration from a JSON file."""
        self.username = ""
        self.password = ""
        self.session_file = "ig_session.json"
        self.post_frequency = 24  # hours
        self.best_times = ["08:00", "12:00", "17:00", "20:00"]
        self.hashtags = []
        self.caption_templates = []
        
        if os.path.exists(config_file):
            self._load_config(config_file)
        else:
            logger.warning(f"Config file {config_file} not found, using defaults")
            self._create_default_config(config_file)
    
    def _load_config(self, config_file: str) -> None:
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                
            self.username = config.get("username", "")
            self.password = config.get("password", "")
            self.session_file = config.get("session_file", "ig_session.json")
            self.post_frequency = config.get("post_frequency", 24)
            self.best_times = config.get("best_times", ["08:00", "12:00", "17:00", "20:00"])
            self.hashtags = config.get("hashtags", [])
            self.caption_templates = config.get("caption_templates", [])
            
            logger.info("Instagram configuration loaded successfully")
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            raise
    
    def _create_default_config(self, config_file: str) -> None:
        """Create a default configuration file."""
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        
        default_config = {
            "username": "YOUR_INSTAGRAM_USERNAME",
            "password": "YOUR_INSTAGRAM_PASSWORD",
            "session_file": "ig_session.json",
            "post_frequency": 24,
            "best_times": ["08:00", "12:00", "17:00", "20:00"],
            "hashtags": [
                "#OMEGABTCAI", "#BTC", "#Bitcoin", "#Trading", "#TradingBot", 
                "#CryptoTrading", "#AITrading", "#QuantTrading", "#AlgoTrading",
                "#BitcoinTrading", "#CryptoBot", "#TradingAlgorithm", "#HODL"
            ],
            "caption_templates": [
                "🔱 OMEGA BTC AI divine market insights for {date} 🔱\n\n{market_summary}\n\nJAH JAH BLESS THE DIVINE FLOW! 🔱",
                "⚡️ Bitcoin market update from OMEGA AI - {date} ⚡️\n\n{market_summary}\n\nFollow for daily divine insights! 🔱",
                "🧠 OMEGA AI analysis for {date}:\n\n{market_summary}\n\nTrust the divine flow! 🔱"
            ]
        }
        
        try:
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            
            logger.info(f"Created default configuration at {config_file}")
            logger.warning("Please edit the configuration with your credentials")
        except Exception as e:
            logger.error(f"Error creating default config: {e}")
            raise

# Content Generator
class ContentGenerator:
    """Generates Instagram content including images and captions."""
    
    def __init__(self, config: InstagramConfig):
        """Initialize content generator with configuration."""
        self.config = config
        self.image_dir = "content/images"
        self.font_path = "assets/fonts/Montserrat-Bold.ttf"
        
        # Create directories if they don't exist
        os.makedirs(self.image_dir, exist_ok=True)
        os.makedirs("assets/fonts", exist_ok=True)
        
        # Download font if it doesn't exist
        if not os.path.exists(self.font_path):
            self._download_font()
    
    def _download_font(self) -> None:
        """Download Montserrat font for image generation."""
        font_url = "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Bold.ttf"
        try:
            response = requests.get(font_url)
            response.raise_for_status()
            
            os.makedirs(os.path.dirname(self.font_path), exist_ok=True)
            with open(self.font_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Font downloaded to {self.font_path}")
        except Exception as e:
            logger.error(f"Error downloading font: {e}")
            # Use system font as fallback
            self.font_path = None
    
    def _get_market_data(self) -> Dict[str, Union[str, float]]:
        """Get current Bitcoin market data."""
        try:
            response = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin")
            response.raise_for_status()
            data = response.json()
            
            price = data["market_data"]["current_price"]["usd"]
            price_change_24h = data["market_data"]["price_change_percentage_24h"]
            market_cap = data["market_data"]["market_cap"]["usd"]
            volume = data["market_data"]["total_volume"]["usd"]
            
            if price_change_24h > 3:
                sentiment = "bullish 📈"
            elif price_change_24h < -3:
                sentiment = "bearish 📉"
            else:
                sentiment = "neutral ⚖️"
            
            return {
                "price": price,
                "price_change_24h": price_change_24h,
                "market_cap": market_cap,
                "volume": volume,
                "sentiment": sentiment
            }
        except Exception as e:
            logger.error(f"Error fetching market data: {e}")
            # Return fallback data
            return {
                "price": 60000,
                "price_change_24h": 0.5,
                "market_cap": 1200000000000,
                "volume": 45000000000,
                "sentiment": "neutral ⚖️"
            }
    
    def generate_image(self) -> str:
        """Generate an image for Instagram posting."""
        market_data = self._get_market_data()
        
        # Create image
        width, height = 1080, 1080
        image = Image.new('RGB', (width, height), color=(10, 12, 20))
        draw = ImageDraw.Draw(image)
        
        # Try to use downloaded font, fall back to default
        try:
            title_font = ImageFont.truetype(self.font_path, 60) if self.font_path else ImageFont.load_default()
            price_font = ImageFont.truetype(self.font_path, 80) if self.font_path else ImageFont.load_default()
            info_font = ImageFont.truetype(self.font_path, 40) if self.font_path else ImageFont.load_default()
        except Exception:
            title_font = ImageFont.load_default()
            price_font = ImageFont.load_default()
            info_font = ImageFont.load_default()
        
        # Draw title
        draw.text((width//2, 120), "OMEGA BTC AI", 
                  fill=(218, 165, 32), font=title_font, anchor="mm")
        
        # Draw divider
        draw.line([(width//4, 180), (width*3//4, 180)], fill=(218, 165, 32), width=3)
        
        # Draw price
        price_text = f"${market_data['price']:,.0f}"
        draw.text((width//2, height//2-50), price_text, 
                  fill=(255, 255, 255), font=price_font, anchor="mm")
        
        # Draw price change
        change_color = (46, 204, 113) if market_data['price_change_24h'] >= 0 else (231, 76, 60)
        change_text = f"{market_data['price_change_24h']:+.2f}% (24h)"
        draw.text((width//2, height//2+50), change_text, 
                  fill=change_color, font=info_font, anchor="mm")
        
        # Draw sentiment
        draw.text((width//2, height//2+130), f"Market: {market_data['sentiment']}", 
                  fill=(200, 200, 200), font=info_font, anchor="mm")
        
        # Draw date
        current_date = datetime.now().strftime("%Y-%m-%d")
        draw.text((width//2, height-150), current_date, 
                  fill=(150, 150, 150), font=info_font, anchor="mm")
        
        # Draw watermark
        draw.text((width//2, height-80), "JAH JAH BLESS THE DIVINE FLOW! 🔱", 
                  fill=(218, 165, 32), font=info_font, anchor="mm")
        
        # Save image
        filename = f"{self.image_dir}/omega_btc_{current_date.replace('-', '')}.jpg"
        image.save(filename, quality=95)
        logger.info(f"Generated image: {filename}")
        
        return filename
    
    def generate_caption(self) -> str:
        """Generate a caption for the Instagram post."""
        market_data = self._get_market_data()
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Create market summary
        market_summary = (
            f"Current BTC price: ${market_data['price']:,.0f}\n"
            f"24h change: {market_data['price_change_24h']:+.2f}%\n"
            f"Market sentiment: {market_data['sentiment']}\n\n"
            f"OMEGA AI is watching the markets 24/7, providing divine trading insights based on our proprietary algorithms. "
            f"Our systems are showing a {market_data['sentiment']} trend for BTC."
        )
        
        # Select random caption template and format it
        template = random.choice(self.config.caption_templates)
        caption = template.format(date=current_date, market_summary=market_summary)
        
        # Add hashtags
        random.shuffle(self.config.hashtags)
        selected_hashtags = self.config.hashtags[:15]  # Instagram allows 30, but we'll use 15
        hashtags_text = " ".join(selected_hashtags)
        
        full_caption = f"{caption}\n\n{hashtags_text}"
        logger.info(f"Generated caption with {len(selected_hashtags)} hashtags")
        
        return full_caption

# Instagram Manager
class InstagramManager:
    """Manages Instagram login and posting."""
    
    def __init__(self, config: InstagramConfig):
        """Initialize Instagram client with configuration."""
        self.config = config
        self.client = Client()
        self.logged_in = False
    
    def login(self) -> bool:
        """Log in to Instagram."""
        if not self.config.username or not self.config.password:
            logger.error("Instagram username or password not configured")
            return False
        
        try:
            # Try to load session
            if os.path.exists(self.config.session_file):
                self.client.load_settings(self.config.session_file)
                self.client.get_timeline_feed()  # Test if session is valid
                logger.info("Loaded existing Instagram session")
                self.logged_in = True
                return True
        except (ClientError, ClientLoginRequired) as e:
            logger.warning(f"Session loading failed: {e}")
        
        # Login with username and password if session loading failed
        try:
            self.client.login(self.config.username, self.config.password)
            self.client.dump_settings(self.config.session_file)
            logger.info("Logged in to Instagram successfully")
            self.logged_in = True
            return True
        except Exception as e:
            logger.error(f"Instagram login failed: {e}")
            return False
    
    def post_image(self, image_path: str, caption: str) -> bool:
        """Post an image to Instagram."""
        if not self.logged_in:
            if not self.login():
                return False
        
        try:
            media = self.client.photo_upload(image_path, caption)
            logger.info(f"Successfully posted to Instagram with media ID: {media.id}")
            return True
        except Exception as e:
            logger.error(f"Failed to post to Instagram: {e}")
            return False
    
    def get_next_post_time(self) -> datetime:
        """Calculate the next optimal posting time."""
        now = datetime.now()
        best_hours = []
        
        # Convert time strings to hours
        for time_str in self.config.best_times:
            try:
                hour, minute = map(int, time_str.split(':'))
                best_hours.append(hour)
            except:
                continue
        
        if not best_hours:
            best_hours = [9, 12, 18, 21]  # Default times if none valid
        
        # Find the next best hour
        current_hour = now.hour
        next_hours = [h for h in best_hours if h > current_hour]
        
        if next_hours:
            # Post later today
            next_hour = min(next_hours)
            next_time = now.replace(hour=next_hour, minute=0, second=0, microsecond=0)
        else:
            # Post tomorrow
            next_hour = min(best_hours)
            next_time = now.replace(hour=next_hour, minute=0, second=0, microsecond=0) + timedelta(days=1)
        
        return next_time

# Automation Controller
class AutomationController:
    """Controls the overall automation workflow."""
    
    def __init__(self, config_file: str = "config/instagram_config.json"):
        """Initialize the automation controller."""
        self.config = InstagramConfig(config_file)
        self.content_generator = ContentGenerator(self.config)
        self.instagram = InstagramManager(self.config)
    
    def post_now(self) -> bool:
        """Generate content and post immediately."""
        print(f"{COLORS['GOLD']}🔱 OMEGA BTC AI - Divine Instagram Automation 🔱{COLORS['RESET']}")
        print(f"{COLORS['CYAN']}Generating divine Instagram content...{COLORS['RESET']}")
        
        image_path = self.content_generator.generate_image()
        caption = self.content_generator.generate_caption()
        
        print(f"{COLORS['GREEN']}✅ Content created successfully{COLORS['RESET']}")
        print(f"{COLORS['CYAN']}Posting to Instagram...{COLORS['RESET']}")
        
        result = self.instagram.post_image(image_path, caption)
        
        if result:
            print(f"{COLORS['GREEN']}✅ Posted successfully to Instagram!{COLORS['RESET']}")
            return True
        else:
            print(f"{COLORS['RED']}❌ Failed to post to Instagram{COLORS['RESET']}")
            return False
    
    def schedule_posts(self, days: int = 7) -> None:
        """Schedule posts for a certain number of days."""
        if not self.instagram.login():
            print(f"{COLORS['RED']}❌ Instagram login failed. Check credentials.{COLORS['RESET']}")
            return
        
        print(f"{COLORS['GOLD']}🔱 OMEGA BTC AI - Divine Instagram Scheduler 🔱{COLORS['RESET']}")
        print(f"{COLORS['CYAN']}Scheduling posts for the next {days} days...{COLORS['RESET']}")
        
        now = datetime.now()
        next_post_time = self.instagram.get_next_post_time()
        
        schedule = []
        for _ in range(days):
            schedule.append(next_post_time)
            next_post_time = next_post_time + timedelta(hours=self.config.post_frequency)
        
        print(f"{COLORS['CYAN']}Scheduled posting times:{COLORS['RESET']}")
        for i, post_time in enumerate(schedule, 1):
            print(f"{COLORS['YELLOW']}  {i}. {post_time.strftime('%Y-%m-%d %H:%M')}{COLORS['RESET']}")
        
        print(f"{COLORS['GREEN']}✅ Posts scheduled. Run with --daemon flag to start the scheduler.{COLORS['RESET']}")
    
    def run_daemon(self) -> None:
        """Run as a daemon, posting at scheduled times."""
        if not self.instagram.login():
            print(f"{COLORS['RED']}❌ Instagram login failed. Check credentials.{COLORS['RESET']}")
            return
        
        print(f"{COLORS['GOLD']}🔱 OMEGA BTC AI - Divine Instagram Daemon 🔱{COLORS['RESET']}")
        print(f"{COLORS['CYAN']}Starting Instagram posting daemon...{COLORS['RESET']}")
        print(f"{COLORS['CYAN']}Posting frequency: Every {self.config.post_frequency} hours{COLORS['RESET']}")
        print(f"{COLORS['CYAN']}Press Ctrl+C to stop{COLORS['RESET']}")
        
        try:
            while True:
                next_post_time = self.instagram.get_next_post_time()
                now = datetime.now()
                wait_seconds = (next_post_time - now).total_seconds()
                
                if wait_seconds <= 0:
                    # Time to post
                    print(f"{COLORS['CYAN']}📌 Posting to Instagram at {now.strftime('%Y-%m-%d %H:%M:%S')}{COLORS['RESET']}")
                    self.post_now()
                    time.sleep(60)  # Wait a minute before calculating next time
                else:
                    # Wait until next post time
                    wait_hours = wait_seconds / 3600
                    print(f"{COLORS['YELLOW']}⏳ Next post in {wait_hours:.2f} hours at {next_post_time.strftime('%Y-%m-%d %H:%M')}{COLORS['RESET']}")
                    
                    # Sleep for a while, then check again
                    time.sleep(min(wait_seconds, 300))  # Sleep at most 5 minutes
        except KeyboardInterrupt:
            print(f"\n{COLORS['YELLOW']}💤 Divine Instagram daemon stopped{COLORS['RESET']}")

# Main function
def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="OMEGA BTC AI - Divine Instagram Automation")
    parser.add_argument("--config", "-c", type=str, default="config/instagram_config.json",
                        help="Path to configuration file")
    parser.add_argument("--post", "-p", action="store_true",
                        help="Generate and post content immediately")
    parser.add_argument("--schedule", "-s", type=int, default=0,
                        help="Schedule posts for specified number of days")
    parser.add_argument("--daemon", "-d", action="store_true",
                        help="Run as a daemon, posting at scheduled times")
    
    args = parser.parse_args()
    
    controller = AutomationController(args.config)
    
    if args.post:
        controller.post_now()
    elif args.schedule > 0:
        controller.schedule_posts(args.schedule)
    elif args.daemon:
        controller.run_daemon()
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 