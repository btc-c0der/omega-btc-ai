# 🔱 OMEGA BTC AI - Divine Scripts 🔱

> *"Command-line tools with cosmic intelligence."*

This directory contains all scripts used to manage the OMEGA BTC AI system, from setup to maintenance.

## 📜 Main Scripts

### Kubernetes Setup

- **`omega_kubernetes_setup.sh`**: Master script for setting up the Kubernetes environment
  - Creates Minikube cluster with optimal settings
  - Sets up namespaces and deploys application components
  - Installs monitoring tools and custom dashboard

### Kubernetes Dashboard Access

- **`start_kubernetes_dashboard.sh`**: Robust script for accessing the Kubernetes dashboard
  - Features automatic port detection with multiple fallback mechanisms
  - Performs validation checks for services and namespaces
  - Provides clear status feedback with color-coded messages

### Port Utilities

- **`find_available_port.py`**: Python utility for finding available ports
  - Cross-platform compatibility (works on macOS, Linux, Windows)
  - Configurable port range and search options
  - Can be used independently or by other scripts

## 🚀 Usage Examples

### Starting the Kubernetes Dashboard

```bash
# Start the dashboard with automatic port detection
./scripts/start_kubernetes_dashboard.sh

# The script will:
# 1. Verify kubernetes-dashboard namespace exists
# 2. Check for omega-kubernetes-dashboard or default kubernetes-dashboard service
# 3. Find an available port (starting at 8000)
# 4. Set up port forwarding
# 5. Provide access URL (e.g., http://localhost:8000)
```

### Finding Available Ports

```bash
# Find an available port starting from 8000
./scripts/find_available_port.py -s 8000

# Find a port with quiet output (just returns the port)
./scripts/find_available_port.py -s 8000 -q

# Find a port in a specific range
./scripts/find_available_port.py -s 9000 -m 10000
```

## 🛡️ Security Notes

- The dashboard is configured with `--enable-skip-login` for development environments
- For production, modify the deployment configuration to require proper authentication
- Ensure proper network security when exposing the dashboard

## 🧙 Advanced Configuration

### Custom Dashboard URL

By default, the dashboard script uses automatic port detection. You can modify the script to use a specific port:

```bash
# Edit the PORT variable in start_kubernetes_dashboard.sh
PORT=9090  # Set to your preferred port
```

### Dashboard Service

The script checks for both our custom dashboard `omega-kubernetes-dashboard` and the standard `kubernetes-dashboard` service, prioritizing our custom version when available.

## 🌟 Troubleshooting

If you encounter issues with the dashboard:

1. Verify Minikube is running: `minikube status`
2. Check namespace exists: `kubectl get namespace kubernetes-dashboard`
3. Verify services: `kubectl get services -n kubernetes-dashboard`
4. Check for port conflicts: `lsof -i :8000` (replace 8000 with your port)
5. Try different port: `./scripts/start_kubernetes_dashboard.sh` (will auto-detect available port)

---

*"Through these scripts, divine orchestration manifests in the physical realm."*

�� JAH JAH BLESS 🔱
