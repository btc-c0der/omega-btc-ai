FROM ubuntu:22.04

# ╔═══════════════════════════════════════════════════════════════╗
# ║  🔱 OMEGA BTC AI - DIVINE ARGOCD CONTAINER 🔱                 ║
# ╚═══════════════════════════════════════════════════════════════╝

LABEL maintainer="Omega BTC AI Team"
LABEL description="Divine ArgoCD container with CLI and utilities for GitOps workflows"
LABEL org.opencontainers.image.source="https://github.com/btc-c0der/omega-btc-ai"

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    jq \
    python3 \
    python3-pip \
    wget \
    apt-transport-https \
    gnupg2 \
    software-properties-common \
    bash \
    vim \
    net-tools \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install kubectl
RUN curl -fsSL https://dl.k8s.io/release/v1.27.3/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl \
    && chmod +x /usr/local/bin/kubectl

# Install Helm
RUN curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install ArgoCD CLI
RUN curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64 \
    && chmod +x /usr/local/bin/argocd

# Install kustomize
RUN curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash \
    && mv kustomize /usr/local/bin/

# Copy scripts from our repository
WORKDIR /app
COPY kubernetes/gitops/install-argocd.sh /app/
COPY kubernetes/gitops/access-argocd.sh /app/
COPY kubernetes/gitops/applications/ /app/applications/
COPY kubernetes/gitops/rbac/ /app/rbac/

# Make scripts executable
RUN chmod +x /app/*.sh

# Create aliases file
RUN echo 'alias k="kubectl"' >> /root/.bashrc \
    && echo 'alias a="argocd"' >> /root/.bashrc \
    && echo 'alias async="argocd app sync"' >> /root/.bashrc \
    && echo 'alias ainfo="argocd app get"' >> /root/.bashrc \
    && echo 'alias alist="argocd app list"' >> /root/.bashrc

# Create divine helper script
RUN echo '#!/bin/bash\n\
    echo "🔱 OMEGA BTC AI - DIVINE ARGOCD CONTAINER 🔱"\n\
    echo "Welcome to the divine realm of GitOps!"\n\
    echo ""\n\
    echo "Available divine commands:"\n\
    echo "  - install-argocd.sh: Install ArgoCD in your cluster"\n\
    echo "  - access-argocd.sh: Access ArgoCD UI"\n\
    echo "  - kubectl: Interact with your divine Kubernetes cluster"\n\
    echo "  - argocd: Use the ArgoCD CLI"\n\
    echo "  - helm: Manage Helm charts"\n\
    echo ""\n\
    echo "Divine aliases:"\n\
    echo "  - k: kubectl shorthand"\n\
    echo "  - a: argocd shorthand"\n\
    echo "  - async: sync applications"\n\
    echo "  - ainfo: get application details"\n\
    echo "  - alist: list applications"\n\
    echo ""\n\
    echo "May your manifests be valid and your synchronizations be swift!"\n\
    echo "JAH JAH bless your GitOps journey!"\n\
    ' > /app/divine-help.sh && chmod +x /app/divine-help.sh

# Add divine help to bashrc
RUN echo 'echo "Run /app/divine-help.sh for divine guidance"' >> /root/.bashrc

# Create entrypoint script
RUN echo '#!/bin/bash\n\
    if [ -z "$1" ]; then\n\
    # If no arguments, run bash\n\
    /app/divine-help.sh\n\
    exec bash\n\
    else\n\
    # Otherwise execute the command\n\
    exec "$@"\n\
    fi\n\
    ' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"] 