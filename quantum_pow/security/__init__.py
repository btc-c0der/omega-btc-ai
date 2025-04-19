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

Security package for Quantum Proof-of-Work (qPoW) implementation.

This package contains security-related modules for the qPoW system,
including CSRF protection, validator privacy, quantum-resistant authentication, 
API security, and other security-enhancing components.

JAH BLESS SATOSHI
"""

from quantum_pow.security.csrf_monitor import (
    CSRFRequest,
    ParsingStrategy,
    SQLRegexParsingStrategy,
    SQLASTParsingStrategy,
    WhitelistManager,
    CSRFMonitor,
    CSRFProtectionMiddleware
)

from quantum_pow.security.validator_privacy import (
    PrivacyThreatLevel,
    ValidatorMetadata,
    DandelionRouting,
    ValidatorPrivacyManager
)

from quantum_pow.security.quantum_resistant_auth import (
    SignatureScheme,
    KeyPair,
    OneTimeToken,
    QuantumResistantAuth
)

__all__ = [
    # CSRF Protection
    'CSRFRequest',
    'ParsingStrategy',
    'SQLRegexParsingStrategy',
    'SQLASTParsingStrategy',
    'WhitelistManager',
    'CSRFMonitor',
    'CSRFProtectionMiddleware',
    
    # Validator Privacy
    'PrivacyThreatLevel',
    'ValidatorMetadata',
    'DandelionRouting',
    'ValidatorPrivacyManager',
    
    # Quantum-Resistant Authentication
    'SignatureScheme',
    'KeyPair',
    'OneTimeToken',
    'QuantumResistantAuth'
]

# Version of the security package
__version__ = '1.1.0' 