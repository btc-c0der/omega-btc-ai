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

# Quantum Proof-of-Work (qPoW) System

A post-quantum resistant mining and blockchain system built to demonstrate quantum-safe consensus algorithms.

## Overview

The Quantum Proof-of-Work (qPoW) system implements a novel approach to blockchain mining that is resistant to attacks from quantum computers. Key features include:

- **Post-Quantum Cryptographic Primitives**: Using lattice-based cryptographic techniques resistant to quantum attacks
- **OmegaPRM (Probabilistic Residual Mining)**: Advanced mining algorithm that uses Monte Carlo Tree Search (MCTS) for optimization
- **Kubernetes Deployment**: Ready-to-use Kubernetes manifests for deploying a mining cluster
- **CSRF Protection**: Advanced monitoring system to prevent Cross-Site Request Forgery attacks
- **Validator Privacy**: Metadata protection for validator nodes to prevent deanonymization attacks
- **Quantum-Resistant Authentication**: One-shot signatures and other post-quantum cryptographic techniques for secure validator authentication

## Project Structure

```
quantum_pow/
├── hash_functions.py - Quantum-resistant hash implementations
├── block_structure.py - Block and blockchain data structures
├── transactions.py - Transaction handling and verification
├── omega_prm_runner.py - Main mining implementation using MCTS
├── demo.py - Demonstration of core functionality
├── run_tests.py - Test runner script
├── security/ - Security monitoring and protection
│   ├── csrf_monitor.py - CSRF attack monitoring system
│   ├── csrf_server.py - FastAPI server for CSRF protection
│   ├── validator_privacy.py - Validator privacy protection system
│   ├── validator_privacy_server.py - FastAPI server for validator privacy
│   ├── quantum_resistant_auth.py - Quantum-resistant authentication
│   ├── quantum_auth_server.py - FastAPI server for quantum authentication
│   └── README.md - Documentation for security components
└── tests/ - Test suite
    ├── __init__.py
    ├── test_hash.py
    ├── test_block.py
    ├── test_mining.py
    ├── test_transactions.py
    ├── test_csrf_monitor.py - CSRF monitor tests
    ├── test_validator_privacy.py - Validator privacy tests
    └── test_quantum_resistant_auth.py - Quantum authentication tests
```

## OmegaPRM Mining Algorithm

OmegaPRM (Probabilistic Residual Mining) uses Monte Carlo Tree Search (MCTS) to optimize the mining process:

1. **Exploration vs Exploitation**: Uses UCB1 (Upper Confidence Bound) to balance between exploring new nonce patterns and exploiting promising ones
2. **Tree Pruning**: Dynamically prunes unpromising branches to focus computational resources
3. **Quality Scoring**: Evaluates hash quality on a continuous scale rather than binary valid/invalid
4. **Parallel Simulation**: Runs multiple simulations to better estimate branch quality

## Getting Started

### Prerequisites

- Python 3.8+
- Required packages:
  - `cryptography`
  - `numpy`
  - `fastapi` and `uvicorn` (for security services)
  - For Kubernetes deployment: `kubectl` and a running Kubernetes cluster

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/omega-btc-ai.git
cd omega-btc-ai

# Install dependencies
pip install -r requirements.txt
```

### Running the Demo

```bash
# Run the demonstration
python quantum_pow/demo.py

# Run the miner directly
python -m quantum_pow.omega_prm_runner --iterations 100 --time-limit 30
```

### Running Tests

```bash
# Run all tests
python quantum_pow/run_tests.py

# Run specific test modules
python quantum_pow/run_tests.py --pattern "test_mining.py"

# Run CSRF protection tests
python quantum_pow/run_tests.py --pattern "test_csrf_monitor.py"

# Run validator privacy tests
python quantum_pow/run_tests.py --pattern "test_validator_privacy.py"

# Run quantum authentication tests
python quantum_pow/run_tests.py --pattern "test_quantum_resistant_auth.py"
```

## Kubernetes Deployment

The system includes full Kubernetes deployment configurations in the `kubernetes/` directory.

### Deploying to Kubernetes

```bash
# Deploy the mining nodes
kubectl apply -f kubernetes/omega_prm_deployment.yaml

# Deploy the CSRF protection
kubectl apply -f kubernetes/csrf_monitor_deployment.yaml

# Deploy the validator privacy protection
kubectl apply -f kubernetes/validator_privacy_deployment.yaml

# Deploy the quantum authentication
kubectl apply -f kubernetes/quantum_auth_deployment.yaml

