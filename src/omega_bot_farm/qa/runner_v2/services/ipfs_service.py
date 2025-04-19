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
IPFS Service for Quantum Test Runner V2
---------------------------------------

This service handles decentralized storage of test artifacts on IPFS via Pinata.
It provides capabilities to:
1. Upload test reports, coverage data, and other artifacts to IPFS
2. Retrieve content from IPFS using Pinata gateways
3. Generate shareable links for test artifacts
4. Manage pinned content lifecycle
"""

import os
import json
import time
import logging
import requests
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
import threading

logger = logging.getLogger("quantum_runner_v2.ipfs_service")


class IPFSService:
    """
    Service to manage test artifacts on IPFS through Pinata integration.
    
    This enables decentralized storage and distribution of:
    - Test reports
    - Coverage data
    - AI model snapshots
    - QA metrics
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        api_secret: Optional[str] = None,
        gateway_url: str = "https://copper-far-catshark-208.mypinata.cloud/ipfs"
    ):
        """
        Initialize the IPFS service.
        
        Args:
            api_key: Pinata API key (will use env var PINATA_API_KEY if not provided)
            api_secret: Pinata API secret (will use env var PINATA_API_SECRET if not provided)
            gateway_url: Custom Pinata gateway URL
        """
        self.api_key = api_key or os.environ.get("PINATA_API_KEY")
        self.api_secret = api_secret or os.environ.get("PINATA_API_SECRET")
        self.gateway_url = gateway_url.rstrip("/")
        self.base_url = "https://api.pinata.cloud"
        self.running = False
        self._upload_queue = []
        self._lock = threading.Lock()
        self._worker_thread = None
        
        # Check credentials
        if not (self.api_key and self.api_secret):
            logger.warning(
                "IPFS Service initialized without Pinata credentials. "
                "Set PINATA_API_KEY and PINATA_API_SECRET environment variables "
                "or provide them as arguments for full functionality."
            )
            self.api_authenticated = False
        else:
            self.api_authenticated = True
    
    def start(self):
        """Start the IPFS service."""
        if self.running:
            return
            
        self.running = True
        logger.info("IPFS Service started")
        
        # Start background worker thread for upload queue
        self._worker_thread = threading.Thread(
            target=self._process_queue, 
            daemon=True
        )
        self._worker_thread.start()
    
    def stop(self):
        """Stop the IPFS service."""
        if not self.running:
            return
            
        self.running = False
        logger.info("IPFS Service stopped")
        
        # Wait for worker thread to finish current uploads
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=5.0)
    
    def _get_headers(self) -> Dict[str, str]:
        """Get API headers with authentication."""
        if not self.api_authenticated:
            raise ValueError("Pinata API credentials not configured")
            
        return {
            "pinata_api_key": self.api_key,
            "pinata_secret_api_key": self.api_secret,
            "Content-Type": "application/json"
        }
    
    def _process_queue(self):
        """Process the upload queue in background."""
        while self.running:
            # Check if there's anything in the queue
            with self._lock:
                if not self._upload_queue:
                    time.sleep(1)
                    continue
                
                # Get the next item
                file_path, name, metadata = self._upload_queue.pop(0)
            
            # Process the upload
            try:
                self._upload_file(file_path, name, metadata)
            except Exception as e:
                logger.error(f"Failed to upload {file_path} to IPFS: {e}")
                
            # Small delay between uploads
            time.sleep(0.5)
    
    def _upload_file(
        self, 
        file_path: Union[str, Path], 
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Upload a file to IPFS via Pinata API.
        
        Args:
            file_path: Path to file to upload
            name: Name for the pin
            metadata: Additional metadata for the pin
            
        Returns:
            IPFS CID if successful, None otherwise
        """
        if not self.api_authenticated:
            logger.warning("Cannot upload to IPFS: No Pinata API credentials")
            return None
            
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return None
            
        # Prepare the file for upload
        try:
            # Use the multipart upload endpoint
            url = f"{self.base_url}/pinning/pinFileToIPFS"
            
            # Prepare metadata
            if metadata is None:
                metadata = {}
                
            # Add file hash to metadata
            file_hash = self._get_file_hash(file_path)
            metadata["file_hash"] = file_hash
            metadata["quantum_runner"] = "v2"
            
            pin_metadata = {
                "name": name or file_path.name,
                "keyvalues": metadata
            }
            
            # Create multipart form data
            files = {
                'file': (file_path.name, open(file_path, 'rb')),
                'pinataMetadata': (None, json.dumps(pin_metadata))
            }
            
            # Make the request
            response = requests.post(
                url, 
                files=files,
                headers={
                    "pinata_api_key": self.api_key,
                    "pinata_secret_api_key": self.api_secret
                }
            )
            
            if response.status_code == 200:
                ipfs_hash = response.json().get("IpfsHash")
                logger.info(f"Successfully uploaded {file_path.name} to IPFS: {ipfs_hash}")
                return ipfs_hash
            else:
                logger.error(
                    f"Failed to upload {file_path.name} to IPFS. "
                    f"Status: {response.status_code}, Response: {response.text}"
                )
                return None
                
        except Exception as e:
            logger.error(f"Error uploading file to IPFS: {e}")
            return None
    
    def _get_file_hash(self, file_path: Union[str, Path]) -> str:
        """
        Calculate SHA256 hash of a file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Hex digest of file hash
        """
        file_path = Path(file_path)
        sha256 = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            # Read in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
                
        return sha256.hexdigest()
    
    def queue_upload(
        self, 
        file_path: Union[str, Path], 
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Queue a file for upload to IPFS.
        
        Args:
            file_path: Path to file to upload
            name: Name for the pin
            metadata: Additional metadata for the pin
        """
        with self._lock:
            self._upload_queue.append((file_path, name, metadata))
            
        logger.debug(f"Queued {file_path} for IPFS upload")
    
    def get_gateway_url(self, ipfs_hash: str) -> str:
        """
        Get a gateway URL for an IPFS hash.
        
        Args:
            ipfs_hash: IPFS CID/hash
            
        Returns:
            Gateway URL for the content
        """
        return f"{self.gateway_url}/{ipfs_hash}"
    
    def upload_artifact(
        self, 
        file_path: Union[str, Path], 
        artifact_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, str]]:
        """
        Upload a test artifact to IPFS.
        
        Args:
            file_path: Path to the artifact file
            artifact_type: Type of artifact (e.g., "report", "coverage", "model")
            metadata: Additional metadata
            
        Returns:
            Dict with CID and gateway URL if successful, None otherwise
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            logger.error(f"Artifact file not found: {file_path}")
            return None
            
        # Prepare metadata
        if metadata is None:
            metadata = {}
            
        metadata["artifact_type"] = artifact_type
        metadata["timestamp"] = time.time()
        metadata["filename"] = file_path.name
        
        # Upload synchronously for direct response
        ipfs_hash = self._upload_file(file_path, f"{artifact_type}_{file_path.name}", metadata)
        
        if ipfs_hash:
            return {
                "ipfs_hash": ipfs_hash,
                "gateway_url": self.get_gateway_url(ipfs_hash)
            }
        return None
    
    def upload_directory(
        self, 
        dir_path: Union[str, Path],
        artifact_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, str]]:
        """
        Upload all files in a directory to IPFS.
        
        Args:
            dir_path: Path to directory
            artifact_type: Type of artifacts
            metadata: Additional metadata
            
        Returns:
            List of successful uploads with CIDs and gateway URLs
        """
        dir_path = Path(dir_path)
        
        if not dir_path.is_dir():
            logger.error(f"Directory not found: {dir_path}")
            return []
            
        results = []
        
        # Add directory info to metadata
        if metadata is None:
            metadata = {}
            
        metadata["directory"] = str(dir_path)
        metadata["dir_basename"] = dir_path.name
        
        # Upload each file
        for file_path in dir_path.glob("*"):
            if file_path.is_file():
                # Add file-specific metadata
                file_metadata = metadata.copy()
                file_metadata["parent_dir"] = dir_path.name
                
                # Queue the upload
                self.queue_upload(
                    file_path, 
                    f"{artifact_type}_{file_path.name}", 
                    file_metadata
                )
                
                # Note: We don't have immediate results since uploads are queued
                results.append({
                    "queued_file": str(file_path),
                    "status": "queued"
                })
                
        return results
    
    def retrieve_pins(
        self, 
        artifact_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve information about pinned content.
        
        Args:
            artifact_type: Filter by artifact type
            limit: Maximum number of results
            
        Returns:
            List of pin data
        """
        if not self.api_authenticated:
            logger.warning("Cannot retrieve pins: No Pinata API credentials")
            return []
            
        try:
            url = f"{self.base_url}/data/pinList"
            params = {"status": "pinned", "limit": limit}
            
            if artifact_type:
                # Filter by metadata
                params["metadata[keyvalues]"] = json.dumps({
                    "artifact_type": {
                        "value": artifact_type,
                        "op": "eq"
                    }
                })
                
            response = requests.get(
                url,
                params=params,
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                pins = response.json().get("rows", [])
                
                # Add gateway URLs to the results
                for pin in pins:
                    pin["gateway_url"] = self.get_gateway_url(pin.get("ipfs_pin_hash", ""))
                    
                return pins
            else:
                logger.error(
                    f"Failed to retrieve pins. "
                    f"Status: {response.status_code}, Response: {response.text}"
                )
                return []
                
        except Exception as e:
            logger.error(f"Error retrieving pins: {e}")
            return []
    
    def unpin(self, ipfs_hash: str) -> bool:
        """
        Remove a pin from Pinata.
        
        Args:
            ipfs_hash: IPFS hash/CID to unpin
            
        Returns:
            True if successful, False otherwise
        """
        if not self.api_authenticated:
            logger.warning("Cannot unpin: No Pinata API credentials")
            return False
            
        try:
            url = f"{self.base_url}/pinning/unpin/{ipfs_hash}"
            
            response = requests.delete(
                url,
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                logger.info(f"Successfully unpinned {ipfs_hash}")
                return True
            else:
                logger.error(
                    f"Failed to unpin {ipfs_hash}. "
                    f"Status: {response.status_code}, Response: {response.text}"
                )
                return False
                
        except Exception as e:
            logger.error(f"Error unpinning {ipfs_hash}: {e}")
            return False
    
    def publish_test_results(
        self, 
        results_dir: Union[str, Path],
        test_name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Publish test results to IPFS.
        
        Args:
            results_dir: Directory containing test results
            test_name: Name of the test run
            metadata: Additional metadata
            
        Returns:
            Dictionary with upload results
        """
        results_dir = Path(results_dir)
        
        if not results_dir.is_dir():
            logger.error(f"Results directory not found: {results_dir}")
            return {"status": "error", "message": "Results directory not found"}
            
        # Prepare metadata
        if metadata is None:
            metadata = {}
            
        metadata["test_name"] = test_name
        metadata["timestamp"] = time.time()
        metadata["datetime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Upload the directory
        upload_results = self.upload_directory(
            results_dir,
            artifact_type="test_results",
            metadata=metadata
        )
        
        return {
            "status": "queued" if upload_results else "error",
            "test_name": test_name,
            "files_queued": len(upload_results),
            "results_dir": str(results_dir),
            "queued_files": upload_results
        } 