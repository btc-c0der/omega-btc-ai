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

Quantum Authentication Server for Quantum Proof-of-Work (qPoW) implementation.

This module implements a FastAPI server that provides REST API endpoints
for the quantum-resistant authentication system, allowing validators to
authenticate using one-shot signatures and other post-quantum cryptographic techniques.
Based on research from "One-shot signatures and applications to hybrid quantum/classical
authentication" (R. Amos et al.).

JAH BLESS SATOSHI
"""
import os
import json
import time
import random
import logging
import argparse
import hashlib
import uuid
from typing import Dict, List, Set, Tuple, Optional, Any, Union
from datetime import datetime, timezone
from enum import Enum

# For using FastAPI
try:
    from fastapi import FastAPI, Request, Response, HTTPException, Depends, BackgroundTasks, status
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel, Field
    import uvicorn
except ImportError:
    raise ImportError("FastAPI and uvicorn required. Install with: pip install fastapi uvicorn")

# Import quantum-resistant authentication components
from quantum_pow.security.quantum_resistant_auth import (
    SignatureScheme,
    KeyPair,
    OneTimeToken,
    QuantumResistantAuth
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("quantum_auth_server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("quantum-auth-server")

# Set log level from environment variable
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.getLogger().setLevel(getattr(logging, log_level))

# Convert SignatureScheme enum to a list of strings for validation
SIGNATURE_SCHEMES = [scheme.value for scheme in SignatureScheme]

# Pydantic models for API request/response
class GenerateKeyPairRequest(BaseModel):
    scheme: str = Field(default="one_shot", description="Signature scheme to use")
    expiration_days: Optional[float] = Field(default=None, description="Expiration period in days")
    validator_id: str = Field(description="ID of the validator")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

class KeyPairResponse(BaseModel):
    key_id: str = Field(description="ID of the generated key pair")
    public_key: str = Field(description="Public key")
    scheme: str = Field(description="Signature scheme used")
    expiration_time: Optional[float] = Field(default=None, description="Expiration time as Unix timestamp")
    creation_time: float = Field(description="Creation time as Unix timestamp")

class SignMessageRequest(BaseModel):
    key_id: str = Field(description="ID of the key pair to use for signing")
    message: str = Field(description="Base64-encoded message to sign")
    validator_id: str = Field(description="ID of the validator")

class SignatureResponse(BaseModel):
    signature: str = Field(description="Base64-encoded signature")
    key_id: str = Field(description="ID of the key pair used for signing")
    scheme: str = Field(description="Signature scheme used")
    timestamp: float = Field(description="Timestamp of when the signature was created")

class VerifySignatureRequest(BaseModel):
    message: str = Field(description="Base64-encoded message")
    signature: str = Field(description="Base64-encoded signature")
    public_key: str = Field(description="Public key to verify against")
    scheme: str = Field(description="Signature scheme used")

class VerifySignatureResponse(BaseModel):
    is_valid: bool = Field(description="Whether the signature is valid")
    timestamp: float = Field(description="Timestamp of when the verification was performed")

class GenerateTokenRequest(BaseModel):
    purpose: str = Field(default="authentication", description="Purpose of the token")
    expiration_seconds: float = Field(default=300, description="Token expiration time in seconds")
    validator_id: str = Field(description="ID of the validator")

class TokenResponse(BaseModel):
    token_id: str = Field(description="ID of the generated token")
    token_value: str = Field(description="Token value")
    expiration_time: float = Field(description="Expiration time as Unix timestamp")

class ValidateTokenRequest(BaseModel):
    token_id: str = Field(description="ID of the token to validate")
    token_value: str = Field(description="Token value to validate")
    validator_id: str = Field(description="ID of the validator")

class RotationRequest(BaseModel):
    reason: str = Field(default="manual", description="Reason for key rotation")
    validator_id: Optional[str] = Field(default=None, description="ID of the validator (if specific)")

class RotationResponse(BaseModel):
    rotated_keys: Dict[str, int] = Field(description="Count of rotated keys by scheme")
    timestamp: float = Field(description="Timestamp of when the rotation was performed")

class ServerStats(BaseModel):
    node_id: str = Field(description="ID of the node")
    start_time: float = Field(description="Server start time as Unix timestamp")
    uptime_seconds: float = Field(description="Server uptime in seconds")
    key_count: int = Field(description="Number of active key pairs")
    token_count: int = Field(description="Number of active tokens")
    default_scheme: str = Field(description="Default signature scheme")

# Global state
app_state = {
    "start_time": time.time(),
    "node_id": os.environ.get("NODE_ID", f"node-{uuid.uuid4().hex[:8]}"),
    "config_file": os.environ.get("CONFIG_FILE", None),
    "validator_keys": {},  # Mapping of validator_id to list of key_ids
    "alert_count": 0,      # Count of security alerts
    "last_rotation": 0     # Timestamp of last emergency rotation
}

# Create FastAPI app
app = FastAPI(
    title="Quantum Authentication API",
    description="API for quantum-resistant authentication in the qPoW system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize authentication manager
auth_manager: Optional[QuantumResistantAuth] = None

@app.on_event("startup")
async def startup_event():
    """Initialize resources on server startup."""
    global auth_manager
    
    config_file = app_state["config_file"]
    
    # Load configuration if specified
    config = {}
    if config_file and os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
    
    # Initialize the authentication manager
    auth_manager = QuantumResistantAuth(config)
    
    logger.info(f"Quantum Authentication Server started with node ID: {app_state['node_id']}")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on server shutdown."""
    logger.info("Quantum Authentication Server stopped")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    if not auth_manager:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "reason": "Authentication manager not initialized"}
        )
    
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/ready")
async def ready_check():
    """Readiness check endpoint."""
    if not auth_manager:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not ready", "reason": "Authentication manager not initialized"}
        )
    
    return {
        "status": "ready",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/stats")
async def get_stats():
    """Get server statistics."""
    global auth_manager
    
    if not auth_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication manager not initialized"
        )
    
    uptime = time.time() - app_state["start_time"]
    key_count = len(auth_manager.key_pairs)
    token_count = len(auth_manager.one_time_tokens)
    
    stats = ServerStats(
        node_id=app_state["node_id"],
        start_time=app_state["start_time"],
        uptime_seconds=uptime,
        key_count=key_count,
        token_count=token_count,
        default_scheme=auth_manager.default_scheme.value
    )
    
    return stats

