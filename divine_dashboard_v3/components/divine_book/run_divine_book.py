#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
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
Divine Book Runner

A script to run the Divine Book components (Dashboard and Browser).
This script provides a command-line interface for launching either
the simplified dashboard or the advanced browser with various options.
"""

import os
import sys
import argparse
from importlib import import_module

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run Divine Book components")
    
    parser.add_argument(
        "--mode",
        type=str,
        default=os.environ.get("DIVINE_MODE", "dashboard"),
        choices=["dashboard", "browser"],
        help="Which component to run: 'dashboard' (simplified interface with sample texts) or 'browser' (advanced interface with repository documents)"
    )
    
    parser.add_argument(
        "--share",
        action="store_true",
        default=os.environ.get("GRADIO_SHARE", "false").lower() == "true",
        help="Share the Gradio interface with a public URL"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("GRADIO_PORT", "7860")),
        help="Port to run the Gradio interface on"
    )
    
    return parser.parse_args()

def run_dashboard(share=False, port=7860):
    """Run the Divine Book Dashboard."""
    try:
        from divine_book_dashboard import create_dashboard, MARKDOWN_FILES
        
        print("✨ Starting Divine Book Dashboard...")
        print(f"📚 Found {len(MARKDOWN_FILES)} Markdown files in the repository")
        dashboard = create_dashboard()
        dashboard.launch(share=share, server_port=port)
    except ImportError:
        # Try alternative import if the direct import fails
        try:
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from divine_book_dashboard import create_dashboard, MARKDOWN_FILES
            
            print("✨ Starting Divine Book Dashboard...")
            print(f"📚 Found {len(MARKDOWN_FILES)} Markdown files in the repository")
            dashboard = create_dashboard()
            dashboard.launch(share=share, server_port=port)
        except ImportError as e:
            print(f"Error: Could not import Divine Book Dashboard: {e}")
            print("Make sure you're running this script from the right directory.")
            sys.exit(1)

def run_browser(share=False, port=7860):
    """Run the Divine Book Browser."""
    try:
        from divine_book_browser import create_dashboard, MARKDOWN_FILES
        
        print("📚 Starting Divine Book Browser...")
        print(f"📚 Found {len(MARKDOWN_FILES)} Markdown files in the repository")
        browser = create_dashboard()
        browser.launch(share=share, server_port=port)
    except ImportError:
        # Try alternative import if the direct import fails
        try:
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from divine_book_browser import create_dashboard, MARKDOWN_FILES
            
            print("📚 Starting Divine Book Browser...")
            print(f"📚 Found {len(MARKDOWN_FILES)} Markdown files in the repository")
            browser = create_dashboard()
            browser.launch(share=share, server_port=port)
        except ImportError as e:
            print(f"Error: Could not import Divine Book Browser: {e}")
            print("Make sure you're running this script from the right directory.")
            sys.exit(1)

def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Set environment variables based on arguments
    os.environ["GRADIO_SHARE"] = str(args.share).lower()
    os.environ["GRADIO_PORT"] = str(args.port)
    
    print(f"🌟 Divine Book Runner")
    print(f"Mode: {args.mode}")
    print(f"Share: {'Enabled' if args.share else 'Disabled'}")
    print(f"Port: {args.port}")
    
    if args.mode == "dashboard":
        run_dashboard(share=args.share, port=args.port)
    elif args.mode == "browser":
        run_browser(share=args.share, port=args.port)
    else:
        print(f"Error: Unknown mode '{args.mode}'")
        sys.exit(1)

if __name__ == "__main__":
    main() 