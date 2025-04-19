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


# 🔱 OMEGA BTC AI - Divine Kubernetes Auto Setup 🔱
# This script creates a blessed Kubernetes environment with all components pre-configured

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
echo "  𝕺𝕸𝕰𝕲𝕬 𝕭𝕿𝕮 𝕬𝕴 - 𝕯𝕴𝖁𝕴𝕹𝕰 𝕶𝟴𝕾 𝕬𝖀𝕿𝕺 𝕾𝕰𝕿𝖀𝕻 𝕭𝕷𝕰𝕾𝕾𝕴𝕹𝕲  "
echo "                                                           "
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo -e "${RESET}"

# Check required tools
check_requirements() {
  echo -e "${CYAN}🔍 Checking for divine requirements...${RESET}"
  
  # Check for Docker
  if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Installing...${RESET}"
    # Install Docker based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
      echo -e "${YELLOW}📥 Please install Docker Desktop for Mac manually from https://www.docker.com/products/docker-desktop${RESET}"
      exit 1
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
      sudo apt-get update
      sudo apt-get install -y docker.io
    else
      echo -e "${RED}❌ Unsupported OS for automatic Docker installation${RESET}"
      exit 1
    fi
  fi
  
  # Check for kubectl
  if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl not found. Installing...${RESET}"
    # Install kubectl based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
      brew install kubectl
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
      sudo apt-get update && sudo apt-get install -y kubectl
    else
      echo -e "${RED}❌ Unsupported OS for automatic kubectl installation${RESET}"
      exit 1
    fi
  fi
  
  # Check for minikube
  if ! command -v minikube &> /dev/null; then
    echo -e "${RED}❌ minikube not found. Installing...${RESET}"
    # Install minikube based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
      brew install minikube
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
      curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
      sudo install minikube-linux-amd64 /usr/local/bin/minikube
      rm minikube-linux-amd64
    else
      echo -e "${RED}❌ Unsupported OS for automatic minikube installation${RESET}"
      exit 1
    fi
  fi
  
  echo -e "${GREEN}✅ All divine requirements satisfied${RESET}"
}

# Check if Docker Desktop is running
check_docker_running() {
  echo -e "${CYAN}🔍 Checking if Docker is running...${RESET}"
  
  if ! docker info &>/dev/null; then
    echo -e "${RED}❌ Docker does not appear to be running${RESET}"
    echo -e "${YELLOW}📥 Please start Docker Desktop and run this script again${RESET}"
    exit 1
  fi
  
  echo -e "${GREEN}✅ Docker is running${RESET}"
}

# Start minikube
start_minikube() {
  echo -e "${CYAN}🔍 Starting divine minikube cluster...${RESET}"
  
  if minikube status | grep -q "Running"; then
    echo -e "${YELLOW}⚠️ Minikube is already running${RESET}"
  else
    # Start minikube with docker driver for macOS ARM compatibility
    if [[ "$OSTYPE" == "darwin"* ]] && [[ $(uname -m) == "arm64" ]]; then
      echo -e "${YELLOW}⚠️ Detected macOS ARM architecture, using Docker driver${RESET}"
      minikube start --driver=docker --cpus 2 --memory 4096 --disk-size 20g
    else
      minikube start --cpus 2 --memory 4096 --disk-size 20g
    fi
    
    # Enable addons
    minikube addons enable ingress
    minikube addons enable metrics-server
    minikube addons enable dashboard
  fi
  
  echo -e "${GREEN}✅ Divine minikube cluster is running${RESET}"
}

# Set up Kubernetes dashboard with token authentication
setup_dashboard() {
  echo -e "${CYAN}🔍 Setting up divine Kubernetes dashboard...${RESET}"
  
  # Create dashboard namespace if it doesn't exist
  kubectl create namespace kubernetes-dashboard 2>/dev/null || true
  
  # Apply dashboard resources if not already deployed
  if ! kubectl get deployment -n kubernetes-dashboard kubernetes-dashboard &> /dev/null; then
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml --validate=false
  fi
  
  # Create admin user for dashboard access
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
  kubectl apply -f - --validate=false <<EOF
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
  
  kubectl apply -f - --validate=false <<EOF
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
  kubectl wait --for=condition=available deployment/kubernetes-dashboard -n kubernetes-dashboard --timeout=120s
  
  echo -e "${GREEN}✅ Divine dashboard is ready${RESET}"
}

# Function to start port forwarding for dashboard
start_dashboard() {
  echo -e "${CYAN}🔍 Starting divine dashboard port forwarding...${RESET}"
  
  # Find available port
  PORT=8443
  while netstat -tna | grep -q ":$PORT "; do
    PORT=$((PORT+1))
  done
  
  # Start port forwarding in background
  kubectl port-forward -n kubernetes-dashboard service/kubernetes-dashboard $PORT:443 &
  DASHBOARD_PID=$!
  
  # Generate access token
  TOKEN=$(kubectl -n kubernetes-dashboard create token admin-user)
  
  echo -e "${GREEN}✅ Divine dashboard is now available:${RESET}"
  echo -e "${CYAN}📌 Dashboard URL: https://localhost:$PORT${RESET}"
  echo -e "${CYAN}📌 Access Token: $TOKEN${RESET}"
  
  # Alternatively, use minikube dashboard
  echo -e "${YELLOW}⚠️ If the port forwarding doesn't work, you can also use:${RESET}"
  echo -e "${CYAN}📌 minikube dashboard${RESET}"
  
  # Set trap to kill port forwarding on script exit
  trap "kill $DASHBOARD_PID 2>/dev/null" EXIT
}

# Main function
main() {
  check_requirements
  check_docker_running
  start_minikube
  setup_dashboard
  setup_omega_resources
  setup_redis
  wait_for_dashboard
  start_dashboard
  
  echo -e "${GREEN}✨ Divine Kubernetes environment has been blessed and is ready!${RESET}"
  echo -e "${YELLOW}JAH JAH BLESS THE ETERNAL FLOW OF KUBERNETES!${RESET}"
  
  # Wait for user to interrupt with Ctrl+C
  echo -e "${CYAN}📌 Press Ctrl+C to stop the port forwarding and exit${RESET}"
  wait $DASHBOARD_PID
}

# Execute main function
main 