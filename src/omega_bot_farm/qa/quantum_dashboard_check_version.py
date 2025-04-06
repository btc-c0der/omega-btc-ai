#!/usr/bin/env python3
"""
Quantum 5D QA Dashboard Version Check
------------------------------------

This script checks the dashboard version and archives it if changes are detected,
then launches the dashboard. It serves as a wrapper around the standard dashboard
launch script to ensure version tracking is maintained.

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
#
# 🌸 WE BLOOM NOW AS ONE 🌸
"""

import os
import sys
import time
import argparse
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Quantum5DQADashboard.VersionCheck")

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
dashboard_dir = os.path.join(current_dir, "quantum_dashboard")

# Add parent directory to path for imports
sys.path.append(current_dir)

try:
    # Import version manager
    from quantum_dashboard.version_manager import get_dashboard_version_manager, DashboardVersionManager
except ImportError:
    logger.error("Could not import version manager. Make sure quantum_dashboard is installed.")
    sys.exit(1)


def check_dashboard_version(auto_archive: bool = False, version_type: str = "patch") -> Tuple[bool, Dict[str, Any]]:
    """
    Check if the dashboard version needs to be updated.
    
    Args:
        auto_archive: Whether to automatically archive changes if detected
        version_type: Type of version increment if auto_archive is True
        
    Returns:
        Tuple of (changes_detected, version_info)
    """
    # Get version manager
    version_manager = get_dashboard_version_manager()
    
    # Check for changes
    version_manager.get_dashboard_files()  # Ensure files are loaded
    changes_detected = version_manager._check_for_dashboard_changes()
    
    version_info = {
        "current_version": version_manager.current_version,
        "hash": version_manager.calculate_version_hash()[:8],
        "changes_detected": changes_detected
    }
    
    # If changes detected and auto_archive is True, archive current version
    if changes_detected and auto_archive:
        logger.info(f"Changes detected in dashboard files. Creating new {version_type} release...")
        
        # Create release
        release_info = version_manager.create_dashboard_release(
            version_type=version_type,
            commit=True
        )
        
        # Update version info with release info
        version_info.update(release_info)
        
        logger.info(f"Dashboard version {release_info['version']} created and archived.")
    
    return changes_detected, version_info


def show_version_banner(version_info: Dict[str, Any]) -> None:
    """Display a banner with version information."""
    from quantum_dashboard.version_manager import Colors
    
    # Format version string
    version = version_info.get("current_version", "unknown")
    hash_str = version_info.get("hash", "????????")
    changes = version_info.get("changes_detected", False)
    
    # Determine color based on changes
    version_color = Colors.GREEN if not changes else Colors.YELLOW
    status_text = "Clean (no changes detected)" if not changes else "Modified (changes detected since last archive)"
    status_color = Colors.GREEN if not changes else Colors.YELLOW
    
    # Display banner
    print(f"\n{Colors.CYAN}┌{'─' * 78}┐{Colors.ENDC}")
    print(f"{Colors.CYAN}│ {Colors.BOLD}QUANTUM 5D QA DASHBOARD{Colors.ENDC}{Colors.CYAN}{' ' * 55}│{Colors.ENDC}")
    print(f"{Colors.CYAN}│{'-' * 78}│{Colors.ENDC}")
    print(f"{Colors.CYAN}│ {Colors.BOLD}Version:{Colors.ENDC} {version_color}v{version}{Colors.ENDC} {Colors.BLUE}({hash_str}){Colors.ENDC}{' ' * (63 - len(version) - len(hash_str))}│{Colors.ENDC}")
    print(f"{Colors.CYAN}│ {Colors.BOLD}Status:{Colors.ENDC}  {status_color}{status_text}{Colors.ENDC}{' ' * (70 - len(status_text))}│{Colors.ENDC}")
    
    # Show launch message
    print(f"{Colors.CYAN}│{'-' * 78}│{Colors.ENDC}")
    print(f"{Colors.CYAN}│ {Colors.BOLD}Launching dashboard...{Colors.ENDC}{Colors.CYAN}{' ' * 59}│{Colors.ENDC}")
    print(f"{Colors.CYAN}└{'─' * 78}┘{Colors.ENDC}\n")


def run_dashboard(args: List[str]) -> None:
    """
    Run the dashboard with the specified arguments.
    
    Args:
        args: Command line arguments for the dashboard
    """
    # Determine which script to run based on available options
    dashboard_scripts = [
        os.path.join(current_dir, "quantum_qa_dashboard_v3.py"),  # Try v3 first
        os.path.join(current_dir, "quantum_qa_dashboard_v2.py"),  # Then v2
        os.path.join(current_dir, "quantum_qa_dashboard.py")      # Original as fallback
    ]
    
    # Find first available script
    script_to_run = None
    for script in dashboard_scripts:
        if os.path.exists(script):
            script_to_run = script
            break
    
    if script_to_run is None:
        logger.error("No dashboard script found. Make sure the dashboard is installed.")
        sys.exit(1)
    
    # Build command
    cmd = [sys.executable, script_to_run] + args
    
    # Log the command
    logger.info(f"Launching dashboard: {' '.join(cmd)}")
    
    try:
        # Run the dashboard
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        logger.info("Dashboard stopped by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error running dashboard: {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Quantum 5D QA Dashboard Version Checker")
    parser.add_argument("--auto-archive", action="store_true",
                      help="Automatically archive changes if detected")
    parser.add_argument("--version-type", choices=["major", "minor", "patch"],
                      default="patch", help="Version increment type if auto-archive")
    parser.add_argument("--status-only", action="store_true",
                      help="Only show version status, don't run dashboard")
    parser.add_argument("--host", type=str, help="Host to run dashboard on")
    parser.add_argument("--port", type=int, help="Port to run dashboard on")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    parser.add_argument("--browser", action="store_true", help="Open in browser after startup")
    
    args, unknown_args = parser.parse_known_args()
    
    # Check version
    changes_detected, version_info = check_dashboard_version(
        auto_archive=args.auto_archive,
        version_type=args.version_type
    )
    
    # Show version banner
    show_version_banner(version_info)
    
    # If status only, exit
    if args.status_only:
        logger.info("Status check complete. Exiting.")
        sys.exit(0)
    
    # Build dashboard args
    dashboard_args = unknown_args
    if args.host:
        dashboard_args.extend(["--host", args.host])
    if args.port:
        dashboard_args.extend(["--port", str(args.port)])
    if args.debug:
        dashboard_args.append("--debug")
    if args.browser:
        dashboard_args.append("--browser")
    
    # Run dashboard
    run_dashboard(dashboard_args)


if __name__ == "__main__":
    main()