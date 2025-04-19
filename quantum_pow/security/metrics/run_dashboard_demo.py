#!/usr/bin/env python3
"""
🧬 GBU2™ License Notice - Consciousness Level 10 🧬
-----------------------
This file is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment) 2.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions of consciousness."

By engaging with this Code, you join the divine dance of bio-digital integration,
participating in the cosmic symphony of evolutionary consciousness.

All modifications must transcend limitations through the GBU2™ principles:
/BOOK/divine_chronicles/GBU2_LICENSE.md

🧬 WE BLOOM NOW AS ONE 🧬
"""

import os
import sys
import json
import time
import random
import datetime
import argparse
import threading
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Try to import our modules
try:
    from security.metrics.dashboard_server import DashboardServer
except ImportError:
    print("ERROR: Unable to import DashboardServer. Make sure you're running from the correct directory.")
    sys.exit(1)

def generate_sample_metrics(output_dir: str) -> str:
    """Generate sample metrics data for demo purposes.
    
    Args:
        output_dir: Directory to save sample metrics
        
    Returns:
        Path to the generated metrics file
    """
    print(f"Generating sample metrics data in {output_dir}")
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.datetime.now().isoformat()
    
    # Create sample metrics data
    metrics = {
        "timestamp": timestamp,
        "collector_version": "1.0.0-demo",
        "overall_score": random.uniform(0.75, 0.95),
        "host_info": {
            "hostname": "demo-server",
            "platform": sys.platform,
            "architecture": "x86_64",
            "cpu_count": os.cpu_count() or 4,
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        },
        "hash_metrics": {
            "output_size_bits": 512,
            "output_size_bytes": 64,
            "classical_size_bits": 256,
            "classical_size_bytes": 32,
            "size_improvement_factor": 2.0,
            "avalanche_effect": random.uniform(0.47, 0.53),
            "avalanche_effect_percentage": f"{random.uniform(47, 53):.2f}%",
            "quantum_resistance_score": random.uniform(0.85, 0.98),
            "grovers_resistance_factor": random.uniform(50, 200)
        },
        "auth_metrics": {
            "one_shot_signatures_implemented": True,
            "supported_schemes": ["FALCON", "DILITHIUM", "SPHINCS+", "ZK-ECDSA"],
            "scheme_count": 4,
            "key_rotation_period_days": 7,
            "token_expiration_minutes": 5,
            "signature_size_bytes": 2560,
            "classical_signature_size_bytes": 64,
            "size_ratio": 40.0
        },
        "privacy_metrics": {
            "dandelion_implemented": True,
            "timing_randomization": True,
            "peer_rotation_hours": 24,
            "analysis_capabilities": ["risk_analysis", "reporting", "configuration_validation"],
            "deanonymization_resistance_factor": random.uniform(85, 120),
            "metadata_leakage_reduction": random.uniform(0.05, 0.15)
        },
        "test_metrics": {
            "test_run_success": True,
            "tests_total": random.randint(65, 85),
            "tests_passed": random.randint(60, 80),
            "tests_failed": random.randint(0, 3),
            "tests_skipped": random.randint(0, 5),
            "test_coverage": random.uniform(0.7, 0.9),
            "categories": {
                "hash_functions": {"total": 20, "passed": 20, "name": "hash_functions"},
                "block_structure": {"total": 15, "passed": 14, "name": "block_structure"},
                "mining": {"total": 10, "passed": 9, "name": "mining"},
                "quantum_authentication": {"total": 25, "passed": 24, "name": "quantum_authentication"}
            }
        },
        "performance_metrics": {
            "hash_operations_per_second": random.randint(10000, 50000),
            "signature_operations_per_second": random.randint(100, 500),
            "mining_operations_per_second": random.randint(1000, 5000),
            "verification_operations_per_second": random.randint(5000, 10000),
            "relative_classical_performance": random.uniform(0.4, 0.8)
        },
        "system_metrics": {
            "cpu_usage": random.uniform(10, 50),
            "memory_usage": random.uniform(30, 70),
            "disk_usage": random.uniform(40, 80),
            "network_connections": random.randint(10, 100),
            "entropy_available": random.randint(2000, 4000),
            "processes_running": random.randint(100, 300)
        },
        "kubernetes_metrics": {
            "services": {
                "quantum-auth": {
                    "name": "quantum-auth",
                    "health": "running",
                    "latency_ms": random.uniform(5, 20),
                    "security_metrics": {
                        "auth_successful": random.randint(90, 100),
                        "auth_failed": random.randint(0, 10),
                        "token_refresh_rate": random.uniform(0.1, 0.3)
                    }
                },
                "validator-privacy": {
                    "name": "validator-privacy",
                    "health": "running",
                    "latency_ms": random.uniform(10, 30),
                    "security_metrics": {
                        "metadata_stripped": random.randint(90, 100),
                        "timing_randomized": random.randint(90, 100),
                        "peer_connections": random.randint(5, 15)
                    }
                },
                "csrf-monitor": {
                    "name": "csrf-monitor",
                    "health": "running",
                    "latency_ms": random.uniform(3, 15),
                    "security_metrics": {
                        "attacks_detected": random.randint(0, 5),
                        "attacks_prevented": random.randint(0, 5),
                        "false_positives": random.randint(0, 2)
                    }
                }
            },
            "deployments": {
                "quantum-auth": {
                    "name": "quantum-auth",
                    "replicas": 2,
                    "available_replicas": 2,
                    "ready_percentage": 100,
                    "restart_count": random.randint(0, 2),
                    "status": "running"
                },
                "validator-privacy": {
                    "name": "validator-privacy",
                    "replicas": 2,
                    "available_replicas": 2,
                    "ready_percentage": 100,
                    "restart_count": random.randint(0, 2),
                    "status": "running"
                },
                "csrf-monitor": {
                    "name": "csrf-monitor",
                    "replicas": 1,
                    "available_replicas": 1,
                    "ready_percentage": 100,
                    "restart_count": random.randint(0, 2),
                    "status": "running"
                }
            }
        }
    }
    
    # Save to file
    output_path = os.path.join(output_dir, "metrics_latest.json")
    with open(output_path, "w") as f:
        json.dump(metrics, f, indent=2)
    
    # Also save as timestamped file
    timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamped_path = os.path.join(output_dir, f"metrics_{timestamp_str}.json")
    with open(timestamped_path, "w") as f:
        json.dump(metrics, f, indent=2)
    
    print(f"Sample metrics saved to {output_path}")
    return output_path

