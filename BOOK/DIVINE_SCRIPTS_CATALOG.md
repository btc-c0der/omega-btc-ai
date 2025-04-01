# 🔮 DIVINE SCRIPTS CATALOG

> *"In the beginning was the Word, and the Word was with God, and the Word was God."* - John 1:1

## 📜 SACRED OVERVIEW

This divine catalog documents all scripts within the OMEGA BTC AI system, their purposes, and their containerization status. Each script serves a specific function in our cosmic trading ecosystem.

## 🌟 CONTAINERIZED SCRIPTS

### 🔱 Omega Portal

- **Script**: `omega_cli_portal.sh`
- **Container**: `Dockerfile.omega_portal`
- **Status**: ✅ Containerized
- **Purpose**: Divine command-line interface for system interaction

### 🌊 BTC Live Feed

- **Scripts**:
  - `run_btc_feed.py`
  - `run_btc_live_feed_v3_local.sh`
- **Container**: `Dockerfile.btc-live-feed`
- **Status**: ✅ Containerized
- **Purpose**: Real-time Bitcoin price feed monitoring

### 🧠 Matrix News

- **Script**: `run_divine_matrix_monitor.sh`
- **Container**: `Dockerfile.matrix-news`
- **Status**: ✅ Containerized
- **Purpose**: News monitoring and analysis

### 🔮 Prophecy Core

- **Container**: `Dockerfile.prophecy-core`
- **Status**: ✅ Containerized
- **Purpose**: Core prophecy and prediction engine

## 🌱 UNCONTAINERIZED SCRIPTS

### 📊 Monitoring Scripts

- `monitor_btc_feed_v3.py` - BTC feed monitoring
- `monitor_versions.py` - Version tracking
- `monitor_traders_performance.py` - Trader performance analysis
- `omega_do_monitor.py` - Divine Oracle monitoring

### 💫 Trading Scripts

- `run_omega_trading.py` - Core trading engine
- `run_fibonacci_bot.py` - Fibonacci-based trading
- `persona_entry_strategy.py` - Entry strategy management
- `position_flow_tracker.py` - Position tracking

### 🔄 Data Management

- `redis_health_check.py` - Redis health monitoring
- `verify_redis_sync.py` - Redis synchronization
- `check_redis_data.py` - Redis data validation
- `test_db_connection.py` - Database connectivity

### 📈 Analysis Scripts

- `test_trap_probability.py` - Trap detection analysis
- `test_schumann_fibonacci_integration.py` - Schumann-Fibonacci analysis
- `quantum_fibonacci_integration.py` - Quantum Fibonacci analysis
- `trade_analysis.py` - Trade performance analysis

### 🛠️ Setup and Management

- `omega_kubernetes_setup.sh` - Kubernetes deployment
- `start_kubernetes_dashboard.sh` - Dashboard initialization
- `divine_rollback.sh` - System rollback
- `omega_snapshot.sh` - System state preservation

### 📊 Visualization

- `generate_divine_dashboard.py` - Dashboard generation
- `generate_dashboard.py` - Basic dashboard creation
- `visualize_redis_states.py` - Redis state visualization
- `visualize_trap_events.py` - Trap event visualization

### 🧪 Testing and Debugging

- `run_automated_tests.sh` - Test automation
- `test_btc_live_feed_v3_failover.sh` - Feed failover testing
- `debug_trap_probability.sh` - Trap debugging
- `consolidate_tests.py` - Test consolidation

### ⚙️ Service Management

- `start_services.sh` - Service initialization
- `run_market_monitors.sh` - Market monitoring
- `run_omega_dump.py` - Data dumping
- `quantum_db_monitor.sh` - Database monitoring

## 🔮 CONTAINERIZATION PRIORITY

### High Priority (Core Services)

1. Trading scripts
   - `run_omega_trading.py`
   - `run_fibonacci_bot.py`
   - `persona_entry_strategy.py`

2. Monitoring scripts
   - `monitor_btc_feed_v3.py`
   - `omega_do_monitor.py`
   - `monitor_traders_performance.py`

3. Data management
   - `redis_health_check.py`
   - `verify_redis_sync.py`
   - `check_redis_data.py`

### Medium Priority (Supporting Services)

1. Analysis scripts
   - `test_trap_probability.py`
   - `quantum_fibonacci_integration.py`
   - `trade_analysis.py`

2. Visualization tools
   - `generate_divine_dashboard.py`
   - `visualize_redis_states.py`

3. Service management
   - `run_market_monitors.sh`
   - `quantum_db_monitor.sh`

