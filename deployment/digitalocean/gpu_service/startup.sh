#!/bin/bash

# Log file setup
LOGFILE="/var/log/gpu-startup.log"
exec 1> >(tee -a "$LOGFILE") 2>&1

echo "[$(date)] Starting GPU droplet initialization..."

# System optimization for GPU workloads
setup_system() {
    echo "[$(date)] Setting up system optimizations..."
    
    # Disable CPU frequency scaling for better performance
    echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
    
    # Set up huge pages for better memory performance
    echo 1024 | tee /proc/sys/vm/nr_hugepages
    
    # Optimize I/O scheduler for NVMe
    echo none | tee /sys/block/nvme0n1/queue/scheduler
    
    # Increase file descriptors limit
    echo "fs.file-max = 2097152" >> /etc/sysctl.conf
    echo "* soft nofile 1048576" >> /etc/security/limits.conf
    echo "* hard nofile 1048576" >> /etc/security/limits.conf
    sysctl -p
}

# NVIDIA configuration
setup_gpu() {
    echo "[$(date)] Configuring NVIDIA settings..."
    
    # Set persistence mode
    nvidia-smi -pm 1
    
    # Set GPU clock speeds to maximum
    nvidia-smi -ac 5001,1590
    
    # Enable ECC if available
    nvidia-smi --ecc-config=1
    
    # Set compute mode to default
    nvidia-smi -c 0
}

# Model preparation
setup_models() {
    echo "[$(date)] Setting up ML models..."
    
    # Create model directory if it doesn't exist
    mkdir -p /app/models
    
    # Set correct permissions
    chown -R www-data:www-data /app/models
    chmod -R 755 /app/models
    
    # Download and cache models if needed
    if [ ! -f "/app/models/.initialized" ]; then
        echo "[$(date)] Initializing model cache..."
        python3 -c "
from diffusers import StableDiffusionPipeline
import torch

# Initialize models with GPU optimization
model_id = 'stabilityai/stable-diffusion-2-1'
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    cache_dir='/app/models'
)

# Save initialization marker
with open('/app/models/.initialized', 'w') as f:
    f.write('Models initialized successfully')
"
    fi
}

# Monitoring setup
setup_monitoring() {
    echo "[$(date)] Setting up monitoring..."
    
    # Install node exporter if not present
    if ! command -v node_exporter &> /dev/null; then
        wget https://github.com/prometheus/node_exporter/releases/download/v1.7.0/node_exporter-1.7.0.linux-amd64.tar.gz
        tar xvfz node_exporter-*.tar.gz
        mv node_exporter-*/node_exporter /usr/local/bin/
        rm -rf node_exporter-*
    fi
    
    # Start node exporter
    nohup node_exporter \
        --collector.gpu \
        --collector.cpu \
        --collector.meminfo \
        --collector.diskstats &
    
    # Setup GPU metrics collection
    nohup nvidia-smi --query-gpu=timestamp,temperature.gpu,utilization.gpu,utilization.memory,memory.total,memory.free,memory.used --format=csv -l 60 > /var/log/gpu-metrics.log &
}

# Security hardening
setup_security() {
    echo "[$(date)] Applying security configurations..."
    
    # Configure firewall
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow ssh
    ufw allow 8080/tcp  # API port
    ufw allow 9100/tcp  # Node exporter
    ufw --force enable
    
    # Set secure permissions
    chmod 600 /app/.env
    chmod 600 /root/.ssh/authorized_keys
    
    # Enable automatic security updates
    apt-get install -y unattended-upgrades
    echo 'APT::Periodic::Update-Package-Lists "1";' > /etc/apt/apt.conf.d/20auto-upgrades
    echo 'APT::Periodic::Unattended-Upgrade "1";' >> /etc/apt/apt.conf.d/20auto-upgrades
}

# Main execution
main() {
    echo "[$(date)] Starting main initialization sequence..."
    
    setup_system
    setup_gpu
    setup_models
    setup_monitoring
    setup_security
    
    echo "[$(date)] GPU droplet initialization completed successfully!"
}

# Execute main function
main 