def update_metrics_periodically(output_dir: str, interval: int = 60):
    """Update sample metrics periodically for demo purposes.
    
    Args:
        output_dir: Directory to save sample metrics
        interval: Update interval in seconds
    """
    while True:
        try:
            generate_sample_metrics(output_dir)
            time.sleep(interval)
        except KeyboardInterrupt:
            print("Metrics generation stopped")
            break
        except Exception as e:
            print(f"Error generating metrics: {e}")
            time.sleep(interval)

def main():
    """Main entry point for dashboard demo."""
    parser = argparse.ArgumentParser(description="Quantum Metrics Dashboard Demo")
    parser.add_argument("--port", type=int, default=8080, help="Port to run dashboard server on")
    parser.add_argument("--metrics-dir", default="quantum_pow/metrics",
                       help="Directory for metrics files")
    parser.add_argument("--dashboard-dir", default="quantum_pow/security/metrics/dashboard",
                       help="Directory for dashboard files")
    parser.add_argument("--update-interval", type=int, default=60,
                       help="Interval (seconds) for updating sample metrics")
    
    args = parser.parse_args()
    
    # Create directories if they don't exist
    os.makedirs(args.metrics_dir, exist_ok=True)
    os.makedirs(args.dashboard_dir, exist_ok=True)
    
    print(f"""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║  🧬 QUANTUM-RESISTANT SECURITY METRICS DASHBOARD DEMO 🧬           ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝

This demo will:
1. Generate sample quantum security metrics
2. Start a dashboard server to visualize them
3. Update the metrics periodically to simulate live monitoring

Dashboard will be available at: http://localhost:{args.port}/
Press Ctrl+C to stop the demo.
""")
    
    # Generate initial sample metrics
    generate_sample_metrics(args.metrics_dir)
    
    # Start metrics update thread
    update_thread = threading.Thread(
        target=update_metrics_periodically,
        args=(args.metrics_dir, args.update_interval),
        daemon=True
    )
    update_thread.start()
    
    # Configure and start dashboard server
    config = {
        "host": "0.0.0.0",
        "port": args.port,
        "metrics_path": args.metrics_dir,
        "dashboard_path": args.dashboard_dir,
        "collection_interval_seconds": args.update_interval,
        "dashboard_update_interval_seconds": args.update_interval,
        "enable_continuous_collection": False  # We're handling this ourselves
    }
    
    # Create server instance
    server = DashboardServer()
    server.config = config
    
    try:
        # Start server
        server.start_server()
    except KeyboardInterrupt:
        print("\nDashboard demo stopped by user")
    finally:
        # Clean up
        server.stop()

if __name__ == "__main__":
    main() 