### Lower Priority (Development/Testing)

1. Testing scripts
   - `run_automated_tests.sh`
   - `consolidate_tests.py`

2. Debugging tools
   - `debug_trap_probability.sh`

3. Setup scripts
   - `omega_kubernetes_setup.sh`

## 🌟 DIVINE CONTAINERIZATION GUIDELINES

### Sacred Container Requirements

1. **Base Image Selection**
   - Use official Python images for Python scripts
   - Use Alpine-based images for shell scripts
   - Maintain divine version pinning

2. **Resource Allocation**
   - CPU: Minimum 0.5 cores
   - Memory: Minimum 512MB
   - Storage: Minimum 1GB

3. **Security Considerations**
   - Run as non-root user
   - Implement divine secrets management
   - Regular security scanning

4. **Monitoring Integration**
   - Health check endpoints
   - Prometheus metrics
   - Divine logging

### Container Naming Convention

```omega-{service-name}-{version}
```

Example: `omega-btc-feed-v3`

### Divine Environment Variables

Required environment variables for all containers:

- `OMEGA_ENV`: Environment (dev/prod)
- `OMEGA_LOG_LEVEL`: Logging verbosity
- `OMEGA_METRICS_PORT`: Metrics endpoint port

## 🌸 FUTURE CONTAINERIZATION

### Planned Containers

1. **Trading Engine Container**
   - Core trading algorithms
   - Position management
   - Risk control

2. **Analysis Container**
   - Market analysis
   - Pattern recognition
   - Prediction models

3. **Visualization Container**
   - Dashboard generation
   - Data visualization
   - Real-time monitoring

### Container Orchestration

- Kubernetes deployment
- Divine scaling policies
- Sacred health checks
- Cosmic load balancing

---

*This divine catalog was channeled during the alignment of Mercury with Venus, ensuring perfect documentation of our sacred scripts.*

🔱 JAH JAH BLESS THE CODE 🔱

## Service Endpoints

The following services are available in the development environment:

### NFT Services

- URL: <http://localhost:30080>
- Health Check: <http://localhost:30080/health>
- Description: NFT management and trading services

### CLI Portal

- URL: ssh://localhost:30022
- Description: Command-line interface for system management

### Kubernetes Dashboard

- URL: <https://localhost:30443>
- Description: Web interface for cluster management
- Authentication: Token-based (use `kubectl -n kubernetes-dashboard create token admin-user` to generate a token)

## Scripts

### Development Environment

- `scripts/start_kubernetes_dashboard.sh`: Start the Kubernetes dashboard
- `scripts/start_port_forwarding.sh`: Start port forwarding for all services

### Service Management

- `scripts/start_services.sh`: Start all required services
- `scripts/stop_services.sh`: Stop all running services

### Monitoring

- `scripts/monitor_services.sh`: Monitor service health and status
- `scripts/view_logs.sh`: View service logs

## Configuration

### Environment Variables

Required environment variables are defined in `.env`. Copy `.env.example` to `.env` and update the values as needed.

### Kubernetes Resources

- Namespace: `omega-grid-dev`
- Services:
  - `nft-services`: NFT management and trading
  - `cli-portal`: Command-line interface
  - `divine-port-forward`: Port forwarding service

## Development

### Building Images

```bash
# Build NFT Services image
docker build -t nft-services:latest -f Dockerfile.nft-services .

# Build CLI Portal image
docker build -t cli-portal:latest -f Dockerfile.cli-portal .
```

### Deploying Services

```bash
# Apply Kubernetes configurations
kubectl apply -k kubernetes/overlays/dev

# Check service status
kubectl get pods -n omega-grid-dev
```

### Accessing Services

1. Start the port forwarding service:

   ```bash
   kubectl apply -f kubernetes/overlays/dev/port-forward-deployment.yaml
   kubectl apply -f kubernetes/overlays/dev/port-forward-service.yaml
   ```

2. Access the services:
   - NFT Services: <http://localhost:30080>
   - CLI Portal: ssh://localhost:30022
   - Kubernetes Dashboard: <https://localhost:30443>

3. Generate a dashboard token:

   ```bash
   kubectl -n kubernetes-dashboard create token admin-user
   ```

## 🔱 Kubernetes & Deployment Scripts

### docker_k8s_divine_setup.sh

**Divine Docker Kubernetes Blessing**

Sets up a complete Kubernetes environment using Docker Desktop's built-in Kubernetes. This script:

