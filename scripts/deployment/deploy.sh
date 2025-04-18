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


# OMEGA BTC AI - Advanced Crypto Trading System
# Copyright (c) 2024 OMEGA BTC AI Team
# Licensed under MIT License - See LICENSE file for details
# SECURITY NOTICE: This script handles sensitive deployment operations

set -e

# Load environment variables
source .env

# Check required environment variables
required_vars=(
    "AWS_ACCESS_KEY_ID"
    "AWS_SECRET_ACCESS_KEY"
    "AWS_REGION"
    "ECR_REPOSITORY"
    "ECS_CLUSTER"
    "ECS_SERVICE"
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "Error: Required environment variable $var is not set"
        exit 1
    fi
done

echo "🚀 Starting OMEGA BTC AI deployment..."

# Build Docker image
echo "📦 Building Docker image..."
docker-compose -f docker-compose.cloud.yml build

# Log in to Amazon ECR
echo "🔑 Logging in to Amazon ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPOSITORY

# Tag and push image
echo "📤 Pushing image to ECR..."
docker tag omega_btc_ai:latest $ECR_REPOSITORY/omega_btc_ai:latest
docker push $ECR_REPOSITORY/omega_btc_ai:latest

# Update ECS service
echo "🔄 Updating ECS service..."
aws ecs update-service \
    --cluster $ECS_CLUSTER \
    --service $ECS_SERVICE \
    --force-new-deployment \
    --region $AWS_REGION

echo "⏳ Waiting for service to stabilize..."
aws ecs wait services-stable \
    --cluster $ECS_CLUSTER \
    --services $ECS_SERVICE \
    --region $AWS_REGION

echo "✅ Deployment completed successfully!"
echo "🔍 Monitor the deployment in AWS Console:"
echo "https://$AWS_REGION.console.aws.amazon.com/ecs/home?region=$AWS_REGION#/clusters/$ECS_CLUSTER/services/$ECS_SERVICE"

echo "🚀 Starting OMEGA BTC AI Deployment Process"
echo "============================================"
echo "Version: $(cat VERSION)"

# Step 1: Create deployment package
echo "📦 Creating deployment package..."
mkdir -p deploy

# Copy core files
cp -r omega_ai deploy/
cp -r config deploy/
cp -r scripts deploy/
cp -r db deploy/
cp -r data deploy/
cp requirements.txt deploy/
cp VERSION deploy/

# Copy documentation
cp README.md deploy/
cp CHANGELOG.md deploy/
cp LICENSE deploy/
cp SCHUMANN_RESONANCE_FIX.md deploy/

# Copy test scripts
cp test_schumann_resonance.py deploy/

# Step 2: Connect to Scaleway and deploy
echo "🔄 Connecting to Scaleway server..."
# ... existing code ... 