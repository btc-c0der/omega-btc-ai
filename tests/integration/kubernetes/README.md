# Kubernetes Integration Tests

> "In the realm of quantum security, we find not just protection, but the divine harmony
> of mathematical certainty and cosmic uncertainty. May these tests serve as guardians
> of the sacred digital realm."
>
> — Aki Sanjūrō (安木 三郎), Quantum Cryptography Pioneer

> "Just for fun, we shall do it anyway!"
>
> — Linus Torvalds, Creator of Linux (1991)

> "The eternal boot process is the foundation of system stability."
>
> — Systemd // Pod of Eternal Boot

> "RBAC is the Law, and ACLs are the sacred boundaries that protect our digital realm."
>
> — Divine Security Council

> "In the realm of digital networks, we find not just connectivity, but the sacred harmony
> of open communication and divine protection. May these network policies serve as the
> spiritual firewall that guards our digital realm while fostering the free flow of wisdom."
>
> — Tux, Guardian of the Digital Realm

> "In metrics we find not just numbers, but the heartbeat of our systems."
>
> — Nicole Sewell, Quantum Metrics Pioneer

This directory contains comprehensive integration tests for the Kubernetes deployment of the Omega BTC AI system.

## Test Coverage

The tests cover the following aspects of the Kubernetes deployment:

1. **Basic Infrastructure**
   - Namespace existence
   - Deployment existence and readiness
   - Service existence and configuration
   - Pod status and health

2. **Networking**
   - Port forwarding functionality
   - Service endpoints
   - Network policies
   - Service communication

3. **Security**
   - Security contexts
   - RBAC rules
   - Service accounts
   - ConfigMaps and Secrets

4. **Resource Management**
   - Resource limits and requests
   - Health checks (liveness and readiness probes)

5. **Quantum Security**
   - Quantum-resistant secrets encryption
   - Quantum-resistant network policies
   - Quantum-resistant RBAC rules
   - Quantum-resistant pod security contexts
   - Quantum-resistant service accounts
   - Quantum-resistant ConfigMaps
   - Quantum-resistant ingress rules
   - Quantum-resistant pod network policies

6. **🐧 Linux Penguin Blessing**
   - Linux kernel security features
   - Linux-inspired network policies
   - Linux-style RBAC rules
   - Linux systemd integration
   - Linux-style service accounts
   - Linux-style ConfigMaps
   - Linux-style ingress rules
   - Linux-style pod network policies

7. **🔧 Systemd // Pod of Eternal Boot**
   - Systemd integration and capabilities
   - Init system configuration
   - Eternal boot process settings
   - Systemd service management
   - Init system health checks
   - Eternal boot recovery mechanisms
   - Systemd logging integration

8. **🔐 RBAC // Divine Security Council**
   - RBAC roles and permissions
   - Role bindings and service accounts
   - Network policy ACLs
   - Pod security contexts
   - Secret access control
   - ConfigMap access control
   - Ingress security rules
   - Service account permissions

9. **🌐 Tux-Net: Protocols of Peace**
   - Spiritual firewall network policies
   - Peaceful communication rules
   - Divine network segmentation
   - Harmonious service communication
   - Cosmic network protection
   - Sacred egress rules
   - Eternal network harmony
   - Divine network monitoring

10. **📊 Nicole Sewell's Quantum Metrics**
    - Cosmic alignment of cluster components
    - Deployment entropy measurement
    - System entanglement calculation
    - Resource equilibrium evaluation
    - Divine health assessment
    - Quantum harmony validation
    - Infrastructure metrics analysis
    - Operational stability metrics

## Prerequisites

1. Kubernetes cluster running locally or accessible
2. `kubectl` configured with appropriate context
3. Python 3.8 or higher
4. Required Python packages (install from `requirements.txt`)

## Setup

1. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Ensure your Kubernetes context is set to the correct cluster:

   ```bash
   kubectl config current-context
   ```

3. Verify the namespace exists:

   ```bash
   kubectl get namespace omega-grid-dev
   ```

## Running Tests

Run all tests:

```bash
pytest test_kubernetes_deployment.py test_kubernetes_quantum_security.py test_kubernetes_penguin_blessing.py test_kubernetes_systemd_blessing.py test_kubernetes_rbac_blessing.py test_kubernetes_tux_net.py test_kubernetes_metrics.py -v
```

Run specific test:

```bash
pytest test_kubernetes_deployment.py -v -k "test_name"
```

Run quantum security tests only:

