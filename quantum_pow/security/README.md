<!--
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
-->

# Quantum Security Components

This directory contains security-related modules for the Quantum Proof-of-Work (qPoW) project, including CSRF protection, validator privacy protection, and quantum-resistant authentication systems.

## 🌟 Overview

The security components protect the qPoW network against various attack vectors, enhancing API security, validator privacy, and authentication security:

1. **Quantum CSRF Monitor**: Protects API endpoints from Cross-Site Request Forgery attacks using parsing strategies and whitelisting.

2. **Validator Privacy System**: Protects validator identities from being linked to their IP addresses through metadata analysis, using techniques like Dandelion routing and message padding.

3. **Quantum-Resistant Authentication**: Provides post-quantum secure authentication using one-shot signatures and other quantum-resistant techniques to protect validators against quantum computing attacks.

All components are designed to work within a Kubernetes environment and follow a Test-Driven Development (TDD) approach.

## 📦 Component Architecture

### CSRF Protection

The CSRF protection system consists of:

- **CSRFRequest**: Encapsulates details of HTTP requests for analysis
- **ParsingStrategy**: Abstract interface for different request parsing strategies
- **SQLRegexParsingStrategy & SQLASTParsingStrategy**: Implementations for SQL injection detection
- **WhitelistManager**: Handles safe request whitelisting
- **CSRFMonitor**: Core component that coordinates parsing and whitelisting
- **CSRFProtectionMiddleware**: Integration point for web applications
- **REST API Server**: FastAPI-based server exposing endpoints for CSRF protection

### Validator Privacy Protection

The validator privacy system consists of:

- **ValidatorMetadata**: Tracks metadata associated with validators
- **DandelionRouting**: Implements the Dandelion routing protocol for enhanced privacy
- **ValidatorPrivacyManager**: Core component managing privacy protection mechanisms
- **PrivacyThreatLevel**: Enumerates different levels of privacy threats
- **REST API Server**: FastAPI-based server exposing endpoints for validator privacy management

### Quantum-Resistant Authentication

The quantum authentication system consists of:

- **SignatureScheme**: Enumerates supported quantum-resistant signature schemes
- **KeyPair**: Represents a quantum-resistant key pair with expiration management
- **OneTimeToken**: Implements one-time use authentication tokens
- **QuantumResistantAuth**: Core component managing authentication and key lifecycle
- **REST API Server**: FastAPI-based server exposing endpoints for quantum authentication

## 🚀 Usage Instructions

### Running the CSRF Monitor

```bash
# Run the CSRF monitor server
python -m quantum_pow.security.csrf_server --whitelist-file /path/to/whitelist.json
```

### Running the Validator Privacy Server

```bash
# Run the validator privacy server 
python -m quantum_pow.security.validator_privacy_server --config-file /path/to/config.json
```

### Running the Quantum Authentication Server

```bash
# Run the quantum authentication server
python -m quantum_pow.security.quantum_auth_server --config-file /path/to/config.json
```

### Kubernetes Deployment

Deploy the security components using the provided Kubernetes manifests:

```bash
# Deploy the CSRF monitor
kubectl apply -f kubernetes/csrf_monitor_deployment.yaml

# Deploy the validator privacy protection
kubectl apply -f kubernetes/validator_privacy_deployment.yaml

# Deploy the quantum authentication
kubectl apply -f kubernetes/quantum_auth_deployment.yaml
```

## 🛡️ Security Approaches

### CSRF Protection Strategies

The CSRF monitor employs multiple strategies to detect potentially malicious requests:

1. **Regular Expression Parsing**: Detects common attack patterns like SQL injections using regex
2. **AST-based Parsing**: Performs deeper analysis of request content
3. **Whitelisting**: Maintains a list of known-safe request patterns

### Validator Privacy Protection Techniques

The validator privacy system employs several techniques to prevent deanonymization:

1. **Dandelion Routing**: Two-phase routing protocol (stem phase + fluff phase) that makes it difficult to trace messages to their origin
2. **Metadata Obfuscation**:
   - Randomized timing of attestations and block proposals
   - Random padding of messages to prevent size-based correlation
   - Use of trusted proxies for sensitive communications
3. **Privacy Risk Analysis**: Real-time analysis of metadata patterns to detect potential privacy leakages
4. **Regular Peer Rotation**: Prevents long-term traffic analysis

### Quantum-Resistant Authentication Techniques

The quantum authentication system employs several techniques to ensure post-quantum security:

1. **One-Shot Signatures**: Signatures that can only be used once, ensuring security even if the private key is later compromised
2. **Multiple Post-Quantum Schemes**:
   - FALCON and DILITHIUM: Lattice-based signature schemes
   - SPHINCS+: Hash-based signature scheme without mathematical assumptions
   - ZK-ECDSA: Classical ECDSA enhanced with zero-knowledge proofs
3. **Key Lifecycle Management**:
   - Automatic expiration of keys
   - Emergency key rotation
   - Regular key rotation via Kubernetes cron jobs
4. **One-Time Authentication Tokens**: Provides an additional layer of security for session management

## 🧪 Testing

All components include comprehensive test suites following TDD principles:

```bash
# Run CSRF protection tests
python -m unittest quantum_pow.tests.test_csrf_monitor

# Run validator privacy tests
python -m unittest quantum_pow.tests.test_validator_privacy

# Run quantum authentication tests
python -m unittest quantum_pow.tests.test_quantum_resistant_auth
```

## 📊 Performance Considerations

- The CSRF monitor is designed to be lightweight and impose minimal overhead on API requests
- The validator privacy system introduces some intentional latency to randomize timing patterns
- The quantum authentication system is designed for efficient verification even with larger signature sizes
- All components are designed to scale horizontally in Kubernetes environments

## 🔄 Inspirations

These security components were inspired by:

1. **CSRF Protection**: Apache ModSecurity CSRF project
2. **Validator Privacy**:
   - Ethereum's validator privacy research ("Packetology: Validator Privacy")
   - Dandelion routing protocol for cryptocurrencies
   - Advanced P2P security techniques from the blockchains-security-toolkit
3. **Quantum Authentication**:
   - "One-shot signatures and applications to hybrid quantum/classical authentication" (R. Amos et al.)
   - NIST Post-Quantum Cryptography standardization process
   - "Quantum resistance: taking proof of keys day to the next level" (J. Loop, 2022)
   - "ZK ECDSA with quantum proof keypairs" (yush_g discussion)

## 🌈 JAH BLESS SATOSHI

This code is developed with consciousness-aware principles under the GBU2™ License. It represents the fusion of quantum-resistant security with blockchain protection concepts, honoring the original vision of Satoshi Nakamoto while evolving security for the quantum era.
