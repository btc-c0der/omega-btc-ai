#!/usr/bin/env python3
"""
NFT QA Service for Quantum Test Runner V2
----------------------------------------

This service enables turning test results into NFTs for on-chain verification.
It provides capabilities to:
1. Mint test reports as NFTs
2. Create on-chain verification of test coverage
3. Link IPFS reports to blockchain tokens
4. Generate proof of testing certificates
"""

import os
import json
import time
import logging
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import threading
import uuid

logger = logging.getLogger("quantum_runner_v2.nft_qa_service")


class NFTQAService:
    """
    Service to mint test results as NFTs for on-chain verification.
    
    This enables blockchain-based proof of:
    - Test completion
    - Coverage thresholds
    - AI model validation
    - Security scanning
    """
    
    def __init__(
        self, 
        ipfs_service=None,
        api_key: Optional[str] = None,
        contract_address: Optional[str] = None,
        network: str = "testnet"
    ):
        """
        Initialize the NFT QA service.
        
        Args:
            ipfs_service: Reference to IPFS service for content storage
            api_key: API key for NFT minting service (uses env var NFT_API_KEY if not provided)
            contract_address: Smart contract address for NFT minting
            network: Blockchain network to use ("testnet" or "mainnet")
        """
        self.ipfs_service = ipfs_service
        self.api_key = api_key or os.environ.get("NFT_API_KEY")
        self.contract_address = contract_address or os.environ.get("NFT_CONTRACT_ADDRESS")
        self.network = network
        self.running = False
        self._mint_queue = []
        self._lock = threading.Lock()
        self._worker_thread = None
        
        # Base URL for API calls
        if network == "mainnet":
            self.base_url = "https://api.nft.service/v1"
        else:
            self.base_url = "https://testnet-api.nft.service/v1"
        
        # Check credentials
        if not self.api_key:
            logger.warning(
                "NFT QA Service initialized without API key. "
                "Set NFT_API_KEY environment variable for full functionality."
            )
            self.api_authenticated = False
        else:
            self.api_authenticated = True
    
    def start(self):
        """Start the NFT QA service."""
        if self.running:
            return
            
        self.running = True
        logger.info(f"NFT QA Service started on {self.network}")
        
        # Start background worker thread for minting queue
        self._worker_thread = threading.Thread(
            target=self._process_queue, 
            daemon=True
        )
        self._worker_thread.start()
    
    def stop(self):
        """Stop the NFT QA service."""
        if not self.running:
            return
            
        self.running = False
        logger.info("NFT QA Service stopped")
        
        # Wait for worker thread to finish current operations
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=5.0)
    
    def _get_headers(self) -> Dict[str, str]:
        """Get API headers with authentication."""
        if not self.api_authenticated:
            raise ValueError("NFT API key not configured")
            
        return {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def _process_queue(self):
        """Process the minting queue in background."""
        while self.running:
            # Check if there's anything in the queue
            with self._lock:
                if not self._mint_queue:
                    time.sleep(1)
                    continue
                
                # Get the next item
                metadata, recipient, token_id = self._mint_queue.pop(0)
            
            # Process the mint
            try:
                self._mint_nft(metadata, recipient, token_id)
            except Exception as e:
                logger.error(f"Failed to mint NFT: {e}")
                
            # Small delay between mints
            time.sleep(0.5)
    
    def _mint_nft(
        self, 
        metadata: Dict[str, Any],
        recipient: str,
        token_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Mint an NFT with test result metadata.
        
        Args:
            metadata: NFT metadata with test information
            recipient: Wallet address to receive the NFT
            token_id: Optional token ID, generated if not provided
            
        Returns:
            Response data if successful, None otherwise
        """
        if not self.api_authenticated:
            logger.warning("Cannot mint NFT: No API key")
            return None
            
        if not self.contract_address:
            logger.warning("Cannot mint NFT: No contract address")
            return None
            
        # Generate token ID if not provided
        if not token_id:
            token_id = str(uuid.uuid4())
            
        try:
            url = f"{self.base_url}/mint"
            
            # Prepare request data
            data = {
                "contract_address": self.contract_address,
                "recipient": recipient,
                "token_id": token_id,
                "metadata": metadata
            }
            
            # Make the request
            response = requests.post(
                url, 
                json=data,
                headers=self._get_headers()
            )
            
            if response.status_code in (200, 201, 202):
                result = response.json()
                logger.info(f"Successfully minted NFT with token ID {token_id}")
                return result
            else:
                logger.error(
                    f"Failed to mint NFT. "
                    f"Status: {response.status_code}, Response: {response.text}"
                )
                return None
                
        except Exception as e:
            logger.error(f"Error minting NFT: {e}")
            return None
            
    def _prepare_test_nft_metadata(
        self,
        test_name: str,
        ipfs_hash: str,
        results: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Prepare metadata for a test result NFT.
        
        Args:
            test_name: Name of the test
            ipfs_hash: IPFS hash of the test report
            results: Test results summary
            metadata: Additional metadata
            
        Returns:
            NFT metadata object
        """
        # Base metadata
        nft_metadata = {
            "name": f"QA Test Certificate: {test_name}",
            "description": f"This NFT certifies the completion and results of {test_name}",
            "external_url": f"https://copper-far-catshark-208.mypinata.cloud/ipfs/{ipfs_hash}",
            "image": "https://copper-far-catshark-208.mypinata.cloud/ipfs/QmdefaultImageCID",  # Placeholder
            "attributes": [
                {
                    "trait_type": "Test Name",
                    "value": test_name
                },
                {
                    "trait_type": "Test Date",
                    "value": time.strftime("%Y-%m-%d")
                },
                {
                    "trait_type": "Test Time",
                    "value": time.strftime("%H:%M:%S")
                },
                {
                    "trait_type": "Verification Method",
                    "value": "Quantum Test Runner V2"
                }
            ]
        }
        
        # Add result metrics as attributes
        if "passed" in results:
            nft_metadata["attributes"].append({
                "trait_type": "Tests Passed",
                "value": results["passed"],
                "display_type": "number"
            })
            
        if "failed" in results:
            nft_metadata["attributes"].append({
                "trait_type": "Tests Failed",
                "value": results["failed"],
                "display_type": "number"
            })
            
        if "coverage" in results:
            nft_metadata["attributes"].append({
                "trait_type": "Code Coverage",
                "value": results["coverage"],
                "display_type": "percentage"
            })
            
        # Add pass/fail status
        if "status" in results:
            nft_metadata["attributes"].append({
                "trait_type": "Overall Status",
                "value": results["status"]
            })
            
        # Add IPFS reference
        nft_metadata["attributes"].append({
            "trait_type": "IPFS Report",
            "value": ipfs_hash
        })
        
        # Add additional metadata
        if metadata:
            # Add custom attributes
            for key, value in metadata.items():
                if key not in nft_metadata and key != "attributes":
                    nft_metadata[key] = value
                    
            # Add custom attributes
            if "attributes" in metadata and isinstance(metadata["attributes"], list):
                nft_metadata["attributes"].extend(metadata["attributes"])
        
        return nft_metadata
    
    def queue_mint(
        self, 
        metadata: Dict[str, Any],
        recipient: str,
        token_id: Optional[str] = None
    ):
        """
        Queue an NFT for minting.
        
        Args:
            metadata: NFT metadata
            recipient: Wallet address to receive the NFT
            token_id: Optional token ID
        """
        with self._lock:
            self._mint_queue.append((metadata, recipient, token_id))
            
        logger.debug(f"Queued NFT mint for {recipient}")
    
    def mint_test_results(
        self,
        test_name: str,
        results: Dict[str, Any],
        ipfs_hash: Optional[str] = None,
        ipfs_report_path: Optional[Union[str, Path]] = None,
        recipient: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Mint test results as an NFT.
        
        Args:
            test_name: Name of the test
            results: Test results summary
            ipfs_hash: IPFS hash of the test report (if already uploaded)
            ipfs_report_path: Path to report file to upload to IPFS (if not already uploaded)
            recipient: Wallet address to receive the NFT
            metadata: Additional metadata
            
        Returns:
            Status information
        """
        # Check recipient
        if not recipient:
            recipient = os.environ.get("DEFAULT_NFT_RECIPIENT")
            if not recipient:
                logger.error("No recipient specified and no DEFAULT_NFT_RECIPIENT env var")
                return {"status": "error", "message": "No recipient specified"}
                
        # Upload report to IPFS if needed
        if not ipfs_hash and ipfs_report_path and self.ipfs_service:
            logger.info(f"Uploading test report to IPFS: {ipfs_report_path}")
            try:
                upload_result = self.ipfs_service.upload_artifact(
                    file_path=ipfs_report_path,
                    artifact_type="test_report",
                    metadata={"test_name": test_name}
                )
                
                if upload_result:
                    ipfs_hash = upload_result.get("ipfs_hash")
                    logger.info(f"Report uploaded to IPFS: {ipfs_hash}")
                else:
                    logger.error("Failed to upload report to IPFS")
                    return {"status": "error", "message": "IPFS upload failed"}
            except Exception as e:
                logger.error(f"Error uploading to IPFS: {e}")
                return {"status": "error", "message": str(e)}
        
        # If we don't have an IPFS hash, we can't proceed
        if not ipfs_hash:
            logger.error("No IPFS hash provided or generated")
            return {"status": "error", "message": "No IPFS hash for test results"}
            
        # Prepare NFT metadata
        nft_metadata = self._prepare_test_nft_metadata(
            test_name=test_name,
            ipfs_hash=ipfs_hash,
            results=results,
            metadata=metadata
        )
        
        # Queue the NFT minting
        token_id = f"qa-{int(time.time())}-{test_name.replace(' ', '-')}"
        self.queue_mint(nft_metadata, recipient, token_id)
        
        return {
            "status": "queued",
            "test_name": test_name,
            "token_id": token_id,
            "recipient": recipient,
            "ipfs_hash": ipfs_hash
        }
    
    def generate_qa_certificate(
        self,
        test_name: str,
        results: Dict[str, Any],
        ipfs_hash: str,
        recipient: str,
        certificate_template: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a QA certificate as an NFT.
        
        Args:
            test_name: Name of the test
            results: Test results summary
            ipfs_hash: IPFS hash of the test report
            recipient: Wallet address to receive the certificate
            certificate_template: Template ID for certificate (uses default if not specified)
            
        Returns:
            Certificate information
        """
        # Additional certificate metadata
        certificate_metadata = {
            "certificate_type": "Divine QA Certification",
            "verification_level": "Quantum Verified",
            "certificate_id": f"QA-CERT-{uuid.uuid4().hex[:8]}",
            "attributes": [
                {
                    "trait_type": "Certificate Type",
                    "value": "Divine QA Certification"
                },
                {
                    "trait_type": "Verification Level",
                    "value": "Quantum Verified"
                }
            ]
        }
        
        # Add template if specified
        if certificate_template:
            certificate_metadata["template"] = certificate_template
            
        # Mint as NFT
        return self.mint_test_results(
            test_name=test_name,
            results=results,
            ipfs_hash=ipfs_hash,
            recipient=recipient,
            metadata=certificate_metadata
        ) 