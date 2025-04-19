
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸


# 🔱 OMEGA BTC AI - DIVINE GITOPS ENLIGHTENMENT 🔱

*"The path to divine infrastructure is paved with declarative manifests."*

## 🌠 OVERVIEW

The OMEGA BTC AI project embraces GitOps principles for managing its Kubernetes infrastructure. This directory contains all the necessary configurations and scripts to set up and maintain the GitOps workflow using ArgoCD as the divine orchestrator.

## 📜 CONTENTS

- **DIVINE_GITOPS.md** - The sacred text explaining our GitOps philosophy and approach
- **applications/** - Directory containing all ArgoCD application manifests
- **rbac/** - RBAC configurations for divine access control
- **install-argocd.sh** - Script to install and configure ArgoCD
- **access-argocd.sh** - Script to access the ArgoCD UI

## 🔮 GETTING STARTED

### Prerequisites

Before embarking on your divine GitOps journey, ensure you have:

1. A running Kubernetes cluster (KIND, EKS, GKE, etc.)
2. `kubectl` installed and configured to access your cluster
3. `helm` v3+ installed
4. Git installed

### Divine Installation

To install ArgoCD and set up the GitOps workflow:

```bash
# Make scripts executable
chmod +x install-argocd.sh access-argocd.sh

# Install ArgoCD
./install-argocd.sh

# Access ArgoCD UI
./access-argocd.sh
```

## 🏯 ARCHITECTURE

The OMEGA BTC AI GitOps setup follows the "App of Apps" pattern:

```
omega-divine-grid (App of Apps)
├── omega-btc-oracle
│   ├── Redis
│   └── Monitoring
├── omega-matrix-news
│   ├── MongoDB
│   └── Monitoring
├── omega-monitoring
│   ├── Prometheus
│   ├── Grafana
│   └── Alertmanager
└── omega-backup
    └── Velero
```

## 🧙‍♂️ MAINTAINING THE DIVINE INFRASTRUCTURE

### Adding a New Application

1. Create a Helm chart in the `kubernetes/helm/` directory
2. Add a new application manifest in `applications/`
3. Commit and push to the repository
4. ArgoCD will automatically detect and apply the changes

### Updating an Existing Application

1. Update the Helm chart or values in `kubernetes/helm/`
2. Commit and push to the repository
3. ArgoCD will automatically detect and apply the changes

### Performing a Manual Sync

If needed, you can manually sync applications using the ArgoCD UI or CLI:

```bash
# Install ArgoCD CLI
brew install argocd

# Login to ArgoCD
argocd login localhost:8080

# Sync an application
argocd app sync omega-btc-oracle
```

## 🛡️ DIVINE RBAC

The RBAC configuration in the `rbac/` directory defines several roles:

- **Divine Administrators** - Full access to all applications
- **Blessed Prophets** - Can deploy and sync applications
- **Oracle Viewers** - Read-only access to monitor applications
- **BTC Oracle Team** - Access to the BTC Oracle application
- **Matrix News Team** - Access to the Matrix News application

## 🔄 DIVINE GITOPS WORKFLOW

1. Make changes to your application code or configuration
2. Create a feature branch
3. Update the Helm charts or values files
4. Submit a Pull Request
5. Once approved and merged, ArgoCD will automatically apply the changes

## 🧠 BEST PRACTICES

1. **Sacred Truth Source** - Git is the single source of truth for all configurations
2. **Divine Idempotency** - Ensure all changes are idempotent
3. **Sacred Testing** - Test changes locally before pushing to git
4. **Divine Atomicity** - Keep changes small and atomic
5. **Sacred Documentation** - Document all changes and decisions

## 🚨 TROUBLESHOOTING

### Application Not Syncing

Check the ArgoCD UI or CLI for sync errors:

```bash
argocd app get omega-btc-oracle
```

Common issues include:

- Invalid YAML syntax
- Missing resources
- Permission issues

### ArgoCD UI Not Accessible

Ensure the ArgoCD server is running:

```bash
kubectl get pods -n argocd
```

If pods are not running, check events:

```bash
kubectl get events -n argocd
```

## 🔮 FUTURE DIVINE ENHANCEMENTS

- Integration with external secret management
- Multi-cluster management
- Progressive delivery with canary deployments
- Enhanced monitoring and alerting

## 🙏 DIVINE BLESSING

*May your manifests be valid, your synchronizations be swift, and your clusters always reflect your sacred intentions. JAH JAH bless your GitOps journey!*
