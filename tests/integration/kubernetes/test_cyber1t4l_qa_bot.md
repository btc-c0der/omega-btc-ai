
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


# CyBer1t4L QA Bot Kubernetes Tests

This test suite verifies the proper deployment and functionality of the CyBer1t4L QA Bot in a Kubernetes environment.

## Overview

The tests verify various aspects of the Kubernetes deployment:

- Deployment, Service, and ConfigMap existence
- PersistentVolumeClaim setup
- Environment variables configuration
- Volume mounts
- Resource limits
- Health probes
- Discord connectivity
- Service endpoints
- Log collection

## Prerequisites

1. A Kubernetes cluster with the CyBer1t4L QA Bot deployed
2. `kubectl` CLI tool installed and configured
3. Python 3.8+ with pip

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Configuration

The tests support the following environment variables:

- `KUBE_NAMESPACE` - The namespace where the CyBer1t4L QA Bot is deployed (default: "omega-bot-farm")
- `KUBECONFIG` - Path to your kubeconfig file (optional, uses default if not specified)

## Running the Tests

### All Tests

Run all tests with:

```bash
pytest -xvs test_cyber1t4l_qa_bot_deployment.py
```

### Individual Tests

Run specific tests with:

```bash
pytest -xvs test_cyber1t4l_qa_bot_deployment.py::TestCyBer1t4LQABotDeployment::test_deployment_exists
```

### Testing a Different Namespace

To test in a different namespace:

```bash
KUBE_NAMESPACE=my-custom-namespace pytest -xvs test_cyber1t4l_qa_bot_deployment.py
```

## Test Categories

### Basic Existence Tests

- `test_namespace_exists`
- `test_deployment_exists`
- `test_service_exists`
- `test_pvc_exists`
- `test_config_map_exists`
- `test_secret_exists`

### Configuration Tests

- `test_environment_variables`
- `test_volume_mounts`
- `test_health_probes`
- `test_resource_limits`

### Runtime Tests

- `test_deployment_is_ready`
- `test_pods_are_running`
- `test_service_connectivity`
- `test_log_collection`

### Integration Tests

- `test_discord_integration`

## Troubleshooting

### "Unable to connect to Kubernetes API server"

Ensure your kubeconfig is correctly set up and the API server is accessible:

```bash
kubectl cluster-info
```

### Test Pod Failures

To check the logs of failing pods:

```bash
kubectl logs -n omega-bot-farm -l app=cyber1t4l-qa-bot
```

### Discord Integration Test Failure

If the Discord integration test fails, check if:

1. The secret contains valid credentials
2. The pod has network access to Discord API
3. The token and app ID are correctly configured

## Contributing

When adding new tests:

1. Add appropriate assertions to verify expected behavior
2. Include proper error handling to provide clear failure messages
3. Add cleanup code to remove test resources after tests
4. Update this documentation to include the new test

## Running in CI/CD

This test suite is designed to run in CI/CD pipelines. Example GitHub Actions workflow:

```yaml
name: Kubernetes Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  k8s-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r tests/integration/kubernetes/requirements.txt
      - name: Set up kubeconfig
        run: |
          echo "${{ secrets.KUBECONFIG }}" > ~/.kube/config
          chmod 600 ~/.kube/config
      - name: Run tests
        run: |
          cd tests/integration/kubernetes
          pytest -xvs test_cyber1t4l_qa_bot_deployment.py
