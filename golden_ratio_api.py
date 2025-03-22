#!/usr/bin/env python3
"""
OMEGA BTC AI - Golden Ratio Visualization API
==================================================

A Flask API that connects the HTML UI to the golden ratio visualization functionality.
"""

import os
import sys
import asyncio
import subprocess
from datetime import datetime
from flask import Flask, request, jsonify, send_file, render_template

# Import the visualization functions from position_flow_tracker
from scripts.position_flow_tracker import visualize_golden_ratio_overlay, connect_to_redis

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    """Serve the HTML UI."""
    return send_file('btc_golden_ratio_ui.html')

@app.route('/api/generate', methods=['POST'])
def generate_visualization():
    """Generate a new golden ratio visualization with the given parameters."""
    try:
        # Get parameters from request
        data = request.json or {}
        years = int(data.get('years', 7))
        use_redis = data.get('dataSource', 'redis') == 'redis'
        
        # Create a timestamp for the output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"btc_golden_ratio_{years}yr_{timestamp}.png"
        
        # This part is tricky since we need to run an async function
        # We'll use a subprocess to run the CLI script instead
        cmd = [
            sys.executable,
            'scripts/position_flow_tracker.py',
            '--golden-ratio',
            f'--years={years}'
        ]
        
        if not use_redis:
            cmd.append('--no-redis')
            
        # Run the subprocess
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return jsonify({
                'success': False,
                'error': f"Error generating visualization: {result.stderr}"
            }), 500
        
        # Find the latest generated file matching our pattern
        files = [f for f in os.listdir('.') if f.startswith(f'btc_golden_ratio_{years}yr_')]
        if not files:
            return jsonify({
                'success': False,
                'error': "No visualization file generated"
            }), 500
            
        # Get the most recent file
        latest_file = max(files, key=lambda f: os.path.getctime(f))
        
        return jsonify({
            'success': True,
            'file': f'/api/images/{latest_file}',
            'message': f"Visualization generated with {years} years of {'historical' if use_redis else 'simulated'} data."
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/images/<filename>')
def serve_image(filename):
    """Serve a generated image."""
    if os.path.exists(filename):
        return send_file(filename)
    else:
        return "Image not found", 404

if __name__ == '__main__':
    print("Starting OMEGA BTC AI Golden Ratio Visualization API...")
    app.run(debug=True, host='0.0.0.0', port=5050) 