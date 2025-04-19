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
Scientific H4x0r PDF Analyzer

Advanced PDF extraction, analysis, and metadata parsing tool for cybersecurity research.
Extracts text, metadata, and security indicators from academic papers and reports.
"""

import os
import re
import io
import json
import hashlib
import logging
import asyncio
import tempfile
from typing import Dict, Any, List, Optional, Tuple, Union
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

try:
    import PyPDF2
    from PyPDF2 import PdfReader
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.corpus import stopwords
    NLTK_SUPPORT = True
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
except ImportError:
    NLTK_SUPPORT = False

# Configure logging
logger = logging.getLogger(__name__)

class PDFAnalyzer:
    """Scientific PDF Analyzer for cybersecurity research papers."""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize the PDF Analyzer.
        
        Args:
            cache_dir: Directory to store processed PDF data
        """
        self.cache_dir = Path(cache_dir) if cache_dir else Path("pdf_cache")
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        
        # Check for required libraries
        if not PDF_SUPPORT:
            logger.warning("PyPDF2 not installed. Install with: pip install PyPDF2")
        if not NLTK_SUPPORT:
            logger.warning("NLTK not installed. Install with: pip install nltk")
        
        # Initialize pattern matchers
        self.url_pattern = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
        self.ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
        self.email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        self.cvss_pattern = re.compile(r'CVSS:3\.\d/AV:[NALP]/AC:[LH]/PR:[NLH]/UI:[NR]/S:[UC]/C:[NLH]/I:[NLH]/A:[NLH]')
        self.cve_pattern = re.compile(r'CVE-\d{4}-\d{4,}')
        
        # Keywords for cybersecurity relevance
        self.security_keywords = [
            'vulnerability', 'exploit', 'breach', 'attack', 'malware', 
            'ransomware', 'phishing', 'botnet', 'backdoor', 'trojan',
            'zero-day', 'rootkit', 'worm', 'ddos', 'injection', 'xss',
            'csrf', 'spoofing', 'mitm', 'metasploit', 'kali', 'pentest'
        ]

    async def extract_text_from_pdf(self, pdf_path: Union[str, Path, io.BytesIO]) -> str:
        """Extract text content from a PDF file.
        
        Args:
            pdf_path: Path to PDF file or BytesIO object
            
        Returns:
            Extracted text content
        """
        if not PDF_SUPPORT:
            raise ImportError("PyPDF2 is required for PDF processing")
        
        try:
            # Handle different input types
            if isinstance(pdf_path, (str, Path)):
                reader = PdfReader(str(pdf_path))
            else:
                reader = PdfReader(pdf_path)
            
            # Extract text from all pages
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n\n"
            
            return text
        
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return ""

    async def extract_metadata(self, pdf_path: Union[str, Path, io.BytesIO]) -> Dict[str, Any]:
        """Extract metadata from a PDF file.
        
        Args:
            pdf_path: Path to PDF file or BytesIO object
            
        Returns:
            Dictionary of metadata
        """
        if not PDF_SUPPORT:
            raise ImportError("PyPDF2 is required for PDF processing")
        
        try:
            # Handle different input types
            if isinstance(pdf_path, (str, Path)):
                reader = PdfReader(str(pdf_path))
            else:
                reader = PdfReader(pdf_path)
            
            # Extract metadata
            info = reader.metadata
            if info:
                metadata = {
                    "title": info.title if info.title else None,
                    "author": info.author if info.author else None, 
                    "subject": info.subject if info.subject else None,
                    "creator": info.creator if info.creator else None,
                    "producer": info.producer if info.producer else None,
                    "creation_date": info.creation_date.strftime("%Y-%m-%d %H:%M:%S") if info.creation_date else None,
                    "modification_date": info.modification_date.strftime("%Y-%m-%d %H:%M:%S") if info.modification_date else None,
                    "page_count": len(reader.pages),
                }
                return {k: v for k, v in metadata.items() if v is not None}
            
            return {"page_count": len(reader.pages)}
            
        except Exception as e:
            logger.error(f"Error extracting metadata from PDF: {e}")
            return {}

    async def analyze_security_indicators(self, text: str) -> Dict[str, Any]:
        """Analyze text for cybersecurity indicators.
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dictionary with security indicators
        """
        if not text:
            return {}
            
        try:
            # Extract URLs
            urls = self.url_pattern.findall(text)
            
            # Extract IP addresses
            ips = self.ip_pattern.findall(text)
            
            # Extract email addresses
            emails = self.email_pattern.findall(text)
            
            # Extract CVSS strings
            cvss_strings = self.cvss_pattern.findall(text)
            
            # Extract CVEs
            cves = self.cve_pattern.findall(text)
            
            # Check for security keywords
            keyword_matches = []
            for keyword in self.security_keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text.lower()):
                    keyword_matches.append(keyword)
            
            # Calculate security relevance score (0-100)
            score_factors = [
                len(urls) * 2,
                len(ips) * 3,
                len(emails) * 1,
                len(cvss_strings) * 10,
                len(cves) * 8,
                len(keyword_matches) * 5
            ]
            
            max_score = 100
            raw_score = sum(score_factors)
            security_score = min(raw_score, max_score)
            
            return {
                "urls": urls[:50],  # Limit to first 50
                "ip_addresses": ips[:30],
                "email_addresses": emails[:20],
                "cvss_strings": cvss_strings,
                "cves": cves,
                "security_keywords": keyword_matches,
                "security_score": security_score
            }
            
        except Exception as e:
            logger.error(f"Error analyzing security indicators: {e}")
            return {}

    async def generate_text_statistics(self, text: str) -> Dict[str, Any]:
        """Generate statistics about the text content.
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dictionary with text statistics
        """
        if not text or not NLTK_SUPPORT:
            return {}
        
        try:
            # Tokenize text
            sentences = sent_tokenize(text)
            words = word_tokenize(text)
            
            # Remove stopwords
            stop_words = set(stopwords.words('english'))
            filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
            
            # Calculate statistics
            word_count = len(words)
            sentence_count = len(sentences)
            avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
            
            # Word frequency
            word_freq = {}
            for word in filtered_words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Get top words
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:30]
            
            return {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "avg_sentence_length": round(avg_sentence_length, 2),
                "top_words": dict(top_words)
            }
            
        except Exception as e:
            logger.error(f"Error generating text statistics: {e}")
            return {}

    async def analyze_pdf(self, 
                         pdf_path: Union[str, Path, io.BytesIO],
                         extract_text: bool = True,
                         analyze_indicators: bool = True,
                         generate_stats: bool = True) -> Dict[str, Any]:
        """Perform comprehensive analysis of a PDF file.
        
        Args:
            pdf_path: Path to PDF file or BytesIO object
            extract_text: Whether to extract text content
            analyze_indicators: Whether to analyze security indicators
            generate_stats: Whether to generate text statistics
            
        Returns:
            Dictionary with analysis results
        """
        # Generate a hash for the PDF for caching
        pdf_hash = None
        if isinstance(pdf_path, (str, Path)):
            with open(pdf_path, 'rb') as f:
                pdf_hash = hashlib.md5(f.read()).hexdigest()
        
        # Check cache if hash is available
        if pdf_hash:
            cache_file = self.cache_dir / f"{pdf_hash}.json"
            if cache_file.exists():
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except Exception:
                    pass
        
        # Start with metadata extraction
        metadata = await self.extract_metadata(pdf_path)
        
        # Extract text if requested
        text_content = ""
        if extract_text:
            text_content = await self.extract_text_from_pdf(pdf_path)
        
        results = {
            "metadata": metadata,
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        # Add text content if extracted
        if text_content and extract_text:
            # Store only the first 10K characters in the results
            results["text_sample"] = text_content[:10000] + "..." if len(text_content) > 10000 else text_content
            
            # Analyze security indicators if requested
            if analyze_indicators:
                indicators = await self.analyze_security_indicators(text_content)
                results["security_indicators"] = indicators
            
            # Generate text statistics if requested
            if generate_stats and NLTK_SUPPORT:
                stats = await self.generate_text_statistics(text_content)
                results["text_statistics"] = stats
        
        # Cache results if we have a hash
        if pdf_hash:
            try:
                with open(self.cache_dir / f"{pdf_hash}.json", 'w') as f:
                    json.dump(results, f, indent=2)
            except Exception as e:
                logger.error(f"Error caching analysis results: {e}")
        
        return results

    async def download_and_analyze_pdf(self, url: str) -> Dict[str, Any]:
        """Download and analyze a PDF from a URL.
        
        Args:
            url: URL of the PDF to download and analyze
            
        Returns:
            Dictionary with analysis results
        """
        import aiohttp
        
        # Parse URL for filename
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        if not filename.lower().endswith('.pdf'):
            filename += '.pdf'
        
        try:
            # Download the PDF
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return {"error": f"Failed to download PDF. Status code: {response.status}"}
                    
                    content = await response.read()
                    
                    # Create a BytesIO object
                    pdf_bytes = io.BytesIO(content)
                    pdf_bytes.seek(0)
                    
                    # Analyze the PDF
                    results = await self.analyze_pdf(pdf_bytes)
                    
                    # Add download information
                    results["download_info"] = {
                        "url": url,
                        "filename": filename,
                        "file_size": len(content),
                        "download_timestamp": datetime.now().isoformat()
                    }
                    
                    # Save to cache directory if needed
                    temp_file = self.cache_dir / filename
                    with open(temp_file, 'wb') as f:
                        f.write(content)
                    
                    results["local_path"] = str(temp_file)
                    
                    return results
                    
        except Exception as e:
            logger.error(f"Error downloading and analyzing PDF: {e}")
            return {"error": str(e)}

class SecurityPaperAnalyzer:
    """Specialized analyzer for security research papers and defacement archives."""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize the Security Paper Analyzer.
        
        Args:
            cache_dir: Directory to store processed data
        """
        self.pdf_analyzer = PDFAnalyzer(cache_dir)
        
        # Specialized cybersecurity paper patterns
        self.defacement_patterns = [
            re.compile(r'\bdefacement\b', re.IGNORECASE),
            re.compile(r'\bhacked\s+by\b', re.IGNORECASE),
            re.compile(r'\bdefaced\b', re.IGNORECASE),
            re.compile(r'\bzone-h\b', re.IGNORECASE),
            re.compile(r'\bhack(er|ing)\s+crew\b', re.IGNORECASE)
        ]
        
        # Names of prominent hacker crews
        self.known_crews = [
            "bl0w", "G-Force Pakistan", "The Digital Crew", "Turkish Hackers", 
            "World of Hell", "H4CK3R CR3W", "Anti-Security", "Global Hell",
            "Masters of Deception", "Legion of Doom", "Cult of the Dead Cow"
        ]
        
    async def analyze_security_paper(self, pdf_path: Union[str, Path, io.BytesIO]) -> Dict[str, Any]:
        """Analyze a security research paper with specialized indicators.
        
        Args:
            pdf_path: Path to PDF file or BytesIO object
            
        Returns:
            Dictionary with specialized analysis results
        """
        # Get basic PDF analysis
        basic_analysis = await self.pdf_analyzer.analyze_pdf(pdf_path)
        
        # Extract text for specialized analysis
        if isinstance(pdf_path, (str, Path)):
            text = await self.pdf_analyzer.extract_text_from_pdf(pdf_path)
        else:
            # If BytesIO, we need to reset the cursor
            pdf_path.seek(0)
            text = await self.pdf_analyzer.extract_text_from_pdf(pdf_path)
        
        # Analyze for defacement indicators
        defacement_matches = []
        for pattern in self.defacement_patterns:
            matches = pattern.findall(text)
            if matches:
                defacement_matches.extend(matches)
        
        # Look for known crews
        crew_mentions = []
        for crew in self.known_crews:
            if re.search(r'\b' + re.escape(crew) + r'\b', text, re.IGNORECASE):
                crew_mentions.append(crew)
        
        # Extract years (1990-2010) that might be relevant to defacements
        year_pattern = re.compile(r'\b(199\d|200\d|201[0-5])\b')
        years = year_pattern.findall(text)
        
        # Calculate defacement relevance score
        defacement_score = min(100, len(defacement_matches) * 15 + len(crew_mentions) * 20)
        
        # Create specialized analysis results
        specialized_results = {
            "is_defacement_related": defacement_score > 30,
            "defacement_relevance_score": defacement_score,
            "defacement_indicators": list(set(defacement_matches)),
            "mentioned_crews": crew_mentions,
            "relevant_years": sorted(list(set(years)))
        }
        
        # Combine with basic analysis
        combined_results = {
            **basic_analysis,
            "defacement_analysis": specialized_results
        }
        
        return combined_results
    
    async def extract_defacement_statistics(self, 
                                          pdf_path: Union[str, Path, io.BytesIO]) -> Dict[str, Any]:
        """Extract statistics about website defacements from research papers.
        
        Args:
            pdf_path: Path to PDF file or BytesIO object
            
        Returns:
            Dictionary with defacement statistics
        """
        # Analyze the security paper
        analysis = await self.analyze_security_paper(pdf_path)
        
        # Extract text for statistics
        if isinstance(pdf_path, (str, Path)):
            text = await self.pdf_analyzer.extract_text_from_pdf(pdf_path)
        else:
            # If BytesIO, we need to reset the cursor
            pdf_path.seek(0)
            text = await self.pdf_analyzer.extract_text_from_pdf(pdf_path)
        
        # Pattern for finding numbers of defacements
        count_pattern = re.compile(r'(\d{1,3}(?:,\d{3})*|\d+)\s+(?:website|web site|site|page)s?\s+(?:were\s+)?defaced', re.IGNORECASE)
        count_matches = count_pattern.findall(text)
        
        # Clean and convert the matched numbers
        defacement_counts = []
        for count in count_matches:
            clean_count = count.replace(',', '')
            try:
                defacement_counts.append(int(clean_count))
            except ValueError:
                pass
        
        # Pattern for dates of defacements
        date_pattern = re.compile(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}|(?:\d{1,2}\s+)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?(?:\s+\d{1,2})?,?\s+\d{4}', re.IGNORECASE)
        date_matches = date_pattern.findall(text)
        
        # Extract country mentions
        country_pattern = re.compile(r'\b(?:USA|United States|Canada|UK|United Kingdom|Russia|China|Iran|Pakistan|Turkey|Brazil|India|Israel|Australia|Germany|France|Italy|Spain|Netherlands|Sweden|Norway|Denmark|Finland|Japan|South Korea|North Korea|Mexico|Argentina|Egypt|Saudi Arabia|UAE|Syria|Iraq|Libya)\b', re.IGNORECASE)
        country_matches = country_pattern.findall(text)
        
        # Count country mentions
        country_counts = {}
        for country in country_matches:
            country_lower = country.lower()
            country_counts[country_lower] = country_counts.get(country_lower, 0) + 1
        
        # Compile statistics
        statistics = {
            "defacement_counts": defacement_counts,
            "mentioned_dates": date_matches[:20],  # Limit to first 20
            "country_mentions": country_counts,
            "top_countries": sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        }
        
        # Add to analysis
        analysis["defacement_statistics"] = statistics
        
        return analysis 