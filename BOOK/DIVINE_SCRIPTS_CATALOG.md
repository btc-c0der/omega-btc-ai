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

```
omega-{service-name}-{version}
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
