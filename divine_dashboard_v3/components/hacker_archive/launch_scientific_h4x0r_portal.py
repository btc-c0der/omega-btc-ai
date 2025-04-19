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
Scientific H4x0r Portal Launcher

Launches the Scientific H4x0r Portal with PDF analysis and defacement research capabilities.
"""

import os
import sys
import time
import asyncio
import logging
import argparse
import subprocess
from pathlib import Path
from typing import Optional, List, Tuple

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("h4x0r_portal")

# ASCII Art Banner
H4X0R_BANNER = r"""
  ███████╗ ██████╗██╗███████╗███╗   ██╗████████╗██╗███████╗██╗ ██████╗
  ██╔════╝██╔════╝██║██╔════╝████╗  ██║╚══██╔══╝██║██╔════╝██║██╔════╝
  ███████╗██║     ██║█████╗  ██╔██╗ ██║   ██║   ██║█████╗  ██║██║     
  ╚════██║██║     ██║██╔══╝  ██║╚██╗██║   ██║   ██║██╔══╝  ██║██║     
  ███████║╚██████╗██║███████╗██║ ╚████║   ██║   ██║██║     ██║╚██████╗
  ╚══════╝ ╚═════╝╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝     ╚═╝ ╚═════╝
  ██╗  ██╗██╗  ██╗██╗  ██╗ ██████╗ ██████╗     ██████╗  ██████╗ ██████╗ ████████╗ █████╗ ██╗     
  ██║  ██║██║  ██║╚██╗██╔╝██╔═══██╗██╔══██╗    ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔══██╗██║     
  ███████║███████║ ╚███╔╝ ██║   ██║██████╔╝    ██████╔╝██║   ██║██████╔╝   ██║   ███████║██║     
  ██╔══██║╚════██║ ██╔██╗ ██║   ██║██╔══██╗    ██╔═══╝ ██║   ██║██╔══██╗   ██║   ██╔══██║██║     
  ██║  ██║     ██║██╔╝ ██╗╚██████╔╝██║  ██║    ██║     ╚██████╔╝██║  ██║   ██║   ██║  ██║███████╗
  ╚═╝  ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝    ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝
"""

def print_banner():
    """Print the ASCII art banner with hacker aesthetic."""
    print("\033[92m" + H4X0R_BANNER + "\033[0m")  # Green color
    print("\033[91m" + "=" * 80 + "\033[0m")  # Red separator
    print("\033[96m    🔬 Scientific H4x0r Portal - Defacement & PDF Analysis Research Tool 🔬\033[0m")
    print("\033[91m" + "=" * 80 + "\033[0m")
    print()

def check_dependencies() -> List[str]:
    """Check if all required dependencies are installed.
    
    Returns:
        List of missing dependencies
    """
    missing = []
    
    try:
        import gradio
        logger.info("Gradio is installed - GUI interface available")
    except ImportError:
        missing.append("gradio")
    
    try:
        import PyPDF2
        logger.info("PyPDF2 is installed - PDF analysis available")
    except ImportError:
        missing.append("PyPDF2")
    
    try:
        import nltk
        logger.info("NLTK is installed - Text analysis available")
    except ImportError:
        missing.append("nltk")
    
    try:
        import aiohttp
        logger.info("aiohttp is installed - URL downloading available")
    except ImportError:
        missing.append("aiohttp")
    
    try:
        import torch
        import transformers
        logger.info("PyTorch and Transformers are installed - AI analysis available")
    except ImportError:
        missing.append("torch")
        missing.append("transformers")
    
    return missing

def install_dependencies(deps: List[str]) -> bool:
    """Install missing dependencies.
    
    Args:
        deps: List of dependencies to install
        
    Returns:
        True if successful, False otherwise
    """
    if not deps:
        return True
    
    print(f"\033[93mInstalling missing dependencies: {', '.join(deps)}\033[0m")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", *deps
        ])
        return True
    except subprocess.CalledProcessError:
        logger.error("Failed to install dependencies")
        return False

def get_available_ports(start_port: int = 7870, num_ports: int = 2) -> List[int]:
    """Find available ports for the services.
    
    Args:
        start_port: Starting port number to check
        num_ports: Number of ports needed
        
    Returns:
        List of available ports
    """
    import socket
    
    available_ports = []
    port = start_port
    
    while len(available_ports) < num_ports:
        try:
            socket.socket().connect(('localhost', port))
            # Port is in use, try next one
            port += 1
        except ConnectionRefusedError:
            # Port is available
            available_ports.append(port)
            port += 1
    
    return available_ports

async def launch_pdf_analyzer(port: int, share: bool = False):
    """Launch the PDF analyzer dashboard.
    
    Args:
        port: Port number to run on
        share: Whether to create a public link
    """
    from .pdf_analyzer_dashboard import launch_pdf_analyzer_dashboard
    
    # Create cache directory
    cache_dir = Path("pdf_cache")
    cache_dir.mkdir(exist_ok=True, parents=True)
    
    logger.info(f"Launching PDF Analyzer Dashboard on port {port}")
    launch_pdf_analyzer_dashboard(
        cache_dir=str(cache_dir),
        share=share,
        server_name="0.0.0.0"
    )

async def main():
    """Main entry point for the Scientific H4x0r Portal."""
    parser = argparse.ArgumentParser(description="Launch the Scientific H4x0r Portal")
    parser.add_argument('--port', type=int, default=7870, help='Starting port number')
    parser.add_argument('--share', action='store_true', help='Create a public link')
    parser.add_argument('--install-deps', action='store_true', help='Install missing dependencies')
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Check dependencies
    missing_deps = check_dependencies()
    if missing_deps:
        if args.install_deps:
            success = install_dependencies(missing_deps)
            if not success:
                logger.error("Failed to install dependencies. Please install manually.")
                sys.exit(1)
        else:
            logger.warning(f"Missing dependencies: {', '.join(missing_deps)}")
            logger.warning("Some features may not be available. Run with --install-deps to install them.")
    
    # Find available ports
    pdf_analyzer_port = args.port
    
    # Launch services
    logger.info("Starting Scientific H4x0r Portal...")
    
    try:
        await launch_pdf_analyzer(pdf_analyzer_port, args.share)
    except Exception as e:
        logger.error(f"Error launching PDF Analyzer: {e}")
        sys.exit(1)
    
    logger.info("All services started successfully")
    logger.info(f"PDF Analyzer Dashboard: http://localhost:{pdf_analyzer_port}")
    
    # Keep running until interrupted
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down Scientific H4x0r Portal...")
    
    logger.info("Portal shutdown complete")

if __name__ == "__main__":
    asyncio.run(main()) 