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
Backup Service Micromodule
--------------------------

This microservice handles backup operations:
- Automatic backups of changed files
- Compression of backups
- Restore functionality
- Backup rotation
"""

import os
import time
import shutil
import logging
import json
import zipfile
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
import threading
from typing import List, Dict, Any, Optional, Set

# Configure logging
logger = logging.getLogger("backup_service")

class BackupService:
    """Backup service for project files."""
    
    def __init__(self, project_root: str, backup_dir: str = None):
        """
        Initialize the backup service.
        
        Args:
            project_root: Path to the project root
            backup_dir: Directory to store backups (default: <project_root>/.quantum/backups)
        """
        self.project_root = Path(project_root).resolve()
        
        if backup_dir:
            self.backup_dir = Path(backup_dir).resolve()
        else:
            self.backup_dir = self.project_root / ".quantum" / "backups"
            
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.watched_files: Set[Path] = set()
        self.file_hashes: Dict[Path, str] = {}
        self.running = False
        self._watcher_thread = None
        self._lock = threading.Lock()
        
        # Keep track of changes since last backup
        self.changes_since_backup: Dict[Path, datetime] = {}
        
        # Load historical info if it exists
        self.metadata_file = self.backup_dir / "backup_metadata.json"
        self._load_metadata()
    
    def _load_metadata(self):
        """Load metadata from disk if it exists."""
        self.metadata = {
            "last_backup": None,
            "total_backups": 0,
            "backup_history": []
        }
        
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r") as f:
                    self.metadata = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Error loading backup metadata: {e}")
    
    def _save_metadata(self):
        """Save metadata to disk."""
        try:
            with open(self.metadata_file, "w") as f:
                json.dump(self.metadata, f, indent=2)
        except IOError as e:
            logger.error(f"Error saving backup metadata: {e}")
    
    def _get_file_hash(self, file_path: Path) -> str:
        """
        Get a simple hash of file contents.
        
        Args:
            file_path: Path to the file
            
        Returns:
            A string hash of the file contents
        """
        import hashlib
        
        if not file_path.exists():
            return ""
        
        hasher = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                buf = f.read(65536)  # 64k chunks
                while buf:
                    hasher.update(buf)
                    buf = f.read(65536)
            return hasher.hexdigest()
        except IOError:
            return ""
    
    def watch_file(self, file_path: str):
        """
        Add a file to the watch list.
        
        Args:
            file_path: Path to the file to watch
        """
        path = Path(file_path)
        if not path.is_absolute():
            path = self.project_root / path
        
        with self._lock:
            self.watched_files.add(path)
            self.file_hashes[path] = self._get_file_hash(path)
    
    def watch_directory(self, dir_path: str, extensions: List[str] = None):
        """
        Add all files in a directory to the watch list.
        
        Args:
            dir_path: Path to the directory
            extensions: Optional list of file extensions to include
        """
        path = Path(dir_path)
        if not path.is_absolute():
            path = self.project_root / path
        
        if not path.exists() or not path.is_dir():
            logger.warning(f"Directory does not exist: {path}")
            return
        
        for root, _, files in os.walk(path):
            for file in files:
                file_path = Path(root) / file
                
                # Skip if we're filtering by extension and this doesn't match
                if extensions and not any(file.endswith(ext) for ext in extensions):
                    continue
                
                self.watch_file(file_path)
    
    def check_for_changes(self) -> List[Path]:
        """
        Check if any watched files have changed.
        
        Returns:
            List of changed file paths
        """
        changed_files = []
        
        with self._lock:
            for file_path in self.watched_files:
                if not file_path.exists():
                    # File was deleted
                    changed_files.append(file_path)
                    continue
                
                current_hash = self._get_file_hash(file_path)
                previous_hash = self.file_hashes.get(file_path, "")
                
                if current_hash != previous_hash:
                    changed_files.append(file_path)
                    self.file_hashes[file_path] = current_hash
                    self.changes_since_backup[file_path] = datetime.now()
        
        return changed_files
    
    def create_backup(self, files: List[Path] = None) -> Optional[Path]:
        """
        Create a backup of the specified files.
        
        Args:
            files: List of files to back up, or None to back up all changed files
            
        Returns:
            Path to the backup file, or None if no backup was created
        """
        if files is None:
            # Back up all files that have changed since last backup
            with self._lock:
                files = list(self.changes_since_backup.keys())
        
        if not files:
            logger.info("No files to back up")
            return None
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"backup_{timestamp}.zip"
        
        # Create a temporary directory for files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copy files to temp directory with relative paths
            for file_path in files:
                if not file_path.exists():
                    continue
                
                # Create relative path within the project
                try:
                    rel_path = file_path.relative_to(self.project_root)
                    target_path = Path(temp_dir) / rel_path
                    
                    # Create parent directories if they don't exist
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy the file
                    shutil.copy2(file_path, target_path)
                except (ValueError, IOError) as e:
                    logger.error(f"Error copying file {file_path}: {e}")
            
            # Create zip archive
            try:
                with zipfile.ZipFile(backup_file, "w", zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(temp_dir):
                        for file in files:
                            # Get the absolute path of the file
                            file_path = os.path.join(root, file)
                            
                            # Get the relative path from the temp directory
                            rel_path = os.path.relpath(file_path, temp_dir)
                            
                            # Add to the zip file
                            zipf.write(file_path, arcname=rel_path)
                
                logger.info(f"Created backup: {backup_file}")
                
                # Update metadata
                self.metadata["last_backup"] = timestamp
                self.metadata["total_backups"] += 1
                self.metadata["backup_history"].append({
                    "timestamp": timestamp,
                    "filename": backup_file.name,
                    "file_count": len(files)
                })
                
                # Limit history size
                if len(self.metadata["backup_history"]) > 100:
                    self.metadata["backup_history"] = self.metadata["backup_history"][-100:]
                
                self._save_metadata()
                
                # Clear the changes since backup
                self.changes_since_backup.clear()
                
                return backup_file
            
            except Exception as e:
                logger.error(f"Error creating backup: {e}")
                return None
    
    def restore_from_backup(self, backup_file: Path, restore_dir: Path = None) -> bool:
        """
        Restore files from a backup.
        
        Args:
            backup_file: Path to the backup file
            restore_dir: Directory to restore to, or None to restore to original location
            
        Returns:
            True if successful, False otherwise
        """
        if not backup_file.exists():
            logger.error(f"Backup file does not exist: {backup_file}")
            return False
        
        try:
            if restore_dir is None:
                # Restore to original location (project root)
                restore_dir = self.project_root
            
            # Extract zip file
            with zipfile.ZipFile(backup_file, "r") as zipf:
                zipf.extractall(restore_dir)
            
            logger.info(f"Restored from backup: {backup_file} to {restore_dir}")
            return True
        
        except Exception as e:
            logger.error(f"Error restoring from backup: {e}")
            return False
    
    def rotate_backups(self, max_age_days: int = 30, max_count: int = 100):
        """
        Delete old backups to save space.
        
        Args:
            max_age_days: Maximum age of backups to keep in days
            max_count: Maximum number of backups to keep
        """
        # Get list of backup files
        backup_files = sorted([f for f in self.backup_dir.glob("backup_*.zip")])
        
        # Keep the most recent max_count backups
        if len(backup_files) > max_count:
            files_to_delete = backup_files[:-max_count]
            for file in files_to_delete:
                try:
                    file.unlink()
                    logger.info(f"Deleted old backup: {file}")
                except IOError as e:
                    logger.error(f"Error deleting backup {file}: {e}")
        
        # Delete backups older than max_age_days
        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        for file in backup_files:
            try:
                # Extract date from filename
                date_str = file.stem.replace("backup_", "")
                file_date = datetime.strptime(date_str, "%Y%m%d_%H%M%S")
                
                if file_date < cutoff_date:
                    file.unlink()
                    logger.info(f"Deleted old backup: {file}")
            except (ValueError, IOError) as e:
                logger.error(f"Error processing backup {file}: {e}")
    
    def watcher_loop(self):
        """Run the continuous file watching loop."""
        logger.info("Starting backup service file watcher")
        self.running = True
        
        while self.running:
            try:
                # Check for changes
                changed_files = self.check_for_changes()
                
                if changed_files:
                    logger.info(f"Detected changes in {len(changed_files)} files")
                    
                    # Skip creating immediate backup if there are many changes at once
                    # We'll capture them next time after allowing for more changes
                    if len(changed_files) <= 10:
                        self.create_backup(changed_files)
                
                # Rotate backups occasionally
                if datetime.now().minute % 30 == 0:  # Every 30 minutes
                    self.rotate_backups()
                
            except Exception as e:
                logger.error(f"Error in backup service watcher: {e}")
            
            # Sleep briefly
            time.sleep(10)
    
    def start(self):
        """Start the backup service in a background thread."""
        if self._watcher_thread and self._watcher_thread.is_alive():
            logger.warning("Backup service is already running")
            return
        
        self._watcher_thread = threading.Thread(target=self.watcher_loop, daemon=True)
        self._watcher_thread.start()
    
    def stop(self):
        """Stop the backup service."""
        logger.info("Stopping backup service")
        self.running = False
        if self._watcher_thread:
            self._watcher_thread.join(timeout=5.0)

# Example usage when module is run directly
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    service = BackupService(".")
    
    # Watch Python files in current directory
    service.watch_directory(".", extensions=[".py"])
    
    service.start()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        service.stop() 