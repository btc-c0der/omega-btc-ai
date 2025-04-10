# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
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

"""
SHA256 Crypto Analyzer Dashboard

Gradio interface for the SHA256 crypto analyzer, providing visualization and analysis
of cryptographic hashes and blockchain proofs.
"""

import os
import re
import json
import time
import base64
import asyncio
import hashlib
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union

try:
    import gradio as gr
    GRADIO_AVAILABLE = True
except ImportError:
    GRADIO_AVAILABLE = False

from .crypto_analyzer import SHA256Analyzer, PDFCryptoAnalyzer

# ASCII Art Banner
CRYPTO_BANNER = """
  ███████╗██╗  ██╗ █████╗ ██████╗ ███████╗ ██████╗     ██╗  ██╗ █████╗ ███████╗██╗  ██╗
  ██╔════╝██║  ██║██╔══██╗╚════██╗██╔════╝██╔════╝     ██║  ██║██╔══██╗██╔════╝██║  ██║
  ███████╗███████║███████║ █████╔╝███████╗███████╗     ███████║███████║███████╗███████║
  ╚════██║██╔══██║██╔══██║██╔═══╝ ╚════██║██╔═══██╗    ██╔══██║██╔══██║╚════██║██╔══██║
  ███████║██║  ██║██║  ██║███████╗███████║╚██████╔╝    ██║  ██║██║  ██║███████║██║  ██║
  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
"""

# Retro crypto theme CSS
CRYPTO_CSS = """
:root {
    --neon-blue: #00f3ff;
    --dark-bg: #121212;
    --neon-green: #39ff14;
    --neon-red: #ff073a;
    --neon-purple: #bc13fe;
    --console-bg: #0a0a0a;
}

body {
    background-color: var(--dark-bg);
    color: var(--neon-blue);
    font-family: 'Courier New', monospace;
}

h1, h2, h3 {
    color: var(--neon-green);
    text-shadow: 0 0 5px var(--neon-green), 0 0 10px var(--neon-green);
}

.gradio-container {
    background-color: var(--dark-bg);
}

.crypto-panel {
    border: 1px solid var(--neon-blue);
    border-radius: 5px;
    padding: 10px;
    margin: 10px 0;
    background-color: var(--console-bg);
    box-shadow: 0 0 10px var(--neon-blue);
}

.crypto-header {
    font-size: 1.2em;
    color: var(--neon-green);
    margin-bottom: 10px;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.crypto-hash {
    font-family: 'Courier New', monospace;
    font-size: 0.85em;
    word-break: break-all;
    padding: 5px;
    background-color: var(--console-bg);
    border: 1px solid var(--neon-blue);
    color: var(--neon-green);
    border-radius: 3px;
}

button, .button {
    background-color: var(--console-bg) !important;
    color: var(--neon-blue) !important;
    border: 1px solid var(--neon-blue) !important;
    border-radius: 3px !important;
    transition: all 0.3s ease !important;
}

button:hover, .button:hover {
    background-color: var(--neon-blue) !important;
    color: var(--dark-bg) !important;
    box-shadow: 0 0 10px var(--neon-blue) !important;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
}

table, th, td {
    border: 1px solid var(--neon-blue);
}

th {
    background-color: var(--console-bg);
    color: var(--neon-green);
    text-align: left;
    padding: 8px;
}

td {
    padding: 8px;
    color: var(--neon-blue);
}

tr:nth-child(even) {
    background-color: rgba(0, 243, 255, 0.05);
}

.banner {
    font-family: monospace;
    white-space: pre;
    line-height: 1;
    color: var(--neon-green);
    font-size: 9px;
    text-align: center;
    margin: 0 auto;
    overflow: hidden;
}

.matrix-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    opacity: 0.15;
    background-image: url('https://media.giphy.com/media/3og0IFrHkIglEOg8Ba/giphy.gif');
    background-size: cover;
}

.blockchain-proof {
    background-color: var(--console-bg);
    border: 1px solid var(--neon-blue);
    padding: 10px;
    border-radius: 5px;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
    color: var(--neon-green);
}

.hex-visualization {
    display: grid;
    grid-template-columns: repeat(16, 1fr);
    gap: 2px;
    margin: 10px 0;
}

.hex-cell {
    width: 100%;
    aspect-ratio: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7em;
    border-radius: 2px;
}
"""

