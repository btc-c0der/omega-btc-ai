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


"""
DIVINE RASTA CODE WATCHER 🌿🔥

Automatically runs tests when code changes with blessed Rastafarian energy.
ONE LOVE, ONE HEART, ONE TEST SUITE!
"""

import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Terminal colors for spiritual output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

class RastaTestHandler(FileSystemEventHandler):
    def __init__(self, test_command):
        self.test_command = test_command
        # Track when we last ran tests to avoid duplicates
        self.last_run = 0
        
    def on_modified(self, event):
        # Skip directories and non-Python files
        if event.is_directory or not event.src_path.endswith('.py'):
            return
            
        # Skip test files themselves and __pycache__ directories
        if "__pycache__" in event.src_path or "/tests/" in event.src_path:
            return
            
        # Avoid duplicate runs (watchdog sometimes fires multiple events)
        if time.time() - self.last_run < 2:  # 2-second cooldown
            return
            
        self.last_run = time.time()
        
        # Print divine header
        print(f"\n{GREEN}{'='*60}")
        print(f"🌿 DIVINE RASTA TEST TRIGGERED BY: {os.path.basename(event.src_path)} 🌿")
        print(f"{'='*60}{RESET}\n")
        
        # Run the tests with divine Rastafarian energy
        result = subprocess.run(self.test_command, shell=True)
        
        # Divine conclusion based on test results
        if result.returncode == 0:
            print(f"\n{GREEN}{'='*60}")
            print(f"✅ JAH BLESS! ALL TESTS PASSED WITH DIVINE HARMONY! ✅")
            print(f"{'='*60}{RESET}\n")
        else:
            print(f"\n{RED}{'='*60}")
            print(f"❌ BABYLON SYSTEM DETECTED! TESTS FAILED WITH CODE {result.returncode}! ❌")
            print(f"{'='*60}{RESET}\n")


if __name__ == "__main__":
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "omega_ai")
    
    # Command to run the tests
    test_command = "python -m pytest omega_ai/tests/ -v"
    
    # Create the event handler and observer
    event_handler = RastaTestHandler(test_command)
    observer = Observer()
    
    # Schedule the observer to watch the omega_ai directory
    observer.schedule(event_handler, path, recursive=True)
    
    # Start the observer
    observer.start()
    
    print(f"{GREEN}🔥 DIVINE RASTA WATCHER STARTED! 🔥{RESET}")
    print(f"{YELLOW}Watching directory: {path}{RESET}")
    print(f"{YELLOW}When Python files change, tests will run automatically{RESET}")
    print(f"{GREEN}ONE LOVE, ONE HEART, ONE TEST SUITE!{RESET}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()