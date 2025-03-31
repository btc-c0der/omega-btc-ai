#!/usr/bin/env python3
# 🔱 OMEGA BTC AI - SACRED TEST LISTENER 🔱

import os
import time
import sqlite3
import subprocess
import logging
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from prometheus_client import start_http_server, Counter, Gauge
import fakeredis
import click
from rich.console import Console
from rich.tree import Tree
from rich.table import Table

# Divine Constants
FAIL_DB = "test_results.db"
FAIL_TABLE = "failures"
PROMETHEUS_PORT = 9091
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# Divine Prometheus Metrics
test_failures_total = Counter('omega_test_failures_total', 'Total number of test failures', ['suite'])
test_failures_duration = Gauge('omega_test_failures_duration_hours', 'Duration of test failures in hours')
last_pass_time = Gauge('omega_last_pass_time_seconds', 'Timestamp of last successful test run')

# Divine Redis Mock
redis_client = fakeredis.FakeRedis()

# Divine Logging
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler('divine_test_listener.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Divine Console
console = Console()

def init_db():
    """Initialize the divine SQLite database."""
    with sqlite3.connect(FAIL_DB) as conn:
        conn.execute(f'''
            CREATE TABLE IF NOT EXISTS {FAIL_TABLE} (
                test_file TEXT,
                suite TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                error_message TEXT
            )
        ''')

def add_failure(test_file, suite, error_message):
    """Record a divine test failure."""
    with sqlite3.connect(FAIL_DB) as conn:
        conn.execute(
            f"INSERT INTO {FAIL_TABLE} (test_file, suite, error_message) VALUES (?, ?, ?)",
            (test_file, suite, error_message)
        )
    test_failures_total.labels(suite=suite).inc()

def get_failures():
    """Retrieve all divine test failures."""
    with sqlite3.connect(FAIL_DB) as conn:
        return conn.execute(f"SELECT DISTINCT test_file, suite FROM {FAIL_TABLE}").fetchall()

def clear_failures():
    """Clear all divine test failures."""
    with sqlite3.connect(FAIL_DB) as conn:
        conn.execute(f"DELETE FROM {FAIL_TABLE}")

def get_suite_from_path(path):
    """Extract the divine suite name from the test path."""
    parts = path.split(os.sep)
    if 'tests' in parts:
        idx = parts.index('tests')
        if len(parts) > idx + 1:
            return parts[idx + 1]
    return 'unknown'

class DivineHandler(FileSystemEventHandler):
    """Divine file system event handler."""
    
    def __init__(self, test_runner):
        self.test_runner = test_runner

    def on_modified(self, event):
        """Handle divine file modification events."""
        if event.src_path.endswith(".py") and "/tests/" in event.src_path:
            logger.info(f"🔍 Divine change detected in {event.src_path}")
            self.test_runner.run_tests()

class DivineTestRunner:
    """Divine test runner with failure tracking."""
    
    def __init__(self):
        self.last_success = None
        self.failures = set()

    def run_tests(self):
        """Run all divine tests and track failures."""
        logger.info("🧪 Running divine test suite...")
        
        # Run tests with pytest
        result = subprocess.run(
            ["pytest", "tests/", "--tb=short", "--maxfail=1"],
            capture_output=True,
            text=True
        )
        
        # Process results
        if result.returncode == 0:
            self.handle_success()
        else:
            self.handle_failures(result.stdout)

    def handle_success(self):
        """Handle divine test success."""
        self.last_success = time.time()
        last_pass_time.set(self.last_success)
        if self.failures:
            logger.info("✨ All divine tests passed! Clearing failure history.")
            clear_failures()
            self.failures.clear()
            test_failures_duration.set(0)

    def handle_failures(self, output):
        """Handle divine test failures."""
        for line in output.split("\n"):
            if "FAILED" in line and "tests/" in line:
                test_file = line.split()[0]
                suite = get_suite_from_path(test_file)
                self.failures.add((test_file, suite))
                add_failure(test_file, suite, line)
        
        # Update Prometheus metrics
        if self.last_success:
            duration = (time.time() - self.last_success) / 3600  # hours
            test_failures_duration.set(duration)

def generate_test_tree():
    """Generate a divine test tree visualization."""
    tree = Tree("📂 tests/")
    
    # Get test statistics
    stats = {}
    for root, _, files in os.walk("tests/"):
        suite = os.path.basename(root)
        if suite == "tests":
            continue
        py_files = [f for f in files if f.endswith(".py")]
        if py_files:
            stats[suite] = len(py_files)
    
    # Build tree
    for suite, count in stats.items():
        branch = tree.add(f"├── {suite}/", style="bold")
        branch.add(f"[{count} tests]")
    
    return tree

def print_test_stats():
    """Print divine test statistics."""
    table = Table(title="📊 Divine Test Statistics")
    table.add_column("Suite", style="cyan")
    table.add_column("Tests", justify="right")
    table.add_column("Failing", justify="right")
    table.add_column("Status", style="green")
    
    failures = get_failures()
    failure_counts = {}
    for _, suite in failures:
        failure_counts[suite] = failure_counts.get(suite, 0) + 1
    
    for root, _, files in os.walk("tests/"):
        suite = os.path.basename(root)
        if suite == "tests":
            continue
        py_files = [f for f in files if f.endswith(".py")]
        if py_files:
            failing = failure_counts.get(suite, 0)
            status = "✅" if failing == 0 else "❌"
            table.add_row(
                suite,
                str(len(py_files)),
                str(failing),
                status
            )
    
    console.print(table)

@click.group()
def cli():
    """🔱 OMEGA BTC AI - Divine Test Listener CLI"""
    pass

@cli.command()
def start():
    """Start the divine test listener."""
    init_db()
    start_http_server(PROMETHEUS_PORT)
    
    runner = DivineTestRunner()
    observer = Observer()
    observer.schedule(DivineHandler(runner), path=".", recursive=True)
    
    logger.info("👁️  NE0 M4TR1X Listener started...")
    observer.start()
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

@cli.command()
def stats():
    """Show divine test statistics."""
    print_test_stats()

@cli.command()
def tree():
    """Show divine test tree."""
    console.print(generate_test_tree())

if __name__ == "__main__":
    cli() 