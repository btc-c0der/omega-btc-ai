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

"""OMEGA Dump Service Installer

This script installs the OMEGA Dump service with warning system integration
as a system service on either macOS (launchd) or Linux (systemd).
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

def is_root():
    """Check if the script is running with root/admin privileges."""
    if platform.system() == 'Windows':
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except (AttributeError, ImportError):
            return False
    else:
        return os.geteuid() == 0

def install_macos_service():
    """Install OMEGA Dump as a macOS launchd service."""
    print("Installing OMEGA Dump as a macOS launchd service...\n")
    
    # Set paths
    plist_source = os.path.join(PROJECT_ROOT, "scripts", "service-config", "omega_dump.plist")
    plist_dest = os.path.expanduser("~/Library/LaunchAgents/com.omegabtcai.omegadump.plist")
    
    # Update working directory path in plist file
    with open(plist_source, 'r') as f:
        plist_content = f.read()
    
    # Replace the placeholder path with the actual project path
    plist_content = plist_content.replace("/Users/fsiqueira/Desktop/GitHub/omega-btc-ai", str(PROJECT_ROOT))
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(PROJECT_ROOT, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Write the updated plist file
    with open(plist_dest, 'w') as f:
        f.write(plist_content)
    
    print(f"Service file installed to: {plist_dest}")
    
    # Load the service
    try:
        subprocess.run(["launchctl", "load", plist_dest], check=True)
        print("Service loaded successfully!")
        print("\nThe OMEGA Dump service is now running in the background.")
        print("\nTo check service status:")
        print(f"  launchctl list | grep com.omegabtcai.omegadump")
        print("\nTo stop the service:")
        print(f"  launchctl unload {plist_dest}")
        print("\nTo restart the service:")
        print(f"  launchctl unload {plist_dest}")
        print(f"  launchctl load {plist_dest}")
        print("\nService logs can be found at:")
        print(f"  {os.path.join(PROJECT_ROOT, 'logs', 'omega_dump_service.log')}")
        print(f"  {os.path.join(PROJECT_ROOT, 'logs', 'omega_dump_service_error.log')}")
    except subprocess.CalledProcessError as e:
        print(f"Error loading service: {e}")
        print("You may need to start the service manually:")
        print(f"  launchctl load {plist_dest}")

def install_linux_service():
    """Install OMEGA Dump as a Linux systemd service."""
    print("Installing OMEGA Dump as a Linux systemd service...\n")
    
    if not is_root():
        print("This operation requires root privileges. Please run with sudo.")
        sys.exit(1)
    
    # Set paths
    service_source = os.path.join(PROJECT_ROOT, "scripts", "service-config", "omega-dump.service")
    service_dest = "/etc/systemd/system/omega-dump.service"
    
    # Update working directory path in service file
    with open(service_source, 'r') as f:
        service_content = f.read()
    
    # Replace the placeholder path with the actual project path
    service_content = service_content.replace("/opt/omega-btc-ai", str(PROJECT_ROOT))
    
    # Replace user if needed
    current_user = os.environ.get('SUDO_USER', os.environ.get('USER', 'omega'))
    service_content = service_content.replace("User=omega", f"User={current_user}")
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(PROJECT_ROOT, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Write the updated service file
    with open(service_dest, 'w') as f:
        f.write(service_content)
    
    print(f"Service file installed to: {service_dest}")
    
    # Reload systemd, enable and start the service
    try:
        subprocess.run(["systemctl", "daemon-reload"], check=True)
        subprocess.run(["systemctl", "enable", "omega-dump"], check=True)
        subprocess.run(["systemctl", "start", "omega-dump"], check=True)
        
        print("Service installed and started successfully!")
        print("\nThe OMEGA Dump service is now running in the background.")
        print("\nTo check service status:")
        print("  systemctl status omega-dump")
        print("\nTo stop the service:")
        print("  systemctl stop omega-dump")
        print("\nTo restart the service:")
        print("  systemctl restart omega-dump")
        print("\nTo view logs:")
        print("  journalctl -u omega-dump")
        print("\nAdditional service logs can be found at:")
        print(f"  {os.path.join(PROJECT_ROOT, 'logs', 'omega_dump_service.log')}")
        print(f"  {os.path.join(PROJECT_ROOT, 'logs', 'omega_dump_service_error.log')}")
    except subprocess.CalledProcessError as e:
        print(f"Error setting up service: {e}")

def main():
    """Main function to install the service on the correct platform."""
    print("="*80)
    print("OMEGA Dump Service Installer")
    print("="*80)
    print("This script will install the OMEGA Dump service with warning system integration\n")
    
    # Create service-config directory if it doesn't exist
    service_config_dir = os.path.join(PROJECT_ROOT, "scripts", "service-config")
    os.makedirs(service_config_dir, exist_ok=True)
    
    # Check if service files exist
    if platform.system() == 'Darwin':  # macOS
        plist_path = os.path.join(service_config_dir, "omega_dump.plist")
        if not os.path.exists(plist_path):
            print(f"Service file not found: {plist_path}")
            print("Please run this script from the project root directory.")
            sys.exit(1)
        install_macos_service()
    elif platform.system() == 'Linux':
        service_path = os.path.join(service_config_dir, "omega-dump.service")
        if not os.path.exists(service_path):
            print(f"Service file not found: {service_path}")
            print("Please run this script from the project root directory.")
            sys.exit(1)
        install_linux_service()
    else:
        print(f"Unsupported platform: {platform.system()}")
        print("This script supports macOS and Linux only.")
        sys.exit(1)

if __name__ == "__main__":
    main() 