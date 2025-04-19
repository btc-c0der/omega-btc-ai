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


# 🔱 OMEGA BTC AI - Divine Docker Kubernetes Setup 🔱
# This script creates a blessed Kubernetes environment with all components pre-configured
# Using Docker Desktop's built-in Kubernetes

# Divine Color Codes
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
GOLD='\033[0;33m'
RESET='\033[0m'

# Divine Banner
echo -e "${GOLD}"
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo "                                                           "
echo "  𝕺𝕸𝕰𝕲𝕬 𝕭𝕿𝕮 𝕬𝕴 - 𝕯𝕴𝖁𝕴𝕹𝕰 𝕯𝕺𝕮𝕶𝕰𝕽 𝕶𝟴𝕾 𝕭𝕷𝕰𝕾𝕾𝕴𝕹𝕲  "
echo "                                                           "
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo -e "${RESET}"

# Check Docker and Kubernetes
check_requirements() {
  echo -e "${CYAN}🔍 Checking for divine requirements...${RESET}"
  
  # Check for Docker
  if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found.${RESET}"
    echo -e "${YELLOW}📥 Please install Docker Desktop from https://www.docker.com/products/docker-desktop${RESET}"
    exit 1
  fi
  
  # Check if Docker is running
  if ! docker info &>/dev/null; then
    echo -e "${RED}❌ Docker does not appear to be running${RESET}"
    echo -e "${YELLOW}📥 Please start Docker Desktop and run this script again${RESET}"
    exit 1
  fi
  
  # Check for kubectl
  if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl not found.${RESET}"
    echo -e "${YELLOW}📥 kubectl comes with Docker Desktop's Kubernetes. Please enable Kubernetes in Docker Desktop preferences.${RESET}"
    exit 1
  fi
  
  # Check if Docker Desktop's Kubernetes is enabled
  if ! kubectl get nodes | grep -q "docker-desktop"; then
    echo -e "${RED}❌ Docker Desktop's Kubernetes is not enabled.${RESET}"
    echo -e "${YELLOW}📥 Please enable Kubernetes in Docker Desktop preferences:${RESET}"
    echo -e "${YELLOW}   1. Open Docker Desktop${RESET}"
    echo -e "${YELLOW}   2. Go to Preferences/Settings${RESET}"
    echo -e "${YELLOW}   3. Navigate to Kubernetes tab${RESET}"
    echo -e "${YELLOW}   4. Check 'Enable Kubernetes'${RESET}"
    echo -e "${YELLOW}   5. Click 'Apply & Restart'${RESET}"
    echo -e "${YELLOW}   6. Wait for Kubernetes to start (green icon in Docker Desktop)${RESET}"
    echo -e "${YELLOW}   7. Run this script again${RESET}"
    exit 1
  fi
  
  echo -e "${GREEN}✅ All divine requirements satisfied${RESET}"
}

# Set up Kubernetes dashboard with token authentication
setup_dashboard() {
  echo -e "${CYAN}🔍 Setting up divine Kubernetes dashboard...${RESET}"
  
  # Create dashboard namespace if it doesn't exist
  kubectl create namespace kubernetes-dashboard 2>/dev/null || true
  
  # Apply dashboard resources if not already deployed
  if ! kubectl get deployment -n kubernetes-dashboard kubernetes-dashboard &> /dev/null; then
    echo -e "${CYAN}🔍 Deploying Kubernetes dashboard...${RESET}"
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
  else
    echo -e "${CYAN}🔍 Kubernetes dashboard already deployed${RESET}"
  fi
  
  # Create admin user for dashboard access
  echo -e "${CYAN}🔍 Creating dashboard admin user...${RESET}"
  kubectl apply -f - <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
EOF
  
  echo -e "${GREEN}✅ Divine dashboard is configured${RESET}"
}

