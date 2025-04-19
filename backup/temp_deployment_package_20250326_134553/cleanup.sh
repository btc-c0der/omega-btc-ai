#!/bin/bash

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸


echo "🔮 OMEGA BTC AI - SACRED CLEANUP SCRIPT 🔮"
echo "=========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

echo "🧹 Cleaning Docker system..."
docker system prune -af --volumes

echo "🧹 Cleaning package cache..."
apt-get clean
apt-get autoremove -y
:q!
echo "🧹 Cleaning old logs..."
journalctl --vacuum-time=2d

echo "🧹 Cleaning /usr..."
# Remove old kernels
dpkg -l | grep linux-image | awk '/^ii/{ print $2}' | grep -v $(uname -r) | xargs -r apt-get -y purge

# Clean up old documentation
rm -rf /usr/share/doc/*
rm -rf /usr/share/man/*

echo "🧹 Cleaning /var..."
# Clean up old logs
find /var/log -type f -name "*.gz" -delete
find /var/log -type f -name "*.old" -delete

echo "🧹 Cleaning /home..."
# Clean up any temporary files
find /home -type f -name "*.tmp" -delete
find /home -type f -name "*.temp" -delete

echo "🧹 Running fstrim..."
fstrim /

echo "📊 Current disk usage:" 
df -h /

echo "✨ Cleanup complete! JAH BLESS! ✨" 