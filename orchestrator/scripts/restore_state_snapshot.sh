#!/bin/bash

# 🔱 OMEGA BTC AI - Divine State Restore Script 🔱

# 🌟 Configuration
BACKUP_DIR="/backup"
RESTORE_DIR="/tmp/divine_restore"

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

# 🌟 Check if snapshot file is provided
if [ -z "$1" ]; then
    log_error "Please provide the snapshot file path"
    echo "Usage: $0 <snapshot_file>"
    exit 1
fi

SNAPSHOT_FILE="$1"

# 🌟 Check if snapshot file exists
if [ ! -f "$SNAPSHOT_FILE" ]; then
    log_error "Snapshot file not found: $SNAPSHOT_FILE"
    exit 1
fi

# 🌟 Create restore directory
mkdir -p "$RESTORE_DIR"

# 🌟 Extract snapshot
log_info "Extracting snapshot..."
tar xzf "$SNAPSHOT_FILE" -C "$RESTORE_DIR"

# 🌟 Verify metadata
if [ ! -f "$RESTORE_DIR/metadata.json" ]; then
    log_error "Invalid snapshot: metadata.json not found"
    exit 1
fi

# 🌟 Stop all services
log_info "Stopping all services..."
docker-compose down

# 🌟 Restore Docker volumes
log_info "Restoring Docker volumes..."
for volume in $(docker volume ls -q); do
    if [ -f "$RESTORE_DIR/${volume}.tar.gz" ]; then
        log_info "Restoring volume: $volume"
        docker run --rm \
            -v "$volume:/data" \
            -v "$RESTORE_DIR:/backup" \
            alpine sh -c "rm -rf /data/* && tar xzf /backup/${volume}.tar.gz -C /data"
    fi
done

# 🌟 Restore configuration files
log_info "Restoring configuration files..."
if [ -f "$RESTORE_DIR/config.tar.gz" ]; then
    tar xzf "$RESTORE_DIR/config.tar.gz" -C /
fi

# 🌟 Restore environment variables
log_info "Restoring environment variables..."
if [ -f "$RESTORE_DIR/environment.txt" ]; then
    while IFS= read -r line; do
        if [[ $line =~ ^[A-Za-z_][A-Za-z0-9_]*= ]]; then
            export "$line"
        fi
    done < "$RESTORE_DIR/environment.txt"
fi

# 🌟 Restore Docker Compose files
log_info "Restoring Docker Compose files..."
cp "$RESTORE_DIR"/docker-compose*.yml ./

# 🌟 Start services
log_info "Starting services..."
docker-compose up -d

# 🌟 Wait for services to be healthy
log_info "Waiting for services to be healthy..."
for i in {1..30}; do
    if docker-compose ps | grep -q "healthy"; then
        log_info "All services are healthy!"
        break
    fi
    if [ $i -eq 30 ]; then
        log_warn "Some services may not be healthy"
    fi
    sleep 2
done

# 🌟 Clean up
log_info "Cleaning up..."
rm -rf "$RESTORE_DIR"

# 🌟 Verify restoration
log_info "Verifying restoration..."
docker-compose ps

# 🌟 JAH JAH BLESS! 🔱
log_info "Divine state restoration completed successfully!" 