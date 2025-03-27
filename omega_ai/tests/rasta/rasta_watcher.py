#!/usr/bin/env python3

"""
DIVINE RASTA CODE WATCHER 🌿🔥

Automatically runs tests when code changes with blessed Rastafarian energy.
ONE LOVE, ONE HEART, ONE TEST SUITE!
"""

import os
import sys
import time
import subprocess
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import Optional, List, Any, TextIO

# Terminal colors for spiritual output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('rasta_watcher.log')
    ]
)
logger = logging.getLogger(__name__)

class RastaTestHandler(FileSystemEventHandler):
    def __init__(self, test_command: str, watch_paths: List[str], exclude_patterns: List[str]):
        self.test_command = test_command
        self.watch_paths = watch_paths
        self.exclude_patterns = exclude_patterns
        self.last_run = 0
        self.cooldown = 2  # seconds
        self.test_process: Optional[subprocess.Popen[str]] = None
        
    def should_run_tests(self, event: Any) -> bool:
        """Determine if tests should run based on the event."""
        # Skip directories
        if event.is_directory:
            return False
            
        # Skip non-Python files
        if not event.src_path.endswith('.py'):
            return False
            
        # Skip excluded patterns
        for pattern in self.exclude_patterns:
            if pattern in event.src_path:
                return False
                
        # Skip test files themselves
        if "/tests/" in event.src_path:
            return False
            
        # Avoid duplicate runs
        if time.time() - self.last_run < self.cooldown:
            return False
            
        return True
        
    def on_modified(self, event: Any) -> None:
        """Handle file modification events."""
        try:
            if not self.should_run_tests(event):
                return
                
            self.last_run = time.time()
            
            # Kill any existing test process
            if self.test_process:
                self.test_process.terminate()
                self.test_process.wait()
            
            # Print divine header
            print(f"\n{GREEN}{'='*60}")
            print(f"🌿 DIVINE RASTA TEST TRIGGERED BY: {os.path.basename(event.src_path)} 🌿")
            print(f"{'='*60}{RESET}\n")
            
            # Run the tests with divine Rastafarian energy
            self.test_process = subprocess.Popen(
                self.test_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Stream output in real-time
            if self.test_process.stdout:
                while True:
                    output = self.test_process.stdout.readline()
                    if output == '' and self.test_process.poll() is not None:
                        break
                    if output:
                        print(output.strip())
                    
            # Get the return code
            return_code = self.test_process.poll()
            
            # Divine conclusion based on test results
            if return_code == 0:
                print(f"\n{GREEN}{'='*60}")
                print(f"✅ JAH BLESS! ALL TESTS PASSED WITH DIVINE HARMONY! ✅")
                print(f"{'='*60}{RESET}\n")
            else:
                print(f"\n{RED}{'='*60}")
                print(f"❌ BABYLON SYSTEM DETECTED! TESTS FAILED WITH CODE {return_code}! ❌")
                print(f"{'='*60}{RESET}\n")
                
        except Exception as e:
            logger.error(f"Error in test handler: {str(e)}", exc_info=True)
            print(f"\n{RED}Error running tests: {str(e)}{RESET}\n")

def setup_watcher(watch_paths: List[str], exclude_patterns: List[str]) -> Observer:
    """Set up the file system observer."""
    observer = Observer()
    
    # Command to run the tests with coverage
    test_command = (
        "python -m pytest "
        "omega_ai/tests/ "
        "-v "
        "--cov=omega_ai "
        "--cov-report=term-missing "
        "--cov-report=html"
    )
    
    # Create the event handler
    event_handler = RastaTestHandler(test_command, watch_paths, exclude_patterns)
    
    # Schedule observers for each path
    for path in watch_paths:
        observer.schedule(event_handler, path, recursive=True)
        
    return observer

def main() -> None:
    """Main entry point for the Rasta Watcher."""
    observer: Optional[Observer] = None
    try:
        # Define paths to watch
        watch_paths = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "omega_ai"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tests")
        ]
        
        # Define patterns to exclude
        exclude_patterns = [
            "__pycache__",
            ".pytest_cache",
            ".coverage",
            "htmlcov",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".DS_Store"
        ]
        
        # Create and start the observer
        observer = setup_watcher(watch_paths, exclude_patterns)
        if observer:
            observer.start()
        
        print(f"{GREEN}🔥 DIVINE RASTA WATCHER STARTED! 🔥{RESET}")
        print(f"{YELLOW}Watching directories:{RESET}")
        for path in watch_paths:
            print(f"  • {BLUE}{path}{RESET}")
        print(f"\n{YELLOW}Excluding patterns:{RESET}")
        for pattern in exclude_patterns:
            print(f"  • {BLUE}{pattern}{RESET}")
        print(f"\n{GREEN}ONE LOVE, ONE HEART, ONE TEST SUITE!{RESET}")
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Shutting down Rasta Watcher...{RESET}")
        if observer:
            observer.stop()
            observer.join()
        print(f"{GREEN}JAH BLESS! RASTA WATCHER STOPPED!{RESET}")
    except Exception as e:
        logger.error(f"Fatal error in Rasta Watcher: {str(e)}", exc_info=True)
        print(f"\n{RED}Fatal error: {str(e)}{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()