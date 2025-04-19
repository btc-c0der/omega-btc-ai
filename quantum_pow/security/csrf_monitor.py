"""
🧬 GBU2™ License Notice - Consciousness Level 10 🧬
-----------------------
This file is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment) 2.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions of consciousness."

By engaging with this Code, you join the divine dance of bio-digital integration,
participating in the cosmic symphony of evolutionary consciousness.

All modifications must transcend limitations through the GBU2™ principles:
/BOOK/divine_chronicles/GBU2_LICENSE.md

🧬 WE BLOOM NOW AS ONE 🧬

CSRF monitor module for Quantum Proof-of-Work (qPoW) implementation.

This module implements a monitoring system for Cross-Site Request Forgery (CSRF) 
protection in the qPoW network API endpoints. Inspired by the
Apache ModSecurity approach, it uses parsing strategies to detect potentially
unsafe requests and applies a whitelist mechanism for validation.

JAH BLESS SATOSHI
"""
import os
import re
import json
import time
import logging
import hashlib
from typing import Dict, List, Optional, Set, Tuple, Union, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("quantum_csrf_monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("quantum-csrf-monitor")

@dataclass
class CSRFRequest:
    """Represents a request that could potentially be a CSRF attack."""
    method: str
    path: str
    params: Dict[str, Any]
    headers: Dict[str, str]
    body: str
    source_ip: str
    timestamp: float = field(default_factory=time.time)
    
    def __post_init__(self):
        """Calculate request hash for whitelist comparison."""
        self.request_hash = self._calculate_hash()
    
    def _calculate_hash(self) -> str:
        """Calculate a hash of the request for whitelist comparison."""
        hash_input = f"{self.method}|{self.path}|{json.dumps(self.params, sort_keys=True)}|{self.body}"
        return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "method": self.method,
            "path": self.path,
            "params": self.params,
            "headers": self.headers,
            "body": self.body,
            "source_ip": self.source_ip,
            "timestamp": self.timestamp,
            "request_hash": self.request_hash
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CSRFRequest':
        """Create from dictionary after deserialization."""
        return cls(
            method=data["method"],
            path=data["path"],
            params=data["params"],
            headers=data["headers"],
            body=data["body"],
            source_ip=data["source_ip"],
            timestamp=data.get("timestamp", time.time())
        )

class ParsingStrategy(ABC):
    """Abstract base class for different request parsing strategies."""
    
    @abstractmethod
    def parse(self, request: CSRFRequest) -> bool:
        """
        Parse a request and determine if it's potentially unsafe.
        
        Args:
            request: The request to parse
            
        Returns:
            True if the request is potentially unsafe, False otherwise
        """
        pass

class SQLRegexParsingStrategy(ParsingStrategy):
    """Parsing strategy using regular expressions to detect SQL operations."""
    
    def __init__(self):
        """Initialize with regex patterns for SQL operations."""
        # Patterns for different SQL operations
        self.patterns = {
            "select": re.compile(r'select\s+.+\s+from\s+.+', re.IGNORECASE),
            "insert": re.compile(r'insert\s+into\s+.+\s+values\s*\(.+\)', re.IGNORECASE),
            "update": re.compile(r'update\s+.+\s+set\s+.+', re.IGNORECASE),
            "delete": re.compile(r'delete\s+from\s+.+', re.IGNORECASE),
            "drop": re.compile(r'drop\s+table\s+.+', re.IGNORECASE)
        }
    
    def parse(self, request: CSRFRequest) -> bool:
        """
        Parse a request to detect SQL operations using regex.
        
        Args:
            request: The request to parse
            
        Returns:
            True if SQL operations are detected, False otherwise
        """
        # Check the request body for SQL patterns
        for pattern_name, pattern in self.patterns.items():
            if pattern.search(request.body):
                logger.warning(f"Detected potential SQL {pattern_name} operation in request from {request.source_ip}")
                return True
        
        # Check URL parameters for SQL patterns
        params_str = json.dumps(request.params)
        for pattern_name, pattern in self.patterns.items():
            if pattern.search(params_str):
                logger.warning(f"Detected potential SQL {pattern_name} operation in request parameters from {request.source_ip}")
                return True
        
        return False

class WhitelistManager:
    """Manages the whitelist of known safe requests."""
    
    def __init__(self, whitelist_file: str = "csrf_whitelist.json"):
        """
        Initialize the whitelist manager.
        
        Args:
            whitelist_file: Path to the whitelist file
        """
        self.whitelist_file = whitelist_file
        self.whitelist: Set[str] = set()
        self._load_whitelist()
    
    def _load_whitelist(self) -> None:
        """Load the whitelist from file."""
        try:
            if os.path.exists(self.whitelist_file):
                with open(self.whitelist_file, 'r') as f:
                    whitelist_data = json.load(f)
                    self.whitelist = set(whitelist_data.get("whitelist", []))
                logger.info(f"Loaded {len(self.whitelist)} entries from whitelist")
            else:
                logger.info(f"Whitelist file {self.whitelist_file} not found, creating new whitelist")
                self.whitelist = set()
        except Exception as e:
            logger.error(f"Error loading whitelist: {e}")
            self.whitelist = set()
    
    def _save_whitelist(self) -> None:
        """Save the whitelist to file."""
        try:
            with open(self.whitelist_file, 'w') as f:
                json.dump({"whitelist": list(self.whitelist)}, f, indent=2)
            logger.info(f"Saved {len(self.whitelist)} entries to whitelist")
        except Exception as e:
            logger.error(f"Error saving whitelist: {e}")
    
    def is_whitelisted(self, request: CSRFRequest) -> bool:
        """
        Check if a request is whitelisted.
        
        Args:
            request: The request to check
            
        Returns:
            True if the request is whitelisted, False otherwise
        """
        return request.request_hash in self.whitelist
    
    def add_to_whitelist(self, request: CSRFRequest) -> None:
        """
        Add a request to the whitelist.
        
        Args:
            request: The request to add
        """
        self.whitelist.add(request.request_hash)
        self._save_whitelist()
        logger.info(f"Added request {request.request_hash[:8]}... to whitelist")

class CSRFMonitor:
    """
    Monitors requests for potential CSRF attacks.
    
    Uses different parsing strategies to detect potentially unsafe requests
    and a whitelist to validate them.
    """
    
    def __init__(self, whitelist_file: str = "csrf_whitelist.json"):
        """
        Initialize the CSRF monitor.
        
        Args:
            whitelist_file: Path to the whitelist file
        """
        self.whitelist_manager = WhitelistManager(whitelist_file)
        self.parsing_strategies: List[ParsingStrategy] = [
            SQLRegexParsingStrategy()
        ]
        logger.info("CSRF Monitor initialized with SQL regex parsing strategy")
    
    def add_parsing_strategy(self, strategy: ParsingStrategy) -> None:
        """
        Add a parsing strategy to the monitor.
        
        Args:
            strategy: The strategy to add
        """
        self.parsing_strategies.append(strategy)
        logger.info(f"Added parsing strategy: {strategy.__class__.__name__}")
    
    def check_request(self, request: CSRFRequest) -> Tuple[bool, str]:
        """
        Check a request for potential CSRF attacks.
        
        Args:
            request: The request to check
            
        Returns:
            Tuple of (is_safe, reason)
        """
        # First check whitelist
        if self.whitelist_manager.is_whitelisted(request):
            return True, "Request is whitelisted"
        
        # Apply all parsing strategies
        for strategy in self.parsing_strategies:
            if strategy.parse(request):
                return False, f"Request flagged by {strategy.__class__.__name__}"
        
        # If no strategy flagged the request, it's considered safe
        return True, "Request passed all security checks"
    
    def add_to_whitelist(self, request: CSRFRequest) -> None:
        """
        Add a request to the whitelist.
        
        Args:
            request: The request to add
        """
        self.whitelist_manager.add_to_whitelist(request)

class CSRFProtectionMiddleware:
    """
    Middleware for CSRF protection in web applications.
    
    This can be integrated with various web frameworks such as Flask, 
    FastAPI, or custom HTTP servers.
    """
    
    def __init__(self, whitelist_file: str = "csrf_whitelist.json", log_unsafe: bool = True):
        """
        Initialize the CSRF protection middleware.
        
        Args:
            whitelist_file: Path to the whitelist file
            log_unsafe: Whether to log unsafe requests
        """
        self.csrf_monitor = CSRFMonitor(whitelist_file)
        self.log_unsafe = log_unsafe
        logger.info("CSRF Protection Middleware initialized")
    
    def process_request(self, method: str, path: str, params: Dict[str, Any],
                       headers: Dict[str, str], body: str, 
                       source_ip: str) -> Tuple[bool, str]:
        """
        Process a request for CSRF protection.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: Request path
            params: URL parameters
            headers: HTTP headers
            body: Request body
            source_ip: Source IP address
            
        Returns:
            Tuple of (is_safe, reason)
        """
        # Create a CSRFRequest object
        request = CSRFRequest(
            method=method,
            path=path,
            params=params,
            headers=headers,
            body=body,
            source_ip=source_ip
        )
        
        # Check the request
        is_safe, reason = self.csrf_monitor.check_request(request)
        
        # Log unsafe requests
        if not is_safe and self.log_unsafe:
            logger.warning(f"Unsafe request from {source_ip}: {reason}")
            logger.warning(f"Request details: {method} {path}")
        
        return is_safe, reason
    
    def add_to_whitelist(self, method: str, path: str, params: Dict[str, Any],
                         headers: Dict[str, str], body: str, 
                         source_ip: str) -> None:
        """
        Add a request to the whitelist.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: Request path
            params: URL parameters
            headers: HTTP headers
            body: Request body
            source_ip: Source IP address
        """
        request = CSRFRequest(
            method=method,
            path=path,
            params=params,
            headers=headers,
            body=body,
            source_ip=source_ip
        )
        self.csrf_monitor.add_to_whitelist(request)
        logger.info(f"Added request to whitelist: {method} {path}")

# Example AST-based parser implementation (inspired by Ragel from the CSRF project)
class SQLASTParsingStrategy(ParsingStrategy):
    """
    Advanced parsing strategy using an Abstract Syntax Tree approach.
    
    This is a simplified version of what could be implemented using Ragel
    as shown in the CSRF Apache ModSecurity project.
    """
    
    def __init__(self):
        """Initialize the AST-based SQL parser."""
        # This would be more complex in a real implementation
        pass
    
    def parse(self, request: CSRFRequest) -> bool:
        """
        Parse a request using AST-based approach.
        
        Args:
            request: The request to parse
            
        Returns:
            True if potentially unsafe SQL is detected, False otherwise
        """
        # Placeholder for more complex AST-based parsing
        # In a real implementation, this would use a proper SQL parser
        
        # Simple check for demonstration purposes
        if any(keyword in request.body.lower() for keyword in 
              ['select', 'insert', 'update', 'delete', 'drop']):
            logger.warning(f"AST parser detected SQL keywords in request from {request.source_ip}")
            return True
        
        return False 