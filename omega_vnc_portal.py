#!/usr/bin/env python3
# 
# OMEGA BTC AI - VNC Portal Gateway
# =================================
#
# Browser-accessible VNC portal to the OMEGA GRID using noVNC and websockify
#
# Copyright (C) 2024 OMEGA BTC AI Team
# License: GNU General Public License v3.0
#
# JAH BLESS the eternal flow of vision and connection.

import subprocess
import os
import time
import webbrowser
import argparse
import socket
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("omega_vnc_portal.log")
    ]
)
logger = logging.getLogger("OMEGA-VNC")

# Default configuration
DEFAULT_VNC_TARGET = "host.docker.internal:5900"  # Docker on Mac maps this to host
DEFAULT_NOVNC_PORT = 6080
DEFAULT_CONTAINER_NAME = "omega-novnc"
DEFAULT_IMAGE = "dorowu/ubuntu-desktop-lxde-vnc"

class OmegaVNCPortal:
    def __init__(self, vnc_target=DEFAULT_VNC_TARGET, novnc_port=DEFAULT_NOVNC_PORT, 
                container_name=DEFAULT_CONTAINER_NAME, image=DEFAULT_IMAGE, 
                open_browser_auto=True, debug=False):
        self.vnc_target = vnc_target
        self.novnc_port = novnc_port
        self.container_name = container_name
        self.image = image
        self.open_browser_auto = open_browser_auto
        self.debug = debug
        
        if debug:
            logger.setLevel(logging.DEBUG)
            
        logger.debug(f"Initialized with: VNC={vnc_target}, PORT={novnc_port}, CONTAINER={container_name}")

    def check_requirements(self):
        """Check if Docker is installed and running"""
        logger.info("🔍 Checking system requirements...")
        
        # Check if Docker is installed
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("❌ Docker is not installed or not in PATH. Please install Docker first.")
            return False
            
        # Check if Docker daemon is running
        try:
            subprocess.run(["docker", "info"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            logger.error("❌ Docker daemon is not running. Please start Docker first.")
            return False
            
        logger.info("✅ Docker is installed and running")
        
        # If using local VNC, check if Screen Sharing is enabled
        if "host.docker.internal" in self.vnc_target or "localhost" in self.vnc_target or "127.0.0.1" in self.vnc_target:
            # On macOS, check if VNC (Screen Sharing) is enabled by attempting connection
            host = "localhost"
            port = int(self.vnc_target.split(":")[-1])
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.settimeout(1)
                s.connect((host, port))
                logger.info("✅ Screen Sharing is enabled on macOS")
                return True
            except (socket.timeout, ConnectionRefusedError):
                logger.error("❌ Screen Sharing is not enabled on macOS")
                logger.error("   Please enable it in System Settings → Sharing → Screen Sharing")
                return False
            finally:
                s.close()
        
        return True

    def pull_novnc_image(self):
        """Pull the noVNC Docker image"""
        logger.info(f"🔄 Pulling noVNC Docker image: {self.image}...")
        try:
            result = subprocess.run(
                ["docker", "pull", self.image], 
                check=True, 
                capture_output=True, 
                text=True
            )
            logger.debug(result.stdout)
            logger.info("✅ Docker image pulled successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to pull Docker image: {e}")
            logger.error(f"Error details: {e.stderr}")
            return False

    def stop_existing_container(self):
        """Stop existing container if running"""
        logger.info(f"🔍 Checking for existing container: {self.container_name}...")
        try:
            result = subprocess.run(
                ["docker", "ps", "-q", "-f", f"name={self.container_name}"],
                check=True,
                capture_output=True,
                text=True
            )
            
            if result.stdout.strip():
                logger.info(f"🛑 Stopping existing container: {self.container_name}")
                subprocess.run(
                    ["docker", "rm", "-f", self.container_name],
                    check=True,
                    capture_output=True
                )
                logger.info("✅ Existing container stopped and removed")
            else:
                logger.info("✅ No existing container found")
                
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Error managing existing container: {e}")
            logger.error(f"Error details: {e.stderr}")
            return False

    def run_novnc_container(self):
        """Launch the noVNC container"""
        logger.info(f"🚀 Launching noVNC container connected to {self.vnc_target}...")
        
        # Stop existing container first
        if not self.stop_existing_container():
            return False
        
        try:
            # Build the docker run command
            cmd = [
                "docker", "run", "-d",
                "--name", self.container_name,
                "-p", f"{self.novnc_port}:80",
                "-e", f"VNC_SERVER={self.vnc_target}",
                "--add-host", "host.docker.internal:host-gateway",
                self.image
            ]
            
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            container_id = result.stdout.strip()
            logger.info(f"✅ Container launched with ID: {container_id[:12]}")
            
            # Verify the container is running
            status = subprocess.run(
                ["docker", "ps", "-f", f"id={container_id}", "--format", "{{.Status}}"],
                check=True,
                capture_output=True,
                text=True
            )
            
            if "Up" in status.stdout:
                logger.info(f"✅ Container is running: {status.stdout.strip()}")
                return True
            else:
                logger.error(f"❌ Container not running properly: {status.stdout.strip()}")
                # Get container logs to diagnose the issue
                logs = subprocess.run(
                    ["docker", "logs", container_id],
                    check=True,
                    capture_output=True,
                    text=True
                )
                logger.error(f"Container logs: {logs.stdout}")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to launch container: {e}")
            logger.error(f"Error details: {e.stderr}")
            return False

    def wait_for_service(self, timeout=30):
        """Wait for the noVNC service to be ready"""
        logger.info(f"⏳ Waiting for the portal to open (timeout: {timeout}s)...")
        
        start_time = time.time()
        url = f"http://localhost:{self.novnc_port}"
        
        while time.time() - start_time < timeout:
            try:
                # Check if port is open
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect(("localhost", self.novnc_port))
                s.close()
                
                logger.info(f"✅ Portal is ready at {url}/vnc.html")
                time.sleep(2)  # Give it a little more time to fully initialize
                return True
            except (socket.timeout, ConnectionRefusedError):
                logger.debug(f"Still waiting for service... ({int(time.time() - start_time)}s)")
                time.sleep(2)
            except Exception as e:
                logger.error(f"Error checking service: {e}")
                time.sleep(2)
        
        logger.error(f"❌ Timed out waiting for the service to be ready")
        return False

    def open_browser(self):
        """Open the browser to the noVNC portal"""
        url = f"http://localhost:{self.novnc_port}/vnc.html"
        logger.info(f"🌐 Opening browser to: {url}")
        
        try:
            webbrowser.open(url)
            logger.info("✅ Browser opened to noVNC portal")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to open browser: {e}")
            logger.info(f"Please manually open: {url}")
            return False

    def display_connection_info(self):
        """Display connection information"""
        print("\n" + "="*60)
        print(f"🔱 OMEGA VNC PORTAL ACTIVATED 🔱")
        print("="*60)
        print(f"✨ Access your OMEGA GRID from anywhere through a browser:")
        print(f"🌐 URL: http://localhost:{self.novnc_port}/vnc.html")
        print(f"🔌 VNC Target: {self.vnc_target}")
        print(f"🐳 Container: {self.container_name}")
        print("="*60)
        print("🛑 To stop the portal: python omega_vnc_portal.py --stop")
        print("🔄 For connection issues: python omega_vnc_portal.py --restart")
        print("="*60)
        print("JAH JAH BLESS THE REMOTE VISION!")
        print("="*60 + "\n")

    def stop_portal(self):
        """Stop the noVNC portal"""
        logger.info(f"🛑 Stopping the OMEGA VNC Portal ({self.container_name})...")
        
        try:
            # Check if container exists
            result = subprocess.run(
                ["docker", "ps", "-a", "-q", "-f", f"name={self.container_name}"],
                check=True,
                capture_output=True,
                text=True
            )
            
            if result.stdout.strip():
                subprocess.run(
                    ["docker", "rm", "-f", self.container_name],
                    check=True,
                    capture_output=True
                )
                logger.info("✅ OMEGA VNC Portal stopped successfully")
                return True
            else:
                logger.info("✅ No OMEGA VNC Portal container found to stop")
                return True
                
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to stop OMEGA VNC Portal: {e}")
            logger.error(f"Error details: {e.stderr}")
            return False

    def check_status(self):
        """Check the status of the noVNC portal"""
        logger.info(f"🔍 Checking status of OMEGA VNC Portal ({self.container_name})...")
        
        try:
            # Check if container exists and its status
            result = subprocess.run(
                ["docker", "ps", "-a", "-f", f"name={self.container_name}", "--format", "{{.Status}}"],
                check=True,
                capture_output=True,
                text=True
            )
            
            status = result.stdout.strip()
            
            if not status:
                print("❓ OMEGA VNC Portal is not running")
                return False
            elif "Up" in status:
                # Get port mapping
                port_result = subprocess.run(
                    ["docker", "port", self.container_name],
                    check=True,
                    capture_output=True,
                    text=True
                )
                ports = port_result.stdout.strip()
                
                print("\n" + "="*60)
                print(f"✅ OMEGA VNC Portal is RUNNING")
                print("="*60)
                print(f"Status: {status}")
                print(f"Ports: {ports}")
                print(f"Access URL: http://localhost:{self.novnc_port}/vnc.html")
                print("="*60 + "\n")
                return True
            else:
                print(f"❌ OMEGA VNC Portal container exists but is not running")
                print(f"Status: {status}")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to check OMEGA VNC Portal status: {e}")
            logger.error(f"Error details: {e.stderr}")
            return False

    def run(self):
        """Run the full OMEGA VNC Portal setup"""
        print("\n🔱 OMEGA VNC PORTAL INITIATION 🔱\n")
        
        # Check requirements
        if not self.check_requirements():
            return False
            
        # Pull the Docker image
        if not self.pull_novnc_image():
            return False
            
        # Run the noVNC container
        if not self.run_novnc_container():
            return False
            
        # Wait for the service to be ready
        if not self.wait_for_service():
            return False
            
        # Display connection information
        self.display_connection_info()
        
        # Open browser
        if self.open_browser_auto:
            self.open_browser()
        
        return True


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="OMEGA VNC Portal - Browser-accessible VNC gateway to the OMEGA GRID")
    
    # Main action arguments
    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument("--start", action="store_true", help="Start the OMEGA VNC Portal (default action)")
    action_group.add_argument("--stop", action="store_true", help="Stop the OMEGA VNC Portal")
    action_group.add_argument("--restart", action="store_true", help="Restart the OMEGA VNC Portal")
    action_group.add_argument("--status", action="store_true", help="Check the status of the OMEGA VNC Portal")
    
    # Configuration arguments
    parser.add_argument("--vnc-target", default=DEFAULT_VNC_TARGET, help=f"VNC server target (default: {DEFAULT_VNC_TARGET})")
    parser.add_argument("--port", type=int, default=DEFAULT_NOVNC_PORT, help=f"noVNC web port (default: {DEFAULT_NOVNC_PORT})")
    parser.add_argument("--container-name", default=DEFAULT_CONTAINER_NAME, help=f"Docker container name (default: {DEFAULT_CONTAINER_NAME})")
    parser.add_argument("--image", default=DEFAULT_IMAGE, help=f"Docker image to use (default: {DEFAULT_IMAGE})")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser automatically")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()
    
    # Create the OMEGA VNC Portal instance
    portal = OmegaVNCPortal(
        vnc_target=args.vnc_target,
        novnc_port=args.port,
        container_name=args.container_name,
        image=args.image,
        open_browser_auto=not args.no_browser,
        debug=args.debug
    )
    
    # Execute the requested action (or start by default)
    if args.stop:
        return portal.stop_portal()
    elif args.status:
        return portal.check_status()
    elif args.restart:
        portal.stop_portal()
        time.sleep(2)
        return portal.run()
    else:  # Default action is to start
        return portal.run()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 