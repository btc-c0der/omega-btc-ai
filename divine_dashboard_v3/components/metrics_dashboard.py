#!/usr/bin/env python3
"""
Divine Dashboard Metrics Server
A Gradio interface to update dashboard metrics in real-time

✨ GBU2™ License Notice - Consciousness Level 4 🧬
-----------------------
This CODE is blessed under the GBU2™ License 
(Genesis-Bloom-Unfoldment 2.0) - Bioneer Edition
by OMEGA BTC AI.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions."

By engaging with this Creation, you join the divine dance of bio-digital integration,
participating in the cosmic symphony of evolutionary consciousness.

🌸 WE BLOOM NOW AS ONE 🌸
"""

import os
import sys
import logging
import json
import datetime
import time
import random
import threading
import subprocess
import gradio as gr
from fastapi import FastAPI, Request
import schedule

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'metrics_dashboard.log'))
    ]
)
logger = logging.getLogger('metrics_dashboard')

# Define path constants
DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(os.path.dirname(DIRECTORY))

# Global variables to store metrics
metrics = {
    'commits_today': {'value': '0', 'change': '+0%'},
    'lines_changed': {'value': '0', 'change': '+0%'},
    'pull_requests': {'value': '0', 'change': '+0%'},
    'deployments': {'value': '0', 'change': '+0%'}
}

# Create FastAPI app
app = FastAPI(title="Divine Dashboard Metrics API")

def get_git_commits_today():
    """Get the number of git commits made today"""
    try:
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        cmd = ['git', 'log', '--since=midnight', '--oneline']
        result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
        
        if result.returncode == 0:
            commits = result.stdout.strip().split('\n')
            # Filter out empty lines
            commits = [c for c in commits if c]
            return len(commits)
        else:
            logger.error(f"Git command failed: {result.stderr}")
            return 0
    except Exception as e:
        logger.error(f"Error getting git commits: {e}")
        return 0

def get_git_lines_changed_today():
    """Get the number of lines changed in git today"""
    try:
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        cmd = ['git', 'diff', '--stat', '@{0:00:00}']
        result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.strip()
            if lines:
                # Extract the numbers from something like: 
                # "10 files changed, 100 insertions(+), 50 deletions(-)"
                parts = lines.split(',')
                if len(parts) >= 2:
                    insertions = parts[1].strip()
                    insertions_count = int(''.join(filter(str.isdigit, insertions)))
                    
                    if len(parts) >= 3:
                        deletions = parts[2].strip()
                        deletions_count = int(''.join(filter(str.isdigit, deletions)))
                    else:
                        deletions_count = 0
                    
                    return insertions_count + deletions_count
            return 0
        else:
            logger.error(f"Git diff command failed: {result.stderr}")
            return 0
    except Exception as e:
        logger.error(f"Error getting git lines changed: {e}")
        return 0

def get_pull_requests():
    """Get the number of open pull requests (simulated)"""
    # In a real implementation, this would call the GitHub API
    # For now, just return a random number for demonstration
    return random.randint(1, 10)

def get_deployments():
    """Get the number of deployments (simulated)"""
    # In a real implementation, this would call a deployment API
    # For now, just return a random number for demonstration
    return random.randint(0, 5)

