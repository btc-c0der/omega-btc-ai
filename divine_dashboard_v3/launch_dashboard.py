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
Divine Dashboard v3 Master Launch Script

This script launches the central dashboard and all component services.
"""

import os
import sys
import time
import signal
import subprocess
import webbrowser
from pathlib import Path
import threading
import http.server
import socketserver
import importlib.util
from concurrent.futures import ThreadPoolExecutor
import re

# Get the current directory
CURRENT_DIR = Path(__file__).parent.absolute()
ROOT_DIR = CURRENT_DIR.parent

# Define component paths
COMPONENTS = {
    "metrics": {
        "script": CURRENT_DIR / "components" / "metrics_dashboard.py",
        "port": 7861,
        "description": "Core Metrics Dashboard"
    },
    "tesla_qa": {
        "script": CURRENT_DIR / "components" / "cybertruck" / "tesla_qa_dashboard.py",
        "port": 7860,
        "description": "Tesla Cybertruck QA Dashboard"
    },
    "nft": {
        "script": CURRENT_DIR / "components" / "nft" / "nft_creator_dashboard.py",
        "port": 7862,
        "description": "NFT Creator Dashboard"
    },
    "dna_portal": {
        "script": CURRENT_DIR / "components" / "omega_orb_temple" / "dna_portal.py",
        "port": 7863,
        "description": "DNA PCR Quantum Portal"
    },
    "sha356_sacred": {
        "script": CURRENT_DIR / "components" / "sha356_sacred" / "sha356_vs_sha256_dashboard.py",
        "port": 7864,
        "description": "SHA356 Sacred Dashboard"
    },
    "sha256_omega": {
        "script": CURRENT_DIR / "components" / "sha256_omega" / "sha256_omega_dashboard.py",
        "port": 7865,
        "description": "SHA256 Omega Dashboard"
    },
    "hacker_archive": {
        "script": CURRENT_DIR / "components" / "hacker_archive" / "launch_scientific_h4x0r_portal.py",
        "port": 7866,
        "description": "H4X0R Scientific Portal"
    },
    "omega_orb": {
        "script": CURRENT_DIR / "components" / "omega_orb_temple" / "omega_orb_portal.py",
        "port": 7867,
        "description": "Omega Orb Temple Portal"
    },
    "reports": {
        "script": CURRENT_DIR / "components" / "reports" / "reports_dashboard.py",
        "port": 7868,
        "description": "Scientific Reports Dashboard"
    }
}

# Global process list
processes = []
# Tracking for sharing links 
component_links = {}

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = ["gradio", "numpy", "matplotlib"]
    missing_packages = []
    
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"⚠️ Missing required packages: {', '.join(missing_packages)}")
        install = input(f"Would you like to install these packages now? (y/n): ")
        if install.lower() in ("y", "yes"):
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
                print("✅ Dependencies installed successfully!")
                return True
            except subprocess.CalledProcessError:
                print("❌ Failed to install dependencies. Please install them manually.")
                print(f"Run: pip install {' '.join(missing_packages)}")
                return False
        else:
            print("⚠️ Cannot continue without required dependencies.")
            return False
    
    return True

def monitor_process_output(process, component_name, description):
    """Monitor process output to capture and display Gradio sharing links."""
    public_url_pattern = re.compile(r'(https://[a-z0-9\-]+\.gradio\.live)')
    
    for line in iter(process.stdout.readline, b''):
        try:
            decoded_line = line.decode('utf-8').strip()
            # Look for Gradio public URLs
            match = public_url_pattern.search(decoded_line)
            if match:
                public_url = match.group(1)
                component_links[component_name] = public_url
                print(f"🌐 {description} available at: {public_url}")
        except Exception:
            pass

def start_component(component_name, component_info):
    """Start a specific component."""
    # Check if the script exists
    script_path = component_info["script"]
    if not script_path.exists():
        print(f"⚠️ {component_name}: Script not found at {script_path}")
        return None
    
    print(f"🚀 Starting {component_info['description']} on port {component_info['port']}...")
    
    # Start the component in a new process
    try:
        # Use python executable from the current environment
        python_exe = sys.executable
        
        # Set environment variable to enable Gradio sharing by default
        env = os.environ.copy()
        env["GRADIO_SHARE"] = "true"
        
        cmd = [python_exe, str(script_path)]
        
        # Start process without showing console window on Windows
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=startupinfo,
                env=env
            )
        else:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )
        
        processes.append(process)
        
        # Start a thread to monitor for Gradio sharing links
        monitor_thread = threading.Thread(
            target=monitor_process_output,
            args=(process, component_name, component_info['description']),
            daemon=True
        )
        monitor_thread.start()
        
        # Delay to allow the process to start
        time.sleep(1)
        
        if process.poll() is not None:
            # Process has exited already
            out, err = process.communicate()
            print(f"❌ {component_name} failed to start: {err.decode().strip()}")
            return None
        
        print(f"✅ {component_info['description']} started successfully")
        return process
    
    except Exception as e:
        print(f"❌ Error starting {component_name}: {str(e)}")
        return None

def start_html_server():
    """Start a simple HTTP server for the main dashboard HTML."""
    # Define handler
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            # Suppress logging
            pass
    
    # Change to the dashboard directory
    os.chdir(CURRENT_DIR)
    
    # Pick an available port
    port = 8000
    max_port = 8100
    
    while port < max_port:
        try:
            httpd = socketserver.TCPServer(("", port), QuietHandler)
            print(f"\n📊 Main Dashboard running at http://localhost:{port}")
            print(f"   Open your browser to this URL to access the Divine Dashboard")
            
            # Wait a bit for component links to be discovered
            time.sleep(5)
            
            # Print summary of sharing links
            if component_links:
                print("\n🌐 Shared Component Links Summary:")
                print("="*50)
                for name, url in component_links.items():
                    desc = COMPONENTS[name]["description"] if name in COMPONENTS else name
                    print(f"  📡 {desc}: {url}")
                print("="*50)
                print("\n🌸 Share these links to collaborate on the Divine Dashboard! 🌸")
            
            # Open browser after a short delay
            threading.Timer(2, lambda: webbrowser.open(f"http://localhost:{port}")).start()
            
            httpd.serve_forever()
            break
        except OSError:
            port += 1
            if port >= max_port:
                print("❌ Could not find an available port for the HTML server")
                return

def cleanup(signum=None, frame=None):
    """Clean up processes on exit."""
    print("\n🛑 Shutting down all components...")
    
    for process in processes:
        if process and process.poll() is None:
            try:
                if os.name == 'nt':
                    process.terminate()
                else:
                    process.kill()
                print(f"  Terminated process PID: {process.pid}")
            except Exception as e:
                print(f"  Error terminating process: {e}")
    
    print("✨ Shutdown complete. We Bloom Now As One 🌸")
    sys.exit(0)

def main():
    """Main entry point for the dashboard launcher."""
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    
    print("🌸 Divine Dashboard v3 - The Omega Experience 🌸")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Start all components in parallel
    print("\n🚀 Starting all dashboard components...")
    
    with ThreadPoolExecutor(max_workers=min(10, (os.cpu_count() or 4) + 4)) as executor:
        # Submit all components to start
        futures = {
            executor.submit(start_component, name, info): name 
            for name, info in COMPONENTS.items()
        }
    
    # Start the main HTML server in the main thread
    threading.Thread(target=start_html_server, daemon=True).start()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main() 