import pytest
import subprocess
import time
import json
from typing import Dict, List
import kubernetes
from kubernetes import client, config
from kubernetes.client.rest import ApiException

class TestKubernetesDeployment:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup Kubernetes client and namespace"""
        config.load_kube_config()
        self.k8s_apps_v1 = client.AppsV1Api()
        self.k8s_core_v1 = client.CoreV1Api()
        self.namespace = "omega-grid-dev"
        
    def test_namespace_exists(self):
        """Test if the namespace exists"""
        try:
            self.k8s_core_v1.read_namespace(name=self.namespace)
        except ApiException as e:
            pytest.fail(f"Namespace {self.namespace} does not exist: {e}")

    def test_deployments_exist(self):
        """Test if all required deployments exist"""
        required_deployments = ["cli-portal", "nft-services"]
        try:
            deployments = self.k8s_apps_v1.list_namespaced_deployment(namespace=self.namespace)
            deployment_names = [deploy.metadata.name for deploy in deployments.items]
            
            for required in required_deployments:
                assert required in deployment_names, f"Deployment {required} not found"
        except ApiException as e:
            pytest.fail(f"Failed to list deployments: {e}")

    def test_services_exist(self):
        """Test if all required services exist"""
        required_services = ["cli-portal", "nft-services"]
        try:
            services = self.k8s_core_v1.list_namespaced_service(namespace=self.namespace)
            service_names = [svc.metadata.name for svc in services.items]
            
            for required in required_services:
                assert required in service_names, f"Service {required} not found"
        except ApiException as e:
            pytest.fail(f"Failed to list services: {e}")

    def test_deployments_are_ready(self):
        """Test if all deployments are ready"""
        try:
            deployments = self.k8s_apps_v1.list_namespaced_deployment(namespace=self.namespace)
            for deploy in deployments.items:
                assert deploy.status.ready_replicas == deploy.spec.replicas, \
                    f"Deployment {deploy.metadata.name} is not ready"
        except ApiException as e:
            pytest.fail(f"Failed to check deployment status: {e}")

    def test_pods_are_running(self):
        """Test if all pods are in Running state"""
        try:
            pods = self.k8s_core_v1.list_namespaced_pod(namespace=self.namespace)
            for pod in pods.items:
                assert pod.status.phase == "Running", \
                    f"Pod {pod.metadata.name} is not in Running state"
        except ApiException as e:
            pytest.fail(f"Failed to check pod status: {e}")

    def test_port_forwarding(self):
        """Test port forwarding for services"""
        # Test CLI Portal port forwarding
        cli_portal_cmd = ["kubectl", "port-forward", "service/cli-portal", "2222:22", "-n", self.namespace]
        try:
            cli_portal_process = subprocess.Popen(cli_portal_cmd)
            time.sleep(2)  # Wait for port forwarding to establish
            # Test connection to port 2222
            result = subprocess.run(["nc", "-z", "localhost", "2222"], capture_output=True)
            assert result.returncode == 0, "Failed to connect to CLI Portal port"
        finally:
            cli_portal_process.terminate()

        # Test NFT Services port forwarding
        nft_services_cmd = ["kubectl", "port-forward", "service/nft-services", "8080:8080", "-n", self.namespace]
        try:
            nft_process = subprocess.Popen(nft_services_cmd)
            time.sleep(2)  # Wait for port forwarding to establish
            # Test connection to port 8080
            result = subprocess.run(["nc", "-z", "localhost", "8080"], capture_output=True)
            assert result.returncode == 0, "Failed to connect to NFT Services port"
        finally:
            nft_process.terminate()

    def test_service_endpoints(self):
        """Test if services have endpoints"""
        try:
            endpoints = self.k8s_core_v1.list_namespaced_endpoints(namespace=self.namespace)
            endpoint_names = [ep.metadata.name for ep in endpoints.items]
            
            required_services = ["cli-portal", "nft-services"]
            for service in required_services:
                assert service in endpoint_names, f"Service {service} has no endpoints"
                
                # Check if endpoints have addresses
                endpoint = self.k8s_core_v1.read_namespaced_endpoints(name=service, namespace=self.namespace)
                assert len(endpoint.subsets) > 0, f"Service {service} has no subsets"
                assert len(endpoint.subsets[0].addresses) > 0, f"Service {service} has no addresses"
        except ApiException as e:
            pytest.fail(f"Failed to check service endpoints: {e}")

    def test_resource_limits(self):
        """Test if pods have resource limits set"""
        try:
            deployments = self.k8s_apps_v1.list_namespaced_deployment(namespace=self.namespace)
            for deploy in deployments.items:
                containers = deploy.spec.template.spec.containers
                for container in containers:
                    assert container.resources.limits is not None, \
                        f"Container {container.name} in deployment {deploy.metadata.name} has no resource limits"
                    assert container.resources.requests is not None, \
                        f"Container {container.name} in deployment {deploy.metadata.name} has no resource requests"
        except ApiException as e:
            pytest.fail(f"Failed to check resource limits: {e}")

    def test_health_checks(self):
        """Test if pods have health checks configured"""
        try:
            deployments = self.k8s_apps_v1.list_namespaced_deployment(namespace=self.namespace)
            for deploy in deployments.items:
                containers = deploy.spec.template.spec.containers
                for container in containers:
                    assert container.liveness_probe is not None, \
                        f"Container {container.name} in deployment {deploy.metadata.name} has no liveness probe"
                    assert container.readiness_probe is not None, \
                        f"Container {container.name} in deployment {deploy.metadata.name} has no readiness probe"
        except ApiException as e:
            pytest.fail(f"Failed to check health probes: {e}")

    def test_security_context(self):
        """Test if pods have security context configured"""
        try:
            deployments = self.k8s_apps_v1.list_namespaced_deployment(namespace=self.namespace)
            for deploy in deployments.items:
                pod_spec = deploy.spec.template.spec
                assert pod_spec.security_context is not None, \
                    f"Deployment {deploy.metadata.name} has no pod security context"
                assert pod_spec.security_context.run_as_non_root is True, \
                    f"Deployment {deploy.metadata.name} is not configured to run as non-root"
        except ApiException as e:
            pytest.fail(f"Failed to check security context: {e}")

    def test_config_maps_and_secrets(self):
        """Test if required ConfigMaps and Secrets exist"""
        try:
            config_maps = self.k8s_core_v1.list_namespaced_config_map(namespace=self.namespace)
            secrets = self.k8s_core_v1.list_namespaced_secret(namespace=self.namespace)
            
            # Add your required ConfigMaps and Secrets here
            required_config_maps = ["cli-portal-config", "nft-services-config"]
            required_secrets = ["cli-portal-secrets", "nft-services-secrets"]
            
            config_map_names = [cm.metadata.name for cm in config_maps.items]
            secret_names = [secret.metadata.name for secret in secrets.items]
            
            for required in required_config_maps:
                assert required in config_map_names, f"ConfigMap {required} not found"
            
            for required in required_secrets:
                assert required in secret_names, f"Secret {required} not found"
        except ApiException as e:
            pytest.fail(f"Failed to check ConfigMaps and Secrets: {e}")

    def test_network_policies(self):
        """Test if NetworkPolicies are configured"""
        try:
            networking_v1 = client.NetworkingV1Api()
            network_policies = networking_v1.list_namespaced_network_policy(namespace=self.namespace)
            assert len(network_policies.items) > 0, "No NetworkPolicies found"
        except ApiException as e:
            pytest.fail(f"Failed to check NetworkPolicies: {e}")

    def test_service_accounts(self):
        """Test if ServiceAccounts are properly configured"""
        try:
            service_accounts = self.k8s_core_v1.list_namespaced_service_account(namespace=self.namespace)
            required_service_accounts = ["cli-portal-sa", "nft-services-sa"]
            
            sa_names = [sa.metadata.name for sa in service_accounts.items]
            for required in required_service_accounts:
                assert required in sa_names, f"ServiceAccount {required} not found"
        except ApiException as e:
            pytest.fail(f"Failed to check ServiceAccounts: {e}")

    def test_rbac_rules(self):
        """Test if RBAC rules are properly configured"""
        try:
            rbac_v1 = client.RbacAuthorizationV1Api()
            roles = rbac_v1.list_namespaced_role(namespace=self.namespace)
            role_bindings = rbac_v1.list_namespaced_role_binding(namespace=self.namespace)
            
            required_roles = ["cli-portal-role", "nft-services-role"]
            required_role_bindings = ["cli-portal-rolebinding", "nft-services-rolebinding"]
            
            role_names = [role.metadata.name for role in roles.items]
            role_binding_names = [rb.metadata.name for rb in role_bindings.items]
            
            for required in required_roles:
                assert required in role_names, f"Role {required} not found"
            
            for required in required_role_bindings:
                assert required in role_binding_names, f"RoleBinding {required} not found"
        except ApiException as e:
            pytest.fail(f"Failed to check RBAC rules: {e}") 