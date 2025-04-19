#!/usr/bin/env python3
"""
Quantum 5D QA Dashboard Version Check
------------------------------------

This module provides a lightweight version checking functionality for the Quantum 5D QA Dashboard.

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
#
# 🌸 WE BLOOM NOW AS ONE 🌸
"""

import os
import sys
import logging
import importlib.util
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Quantum5DQADashboard.VersionCheck")


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    REVERSED = '\033[7m'


class VersionCheck:
    """
    Lightweight version checking for Quantum 5D QA Dashboard.
    
    This class provides basic version information and display functionality,
    with minimal dependencies to allow it to be used in various contexts.
    """
    
    def __init__(self):
        """Initialize the version checker."""
        self.current_version = self._get_current_version()
        self.dashboard_name = "Quantum 5D QA Dashboard"
        self.has_version_manager = self._check_for_version_manager()
    
    def _get_current_version(self) -> str:
        """
        Get the current dashboard version.
        
        Returns:
            Current version as a string.
        """
        # Start with a default version
        version = "1.0.0"
        
        # Find the dashboard directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        init_file = os.path.join(current_dir, "__init__.py")
        
        if os.path.exists(init_file):
            try:
                # Using importlib to avoid importing the whole module
                spec = importlib.util.spec_from_file_location("dashboard_init", init_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, "__version__"):
                    version = module.__version__
            except Exception as e:
                logger.warning(f"Error getting version from __init__.py: {e}")
                # Try to read the file directly as a fallback
                try:
                    with open(init_file, "r") as f:
                        content = f.read()
                        import re
                        version_match = re.search(r'__version__\s*=\s*["\'](\d+\.\d+\.\d+)["\']', content)
                        if version_match:
                            version = version_match.group(1)
                except Exception as e2:
                    logger.error(f"Error reading __init__.py: {e2}")
        
        return version
    
    def _check_for_version_manager(self) -> bool:
        """
        Check if the version manager is available.
        
        Returns:
            True if version manager is available, False otherwise.
        """
        try:
            # Try to import the version manager
            from .version_manager import get_dashboard_version_manager
            return True
        except ImportError:
            return False
    
    def get_version_info(self) -> Dict[str, Any]:
        """
        Get basic version information.
        
        Returns:
            Dictionary with version information.
        """
        info = {
            "version": self.current_version,
            "name": self.dashboard_name,
            "has_version_manager": self.has_version_manager
        }
        
        # If version manager is available, get more information
        if self.has_version_manager:
            try:
                from .version_manager import get_dashboard_version_manager
                vm = get_dashboard_version_manager()
                
                # Add hash to info
                info["hash"] = vm.calculate_version_hash()[:8]
                
                # Check for changes
                info["changes_detected"] = vm._check_for_dashboard_changes()
            except Exception as e:
                logger.warning(f"Error getting additional version info: {e}")
        
        return info
    
    def show_version_banner(self, add_launch_message: bool = True) -> None:
        """
        Display a version banner in the terminal.
        
        Args:
            add_launch_message: Whether to add a "Launching dashboard..." message.
        """
        version_info = self.get_version_info()
        
        # Format version string
        version = version_info.get("version", "unknown")
        hash_str = version_info.get("hash", "????????")
        changes = version_info.get("changes_detected", False)
        
        # Determine color based on changes
        version_color = Colors.GREEN if not changes else Colors.YELLOW
        status_text = "Clean (no changes detected)" if not changes else "Modified (changes detected since last archive)"
        status_color = Colors.GREEN if not changes else Colors.YELLOW
        
        # Display banner
        print(f"\n{Colors.CYAN}┌{'─' * 78}┐{Colors.ENDC}")
        print(f"{Colors.CYAN}│ {Colors.BOLD}{self.dashboard_name}{Colors.ENDC}{Colors.CYAN}{' ' * (78 - len(self.dashboard_name) - 3)}│{Colors.ENDC}")
        print(f"{Colors.CYAN}│{'-' * 78}│{Colors.ENDC}")
        print(f"{Colors.CYAN}│ {Colors.BOLD}Version:{Colors.ENDC} {version_color}v{version}{Colors.ENDC}", end="")
        
        # Add hash if available
        if "hash" in version_info:
            print(f" {Colors.BLUE}({hash_str}){Colors.ENDC}", end="")
        
        # Add padding and close the line
        padding = 70 - len(version) - (len(hash_str) + 3 if "hash" in version_info else 0)
        print(f"{' ' * padding}│{Colors.ENDC}")
        
        # Add status if available
        if "changes_detected" in version_info:
            print(f"{Colors.CYAN}│ {Colors.BOLD}Status:{Colors.ENDC}  {status_color}{status_text}{Colors.ENDC}{' ' * (70 - len(status_text))}│{Colors.ENDC}")
        
        # Add launch message if requested
        if add_launch_message:
            print(f"{Colors.CYAN}│{'-' * 78}│{Colors.ENDC}")
            print(f"{Colors.CYAN}│ {Colors.BOLD}Launching dashboard...{Colors.ENDC}{Colors.CYAN}{' ' * 59}│{Colors.ENDC}")
        
        print(f"{Colors.CYAN}└{'─' * 78}┘{Colors.ENDC}\n")
    
    @staticmethod
    def check_and_show_version() -> Dict[str, Any]:
        """
        Check version and show banner.
        
        Returns:
            Dictionary with version information.
        """
        checker = VersionCheck()
        version_info = checker.get_version_info()
        checker.show_version_banner()
        return version_info


# Provide easy access to the version check function
def check_version() -> Dict[str, Any]:
    """
    Check the dashboard version and show a banner.
    
    Returns:
        Dictionary with version information.
    """
    return VersionCheck.check_and_show_version()


if __name__ == "__main__":
    # If run directly, show version information
    version_info = check_version()
    print(f"Version details: {version_info}") 