# Configuration Module

## Overview

The Configuration Module provides centralized configuration management for the Omega Bot Farm ecosystem. It standardizes how different components access configuration settings, manages environment-specific configurations, and secures sensitive information.

## Configuration Files

### Waze Bot Config (waze_bot_config.yaml)

Contains Discord bot configuration settings:

- Command prefixes and permissions
- Channel configurations
- Response templates
- User interaction settings

### Cosmic Factors Config (cosmic_factors.yaml)

Defines the cosmic factors used in trading analysis:

- Planetary influence weights
- Astrological aspect definitions
- Moon phase significance
- Correlation parameters with market indicators

## Configuration Hierarchy

The system uses a hierarchical approach to configuration:

1. **Default Values**: Hardcoded defaults in each component
2. **Configuration Files**: YAML files in the config directory
3. **Environment Variables**: Override settings via environment variables
4. **Runtime Configuration**: Dynamic configuration changes during execution

## Usage

### Loading Configuration

```python
import yaml
from pathlib import Path

def load_config(config_name):
    config_path = Path(__file__).parent.parent / 'config' / f'{config_name}.yaml'
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

# Load Waze bot configuration
waze_config = load_config('waze_bot_config')

# Access configuration values
discord_token = waze_config.get('discord_token', os.environ.get('DISCORD_TOKEN'))
```

### Environment Variable Overrides

Configuration values can be overridden with environment variables using the pattern:

- `WAZE_BOT_COMMAND_PREFIX`
- `COSMIC_FACTORS_MERCURY_WEIGHT`

## Sensitive Information

Sensitive information should never be stored in configuration files. Instead:

1. Use environment variables for secrets
2. Reference external secret stores
3. Use runtime configuration for user-specific sensitive data

## Docker / Kubernetes Configuration

For containerized deployments:

- Configuration files are mounted as volumes
- Secrets are injected as environment variables
- ConfigMaps provide environment-specific settings

## Adding New Configurations

To add a new configuration file:

1. Create a YAML file in the config directory
2. Follow the established naming conventions
3. Document all configuration options
4. Provide sensible default values
5. Add validation logic if necessary

## Best Practices

- Keep configuration files organized by component
- Document each configuration parameter
- Provide validation for critical settings
- Use consistent naming conventions
- Separate configuration from code