@app.post("/keys/generate", response_model=KeyPairResponse)
async def generate_key_pair(request: GenerateKeyPairRequest):
    """Generate a new quantum-resistant key pair."""
    global auth_manager
    
    if not auth_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication manager not initialized"
        )
    
    # Validate the signature scheme
    if request.scheme not in SIGNATURE_SCHEMES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid signature scheme. Must be one of: {', '.join(SIGNATURE_SCHEMES)}"
        )
    
    try:
        # Convert scheme string to enum
        scheme = SignatureScheme(request.scheme)
        
        # Generate the key pair
        key_pair = auth_manager.generate_keypair(scheme, request.expiration_days)
        
        # Generate key ID
        key_id = hashlib.sha256(key_pair.public_key.encode()).hexdigest()[:16]
        
        # Store the key ID in the validator's keys
        if request.validator_id not in app_state["validator_keys"]:
            app_state["validator_keys"][request.validator_id] = []
        app_state["validator_keys"][request.validator_id].append(key_id)
        
        # Add any additional metadata
        if request.metadata:
            key_pair.metadata.update(request.metadata)
        
        # Log key generation
        logger.info(f"Generated {scheme.value} key pair for validator {request.validator_id}: {key_id}")
        
        # Create the response
        return KeyPairResponse(
            key_id=key_id,
            public_key=key_pair.public_key,
            scheme=scheme.value,
            expiration_time=key_pair.expiration_time,
            creation_time=key_pair.creation_time
        )
    except Exception as e:
        logger.error(f"Error generating key pair: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating key pair: {str(e)}"
        )