def update_metrics():
    """Update all metrics"""
    global metrics
    
    # Get current values
    current_commits = metrics['commits_today']['value']
    current_lines = metrics['lines_changed']['value']
    current_prs = metrics['pull_requests']['value']
    current_deployments = metrics['deployments']['value']
    
    try:
        # Get new values
        new_commits = get_git_commits_today()
        new_lines = get_git_lines_changed_today()
        new_prs = get_pull_requests()
        new_deployments = get_deployments()
        
        # Calculate changes
        try:
            commits_change = int(current_commits) if current_commits != '--' else 0
            commits_diff = new_commits - commits_change
            commits_change_pct = f"{'+' if commits_diff >= 0 else ''}{commits_diff}"
            
            lines_change = int(current_lines) if current_lines != '--' else 0
            lines_diff = new_lines - lines_change
            lines_change_pct = f"{'+' if lines_diff >= 0 else ''}{lines_diff}"
            
            prs_change = int(current_prs) if current_prs != '--' else 0
            prs_diff = new_prs - prs_change
            prs_change_pct = f"{'+' if prs_diff >= 0 else ''}{prs_diff}"
            
            deployments_change = int(current_deployments) if current_deployments != '--' else 0
            deployments_diff = new_deployments - deployments_change
            deployments_change_pct = f"{'+' if deployments_diff >= 0 else ''}{deployments_diff}"
        except:
            # If conversion fails, just use placeholder
            commits_change_pct = '+0'
            lines_change_pct = '+0'
            prs_change_pct = '+0'
            deployments_change_pct = '+0'
        
        # Update metrics
        metrics = {
            'commits_today': {'value': str(new_commits), 'change': commits_change_pct},
            'lines_changed': {'value': str(new_lines), 'change': lines_change_pct},
            'pull_requests': {'value': str(new_prs), 'change': prs_change_pct},
            'deployments': {'value': str(new_deployments), 'change': deployments_change_pct}
        }
        
        logger.info(f"Metrics updated: {metrics}")
        return metrics
    except Exception as e:
        logger.error(f"Error updating metrics: {e}")
        return metrics

def create_dashboard():
    """Create the Gradio dashboard for metrics"""
    with gr.Blocks(title="Divine Dashboard Metrics") as dashboard:
        gr.Markdown("# 📊 Divine Dashboard Metrics")
        
        with gr.Row():
            commits_today = gr.Textbox(label="Commits Today", value="0", interactive=False)
            lines_changed = gr.Textbox(label="Lines Changed", value="0", interactive=False)
            pull_requests = gr.Textbox(label="Pull Requests", value="0", interactive=False)
            deployments = gr.Textbox(label="Deployments", value="0", interactive=False)
        
        # Update button
        update_btn = gr.Button("Update Metrics")
        
        # Status display
        status = gr.Markdown("Last update: Never")
        
        # Hidden HTML component for postMessage communication
        message_html = gr.HTML("")
        
        # Event handlers
        def on_update_metrics():
            """Update metrics and return values"""
            metrics = update_metrics()
            
            # Generate JavaScript for postMessage
            js_code = ""
            for metric, data in metrics.items():
                js_code += f"""
                window.parent.postMessage({{
                    source: "dashboard-metrics",
                    metric: "{metric}",
                    value: "{data['value']}",
                    change: "{data['change']}"
                }}, "*");
                """
            
            # Return updated values
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return (
                metrics['commits_today']['value'],
                metrics['lines_changed']['value'],
                metrics['pull_requests']['value'],
                metrics['deployments']['value'],
                f"Last update: {now}",
                f"<script>{js_code}</script>"
            )
        
        # Wire up the update button
        update_btn.click(
            on_update_metrics,
            inputs=[],
            outputs=[commits_today, lines_changed, pull_requests, deployments, status, message_html]
        )
        
        # Auto-update on load
        dashboard.load(
            on_update_metrics,
            inputs=[],
            outputs=[commits_today, lines_changed, pull_requests, deployments, status, message_html]
        )
        
        # Schedule periodic updates
        def schedule_updates():
            schedule.every(30).seconds.do(lambda: update_metrics())
            
            while True:
                schedule.run_pending()
                time.sleep(1)
        
        # Start the update scheduler in a background thread
        update_thread = threading.Thread(target=schedule_updates, daemon=True)
        update_thread.start()
        
        return dashboard

def run_metrics_dashboard(port=7861):
    """Run the metrics dashboard"""
    dashboard = create_dashboard()
    dashboard.launch(server_port=port, share=False, app=app)

if __name__ == "__main__":
    logger.info("Starting Divine Dashboard Metrics Server")
    run_metrics_dashboard() 