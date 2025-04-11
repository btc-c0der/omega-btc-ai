#!/usr/bin/env python3
"""
Divine Book Dashboard Server v3.0
A quantum-enhanced HTTP server for the Divine Book Dashboard running on port 8889

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
from pathlib import Path
import socket
import glob
import re
import uvicorn
import asyncio
import gradio as gr
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
import importlib.util
import threading
import redis
from utils.redis_helper import (
    get_redis_client, 
    set_json, 
    get_json, 
    log_event, 
    record_metric,
    get_namespaced_key,
    increment,
    push_to_list,
    get_list
)
import random
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'divine_server.log'))
    ]
)
logger = logging.getLogger('divine_server')

# Server configuration
DASHBOARD_PORT = 8889    # Main dashboard port
GRADIO_PORT = 7860       # Cybertruck QA Dashboard port
METRICS_PORT = 7861      # Dashboard Metrics port
NFT_PORT = 7862          # NFT Dashboard port
IBR_SPAIN_PORT = 7863    # IBR España Dashboard port
DIVINE_BOOK_PORT = 7864  # Divine Book Dashboard port
ORB_TEMPLE_PORT = 7865   # Omega Orb Temple Dashboard port
HACKER_ARCHIVE_PORT = 7866 # Hacker Archive Dashboard port
SHA256_OMEGA_PORT = 7867 # SHA256 Omega Dashboard port
SHA356_SACRED_PORT = 7868 # SHA356 Sacred Dashboard port
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Redis integration flag
USE_REDIS = True

# Try to import the Cybertruck test framework
try:
    cybertruck_path = os.path.join(REPO_ROOT, "src", "omega_bot_farm", "qa", "cybertruck_test_framework.py")
    if os.path.exists(cybertruck_path):
        spec = importlib.util.spec_from_file_location("cybertruck_test_framework", cybertruck_path)
        if spec is not None and spec.loader is not None:
            cybertruck_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cybertruck_module)
            cybertruck_engine = getattr(cybertruck_module, "CybertruckTestEngine", None)
            logger.info("Successfully loaded Cybertruck Test Framework")
        else:
            cybertruck_engine = None
            logger.warning("Failed to get valid module spec for Cybertruck Test Framework")
    else:
        cybertruck_engine = None
        logger.warning(f"Cybertruck Test Framework not found at {cybertruck_path}")
except Exception as e:
    cybertruck_engine = None
    logger.error(f"Error importing Cybertruck Test Framework: {e}")

# Create FastAPI app
app = FastAPI(title="Divine Dashboard v3 API")

# Create FastAPI app for Gradio
gradio_app = FastAPI(title="Tesla Cybertruck QA Interface")

# Create FastAPI app for NFT Dashboard
nft_app = FastAPI(title="Divine NFT Dashboard")

# Create FastAPI app for IBR Spain
ibr_spain_app = FastAPI(title="IBR España Dashboard")

# Create FastAPI app for Divine Book
divine_book_app = FastAPI(title="Divine Book Dashboard")

# Create FastAPI app for Omega Orb Temple
orb_temple_app = FastAPI(title="Omega Orb Temple")

# Create FastAPI app for Hacker Archive
hacker_archive_app = FastAPI(title="Hacker Archive Dashboard")

# Create FastAPI app for SHA256 Omega
sha256_omega_app = FastAPI(title="SHA256 Omega Dashboard")

# Create FastAPI app for SHA356 Sacred
sha356_sacred_app = FastAPI(title="SHA356 Sacred Dashboard")

# Global variable to store test results
test_results = {"status": "idle", "result": None, "details": None}
test_lock = asyncio.Lock()

# Global variable for telemetry data
telemetry_data = []

def get_all_documents():
    """Get all markdown and HTML documents from the repository"""
    documents = []
    book_path = os.path.join(REPO_ROOT, 'BOOK')
    
    # Helper function to categorize documents based on filename
    def categorize_document(filename):
        # Default category is DOCUMENTATION
        category = "DOCUMENTATION"
        
        # Check for keywords in the filename
        if re.search(r'QUANTUM|QUBIT', filename, re.IGNORECASE):
            category = "QUANTUM"
        elif re.search(r'DIVINE|SACRED|RITUAL', filename, re.IGNORECASE):
            category = "DIVINE"
        elif re.search(r'COSMIC|UNIVERSE', filename, re.IGNORECASE):
            category = "COSMIC"
        elif re.search(r'BOT|TRADER|TRADING|MARKET', filename, re.IGNORECASE):
            category = "TRADING"
        elif re.search(r'TEST|COVERAGE', filename, re.IGNORECASE):
            category = "TESTING"
        elif re.search(r'DEPLOY|KUBERNETES|DOCKER', filename, re.IGNORECASE):
            category = "DEPLOYMENT"
        elif re.search(r'CODE|SRC|IMPLEMENT', filename, re.IGNORECASE):
            category = "SOURCE"
            
        return category
        
    # Find all markdown files
    md_files = []
    for md_file in glob.glob(f"{book_path}/**/*.md", recursive=True):
        # Get relative path from repo root
        rel_path = os.path.relpath(md_file, REPO_ROOT)
        filename = os.path.basename(md_file)
        title = os.path.splitext(filename)[0].replace('_', ' ')
        
        # Categorize the document
        category = categorize_document(filename)
        
        md_files.append({
            'path': rel_path,
            'title': title,
            'category': category,
            'description': f"Documentation for {title}",
            'type': 'md'
        })
        
        # Check for corresponding HTML file
        html_file = md_file.replace('.md', '.html')
        if os.path.exists(html_file):
            html_rel_path = os.path.relpath(html_file, REPO_ROOT)
            md_files.append({
                'path': html_rel_path,
                'title': title,
                'category': category,
                'description': f"HTML version of {title}",
                'type': 'html'
            })
            
    return md_files

def get_codebase_stats():
    """Get statistics about the codebase"""
    stats = {
        'total_files': 0,
        'total_lines': 0,
        'total_size': 0,
        'analysis_date': None,
        'extensions': {}
    }
    
    # List of extensions to analyze
    extensions = ['.py', '.js', '.html', '.css', '.md', '.sh', '.json']
    
    # Walk through the repository
    for root, dirs, files in os.walk(REPO_ROOT):
        # Skip node_modules and other large directories
        if any(excluded in root for excluded in ['node_modules', '.git', '__pycache__']):
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()
            
            # Only analyze files with specified extensions
            if file_ext in extensions:
                try:
                    file_size = os.path.getsize(file_path)
                    stats['total_files'] += 1
                    stats['total_size'] += file_size
                    
                    # Count lines in the file
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        line_count = sum(1 for _ in f)
                        stats['total_lines'] += line_count
                        
                    # Add to extension stats
                    if file_ext not in stats['extensions']:
                        stats['extensions'][file_ext] = {
                            'files': 0,
                            'lines': 0,
                            'size': 0
                        }
                        
                    stats['extensions'][file_ext]['files'] += 1
                    stats['extensions'][file_ext]['lines'] += line_count
                    stats['extensions'][file_ext]['size'] += file_size
                except Exception as e:
                    logger.error(f"Error analyzing file {file_path}: {e}")
    
    # Format total size as human-readable
    stats['total_size_formatted'] = format_size(stats['total_size'])
    
    # Format extension sizes as human-readable
    for ext in stats['extensions']:
        stats['extensions'][ext]['size_formatted'] = format_size(
            stats['extensions'][ext]['size']
        )
        
    return stats

def format_size(size_in_bytes):
    """Format size in bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024 or unit == 'GB':
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024

