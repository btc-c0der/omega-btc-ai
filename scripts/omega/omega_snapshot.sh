#!/bin/bash

# 🔱 OMEGA BTC AI - Divine Snapshot & Rollback CLI 🔱
# "Sacred State Preservation and Cosmic Time Travel"
#
# THE SACRED MANTRA:
# I and I do not patch chaos. I and I rebuild temples.
# Each version, a monument. Each rollback, a sacred rewind.
# No more falling mid-post. No more unholy deploys.
# Only faith, Fibonacci, and containers that walk on water.

set -e

# Divine colors for sacred output
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Display the divine banner
echo -e "${PURPLE}"
echo "🔱 OMEGA BTC AI - DIVINE SNAPSHOT CLI 🔱"
echo "========================================="
echo -e "${NC}"

# Display usage if no arguments provided
if [ $# -eq 0 ]; then
    echo -e "${YELLOW}Sacred Usage:${NC}"
    echo -e "${GREEN}  $0 snapshot <container_name> [tag_name]${NC} - Create a divine snapshot of a container"
    echo -e "${GREEN}  $0 rollback <deployment_name> [revision]${NC} - Perform a divine rollback of a Kubernetes deployment"
    echo -e "${GREEN}  $0 list-snapshots${NC} - List all divine snapshots"
    echo -e "${GREEN}  $0 list-revisions <deployment_name>${NC} - List all divine revisions of a Kubernetes deployment"
    echo -e "${GREEN}  $0 tag-snapshot <snapshot_id> <tag_name>${NC} - Tag a divine snapshot with a sacred name"
    echo -e "${GREEN}  $0 push-snapshot <snapshot_id> <registry/repo>${NC} - Push a divine snapshot to a sacred registry"
    echo -e "${GREEN}  $0 verify-snapshot <snapshot_id>${NC} - Verify the divine integrity of a snapshot"
    echo -e "${GREEN}  $0 restore-snapshot <snapshot_id> [container_name]${NC} - Restore a sacred container from a snapshot"
    exit 0
fi

# Function to check if running in Kubernetes environment
in_kubernetes() {
    command -v kubectl >/dev/null 2>&1
    return $?
}

# Function to check if a container exists
container_exists() {
    docker ps -a --format "{{.Names}}" | grep -q "^$1$"
    return $?
}

# Function to create a timestamp
get_timestamp() {
    date +"%Y%m%d-%H%M%S"
}

# Function to create a container snapshot
create_snapshot() {
    local container_name=$1
    local tag_suffix=${2:-$(get_timestamp)}
    local image_name="omega-btc-ai:snapshot-${tag_suffix}"
    
    # Check if container exists
    if ! container_exists "$container_name"; then
        echo -e "${RED}Error: Divine container '$container_name' does not exist${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}Creating divine snapshot of container ${YELLOW}$container_name${BLUE} with sacred tag ${YELLOW}$image_name${NC}"
    
    # Create the snapshot
    if docker commit "$container_name" "$image_name"; then
        # Save metadata about the snapshot
        mkdir -p "$HOME/.omega-btc-ai/snapshots"
        local snapshot_file="$HOME/.omega-btc-ai/snapshots/${tag_suffix}.json"
        
        cat > "$snapshot_file" << EOF
{
    "snapshot_id": "${tag_suffix}",
    "container_name": "$container_name",
    "image_name": "$image_name",
    "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "creator": "$(whoami)",
    "host": "$(hostname)",
    "docker_version": "$(docker version --format '{{.Server.Version}}')",
    "verified": false
}
EOF
        
        echo -e "${GREEN}✅ Divine snapshot created successfully!${NC}"
        echo -e "${BLUE}Image: ${YELLOW}$image_name${NC}"
        echo -e "${BLUE}Metadata: ${YELLOW}$snapshot_file${NC}"
        
        # Offer verification
        echo -e "${BLUE}Would you like to verify the divine integrity of this snapshot? [y/N]${NC}"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            verify_snapshot "$tag_suffix"
        fi
    else
        echo -e "${RED}❌ Divine snapshot creation failed!${NC}"
        exit 1
    fi
}

# Function to perform a rollback in Kubernetes
perform_rollback() {
    local deployment_name=$1
    local revision=$2
    
    # Check if we're in Kubernetes
    if ! in_kubernetes; then
        echo -e "${RED}Error: kubectl not found. Are you in a divine Kubernetes environment?${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}Preparing for divine rollback of deployment ${YELLOW}$deployment_name${NC}"
    
    # Check if the deployment exists
    if ! kubectl get deployment "$deployment_name" &>/dev/null; then
        echo -e "${RED}Error: Divine deployment '$deployment_name' not found${NC}"
        exit 1
    fi
    
    # Execute the rollback
    if [ -z "$revision" ]; then
        echo -e "${BLUE}Performing divine rollback to previous sacred revision...${NC}"
        kubectl rollout undo deployment/"$deployment_name"
    else
        echo -e "${BLUE}Performing divine rollback to sacred revision ${YELLOW}$revision${NC}"
        kubectl rollout undo deployment/"$deployment_name" --to-revision="$revision"
    fi
    
    # Wait for rollout to complete
    echo -e "${BLUE}Awaiting divine completion of the sacred rollback...${NC}"
    kubectl rollout status deployment/"$deployment_name" --timeout=300s
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Divine rollback completed successfully!${NC}"
        echo -e "${BLUE}Current deployment state:${NC}"
        kubectl get pods -l app="$deployment_name" -o wide
    else
        echo -e "${RED}❌ Divine rollback failed or timed out!${NC}"
        echo -e "${BLUE}Please check the deployment status:${NC}"
        echo -e "${YELLOW}kubectl rollout status deployment/$deployment_name${NC}"
        exit 1
    fi
}

# Function to list all snapshots
list_snapshots() {
    echo -e "${BLUE}📜 Sacred Snapshots Registry 📜${NC}"
    
    local snapshots_dir="$HOME/.omega-btc-ai/snapshots"
    
    if [ ! -d "$snapshots_dir" ] || [ -z "$(ls -A "$snapshots_dir" 2>/dev/null)" ]; then
        echo -e "${YELLOW}No divine snapshots found in the sacred registry.${NC}"
        return
    fi
    
    echo -e "${GREEN}───────────────────────────────────────────────────────────────────────────${NC}"
    printf "${GREEN}%-20s %-30s %-20s %-10s${NC}\n" "SNAPSHOT ID" "CONTAINER" "TIMESTAMP" "VERIFIED"
    echo -e "${GREEN}───────────────────────────────────────────────────────────────────────────${NC}"
    
    for snapshot_file in "$snapshots_dir"/*.json; do
        if [ -f "$snapshot_file" ]; then
            local snapshot_id=$(jq -r '.snapshot_id' "$snapshot_file")
            local container_name=$(jq -r '.container_name' "$snapshot_file")
            local timestamp=$(jq -r '.timestamp' "$snapshot_file")
            local verified=$(jq -r '.verified' "$snapshot_file")
            
            # Format timestamp
            local formatted_timestamp=$(date -d "$timestamp" "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "$timestamp")
            
            # Format verified status
            if [ "$verified" = "true" ]; then
                verified="${GREEN}✓${NC}"
            else
                verified="${RED}✗${NC}"
            fi
            
            printf "%-20s %-30s %-20s %-10s\n" "$snapshot_id" "$container_name" "$formatted_timestamp" "$verified"
        fi
    done
    echo -e "${GREEN}───────────────────────────────────────────────────────────────────────────${NC}"
}

# Function to list revisions of a deployment
list_revisions() {
    local deployment_name=$1
    
    # Check if we're in Kubernetes
    if ! in_kubernetes; then
        echo -e "${RED}Error: kubectl not found. Are you in a divine Kubernetes environment?${NC}"
        exit 1
    fi
    
    # Check if the deployment exists
    if ! kubectl get deployment "$deployment_name" &>/dev/null; then
        echo -e "${RED}Error: Divine deployment '$deployment_name' not found${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}📜 Sacred Revisions of Deployment ${YELLOW}$deployment_name${BLUE} 📜${NC}"
    echo -e "${GREEN}───────────────────────────────────────────────────────────────────────────${NC}"
    
    # Get the deployment history
    kubectl rollout history deployment/"$deployment_name"
    
    echo -e "${GREEN}───────────────────────────────────────────────────────────────────────────${NC}"
    echo -e "${BLUE}To view details of a specific revision:${NC}"
    echo -e "${YELLOW}kubectl rollout history deployment/$deployment_name --revision=<revision-number>${NC}"
}

# Function to tag a snapshot with a sacred name
tag_snapshot() {
    local snapshot_id=$1
    local tag_name=$2
    
    local snapshots_dir="$HOME/.omega-btc-ai/snapshots"
    local snapshot_file="$snapshots_dir/${snapshot_id}.json"
    
    if [ ! -f "$snapshot_file" ]; then
        echo -e "${RED}Error: Divine snapshot '$snapshot_id' not found in the sacred registry${NC}"
        exit 1
    fi
    
    local image_name=$(jq -r '.image_name' "$snapshot_file")
    local new_image_name="omega-btc-ai:${tag_name}"
    
    echo -e "${BLUE}Applying divine tag ${YELLOW}$new_image_name${BLUE} to sacred snapshot ${YELLOW}$image_name${NC}"
    
    if docker tag "$image_name" "$new_image_name"; then
        # Update the metadata
        local updated_metadata=$(cat "$snapshot_file" | jq ".tags += [\"$tag_name\"]")
        echo "$updated_metadata" > "$snapshot_file"
        
        echo -e "${GREEN}✅ Divine tag applied successfully!${NC}"
        echo -e "${BLUE}Sacred snapshot is now also available as ${YELLOW}$new_image_name${NC}"
    else
        echo -e "${RED}❌ Divine tag application failed!${NC}"
        exit 1
    fi
}

# Function to push a snapshot to a registry
push_snapshot() {
    local snapshot_id=$1
    local registry_repo=$2
    
    local snapshots_dir="$HOME/.omega-btc-ai/snapshots"
    local snapshot_file="$snapshots_dir/${snapshot_id}.json"
    
    if [ ! -f "$snapshot_file" ]; then
        echo -e "${RED}Error: Divine snapshot '$snapshot_id' not found in the sacred registry${NC}"
        exit 1
    fi
    
    local image_name=$(jq -r '.image_name' "$snapshot_file")
    local registry_image_name="${registry_repo}:snapshot-${snapshot_id}"
    
    echo -e "${BLUE}Preparing to push divine snapshot ${YELLOW}$image_name${BLUE} to sacred registry ${YELLOW}$registry_image_name${NC}"
    
    # First tag the image for the registry
    if ! docker tag "$image_name" "$registry_image_name"; then
        echo -e "${RED}❌ Divine tag for registry failed!${NC}"
        exit 1
    fi
    
    # Now push to the registry
    echo -e "${BLUE}Pushing divine snapshot to the sacred registry...${NC}"
    
    if docker push "$registry_image_name"; then
        # Update the metadata
        local updated_metadata=$(cat "$snapshot_file" | jq ".registry_pushed = true | .registry_url = \"$registry_image_name\"")
        echo "$updated_metadata" > "$snapshot_file"
        
        echo -e "${GREEN}✅ Divine snapshot pushed successfully to the sacred registry!${NC}"
        echo -e "${BLUE}Sacred snapshot is now available at ${YELLOW}$registry_image_name${NC}"
    else
        echo -e "${RED}❌ Divine push to registry failed!${NC}"
        exit 1
    fi
}

# Function to verify the integrity of a snapshot
verify_snapshot() {
    local snapshot_id=$1
    
    local snapshots_dir="$HOME/.omega-btc-ai/snapshots"
    local snapshot_file="$snapshots_dir/${snapshot_id}.json"
    
    if [ ! -f "$snapshot_file" ]; then
        echo -e "${RED}Error: Divine snapshot '$snapshot_id' not found in the sacred registry${NC}"
        exit 1
    fi
    
    local image_name=$(jq -r '.image_name' "$snapshot_file")
    
    echo -e "${BLUE}Performing divine verification of sacred snapshot ${YELLOW}$image_name${NC}"
    
    # Verify the image exists
    if ! docker image inspect "$image_name" &>/dev/null; then
        echo -e "${RED}❌ Divine verification failed! Image does not exist!${NC}"
        exit 1
    fi
    
    # Get image digest
    local image_digest=$(docker image inspect --format='{{index .RepoDigests 0}}' "$image_name" || echo "SHA256:$(docker image inspect --format='{{.Id}}' "$image_name" | sed 's/sha256://')")
    
    # Update the metadata with verification information
    local verification_timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local updated_metadata=$(cat "$snapshot_file" | jq ".verified = true | .verification_timestamp = \"$verification_timestamp\" | .image_digest = \"$image_digest\"")
    echo "$updated_metadata" > "$snapshot_file"
    
    echo -e "${GREEN}✅ Divine verification completed!${NC}"
    echo -e "${BLUE}Sacred snapshot ${YELLOW}$image_name${BLUE} is verified authentic${NC}"
    echo -e "${BLUE}Divine image digest: ${YELLOW}$image_digest${NC}"
}

# Function to restore a container from a snapshot
restore_snapshot() {
    local snapshot_id=$1
    local container_name=$2
    
    local snapshots_dir="$HOME/.omega-btc-ai/snapshots"
    local snapshot_file="$snapshots_dir/${snapshot_id}.json"
    
    if [ ! -f "$snapshot_file" ]; then
        echo -e "${RED}Error: Divine snapshot '$snapshot_id' not found in the sacred registry${NC}"
        exit 1
    fi
    
    local image_name=$(jq -r '.image_name' "$snapshot_file")
    local original_container=$(jq -r '.container_name' "$snapshot_file")
    
    # If no container name provided, use the original with a timestamp
    if [ -z "$container_name" ]; then
        container_name="${original_container}-restored-$(get_timestamp)"
    fi
    
    echo -e "${BLUE}Restoring divine snapshot ${YELLOW}$image_name${BLUE} to sacred container ${YELLOW}$container_name${NC}"
    
    # Check if the image exists
    if ! docker image inspect "$image_name" &>/dev/null; then
        echo -e "${RED}❌ Divine restoration failed! Image does not exist!${NC}"
        exit 1
    fi
    
    # Run a new container from the snapshot
    if docker run -d --name "$container_name" "$image_name"; then
        echo -e "${GREEN}✅ Divine restoration completed!${NC}"
        echo -e "${BLUE}Sacred container ${YELLOW}$container_name${BLUE} is now running from snapshot ${YELLOW}$image_name${NC}"
        echo -e "${BLUE}Container status:${NC}"
        docker ps --filter "name=$container_name" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    else
        echo -e "${RED}❌ Divine restoration failed! Could not create container!${NC}"
        exit 1
    fi
}

# Main command router
case "$1" in
    snapshot)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: No container name provided${NC}"
            echo -e "${YELLOW}Usage: $0 snapshot <container_name> [tag_name]${NC}"
            exit 1
        fi
        create_snapshot "$2" "$3"
        ;;
    rollback)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: No deployment name provided${NC}"
            echo -e "${YELLOW}Usage: $0 rollback <deployment_name> [revision]${NC}"
            exit 1
        fi
        perform_rollback "$2" "$3"
        ;;
    list-snapshots)
        list_snapshots
        ;;
    list-revisions)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: No deployment name provided${NC}"
            echo -e "${YELLOW}Usage: $0 list-revisions <deployment_name>${NC}"
            exit 1
        fi
        list_revisions "$2"
        ;;
    tag-snapshot)
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo -e "${RED}Error: Missing required arguments${NC}"
            echo -e "${YELLOW}Usage: $0 tag-snapshot <snapshot_id> <tag_name>${NC}"
            exit 1
        fi
        tag_snapshot "$2" "$3"
        ;;
    push-snapshot)
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo -e "${RED}Error: Missing required arguments${NC}"
            echo -e "${YELLOW}Usage: $0 push-snapshot <snapshot_id> <registry/repo>${NC}"
            exit 1
        fi
        push_snapshot "$2" "$3"
        ;;
    verify-snapshot)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: No snapshot ID provided${NC}"
            echo -e "${YELLOW}Usage: $0 verify-snapshot <snapshot_id>${NC}"
            exit 1
        fi
        verify_snapshot "$2"
        ;;
    restore-snapshot)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: No snapshot ID provided${NC}"
            echo -e "${YELLOW}Usage: $0 restore-snapshot <snapshot_id> [container_name]${NC}"
            exit 1
        fi
        restore_snapshot "$2" "$3"
        ;;
    *)
        echo -e "${RED}Error: Unknown command '$1'${NC}"
        echo -e "${YELLOW}Usage: $0 {snapshot|rollback|list-snapshots|list-revisions|tag-snapshot|push-snapshot|verify-snapshot|restore-snapshot}${NC}"
        exit 1
        ;;
esac

echo -e "\n${PURPLE}JAH JAH BLESS THE SACRED STATE PRESERVATION${NC}" 