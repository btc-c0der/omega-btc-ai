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
H4x0r PDF Analyzer Dashboard

Gradio-based interface for analyzing cybersecurity PDFs using the advanced PDF extraction,
analysis, and metadata parsing tool for cybersecurity research.
"""

import os
import json
import time
import asyncio
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

import gradio as gr
from .pdf_analyzer import PDFAnalyzer, SecurityPaperAnalyzer

# ASCII Art Banner
H4X0R_BANNER = """
  ██╗  ██╗██╗  ██╗██╗  ██╗ ██████╗ ██████╗     ██████╗ ██████╗ ███████╗
  ██║  ██║██║  ██║╚██╗██╔╝██╔═══██╗██╔══██╗    ██╔══██╗██╔══██╗██╔════╝
  ███████║███████║ ╚███╔╝ ██║   ██║██████╔╝    ██████╔╝██║  ██║█████╗  
  ██╔══██║╚════██║ ██╔██╗ ██║   ██║██╔══██╗    ██╔═══╝ ██║  ██║██╔══╝  
  ██║  ██║     ██║██╔╝ ██╗╚██████╔╝██║  ██║    ██║     ██████╔╝██║     
  ╚═╝  ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝    ╚═╝     ╚═════╝ ╚═╝     
  ██████╗ ██████╗ ███████╗     █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗███████╗███████╗██████╗ 
  ██╔══██╗██╔══██╗██╔════╝    ██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝╚══███╔╝██╔════╝██╔══██╗
  ██████╔╝██║  ██║█████╗      ███████║██╔██╗ ██║███████║██║   ╚████╔╝   ███╔╝ █████╗  ██████╔╝
  ██╔═══╝ ██║  ██║██╔══╝      ██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝   ███╔╝  ██╔══╝  ██╔══██╗
  ██║     ██████╔╝██║         ██║  ██║██║ ╚████║██║  ██║███████╗██║   ███████╗███████╗██║  ██║
  ╚═╝     ╚═════╝ ╚═╝         ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝
"""

# Default CSS for retro hacker aesthetic
CSS = """
:root {
    --primary-color: #00ff00;
    --background-color: #111111;
    --secondary-background: #222222;
    --text-color: #00ff00;
    --header-color: #ff3300;
    --border-color: #00ff00;
}

body {
    background-color: var(--background-color);
    color: var(--text-color);
    font-family: 'Courier New', monospace;
}

h1, h2, h3 {
    color: var(--header-color);
    text-shadow: 0 0 5px var(--header-color);
}

.gradio-container {
    background-color: var(--background-color);
}

.prose {
    color: var(--text-color);
}

button, .button {
    background-color: var(--secondary-background) !important;
    color: var(--primary-color) !important;
    border: 1px solid var(--border-color) !important;
    box-shadow: 0 0 5px var(--border-color) !important;
}

button:hover, .button:hover {
    background-color: var(--border-color) !important;
    color: var(--background-color) !important;
}

input, textarea, select {
    background-color: var(--secondary-background) !important;
    color: var(--text-color) !important;
    border: 1px solid var(--border-color) !important;
}

table {
    background-color: var(--secondary-background);
    color: var(--text-color);
    border: 1px solid var(--border-color);
}

pre {
    background-color: var(--secondary-background);
    color: var(--primary-color);
    border: 1px solid var(--border-color);
    padding: 10px;
    overflow-x: auto;
}

.banner {
    font-family: monospace;
    white-space: pre;
    line-height: 1;
    color: var(--primary-color);
    font-size: 10px;
    text-align: center;
    margin: 0 auto;
    overflow: hidden;
}

.status {
    color: var(--primary-color);
    border: 1px solid var(--border-color);
    padding: 10px;
    background-color: var(--secondary-background);
    font-family: 'Courier New', monospace;
    margin-top: 10px;
}

