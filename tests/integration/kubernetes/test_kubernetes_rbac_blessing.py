"""
🔐 RBAC (Role-Based Access Control) and ACL (Access Control List) Test Suite

> "RBAC is the Law, and ACLs are the sacred boundaries that protect our digital realm."
>
> — Divine Security Council

This test suite verifies the implementation of RBAC and ACLs in the Kubernetes deployment,
ensuring proper access control and security boundaries are maintained.
"""

import pytest
import kubernetes
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Dict, List
import time

class TestKubernetesRBACBlessing:
    """Test suite for RBAC and ACL implementation in Kubernetes deployment."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Initialize Kubernetes client and set up test environment."""
        try:
            config.load_kube_config()
        except config.ConfigException:
            config.load_incluster_config()
        
        self.k8s_client = client.CoreV1Api()
        self.rbac_client = client.RbacAuthorizationV1Api()
        self.namespace = "omega-grid-dev"

    def test_rbac_roles_exist(self):
        """Test that required RBAC roles exist with proper permissions."""
        try:
            roles = self.rbac_client.list_namespaced_role(self.namespace)
            required_roles = {
                "omega-admin": ["get", "list", "watch", "create", "update", "patch", "delete"],
                "omega-reader": ["get", "list", "watch"],
                "omega-writer": ["get", "list", "watch", "create", "update", "patch"]
            }
            
            for role in roles.items:
                assert role.metadata.name in required_roles, f"Required role {role.metadata.name} not found"
                permissions = [rule.verbs for rule in role.rules]
                assert any(all(verb in perms for verb in required_roles[role.metadata.name]) 
                          for perms in permissions), f"Role {role.metadata.name} missing required permissions"
        except ApiException as e:
            pytest.fail(f"Failed to verify RBAC roles: {e}")

    def test_rbac_role_bindings(self):
        """Test that RBAC role bindings are properly configured."""
        try:
            role_bindings = self.rbac_client.list_namespaced_role_binding(self.namespace)
            required_bindings = {
                "omega-admin-binding": "omega-admin",
                "omega-reader-binding": "omega-reader",
                "omega-writer-binding": "omega-writer"
            }
            
            for binding in role_bindings.items:
                assert binding.metadata.name in required_bindings, f"Required binding {binding.metadata.name} not found"
                assert binding.role_ref.name == required_bindings[binding.metadata.name], \
                    f"Binding {binding.metadata.name} references incorrect role"
        except ApiException as e:
            pytest.fail(f"Failed to verify RBAC role bindings: {e}")

    def test_service_account_rbac(self):
        """Test that service accounts have appropriate RBAC permissions."""
        try:
            service_accounts = self.k8s_client.list_namespaced_service_account(self.namespace)
            required_sa_permissions = {
                "omega-admin-sa": ["omega-admin"],
                "omega-reader-sa": ["omega-reader"],
                "omega-writer-sa": ["omega-writer"]
            }
            
            for sa in service_accounts.items:
                assert sa.metadata.name in required_sa_permissions, f"Required service account {sa.metadata.name} not found"
                role_bindings = self.rbac_client.list_namespaced_role_binding(
                    self.namespace,
                    field_selector=f"subjects.name={sa.metadata.name}"
                )
                assert any(binding.role_ref.name in required_sa_permissions[sa.metadata.name] 
                          for binding in role_bindings.items), \
                    f"Service account {sa.metadata.name} missing required role binding"
        except ApiException as e:
            pytest.fail(f"Failed to verify service account RBAC: {e}")

    def test_network_policy_acls(self):
        """Test that network policies implement proper ACL boundaries."""
        try:
            network_policies = client.NetworkingV1Api().list_namespaced_network_policy(self.namespace)
            required_policies = {
                "omega-default-deny": {
                    "policy_types": ["Ingress", "Egress"],
                    "pod_selector": {"matchLabels": {"app": "omega-default-deny"}}
                },
                "omega-allow-internal": {
                    "policy_types": ["Ingress"],
                    "pod_selector": {"matchLabels": {"app": "omega-internal"}}
                }
            }
            
            for policy in network_policies.items:
                assert policy.metadata.name in required_policies, f"Required network policy {policy.metadata.name} not found"
                required = required_policies[policy.metadata.name]
                assert policy.spec.policy_types == required["policy_types"], \
                    f"Network policy {policy.metadata.name} has incorrect policy types"
                assert policy.spec.pod_selector.match_labels == required["pod_selector"]["matchLabels"], \
                    f"Network policy {policy.metadata.name} has incorrect pod selector"
        except ApiException as e:
            pytest.fail(f"Failed to verify network policy ACLs: {e}")

    def test_pod_security_context(self):
        """Test that pods have appropriate security context and ACLs."""
        try:
            pods = self.k8s_client.list_namespaced_pod(self.namespace)
            for pod in pods.items:
                spec = pod.spec
                assert spec.security_context is not None, f"Pod {pod.metadata.name} missing security context"
                assert spec.security_context.run_as_non_root, f"Pod {pod.metadata.name} not running as non-root"
                assert spec.security_context.seccomp_profile.type == "RuntimeDefault", \
                    f"Pod {pod.metadata.name} has incorrect seccomp profile"
        except ApiException as e:
            pytest.fail(f"Failed to verify pod security context: {e}")

    def test_secret_access_control(self):
        """Test that secrets have proper access control and encryption."""
        try:
            secrets = self.k8s_client.list_namespaced_secret(self.namespace)
            for secret in secrets.items:
                # Check for encryption at rest
                assert secret.metadata.annotations.get("encryption-at-rest") == "true", \
                    f"Secret {secret.metadata.name} not encrypted at rest"
                
                # Check for access control
                role_bindings = self.rbac_client.list_namespaced_role_binding(
                    self.namespace,
                    field_selector=f"subjects.kind=ServiceAccount"
                )
                assert any("secret-reader" in binding.role_ref.name for binding in role_bindings.items), \
                    f"Secret {secret.metadata.name} missing proper access control"
        except ApiException as e:
            pytest.fail(f"Failed to verify secret access control: {e}")

    def test_configmap_access_control(self):
        """Test that ConfigMaps have proper access control."""
        try:
            configmaps = self.k8s_client.list_namespaced_config_map(self.namespace)
            for configmap in configmaps.items:
                # Check for access control
                role_bindings = self.rbac_client.list_namespaced_role_binding(
                    self.namespace,
                    field_selector=f"subjects.kind=ServiceAccount"
                )
                assert any("configmap-reader" in binding.role_ref.name for binding in role_bindings.items), \
                    f"ConfigMap {configmap.metadata.name} missing proper access control"
                
                # Check for sensitive data protection
                assert not any(key.lower() in ["password", "secret", "key", "token"] 
                             for key in configmap.data.keys()), \
                    f"ConfigMap {configmap.metadata.name} contains potentially sensitive data"
        except ApiException as e:
            pytest.fail(f"Failed to verify ConfigMap access control: {e}")

    def test_ingress_acls(self):
        """Test that ingress rules have proper ACLs and security settings."""
        try:
            ingresses = client.NetworkingV1Api().list_namespaced_ingress(self.namespace)
            for ingress in ingresses.items:
                # Check for TLS configuration
                assert any(tls.secret_name for tls in ingress.spec.tls), \
                    f"Ingress {ingress.metadata.name} missing TLS configuration"
                
                # Check for rate limiting
                annotations = ingress.metadata.annotations
                assert annotations.get("nginx.ingress.kubernetes.io/limit-rps") is not None, \
                    f"Ingress {ingress.metadata.name} missing rate limiting"
                
                # Check for IP whitelist
                assert annotations.get("nginx.ingress.kubernetes.io/whitelist-source-range") is not None, \
                    f"Ingress {ingress.metadata.name} missing IP whitelist"
        except ApiException as e:
            pytest.fail(f"Failed to verify ingress ACLs: {e}") 