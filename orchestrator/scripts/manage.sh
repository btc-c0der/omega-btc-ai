#!/bin/bash

# 🔱 OMEGA BTC AI - SACRED ORCHESTRATION MANAGEMENT SCRIPT 🔱

# Divine Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Divine Functions
print_header() {
    echo -e "${BLUE}🔱 OMEGA BTC AI - $1 🔱${NC}"
    echo "----------------------------------------"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
}

check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
}

check_env_file() {
    if [ ! -f .env ]; then
        print_error ".env file not found. Please create one from .env.example"
        exit 1
    fi
}

create_directories() {
    print_header "Creating Divine Directories"
    mkdir -p data/{matrix-news,btc-live-feed,prophecy-core,redis,grafana,prometheus,alertmanager}
    mkdir -p logs/{nginx,matrix-news,btc-live-feed,prophecy-core,redis,grafana,prometheus,alertmanager}
    print_success "Directories created successfully"
}

generate_ssl_certificates() {
    print_header "Generating Divine SSL Certificates"
    mkdir -p infra/ng1n1x/ssl
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout infra/ng1n1x/ssl/omega-btc-ai.key \
        -out infra/ng1n1x/ssl/omega-btc-ai.crt \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    print_success "SSL certificates generated successfully"
}

start_services() {
    print_header "Starting Divine Services"
    docker-compose up -d
    print_success "Services started successfully"
}

stop_services() {
    print_header "Stopping Divine Services"
    docker-compose down
    print_success "Services stopped successfully"
}

restart_services() {
    print_header "Restarting Divine Services"
    docker-compose restart
    print_success "Services restarted successfully"
}

check_services() {
    print_header "Checking Divine Services Status"
    docker-compose ps
}

view_logs() {
    print_header "Viewing Divine Logs"
    docker-compose logs -f
}

cleanup() {
    print_header "Cleaning Up Divine Resources"
    docker-compose down -v
    print_success "Resources cleaned up successfully"
}

backup_data() {
    print_header "Backing Up Divine Data"
    timestamp=$(date +%Y%m%d_%H%M%S)
    backup_dir="backups/$timestamp"
    mkdir -p "$backup_dir"
    cp -r data "$backup_dir/"
    print_success "Data backed up successfully to $backup_dir"
}

restore_data() {
    print_header "Restoring Divine Data"
    if [ -z "$1" ]; then
        print_error "Please specify backup directory"
        exit 1
    fi
    cp -r "$1/data"/* data/
    print_success "Data restored successfully"
}

update_services() {
    print_header "Updating Divine Services"
    docker-compose pull
    docker-compose up -d
    print_success "Services updated successfully"
}

# Divine Main Menu
show_menu() {
    print_header "Divine Orchestration Menu"
    echo "1. Start Services"
    echo "2. Stop Services"
    echo "3. Restart Services"
    echo "4. Check Status"
    echo "5. View Logs"
    echo "6. Cleanup Resources"
    echo "7. Backup Data"
    echo "8. Restore Data"
    echo "9. Update Services"
    echo "0. Exit"
    echo "----------------------------------------"
}

# Divine Main Logic
main() {
    check_docker
    check_docker_compose
    check_env_file
    create_directories
    generate_ssl_certificates

    while true; do
        show_menu
        read -p "Enter your choice (0-9): " choice
        case $choice in
            1) start_services ;;
            2) stop_services ;;
            3) restart_services ;;
            4) check_services ;;
            5) view_logs ;;
            6) cleanup ;;
            7) backup_data ;;
            8) read -p "Enter backup directory: " backup_dir; restore_data "$backup_dir" ;;
            9) update_services ;;
            0) print_success "Exiting Divine Orchestration"; exit 0 ;;
            *) print_error "Invalid choice. Please try again." ;;
        esac
        echo
    done
}

# Divine Script Execution
main 