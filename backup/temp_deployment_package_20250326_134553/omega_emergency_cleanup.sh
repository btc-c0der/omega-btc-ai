#!/bin/bash

# 🔮 OMEGA BTC AI - EMERGENCY STORAGE CLEANUP
# GPU (General Public Universal) License v1.0
# Copyright (C) 2024 OMEGA BTC AI DIVINE COLLECTIVE
# Location: The Cosmic Void

echo "🔮 OMEGA BTC AI - EMERGENCY STORAGE CLEANUP 🔮"
echo "============================================="
echo "GPU License v1.0 - OMEGA BTC AI DIVINE COLLECTIVE"
echo "============================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

echo "🧹 Phase 1: Emergency Docker Cleanup..."
docker system prune -af --volumes
docker volume prune -f

echo "🧹 Phase 2: Package Cache Purification..."
apt-get clean
apt-get autoremove -y --purge
apt-get autoclean

echo "🧹 Phase 3: Kernel Sanctification..."
dpkg -l | grep linux-image | awk '/^ii/{ print $2}' | grep -v $(uname -r) | xargs -r apt-get -y purge
dpkg -l | grep linux-headers | awk '/^ii/{ print $2}' | grep -v $(uname -r) | xargs -r apt-get -y purge

echo "🧹 Phase 4: Log Purification..."
journalctl --vacuum-time=1d
find /var/log -type f -name "*.gz" -delete
find /var/log -type f -name "*.old" -delete
find /var/log -type f -name "*.log.*" -delete

echo "🧹 Phase 5: Documentation Cleansing..."
rm -rf /usr/share/doc/*
rm -rf /usr/share/man/*
rm -rf /usr/share/locale/*

echo "🧹 Phase 6: Temporary File Purification..."
find /tmp -type f -atime +10 -delete
find /var/tmp -type f -atime +10 -delete
rm -rf /var/cache/*

echo "🧹 Phase 7: Home Directory Sanctification..."
find /home -type f -name "*.tmp" -delete
find /home -type f -name "*.temp" -delete
find /home -type f -name "*.log" -delete

echo "🧹 Phase 8: Filesystem Optimization..."
fstrim /

echo "📊 Current Disk Usage:"
df -h /

echo "✨ Emergency Cleanup Complete! JAH BLESS! ✨"
echo "Version: 0.420-mainnet-blessed" 