@app.post("/sign", response_model=SignatureResponse)
async def sign_message(request: SignMessageRequest):
    """Sign a message using a quantum-resistant key pair."""
    global auth_manager
    
    if not auth_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication manager not initialized"
        )
    
    # Find the key pair
    key_id = request.key_id
    key_pair = None
    
    for kp in auth_manager.key_pairs.values():
        if hashlib.sha256(kp.public_key.encode()).hexdigest()[:16] == key_id:
            key_pair = kp
            break
    
    if not key_pair:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Key pair with ID {key_id} not found"
        )
    
    try:
        # Decode the message (assumed to be base64-encoded)
        import base64
        message_bytes = base64.b64decode(request.message)
        
        # Sign the message
        signature = auth_manager.sign_message(message_bytes, key_pair)
        
        # Log the signature
        logger.info(f"Signed message with key ID {key_id} for validator {request.validator_id}")
        
        # Create the response
        return SignatureResponse(
            signature=signature,
            key_id=key_id,
            scheme=key_pair.scheme.value,
            timestamp=time.time()
        )
    except ValueError as e:
        # This could be due to expired key or one-shot key already used
        logger.warning(f"Error signing message: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error signing message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error signing message: {str(e)}"
        )

@app.post("/verify", response_model=VerifySignatureResponse)
async def verify_signature(request: VerifySignatureRequest):
    """Verify a quantum-resistant signature."""
    global auth_manager
    
    if not auth_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication manager not initialized"
        )
    
    # Validate the signature scheme
    if request.scheme not in SIGNATURE_SCHEMES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid signature scheme. Must be one of: {', '.join(SIGNATURE_SCHEMES)}"
        )
    
    try:
        # Convert scheme string to enum
        scheme = SignatureScheme(request.scheme)
        
        # Decode the message (assumed to be base64-encoded)
        import base64
        message_bytes = base64.b64decode(request.message)
        
        # Verify the signature
        is_valid = auth_manager.verify_signature(
            message_bytes,
            request.signature,
            request.public_key,
            scheme
        )
        
        # Log the verification result
        if is_valid:
            logger.info(f"Successfully verified {scheme.value} signature")
        else:
            logger.warning(f"Invalid {scheme.value} signature")
            # Increment alert count for invalid signatures
            app_state["alert_count"] += 1
            
            # Check if we should trigger emergency rotation
            if app_state["alert_count"] >= 5 and time.time() - app_state["last_rotation"] > 24 * 60 * 60:
                # Trigger emergency rotation in the background
                background_tasks = BackgroundTasks()
                background_tasks.add_task(perform_emergency_rotation)
        
        # Create the response
        return VerifySignatureResponse(
            is_valid=is_valid,
            timestamp=time.time()
        )
    except Exception as e:
        logger.error(f"Error verifying signature: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verifying signature: {str(e)}"
        )

@app.post("/tokens/generate", response_model=TokenResponse)
async def generate_token(request: GenerateTokenRequest):
    """Generate a new one-time authentication token."""
    global auth_manager
    
    if not auth_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication manager not initialized"
        )
    
    try:
        # Generate the token
        token = auth_manager.generate_one_time_token(
            purpose=request.purpose,
            expiration_seconds=request.expiration_seconds
        )
        
        # Log token generation
        logger.info(f"Generated one-time token for validator {request.validator_id}: {token.token_id}")
        
        # Create the response
        return TokenResponse(
            token_id=token.token_id,
            token_value=token.token_value,
            expiration_time=token.expiration_time
        )
    except Exception as e:
        logger.error(f"Error generating token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating token: {str(e)}"
        )

@app.post("/tokens/validate")
async def validate_token(request: ValidateTokenRequest):
    """Validate a one-time authentication token."""
    global auth_manager
    
    if not auth_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication manager not initialized"
        )
    
    try:
        # Validate the token
        is_valid = auth_manager.validate_one_time_token(
            request.token_id,
            request.token_value
        )
        
        # Log the validation result
        if is_valid:
            logger.info(f"Successfully validated token {request.token_id} for validator {request.validator_id}")
        else:
            logger.warning(f"Invalid token {request.token_id} for validator {request.validator_id}")
            # Increment alert count for invalid tokens
            app_state["alert_count"] += 1
        
        # Create the response
        return {
            "is_valid": is_valid,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Error validating token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error validating token: {str(e)}"
        )

