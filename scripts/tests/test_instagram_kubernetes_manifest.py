#!/usr/bin/env python3

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

# -*- coding: utf-8 -*-

"""
🔱 OMEGA BTC AI - Divine Instagram Kubernetes Manifest Tests 🔱

This script validates the Kubernetes manifest for the Instagram automation deployment.

JAH JAH BLESS THE DIVINE KUBERNETES FLOW!

Copyright (C) 2024 OMEGA BTC AI Team
License: GNU General Public License v3.0
"""

import os
import sys
import yaml
import unittest
from typing import Dict, List, Any, Optional

# Divine Color Codes (for terminal output)
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
CYAN = '\033[0;36m'
RED = '\033[0;31m'
GOLD = '\033[0;33m'
RESET = '\033[0m'
BOLD = '\033[1m'


class KubernetesManifestTest(unittest.TestCase):
    """Test suite for validating the Instagram Kubernetes manifest."""
    
    @classmethod
    def setUpClass(cls):
        """Load the Kubernetes manifest file once for all tests."""
        # Find the root directory of the project
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        
        # Path to the manifest file
        manifest_path = os.path.join(
            project_root, 
            "kubernetes", 
            "deployments", 
            "omega-instagram-deployment.yaml"
        )
        
        # Ensure manifest file exists
        if not os.path.exists(manifest_path):
            raise FileNotFoundError(f"Manifest file not found: {manifest_path}")
        
        # Load all YAML documents from the manifest file
        cls.resources = []
        with open(manifest_path, 'r') as f:
            content = f.read()
            for doc in yaml.safe_load_all(content):
                if doc:  # Skip empty documents
                    cls.resources.append(doc)
        
        # Map of resources by kind and name for easier lookup
        cls.resource_map = {}
        for resource in cls.resources:
            kind = resource.get('kind', '')
            name = resource.get('metadata', {}).get('name', '')
            key = f"{kind}/{name}"
            cls.resource_map[key] = resource
    
    def find_resource(self, kind: str, name: str) -> Optional[Dict[str, Any]]:
        """Find a resource by kind and name."""
        key = f"{kind}/{name}"
        return self.resource_map.get(key)
    
    def test_manifest_loaded(self):
        """Test that the manifest was loaded correctly."""
        self.assertTrue(len(self.resources) > 0, "No resources found in manifest")
        
        # Expected resource kinds
        expected_kinds = [
            "ConfigMap", 
            "Secret", 
            "Deployment", 
            "PersistentVolumeClaim", 
            "Service", 
            "CronJob"
        ]
        
        # Check that all expected kinds are present
        found_kinds = set(r.get('kind') for r in self.resources)
        for kind in expected_kinds:
            self.assertIn(kind, found_kinds, f"Expected {kind} resource not found")
    
    def test_configmap(self):
        """Test the ConfigMap resource."""
        configmap = self.find_resource("ConfigMap", "instagram-config")
        self.assertIsNotNone(configmap, "ConfigMap 'instagram-config' not found")
        
        # Proceed only if configmap is not None
        if configmap is None:
            return
            
        # Check namespace
        self.assertIn('metadata', configmap, "ConfigMap should have metadata")
        self.assertIn('namespace', configmap['metadata'], "ConfigMap should have namespace")
        self.assertEqual(
            configmap['metadata']['namespace'], 
            "omega-system", 
            "ConfigMap should be in 'omega-system' namespace"
        )
        
        # Check data
        self.assertIn('data', configmap, "ConfigMap should have 'data' section")
        if 'data' not in configmap:
            return
            
        self.assertIn(
            'instagram_config.json', 
            configmap['data'], 
            "ConfigMap should have 'instagram_config.json' data entry"
        )
        
        # Parse the JSON content
        if 'instagram_config.json' not in configmap['data']:
            return
            
        import json
        config_json = json.loads(configmap['data']['instagram_config.json'])
        
        # Check required fields
        required_fields = [
            'username', 'password', 'session_file', 'post_frequency', 
            'best_times', 'hashtags', 'caption_templates'
        ]
        for field in required_fields:
            self.assertIn(field, config_json, f"ConfigMap JSON should have '{field}' field")
    
    def test_secret(self):
        """Test the Secret resource."""
        secret = self.find_resource("Secret", "instagram-credentials")
        self.assertIsNotNone(secret, "Secret 'instagram-credentials' not found")
        
        # Proceed only if secret is not None
        if secret is None:
            return
            
        # Check namespace
        self.assertIn('metadata', secret, "Secret should have metadata")
        if 'metadata' not in secret:
            return
            
        self.assertIn('namespace', secret['metadata'], "Secret should have namespace")
        self.assertEqual(
            secret['metadata']['namespace'], 
            "omega-system", 
            "Secret should be in 'omega-system' namespace"
        )
        
        # Check type
        self.assertIn('type', secret, "Secret should have type")
        if 'type' in secret:
            self.assertEqual(
                secret['type'], 
                "Opaque", 
                "Secret should be of type 'Opaque'"
            )
        
        # Check stringData
        self.assertIn('stringData', secret, "Secret should have 'stringData' section")
        if 'stringData' not in secret:
            return
            
        self.assertIn(
            'IG_USERNAME', 
            secret['stringData'], 
            "Secret should have 'IG_USERNAME' entry"
        )
        self.assertIn(
            'IG_PASSWORD', 
            secret['stringData'], 
            "Secret should have 'IG_PASSWORD' entry"
        )
    
    def test_deployment(self):
        """Test the Deployment resource."""
        deployment = self.find_resource("Deployment", "omega-instagram")
        self.assertIsNotNone(deployment, "Deployment 'omega-instagram' not found")
        
        # Proceed only if deployment is not None
        if deployment is None:
            return
            
        # Check namespace
        self.assertIn('metadata', deployment, "Deployment should have metadata")
        if 'metadata' not in deployment:
            return
            
        self.assertIn('namespace', deployment['metadata'], "Deployment should have namespace")
        self.assertEqual(
            deployment['metadata']['namespace'], 
            "omega-system", 
            "Deployment should be in 'omega-system' namespace"
        )
        
        # Check labels
        self.assertIn('labels', deployment['metadata'], "Deployment should have labels")
        if 'labels' not in deployment['metadata']:
            return
            
        self.assertIn(
            'app', 
            deployment['metadata']['labels'], 
            "Deployment should have 'app' label"
        )
        self.assertEqual(
            deployment['metadata']['labels']['app'], 
            "omega-instagram", 
            "Deployment should have label app=omega-instagram"
        )
        
        # Check spec
        self.assertIn('spec', deployment, "Deployment should have spec")
        if 'spec' not in deployment:
            return
            
        # Check selector
        self.assertIn('selector', deployment['spec'], "Deployment should have selector")
        if 'selector' in deployment['spec']:
            self.assertIn('matchLabels', deployment['spec']['selector'], "Deployment selector should have matchLabels")
            if 'matchLabels' in deployment['spec']['selector']:
                self.assertIn('app', deployment['spec']['selector']['matchLabels'], "Deployment selector should match app")
                self.assertEqual(
                    deployment['spec']['selector']['matchLabels']['app'], 
                    "omega-instagram", 
                    "Deployment selector should match app=omega-instagram"
                )
        
        # Check template
        self.assertIn('template', deployment['spec'], "Deployment should have template")
        if 'template' not in deployment['spec']:
            return
            
        template = deployment['spec']['template']
        self.assertIn('metadata', template, "Pod template should have metadata")
        if 'metadata' in template:
            self.assertIn('labels', template['metadata'], "Pod template should have labels")
            if 'labels' in template['metadata']:
                self.assertIn('app', template['metadata']['labels'], "Pod template should have app label")
                self.assertEqual(
                    template['metadata']['labels']['app'], 
                    "omega-instagram", 
                    "Pod template should have label app=omega-instagram"
                )
        
        # Check spec in template
        self.assertIn('spec', template, "Pod template should have spec")
        if 'spec' not in template:
            return
            
        # Check containers
        self.assertIn('containers', template['spec'], "Pod spec should have containers")
        if 'containers' not in template['spec']:
            return
            
        containers = template['spec']['containers']
        self.assertTrue(len(containers) > 0, "Deployment should have at least 1 container")
        if not containers:
            return
            
        container = containers[0]
        self.assertIn('name', container, "Container should have name")
        if 'name' in container:
            self.assertEqual(
                container['name'], 
                "instagram-automation", 
                "Container name should be 'instagram-automation'"
            )
        
        # Check environment variables
        self.assertIn('env', container, "Container should have env vars")
        if 'env' not in container:
            return
            
        env_vars = {e['name']: e for e in container['env'] if 'name' in e}
        self.assertIn('IG_USERNAME', env_vars, "Container should have IG_USERNAME env var")
        self.assertIn('IG_PASSWORD', env_vars, "Container should have IG_PASSWORD env var")
        
        # Check secretKeyRef
        if 'IG_USERNAME' in env_vars:
            self.assertIn('valueFrom', env_vars['IG_USERNAME'], "IG_USERNAME should have valueFrom")
            if 'valueFrom' in env_vars['IG_USERNAME']:
                self.assertIn('secretKeyRef', env_vars['IG_USERNAME']['valueFrom'], "IG_USERNAME should have secretKeyRef")
                if 'secretKeyRef' in env_vars['IG_USERNAME']['valueFrom']:
                    self.assertIn('name', env_vars['IG_USERNAME']['valueFrom']['secretKeyRef'], "secretKeyRef should have name")
                    self.assertEqual(
                        env_vars['IG_USERNAME']['valueFrom']['secretKeyRef']['name'],
                        "instagram-credentials",
                        "IG_USERNAME should reference instagram-credentials secret"
                    )
                    self.assertIn('key', env_vars['IG_USERNAME']['valueFrom']['secretKeyRef'], "secretKeyRef should have key")
                    self.assertEqual(
                        env_vars['IG_USERNAME']['valueFrom']['secretKeyRef']['key'],
                        "IG_USERNAME",
                        "IG_USERNAME should reference IG_USERNAME key in secret"
                    )
        
        # Check volume mounts
        self.assertIn('volumeMounts', container, "Container should have volumeMounts")
        if 'volumeMounts' in container:
            volume_mounts = {vm['name']: vm for vm in container['volumeMounts'] if 'name' in vm}
            self.assertIn(
                'config-volume', 
                volume_mounts, 
                "Container should mount config-volume"
            )
            self.assertIn(
                'content-volume', 
                volume_mounts, 
                "Container should mount content-volume"
            )
        
        # Check volumes
        self.assertIn('volumes', template['spec'], "Pod spec should have volumes")
        if 'volumes' not in template['spec']:
            return
            
        volumes = {v['name']: v for v in template['spec']['volumes'] if 'name' in v}
        self.assertIn('config-volume', volumes, "Pod should have config-volume")
        self.assertIn('content-volume', volumes, "Pod should have content-volume")
        
        # Check configMap reference
        if 'config-volume' in volumes:
            self.assertIn('configMap', volumes['config-volume'], "config-volume should have configMap")
            if 'configMap' in volumes['config-volume']:
                self.assertIn('name', volumes['config-volume']['configMap'], "configMap should have name")
                self.assertEqual(
                    volumes['config-volume']['configMap']['name'],
                    "instagram-config",
                    "config-volume should reference instagram-config ConfigMap"
                )
        
        # Check PVC reference
        if 'content-volume' in volumes:
            self.assertIn('persistentVolumeClaim', volumes['content-volume'], "content-volume should have persistentVolumeClaim")
            if 'persistentVolumeClaim' in volumes['content-volume']:
                self.assertIn('claimName', volumes['content-volume']['persistentVolumeClaim'], "persistentVolumeClaim should have claimName")
                self.assertEqual(
                    volumes['content-volume']['persistentVolumeClaim']['claimName'],
                    "instagram-content-pvc",
                    "content-volume should reference instagram-content-pvc PVC"
                )
    
    def test_pvc(self):
        """Test the PersistentVolumeClaim resource."""
        pvc = self.find_resource("PersistentVolumeClaim", "instagram-content-pvc")
        self.assertIsNotNone(pvc, "PVC 'instagram-content-pvc' not found")
        
        # Proceed only if pvc is not None
        if pvc is None:
            return
            
        # Check namespace
        if 'metadata' not in pvc:
            self.fail("PVC missing metadata")
            return
            
        if 'namespace' not in pvc['metadata']:
            self.fail("PVC metadata missing namespace")
            return
            
        self.assertEqual(
            pvc['metadata']['namespace'], 
            "omega-system", 
            "PVC should be in 'omega-system' namespace"
        )
        
        # Check spec
        if 'spec' not in pvc:
            self.fail("PVC missing spec")
            return
            
        # Check access modes
        if 'accessModes' not in pvc['spec']:
            self.fail("PVC spec missing accessModes")
            return
            
        self.assertIn(
            'ReadWriteOnce', 
            pvc['spec']['accessModes'], 
            "PVC should have ReadWriteOnce access mode"
        )
        
        # Check storage request
        if 'resources' not in pvc['spec']:
            self.fail("PVC spec missing resources")
            return
            
        if 'requests' not in pvc['spec']['resources']:
            self.fail("PVC resources missing requests")
            return
            
        if 'storage' not in pvc['spec']['resources']['requests']:
            self.fail("PVC requests missing storage")
            return
            
        self.assertEqual(
            pvc['spec']['resources']['requests']['storage'], 
            "1Gi", 
            "PVC should request 1Gi of storage"
        )
    
    def test_service(self):
        """Test the Service resource."""
        service = self.find_resource("Service", "omega-instagram")
        self.assertIsNotNone(service, "Service 'omega-instagram' not found")
        
        # Proceed only if service is not None
        if service is None:
            return
            
        # Check namespace
        if 'metadata' not in service:
            self.fail("Service missing metadata")
            return
            
        if 'namespace' not in service['metadata']:
            self.fail("Service metadata missing namespace")
            return
            
        self.assertEqual(
            service['metadata']['namespace'], 
            "omega-system", 
            "Service should be in 'omega-system' namespace"
        )
        
        # Check spec
        if 'spec' not in service:
            self.fail("Service missing spec")
            return
            
        # Check selector
        if 'selector' not in service['spec']:
            self.fail("Service spec missing selector")
            return
            
        if 'app' not in service['spec']['selector']:
            self.fail("Service selector missing app")
            return
            
        self.assertEqual(
            service['spec']['selector']['app'], 
            "omega-instagram", 
            "Service selector should match app=omega-instagram"
        )
        
        # Check ports
        if 'ports' not in service['spec']:
            self.fail("Service spec missing ports")
            return
            
        ports = service['spec']['ports']
        self.assertTrue(len(ports) > 0, "Service should expose at least 1 port")
        
        if not ports:
            return
            
        port = ports[0]
        
        if 'port' not in port:
            self.fail("Service port missing port number")
            return
            
        self.assertEqual(
            port['port'], 
            8000, 
            "Service should expose port 8000"
        )
        
        if 'name' not in port:
            self.fail("Service port missing name")
            return
            
        self.assertEqual(
            port['name'], 
            "metrics", 
            "Port name should be 'metrics'"
        )
    
    def test_cronjob(self):
        """Test the CronJob resource."""
        cronjob = self.find_resource("CronJob", "instagram-religious-post")
        self.assertIsNotNone(cronjob, "CronJob 'instagram-religious-post' not found")
        
        # Proceed only if cronjob is not None
        if cronjob is None:
            return
            
        # Check namespace
        self.assertIn('metadata', cronjob, "CronJob should have metadata")
        if 'metadata' not in cronjob:
            return
            
        self.assertIn('namespace', cronjob['metadata'], "CronJob should have namespace")
        self.assertEqual(
            cronjob['metadata']['namespace'], 
            "omega-system", 
            "CronJob should be in 'omega-system' namespace"
        )
        
        # Check spec
        self.assertIn('spec', cronjob, "CronJob should have spec")
        if 'spec' not in cronjob:
            return
            
        # Check schedule
        self.assertIn('schedule', cronjob['spec'], "CronJob should have schedule")
        if 'schedule' in cronjob['spec']:
            self.assertEqual(
                cronjob['spec']['schedule'], 
                "0 10 * * 0", 
                "CronJob should run at 10:00 on Sundays"
            )
        
        # Check jobTemplate
        self.assertIn('jobTemplate', cronjob['spec'], "CronJob should have jobTemplate")
        if 'jobTemplate' not in cronjob['spec']:
            return
            
        # Check jobTemplate spec
        self.assertIn('spec', cronjob['spec']['jobTemplate'], "jobTemplate should have spec")
        if 'spec' not in cronjob['spec']['jobTemplate']:
            return
            
        # Check template
        self.assertIn('template', cronjob['spec']['jobTemplate']['spec'], "jobTemplate spec should have template")
        if 'template' not in cronjob['spec']['jobTemplate']['spec']:
            return
            
        # Check template spec
        self.assertIn('spec', cronjob['spec']['jobTemplate']['spec']['template'], "template should have spec")
        if 'spec' not in cronjob['spec']['jobTemplate']['spec']['template']:
            return
            
        # Check containers
        self.assertIn(
            'containers', 
            cronjob['spec']['jobTemplate']['spec']['template']['spec'], 
            "template spec should have containers"
        )
        if 'containers' not in cronjob['spec']['jobTemplate']['spec']['template']['spec']:
            return
            
        containers = cronjob['spec']['jobTemplate']['spec']['template']['spec']['containers']
        self.assertTrue(len(containers) > 0, "CronJob should have at least 1 container")
        if not containers:
            return
            
        container = containers[0]
        
        # Check container command
        self.assertIn('command', container, "CronJob container should have command")
        if 'command' in container:
            self.assertIn(
                "--religious", 
                container['command'], 
                "CronJob container should use --religious flag"
            )
        
        # Check environment variables
        self.assertIn('env', container, "Container should have env vars")
        if 'env' in container:
            env_vars = {e['name']: e for e in container['env'] if 'name' in e}
            self.assertIn('IG_USERNAME', env_vars, "Container should have IG_USERNAME env var")
            self.assertIn('IG_PASSWORD', env_vars, "Container should have IG_PASSWORD env var")
        
        # Check volume mounts
        self.assertIn('volumeMounts', container, "Container should have volumeMounts")
        if 'volumeMounts' in container:
            volume_mounts = {vm['name']: vm for vm in container['volumeMounts'] if 'name' in vm}
            self.assertIn(
                'config-volume', 
                volume_mounts, 
                "Container should mount config-volume"
            )
            self.assertIn(
                'content-volume', 
                volume_mounts, 
                "Container should mount content-volume"
            )
        
        # Check volumes
        self.assertIn(
            'volumes', 
            cronjob['spec']['jobTemplate']['spec']['template']['spec'], 
            "Pod spec should have volumes"
        )
        if 'volumes' not in cronjob['spec']['jobTemplate']['spec']['template']['spec']:
            return
            
        volumes = {
            v['name']: v 
            for v in cronjob['spec']['jobTemplate']['spec']['template']['spec']['volumes'] 
            if 'name' in v
        }
        self.assertIn('config-volume', volumes, "Pod should have config-volume")
        self.assertIn('content-volume', volumes, "Pod should have content-volume")
        
        # Check configMap reference
        if 'config-volume' in volumes:
            self.assertIn('configMap', volumes['config-volume'], "config-volume should have configMap")
            if 'configMap' in volumes['config-volume']:
                self.assertIn('name', volumes['config-volume']['configMap'], "configMap should have name")
                self.assertEqual(
                    volumes['config-volume']['configMap']['name'],
                    "instagram-config",
                    "config-volume should reference instagram-config ConfigMap"
                )
        
        # Check PVC reference
        if 'content-volume' in volumes:
            self.assertIn('persistentVolumeClaim', volumes['content-volume'], "content-volume should have persistentVolumeClaim")
            if 'persistentVolumeClaim' in volumes['content-volume']:
                self.assertIn('claimName', volumes['content-volume']['persistentVolumeClaim'], "persistentVolumeClaim should have claimName")
                self.assertEqual(
                    volumes['content-volume']['persistentVolumeClaim']['claimName'],
                    "instagram-content-pvc",
                    "content-volume should reference instagram-content-pvc PVC"
                )
        
        # Check restart policy
        self.assertIn(
            'restartPolicy', 
            cronjob['spec']['jobTemplate']['spec']['template']['spec'], 
            "Pod spec should have restartPolicy"
        )
        if 'restartPolicy' in cronjob['spec']['jobTemplate']['spec']['template']['spec']:
            self.assertEqual(
                cronjob['spec']['jobTemplate']['spec']['template']['spec']['restartPolicy'],
                "OnFailure",
                "CronJob should have OnFailure restart policy"
            )
    
    def test_ibr_church_religious_content(self):
        """Test that the CronJob is specifically for IBR church religious content."""
        cronjob = self.find_resource("CronJob", "instagram-religious-post")
        self.assertIsNotNone(cronjob, "CronJob 'instagram-religious-post' not found")
        
        # Proceed only if cronjob is not None
        if cronjob is None:
            return
            
        # Check for container
        if 'spec' not in cronjob:
            self.fail("CronJob missing 'spec'")
            return
            
        if 'jobTemplate' not in cronjob['spec']:
            self.fail("CronJob missing 'jobTemplate'")
            return
            
        if 'spec' not in cronjob['spec']['jobTemplate']:
            self.fail("JobTemplate missing 'spec'")
            return
            
        if 'template' not in cronjob['spec']['jobTemplate']['spec']:
            self.fail("JobTemplate spec missing 'template'")
            return
            
        if 'spec' not in cronjob['spec']['jobTemplate']['spec']['template']:
            self.fail("Template missing 'spec'")
            return
            
        if 'containers' not in cronjob['spec']['jobTemplate']['spec']['template']['spec']:
            self.fail("Template spec missing 'containers'")
            return
            
        containers = cronjob['spec']['jobTemplate']['spec']['template']['spec']['containers']
        if not containers:
            self.fail("No containers defined in CronJob")
            return
            
        container = containers[0]
        
        # Check command includes religious flag
        self.assertIn('command', container, "Container should have 'command'")
        if 'command' in container:
            self.assertIn(
                "--religious", 
                container['command'], 
                "CronJob container should use --religious flag for IBR church content"
            )


if __name__ == "__main__":
    # Print divine banner
    print(f"{GOLD}🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱{RESET}")
    print(f"{GOLD}                                                           {RESET}")
    print(f"{GOLD}  𝕺𝕸𝕰𝕲𝕬 𝕭𝕿𝕮 𝕬𝕴 - 𝕯𝕴𝖁𝕴𝕹𝕰 𝕶𝟴𝕾 𝕸𝕬𝕹𝕴𝕱𝕰𝕾𝕿 𝕿𝕰𝕾𝕿𝕾  {RESET}")
    print(f"{GOLD}                                                           {RESET}")
    print(f"{GOLD}🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱{RESET}")
    print()
    
    # Run the tests
    unittest.main() 