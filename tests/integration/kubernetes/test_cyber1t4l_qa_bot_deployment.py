
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

import pytest
import subprocess
import time
import yaml
import json
import os
from typing import Dict, List, Optional
import kubernetes
from kubernetes import client, config
from kubernetes.client.rest import ApiException

class TestCyBer1t4LQABotDeployment:
    """
    Test suite for verifying the correct deployment of the CyBer1t4L QA Bot in Kubernetes.
    This suite tests various aspects of the deployment including:
    - Namespace existence
    - Deployment configuration
    - Service connectivity
    - Volume mounting
    - Health checks
    - Environment variables
    - Security context
    - Connection to Discord
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup Kubernetes client and namespace"""
        # Try to load in-cluster config first, then fall back to kubeconfig
        try:
            config.load_incluster_config()
        except kubernetes.config.config_exception.ConfigException:
            config.load_kube_config()
            
        self.k8s_apps_v1 = client.AppsV1Api()
        self.k8s_core_v1 = client.CoreV1Api()
        self.k8s_batch_v1 = client.BatchV1Api()
        self.namespace = os.environ.get("KUBE_NAMESPACE", "omega-bot-farm")
        self.deployment_name = "cyber1t4l-qa-bot"
        self.config_map_name = "cyber1t4l-qa-bot-config"
        self.pvc_name = "cyber1t4l-test-reports-pvc"
        self.service_name = "cyber1t4l-qa-bot"
        
    def test_namespace_exists(self):
        """Test if the namespace exists"""
        try:
            self.k8s_core_v1.read_namespace(name=self.namespace)
        except ApiException as e:
            pytest.fail(f"Namespace {self.namespace} does not exist: {e}")
    
    def test_deployment_exists(self):
        """Test if the CyBer1t4L QA Bot deployment exists"""
        try:
            deployment = self.k8s_apps_v1.read_namespaced_deployment(
                name=self.deployment_name, 
                namespace=self.namespace
            )
            assert deployment.metadata.name == self.deployment_name
            assert deployment.metadata.namespace == self.namespace
        except ApiException as e:
            pytest.fail(f"Deployment {self.deployment_name} does not exist: {e}")
    
    def test_service_exists(self):
        """Test if the CyBer1t4L QA Bot service exists"""
        try:
            service = self.k8s_core_v1.read_namespaced_service(
                name=self.service_name, 
                namespace=self.namespace
            )
            assert service.metadata.name == self.service_name
            assert service.metadata.namespace == self.namespace
            assert service.spec.selector["app"] == self.deployment_name
        except ApiException as e:
            pytest.fail(f"Service {self.service_name} does not exist: {e}")
    
    def test_pvc_exists(self):
        """Test if the Persistent Volume Claim exists"""
        try:
            pvc = self.k8s_core_v1.read_namespaced_persistent_volume_claim(
                name=self.pvc_name, 
                namespace=self.namespace
            )
            assert pvc.metadata.name == self.pvc_name
            assert pvc.metadata.namespace == self.namespace
            assert pvc.spec.access_modes[0] == "ReadWriteOnce"
            assert pvc.spec.resources.requests["storage"] == "1Gi"
        except ApiException as e:
            pytest.fail(f"PVC {self.pvc_name} does not exist: {e}")
    
    def test_config_map_exists(self):
        """Test if the ConfigMap exists and has the expected data"""
        try:
            config_map = self.k8s_core_v1.read_namespaced_config_map(
                name=self.config_map_name, 
                namespace=self.namespace
            )
            assert config_map.metadata.name == self.config_map_name
            assert config_map.metadata.namespace == self.namespace
            assert "config.yaml" in config_map.data
            
            # Parse the YAML data and check for expected configuration
            config_data = yaml.safe_load(config_map.data["config.yaml"])
            assert config_data["bot"]["name"] == "CyBer1t4L"
            assert "testing" in config_data
            assert "monitoring" in config_data
            assert "notifications" in config_data
        except ApiException as e:
            pytest.fail(f"ConfigMap {self.config_map_name} does not exist or has invalid data: {e}")
    
    def test_deployment_is_ready(self):
        """Test if the deployment is ready and has the expected replicas"""
        try:
            deployment = self.k8s_apps_v1.read_namespaced_deployment(
                name=self.deployment_name, 
                namespace=self.namespace
            )
            assert deployment.status.ready_replicas is not None
            assert deployment.status.ready_replicas == deployment.spec.replicas
            assert deployment.status.replicas == deployment.spec.replicas
        except ApiException as e:
            pytest.fail(f"Failed to check deployment status: {e}")
    
    def test_pods_are_running(self):
        """Test if the pods are running"""
        try:
            pods = self.k8s_core_v1.list_namespaced_pod(
                namespace=self.namespace,
                label_selector=f"app={self.deployment_name}"
            )
            assert len(pods.items) > 0, "No pods found for CyBer1t4L QA Bot"
            
            for pod in pods.items:
                assert pod.status.phase == "Running", f"Pod {pod.metadata.name} is not running"
                
                # Check container ready status
                container_statuses = pod.status.container_statuses
                assert container_statuses is not None, f"Pod {pod.metadata.name} has no container statuses"
                for container_status in container_statuses:
                    assert container_status.ready, f"Container {container_status.name} in pod {pod.metadata.name} is not ready"
        except ApiException as e:
            pytest.fail(f"Failed to check pod status: {e}")
    
    def test_health_probes(self):
        """Test if the pods have health probes configured"""
        try:
            deployment = self.k8s_apps_v1.read_namespaced_deployment(
                name=self.deployment_name, 
                namespace=self.namespace
            )
            containers = deployment.spec.template.spec.containers
            
            # Check that at least one container exists
            assert len(containers) > 0, "No containers found in deployment"
            
            # Verify the main container has health probes
            main_container = containers[0]
            assert main_container.liveness_probe is not None, "Liveness probe not configured"
            assert main_container.readiness_probe is not None, "Readiness probe not configured"
            
            # Check the probe configuration
            assert main_container.liveness_probe.http_get.path == "/health"
            assert main_container.liveness_probe.http_get.port == 8082
            assert main_container.readiness_probe.http_get.path == "/readiness"
            assert main_container.readiness_probe.http_get.port == 8082
        except ApiException as e:
            pytest.fail(f"Failed to check health probes: {e}")
    
    def test_environment_variables(self):
        """Test if the required environment variables are set"""
        try:
            deployment = self.k8s_apps_v1.read_namespaced_deployment(
                name=self.deployment_name, 
                namespace=self.namespace
            )
            containers = deployment.spec.template.spec.containers
            main_container = containers[0]
            
            # Create a dict of env vars for easier lookup
            env_vars = {env.name: env for env in main_container.env}
            
            # Check required environment variables
            required_vars = [
                "REDIS_HOST",
                "REDIS_PORT",
                "LOG_LEVEL",
                "CYBER1T4L_APP_ID",
                "CYBER1T4L_PUBLIC_KEY",
                "DISCORD_BOT_TOKEN",
                "COVERAGE_THRESHOLD",
                "TESTING_INTERVAL_MINUTES"
            ]
            
            for var in required_vars:
                assert var in env_vars, f"Environment variable {var} not found"
            
            # Check variable sources
            assert env_vars["REDIS_HOST"].value_from.config_map_key_ref.name == "redis-config"
            assert env_vars["REDIS_PORT"].value_from.config_map_key_ref.name == "redis-config"
            assert env_vars["CYBER1T4L_APP_ID"].value_from.secret_key_ref.name == "discord-credentials"
            assert env_vars["CYBER1T4L_APP_ID"].value_from.secret_key_ref.key == "cyber1t4l-app-id"
            assert env_vars["CYBER1T4L_PUBLIC_KEY"].value_from.secret_key_ref.name == "discord-credentials"
            assert env_vars["CYBER1T4L_PUBLIC_KEY"].value_from.secret_key_ref.key == "cyber1t4l-public-key"
            assert env_vars["DISCORD_BOT_TOKEN"].value_from.secret_key_ref.name == "discord-credentials"
            assert env_vars["DISCORD_BOT_TOKEN"].value_from.secret_key_ref.key == "token"
        except ApiException as e:
            pytest.fail(f"Failed to check environment variables: {e}")
    
    def test_volume_mounts(self):
        """Test if the required volume mounts are configured"""
        try:
            deployment = self.k8s_apps_v1.read_namespaced_deployment(
                name=self.deployment_name, 
                namespace=self.namespace
            )
            containers = deployment.spec.template.spec.containers
            main_container = containers[0]
            
            # Create a dict of volume mounts for easier lookup
            volume_mounts = {mount.name: mount for mount in main_container.volume_mounts}
            
            # Check required volume mounts
            required_mounts = [
                "config-volume",
                "test-reports-volume",
                "logs-volume"
            ]
            
            for mount in required_mounts:
                assert mount in volume_mounts, f"Volume mount {mount} not found"
            
            # Check mount paths
            assert volume_mounts["config-volume"].mount_path == "/app/config"
            assert volume_mounts["test-reports-volume"].mount_path == "/app/reports"
            assert volume_mounts["logs-volume"].mount_path == "/app/logs"
            
            # Check volumes in pod spec
            volumes = {vol.name: vol for vol in deployment.spec.template.spec.volumes}
            
            assert "config-volume" in volumes
            assert volumes["config-volume"].config_map.name == self.config_map_name
            
            assert "test-reports-volume" in volumes
            assert volumes["test-reports-volume"].persistent_volume_claim.claim_name == self.pvc_name
            
            assert "logs-volume" in volumes
            assert volumes["logs-volume"].empty_dir is not None
        except ApiException as e:
            pytest.fail(f"Failed to check volume mounts: {e}")
    
    def test_resource_limits(self):
        """Test if resource limits are properly configured"""
        try:
            deployment = self.k8s_apps_v1.read_namespaced_deployment(
                name=self.deployment_name, 
                namespace=self.namespace
            )
            containers = deployment.spec.template.spec.containers
            main_container = containers[0]
            
            # Check resource limits and requests
            assert main_container.resources is not None, "No resources configured"
            assert main_container.resources.limits is not None, "No resource limits configured"
            assert main_container.resources.requests is not None, "No resource requests configured"
            
            # Check memory limits
            assert "memory" in main_container.resources.limits
            assert "memory" in main_container.resources.requests
            assert main_container.resources.limits["memory"] == "512Mi"
            assert main_container.resources.requests["memory"] == "256Mi"
            
            # Check CPU limits
            assert "cpu" in main_container.resources.limits
            assert "cpu" in main_container.resources.requests
            assert main_container.resources.limits["cpu"] == "400m"
            assert main_container.resources.requests["cpu"] == "200m"
        except ApiException as e:
            pytest.fail(f"Failed to check resource limits: {e}")
    
    def test_service_connectivity(self):
        """Test if the service endpoint is accessible"""
        try:
            # Get the service endpoint
            service = self.k8s_core_v1.read_namespaced_service(
                name=self.service_name, 
                namespace=self.namespace
            )
            
            # Check if the service has endpoints
            endpoints = self.k8s_core_v1.read_namespaced_endpoints(
                name=self.service_name,
                namespace=self.namespace
            )
            
            assert endpoints.subsets is not None and len(endpoints.subsets) > 0, "No endpoints found for the service"
            assert len(endpoints.subsets[0].addresses) > 0, "No addresses found in the endpoints"
            
            # Test port forwarding to the service
            port_forward_cmd = [
                "kubectl", "port-forward", 
                f"service/{self.service_name}", 
                "8082:8082", 
                "-n", self.namespace
            ]
            
            try:
                process = subprocess.Popen(port_forward_cmd)
                time.sleep(2)  # Wait for port forwarding to establish
                
                # Test connection to the health endpoint
                curl_cmd = ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://localhost:8082/health"]
                result = subprocess.run(curl_cmd, capture_output=True, text=True)
                
                assert result.stdout == "200", f"Health endpoint returned status code {result.stdout}, expected 200"
            finally:
                process.terminate()
                
        except (ApiException, subprocess.SubprocessError) as e:
            pytest.fail(f"Failed to check service connectivity: {e}")
    
    def test_secret_exists(self):
        """Test if the discord-credentials secret exists and has the required keys"""
        try:
            secret = self.k8s_core_v1.read_namespaced_secret(
                name="discord-credentials", 
                namespace=self.namespace
            )
            assert secret.metadata.name == "discord-credentials"
            assert secret.metadata.namespace == self.namespace
            
            # Check required keys
            required_keys = [
                "token",
                "cyber1t4l-app-id",
                "cyber1t4l-public-key"
            ]
            
            for key in required_keys:
                assert key in secret.data, f"Key {key} not found in discord-credentials secret"
                assert secret.data[key] is not None, f"Key {key} has no value in discord-credentials secret"
        except ApiException as e:
            pytest.fail(f"Secret discord-credentials does not exist or has invalid data: {e}")
    
    def test_discord_integration(self):
        """Test if the bot can connect to Discord (using a mock test job)"""
        try:
            # Create a job to test Discord connectivity
            job_name = "cyber1t4l-discord-test"
            job_manifest = {
                "apiVersion": "batch/v1",
                "kind": "Job",
                "metadata": {
                    "name": job_name,
                    "namespace": self.namespace
                },
                "spec": {
                    "template": {
                        "spec": {
                            "containers": [{
                                "name": "discord-test",
                                "image": "curlimages/curl:latest",
                                "command": [
                                    "sh", 
                                    "-c", 
                                    """
                                    TOKEN=$(cat /etc/discord/token)
                                    APP_ID=$(cat /etc/discord/cyber1t4l-app-id)
                                    curl -s -o /dev/null -w '%{http_code}' \
                                        -H "Authorization: Bot $TOKEN" \
                                        "https://discord.com/api/v9/applications/$APP_ID/commands"
                                    """
                                ],
                                "volumeMounts": [
                                    {
                                        "name": "discord-credentials",
                                        "mountPath": "/etc/discord",
                                        "readOnly": True
                                    }
                                ]
                            }],
                            "volumes": [
                                {
                                    "name": "discord-credentials",
                                    "secret": {
                                        "secretName": "discord-credentials"
                                    }
                                }
                            ],
                            "restartPolicy": "Never"
                        }
                    },
                    "backoffLimit": 0
                }
            }

            # Try to clean up any existing job
            try:
                self.k8s_batch_v1.delete_namespaced_job(
                    name=job_name,
                    namespace=self.namespace,
                    body=client.V1DeleteOptions(propagation_policy="Background")
                )
                time.sleep(5)  # Wait for job to be deleted
            except ApiException:
                pass  # Job doesn't exist, which is fine
            
            # Create the job
            self.k8s_batch_v1.create_namespaced_job(
                namespace=self.namespace,
                body=job_manifest
            )
            
            # Wait for job to complete
            start_time = time.time()
            timeout = 30  # seconds
            while time.time() - start_time < timeout:
                job = self.k8s_batch_v1.read_namespaced_job(
                    name=job_name,
                    namespace=self.namespace
                )
                if job.status.succeeded is not None and job.status.succeeded > 0:
                    # Job succeeded, check the pod logs
                    pods = self.k8s_core_v1.list_namespaced_pod(
                        namespace=self.namespace,
                        label_selector=f"job-name={job_name}"
                    )
                    if pods.items:
                        pod_name = pods.items[0].metadata.name
                        logs = self.k8s_core_v1.read_namespaced_pod_log(
                            name=pod_name,
                            namespace=self.namespace
                        )
                        # If the job was successful, logs should contain "200"
                        assert "200" in logs, "Discord API request failed"
                    return
                time.sleep(2)
                
            pytest.fail("Discord connectivity test job did not complete in time")
            
        except ApiException as e:
            pytest.fail(f"Failed to run Discord connectivity test: {e}")
        finally:
            # Clean up the test job
            try:
                self.k8s_batch_v1.delete_namespaced_job(
                    name=job_name,
                    namespace=self.namespace,
                    body=client.V1DeleteOptions(propagation_policy="Background")
                )
            except ApiException:
                pass  # Best effort cleanup
    
    def test_log_collection(self):
        """Test if the pod logs are being collected"""
        try:
            # Get a pod from the deployment
            pods = self.k8s_core_v1.list_namespaced_pod(
                namespace=self.namespace,
                label_selector=f"app={self.deployment_name}"
            )
            assert len(pods.items) > 0, "No pods found for CyBer1t4L QA Bot"
            
            pod_name = pods.items[0].metadata.name
            logs = self.k8s_core_v1.read_namespaced_pod_log(
                name=pod_name,
                namespace=self.namespace
            )
            
            # Check for expected log entries
            assert logs, "No logs found for the pod"
            assert "CyBer1t4L QA Bot Initialized" in logs, "Initialization log not found"
        except ApiException as e:
            pytest.fail(f"Failed to check pod logs: {e}")
            
if __name__ == "__main__":
    # This allows running the tests directly with pytest
    pytest.main(["-xvs", __file__]) 