#!/bin/bash

# OMEGA Dump Service Runner
# Divine log management system

# Default configuration
LOGS_DIR="logs"
BACKUP_DIR="logs/backup"
REDIS_URL="redis://localhost:6379/0"
BACKUP_INTERVAL=3600

# Create tmux session
SESSION="omega-dump"
tmux new-session -d -s $SESSION

# Set divine window title
tmux rename-window -t $SESSION:0 'OMEGA-DUMP'

# Run the service
tmux send-keys -t $SESSION:0 "python scripts/run_omega_dump.py \
    --logs-dir $LOGS_DIR \
    --backup-dir $BACKUP_DIR \
    --redis-url $REDIS_URL \
    --backup-interval $BACKUP_INTERVAL" C-m

# Attach to session
tmux attach-session -t $SESSION

# JAH BLESS the eternal log stream 