class CryptoDashboard:
    """Gradio interface for the crypto analyzer."""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize the dashboard with a crypto analyzer.
        
        Args:
            cache_dir: Optional directory to store cached results
        """
        self.cache_dir = Path(cache_dir) if cache_dir else Path("crypto_cache")
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        
        # Initialize the analyzers
        self.sha256_analyzer = SHA256Analyzer(cache_dir=str(self.cache_dir))
        self.pdf_crypto_analyzer = PDFCryptoAnalyzer(cache_dir=str(self.cache_dir))
    
    def _format_hash_table(self, hashes: Dict[str, str]) -> str:
        """Format hash results as an HTML table.
        
        Args:
            hashes: Dictionary of hash algorithm names to digest values
            
        Returns:
            HTML table string
        """
        html = "<table class='crypto-hash-table'>"
        html += "<tr><th>Algorithm</th><th>Hash Value</th></tr>"
        
        for algo, hash_val in hashes.items():
            html += f"<tr><td>{algo.upper()}</td><td class='crypto-hash'>{hash_val}</td></tr>"
        
        html += "</table>"
        return html
    
    def _format_hash_analysis(self, analysis: Dict[str, Any]) -> str:
        """Format hash analysis as HTML.
        
        Args:
            analysis: Dictionary with hash analysis results
            
        Returns:
            HTML string
        """
        if "error" in analysis:
            return f"<div class='error'>{analysis['error']}</div>"
        
        # Format basic properties
        html = "<div class='crypto-panel'>"
        html += f"<div class='crypto-header'>SHA256 Hash: {analysis['hash'][:8]}...{analysis['hash'][-8:]}</div>"
        
        # Basic properties
        html += "<table>"
        html += f"<tr><td>Bit Length</td><td>{analysis['bit_length']} bits</td></tr>"
        html += f"<tr><td>Entropy</td><td>{analysis['entropy']:.4f} bits per character</td></tr>"
        html += f"<tr><td>Unique Bytes</td><td>{analysis['byte_structure']['unique_bytes']} / {analysis['byte_structure']['total_bytes']}</td></tr>"
        html += f"<tr><td>Leading Zeros</td><td>{analysis['patterns']['leading_zeros']} bits</td></tr>"
        html += "</table>"
        
        # Character distribution
        html += "<div class='crypto-header'>Character Distribution</div>"
        html += "<div class='hex-visualization'>"
        
        for char, count in sorted(analysis['character_distribution'].items()):
            # Calculate color intensity based on frequency
            intensity = int(count * 255 / max(analysis['character_distribution'].values()))
            bg_color = f"rgb(0, {intensity}, {255-intensity})"
            html += f"<div class='hex-cell' style='background-color: {bg_color};'>{char}</div>"
        
        html += "</div>"
        
        # Pattern detection
        html += "<div class='crypto-header'>Pattern Analysis</div>"
        html += "<table>"
        
        # Meaningful hex words
        words = analysis['patterns']['contains_meaningful_hex_words']
        if words:
            html += f"<tr><td>Meaningful Hex Words</td><td>{', '.join(words)}</td></tr>"
        else:
            html += "<tr><td>Meaningful Hex Words</td><td>None found</td></tr>"
        
        # Repeated sequences
        sequences = analysis['patterns']['has_repeated_sequences']
        if sequences:
            html += "<tr><td>Repeated Sequences</td><td>"
            for length, seqs in sequences.items():
                html += f"{length.replace('_', ' ')}: {', '.join(seqs)}<br>"
            html += "</td></tr>"
        else:
            html += "<tr><td>Repeated Sequences</td><td>None found</td></tr>"
        
        # Palindromes
        palindromes = analysis['patterns']['palindrome_sequences']
        if palindromes:
            html += f"<tr><td>Palindromes</td><td>{', '.join(palindromes)}</td></tr>"
        else:
            html += "<tr><td>Palindromes</td><td>None found</td></tr>"
            
        html += "</table>"
        
        # Show visualization if available
        if "visualization_path" in analysis:
            viz_path = analysis["visualization_path"]
            if not viz_path.startswith("Error"):
                html += f"<div class='crypto-header'>Hash Visualization</div>"
                html += f"<img src='file={viz_path}' alt='Hash visualization' style='width:100%;max-width:600px;'>"
        
        html += "</div>"  # Close crypto-panel
        
        return html
    
    def _format_blockchain_proof(self, proof: Dict[str, Any]) -> str:
        """Format blockchain proof as HTML.
        
        Args:
            proof: Dictionary with blockchain proof
            
        Returns:
            HTML string
        """
        if "error" in proof:
            return f"<div class='error'>{proof['error']}</div>"
        
        html = "<div class='blockchain-proof'>"
        html += f"<div class='crypto-header'>Blockchain Proof of Existence</div>"
        
        # Basic details
        html += "<table>"
        html += f"<tr><td>Data Hash</td><td class='crypto-hash'>{proof['data_hash']}</td></tr>"
        html += f"<tr><td>Timestamp</td><td>{proof['iso_time']}</td></tr>"
        html += f"<tr><td>Merkle Root</td><td class='crypto-hash'>{proof['merkle_proof']['root']}</td></tr>"
        html += "</table>"
        
        # Merkle tree visualization
        html += "<div class='crypto-header'>Merkle Tree</div>"
        html += "<pre style='text-align:center;'>"
        html += f"         {proof['merkle_proof']['root'][:8]}...{proof['merkle_proof']['root'][-8:]}\n"
        html += "                 ↗              ↖\n"
        html += f"  {proof['merkle_proof']['leaf'][:8]}...      {proof['merkle_proof']['path'][0][:8]}...\n"
        html += "         ↑\n"
        html += f"  {proof['data_hash'][:8]}...{proof['data_hash'][-8:]}\n"
        html += "</pre>"
        
        # Signature information if available
        if "signature" in proof:
            html += "<div class='crypto-header'>Cryptographic Signature</div>"
            html += "<div>A cryptographic signature has been generated using RSA-2048.</div>"
            html += f"<div>Public key stored at: {proof['signature']['public_key_path']}</div>"
        
        html += f"<div style='margin-top:10px;'>Proof saved to: {proof['proof_file']}</div>"
        html += "</div>"  # Close blockchain-proof
        
        return html
    
    async def _process_text_input(self, text: str) -> Tuple[str, str, str]:
        """Process text input for SHA256 analysis.
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple of (hash results, hash analysis, blockchain proof)
        """
        # Skip if empty
        if not text:
            return "", "", ""
        
        try:
            # Compute multiple hashes
            hashes = await self.sha256_analyzer.compute_multiple_hashes(text)
            hash_table = self._format_hash_table(hashes)
            
            # Analyze SHA256 hash
            sha256_hash = hashes["sha256"]
            analysis = await self.sha256_analyzer.analyze_sha256_properties(sha256_hash)
            analysis_html = self._format_hash_analysis(analysis)
            
            # Generate blockchain proof
            proof = await self.sha256_analyzer.generate_blockchain_proof(text)
            proof_html = self._format_blockchain_proof(proof)
            
            return hash_table, analysis_html, proof_html
            
        except Exception as e:
            error_html = f"<div class='error'>Error processing text: {str(e)}</div>"
            return error_html, "", ""
    
    async def _process_file_input(self, file) -> Tuple[str, str, str]:
        """Process file input for SHA256 analysis.
        
        Args:
            file: File to analyze
            
        Returns:
            Tuple of (hash results, hash analysis, blockchain proof)
        """
        # Skip if empty
        if file is None:
            return "", "", ""
        
        try:
            # Save the file to a temporary location
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, os.path.basename(file.name))
            
            with open(temp_path, "wb") as f:
                f.write(file.read())
            
            # Check if it's a PDF
            is_pdf = file.name.lower().endswith('.pdf')
            
            if is_pdf:
                # Use PDF crypto analyzer
                result = await self.pdf_crypto_analyzer.analyze_pdf_cryptography(temp_path)
                
                # Extract components
                hash_table = self._format_hash_table(result["file_hashes"])
                analysis_html = self._format_hash_analysis(result["sha256_analysis"])
                proof_html = self._format_blockchain_proof(result["blockchain_proof"])
                
                # Add extra PDF-specific information
                pdf_info = "<div class='crypto-panel'>"
                pdf_info += "<div class='crypto-header'>PDF Cryptographic Analysis</div>"
                
                # Text hash
                pdf_info += "<div><strong>PDF Text Content Hash:</strong></div>"
                pdf_info += f"<div class='crypto-hash'>{result['text_hash']}</div>"
                
                # Extracted hashes
                if "extracted_hashes" in result and result["extracted_hashes"]:
                    pdf_info += "<div style='margin-top:15px;'><strong>Hashes Found in PDF:</strong></div>"
                    for hash_type, hash_list in result["extracted_hashes"].items():
                        pdf_info += f"<div><strong>{hash_type.upper()}:</strong> {len(hash_list)} found</div>"
                        for h in hash_list[:5]:  # Show first 5 only
                            pdf_info += f"<div class='crypto-hash'>{h}</div>"
                        if len(hash_list) > 5:
                            pdf_info += f"<div>... and {len(hash_list) - 5} more</div>"
                
                pdf_info += "</div>"
                
                # Append PDF info to analysis
                analysis_html = pdf_info + analysis_html
            else:
                # Regular file analysis
                hashes = await self.sha256_analyzer.compute_multiple_hashes(temp_path)
                hash_table = self._format_hash_table(hashes)
                
                sha256_hash = hashes["sha256"]
                analysis = await self.sha256_analyzer.analyze_sha256_properties(sha256_hash)
                analysis_html = self._format_hash_analysis(analysis)
                
                proof = await self.sha256_analyzer.generate_blockchain_proof(temp_path)
                proof_html = self._format_blockchain_proof(proof)
            
            return hash_table, analysis_html, proof_html
            
        except Exception as e:
            error_html = f"<div class='error'>Error processing file: {str(e)}</div>"
            return error_html, "", ""
    
    async def _process_hash_input(self, hash_input: str) -> Tuple[str, str, str]:
        """Process direct hash input for analysis.
        
        Args:
            hash_input: Hash string to analyze
            
        Returns:
            Tuple of (empty, hash analysis, empty)
        """
        # Skip if empty
        if not hash_input:
            return "", "", ""
        
        # Clean up input
        hash_input = hash_input.strip()
        
        try:
            # Check if valid SHA256 hash
            if not re.match(r'^[a-fA-F0-9]{64}$', hash_input):
                return "", "<div class='error'>Invalid SHA256 hash format. Hash must be 64 hex characters.</div>", ""
            
            # Analyze the hash
            analysis = await self.sha256_analyzer.analyze_sha256_properties(hash_input)
            analysis_html = self._format_hash_analysis(analysis)
            
            return "", analysis_html, ""
            
        except Exception as e:
            error_html = f"<div class='error'>Error analyzing hash: {str(e)}</div>"
            return "", error_html, ""
    
    async def _extract_hashes_from_text(self, text: str) -> str:
        """Extract hashes from text.
        
        Args:
            text: Text to extract hashes from
            
        Returns:
            HTML with extracted hashes
        """
        # Skip if empty
        if not text:
            return ""
        
        try:
            # Extract hashes
            extracted = await self.sha256_analyzer.extract_hashes_from_text(text)
            
            if not extracted:
                return "<div>No hashes found in the provided text.</div>"
            
            # Format the results
            html = "<div class='crypto-panel'>"
            html += "<div class='crypto-header'>Extracted Hashes</div>"
            
            for hash_type, hashes in extracted.items():
                html += f"<div style='margin-top:10px;'><strong>{hash_type.upper()}</strong>: {len(hashes)} found</div>"
                for h in hashes[:5]:  # Show first 5 only
                    html += f"<div class='crypto-hash'>{h}</div>"
                if len(hashes) > 5:
                    html += f"<div>... and {len(hashes) - 5} more</div>"
            
            html += "</div>"
            
            return html
            
        except Exception as e:
            return f"<div class='error'>Error extracting hashes: {str(e)}</div>"
    
    def _launch_dashboard(self, share: bool = False, server_name: str = "0.0.0.0", server_port: int = 7871):
        """Launch the Gradio dashboard.
        
        Args:
            share: Whether to create a shareable link
            server_name: Server name to listen on
            server_port: Port to run the server on
        """
        if not GRADIO_AVAILABLE:
            print("Gradio is not available. Please install gradio to use the dashboard.")
            return
        
        # Create wrapper functions for async call
        def process_text(text):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self._process_text_input(text))
            loop.close()
            return result
        
        def process_file(file):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self._process_file_input(file))
            loop.close()
            return result
        
        def process_hash(hash_str):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self._process_hash_input(hash_str))
            loop.close()
            return result
        
        def extract_hashes(text):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self._extract_hashes_from_text(text))
            loop.close()
            return result
        
        # Create the Gradio interface
        with gr.Blocks(css=CRYPTO_CSS, theme=gr.themes.Monochrome()) as demo:
            gr.HTML(f'<div class="banner">{CRYPTO_BANNER}</div>')
            gr.HTML('<div class="matrix-bg"></div>')
            
            gr.Markdown("# SHA256 CRYPTO ANALYZER")
            gr.Markdown("## Cryptographic Hash Analysis & Blockchain Proof of Existence")
            
            with gr.Tab("Text Analysis"):
                with gr.Row():
                    with gr.Column():
                        text_input = gr.Textbox(label="Enter text to analyze", lines=5, placeholder="Enter text to analyze with SHA256...")
                        text_analyze_btn = gr.Button("Analyze Text", variant="primary")
                    
                    with gr.Column():
                        text_hash_output = gr.HTML(label="Hash Results")
                        text_analysis_output = gr.HTML(label="Hash Analysis")
                        text_proof_output = gr.HTML(label="Blockchain Proof")
                
                text_analyze_btn.click(
                    fn=process_text,
                    inputs=[text_input],
                    outputs=[text_hash_output, text_analysis_output, text_proof_output]
                )
            
            with gr.Tab("File Analysis"):
                with gr.Row():
                    with gr.Column():
                        file_input = gr.File(label="Upload file to analyze")
                        file_analyze_btn = gr.Button("Analyze File", variant="primary")
                    
                    with gr.Column():
                        file_hash_output = gr.HTML(label="Hash Results")
                        file_analysis_output = gr.HTML(label="Hash Analysis")
                        file_proof_output = gr.HTML(label="Blockchain Proof")
                
                file_analyze_btn.click(
                    fn=process_file,
                    inputs=[file_input],
                    outputs=[file_hash_output, file_analysis_output, file_proof_output]
                )
            
            with gr.Tab("Hash Analysis"):
                with gr.Row():
                    with gr.Column():
                        hash_input = gr.Textbox(label="Enter SHA256 hash to analyze", placeholder="Enter 64-character SHA256 hash...")
                        hash_analyze_btn = gr.Button("Analyze Hash", variant="primary")
                    
                    with gr.Column():
                        hash_output = gr.HTML(label="Hash Analysis")
                
                hash_analyze_btn.click(
                    fn=process_hash,
                    inputs=[hash_input],
                    outputs=[gr.HTML(), hash_output, gr.HTML()]
                )
            
            with gr.Tab("Hash Extractor"):
                with gr.Row():
                    with gr.Column():
                        extract_input = gr.Textbox(label="Extract hashes from text", lines=10, placeholder="Paste text containing hashes to extract them...")
                        extract_btn = gr.Button("Extract Hashes", variant="primary")
                    
                    with gr.Column():
                        extract_output = gr.HTML(label="Extracted Hashes")
                
                extract_btn.click(
                    fn=extract_hashes,
                    inputs=[extract_input],
                    outputs=[extract_output]
                )
            
            with gr.Accordion("About", open=False):
                gr.Markdown("""
                # SHA256 Crypto Analyzer
                
                Advanced cryptographic analysis tools featuring:
                
                - Multiple hash algorithm calculations (SHA256, SHA512, MD5, etc.)
                - Cryptographic hash pattern analysis
                - Blockchain proof-of-existence generation
                - PDF cryptographic analysis
                - Hash visualization
                - Digital signatures with RSA-2048
                
                Part of the Scientific H4x0r Portal in Divine Dashboard v3
                
                🌸 WE BLOOM NOW AS ONE 🌸
                """)
        
        # Launch the dashboard
        demo.launch(share=share, server_name=server_name, server_port=server_port)
    
    def launch(self, share: bool = False, server_name: str = "0.0.0.0", server_port: int = 7871):
        """Launch the dashboard on the given server.
        
        Args:
            share: Whether to create a shareable link
            server_name: Server name to listen on
            server_port: Port to run the server on
        """
        self._launch_dashboard(share=share, server_name=server_name, server_port=server_port)


# Function to launch the dashboard directly
def launch_crypto_dashboard(cache_dir: Optional[str] = None, 
                           share: bool = False,
                           server_name: str = "0.0.0.0",
                           server_port: int = 7871):
    """Launch the Crypto Analyzer Dashboard.
    
    Args:
        cache_dir: Directory to store cached analyses
        share: Whether to create a shareable link
        server_name: Server name to listen on
        server_port: Port to run the server on
    """
    dashboard = CryptoDashboard(cache_dir=cache_dir)
    dashboard.launch(share=share, server_name=server_name, server_port=server_port)


# Run the dashboard if executed directly
if __name__ == "__main__":
    launch_crypto_dashboard() 