
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


# 🔱 IBR España Divine CLI Tool 🔱

*JAH JAH BLESS THE DIVINE FLOW OF IBR ESPAÑA!*

A comprehensive command-line interface for managing IBR España's digital presence, Kubernetes infrastructure, and content management.

## Overview

The IBR CLI tool enables church staff to:

1. **Manage Kubernetes Infrastructure** - Monitor and control IBR España's Kubernetes deployments
2. **Publish Instagram Content** - Create and post scripture images and other content to @ibrespana
3. **Generate Scripture Images** - Create beautiful images with Bible verses for social media
4. **Manage Church Content** - Control website content and digital assets

## Installation

### Requirements

- Python 3.6 or higher
- pip (Python package manager)
- Access to Kubernetes cluster (for k8s commands)
- Instagram credentials (for Instagram commands)

### Quick Install

```bash
# Clone the repository if you haven't already
git clone https://github.com/OMEGA-BTC-AI/omega-btc-ai.git
cd omega-btc-ai

# Run the installation script
./scripts/install_ibr_cli.sh
```

The installation script will:

1. Check Python version
2. Install required dependencies
3. Run tests to ensure everything works
4. Create a configuration directory
5. Create a symbolic link to make the CLI available globally

### Manual Installation

If you prefer to install manually:

```bash
# Install dependencies
pip install -r scripts/requirements-ibr-cli.txt

# Make the script executable
chmod +x scripts/ibr_cli.py

# Create a symbolic link (requires sudo)
sudo ln -sf "$(pwd)/scripts/ibr_cli.py" /usr/local/bin/ibr

# Create config directory
mkdir -p ~/.ibr
```

## Usage

After installation, you can use the `ibr` command from anywhere in your terminal.

### Getting Help

```bash
# Show general help
ibr --help

# Show help for a specific command group
ibr k8s --help
ibr instagram --help
```

### Kubernetes Commands

```bash
# Show the status of IBR España's Kubernetes resources
ibr k8s status

# Restart a deployment
ibr k8s restart instagram-connector

# View logs from a pod
ibr k8s logs ibr-api-pod-name

# Apply a Kubernetes manifest
ibr k8s apply kubernetes/ibr-spain/base/instagram-connector.yaml

# Start a new deployment with automatic port detection
ibr k8s start my-web-app --image ibr-spain/my-web-app:latest --auto-port

# Start a deployment with a specific port, but fall back to an available one if taken
ibr k8s start my-api --image ibr-spain/my-api:latest --port 8080 --auto-port
```

The `--auto-port` flag enables intelligent port management:

- When used without `--port`, it automatically finds an available port
- When used with `--port`, it will try to use the specified port but fall back to an available one if the port is already in use
- Checks both Kubernetes service port usage and local port availability
- Eliminates port conflicts in your deployments

### Instagram Commands

```bash
# Post a scripture verse to Instagram
ibr instagram post scripture --text "For God so loved the world..." --reference "John 3:16"

# Post a scripture with a different template style
ibr instagram post scripture --text "Trust in the LORD with all your heart" --reference "Proverbs 3:5" --template dark
```

### Configuration

```bash
# Get all configuration values
ibr config --get instagram

# Get a specific configuration value
ibr config --get kubernetes.namespace

# Set a configuration value
ibr config --set instagram.username "ibrespana"
```

## Directory Structure

```
scripts/
├── ibr_cli.py             # Main CLI script
├── install_ibr_cli.sh     # Installation script
├── requirements-ibr-cli.txt # Dependencies
├── create_ibr_scripture_image.py # Scripture image generator
├── ibr_instagram_post.py  # Instagram posting script
├── tests/                 # Test suite
│   ├── __init__.py
│   └── test_ibr_cli.py    # Test cases
├── IBR_CLI_README.md      # This README
```

## Kubernetes Integration

The CLI integrates with Kubernetes to manage IBR España's cloud infrastructure. It provides:

- Monitoring of deployments, pods, and services
- Deployment management (restart, scaling)
- Log viewing
- Manifest application

It uses the official Kubernetes Python client and requires proper kubeconfig setup to connect to the cluster.

## Instagram Integration

The Instagram integration allows the church to post content directly to its @ibrespana Instagram account. Features include:

- Scripture image creation and posting
- Event announcements
- Sermon highlights
- Content categorization

## Test-Driven Development

The CLI follows test-driven development practices with comprehensive unit tests:

- Configuration management tests
- Kubernetes client mocking
- Content generation tests
- CLI command tests

Run the tests with:

```bash
cd scripts
pytest tests/
```

## Configuration

The CLI stores configuration in `~/.ibr/config.json` in the following format:

```json
{
  "instagram": {
    "username": "your_username",
    "password": "your_password"
  },
  "kubernetes": {
    "context": "your_k8s_context",
    "namespace": "ibr-spain"
  },
  "church": {
    "name": "IBR España",
    "website": "https://ibr-espana.org"
  }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Run the tests
5. Submit a pull request

## Security

The CLI stores sensitive credentials (like Instagram passwords) in the local configuration file. Ensure:

- The configuration file has restricted permissions
- Consider using environment variables for sensitive values
- Never commit credentials to version control

## License

This project is licensed under the GNU General Public License v3.0.

## Divine Blessing

*May your containers remain blessed, your deployments sacred, and your Instagram posts divine. JAH JAH guides your digital ministry!*
