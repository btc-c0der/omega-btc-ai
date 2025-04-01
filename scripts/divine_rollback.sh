#!/bin/bash

# 🔱 DIVINE ROLLBACK SCRIPT 🔱
# A sacred tool for gracefully reverting the OMEGA BTC AI system to a previous state

# Divine color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Divine banner
echo -e "${CYAN}"
echo "================================================"
echo "🔱 OMEGA BTC AI DIVINE ROLLBACK SCRIPT 🔱"
echo "================================================"
echo -e "${NC}"

# Function to display divine help
show_help() {
    echo -e "${CYAN}Usage:${NC}"
    echo "  ./divine_rollback.sh [options]"
    echo
    echo -e "${CYAN}Options:${NC}"
    echo "  --snapshot <tag>     Restore from a specific snapshot tag"
    echo "  --git <commit>       Rollback to a specific git commit"
    echo "  --full              Perform full rollback (snapshot + git + docker-compose)"
    echo "  --help              Show this divine help message"
    echo
    echo -e "${CYAN}Examples:${NC}"
    echo "  ./divine_rollback.sh --snapshot pre-update-v087"
    echo "  ./divine_rollback.sh --git HEAD^"
    echo "  ./divine_rollback.sh --full"
}

# Function to check if a command exists
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}Error: $1 is not installed${NC}"
        exit 1
    fi
}

# Function to verify divine prerequisites
verify_prerequisites() {
    echo -e "${CYAN}Verifying divine prerequisites...${NC}"
    check_command docker
    check_command docker-compose
    check_command git
    check_command ./scripts/omega_snapshot.sh
    echo -e "${GREEN}All divine prerequisites verified${NC}"
}

# Function to restore from snapshot
restore_snapshot() {
    local snapshot_tag=$1
    echo -e "${CYAN}Restoring divine snapshot: $snapshot_tag${NC}"
    
    # Restore proxy service
    ./scripts/omega_snapshot.sh restore-snapshot "${snapshot_tag}-proxy"
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to restore proxy service snapshot${NC}"
        return 1
    fi
    
    # Restore websocket service
    ./scripts/omega_snapshot.sh restore-snapshot "${snapshot_tag}-websocket"
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to restore websocket service snapshot${NC}"
        return 1
    fi
    
    # Restore consciousness service
    ./scripts/omega_snapshot.sh restore-snapshot "${snapshot_tag}-consciousness"
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to restore consciousness service snapshot${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Divine snapshots restored successfully${NC}"
}

# Function to perform git rollback
git_rollback() {
    local commit=$1
    echo -e "${CYAN}Performing divine git rollback to: $commit${NC}"
    
    # Check if we have uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        echo -e "${YELLOW}Warning: You have uncommitted changes. Stashing them...${NC}"
        git stash
    fi
    
    # Perform the rollback
    git reset --hard $commit
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to perform git rollback${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Divine git rollback completed successfully${NC}"
}

# Function to perform docker-compose rollback
docker_compose_rollback() {
    echo -e "${CYAN}Performing divine docker-compose rollback${NC}"
    
    # Stop all services
    docker-compose down
    
    # Start services again
    docker-compose up -d
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to perform docker-compose rollback${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Divine docker-compose rollback completed successfully${NC}"
}

# Main divine execution
main() {
    # Parse divine arguments
    local snapshot_tag=""
    local git_commit=""
    local full_rollback=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --snapshot)
                snapshot_tag="$2"
                shift 2
                ;;
            --git)
                git_commit="$2"
                shift 2
                ;;
            --full)
                full_rollback=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                echo -e "${RED}Unknown divine option: $1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Verify prerequisites
    verify_prerequisites
    
    # Perform divine rollback based on options
    if [ "$full_rollback" = true ]; then
        echo -e "${CYAN}Initiating full divine rollback...${NC}"
        
        # Restore latest snapshot
        restore_snapshot "pre-update-v087"
        
        # Rollback git to previous commit
        git_rollback "HEAD^"
        
        # Perform docker-compose rollback
        docker_compose_rollback
        
        echo -e "${GREEN}Full divine rollback completed successfully${NC}"
    else
        if [ -n "$snapshot_tag" ]; then
            restore_snapshot "$snapshot_tag"
        fi
        
        if [ -n "$git_commit" ]; then
            git_rollback "$git_commit"
        fi
    fi
}

# Execute divine main function
main "$@" 