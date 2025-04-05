"""
File monitoring system for the Quantum Test Runner.
"""

import os
import time
import logging
import queue
from typing import Dict, List, Set, Any, Optional, Tuple, Union

from watchdog.events import FileSystemEventHandler, FileSystemEvent

from .types import TestDimension, Colors

logger = logging.getLogger("0M3G4_B0TS_QA_AUT0_TEST_SUITES_RuNn3R_5D")

class FileChangeHandler(FileSystemEventHandler):
    """Handler for file system changes that trigger test runs."""
    
    def __init__(self, queue: queue.Queue, watched_extensions: Set[str], 
                 ignored_dirs: Set[str], test_map: Dict[str, List[TestDimension]]):
        """Initialize the handler with a queue for events."""
        self.queue = queue
        self.watched_extensions = watched_extensions
        self.ignored_dirs = ignored_dirs
        self.test_map = test_map
        self.last_events = {}  # Track last event time for each file
        
    def on_any_event(self, event: FileSystemEvent) -> None:
        """Handle file system events."""
        if event.is_directory:
            return
        
        # Get the name of the file
        file_name = os.path.basename(event.src_path)
        event_type = event.event_type.upper()
        
        # Determine color based on event type
        color = Colors.GREEN
        if event_type == 'MODIFIED':
            color = Colors.BLUE
        elif event_type == 'DELETED':
            color = Colors.RED
        elif event_type == 'MOVED':
            color = Colors.YELLOW
        
        # Ignore temporary files and files in ignored directories
        if any(ignored in event.src_path for ignored in self.ignored_dirs):
            return
        
        # Only watch files with specific extensions
        _, ext = os.path.splitext(event.src_path)
        if ext.lower() not in self.watched_extensions:
            return
        
        # Avoid duplicate events (some file systems trigger multiple events)
        current_time = time.time()
        if event.src_path in self.last_events:
            if current_time - self.last_events[event.src_path] < 1.0:  # 1 second debounce
                return
            
        self.last_events[event.src_path] = current_time
        
        # Log the detected change with color
        logger.info(f"{color}⚡ FILE {event_type}: {file_name}{Colors.ENDC}")
            
        # Determine which tests to run based on the file path
        dimensions_to_test = self._get_dimensions_to_test(event.src_path)
        
        if dimensions_to_test:
            dimension_names = [dim.name for dim in dimensions_to_test]
            logger.info(f"{Colors.CYAN}↪ Queueing tests: {Colors.YELLOW}{', '.join(dimension_names)}{Colors.ENDC}")
            self.queue.put((event.src_path, dimensions_to_test))
    
    def _get_dimensions_to_test(self, file_path: str) -> List[TestDimension]:
        """Determine which test dimensions to run based on the changed file."""
        dimensions = []
        
        # First check for exact path matches
        for pattern, dims in self.test_map.items():
            if pattern in file_path:
                dimensions.extend(dims)
        
        # Then check file extensions
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # If Python file, add UNIT test dimension by default
        if ext == '.py' and TestDimension.UNIT not in dimensions:
            dimensions.append(TestDimension.UNIT)
            
            # Add INTEGRATION for files that likely touch multiple components
            if ('integration' in file_path or 
                'api' in file_path or 
                'service' in file_path or 
                'controller' in file_path or
                'manager' in file_path):
                dimensions.append(TestDimension.INTEGRATION)
            
            # Add PERFORMANCE for performance-sensitive code
            if ('performance' in file_path or 
                'optimiz' in file_path or 
                'speed' in file_path or 
                'benchmark' in file_path):
                dimensions.append(TestDimension.PERFORMANCE)
                
            # Add SECURITY for security-related code
            if ('security' in file_path or 
                'auth' in file_path or 
                'permission' in file_path or 
                'encrypt' in file_path or
                'decrypt' in file_path or
                'password' in file_path):
                dimensions.append(TestDimension.SECURITY)
                
        return list(set(dimensions))  # Remove duplicates 