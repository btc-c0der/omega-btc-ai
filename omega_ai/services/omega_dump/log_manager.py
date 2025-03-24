"""OMEGA Dump Service - Divine Log Manager"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
import redis
import json
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .models import LogEntry

class LogFileHandler(FileSystemEventHandler):
    """Divine Log File Event Handler"""
    def __init__(self, manager: 'OMEGALogManager'):
        self.manager = manager
        
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.log'):
            self.manager.process_log_file(event.src_path)

class OMEGALogManager:
    """Divine Log Management System"""
    
    def __init__(
        self,
        logs_dir: str = "logs",
        backup_dir: str = "logs/backup",
        redis_url: str = "redis://localhost:6379/0",
        backup_interval: int = 3600  # 1 hour
    ):
        """Initialize the divine log manager.
        
        Args:
            logs_dir: Directory containing log files
            backup_dir: Directory for log backups
            redis_url: Redis connection URL
            backup_interval: Backup interval in seconds
        """
        self.logs_dir = Path(logs_dir)
        self.backup_dir = Path(backup_dir)
        self.redis_url = redis_url
        self.backup_interval = backup_interval
        
        # Create directories
        self.logs_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True, parents=True)
        
        # Setup Redis connection
        self.redis = redis.from_url(redis_url)
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Setup file watcher
        self.observer = Observer()
        self.observer.schedule(
            LogFileHandler(self),
            str(self.logs_dir),
            recursive=False
        )
    
    def start(self):
        """Start the divine log management service"""
        self.logger.info("Starting OMEGA Dump Service...")
        self.observer.start()
        
    def stop(self):
        """Stop the divine log management service"""
        self.logger.info("Stopping OMEGA Dump Service...")
        self.observer.stop()
        self.observer.join()
    
    def process_log_file(self, file_path: str):
        """Process a log file and store its contents.
        
        Args:
            file_path: Path to the log file
        """
        path = Path(file_path)
        if not path.exists():
            return
            
        try:
            # Read log file
            with open(path, 'r') as f:
                content = f.read()
            
            # Create log entry
            entry = LogEntry(
                timestamp=datetime.now(),
                source=path.name,
                content=content,
                level="INFO",
                metadata={"file_size": path.stat().st_size}
            )
            
            # Store in Redis
            key = f"logs:{path.stem}:{entry.timestamp.isoformat()}"
            self.redis.set(key, json.dumps(entry.to_dict()))
            
            # Move to backup
            backup_path = self.backup_dir / f"{path.stem}_{entry.timestamp.strftime('%Y%m%d_%H%M%S')}.log"
            shutil.copy2(path, backup_path)
            
            # Clear original file
            with open(path, 'w') as f:
                f.write("")
                
            self.logger.info(f"Processed and backed up log file: {path.name}")
            
        except Exception as e:
            self.logger.error(f"Error processing log file {path.name}: {str(e)}")
    
    def get_logs(
        self,
        source: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        level: Optional[str] = None
    ) -> List[LogEntry]:
        """Retrieve logs from Redis storage.
        
        Args:
            source: Filter by log source
            start_time: Filter by start time
            end_time: Filter by end time
            level: Filter by log level
            
        Returns:
            List of matching log entries
        """
        entries = []
        pattern = "logs:*"
        
        for key in self.redis.scan_iter(match=pattern):
            data = json.loads(self.redis.get(key))
            entry = LogEntry.from_dict(data)
            
            # Apply filters
            if source and entry.source != source:
                continue
            if start_time and entry.timestamp < start_time:
                continue
            if end_time and entry.timestamp > end_time:
                continue
            if level and entry.level != level:
                continue
                
            entries.append(entry)
            
        return sorted(entries, key=lambda x: x.timestamp)
    
    def cleanup_old_backups(self, days: int = 30):
        """Clean up old backup files.
        
        Args:
            days: Remove backups older than this many days
        """
        cutoff = datetime.now().timestamp() - (days * 24 * 3600)
        
        for path in self.backup_dir.glob("*.log"):
            if path.stat().st_mtime < cutoff:
                path.unlink()
                self.logger.info(f"Removed old backup: {path.name}") 