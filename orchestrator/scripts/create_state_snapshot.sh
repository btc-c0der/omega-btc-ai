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


# 🔱 OMEGA BTC AI - Divine State Snapshot Script 🔱

# 🌟 Configuration
BACKUP_DIR="/backup"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SNAPSHOT_NAME="divine_state_${TIMESTAMP}"
COMPRESSION_LEVEL=9

# 🎨 Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 🌟 Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 🌟 Create backup directory
mkdir -p "${BACKUP_DIR}/${SNAPSHOT_NAME}"

# 🌟 Backup Docker volumes
log_info "Backing up Docker volumes..."
docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "${BACKUP_DIR}/${SNAPSHOT_NAME}:/backup" \
    alpine sh -c '
        for volume in $(docker volume ls -q); do
            echo "Backing up volume: $volume"
            docker run --rm -v $volume:/data -v /backup:/backup alpine tar czf /backup/${volume}.tar.gz -C /data .
        done
    '

# 🌟 Backup configuration files
log_info "Backing up configuration files..."
tar czf "${BACKUP_DIR}/${SNAPSHOT_NAME}/config.tar.gz" \
    -C /etc/nginx/conf.d . \
    -C /etc/prometheus . \
    -C /etc/alertmanager . \
    -C /etc/grafana . \
    -C /etc/falco . \
    -C /etc/vault . \
    -C /etc/cert-manager .

# 🌟 Backup environment variables
log_info "Backing up environment variables..."
env | sort > "${BACKUP_DIR}/${SNAPSHOT_NAME}/environment.txt"

# 🌟 Backup Docker Compose files
log_info "Backing up Docker Compose files..."
cp docker-compose*.yml "${BACKUP_DIR}/${SNAPSHOT_NAME}/"

# 🌟 Create metadata file
cat > "${BACKUP_DIR}/${SNAPSHOT_NAME}/metadata.json" << EOF
{
    "timestamp": "${TIMESTAMP}",
    "version": "1.0",
    "services": [
        "matrix-news",
        "consciousness",
        "redis",
        "temporal-worker",
        "nginx",
        "prometheus",
        "grafana",
        "alertmanager",
        "node-exporter",
        "cadvisor",
        "waf",
        "security-scanner",
        "vault",
        "cert-manager",
        "falco",
        "zap"
    ],
    "volumes": [
        "redis_data",
        "prometheus_data",
        "grafana_data",
        "jaeger_data",
        "alertmanager_data",
        "vault_data"
    ]
}
EOF

# 🌟 Compress the entire snapshot
log_info "Compressing snapshot..."
tar czf "${BACKUP_DIR}/${SNAPSHOT_NAME}.tar.gz" \
    -C "${BACKUP_DIR}" \
    "${SNAPSHOT_NAME}"

# 🌟 Clean up temporary directory
log_info "Cleaning up..."
rm -rf "${BACKUP_DIR}/${SNAPSHOT_NAME}"

# 🌟 Verify backup
if [ -f "${BACKUP_DIR}/${SNAPSHOT_NAME}.tar.gz" ]; then
    log_info "Snapshot created successfully: ${SNAPSHOT_NAME}.tar.gz"
    log_info "Backup size: $(du -h "${BACKUP_DIR}/${SNAPSHOT_NAME}.tar.gz" | cut -f1)"
else
    log_error "Failed to create snapshot"
    exit 1
fi

# 🌟 Clean up old snapshots (keep last 5)
log_info "Cleaning up old snapshots..."
ls -t "${BACKUP_DIR}"/divine_state_*.tar.gz | tail -n +6 | xargs -r rm

# 🌟 JAH JAH BLESS! 🔱
log_info "Divine state snapshot completed successfully!" 