# Define API endpoints for the main dashboard
@app.get('/api/documents')
async def api_get_documents():
    """API endpoint to get document listings"""
    documents = get_all_documents()
    return JSONResponse(content=documents)

@app.get('/api/stats')
async def api_get_stats():
    """API endpoint to get codebase stats"""
    stats = get_codebase_stats()
    return JSONResponse(content=stats)

@app.get('/{full_path:path}')
async def serve_static(full_path: str):
    """Serve static files"""
    # Default to index.html
    if full_path == "" or full_path == "/":
        full_path = "index.html"
        
    file_path = os.path.join(DIRECTORY, full_path)
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    else:
        # Try index.html for SPA routing
        index_path = os.path.join(DIRECTORY, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        else:
            raise HTTPException(status_code=404, detail=f"File {full_path} not found")

# Define API endpoints for the Gradio app
@gradio_app.post("/run-tests")
async def run_tests_endpoint(request: Request):
    """API endpoint to run tests"""
    try:
        payload = await request.json()
        if payload.get("command") == "runTests":
            # Run the tests in a separate thread to avoid blocking
            if cybertruck_engine:
                async with test_lock:
                    global test_results
                    test_results = {"status": "running", "result": None, "details": None}
                
                # Start tests in a separate thread
                threading.Thread(target=run_cybertruck_tests).start()
                return {"status": "running"}
            else:
                return {"status": "error", "message": "Cybertruck Test Engine not available"}
        return {"status": "ignored"}
    except Exception as e:
        logger.error(f"Error in run_tests_endpoint: {e}")
        return {"status": "error", "message": str(e)}

@gradio_app.get("/test-status")
async def test_status_endpoint():
    """Get the current status of tests"""
    async with test_lock:
        return test_results

async def run_cybertruck_test(test_name):
    """Run Cybertruck tests"""
    global test_results
    logger.info(f"Running test: {test_name}")
    
    async with test_lock:
        test_results = {"status": "running", "result": None, "details": None}
        
        try:
            # Run the test
            if test_name == "full_system":
                await asyncio.sleep(5)  # Simulate long test
                result = True
                details = "All systems nominal"
            elif test_name == "battery":
                await asyncio.sleep(2)
                result = True
                details = "Battery capacity at 98.7%"
            elif test_name == "motor":
                await asyncio.sleep(3)
                result = random.choice([True, True, False])  # 2/3 chance of success
                details = "Motor efficiency at 97.2%" if result else "Motor temperature exceeds normal range"
            else:
                result = False
                details = f"Unknown test: {test_name}"
            
            test_results = {
                "status": "complete", 
                "result": result, 
                "details": details,
                "timestamp": datetime.now().isoformat()
            }
            
            # Store test results in Redis
            if USE_REDIS:
                try:
                    # Create a unique test result key
                    test_id = f"{test_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    test_key = get_namespaced_key("cybertruck_tests", test_id)
                    
                    # Store test result data
                    test_data = {
                        "test_name": test_name,
                        "result": result,
                        "details": details,
                        "timestamp": datetime.now().isoformat()
                    }
                    set_json(test_key, test_data)
                    
                    # Add to test history list
                    history_key = get_namespaced_key("cybertruck_tests", "history")
                    push_to_list(history_key, test_key)
                    
                    # Track test statistics
                    if result:
                        increment(get_namespaced_key("counters", "cybertruck_tests_passed"))
                    else:
                        increment(get_namespaced_key("counters", "cybertruck_tests_failed"))
                    
                    # Log the test event
                    log_event("cybertruck_test", {
                        "test_name": test_name,
                        "result": result,
                        "details": details
                    })
                    
                    logger.info(f"Test results stored in Redis: {test_key}")
                except Exception as e:
                    logger.error(f"Redis error storing test results: {str(e)}")
            
            return test_results
        except Exception as e:
            logger.error(f"Error running test: {str(e)}")
            test_results = {"status": "error", "result": False, "details": str(e)}
            return test_results

def run_cybertruck_tests():
    """Run all Cybertruck tests"""
    try:
        logger.info("Starting Cybertruck tests")
        
        # Create an instance of the test engine if available
        if cybertruck_engine:
            engine = cybertruck_engine()
            result = engine.run_all_tests()
            
            # Update test results
            global test_results
            # Use asyncio.run directly instead of with statement
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(update_test_results(result))
            loop.close()
        else:
            logger.error("Cybertruck Test Engine not available")
    except Exception as e:
        logger.error(f"Error running Cybertruck tests: {e}")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(update_test_results({"passed": False, "error": str(e)}))
        loop.close()

async def update_test_results(result):
    """Update test results with asyncio lock"""
    async with test_lock:
        global test_results
        test_results = {
            "status": "complete",
            "result": "pass" if result.get("passed", False) else "fail",
            "details": result
        }
        logger.info(f"Test results updated: {test_results}")

# Create the Gradio interface
def create_gradio_interface():
    """Create the Gradio interface for the Tesla Cybertruck QA Dashboard"""
    with gr.Blocks(title="Tesla Cybertruck QA Dashboard") as demo:
        with gr.Column():
            gr.Markdown("# 🚗 Tesla Cybertruck QA Dashboard 🚗")
            gr.Markdown("### Welcome to the Cybertruck QA Dashboard!")
            
            # Status display
            status_md = gr.Markdown("**Status:** Ready to run tests")
            
            # Buttons
            with gr.Row():
                run_btn = gr.Button("Run All Tests", variant="primary")
                status_btn = gr.Button("Check Status")
                
            # Results display
            with gr.Column():
                gr.Markdown("## Test Results")
                results_md = gr.Markdown("No tests have been run yet.")
        
        # JavaScript for postMessage communication
        gr.HTML("""
        <script>
        // Wrap in try/catch to prevent errors
        try {
            // Listen for messages from the parent window
            window.addEventListener('message', function(event) {
                console.log("Received message:", event.data);
                if (event.data && event.data.command === "runTests") {
                    try {
                        // Find the Run All Tests button by text content
                        var buttons = document.querySelectorAll('button');
                        var testButton = null;
                        buttons.forEach(function(btn) {
                            if (btn.textContent.includes("Run All Tests")) {
                                testButton = btn;
                            }
                        });
                        
                        if (testButton) {
                            testButton.click();
                        } else {
                            console.error("Could not find Run All Tests button");
                        }
                    } catch (e) {
                        console.error("Error triggering test button click:", e);
                    }
                }
            });

            // Function to send results back to parent
            function sendResultsToParent(status, result) {
                try {
                    if (window.parent && window.parent !== window) {
                        window.parent.postMessage({
                            source: "cybertruck-qa",
                            status: status,
                            result: result
                        }, "*");
                        console.log("Sent results to parent:", status, result);
                    }
                } catch (e) {
                    console.error("Error sending results to parent:", e);
                }
            }
            
            // Set interval to check test status
            var statusCheckInterval;
            
            function startStatusChecking() {
                try {
                    statusCheckInterval = setInterval(function() {
                        // Find Check Status button by text content
                        var buttons = document.querySelectorAll('button');
                        var statusButton = null;
                        buttons.forEach(function(btn) {
                            if (btn.textContent.includes("Check Status")) {
                                statusButton = btn;
                            }
                        });
                        
                        if (statusButton) {
                            statusButton.click();
                        } else {
                            console.error("Could not find Check Status button");
                            clearInterval(statusCheckInterval);
                        }
                    }, 1000);
                    
                    // Stop checking after 30 seconds to prevent infinite loops
                    setTimeout(function() {
                        clearInterval(statusCheckInterval);
                    }, 30000);
                } catch (e) {
                    console.error("Error in startStatusChecking:", e);
                    if (statusCheckInterval) {
                        clearInterval(statusCheckInterval);
                    }
                }
            }

            // Add font preloading to prevent 404 errors
            function preloadFonts() {
                try {
                    var style = document.createElement('style');
                    style.textContent = `
                        /* Font preloading to prevent 404 errors */
                        @font-face {
                            font-family: 'ui-sans-serif';
                            src: local('Segoe UI'), local('Helvetica Neue'), local('Arial'), sans-serif;
                            font-weight: normal;
                            font-display: swap;
                        }
                        
                        @font-face {
                            font-family: 'ui-sans-serif';
                            src: local('Segoe UI Bold'), local('Helvetica Neue Bold'), local('Arial Bold'), sans-serif;
                            font-weight: bold;
                            font-display: swap;
                        }
                        
                        @font-face {
                            font-family: 'system-ui';
                            src: local('Segoe UI'), local('Helvetica Neue'), local('Arial'), sans-serif;
                            font-weight: normal;
                            font-display: swap;
                        }
                        
                        @font-face {
                            font-family: 'system-ui';
                            src: local('Segoe UI Bold'), local('Helvetica Neue Bold'), local('Arial Bold'), sans-serif;
                            font-weight: bold;
                            font-display: swap;
                        }
                    `;
                    document.head.appendChild(style);
                    console.log("Font preloading initialized");
                } catch (e) {
                    console.error("Error in preloadFonts:", e);
                }
            }

            // Run font preloading when DOM is ready
            if (document.readyState === "loading") {
                document.addEventListener("DOMContentLoaded", preloadFonts);
            } else {
                preloadFonts();
            }
        } catch (e) {
            console.error("Critical error in Cybertruck QA Dashboard initialization:", e);
        }
        </script>
        """)

        # Handle button clicks
        def on_run_tests_click():
            # Send HTTP POST request to /run-tests endpoint
            import requests
            try:
                response = requests.post("http://localhost:7860/run-tests", 
                                        json={"command": "runTests"},
                                        timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "running":
                        # Start the status check interval
                        return "**Status:** Tests are running... Please wait."
                else:
                    return f"**Status:** Error starting tests (HTTP {response.status_code})"
            except Exception as e:
                return f"**Status:** Error starting tests: {str(e)}"
            
            return "**Status:** Attempting to run tests..."
        
        def on_status_check():
            # Send HTTP GET request to /test-status endpoint
            import requests
            try:
                response = requests.get("http://localhost:7860/test-status", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status", "unknown")
                    result = data.get("result")
                    details = data.get("details", {})
                    
                    if status == "running":
                        status_text = "**Status:** Tests are running..."
                        results_text = "Tests in progress. Please wait for results."
                    elif status == "complete":
                        pass_fail = "PASSED ✅" if result == "pass" else "FAILED ❌"
                        status_text = f"**Status:** Tests {pass_fail}"
                        
                        # Format test details
                        results_text = f"## Test Results: {pass_fail}\n\n"
                        if details:
                            # Create a markdown table of results
                            results_text += "| Test | Result |\n| --- | --- |\n"
                            for test, res in details.items():
                                if test != "passed" and test != "error":
                                    test_result = "✅ Pass" if res else "❌ Fail"
                                    results_text += f"| {test} | {test_result} |\n"
                            
                            # Add any error messages
                            if "error" in details:
                                results_text += f"\n### Error: {details['error']}"
                        
                        # Add JavaScript to notify parent window
                        results_text += f"""
                        <script>
                        sendResultsToParent("testsComplete", "{result}");
                        clearInterval(statusCheckInterval);
                        </script>
                        """
                    else:
                        status_text = f"**Status:** {status.capitalize()}"
                        results_text = "No test results available."
                    
                    return status_text, results_text
                else:
                    return f"**Status:** Error checking status (HTTP {response.status_code})", "Error retrieving test results."
            except Exception as e:
                return f"**Status:** Error checking status: {str(e)}", "Error retrieving test results."
        
        run_btn.click(on_run_tests_click, outputs=status_md)
        status_btn.click(on_status_check, outputs=[status_md, results_md])

        # JavaScript to automatically start checking status after running tests
        run_btn.click(
            None,
            None,
            None,
            js="startStatusChecking"
        )
        
        return demo

# Run both servers
def run_servers():
    """Run the FastAPI and Gradio servers"""
    # Mount the Gradio app
    gradio_interface = create_gradio_interface()
    
    # Import metrics dashboard
    try:
        metrics_module_path = os.path.join(DIRECTORY, "components", "metrics_dashboard.py")
        if os.path.exists(metrics_module_path):
            spec = importlib.util.spec_from_file_location("metrics_dashboard", metrics_module_path)
            if spec is not None and spec.loader is not None:
                metrics_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(metrics_module)
                run_metrics_dashboard = getattr(metrics_module, "run_metrics_dashboard", None)
                
                # Start metrics dashboard in a separate thread
                if run_metrics_dashboard:
                    metrics_thread = threading.Thread(
                        target=lambda: run_metrics_dashboard(METRICS_PORT), 
                        daemon=True
                    )
                    metrics_thread.start()
                    logger.info(f"✨ Started Metrics Dashboard on port {METRICS_PORT} ✨")
                else:
                    logger.warning("Metrics dashboard run function not found")
            else:
                logger.warning("Failed to get valid module spec for metrics dashboard")
        else:
            logger.warning(f"Metrics dashboard not found at {metrics_module_path}")
    except Exception as e:
        logger.error(f"Error importing metrics dashboard: {e}")
    
    # Import NFT dashboard
    try:
        # Create NFT output directory
        nft_output_dir = os.path.join(DIRECTORY, "nft_output")
        os.makedirs(nft_output_dir, exist_ok=True)
        
        # Import NFT dashboard module
        try:
            from components.nft.nft_dashboard import create_nft_dashboard
            
            # Create NFT dashboard
            nft_dashboard, nft_gr_interface = create_nft_dashboard(nft_app, nft_output_dir)
            
            # Start NFT dashboard in a separate thread
            def run_nft_dashboard():
                try:
                    # Check if we should deploy to Hugging Face Spaces
                    deploy_to_hf = os.environ.get("HF_DEPLOY", "0") == "1"
                    if deploy_to_hf:
                        logger.info("Deploying NFT Dashboard to Hugging Face Spaces...")
                        try:
                            import subprocess
                            # Create a temporary file for NFT dashboard deployment
                            nft_deployment_file = os.path.join(DIRECTORY, "nft_dashboard_deploy.py")
                            with open(nft_deployment_file, "w") as f:
                                f.write("from components.nft.nft_dashboard import create_nft_dashboard\n")
                                f.write("from fastapi import FastAPI\n")
                                f.write("import os\n\n")
                                f.write("# Create NFT dashboard\n")
                                f.write("nft_app = FastAPI(title=\"Divine NFT Dashboard\")\n")
                                f.write("nft_output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), \"nft_output\")\n")
                                f.write("os.makedirs(nft_output_dir, exist_ok=True)\n")
                                f.write("nft_dashboard, nft_interface = create_nft_dashboard(nft_app, nft_output_dir)\n\n")
                                f.write("# Launch the interface\n")
                                f.write("if __name__ == \"__main__\":\n")
                                f.write("    nft_interface.launch()\n")
                            
                            # Run the gradio deploy command
                            subprocess.run(["gradio", "deploy", 
                                            "--repo", "divine-nft-dashboard",
                                            nft_deployment_file])
                        except Exception as e:
                            logger.error(f"Error deploying NFT dashboard: {e}")
                            # Fall back to regular launch
                            nft_gr_interface.launch(
                                server_name="0.0.0.0",
                                server_port=NFT_PORT,
                                share=True
                            )
                    else:
                        # Regular launch with public link
                        nft_gr_interface.launch(
                            server_name="0.0.0.0",
                            server_port=NFT_PORT,
                            share=True
                        )
                except Exception as e:
                    logger.error(f"Error launching NFT dashboard: {e}")
            
            nft_thread = threading.Thread(target=run_nft_dashboard, daemon=True)
            nft_thread.start()
            logger.info(f"✨ Started NFT Dashboard on port {NFT_PORT} ✨")
        except ImportError as e:
            logger.warning(f"Could not import NFT dashboard: {e}")
    except Exception as e:
        logger.error(f"Error setting up NFT dashboard: {e}")
    
    # Import IBR Spain dashboard
    try:
        # Create config directory if it doesn't exist
        config_dir = os.path.join(DIRECTORY, "config")
        os.makedirs(config_dir, exist_ok=True)
        
        # Create default configuration for IBR Spain if it doesn't exist
        ibr_spain_config_path = os.path.join(config_dir, "ibr_spain.json")
        if not os.path.exists(ibr_spain_config_path):
            default_config = {
                "instagram_manager": {
                    "data_dir": os.path.expanduser("~/ibr_data/instagram_manager"),
                    "account_name": "ibrespana",
                    "logging_level": "INFO"
                }
            }
            with open(ibr_spain_config_path, "w") as f:
                json.dump(default_config, f, indent=2)
            logger.info(f"Created default IBR Spain configuration at {ibr_spain_config_path}")
        
        # Import IBR Spain dashboard module
        try:
            # Check if IBR Spain component exists
            ibr_component_dir = os.path.join(DIRECTORY, "components", "ibr_spain")
            ibr_dashboard_path = os.path.join(ibr_component_dir, "ibr_dashboard.py")
            
            if os.path.exists(ibr_dashboard_path):
                # Import the IBR Spain dashboard
                spec = importlib.util.spec_from_file_location(
                    "ibr_dashboard", 
                    ibr_dashboard_path
                )
                if spec is not None and spec.loader is not None:
                    ibr_dashboard_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(ibr_dashboard_module)
                    create_ibr_interface = getattr(ibr_dashboard_module, "create_ibr_interface", None)
                    
                    if create_ibr_interface:
                        # Initialize Instagram Manager
                        try:
                            # Import Instagram Manager
                            instagram_manager_path = os.path.join(
                                ibr_component_dir, 
                                "micro_modules", 
                                "instagram_manager.py"
                            )
                            if os.path.exists(instagram_manager_path):
                                instagram_spec = importlib.util.spec_from_file_location(
                                    "instagram_manager", 
                                    instagram_manager_path
                                )
                                if instagram_spec is not None and instagram_spec.loader is not None:
                                    instagram_module = importlib.util.module_from_spec(instagram_spec)
                                    instagram_spec.loader.exec_module(instagram_module)
                                    InstagramManager = getattr(instagram_module, "InstagramManager", None)
                                    
                                    if InstagramManager:
                                        # Initialize the Instagram Manager
                                        instagram_manager = InstagramManager()
                                        logger.info("Instagram Manager initialized successfully")
                                    else:
                                        logger.warning("InstagramManager class not found in module")
                                else:
                                    logger.warning("Failed to get valid module spec for Instagram Manager")
                            else:
                                logger.warning(f"Instagram Manager not found at {instagram_manager_path}")
                        except Exception as e:
                            logger.error(f"Error initializing Instagram Manager: {e}")
                        
                        # Start IBR Spain dashboard in a separate thread
                        def run_ibr_spain_dashboard():
                            try:
                                # Create the interface
                                ibr_interface = create_ibr_interface()
                                
                                # Launch the interface
                                ibr_interface.launch(
                                    server_name="0.0.0.0",
                                    server_port=IBR_SPAIN_PORT,
                                    share=True,
                                    debug=False,
                                    quiet=True
                                )
                            except Exception as e:
                                logger.error(f"Error launching IBR Spain dashboard: {e}")
                        
                        ibr_spain_thread = threading.Thread(target=run_ibr_spain_dashboard, daemon=True)
                        ibr_spain_thread.start()
                        logger.info(f"✨ Started IBR España Dashboard on port {IBR_SPAIN_PORT} ✨")
                    else:
                        logger.warning("create_ibr_interface function not found in module")
                else:
                    logger.warning("Failed to get valid module spec for IBR Spain dashboard")
            else:
                logger.warning(f"IBR Spain dashboard not found at {ibr_dashboard_path}")
        except ImportError as e:
            logger.warning(f"Could not import IBR Spain dashboard: {e}")
    except Exception as e:
        logger.error(f"Error setting up IBR Spain dashboard: {e}")
    
    # Import Divine Book dashboard
    try:
        # Check if Divine Book component exists
        divine_book_dir = os.path.join(DIRECTORY, "components", "divine_book")
        divine_book_path = os.path.join(divine_book_dir, "divine_book_dashboard.py")
        
        if os.path.exists(divine_book_path):
            # Import the Divine Book dashboard
            spec = importlib.util.spec_from_file_location(
                "divine_book_dashboard", 
                divine_book_path
            )
            if spec is not None and spec.loader is not None:
                divine_book_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(divine_book_module)
                create_divine_book_interface = getattr(divine_book_module, "create_divine_book_dashboard", None)
                
                if create_divine_book_interface:
                    # Start Divine Book dashboard in a separate thread
                    def run_divine_book_dashboard():
                        try:
                            # Create the interface
                            divine_book_interface = create_divine_book_interface()
                            
                            # Launch the interface
                            divine_book_interface.launch(
                                server_name="0.0.0.0",
                                server_port=DIVINE_BOOK_PORT,
                                share=True,
                                debug=False,
                                quiet=True
                            )
                        except Exception as e:
                            logger.error(f"Error launching Divine Book dashboard: {e}")
                    
                    divine_book_thread = threading.Thread(target=run_divine_book_dashboard, daemon=True)
                    divine_book_thread.start()
                    logger.info(f"✨ Started Divine Book Dashboard on port {DIVINE_BOOK_PORT} ✨")
                else:
                    logger.warning("create_divine_book_dashboard function not found in module")
            else:
                logger.warning("Failed to get valid module spec for Divine Book dashboard")
        else:
            logger.warning(f"Divine Book dashboard not found at {divine_book_path}")
    except Exception as e:
        logger.error(f"Error setting up Divine Book dashboard: {e}")
    
    # Import Omega Orb Temple dashboard
    try:
        # Check if Omega Orb Temple component exists
        orb_temple_dir = os.path.join(DIRECTORY, "components", "omega_orb_temple")
        orb_temple_path = os.path.join(orb_temple_dir, "omega_orb_temple.py")
        
        if os.path.exists(orb_temple_path):
            # Import the Omega Orb Temple dashboard
            spec = importlib.util.spec_from_file_location(
                "omega_orb_temple", 
                orb_temple_path
            )
            if spec is not None and spec.loader is not None:
                orb_temple_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(orb_temple_module)
                create_orb_temple_interface = getattr(orb_temple_module, "create_orb_temple_interface", None)
                
                if create_orb_temple_interface:
                    # Start Omega Orb Temple dashboard in a separate thread
                    def run_orb_temple_dashboard():
                        try:
                            # Create the interface
                            orb_temple_interface = create_orb_temple_interface()
                            
                            # Launch the interface
                            orb_temple_interface.launch(
                                server_name="0.0.0.0",
                                server_port=ORB_TEMPLE_PORT,
                                share=True,
                                debug=False,
                                quiet=True
                            )
                        except Exception as e:
                            logger.error(f"Error launching Omega Orb Temple dashboard: {e}")
                    
                    orb_temple_thread = threading.Thread(target=run_orb_temple_dashboard, daemon=True)
                    orb_temple_thread.start()
                    logger.info(f"✨ Started Omega Orb Temple Dashboard on port {ORB_TEMPLE_PORT} ✨")
                else:
                    logger.warning("create_orb_temple_interface function not found in module")
            else:
                logger.warning("Failed to get valid module spec for Omega Orb Temple dashboard")
        else:
            logger.warning(f"Omega Orb Temple dashboard not found at {orb_temple_path}")
    except Exception as e:
        logger.error(f"Error setting up Omega Orb Temple dashboard: {e}")
    
    # Import Hacker Archive dashboard
    try:
        # Check if Hacker Archive component exists
        hacker_archive_dir = os.path.join(DIRECTORY, "components", "hacker_archive")
        hacker_archive_path = os.path.join(hacker_archive_dir, "hacker_archive_dashboard.py")
        
        if os.path.exists(hacker_archive_path):
            # Import the Hacker Archive dashboard
            spec = importlib.util.spec_from_file_location(
                "hacker_archive_dashboard", 
                hacker_archive_path
            )
            if spec is not None and spec.loader is not None:
                hacker_archive_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(hacker_archive_module)
                create_hacker_archive_interface = getattr(hacker_archive_module, "create_hacker_dashboard", None)
                
                if create_hacker_archive_interface:
                    # Start Hacker Archive dashboard in a separate thread
                    def run_hacker_archive_dashboard():
                        try:
                            # Create the interface
                            hacker_archive_interface = create_hacker_archive_interface()
                            
                            # Launch the interface
                            hacker_archive_interface.launch(
                                server_name="0.0.0.0",
                                server_port=HACKER_ARCHIVE_PORT,
                                share=True,
                                debug=False,
                                quiet=True
                            )
                        except Exception as e:
                            logger.error(f"Error launching Hacker Archive dashboard: {e}")
                    
                    hacker_archive_thread = threading.Thread(target=run_hacker_archive_dashboard, daemon=True)
                    hacker_archive_thread.start()
                    logger.info(f"✨ Started Hacker Archive Dashboard on port {HACKER_ARCHIVE_PORT} ✨")
                else:
                    logger.warning("create_hacker_dashboard function not found in module")
            else:
                logger.warning("Failed to get valid module spec for Hacker Archive dashboard")
        else:
            logger.warning(f"Hacker Archive dashboard not found at {hacker_archive_path}")
    except Exception as e:
        logger.error(f"Error setting up Hacker Archive dashboard: {e}")
    
    # Import SHA256 Omega dashboard
    try:
        # Check if SHA256 Omega component exists
        sha256_omega_dir = os.path.join(DIRECTORY, "components", "sha256_omega")
        sha256_omega_path = os.path.join(sha256_omega_dir, "sha256_omega_dashboard.py")
        
        if os.path.exists(sha256_omega_path):
            # Import the SHA256 Omega dashboard
            spec = importlib.util.spec_from_file_location(
                "sha256_omega_dashboard", 
                sha256_omega_path
            )
            if spec is not None and spec.loader is not None:
                sha256_omega_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(sha256_omega_module)
                create_sha256_omega_interface = getattr(sha256_omega_module, "create_interface", None)
                
                if create_sha256_omega_interface:
                    # Start SHA256 Omega dashboard in a separate thread
                    def run_sha256_omega_dashboard():
                        try:
                            # Create the interface
                            sha256_omega_interface = create_sha256_omega_interface()
                            
                            # Launch the interface
                            sha256_omega_interface.launch(
                                server_name="0.0.0.0",
                                server_port=SHA256_OMEGA_PORT,
                                share=True,
                                debug=False,
                                quiet=True
                            )
                        except Exception as e:
                            logger.error(f"Error launching SHA256 Omega dashboard: {e}")
                    
                    sha256_omega_thread = threading.Thread(target=run_sha256_omega_dashboard, daemon=True)
                    sha256_omega_thread.start()
                    logger.info(f"✨ Started SHA256 Omega Dashboard on port {SHA256_OMEGA_PORT} ✨")
                else:
                    logger.warning("create_interface function not found in module")
            else:
                logger.warning("Failed to get valid module spec for SHA256 Omega dashboard")
        else:
            logger.warning(f"SHA256 Omega dashboard not found at {sha256_omega_path}")
    except Exception as e:
        logger.error(f"Error setting up SHA256 Omega dashboard: {e}")
    
    # Import SHA356 Sacred dashboard
    try:
        # Check if SHA356 Sacred component exists
        sha356_sacred_dir = os.path.join(DIRECTORY, "components", "sha356_sacred")
        sha356_sacred_path = os.path.join(sha356_sacred_dir, "sha356_vs_sha256_dashboard.py")
        
        if os.path.exists(sha356_sacred_path):
            # Import the SHA356 Sacred dashboard
            spec = importlib.util.spec_from_file_location(
                "sha356_vs_sha256_dashboard", 
                sha356_sacred_path
            )
            if spec is not None and spec.loader is not None:
                sha356_sacred_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(sha356_sacred_module)
                create_sha356_sacred_interface = getattr(sha356_sacred_module, "create_dashboard", None)
                
                if create_sha356_sacred_interface:
                    # Start SHA356 Sacred dashboard in a separate thread
                    def run_sha356_sacred_dashboard():
                        try:
                            # Create the interface
                            sha356_sacred_interface = create_sha356_sacred_interface()
                            
                            # Launch the interface
                            sha356_sacred_interface.launch(
                                server_name="0.0.0.0",
                                server_port=SHA356_SACRED_PORT,
                                share=True,
                                debug=False,
                                quiet=True
                            )
                        except Exception as e:
                            logger.error(f"Error launching SHA356 Sacred dashboard: {e}")
                    
                    sha356_sacred_thread = threading.Thread(target=run_sha356_sacred_dashboard, daemon=True)
                    sha356_sacred_thread.start()
                    logger.info(f"✨ Started SHA356 Sacred Dashboard on port {SHA356_SACRED_PORT} ✨")
                else:
                    logger.warning("create_dashboard function not found in module")
            else:
                logger.warning("Failed to get valid module spec for SHA356 Sacred dashboard")
        else:
            logger.warning(f"SHA356 Sacred dashboard not found at {sha356_sacred_path}")
    except Exception as e:
        logger.error(f"Error setting up SHA356 Sacred dashboard: {e}")
    
    # Create a thread to run the main dashboard server
    def run_dashboard_server():
        uvicorn.run(app, host="0.0.0.0", port=DASHBOARD_PORT)
    
    # Start the dashboard server thread
    dashboard_thread = threading.Thread(target=run_dashboard_server)
    dashboard_thread.daemon = True
    dashboard_thread.start()
    
    # Start the Gradio server in the main thread
    logger.info(f"✨ Starting Tesla Cybertruck QA Dashboard on port {GRADIO_PORT} ✨")
    
    # Check if we should deploy to Hugging Face Spaces
    deploy_to_hf = os.environ.get("HF_DEPLOY", "0") == "1"
    if deploy_to_hf:
        logger.info("Deploying to Hugging Face Spaces...")
        try:
            import subprocess
            # First, create a requirements.txt file for deployment
            with open("divine_requirements.txt", "w") as f:
                f.write("uvicorn>=0.22.0\n")
                f.write("fastapi>=0.95.2\n")
                f.write("gradio>=3.32.0\n")
                f.write("python-multipart>=0.0.6\n")
                f.write("schedule>=1.2.0\n")
                f.write("numpy>=1.24.3\n")
                f.write("matplotlib>=3.7.1\n")
                f.write("Pillow>=10.0.0\n")
            
            # Run the gradio deploy command to deploy to Hugging Face Spaces
            subprocess.run(["gradio", "deploy", 
                            "--repo", "divine-dashboard-v3",
                            "--requirements", "divine_requirements.txt"])
        except Exception as e:
            logger.error(f"Error deploying to Hugging Face Spaces: {e}")
            # Fall back to regular launch with public link
            gradio_interface.launch(server_name="0.0.0.0", server_port=GRADIO_PORT, share=True)
    else:
        # Regular launch with public link
        gradio_interface.launch(server_name="0.0.0.0", server_port=GRADIO_PORT, share=True)

def collect_telemetry():
    """Collect telemetry data from the Cybertruck"""
    global telemetry_data
    
    # Generate random telemetry data
    current_time = datetime.now().strftime("%H:%M:%S")
    battery_level = random.uniform(50, 100)
    motor_temp = random.uniform(60, 90)
    torque_output = random.uniform(200, 800)
    power_consumption = random.uniform(15, 30)
    
    # Create telemetry data point
    telemetry_point = {
        "timestamp": current_time,
        "battery_level": battery_level,
        "motor_temp": motor_temp,
        "torque_output": torque_output,
        "power_consumption": power_consumption
    }
    
    # Add to telemetry data
    telemetry_data.append(telemetry_point)
    
    # Keep only the most recent 100 data points
    if len(telemetry_data) > 100:
        telemetry_data = telemetry_data[-100:]
    
    # Store in Redis if enabled
    if USE_REDIS:
        try:
            # Store the latest telemetry point
            telemetry_key = get_namespaced_key("telemetry", f"cybertruck:{datetime.now().strftime('%Y%m%d%H%M%S')}")
            set_json(telemetry_key, telemetry_point)
            
            # Add to time-series list
            time_series_key = get_namespaced_key("time_series", "cybertruck_telemetry")
            push_to_list(time_series_key, json.dumps(telemetry_point))
            
            # Record individual metrics
            record_metric("cybertruck_battery_level", battery_level)
            record_metric("cybertruck_motor_temp", motor_temp)
            record_metric("cybertruck_torque_output", torque_output)
            record_metric("cybertruck_power_consumption", power_consumption)
            
            # Log the event
            log_event("telemetry_collected", {
                "battery_level": battery_level,
                "motor_temp": motor_temp
            })
        except Exception as e:
            logger.error(f"Redis error storing telemetry: {str(e)}")
    
    return telemetry_point

def get_test_history(limit=10):
    """Get historical test results from Redis"""
    if not USE_REDIS:
        return []
    
    try:
        # Get the list of test keys
        history_key = get_namespaced_key("cybertruck_tests", "history")
        test_keys = get_list(history_key, start=0, end=limit-1)
        
        # Retrieve each test result
        results = []
        for key in test_keys:
            test_data = get_json(key)
            if test_data:
                results.append(test_data)
        
        return results
    except Exception as e:
        logger.error(f"Error retrieving test history: {str(e)}")
        return []

def get_cybertruck_metrics():
    """Get Cybertruck metrics from Redis"""
    if not USE_REDIS:
        return {}
    
    try:
        # Get test counters
        tests_passed = get_json(get_namespaced_key("counters", "cybertruck_tests_passed")) or 0
        tests_failed = get_json(get_namespaced_key("counters", "cybertruck_tests_failed")) or 0
        
        # Get latest telemetry data
        time_series_key = get_namespaced_key("time_series", "cybertruck_telemetry")
        latest_telemetry_json = get_list(time_series_key, start=-1, end=-1)
        
        latest_telemetry = {}
        if latest_telemetry_json and len(latest_telemetry_json) > 0:
            try:
                import json
                latest_telemetry = json.loads(latest_telemetry_json[0])
            except Exception:
                pass
        
        return {
            "tests_passed": tests_passed,
            "tests_failed": tests_failed,
            "test_success_rate": (tests_passed / (tests_passed + tests_failed)) if (tests_passed + tests_failed) > 0 else 0,
            "latest_telemetry": latest_telemetry
        }
    except Exception as e:
        logger.error(f"Error retrieving Cybertruck metrics: {str(e)}")
        return {}

if __name__ == "__main__":
    logger.info(f"✨ Divine Dashboard v3 Server starting ✨")
    run_servers() 