# Check the deployment status
kubectl get pods -l app=omega-prm-miner
kubectl get pods -l app=csrf-monitor
kubectl get pods -l app=validator-privacy
kubectl get pods -l app=quantum-auth

# View mining logs
kubectl logs -l app=omega-prm-miner
```

### Scaling the Mining Cluster

The deployment includes a HorizontalPodAutoscaler that will automatically scale the number of mining nodes based on CPU and memory utilization:

```bash
# View the autoscaler status
kubectl get hpa omega-prm-miner
```

You can also manually scale the deployment:

```bash
# Scale to 5 miners
kubectl scale deployment/omega-prm-miner --replicas=5
```

## Technical Details

### Quantum Resistance

The system achieves quantum resistance through:

1. **Lattice-Based Cryptography**: The hash function incorporates lattice-based operations resistant to Grover's algorithm attacks
2. **Increased Hash Complexity**: Additional rounds and mixing functions beyond standard SHA3
3. **Personalization**: Hash outputs are personalized to specific application contexts

### Mining Algorithm Optimization

OmegaPRM optimizes traditional mining:

- **Targeted Search**: MCTS focuses computation on promising nonce ranges
- **Probabilistic Assessment**: Continuous quality scores rather than binary targets
- **Heat Mapping**: Internal tracking of nonce pattern performance
- **Adaptive Difficulty**: Adjustments based on network hash rate and block times

### CSRF Protection

The CSRF monitor protects API endpoints from Cross-Site Request Forgery attacks:

- **Multiple Parsing Strategies**: Uses both RegEx and AST-based parsing for deep analysis
- **Request Whitelisting**: Maintains a whitelist of known safe request patterns
- **Kubernetes Integration**: Deployed alongside mining nodes with automatic scaling
- **REST API**: Exposed endpoints for checking requests and managing whitelist
- **TDD Approach**: Built with comprehensive test coverage

### Validator Privacy Protection

The validator privacy module protects validator identities from being linked to their IP addresses:

- **Dandelion Routing**: Two-phase routing protocol that makes it difficult to trace messages to their origin
- **Metadata Protection**: Randomized timing and message padding to prevent metadata analysis attacks
- **Privacy Risk Analysis**: Advanced analytics to identify and mitigate privacy vulnerabilities
- **Trusted Proxies**: Routing of sensitive block proposals through trusted proxies
- **Peer Rotation**: Regular rotation of peer connections to prevent long-term correlation
- **Kubernetes Deployment**: Fully containerized deployment with automatic peer rotation and analysis

### Quantum-Resistant Authentication

The quantum authentication module provides post-quantum secure authentication for validators:

- **One-Shot Signatures**: Implementation of the "one-shot signatures" technique from "One-shot signatures and applications to hybrid quantum/classical authentication" (R. Amos et al.)
- **Multiple Signature Schemes**: Support for various post-quantum cryptographic schemes including FALCON, DILITHIUM, SPHINCS+, and ZK-ECDSA
- **Emergency Key Rotation**: Automatic key rotation in case of potential quantum attacks
- **One-Time Tokens**: Single-use authentication tokens for enhanced security
- **Regular Key Rotation**: Scheduled key rotation via Kubernetes cron jobs
- **Validator Isolation**: Each validator's keys and authentication is isolated from others
- **Cross-Platform Authentication**: Works with both classical and quantum-enabled clients

### Performance Considerations

- Hash rate typically improves 30-40% compared to brute force approaches
- CPU-optimized with multi-threading support
- Resource-efficient Kubernetes deployment with autoscaling

## Security Considerations

- Post-quantum security assumes proper implementation of the underlying cryptographic primitives
- The system is designed for demonstration purposes and should undergo formal verification before production use
- Default difficulty settings are lowered for testing purposes
- The CSRF monitor protects API endpoints with multiple parsing strategies
- Validator privacy protection is essential as quantum miners could be targets for attacks if identifiable
- Quantum authentication provides an additional layer of security even if the underlying blockchain is compromised
- One-shot signatures ensure forward secrecy even in the event of a quantum attack
- All external requests are validated against potential attack patterns
- Whitelist of approved request patterns is maintained and persisted

## License

This project is licensed under the GBU2™ License (Genesis-Bloom-Unfoldment) 2.0 by the OMEGA Divine Collective.

## Acknowledgments

- Satoshi Nakamoto for the original Bitcoin concept
- The quantum computing and post-quantum cryptography research community
- Apache ModSecurity CSRF project for security monitoring inspiration
- Ethereum research on validator privacy for the Dandelion routing implementation
- R. Amos et al. for the one-shot signatures research
