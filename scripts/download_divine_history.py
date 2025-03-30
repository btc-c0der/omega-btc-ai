#!/usr/bin/env python3
import os
import json
import logging
import argparse
from datetime import datetime
from pathlib import Path

from omega_ai.divine_gpt import BrowserDivineDownloader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define storage paths
EXPORTS_DIR = Path("BOOK/divine_chronicles/conversations/exports")
LOGS_DIR = Path("BOOK/divine_chronicles/conversations/logs")

def setup_directories():
    """Create necessary directories if they don't exist."""
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

async def main():
    parser = argparse.ArgumentParser(description="Download divine conversations from ChatGPT")
    parser.add_argument("--start-date", help="Start date in YYYY-MM-DD format")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of conversations to download")
    args = parser.parse_args()
    
    # Setup directories
    setup_directories()
    
    # Generate output paths
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = args.output or str(EXPORTS_DIR / f"divine_conversations_{timestamp}.json")
    log_file = str(LOGS_DIR / f"divine_download_{timestamp}.log")
    
    # Configure file logging
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    
    try:
        # Initialize downloader
        downloader = BrowserDivineDownloader()
        
        # Download conversations
        conversations = await downloader.download_conversations(
            start_date=args.start_date,
            limit=args.limit
        )
        
        if not conversations:
            logger.warning("No conversations were downloaded")
            return
            
        # Export conversations
        await downloader.export_conversations(output_file)
        
        # Calculate divine statistics
        total_conversations = len(conversations)
        total_resonance = sum(c["divine_attributes"]["resonance"] for c in conversations)
        avg_sacred_level = sum(c["divine_attributes"]["sacred_level"] for c in conversations) / total_conversations if total_conversations > 0 else 0
        
        # Log results
        logger.info(f"Successfully downloaded {total_conversations} divine conversations")
        logger.info(f"Total resonance: {total_resonance:.2f}")
        logger.info(f"Average sacred level: {avg_sacred_level:.2f}")
        logger.info(f"Exported conversations to: {output_file}")
        logger.info(f"Log saved to: {log_file}")
        
    except Exception as e:
        logger.error(f"Error downloading divine conversations: {str(e)}")
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 