@app.post("/keys/rotate", response_model=RotationResponse)
async def rotate_keys(request: RotationRequest):
    """Rotate quantum-resistant keys."""
    global auth_manager
    
    if not auth_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication manager not initialized"
        )
    
    try:
        # If a specific validator is specified, rotate only their keys
        if request.validator_id:
            if request.validator_id not in app_state["validator_keys"]:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No keys found for validator {request.validator_id}"
                )
            
            # Get the key IDs for this validator
            key_ids = app_state["validator_keys"][request.validator_id]
            
            # Expire the keys
            rotation_counts = {scheme.value: 0 for scheme in SignatureScheme}
            
            for key_id in key_ids:
                # Find the key pair
                for internal_key_id, key_pair in auth_manager.key_pairs.items():
                    if hashlib.sha256(key_pair.public_key.encode()).hexdigest()[:16] == key_id:
                        # Mark the key as expired
                        key_pair.expiration_time = time.time()
                        
                        # Generate a new key with the same scheme
                        new_key_pair = auth_manager.generate_keypair(key_pair.scheme)
                        
                        # Generate new key ID
                        new_key_id = hashlib.sha256(new_key_pair.public_key.encode()).hexdigest()[:16]
                        
                        # Update the validator's keys
                        app_state["validator_keys"][request.validator_id].append(new_key_id)
                        
                        # Update rotation counts
                        rotation_counts[key_pair.scheme.value] += 1
                        
                        break
        else:
            # Rotate all keys
            rotation_counts = auth_manager.emergency_key_rotation()
            
            # Update the last rotation timestamp
            app_state["last_rotation"] = time.time()
            
            # Reset the alert count
            app_state["alert_count"] = 0
        
        # Log the rotation
        logger.info(f"Rotated keys: {rotation_counts}, reason: {request.reason}")
        
        # Create the response
        return RotationResponse(
            rotated_keys=rotation_counts,
            timestamp=time.time()
        )
    except Exception as e:
        logger.error(f"Error rotating keys: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error rotating keys: {str(e)}"
        )

@app.post("/cleanup")
async def cleanup_tokens():
    """Clean up expired tokens."""
    global auth_manager
    
    if not auth_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication manager not initialized"
        )
    
    try:
        # Clean up expired tokens
        count = auth_manager.cleanup_expired_tokens()
        
        # Log the cleanup
        logger.info(f"Cleaned up {count} expired tokens")
        
        # Create the response
        return {
            "deleted_count": count,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Error cleaning up tokens: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error cleaning up tokens: {str(e)}"
        )

async def perform_emergency_rotation():
    """Perform emergency key rotation in the background."""
    global auth_manager
    
    if not auth_manager:
        logger.error("Cannot perform emergency rotation: Authentication manager not initialized")
        return
    
    try:
        # Rotate all keys
        rotation_counts = auth_manager.emergency_key_rotation()
        
        # Update the last rotation timestamp
        app_state["last_rotation"] = time.time()
        
        # Reset the alert count
        app_state["alert_count"] = 0
        
        # Log the emergency rotation
        logger.warning(f"Performed emergency key rotation: {rotation_counts}")
    except Exception as e:
        logger.error(f"Error during emergency key rotation: {e}")

def main():
    """Main entry point for the quantum authentication server."""
    parser = argparse.ArgumentParser(description="Quantum Authentication Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8083, help="Port to bind to")
    parser.add_argument("--config-file", help="Path to configuration file")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    args = parser.parse_args()
    
    # Update app state from args
    if args.config_file:
        app_state["config_file"] = args.config_file
    
    # Set log level
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper()))
    
    # Start server
    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main() 