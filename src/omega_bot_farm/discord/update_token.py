#!/usr/bin/env python3

"""
Discord Token Update Utility

This script helps users update their Discord bot token in the .env file.
"""

import os
import re
import sys
import getpass
from pathlib import Path
from dotenv import load_dotenv, set_key

def print_header():
    """Print a header for the script."""
    print("\n" + "=" * 80)
    print("DISCORD TOKEN UPDATE UTILITY")
    print("=" * 80)
    print("\nThis utility will help you update your Discord bot token in the .env file.\n")

def validate_token(token):
    """
    Validate the token format.
    
    A valid Discord token generally looks like:
    NzkyNzE1NDU0MTk2MDg4ODQy.X-hvzA.Jk2P1PbhCeeY9958qkgWUz78rtQ
    """
    # Very basic validation - should be 3 parts separated by periods
    if not token or len(token) < 50:  # tokens are generally quite long
        return False
        
    parts = token.split('.')
    if len(parts) != 3:
        return False
        
    # First part is typically Base64 (letters, numbers, sometimes -)
    if not re.match(r'^[A-Za-z0-9_-]+$', parts[0]):
        return False
        
    # Second and third parts have a specific format
    if not (re.match(r'^[A-Za-z0-9_-]+$', parts[1]) and re.match(r'^[A-Za-z0-9_-]+$', parts[2])):
        return False
        
    return True

def update_token():
    """Update the Discord token in the .env file."""
    # Find the .env file
    env_path = Path('.env')
    if not env_path.exists():
        print("Error: .env file not found in the current directory.")
        alt_path = Path('src/omega_bot_farm/.env')
        if alt_path.exists():
            env_path = alt_path
            print(f"Using alternate .env file at {alt_path}")
        else:
            print("No .env file found. Please create one.")
            return False
    
    # Load current environment
    load_dotenv(env_path)
    current_token = os.environ.get('DISCORD_TOKEN', '')
    
    # Get the new token
    print("\nPlease enter your Discord bot token (the token will be hidden):")
    print("You can get this from the Discord Developer Portal -> Applications -> Your Bot -> Bot tab")
    new_token = getpass.getpass("Token: ")
    
    # Validate the token
    if not validate_token(new_token):
        print("\nWarning: The token you entered doesn't look like a valid Discord bot token.")
        print("A valid token looks like: NzkyNzE1NDU0MTk2MDg4ODQy.X-hvzA.Jk2P1PbhCeeY9958qkgWUz78rtQ")
        confirm = input("Do you want to use this token anyway? (y/n): ")
        if confirm.lower() != 'y':
            print("Token update cancelled.")
            return False
    
    # Update the token in the .env file
    try:
        set_key(env_path, 'DISCORD_TOKEN', new_token)
        print("\n✅ Discord token updated successfully in", env_path)
        return True
    except Exception as e:
        print(f"\nError updating token: {e}")
        return False

def main():
    """Main function."""
    print_header()
    
    success = update_token()
    
    if success:
        print("\nNext Steps:")
        print("1. Run the test script to verify your token:")
        print("   python -m src.omega_bot_farm.discord.test_connection")
        print("2. If the test is successful, run your Discord bot:")
        print("   python -m src.omega_bot_farm.discord.bot")
    else:
        print("\nToken update failed. Please try again.")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main() 