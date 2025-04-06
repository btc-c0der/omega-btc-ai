#!/usr/bin/env python3
"""
IPFS Pinata Integration for Quantum Test Runner V2
------------------------------------------------

This module provides utilities to integrate test runners with IPFS via Pinata.
It includes:
1. Helper functions to upload test artifacts
2. Utilities to generate gateway URLs
3. Functions for batching uploads
4. Verification tools for content integrity
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

# Local imports
from .ipfs_service import IPFSService

logger = logging.getLogger("quantum_runner_v2.ipfs_pinata_integration")


def configure_services(
    ipfs_service: Optional[IPFSService] = None,
    api_key: Optional[str] = None,
    api_secret: Optional[str] = None,
    gateway_url: Optional[str] = None
) -> IPFSService:
    """
    Configure IPFS service for Pinata integration.
    
    Args:
        ipfs_service: Existing IPFS service to use (creates new if None)
        api_key: Pinata API key
        api_secret: Pinata API secret
        gateway_url: Custom gateway URL
        
    Returns:
        Configured IPFS service
    """
    # Use existing service or create new one
    if ipfs_service is None:
        # Use provided credentials or environment variables
        ipfs_service = IPFSService(
            api_key=api_key,
            api_secret=api_secret,
            gateway_url=gateway_url or "https://copper-far-catshark-208.mypinata.cloud/ipfs"
        )
        ipfs_service.start()
        
    return ipfs_service


def upload_test_report(
    report_path: Union[str, Path],
    ipfs_service: IPFSService,
    test_metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Upload a test report to IPFS.
    
    Args:
        report_path: Path to the test report file
        ipfs_service: IPFS service instance
        test_metadata: Additional test metadata
        
    Returns:
        Upload result with IPFS hash and gateway URL
    """
    report_path = Path(report_path)
    
    if not report_path.exists():
        logger.error(f"Test report not found: {report_path}")
        return {
            "status": "error",
            "message": f"Test report not found: {report_path}",
            "path": str(report_path)
        }
    
    # Prepare metadata
    metadata = {
        "source": "quantum_runner_v2",
        "file_type": report_path.suffix.lstrip("."),
        "timestamp": time.time(),
        "datetime": time.strftime("%Y-%m-%d %H:%M:%S"),
        "artifact_type": "test_report"
    }
    
    # Add test metadata if provided
    if test_metadata:
        metadata.update(test_metadata)
    
    # Upload the file
    try:
        result = ipfs_service.upload_artifact(
            file_path=report_path,
            artifact_type="test_report",
            metadata=metadata
        )
        
        if result:
            logger.info(f"Test report uploaded to IPFS: {result.get('ipfs_hash')}")
            return {
                "status": "success",
                "ipfs_hash": result.get("ipfs_hash"),
                "gateway_url": result.get("gateway_url"),
                "file": str(report_path)
            }
        else:
            logger.error(f"Failed to upload test report: {report_path}")
            return {
                "status": "error",
                "message": "Upload failed",
                "path": str(report_path)
            }
    
    except Exception as e:
        logger.error(f"Error uploading test report: {e}")
        return {
            "status": "error",
            "message": str(e),
            "path": str(report_path)
        }


def create_result_gateway_url(ipfs_hash: str, gateway_url: Optional[str] = None) -> str:
    """
    Create a gateway URL for an IPFS hash.
    
    Args:
        ipfs_hash: IPFS hash/CID
        gateway_url: Custom gateway URL (uses default if None)
        
    Returns:
        Complete gateway URL
    """
    base_url = gateway_url or "https://copper-far-catshark-208.mypinata.cloud/ipfs"
    base_url = base_url.rstrip("/")
    
    return f"{base_url}/{ipfs_hash}"


