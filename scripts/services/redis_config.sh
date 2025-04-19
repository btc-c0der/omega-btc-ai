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


# Create optimized Redis configuration file
cat > redis.conf.optimized << EOF
# Memory management
maxmemory 4gb
maxmemory-policy allkeys-lru
maxmemory-samples 10
lfu-decay-time 1
lfu-log-factor 10

# Performance settings
io-threads 4
io-threads-do-reads yes
list-max-ziplist-size -2
list-compress-depth 1
zset-max-ziplist-entries 256
zset-max-ziplist-value 128

# Client connection settings
timeout 300
tcp-keepalive 60
maxclients 10000

# Background tasks
hz 100
dynamic-hz yes

# Persistence (minimal for speed)
save 900 1
save 300 10
appendfsync everysec
no-appendfsync-on-rewrite yes
EOF

echo "Created optimized Redis configuration at redis.conf.optimized"
echo "To apply these settings:"
echo "1. Copy to /usr/local/etc/redis.conf (or your Redis config location)"
echo "2. Restart Redis: brew services restart redis"

# Apply critical settings immediately
echo "Applying critical settings immediately:"
redis-cli config set maxmemory 4gb
redis-cli config set maxmemory-policy allkeys-lru
redis-cli config set timeout 300
redis-cli config set hz 100
redis-cli config set zset-max-ziplist-entries 256