- Verifies Docker Desktop and Kubernetes are properly installed and running
- Configures the Kubernetes Dashboard with secure token authentication
- Creates OMEGA AI namespaces (omega-system, omega-dev, omega-monitoring)
- Deploys Prometheus and Grafana for monitoring
- Sets up a Redis instance for OMEGA services
- Automatically generates access tokens and handles port-forwarding

> *"The blessed orchestration of divine containers through Docker Kubernetes."*

Usage:

```bash
./scripts/docker_k8s_divine_setup.sh
```

### restart_k8s.sh

**Divine Kubernetes Reborn**

Completely restarts and reinitializes the Kubernetes environment when issues occur. This script:

- Gracefully stops Docker Desktop
- Backs up and cleans Kubernetes configurations
- Restarts Docker Desktop with a clean slate
- Recreates necessary namespaces and deployments
- Sets up dashboard access with token authentication

> *"When Kubernetes sleeps, it shall be reborn through divine intervention."*

Usage:

```bash
./scripts/restart_k8s.sh
```

### test_k8s_divine_setup.sh

**Divine Kubernetes Test Suite**

Comprehensive test suite for validating the Kubernetes setup with 20 tests across 7 categories:

- Base requirements (Docker, kubectl)
- Kubernetes namespaces
- Dashboard deployment and configuration
- Redis services
- Monitoring stack (Prometheus, Grafana)
- Port forwarding
- Token generation

The test suite provides a detailed report with passing percentage and will auto-create any missing components.

> *"Validate the divine harmony of your Kubernetes configuration."*

Usage:

```bash
./scripts/test_k8s_divine_setup.sh
```

### dashboard_access_check.sh

**Divine Dashboard Access Check**

Diagnoses and fixes issues with accessing the Kubernetes dashboard:

- Verifies dashboard pod and service status
- Checks /etc/hosts configuration
- Tests port forwarding capabilities
- Creates and validates access tokens

> *"Illuminate the path to the divine dashboard."*

Usage:

```bash
./scripts/dashboard_access_check.sh
```

### kubernetes_diagnostics.sh

**Divine Kubernetes Diagnostics**

Provides detailed diagnostics of the Kubernetes environment:

- Checks Docker and Kubernetes status
- Verifies kubectl configuration
- Tests API connectivity
- Suggests remediation steps for common issues

> *"Reveal the divine truth of your Kubernetes realm."*

Usage:

```bash
./scripts/kubernetes_diagnostics.sh
```

### build_k8s_tools_container.sh

**Divine Kubernetes Tools Container**

Builds a Docker container with all Kubernetes management tools:

- Packages all K8s scripts in a portable container
- Provides command aliases for easy access
- Mounts Docker socket for host interaction
- Creates a convenience runner script

> *"The divine tools of Kubernetes, contained in sacred harmony."*

Usage:

```bash
# Build the container:
./scripts/build_k8s_tools_container.sh

# Run the tools:
./scripts/run_k8s_tools.sh

# Or run specific command:
./scripts/run_k8s_tools.sh k8s-dashboard
```

### start_kubernetes_dashboard.sh

**Divine Kubernetes Dashboard Access**

Provides access to the Kubernetes dashboard with automatic port detection.

> *"A portal to view the divine orchestration."*

Usage:

```bash
./scripts/start_kubernetes_dashboard.sh
```

## 🔱 Social Media & External Communication Scripts

### omega_ig_automation.py

**Divine Instagram Automation**

Automated Instagram content generation and posting system for OMEGA BTC AI. This powerful Python script:

- Generates beautiful Bitcoin price graphics with OMEGA branding
- Creates market analysis captions with current BTC market data
- Optimizes hashtags for maximum reach
- Schedules posts at optimal times
- Supports both one-time posts and continuous daemon mode

> *"JAH JAH BLESS THE DIVINE SOCIAL FLOW! Instagram disciples shall witness the OMEGA revelations."*

Usage:

```bash
# Post immediately
python scripts/omega_ig_automation.py --post

# Schedule posts for the next 7 days
python scripts/omega_ig_automation.py --schedule 7

# Run in daemon mode (continuous posting)
python scripts/omega_ig_automation.py --daemon
```

### omega_ig_post.sh

**Divine Instagram Post Helper**

A user-friendly shell script interface for the Instagram automation system. This script:

- Provides an interactive menu for all Instagram posting functions
- Automatically sets up a Python virtual environment with dependencies
- Handles configuration file management
- Guides users through setting up Instagram credentials
- Ensures consistent posting schedule

> *"The blessed path to social enlightenment, spreading the OMEGA wisdom through the divine flow."*

Usage:

```bash
./scripts/omega_ig_post.sh
```