.matrix-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    opacity: 0.1;
    background-image: url('https://media.giphy.com/media/l4Epf0KwYUQY5DcGc/giphy.gif');
    background-size: cover;
}
"""

class PDFAnalyzerDashboard:
    """Gradio interface for the PDF Analyzer component."""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize the dashboard with an analyzer.
        
        Args:
            cache_dir: Optional directory to store cached PDF analyses
        """
        self.cache_dir = Path(cache_dir) if cache_dir else Path("pdf_cache")
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        
        # Initialize analyzers
        self.pdf_analyzer = PDFAnalyzer(cache_dir=str(self.cache_dir))
        self.security_analyzer = SecurityPaperAnalyzer(cache_dir=str(self.cache_dir))
        
        # Track the latest analysis result
        self.latest_result = None
        self.latest_pdf_path = None
    
    def _format_security_score(self, score: float) -> str:
        """Format a security score with H4X0R-style rating."""
        if score >= 80:
            return f"[H1GH S3CUR1TY R3L3V4NC3] Score: {score}/100 🔥"
        elif score >= 50:
            return f"[M0D3R4T3 S3CUR1TY R3L3V4NC3] Score: {score}/100 ⚠️"
        else:
            return f"[L0W S3CUR1TY R3L3V4NC3] Score: {score}/100 ℹ️"
    
    def _format_analysis_result(self, result: Dict[str, Any]) -> str:
        """Format the analysis result in a h4x0r-style output."""
        if not result or "error" in result:
            return f"[ERR0R] {result.get('error', 'Unknown error occurred')}"
        
        formatted = []
        formatted.append("==== PDF 4N4LYS1S R3P0RT ====")
        formatted.append("")
        
        # Add metadata
        meta = result.get("metadata", {})
        formatted.append("[M3T4D4T4]")
        for key, val in meta.items():
            formatted.append(f"  {key}: {val}")
        formatted.append("")
        
        # Add security indicators
        indicators = result.get("security_indicators", {})
        if indicators:
            score = indicators.get("security_score", 0)
            formatted.append(self._format_security_score(score))
            formatted.append("")
            
            # Add CVEs
            cves = indicators.get("cves", [])
            if cves:
                formatted.append(f"[CVEs D3T3CT3D] {len(cves)} found")
                for cve in cves[:10]:  # Limit to 10
                    formatted.append(f"  {cve}")
                if len(cves) > 10:
                    formatted.append(f"  ... and {len(cves) - 10} more")
                formatted.append("")
            
            # Add security keywords
            keywords = indicators.get("security_keywords", [])
            if keywords:
                formatted.append(f"[S3CUR1TY K3YW0RDS] {len(keywords)} found")
                formatted.append(f"  {', '.join(keywords)}")
                formatted.append("")
        
        # Add defacement analysis
        defacement = result.get("defacement_analysis", {})
        if defacement:
            is_defacement = defacement.get("is_defacement_related", False)
            score = defacement.get("defacement_relevance_score", 0)
            
            if is_defacement:
                formatted.append(f"[D3F4C3M3NT R3L4T3D] Score: {score}/100 🔴")
            else:
                formatted.append(f"[N0T D3F4C3M3NT R3L4T3D] Score: {score}/100")
            
            crews = defacement.get("mentioned_crews", [])
            if crews:
                formatted.append(f"[H4CK3R CR3WS M3NT10N3D]")
                formatted.append(f"  {', '.join(crews)}")
            
            years = defacement.get("relevant_years", [])
            if years:
                formatted.append(f"[R3L3V4NT Y34RS]")
                formatted.append(f"  {', '.join(years)}")
            
            formatted.append("")
        
        # Add defacement statistics if available
        stats = result.get("defacement_statistics", {})
        if stats:
            formatted.append("[D3F4C3M3NT ST4T1ST1CS]")
            
            # Show defacement counts
            counts = stats.get("defacement_counts", [])
            if counts:
                formatted.append(f"  Defacement Counts: {', '.join(map(str, counts))}")
            
            # Show top countries
            countries = stats.get("top_countries", [])
            if countries:
                formatted.append("  Top Countries:")
                for country, count in countries:
                    formatted.append(f"    {country}: {count} mentions")
            
            formatted.append("")
        
        # Add text statistics
        text_stats = result.get("text_statistics", {})
        if text_stats:
            word_count = text_stats.get("word_count", 0)
            sentence_count = text_stats.get("sentence_count", 0)
            formatted.append("[T3XT ST4T1ST1CS]")
            formatted.append(f"  Words: {word_count}")
            formatted.append(f"  Sentences: {sentence_count}")
            
            # Add top words if available (limit to 10)
            top_words = text_stats.get("top_words", {})
            if top_words:
                formatted.append("  Top Words:")
                for i, (word, count) in enumerate(list(top_words.items())[:10]):
                    formatted.append(f"    {word}: {count} occurrences")
            
            formatted.append("")
        
        formatted.append("==== 3ND 0F R3P0RT ====")
        
        return "\n".join(formatted)
    
    async def _process_uploaded_file(self, file) -> Tuple[str, str]:
        """Process an uploaded PDF file.
        
        Args:
            file: The uploaded file object
            
        Returns:
            Tuple of (status message, analysis report)
        """
        if file is None:
            return "No file uploaded", ""
        
        try:
            # Save the file
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, os.path.basename(file.name))
            
            with open(temp_path, "wb") as f:
                f.write(file.read())
            
            # Store the path for later
            self.latest_pdf_path = temp_path
            
            # Analyze the file
            status_msg = "Analyzing PDF..."
            result = await self.security_analyzer.extract_defacement_statistics(temp_path)
            
            # Store result
            self.latest_result = result
            
            # Format and return the result
            status_msg = "Analysis complete"
            return status_msg, self._format_analysis_result(result)
            
        except Exception as e:
            return f"Error: {str(e)}", ""
    
    async def _process_pdf_url(self, url: str) -> Tuple[str, str]:
        """Process a PDF from a URL.
        
        Args:
            url: The URL to the PDF file
            
        Returns:
            Tuple of (status message, analysis report)
        """
        if not url:
            return "No URL provided", ""
        
        if not url.lower().endswith('.pdf') and not '?pdf=' in url.lower():
            return "URL does not appear to point to a PDF file", ""
        
        try:
            # Download and analyze
            status_msg = "Downloading and analyzing PDF..."
            result = await self.pdf_analyzer.download_and_analyze_pdf(url)
            
            if "error" in result:
                return f"Error: {result['error']}", ""
            
            # Get the downloaded path
            self.latest_pdf_path = result.get("local_path")
            
            # Perform defacement analysis
            result = await self.security_analyzer.extract_defacement_statistics(self.latest_pdf_path)
            
            # Store result
            self.latest_result = result
            
            # Format and return the result
            status_msg = "Analysis complete"
            return status_msg, self._format_analysis_result(result)
            
        except Exception as e:
            return f"Error: {str(e)}", ""
    
    def _launch_dashboard(self, share: bool = False, server_name: str = "0.0.0.0"):
        """Launch the Gradio dashboard.
        
        Args:
            share: Whether to create a shareable link
            server_name: Server name to listen on
        """
        # Create wrapper functions for async call
        def upload_and_analyze(file):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            status, report = loop.run_until_complete(self._process_uploaded_file(file))
            loop.close()
            return status, report
        
        def url_analyze(url):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            status, report = loop.run_until_complete(self._process_pdf_url(url))
            loop.close()
            return status, report
        
        # Create the Gradio interface
        with gr.Blocks(css=CSS, theme=gr.themes.Monochrome()) as demo:
            gr.HTML(f'<div class="banner">{H4X0R_BANNER}</div>')
            gr.HTML('<div class="matrix-bg"></div>')
            
            gr.Markdown("# H4X0R PDF 4N4LYZ3R")
            gr.Markdown("## Extract cybersecurity insights from research papers")
            
            with gr.Tab("Upload PDF"):
                with gr.Row():
                    with gr.Column():
                        file_input = gr.File(label="Upload PDF File")
                        analyze_btn = gr.Button("4N4LYZ3 PDF", variant="primary")
                    
                    with gr.Column():
                        status_output = gr.Textbox(label="Status", value="Ready", elem_classes=["status"])
                        report_output = gr.Textbox(label="Analysis Report", lines=20, elem_classes=["report"])
                
                analyze_btn.click(
                    fn=upload_and_analyze,
                    inputs=[file_input],
                    outputs=[status_output, report_output]
                )
            
            with gr.Tab("PDF URL"):
                with gr.Row():
                    with gr.Column():
                        url_input = gr.Textbox(label="PDF URL", placeholder="https://example.com/paper.pdf")
                        url_btn = gr.Button("4N4LYZ3 URL", variant="primary")
                    
                    with gr.Column():
                        url_status_output = gr.Textbox(label="Status", value="Ready", elem_classes=["status"])
                        url_report_output = gr.Textbox(label="Analysis Report", lines=20, elem_classes=["report"])
                
                url_btn.click(
                    fn=url_analyze,
                    inputs=[url_input],
                    outputs=[url_status_output, url_report_output]
                )
            
            with gr.Accordion("About", open=False):
                gr.Markdown("""
                # H4X0R PDF 4N4LYZ3R
                
                Advanced cybersecurity research paper analyzer that extracts:
                
                - Security indicators and CVEs
                - Website defacement statistics
                - Hacker crew mentions
                - Technical intelligence
                
                Part of the Divine Dashboard v3 - Hacker Archives module
                
                🌸 WE BLOOM NOW AS ONE 🌸
                """)
        
        # Launch the dashboard
        demo.launch(share=share, server_name=server_name)
    
    def launch(self, share: bool = False, server_name: str = "0.0.0.0"):
        """Launch the dashboard on the given server.
        
        Args:
            share: Whether to create a shareable link
            server_name: Server name to listen on
        """
        self._launch_dashboard(share=share, server_name=server_name)


# Function to launch the dashboard directly
def launch_pdf_analyzer_dashboard(cache_dir: Optional[str] = None, 
                                 share: bool = False,
                                 server_name: str = "0.0.0.0"):
    """Launch the PDF Analyzer Dashboard.
    
    Args:
        cache_dir: Directory to store cached PDF analyses
        share: Whether to create a shareable link
        server_name: Server name to listen on
    """
    dashboard = PDFAnalyzerDashboard(cache_dir=cache_dir)
    dashboard.launch(share=share, server_name=server_name)


# Run the dashboard if executed directly
if __name__ == "__main__":
    launch_pdf_analyzer_dashboard() 