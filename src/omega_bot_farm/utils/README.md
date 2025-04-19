
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸


# Utils Module

## Overview

The Utils Module provides common utility functions and helpers used throughout the Omega Bot Farm ecosystem. These utilities abstract shared functionality, simplify complex operations, and provide standardized implementations of common tasks.

## Key Components

### Redis Client (redis_client.py)

A wrapper around the Redis client for simplified Redis operations:

- JSON serialization/deserialization
- Connection management for containerized environments
- Error handling and fallback functionality
- Standardized methods for common Redis operations

### Cosmic Factor Service (cosmic_factor_service.py)

A service for calculating cosmic and astrological factors that may influence markets:

- Planetary position calculations
- Astrological aspect analysis
- Cosmic event detection
- Integration with trading algorithms

## Usage

### Redis Client

```python
from omega_bot_farm.utils.redis_client import RedisClient

# Initialize client
redis = RedisClient(host='redis.service', port=6379)

# Store data
redis.set('market:btc:price', {'price': 50000, 'timestamp': 1617293940})

# Retrieve data
price_data = redis.get('market:btc:price')
```

### Cosmic Factor Service

```python
from omega_bot_farm.utils.cosmic_factor_service import CosmicFactorService

# Initialize service
cosmic = CosmicFactorService()

# Get current cosmic factors
factors = cosmic.get_current_factors()

# Check if Mercury is retrograde
is_retrograde = cosmic.is_mercury_retrograde()

# Get moon phase
moon_phase = cosmic.get_moon_phase()
```

## Integration

The Utils Module is used by:

- Trading bots for data persistence and cosmic factor analysis
- Services for shared functionality
- Discord bots for user data management
- Analytics components for data storage

## Extension

To add new utilities:

1. Create a new Python file in the utils directory
2. Implement well-documented functions with proper type hints
3. Follow the established error handling patterns
4. Add comprehensive unit tests

## Best Practices

- Keep utility functions focused on a single responsibility
- Implement proper error handling and logging
- Provide meaningful default values for parameters
- Document parameters, return values, and exceptions
- Ensure thread safety for shared utilities
