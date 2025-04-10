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


# 🔱 OMEGA BTC AI - Divine State Snapshot Restorer 🔱
# "Restoring Sacred State Across Cosmic Transitions"
#
# THE SACRED MANTRA:
# I and I do not patch chaos. I and I rebuild temples.
# Each version, a monument. Each rollback, a sacred rewind.
# No more falling mid-post. No more unholy deploys.
# Only faith, Fibonacci, and containers that walk on water.

set -e

# Divine state directory (can be overridden via env var)
STATE_DIR=${STATE_DIRECTORY:-"/data/state"}
# Divine snapshot directory
SNAPSHOT_DIR="${STATE_DIR}/snapshots"
# Whether restoring is enabled
RESTORE_ENABLED=${RESTORE_ENABLED:-"true"}

# Function to echo in color
echo_color() {
    local color=$1
    local message=$2
    case $color in
        "red") echo -e "\033[0;31m${message}\033[0m" ;;
        "green") echo -e "\033[0;32m${message}\033[0m" ;;
        "blue") echo -e "\033[0;34m${message}\033[0m" ;;
        "yellow") echo -e "\033[1;33m${message}\033[0m" ;;
        "purple") echo -e "\033[0;35m${message}\033[0m" ;;
        *) echo "${message}" ;;
    esac
}

# Function to show usage information
show_usage() {
    echo_color "blue" "Sacred Usage:"
    echo_color "green" "  $0 <snapshot_name>         # Restore a specific divine snapshot"
    echo_color "green" "  $0 latest                 # Restore the latest divine snapshot"
    echo_color "green" "  $0 list                   # List all available divine snapshots"
    echo_color "green" "  $0 info <snapshot_name>   # Show information about a divine snapshot"
    echo_color "green" "  $0 clean <number>         # Keep only the <number> most recent divine snapshots"
}