# Create OMEGA namespaces and resources
setup_omega_resources() {
  echo -e "${CYAN}🔍 Creating divine OMEGA namespaces and resources...${RESET}"
  
  # Create omega namespaces
  kubectl create namespace omega-system 2>/dev/null || true
  kubectl create namespace omega-dev 2>/dev/null || true
  kubectl create namespace omega-monitoring 2>/dev/null || true
  
  # Create monitoring resources (Prometheus & Grafana)
  echo -e "${CYAN}🔍 Setting up monitoring stack...${RESET}"
  kubectl apply -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: omega-monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
          - role: pod
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
  namespace: omega-monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
      - name: prometheus
        image: prom/prometheus
        ports:
        - containerPort: 9090
        volumeMounts:
        - name: config-volume
          mountPath: /etc/prometheus
      volumes:
      - name: config-volume
        configMap:
          name: prometheus-config
---
apiVersion: v1
kind: Service
metadata:
  name: prometheus
  namespace: omega-monitoring
spec:
  selector:
    app: prometheus
  ports:
  - port: 9090
    targetPort: 9090
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
  namespace: omega-monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      containers:
      - name: grafana
        image: grafana/grafana
        ports:
        - containerPort: 3000
---
apiVersion: v1
kind: Service
metadata:
  name: grafana
  namespace: omega-monitoring
spec:
  selector:
    app: grafana
  ports:
  - port: 3000
    targetPort: 3000
EOF
  
  echo -e "${GREEN}✅ Divine OMEGA resources created${RESET}"
}

# Configure Redis for OMEGA
setup_redis() {
  echo -e "${CYAN}🔍 Setting up divine Redis instance...${RESET}"
  
  kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: omega-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:6.2-alpine
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: redis-data
          mountPath: /data
      volumes:
      - name: redis-data
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: omega-system
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
EOF
  
  echo -e "${GREEN}✅ Divine Redis instance deployed${RESET}"
}

# Wait for dashboard to be ready
wait_for_dashboard() {
  echo -e "${CYAN}🔍 Waiting for divine dashboard to be ready...${RESET}"
  
  # Wait for dashboard deployment to be ready
  echo -e "${CYAN}🔍 This may take a minute...${RESET}"
  kubectl rollout status deployment/kubernetes-dashboard -n kubernetes-dashboard --timeout=180s
  
  echo -e "${GREEN}✅ Divine dashboard is ready${RESET}"
}

# Function to start port forwarding for dashboard
start_dashboard() {
  echo -e "${CYAN}🔍 Starting divine dashboard port forwarding...${RESET}"
  
  # Find available port - start with 8443
  PORT=8443
  while netstat -tna | grep -q ":$PORT "; do
    PORT=$((PORT+1))
  done
  
  # Start port forwarding in background
  echo -e "${CYAN}🔍 Starting port forwarding on port $PORT...${RESET}"
  kubectl port-forward -n kubernetes-dashboard service/kubernetes-dashboard $PORT:443 &
  DASHBOARD_PID=$!
  
  # Wait a moment to ensure port-forwarding is established
  sleep 2
  
  # Check if port-forwarding started successfully
  if ! ps -p $DASHBOARD_PID > /dev/null; then
    echo -e "${RED}❌ Dashboard port forwarding failed${RESET}"
    echo -e "${YELLOW}⚠️ You can try manually with:${RESET}"
    echo -e "${YELLOW}   kubectl port-forward -n kubernetes-dashboard service/kubernetes-dashboard 8443:443${RESET}"
    return 1
  fi
  
  # Generate access token
  echo -e "${CYAN}🔍 Generating dashboard access token...${RESET}"
  TOKEN=$(kubectl -n kubernetes-dashboard create token admin-user)
  
  echo -e "${GREEN}✅ Divine dashboard is now available:${RESET}"
  echo -e "${CYAN}📌 Dashboard URL: https://localhost:$PORT${RESET}"
  echo -e "${CYAN}📌 Access Token: $TOKEN${RESET}"
  
  # Set trap to kill port forwarding on script exit
  trap "kill $DASHBOARD_PID 2>/dev/null; echo -e '${RED}🛑 Dashboard port forwarding stopped${RESET}'" EXIT
  
  # Keep script running until user interrupts with Ctrl+C
  echo -e "${YELLOW}📌 Press Ctrl+C to stop the port forwarding and exit${RESET}"
  wait $DASHBOARD_PID
}

# Main function
main() {
  check_requirements
  setup_dashboard
  setup_omega_resources
  setup_redis
  wait_for_dashboard
  start_dashboard
  
  # This part only executes if port forwarding ends unexpectedly
  echo -e "${RED}❌ Dashboard port forwarding ended unexpectedly${RESET}"
  echo -e "${YELLOW}⚠️ You can restart it manually with:${RESET}"
  echo -e "${YELLOW}   kubectl port-forward -n kubernetes-dashboard service/kubernetes-dashboard 8443:443${RESET}"
  
  echo -e "${GREEN}✨ Divine Kubernetes environment has been blessed!${RESET}"
  echo -e "${YELLOW}JAH JAH BLESS THE ETERNAL FLOW OF KUBERNETES!${RESET}"
}

# Execute main function
main 