#!/usr/bin/env python3

"""
IBR España Dashboard Runner

This script runs the IBR España component for Divine Dashboard v3
"""

import os
import sys
import json
import logging
import argparse
import importlib.util
from pathlib import Path

# Configure logging with timestamps
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("ibr_spain_dashboard.log")
    ]
)
logger = logging.getLogger("ibr_spain_runner")

def check_environment():
    """Check if the environment is properly set up"""
    # Check Python version
    python_version = sys.version_info
    logger.info(f"Using Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        logger.error("Python 3.7 or higher is required")
        return False
    
    # Make sure we can import required packages
    required_packages = ["gradio"]
    missing_packages = []
    
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing required packages: {', '.join(missing_packages)}")
        logger.info("Installing missing packages...")
        
        try:
            import pip
            for package in missing_packages:
                logger.info(f"Installing {package}...")
                pip.main(["install", package])
            logger.info("All required packages installed")
        except Exception as e:
            logger.error(f"Failed to install missing packages: {str(e)}")
            return False
    
    # Check if component directory exists
    component_dir = Path("components/ibr_spain")
    if not component_dir.exists():
        logger.error(f"IBR España component directory not found at {component_dir.absolute()}")
        return False
    
    # Check if main component file exists
    dashboard_file = component_dir / "ibr_dashboard.py"
    if not dashboard_file.exists():
        logger.error(f"IBR dashboard file not found at {dashboard_file.absolute()}")
        return False
        
    return True

def ensure_config():
    """Ensure config directory and file exist"""
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / "ibr_spain.json"
    if not config_file.exists():
        logger.info("Creating default configuration...")
        default_config = {
            "instagram_manager": {
                "data_dir": os.path.expanduser("~/ibr_data/instagram_manager"),
                "account_name": "ibrespana",
                "logging_level": "INFO"
            }
        }
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        logger.info(f"Default configuration created at {config_file}")
    else:
        logger.info(f"Using existing configuration at {config_file}")
    
    # Ensure data directory exists
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        data_dir = config.get("instagram_manager", {}).get("data_dir")
        if data_dir:
            data_path = Path(data_dir)
            data_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Ensuring data directory exists at {data_dir}")
        else:
            logger.warning("No data_dir found in configuration. Using default.")
            default_data_dir = os.path.expanduser("~/ibr_data/instagram_manager")
            Path(default_data_dir).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Error processing configuration: {str(e)}")
        return False
    
    return True

def initialize_instagram_manager():
    """Initialize the Instagram Manager"""
    try:
        logger.info("Attempting to import InstagramManager...")
        from components.ibr_spain.micro_modules.instagram_manager import InstagramManager
        logger.info("Successfully imported InstagramManager")
        
        logger.info("Initializing InstagramManager...")
        manager = InstagramManager()
        logger.info("Instagram Manager initialized successfully")
    except ImportError as e:
        logger.error(f"Failed to import InstagramManager: {str(e)}")
        logger.error("Please make sure the IBR España component is installed correctly")
        return False
    except Exception as e:
        logger.error(f"Failed to initialize Instagram Manager: {str(e)}")
        return False
    return True

def main():
    """Main function to run the IBR España Dashboard"""
    parser = argparse.ArgumentParser(description="Run IBR España Dashboard")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the server on")
    parser.add_argument("--share", action="store_true", help="Create a shareable link")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    parser.add_argument("--check-only", action="store_true", help="Only check if the component can be run, don't start it")
    args = parser.parse_args()
    
    # Set log level based on debug flag
    log_level = logging.DEBUG if args.debug else logging.INFO
    logger.setLevel(log_level)
    
    # Display banner
    print("=======================================================")
    print("      IBR España Instagram Manager Dashboard")
    print("=======================================================")
    print(f"Working directory: {os.getcwd()}")
    
    # Check the environment
    logger.info("Checking environment...")
    if not check_environment():
        logger.error("Environment check failed. Please fix the issues and try again.")
        sys.exit(1)
    
    # Ensure configuration is set up
    logger.info("Setting up configuration...")
    if not ensure_config():
        logger.error("Configuration setup failed. Please fix the issues and try again.")
        sys.exit(1)
    
    # Initialize Instagram Manager
    logger.info("Setting up Instagram Manager...")
    if not initialize_instagram_manager():
        logger.error("Instagram Manager initialization failed. Please fix the issues and try again.")
        sys.exit(1)
    
    # If this is a check-only run, exit now
    if args.check_only:
        logger.info("Check-only mode: All checks passed. Component can be run.")
        sys.exit(0)
    
    # Set environment variables
    os.environ["IBR_ENV"] = "production"
    os.environ["IBR_LOG_LEVEL"] = "DEBUG" if args.debug else "INFO"
    
    # Add the current directory to the Python path
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())
    
    # Import and run the dashboard
    try:
        logger.info("Starting IBR España Dashboard...")
        import gradio as gr
        from components.ibr_spain.ibr_dashboard import create_ibr_interface
        
        # Create the interface
        logger.info("Creating interface...")
        interface = create_ibr_interface()
        
        # Launch the interface
        logger.info(f"Launching interface on port {args.port}...")
        interface.launch(
            server_name="0.0.0.0",
            server_port=args.port,
            share=args.share,
            debug=args.debug,
            quiet=not args.debug
        )
    except ImportError as e:
        logger.error(f"Failed to import required modules: {str(e)}")
        print("\nPlease make sure gradio is installed: pip install gradio")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to start IBR España Dashboard: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 