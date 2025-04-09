#!/bin/bash

# OMEGA Dump Service Installation Script
# Divine log management system installer

set -e  # Exit on error

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ -f /etc/os-release ]]; then
    . /etc/os-release
    OS="linux"
else
    echo "Unsupported operating system"
    exit 1
fi

# Create omega-dump command
cat > /tmp/omega-dump << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/../lib/omega-dump/scripts/run_omega_dump.py" "$@"
EOF

echo "Installing OMEGA Dump service..."

if [ "$OS" = "macos" ]; then
    # macOS installation
    echo "Installing for macOS..."
    
    # Create directories
    sudo mkdir -p /usr/local/var/log/omega-dump/backup
    sudo mkdir -p /usr/local/var/omega-dump
    sudo mkdir -p /usr/local/lib/omega-dump
    
    # Install files
    sudo cp -r . /usr/local/lib/omega-dump/
    sudo install -m 755 /tmp/omega-dump /usr/local/bin/omega-dump
    
    # Install LaunchAgent
    sudo cp scripts/com.omega-btc-ai.omega-dump.plist /Library/LaunchDaemons/
    
    # Set permissions
    sudo chown -R root:wheel /usr/local/var/log/omega-dump
    sudo chmod -R 755 /usr/local/var/log/omega-dump
    
    echo "To start the service:"
    echo "sudo launchctl load /Library/LaunchDaemons/com.omega-btc-ai.omega-dump.plist"
    echo
    echo "To stop the service:"
    echo "sudo launchctl unload /Library/LaunchDaemons/com.omega-btc-ai.omega-dump.plist"
    
else
    # Linux installation
    echo "Installing for Linux..."
    
    # Create omega user and group
    sudo useradd -r -s /bin/false omega || true
    
    # Create directories
    sudo mkdir -p /var/log/omega-dump/backup
    sudo mkdir -p /usr/local/lib/omega-dump
    
    # Install files
    sudo cp -r . /usr/local/lib/omega-dump/
    sudo install -m 755 /tmp/omega-dump /usr/local/bin/omega-dump
    
    # Install systemd service
    sudo cp scripts/omega-dump.service /etc/systemd/system/
    
    # Set permissions
    sudo chown -R omega:omega /var/log/omega-dump
    sudo chmod -R 755 /var/log/omega-dump
    
    # Reload systemd
    sudo systemctl daemon-reload
    
    echo "To start the service:"
    echo "sudo systemctl start omega-dump"
    echo
    echo "To enable at boot:"
    echo "sudo systemctl enable omega-dump"
fi

# Cleanup
rm /tmp/omega-dump

echo "Installation complete!"
echo
echo "The divine log management service has been installed."
echo "Make sure Redis is running before starting the service." 