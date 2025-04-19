#!/usr/bin/env python3

"""
IBR España Component Setup Script

This script checks if the IBR España component directory structure is complete
and creates essential files and directories if they don't exist.
"""

import os
import sys
import shutil
import json
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("ibr_spain_setup.log")
    ]
)
logger = logging.getLogger("ibr_spain_setup")

# Essential directory structure
REQUIRED_DIRS = [
    "components/ibr_spain",
    "components/ibr_spain/micro_modules",
    "components/ibr_spain/tests",
    "components/ibr_spain/docs",
    "config"
]

# Essential files with their templates
REQUIRED_FILES = {
    "components/ibr_spain/__init__.py": """#!/usr/bin/env python3

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
Iglesia Bautista Reformada (IBR) España Dashboard Component

This component provides digital ministry services for IBR España, featuring:
- Sermon library with search and filtering
- Church event calendar
- Weekly devotional content
- Prayer request submission
- Social media integration (Instagram)

The component follows a modular architecture with React frontend components
integrated into the Divine Dashboard v3 infrastructure.
"""

# Version information
__version__ = "1.0.0"
__author__ = "OMEGA Bot Farm Team"

# Make modules available for import
try:
    from .ibr_dashboard import create_ibr_interface
    from .micro_modules.sermon_library import SermonLibrary
    from .micro_modules.prayer_requests import PrayerRequests
    from .micro_modules.church_events import ChurchEvents
    from .micro_modules.devotionals import Devotionals
    from .micro_modules.instagram_integration import InstagramIntegration
except ImportError as e:
    print(f"Warning: Unable to import some modules: {e}")
""",
    
    "components/ibr_spain/micro_modules/__init__.py": """#!/usr/bin/env python3

"""
IBR España Micro Modules

This package contains the micro modules for the IBR España dashboard component.
Each module provides specific functionality for the dashboard.
"""

# Version information
__version__ = "1.0.0"
__author__ = "OMEGA Bot Farm Team"
""",
    
    "components/ibr_spain/micro_modules/requirements.txt": """requests==2.31.0
pydantic==2.5.2
tenacity==8.2.3
python-dotenv==1.0.0
python-json-logger==2.0.7
gradio>=3.50.0
""",
    
    "components/ibr_spain/micro_modules/instagram_manager.py": """#!/usr/bin/env python3

"""
Instagram Manager for IBR España

This module provides functionality to manage the Instagram account for IBR España.
"""

import os
import json
import logging
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("ibr_spain_dashboard.log")
    ]
)
logger = logging.getLogger("instagram_manager")

class Post:
    """Instagram post class"""
    def __init__(self, image_path: str, caption: str, first_comment: Optional[str] = None, scheduled_time: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.image_path = image_path
        self.caption = caption
        self.first_comment = first_comment
        self.scheduled_time = scheduled_time
        self.created_at = datetime.now().isoformat()
        self.published = False
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "image_path": self.image_path,
            "caption": self.caption,
            "first_comment": self.first_comment,
            "scheduled_time": self.scheduled_time,
            "created_at": self.created_at,
            "published": self.published
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Post':
        """Create from dictionary"""
        post = cls(
            image_path=data.get("image_path", ""),
            caption=data.get("caption", ""),
            first_comment=data.get("first_comment"),
            scheduled_time=data.get("scheduled_time")
        )
        post.id = data.get("id", str(uuid.uuid4()))
        post.created_at = data.get("created_at", datetime.now().isoformat())
        post.published = data.get("published", False)
        return post

class Comment:
    """Instagram comment class"""
    def __init__(self, text: str, author: str, post_id: str):
        self.id = str(uuid.uuid4())
        self.text = text
        self.author = author
        self.post_id = post_id
        self.created_at = datetime.now().isoformat()
        self.hidden = False
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "text": self.text,
            "author": self.author,
            "post_id": self.post_id,
            "created_at": self.created_at,
            "hidden": self.hidden
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Comment':
        """Create from dictionary"""
        comment = cls(
            text=data.get("text", ""),
            author=data.get("author", ""),
            post_id=data.get("post_id", "")
        )
        comment.id = data.get("id", str(uuid.uuid4()))
        comment.created_at = data.get("created_at", datetime.now().isoformat())
        comment.hidden = data.get("hidden", False)
        return comment

class InstagramManager:
    """Instagram Manager class"""
    def __init__(self):
        """Initialize the Instagram Manager"""
        self.config = self._load_config()
        self.data_dir = Path(self.config.get("data_dir", os.path.expanduser("~/ibr_data/instagram_manager")))
        self.account_name = self.config.get("account_name", "ibrespana")
        
        # Create directories
        self._create_directories()
        
        logger.info(f"Instagram Manager initialized for account {self.account_name}")
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration"""
        config_path = Path("config/ibr_spain.json")
        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                return config.get("instagram_manager", {})
            except Exception as e:
                logger.error(f"Error loading configuration: {e}")
                return {}
        else:
            logger.warning("Configuration file not found, using defaults")
            return {}
            
    def _create_directories(self):
        """Create necessary directories"""
        dirs = [
            self.data_dir,
            self.data_dir / "posts",
            self.data_dir / "comments",
            self.data_dir / "reports",
            self.data_dir / "campaigns",
            self.data_dir / "livestreams"
        ]
        
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
            
        logger.info(f"Created directories at {self.data_dir}")
""",
    
    "config/ibr_spain.json": """{
  "instagram_manager": {
    "data_dir": "~/ibr_data/instagram_manager",
    "account_name": "ibrespana",
    "logging_level": "INFO"
  }
}
"""
}

