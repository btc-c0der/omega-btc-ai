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
Demo PDF Analyzer

Simple demonstration of the PDF analyzer for cybersecurity research papers.
"""

import os
import asyncio
import json
from pathlib import Path

# Import the PDF analyzer components
try:
    from pdf_analyzer import PDFAnalyzer, SecurityPaperAnalyzer
    ANALYZER_AVAILABLE = True
except ImportError:
    print("PDF Analyzer not available. Please install required dependencies.")
    ANALYZER_AVAILABLE = False

# ANSI colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Sample defacement research paper URL
SAMPLE_PDF_URL = "https://maggi.cc/publication/maggi_defplorex_2018/maggi_defplorex_2018.pdf"

async def run_demo():
    """Run a demonstration of the PDF analyzer."""
    if not ANALYZER_AVAILABLE:
        return
    
    print(f"{CYAN}=== Scientific H4x0r PDF Analyzer Demo ==={RESET}")
    print(f"{YELLOW}Analyzing defacement research paper: {SAMPLE_PDF_URL}{RESET}")
    print()
    
    # Create cache directory
    cache_dir = Path("pdf_cache")
    cache_dir.mkdir(exist_ok=True, parents=True)
    
    # Initialize analyzers
    pdf_analyzer = PDFAnalyzer(cache_dir=str(cache_dir))
    security_analyzer = SecurityPaperAnalyzer(cache_dir=str(cache_dir))
    
    try:
        # Step 1: Download and analyze the PDF
        print(f"{BLUE}[1/3] Downloading and analyzing PDF...{RESET}")
        result = await pdf_analyzer.download_and_analyze_pdf(SAMPLE_PDF_URL)
        
        if "error" in result:
            print(f"{RED}Error downloading PDF: {result['error']}{RESET}")
            return
        
        # Get the local path
        local_path = result.get("local_path")
        if not local_path or not os.path.exists(local_path):
            print(f"{RED}Error: Downloaded PDF not found{RESET}")
            return
        
        print(f"{GREEN}PDF downloaded successfully to: {local_path}{RESET}")
        
        # Step 2: Extract metadata
        print(f"{BLUE}[2/3] Extracting metadata...{RESET}")
        metadata = result.get("metadata", {})
        
        print(f"{GREEN}Title: {metadata.get('title', 'Unknown')}{RESET}")
        print(f"{GREEN}Author: {metadata.get('author', 'Unknown')}{RESET}")
        print(f"{GREEN}Pages: {metadata.get('page_count', 'Unknown')}{RESET}")
        print()
        
        # Step 3: Analyze for defacement content
        print(f"{BLUE}[3/3] Analyzing for defacement content...{RESET}")
        defacement_result = await security_analyzer.analyze_security_paper(local_path)
        
        # Print defacement analysis
        defacement = defacement_result.get("defacement_analysis", {})
        if defacement:
            score = defacement.get("defacement_relevance_score", 0)
            is_related = defacement.get("is_defacement_related", False)
            
            print(f"{MAGENTA}Defacement relevance score: {score}/100{RESET}")
            print(f"{MAGENTA}Is defacement related: {'Yes' if is_related else 'No'}{RESET}")
            
            crews = defacement.get("mentioned_crews", [])
            if crews:
                print(f"{MAGENTA}Mentioned hacker crews: {', '.join(crews)}{RESET}")
            
            years = defacement.get("relevant_years", [])
            if years:
                print(f"{MAGENTA}Relevant years: {', '.join(years)}{RESET}")
        
        # Print security indicators
        indicators = result.get("security_indicators", {})
        if indicators:
            score = indicators.get("security_score", 0)
            print(f"{YELLOW}Security relevance score: {score}/100{RESET}")
            
            cves = indicators.get("cves", [])
            if cves:
                print(f"{YELLOW}CVEs detected: {len(cves)}{RESET}")
                for cve in cves[:5]:  # Limit to 5
                    print(f"{YELLOW}  - {cve}{RESET}")
        
        # Save the full result to a JSON file
        with open(cache_dir / "demo_result.json", "w") as f:
            json.dump(defacement_result, f, indent=2)
        
        print()
        print(f"{GREEN}Full analysis saved to: {cache_dir / 'demo_result.json'}{RESET}")
        print(f"{CYAN}=== Demo Completed Successfully ==={RESET}")
    
    except Exception as e:
        print(f"{RED}Error during analysis: {str(e)}{RESET}")

if __name__ == "__main__":
    asyncio.run(run_demo()) 