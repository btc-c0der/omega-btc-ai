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

import http.server
import socketserver
import os
import sys
import logging
import json
from pathlib import Path
import socket
import glob
import re

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
PORT = 8889  # Use a different port from v2 to avoid conflicts
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class DivineDashboardHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler for Divine Dashboard v3"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def log_message(self, format, *args):
        """Override log_message to use our logger"""
        logger.info("%s - %s", self.address_string(), format % args)
    
    def end_headers(self):
        """Add CORS headers to allow access from any origin"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def do_GET(self):
        """Handle GET requests, with API endpoints for document listings and content"""
        # Redirect root to index.html
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        
        # API endpoint for document listings
        elif self.path.startswith('/api/documents'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            documents = self.get_all_documents()
            self.wfile.write(json.dumps(documents).encode())
            return
            
        # API endpoint for stats
        elif self.path.startswith('/api/stats'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            stats = self.get_codebase_stats()
            self.wfile.write(json.dumps(stats).encode())
            return
            
        # Handle normal files
        return super().do_GET()
    
    def get_all_documents(self):
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
    
    def get_codebase_stats(self):
        """Get statistics about the codebase"""
        stats = {
            'total_files': 0,
            'total_lines': 0,
            'total_size': 0,
            'analysis_date': self.date_time_string(),
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
        stats['total_size_formatted'] = self.format_size(stats['total_size'])
        
        # Format extension sizes as human-readable
        for ext in stats['extensions']:
            stats['extensions'][ext]['size_formatted'] = self.format_size(
                stats['extensions'][ext]['size']
            )
            
        return stats
    
    def format_size(self, size_in_bytes):
        """Format size in bytes to human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_in_bytes < 1024 or unit == 'GB':
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024

def run_server():
    """Run the divine dashboard server"""
    os.chdir(DIRECTORY)
    handler = DivineDashboardHandler
    
    # Try to bind to the primary port, if that fails try alternate ports
    port = PORT
    max_port_attempts = 5
    for attempt in range(max_port_attempts):
        try:
            with socketserver.TCPServer(("", port), handler) as httpd:
                logger.info(f"✨ Divine Dashboard v3 Server started at http://localhost:{port} ✨")
                logger.info(f"Serving from directory: {DIRECTORY}")
                logger.info("Press Ctrl+C to stop the server")
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    logger.info("Server stopped by user")
                except Exception as e:
                    logger.error(f"Server error: {e}")
                finally:
                    httpd.server_close()
                    logger.info("Server closed")
                return
        except OSError as e:
            if e.errno == 48:  # Address already in use
                logger.warning(f"Port {port} is already in use")
                port += 1
                if attempt < max_port_attempts - 1:
                    logger.info(f"Trying alternate port: {port}")
                else:
                    logger.error(f"Failed to find an available port after {max_port_attempts} attempts")
                    sys.exit(1)
            else:
                logger.error(f"Error starting server: {e}")
                sys.exit(1)

if __name__ == "__main__":
    run_server() 