def create_minimal_files():
    """Create minimal set of files if they don't exist"""
    # Create main dashboard file if it doesn't exist
    ibr_dashboard_path = Path("components/ibr_spain/ibr_dashboard.py")
    if not ibr_dashboard_path.exists():
        minimal_dashboard = """#!/usr/bin/env python3

"""
IBR España Dashboard - Main Interface

This module integrates all IBR España micro modules into a unified
Gradio interface for the Divine Dashboard v3.
"""

import os
import gradio as gr
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("ibr_spain_dashboard.log")
    ]
)
logger = logging.getLogger("ibr_spain_dashboard")

def create_ibr_interface():
    """Create the IBR España dashboard interface"""
    with gr.Blocks(title="IBR España Dashboard", theme=gr.themes.Base()) as iface:
        gr.Markdown("# IBR España Dashboard")
        gr.Markdown("## Instagram Manager")
        
        with gr.Tab("Instagram Manager"):
            gr.Markdown("### Instagram Manager")
            gr.Markdown("This component is under development.")
            
        with gr.Tab("About"):
            gr.Markdown("## About IBR España Dashboard")
            gr.Markdown("The IBR España Dashboard provides digital ministry services for IBR España.")
            gr.Markdown("Version: 1.0.0")
            
    return iface

# For testing purposes
if __name__ == "__main__":
    iface = create_ibr_interface()
    iface.launch()
"""
        with open(ibr_dashboard_path, "w") as f:
            f.write(minimal_dashboard)
        logger.info(f"Created minimal dashboard file at {ibr_dashboard_path}")

def check_structure():
    """Check if the required directory structure exists"""
    missing_dirs = []
    
    for dir_path in REQUIRED_DIRS:
        full_path = Path(dir_path)
        if not full_path.exists():
            missing_dirs.append(dir_path)
            
    if missing_dirs:
        logger.warning(f"Missing directories: {', '.join(missing_dirs)}")
        return False
    
    logger.info("All required directories exist")
    return True

def check_files():
    """Check if the required files exist"""
    missing_files = []
    
    for file_path in REQUIRED_FILES:
        full_path = Path(file_path)
        if not full_path.exists():
            missing_files.append(file_path)
            
    if missing_files:
        logger.warning(f"Missing files: {', '.join(missing_files)}")
        return False
    
    logger.info("All required files exist")
    return True

def create_dirs():
    """Create the required directory structure"""
    for dir_path in REQUIRED_DIRS:
        full_path = Path(dir_path)
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {dir_path}")
    
    logger.info("All required directories have been created")

def create_files():
    """Create the required files with templates"""
    for file_path, template in REQUIRED_FILES.items():
        full_path = Path(file_path)
        if not full_path.exists():
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, "w") as f:
                f.write(template)
            logger.info(f"Created file: {file_path}")
    
    logger.info("All required files have been created")

def setup():
    """Set up the IBR España component"""
    # Display banner
    print("=======================================================")
    print("      IBR España Component Setup")
    print("=======================================================")
    
    # Check the directory structure
    logger.info("Checking directory structure...")
    if not check_structure():
        logger.info("Creating missing directories...")
        create_dirs()
    
    # Check the files
    logger.info("Checking required files...")
    if not check_files():
        logger.info("Creating missing files...")
        create_files()
    
    # Create minimal files if needed
    logger.info("Creating minimal dashboard file if needed...")
    create_minimal_files()
    
    # Set file permissions
    run_scripts = [
        "run_ibr_spain.sh",
        "run_ibr_spain.py",
        "setup_ibr_spain.py"
    ]
    
    for script in run_scripts:
        script_path = Path(script)
        if script_path.exists():
            os.chmod(script_path, 0o755)
            logger.info(f"Made script executable: {script}")
    
    # Success message
    print("=======================================================")
    print("      IBR España Component Setup Complete")
    print("=======================================================")
    print("\nYou can now run the IBR España component with:")
    print("./run_ibr_spain.sh")
    print("\nOr with the Python script:")
    print("./run_ibr_spain.py")

if __name__ == "__main__":
    setup() 