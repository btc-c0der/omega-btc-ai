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
AI H4x0r Assistant for PDF Analysis

LLM-powered analysis for cybersecurity research papers and defacement archives.
"""

import os
import json
import asyncio
import logging
from typing import Dict, Any, Optional, List, Union, Tuple
from pathlib import Path

from .pdf_analyzer import PDFAnalyzer, SecurityPaperAnalyzer

# Configure logging
logger = logging.getLogger(__name__)

class AISecurityAnalyzer:
    """AI-powered analyzer for cybersecurity research papers."""
    
    def __init__(self, 
                cache_dir: Optional[str] = None,
                llm_provider: str = "local",
                api_key: Optional[str] = None):
        """Initialize the AI Security Analyzer.
        
        Args:
            cache_dir: Directory to store cached analyses
            llm_provider: LLM provider to use ('local', 'openai', 'huggingface')
            api_key: API key for the LLM provider
        """
        self.cache_dir = Path(cache_dir) if cache_dir else Path("ai_cache")
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        
        # Initialize analyzers
        self.pdf_analyzer = PDFAnalyzer(cache_dir=str(self.cache_dir))
        self.security_analyzer = SecurityPaperAnalyzer(cache_dir=str(self.cache_dir))
        
        # LLM settings
        self.llm_provider = llm_provider
        self.api_key = api_key
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the appropriate LLM based on provider."""
        self.llm_available = False
        
        try:
            if self.llm_provider == "local":
                # Check for local LLM support
                try:
                    import torch
                    from transformers import AutoModelForCausalLM, AutoTokenizer
                    
                    # Try to initialize a small model for testing
                    self.tokenizer = AutoTokenizer.from_pretrained("gpt2-medium")
                    # Don't actually load the model until needed
                    self.model = None
                    self.llm_available = True
                    self.model_name = "gpt2-medium"  # Default model
                    logger.info("Local LLM initialized successfully")
                except ImportError:
                    logger.warning("Local LLM requires torch and transformers. Install with: pip install torch transformers")
            
            elif self.llm_provider == "openai":
                # Check for OpenAI support
                try:
                    import openai
                    
                    if self.api_key:
                        openai.api_key = self.api_key
                        self.llm_available = True
                        logger.info("OpenAI API initialized successfully")
                    else:
                        logger.warning("OpenAI API key not provided")
                except ImportError:
                    logger.warning("OpenAI support requires openai. Install with: pip install openai")
            
            elif self.llm_provider == "huggingface":
                # Check for Hugging Face support
                try:
                    from huggingface_hub import InferenceClient
                    
                    if self.api_key:
                        self.hf_client = InferenceClient(token=self.api_key)
                        self.llm_available = True
                        logger.info("Hugging Face API initialized successfully")
                    else:
                        logger.warning("Hugging Face API token not provided")
                except ImportError:
                    logger.warning("Hugging Face support requires huggingface_hub. Install with: pip install huggingface_hub")
        
        except Exception as e:
            logger.error(f"Error initializing LLM: {e}")
    
    async def generate_response(self, prompt: str) -> str:
        """Generate a response using the configured LLM.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            The generated response
        """
        if not self.llm_available:
            return "AI analysis unavailable. Please configure an LLM provider."
        
        try:
            if self.llm_provider == "local":
                # Load model if not already loaded
                if self.model is None:
                    try:
                        import torch
                        from transformers import AutoModelForCausalLM
                        
                        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
                        logger.info(f"Local model {self.model_name} loaded successfully")
                    except Exception as e:
                        logger.error(f"Error loading local model: {e}")
                        return f"Error loading local LLM model: {str(e)}"
                
                # Generate response
                inputs = self.tokenizer(prompt, return_tensors="pt")
                with torch.no_grad():
                    outputs = self.model.generate(
                        inputs["input_ids"],
                        max_length=500,
                        temperature=0.7,
                        top_p=0.9,
                        num_return_sequences=1
                    )
                response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                return response.replace(prompt, "").strip()
            
            elif self.llm_provider == "openai":
                import openai
                
                response = await asyncio.to_thread(
                    openai.ChatCompletion.create,
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a cybersecurity expert analyzing technical papers."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
            
            elif self.llm_provider == "huggingface":
                from huggingface_hub import InferenceClient
                
                # Use a good default model
                model = "mistralai/Mistral-7B-Instruct-v0.2"
                
                response = await asyncio.to_thread(
                    self.hf_client.text_generation,
                    prompt,
                    model=model,
                    max_new_tokens=500,
                    temperature=0.7,
                    top_p=0.9
                )
                return response.strip()
            
            return "No valid LLM provider configured"
        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"Error generating AI response: {str(e)}"
    
    def _create_security_prompt(self, analysis_result: Dict[str, Any]) -> str:
        """Create a prompt for the LLM based on PDF analysis.
        
        Args:
            analysis_result: Analysis results from the PDF analyzer
            
        Returns:
            A prompt for the LLM
        """
        # Extract key information
        metadata = analysis_result.get("metadata", {})
        text_sample = analysis_result.get("text_sample", "")
        indicators = analysis_result.get("security_indicators", {})
        defacement = analysis_result.get("defacement_analysis", {})
        stats = analysis_result.get("defacement_statistics", {})
        
        # Create the prompt
        prompt = "You are a cybersecurity expert analyzing a research paper. "
        prompt += "Please provide insights based on the following information extracted from the document:\n\n"
        
        # Add metadata
        prompt += "DOCUMENT METADATA:\n"
        for key, val in metadata.items():
            prompt += f"- {key}: {val}\n"
        prompt += "\n"
        
        # Add security indicators
        if indicators:
            prompt += "SECURITY INDICATORS:\n"
            score = indicators.get("security_score", 0)
            prompt += f"- Security relevance score: {score}/100\n"
            
            keywords = indicators.get("security_keywords", [])
            if keywords:
                prompt += f"- Security keywords: {', '.join(keywords)}\n"
            
            cves = indicators.get("cves", [])
            if cves:
                prompt += f"- CVEs mentioned: {', '.join(cves[:5])}"
                if len(cves) > 5:
                    prompt += f" and {len(cves) - 5} more"
                prompt += "\n"
            
            prompt += "\n"
        
        # Add defacement analysis
        if defacement:
            prompt += "DEFACEMENT ANALYSIS:\n"
            score = defacement.get("defacement_relevance_score", 0)
            is_related = defacement.get("is_defacement_related", False)
            prompt += f"- Defacement relevance: {'Yes' if is_related else 'No'} (Score: {score}/100)\n"
            
            crews = defacement.get("mentioned_crews", [])
            if crews:
                prompt += f"- Hacker crews mentioned: {', '.join(crews)}\n"
            
            years = defacement.get("relevant_years", [])
            if years:
                prompt += f"- Relevant years: {', '.join(years)}\n"
            
            prompt += "\n"
        
        # Add defacement statistics
        if stats:
            prompt += "DEFACEMENT STATISTICS:\n"
            
            counts = stats.get("defacement_counts", [])
            if counts:
                prompt += f"- Defacement counts mentioned: {', '.join(map(str, counts))}\n"
            
            countries = stats.get("top_countries", [])
            if countries:
                prompt += "- Top countries mentioned:\n"
                for country, count in countries:
                    prompt += f"  - {country}: {count} mentions\n"
            
            prompt += "\n"
        
        # Add the text sample if available
        if text_sample:
            # Limit sample size
            max_text = 3000
            if len(text_sample) > max_text:
                text_sample = text_sample[:max_text] + "..."
            
            prompt += "DOCUMENT EXCERPT:\n"
            prompt += f"{text_sample}\n\n"
        
        # Add the final questions
        prompt += "Based on the above information, please provide:\n"
        prompt += "1. A brief summary of what this document appears to be about\n"
        prompt += "2. Key cybersecurity insights from the document\n"
        prompt += "3. Historical context for any defacements or hacking incidents mentioned\n"
        prompt += "4. Technical significance of this document for security researchers\n"
        
        return prompt
    
    async def analyze_with_ai(self, pdf_path: Union[str, Path]) -> Dict[str, Any]:
        """Analyze a PDF with both technical analysis and AI insights.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Analysis results including AI insights
        """
        # First perform technical analysis
        analysis = await self.security_analyzer.extract_defacement_statistics(pdf_path)
        
        # If LLM is not available, return just the technical analysis
        if not self.llm_available:
            analysis["ai_insights"] = {
                "error": "AI analysis unavailable. Please configure an LLM provider."
            }
            return analysis
        
        # Create the prompt
        prompt = self._create_security_prompt(analysis)
        
        # Generate the AI response
        ai_response = await self.generate_response(prompt)
        
        # Add the AI insights to the analysis
        analysis["ai_insights"] = {
            "full_response": ai_response,
            "prompt_length": len(prompt),
            "response_length": len(ai_response)
        }
        
        return analysis
    
    async def quick_defacement_assessment(self, text: str) -> Dict[str, Any]:
        """Generate a quick assessment of defacement-related text.
        
        Args:
            text: Text excerpt from a defacement or security paper
            
        Returns:
            Dictionary with AI assessment
        """
        if not self.llm_available:
            return {
                "error": "AI analysis unavailable. Please configure an LLM provider."
            }
        
        # Create a prompt for defacement analysis
        prompt = "You are a cybersecurity expert analyzing a possible website defacement. "
        prompt += "Please analyze the following text excerpt and identify key details:\n\n"
        prompt += f"{text}\n\n"
        prompt += "Please provide:\n"
        prompt += "1. Who likely performed this defacement (individual or group)?\n"
        prompt += "2. What is the likely motivation (political, religious, for fun, etc.)?\n"
        prompt += "3. What technical indicators are present?\n"
        prompt += "4. How would you categorize this in terms of threat level?\n"
        prompt += "5. Any historical context about the actors or techniques used?\n"
        
        # Generate the AI response
        ai_response = await self.generate_response(prompt)
        
        # Return the analysis
        return {
            "full_response": ai_response,
            "analyzed_text": text[:100] + "..." if len(text) > 100 else text
        }

# Demo for testing
async def demo():
    """Run a demo of the AI analyzer."""
    analyzer = AISecurityAnalyzer(llm_provider="local")
    
    test_text = """
    !!! HACKED BY BL0W CREW !!!
    
    Your security has been compromised. This defacement is proof of your weak security.
    
    We are bl0w, we do not forgive, we do not forget.
    
    Greetz to: AnonGhost, Turkish Hackers, Zone-H, and all our brothers in the scene.
    
    [Indonesia Hackers]
    """
    
    result = await analyzer.quick_defacement_assessment(test_text)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(demo()) 