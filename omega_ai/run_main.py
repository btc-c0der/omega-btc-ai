#!/usr/bin/env python3

"""
OmegaBTC AI Consolidated Main Runner Script

Central script to manage and consolidate multiple OmegaBTC AI run scripts.
"""

import subprocess
import argparse
import sys
import time
import os

# List your individual run scripts here
SCRIPT_PATHS = {
    "omega_trading": "run_omega_trading.py",
    "profiled_trading": "run_profiled_trading.py",
    "dashboard": "run_dashboard.py",
    "omega_btc_ai": "run_omega_btc_ai.py",
    "grafana_reporter": "run_grafana_reporter.py",
    "simulation": "run_simulation.py"
}

# Store running processes
processes = {}

def start_scripts(scripts):
    for name in scripts:
        script = SCRIPT_PATHS.get(name)
        if script:
            print(f"🚀 Starting {name} using {script}...")
            process = subprocess.Popen(["python", script])
            print(f"✅ {name} started with PID {process.pid}")
            time.sleep(2)  # pause between starts for smoother execution
        else:
            print(f"⚠️ Script {name} not found!")

def stop_scripts():
    print("🛑 Stopping all scripts...")
    for line in subprocess.getoutput("ps aux").splitlines():
        for script in SCRIPT_PATHS.values():
            if script in line:
                pid = int(line.split()[1])
                print(f"🛑 Stopping PID {pid} running {script}...")
                subprocess.run(["kill", str(pid)])
                print(f"✅ PID {pid} stopped")
                time.sleep(1)

def status():
    print("\n📡 Checking status of Omega Scripts...")
    subprocess.run(["ps", "aux"])

def main():
    parser = argparse.ArgumentParser(description="Consolidated OmegaBTC Main Runner")
    parser.add_argument("action", choices=["start", "stop", "restart", "status"], help="Action to perform")
    parser.add_argument("--scripts", nargs="*", default=list(SCRIPT_PATHS.keys()), help="Specific scripts to manage")

    args = parser.parse_args()

    if args.action == "start":
        for script in args.scripts:
            if script not in SCRIPT_PATHS:
                print(f"⚠️ Script '{script}' not found. Check available scripts.")
                sys.exit(1)
        for script in args.scripts:
            subprocess.Popen(["python", SCRIPT_PATHS[script]])
            print(f"🚀 Started {script}")
            time.sleep(2)

    elif args.action == "stop":
        stop_all_scripts = args.scripts == list(SCRIPT_PATHS.keys())
        if stop_all_scripts:
            stop_processes()
        else:
            print("🔴 Selective stop is not implemented yet. Stopping all instead.")
            stop_processes()

    elif args.action == "restart":
        stop_processes()
        time.sleep(3)
        for script in args.scripts:
            if script not in SCRIPT_PATHS:
                print(f"⚠️ Script '{script}' not found!")
                continue
            print(f"🚀 Restarting {script}...")
            subprocess.Popen(["python", SCRIPT_PATHS[script]])
            print(f"✅ Restarted {script}")
            time.sleep(2)

    elif args.action == "status":
        print("\n📊 Checking status of scripts:")
        for name, script in SCRIPT_PATHS.items():
            result = subprocess.run(["pgrep", "-f", script], capture_output=True, text=True)
            if result.stdout.strip():
                print(f"🟢 {name} running (PID: {result.stdout.strip()})")
            else:
                print(f"🔴 {name} NOT running")

if __name__ == "__main__":
    main()