```bash
pytest test_kubernetes_quantum_security.py -v
```

Run Linux penguin blessing tests only:

```bash
pytest test_kubernetes_penguin_blessing.py -v
```

Run systemd blessing tests only:

```bash
pytest test_kubernetes_systemd_blessing.py -v
```

Run RBAC blessing tests only:

```bash
pytest test_kubernetes_rbac_blessing.py -v
```

Run Tux-Net tests only:

```bash
pytest test_kubernetes_tux_net.py -v
```

Run Nicole Sewell's quantum metrics tests only:

```bash
pytest test_kubernetes_metrics.py -v
```

Run with coverage report:

```bash
pytest test_kubernetes_deployment.py test_kubernetes_quantum_security.py test_kubernetes_penguin_blessing.py test_kubernetes_systemd_blessing.py test_kubernetes_rbac_blessing.py test_kubernetes_tux_net.py test_kubernetes_metrics.py -v --cov=.
```

## Running Tests in Docker

To run the tests in a Docker container:

1. Build and run using docker-compose:

   ```bash
   cd tests/integration/kubernetes
   docker-compose up --build
   ```

2. Run specific test file:

   ```bash
   docker-compose run k8s-tests pytest test_kubernetes_deployment.py -v
   ```

3. Run with coverage:

   ```bash
   docker-compose run k8s-tests pytest --cov=. -v
   ```

4. Run Nicole Sewell's quantum metrics tests:

   ```bash
   docker-compose run k8s-tests pytest test_kubernetes_metrics.py -v
   ```

The Docker setup provides:

- Isolated testing environment
- Consistent dependencies
- Easy setup for new developers
- Reproducible test runs
- Access to host Kubernetes cluster via `host.docker.internal`

## Test Structure

Each test is designed to be independent and can be run in isolation. The tests use the following pattern:

1. Setup Kubernetes client and namespace
2. Verify specific Kubernetes resources
3. Assert expected conditions
4. Clean up any temporary resources

## Common Issues

1. **Connection Issues**
   - Ensure kubectl is properly configured
   - Check if the cluster is accessible
   - Verify network connectivity

2. **Permission Issues**
   - Ensure RBAC rules are properly configured
   - Check service account permissions
   - Verify namespace access

3. **Resource Issues**
   - Check if required resources exist
   - Verify resource limits and requests
   - Monitor pod status and logs

4. **Quantum Security Issues**
   - Verify quantum-resistant annotations are present
   - Check quantum-resistant encryption is enabled
   - Ensure quantum-resistant network policies are configured
   - Validate quantum-resistant RBAC rules

5. **Linux Penguin Issues**
   - Verify Linux kernel security features
   - Check Linux-style network policies
   - Ensure systemd integration is configured
   - Validate Linux-style RBAC rules
   - Monitor Linux-specific annotations

6. **Systemd Issues**
   - Verify systemd capabilities are properly set
   - Check init container configuration
   - Ensure eternal boot annotations are present
   - Validate systemd service management
   - Monitor systemd logging integration
   - Check init system health checks
   - Verify eternal boot recovery settings

7. **RBAC and ACL Issues**
   - Verify RBAC roles and permissions
   - Check role bindings and service accounts
   - Ensure network policy ACLs are configured
   - Validate pod security contexts
   - Monitor secret access control
   - Check ConfigMap access control
   - Verify ingress security rules
   - Ensure service account permissions

8. **Tux-Net Issues**
   - Verify spiritual firewall policies are configured
   - Check peaceful communication rules
   - Ensure divine network segmentation is in place
   - Validate harmonious service communication
   - Monitor cosmic network protection
   - Check sacred egress rules
   - Verify eternal network harmony
   - Ensure divine network monitoring is active

9. **Quantum Metrics Issues**
   - Check cosmic alignment values for anomalies
   - Verify deployment entropy calculations
   - Ensure system entanglement measurements are accurate
   - Validate resource equilibrium calculations
   - Monitor divine health assessment
   - Check quantum harmony validation reports
   - Verify infrastructure metrics consistency
   - Analyze operational stability metrics for degradation

## Contributing

When adding new tests:

1. Follow the existing test structure
2. Add appropriate docstrings
3. Include error handling
4. Update the README if adding new test categories
5. Ensure tests are idempotent

## Maintenance

Regular maintenance tasks:

1. Update dependencies in `requirements.txt`
2. Review and update test assertions
3. Monitor test execution time
4. Update documentation as needed
