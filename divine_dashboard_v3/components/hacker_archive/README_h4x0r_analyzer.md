# 🔬 Scientific H4x0r PDF Analyzer 🔬

Advanced PDF analysis toolkit for cybersecurity research papers and website defacement analysis.

## Features

- 📄 PDF metadata extraction
- 🔍 Defacement indicator analysis
- 🛡️ Security relevance scoring
- 👥 Hacker crew detection
- 📊 Text statistics
- 🌐 URL downloading and caching
- 🤖 AI-powered analysis (with optional LLM support)

## Components

- **PDFAnalyzer**: Core PDF processing and metadata extraction
- **SecurityPaperAnalyzer**: Specialized analysis for defacement research papers
- **AISecurityAnalyzer**: LLM-powered analysis with multiple backend options
- **PDFAnalyzerDashboard**: Gradio web interface for interactive analysis

## Usage

```python
import asyncio
from pdf_analyzer import PDFAnalyzer, SecurityPaperAnalyzer

async def analyze_defacement_paper(url):
    """Analyze a defacement research paper from a URL."""
    analyzer = PDFAnalyzer(cache_dir="pdf_cache")
    security_analyzer = SecurityPaperAnalyzer(cache_dir="pdf_cache")
    
    # Download and analyze the PDF
    result = await analyzer.download_and_analyze_pdf(url)
    
    # Check if the paper is related to defacements
    if result.get("local_path"):
        analysis = await security_analyzer.analyze_security_paper(result["local_path"])
        return analysis
    
    return result

# Run with asyncio
result = asyncio.run(analyze_defacement_paper("https://example.com/paper.pdf"))
```

## Running the Demo

```bash
python demo_pdf_analyzer.py
```

## Running the Web Interface

```bash
python -m launch_scientific_h4x0r_portal
```

## Requirements

- PyPDF2: PDF parsing and extraction
- NLTK: Text analysis and statistics
- aiohttp: Asynchronous HTTP requests
- Gradio: Web interface
- (Optional) PyTorch + Transformers: For local LLM support
- (Optional) OpenAI API: For OpenAI integration
- (Optional) Hugging Face Hub: For Hugging Face model integration

✨ GBU2™ License - Consciousness Level 9 🧬