def upload_test_artifacts(
    artifacts_dir: Union[str, Path],
    ipfs_service: IPFSService,
    metadata: Optional[Dict[str, Any]] = None,
    patterns: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Upload multiple test artifacts to IPFS.
    
    Args:
        artifacts_dir: Directory containing test artifacts
        ipfs_service: IPFS service instance
        metadata: Additional metadata
        patterns: File patterns to include (e.g., ["*.json", "*.html"])
        
    Returns:
        Upload results
    """
    artifacts_dir = Path(artifacts_dir)
    
    if not artifacts_dir.is_dir():
        logger.error(f"Artifacts directory not found: {artifacts_dir}")
        return {
            "status": "error",
            "message": f"Directory not found: {artifacts_dir}"
        }
    
    # Find files to upload
    files_to_upload = []
    
    if patterns:
        # Use specified patterns
        for pattern in patterns:
            files_to_upload.extend(list(artifacts_dir.glob(pattern)))
    else:
        # Use all files
        files_to_upload = [f for f in artifacts_dir.iterdir() if f.is_file()]
    
    if not files_to_upload:
        logger.warning(f"No files found in {artifacts_dir}")
        return {
            "status": "warning",
            "message": "No files found",
            "directory": str(artifacts_dir)
        }
    
    # Upload each file
    upload_results = []
    
    for file_path in files_to_upload:
        # Prepare file-specific metadata
        file_metadata = {
            "source": "quantum_runner_v2",
            "file_type": file_path.suffix.lstrip("."),
            "parent_dir": artifacts_dir.name,
            "artifact_type": "test_artifact"
        }
        
        # Add common metadata
        if metadata:
            file_metadata.update(metadata)
        
        # Queue the upload
        ipfs_service.queue_upload(
            file_path=file_path,
            name=f"artifact_{file_path.name}",
            metadata=file_metadata
        )
        
        upload_results.append({
            "file": str(file_path),
            "status": "queued"
        })
    
    return {
        "status": "queued",
        "files_queued": len(upload_results),
        "directory": str(artifacts_dir),
        "queued_files": upload_results
    }


def verify_ipfs_content(
    ipfs_hash: str,
    local_file: Union[str, Path],
    ipfs_service: Optional[IPFSService] = None
) -> Dict[str, Any]:
    """
    Verify that IPFS content matches a local file.
    
    Args:
        ipfs_hash: IPFS hash/CID to verify
        local_file: Local file to compare against
        ipfs_service: IPFS service (for gateway URL)
        
    Returns:
        Verification result
    """
    local_file = Path(local_file)
    
    if not local_file.exists():
        return {
            "status": "error",
            "message": f"Local file not found: {local_file}",
            "verified": False
        }
    
    # Calculate hash of local file
    try:
        sha256 = hashlib.sha256()
        
        with open(local_file, "rb") as f:
            # Read in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
                
        local_hash = sha256.hexdigest()
        
        # Get gateway URL
        gateway_url = None
        if ipfs_service:
            gateway_url = ipfs_service.get_gateway_url(ipfs_hash)
        else:
            gateway_url = create_result_gateway_url(ipfs_hash)
        
        # Fetch the IPFS content to verify
        try:
            response = requests.get(gateway_url, timeout=30)
            
            if response.status_code == 200:
                # Calculate hash of content
                content_hash = hashlib.sha256(response.content).hexdigest()
                
                # Compare hashes
                if content_hash == local_hash:
                    return {
                        "status": "success",
                        "verified": True,
                        "ipfs_hash": ipfs_hash,
                        "gateway_url": gateway_url,
                        "local_file": str(local_file)
                    }
                else:
                    return {
                        "status": "error",
                        "message": "Content hash mismatch",
                        "verified": False,
                        "ipfs_hash": ipfs_hash,
                        "local_hash": local_hash,
                        "content_hash": content_hash
                    }
                    
            else:
                return {
                    "status": "error",
                    "message": f"Failed to fetch IPFS content: {response.status_code}",
                    "verified": False,
                    "ipfs_hash": ipfs_hash
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error fetching IPFS content: {str(e)}",
                "verified": False,
                "ipfs_hash": ipfs_hash
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error calculating local file hash: {str(e)}",
            "verified": False,
            "local_file": str(local_file)
        }


def upload_coverage_report(
    coverage_path: Union[str, Path],
    test_name: str,
    ipfs_service: IPFSService,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Upload a coverage report to IPFS.
    
    Args:
        coverage_path: Path to coverage report file
        test_name: Name of the test
        ipfs_service: IPFS service instance
        metadata: Additional metadata
        
    Returns:
        Upload result
    """
    # Prepare coverage-specific metadata
    coverage_metadata = {
        "test_name": test_name,
        "artifact_type": "coverage_report",
        "timestamp": time.time(),
        "datetime": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Add additional metadata
    if metadata:
        coverage_metadata.update(metadata)
    
    # Upload the coverage report
    return upload_test_report(
        report_path=coverage_path,
        ipfs_service=ipfs_service,
        test_metadata=coverage_metadata
    )


def upload_test_run_batch(
    test_dir: Union[str, Path],
    ipfs_service: IPFSService,
    test_name: str,
    include_patterns: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Upload a batch of test run artifacts.
    
    Args:
        test_dir: Directory containing test artifacts
        ipfs_service: IPFS service instance
        test_name: Name of the test run
        include_patterns: File patterns to include
        metadata: Additional metadata
        
    Returns:
        Batch upload results
    """
    test_dir = Path(test_dir)
    
    if not test_dir.is_dir():
        logger.error(f"Test directory not found: {test_dir}")
        return {
            "status": "error",
            "message": f"Test directory not found: {test_dir}"
        }
    
    # Default patterns if none provided
    if not include_patterns:
        include_patterns = ["*.json", "*.html", "*.xml", "*.log"]
    
    # Prepare batch metadata
    batch_metadata = {
        "test_name": test_name,
        "batch_id": f"batch_{int(time.time())}",
        "source": "quantum_runner_v2"
    }
    
    # Add additional metadata
    if metadata:
        batch_metadata.update(metadata)
    
    # Upload the batch
    return upload_test_artifacts(
        artifacts_dir=test_dir,
        ipfs_service=ipfs_service,
        metadata=batch_metadata,
        patterns=include_patterns
    )


def get_ipfs_status(ipfs_service: IPFSService) -> Dict[str, Any]:
    """
    Get status information about IPFS service.
    
    Args:
        ipfs_service: IPFS service instance
        
    Returns:
        Status information
    """
    status = {
        "service_running": ipfs_service.running,
        "api_authenticated": ipfs_service.api_authenticated,
        "gateway_url": ipfs_service.gateway_url,
        "queue_size": len(ipfs_service._upload_queue) if hasattr(ipfs_service, "_upload_queue") else 0
    }
    
    # Try to get recent pins
    try:
        pins = ipfs_service.retrieve_pins(limit=5)
        status["recent_pins"] = pins
        status["recent_pin_count"] = len(pins)
    except Exception as e:
        status["pin_retrieval_error"] = str(e)
    
    return status 