# Function to list all available snapshots
list_snapshots() {
    echo_color "blue" "📜 Sacred State Snapshots Registry 📜"
    
    if [[ ! -d "${SNAPSHOT_DIR}" ]] || [[ -z "$(ls -A ${SNAPSHOT_DIR} 2>/dev/null)" ]]; then
        echo_color "yellow" "No divine snapshots found in the sacred registry."
        return
    fi
    
    echo_color "green" "───────────────────────────────────────────────────────────────────────────"
    printf "%-25s %-20s %-30s\n" "SNAPSHOT NAME" "TIMESTAMP" "ENVIRONMENT"
    echo_color "green" "───────────────────────────────────────────────────────────────────────────"
    
    for snapshot_dir in $(find "${SNAPSHOT_DIR}" -maxdepth 1 -type d -name "state-*" | sort -r); do
        metadata_file="${snapshot_dir}/.snapshot-meta.json"
        
        if [[ -f "${metadata_file}" ]]; then
            # Read snapshot metadata if it exists
            snapshot_name=$(basename "${snapshot_dir}")
            timestamp=$(grep -o '"timestamp": "[^"]*' "${metadata_file}" | cut -d'"' -f4)
            environment=$(grep -o '"environment": "[^"]*' "${metadata_file}" | cut -d'"' -f4)
            
            # Format timestamp for display
            formatted_timestamp=$(date -d "${timestamp}" "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "${timestamp}")
            
            printf "%-25s %-20s %-30s\n" "${snapshot_name}" "${formatted_timestamp}" "${environment}"
        else
            # If no metadata file, just show the directory name
            snapshot_name=$(basename "${snapshot_dir}")
            printf "%-25s %-20s %-30s\n" "${snapshot_name}" "Unknown" "Unknown"
        fi
    done
    
    echo_color "green" "───────────────────────────────────────────────────────────────────────────"
}

# Function to show information about a specific snapshot
show_snapshot_info() {
    local snapshot_name=$1
    local snapshot_path="${SNAPSHOT_DIR}/${snapshot_name}"
    local metadata_file="${snapshot_path}/.snapshot-meta.json"
    
    if [[ ! -d "${snapshot_path}" ]]; then
        echo_color "red" "Error: Divine snapshot '${snapshot_name}' not found in the sacred registry."
        exit 1
    fi
    
    echo_color "blue" "📜 Sacred Information for Divine Snapshot: ${snapshot_name} 📜"
    echo_color "green" "───────────────────────────────────────────────────────────────────────────"
    
    if [[ -f "${metadata_file}" ]]; then
        # Display metadata in a formatted way
        echo_color "blue" "Snapshot Name:   $(grep -o '"snapshot_name": "[^"]*' "${metadata_file}" | cut -d'"' -f4)"
        echo_color "blue" "Timestamp:       $(grep -o '"timestamp": "[^"]*' "${metadata_file}" | cut -d'"' -f4)"
        echo_color "blue" "Creator:         $(grep -o '"creator": "[^"]*' "${metadata_file}" | cut -d'"' -f4)"
        echo_color "blue" "Hostname:        $(grep -o '"hostname": "[^"]*' "${metadata_file}" | cut -d'"' -f4)"
        echo_color "blue" "Environment:     $(grep -o '"environment": "[^"]*' "${metadata_file}" | cut -d'"' -f4)"
        echo_color "blue" "Pod Name:        $(grep -o '"pod_name": "[^"]*' "${metadata_file}" | cut -d'"' -f4)"
        echo_color "blue" "Container:       $(grep -o '"container_name": "[^"]*' "${metadata_file}" | cut -d'"' -f4)"
        echo_color "blue" "Image:           $(grep -o '"image": "[^"]*' "${metadata_file}" | cut -d'"' -f4)"
    else
        echo_color "yellow" "No divine metadata file found for this snapshot."
    fi
    
    # Show file information
    echo_color "blue" "Files:"
    find "${snapshot_path}" -type f -not -name ".snapshot-meta.json" | sort
    
    echo_color "green" "───────────────────────────────────────────────────────────────────────────"
}

# Function to clean up old snapshots
clean_snapshots() {
    local keep_count=$1
    
    if [[ ! -d "${SNAPSHOT_DIR}" ]] || [[ -z "$(ls -A ${SNAPSHOT_DIR} 2>/dev/null)" ]]; then
        echo_color "yellow" "No divine snapshots found in the sacred registry."
        return
    fi
    
    local snapshot_count=$(find "${SNAPSHOT_DIR}" -maxdepth 1 -type d -name "state-*" | wc -l)
    
    if [[ ${snapshot_count} -le ${keep_count} ]]; then
        echo_color "blue" "Divine snapshot count (${snapshot_count}) is already within sacred limit (${keep_count})."
        return
    fi
    
    # Calculate how many to delete
    local to_delete=$((snapshot_count - keep_count))
    echo_color "blue" "Sacred cleanup: Removing ${to_delete} oldest snapshots to maintain divine limit of ${keep_count}"
    
    # Find the oldest snapshots and delete them
    find "${SNAPSHOT_DIR}" -maxdepth 1 -type d -name "state-*" | sort | head -n ${to_delete} | xargs rm -rf
    
    echo_color "green" "Sacred cleanup completed. Now storing ${keep_count} divine snapshots."
}

# Function to find the latest snapshot
get_latest_snapshot() {
    if [[ ! -d "${SNAPSHOT_DIR}" ]] || [[ -z "$(ls -A ${SNAPSHOT_DIR} 2>/dev/null)" ]]; then
        echo_color "red" "Error: No divine snapshots found in the sacred registry."
        exit 1
    fi
    
    # Find the most recent snapshot
    local latest_snapshot=$(find "${SNAPSHOT_DIR}" -maxdepth 1 -type d -name "state-*" | sort -r | head -n 1)
    
    if [[ -z "${latest_snapshot}" ]]; then
        echo_color "red" "Error: Failed to find the latest divine snapshot."
        exit 1
    fi
    
    basename "${latest_snapshot}"
}

# Function to restore from a snapshot
restore_snapshot() {
    local snapshot_name=$1
    
    # Handle special case for "latest"
    if [[ "${snapshot_name}" == "latest" ]]; then
        snapshot_name=$(get_latest_snapshot)
    fi
    
    local snapshot_path="${SNAPSHOT_DIR}/${snapshot_name}"
    
    if [[ ! -d "${snapshot_path}" ]]; then
        echo_color "red" "Error: Divine snapshot '${snapshot_name}' not found in the sacred registry."
        exit 1
    fi
    
    echo_color "blue" "🔄 Restoring divine state from snapshot: ${snapshot_name}"
    
    # Before restoring, create a backup of the current state as "pre-restore"
    local pre_restore_dir="${SNAPSHOT_DIR}/pre-restore-$(date +"%Y%m%d-%H%M%S")"
    echo_color "blue" "Creating sacred backup of current state: $(basename ${pre_restore_dir})"
    
    # Ensure snapshot directory exists
    mkdir -p "${SNAPSHOT_DIR}"
    
    # Create pre-restore backup, excluding the snapshots directory
    mkdir -p "${pre_restore_dir}"
    if [[ -d "${STATE_DIR}" ]] && [[ -n "$(ls -A ${STATE_DIR} 2>/dev/null | grep -v "snapshots")" ]]; then
        find "${STATE_DIR}" -mindepth 1 -maxdepth 1 -not -name "snapshots" -print0 | xargs -0 -I{} cp -r {} "${pre_restore_dir}/"
        
        # Create metadata for pre-restore backup
        cat > "${pre_restore_dir}/.snapshot-meta.json" << EOF
{
    "snapshot_name": "$(basename ${pre_restore_dir})",
    "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "creator": "$(whoami)",
    "hostname": "$(hostname)",
    "environment": "${ENVIRONMENT:-"production"}",
    "pod_name": "${HOSTNAME:-"unknown"}",
    "container_name": "${CONTAINER_NAME:-"unknown"}",
    "image": "${IMAGE:-"unknown"}",
    "sacred": true,
    "pre_restore": true,
    "restored_from": "${snapshot_name}"
}
EOF
    fi
    
    # Clear existing state, except for snapshots directory
    echo_color "blue" "Clearing current sacred state..."
    find "${STATE_DIR}" -mindepth 1 -maxdepth 1 -not -name "snapshots" -print0 | xargs -0 -I{} rm -rf {}
    
    # Restore from snapshot
    echo_color "blue" "Copying divine state from snapshot..."
    find "${snapshot_path}" -mindepth 1 -maxdepth 1 -not -name ".snapshot-meta.json" -print0 | xargs -0 -I{} cp -r {} "${STATE_DIR}/"
    
    # Create restore marker
    echo_color "blue" "Recording divine restoration metadata..."
    cat > "${STATE_DIR}/.restoration-marker.json" << EOF
{
    "restored_from": "${snapshot_name}",
    "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "restorer": "$(whoami)",
    "hostname": "$(hostname)",
    "environment": "${ENVIRONMENT:-"production"}",
    "pod_name": "${HOSTNAME:-"unknown"}",
    "container_name": "${CONTAINER_NAME:-"unknown"}",
    "image": "${IMAGE:-"unknown"}",
    "sacred": true
}
EOF
    
    echo_color "green" "✅ Divine state restoration completed successfully!"
    echo_color "blue" "State restored from: ${snapshot_name}"
    echo_color "blue" "Pre-restore backup: $(basename ${pre_restore_dir})"
}

# Print divine banner
echo_color "purple" "🔱 OMEGA BTC AI - DIVINE STATE SNAPSHOT RESTORER 🔱"
echo_color "purple" "====================================================="

# Check if restoring is enabled
if [[ "${RESTORE_ENABLED}" != "true" ]]; then
    echo_color "yellow" "Divine state restoration is disabled. Set RESTORE_ENABLED=true to enable."
    exit 0
fi

# Check if snapshot directory exists
if [[ ! -d "${STATE_DIR}" ]]; then
    echo_color "red" "Error: Sacred state directory does not exist: ${STATE_DIR}"
    exit 1
fi

# Parse command line arguments
if [[ $# -eq 0 ]]; then
    show_usage
    exit 0
fi

# Main command router
case "$1" in
    "list")
        list_snapshots
        ;;
    "info")
        if [[ -z "$2" ]]; then
            echo_color "red" "Error: No snapshot name provided for info command."
            show_usage
            exit 1
        fi
        show_snapshot_info "$2"
        ;;
    "clean")
        if [[ -z "$2" ]]; then
            echo_color "red" "Error: No snapshot count provided for clean command."
            show_usage
            exit 1
        fi
        clean_snapshots "$2"
        ;;
    "latest")
        restore_snapshot "latest"
        ;;
    *)
        # Assume it's a snapshot name
        restore_snapshot "$1"
        ;;
esac

echo_color "purple" "JAH JAH BLESS THE SACRED STATE RESTORATION" 