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
Discord Matrix Bot Setup Script

This script helps users quickly set up and configure the BitGet Matrix Bot
for Discord integration.
"""

import os
import sys
import shutil
import getpass
import subprocess
from pathlib import Path
import urllib.request
import dotenv

def print_header():
    """Print a stylish ASCII header."""
    header = """
    ╔══════════════════════════════════════════════════════════════╗
    ║   _____  ___ ___  _____ _____ ___    ___ _____ _____ ___    ║
    ║  |     || . | . ||     |_   _|  _|  |  _|  _  |_   _|   |   ║
    ║  | | | || . | . || | | | | | |  _|  | |_|     | | | | | |   ║
    ║  |_|_|_||___|___||_|_|_| |_| |_|    |___|__|__| |_| |___|   ║
    ║                                                              ║
    ║   DISCORD INTEGRATION SETUP - CYBERPUNK MATRIX EDITION       ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(header)

def check_prerequisites():
    """Check for required tools and prerequisites."""
    print("📋 Checking prerequisites...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("⚠️  Warning: Python 3.8+ is recommended. You're running:", sys.version)
    else:
        print("✅ Python version:", sys.version)

    # Check for pip
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("✅ pip is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ pip not found - please install pip first")
        return False
        
    # Try to import required packages
    required_packages = ['discord', 'colorama', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print("\nInstalling missing packages...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages, check=True)
            print("✅ All required packages installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please install them manually:")
            print(f"   pip install {' '.join(missing_packages)}")
            return False
    
    return True

def setup_env_file():
    """Set up the .env file with Discord token."""
    print("\n🔑 Setting up environment configuration...")
    
    env_path = Path('.env')
    if env_path.exists():
        print("Found existing .env file.")
        update = input("Do you want to update it? (y/n): ").lower() == 'y'
        if not update:
            return True
    
    # Get Discord token from user
    print("\nYou need a Discord Bot Token to continue.")
    print("Instructions to get one:")
    print("1. Go to https://discord.com/developers/applications")
    print("2. Create a 'New Application' and go to the Bot section")
    print("3. Click 'Add Bot' and then copy the token")
    
    token = getpass.getpass("\nEnter your Discord bot token (input will be hidden): ")
    if not token:
        print("❌ No token provided. Setup cannot continue.")
        return False
    
    # Create or update .env file
    dotenv.set_key(env_path, "DISCORD_TOKEN", token)
    print("✅ Discord token saved to .env file")
    
    # Optional: BitGet API credentials
    add_bitget = input("\nDo you want to add BitGet API credentials? (y/n): ").lower() == 'y'
    if add_bitget:
        api_key = getpass.getpass("Enter BitGet API Key: ")
        api_secret = getpass.getpass("Enter BitGet API Secret: ")
        api_passphrase = getpass.getpass("Enter BitGet API Passphrase: ")
        
        if api_key and api_secret and api_passphrase:
            dotenv.set_key(env_path, "BITGET_API_KEY", api_key)
            dotenv.set_key(env_path, "BITGET_API_SECRET", api_secret)
            dotenv.set_key(env_path, "BITGET_API_PASSPHRASE", api_passphrase)
            print("✅ BitGet API credentials saved to .env file")
        else:
            print("⚠️  Some BitGet credentials were not provided. Using mock data instead.")
    
    return True

def generate_discord_invite_link():
    """Generate a Discord bot invite link."""
    print("\n🔗 Generating Discord bot invite link...")
    
    client_id = input("Enter your Discord Application Client ID: ")
    if not client_id:
        print("❌ No Client ID provided. Cannot generate invite link.")
        return
    
    permissions = 2147608640  # Includes essential bot permissions
    
    invite_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions={permissions}&scope=bot%20applications.commands"
    
    print("\n✅ Your bot invite link is ready:")
    print(f"{invite_url}")
    print("\nOpen this link in your browser to add the bot to your server.")

def setup_complete():
    """Display completion message and instructions to run the bot."""
    print("\n🎉 Setup Complete! 🎉")
    print("\nTo run your Discord Matrix Bot, use this command:")
    print("python -m src.omega_bot_farm.discord.bot")
    
    print("\nAvailable commands in Discord:")
    print("- /matrix-positions  - Show BitGet positions with Matrix visualization")
    print("- /matrix-account    - Show account overview with Matrix styling")
    print("- /matrix-snapshot   - Take a snapshot of positions with cyberpunk styling")
    
    print("\n🌐 For more information, check the documentation at:")
    print("src/omega_bot_farm/README.md")
    
    print("\n🧬 CH33RS TO THE B0TS! 🧬")

def main():
    """Main setup function."""
    print_header()
    
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed. Please fix the issues and try again.")
        return
    
    if not setup_env_file():
        print("\n❌ Environment setup failed. Please try again.")
        return
    
    generate_discord_invite_link()
    setup_complete()

if __name__ == "__main__":
    main() 