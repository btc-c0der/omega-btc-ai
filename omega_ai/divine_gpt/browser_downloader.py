import os
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrowserDivineDownloader:
    """Download ChatGPT conversation history using browser automation."""
    
    def __init__(self):
        """Initialize the browser downloader."""
        self._conversations: List[Dict[str, Any]] = []
        self._driver = None
        
    def _setup_driver(self):
        """Set up the Chrome driver using a temporary profile."""
        options = Options()
        
        # Create a temporary profile directory
        self._temp_dir = os.path.join(os.getcwd(), 'temp_chrome_profile')
        os.makedirs(self._temp_dir, exist_ok=True)
        
        # Add stealth arguments
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--disable-site-isolation-trials')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
        
        # Add experimental options
        options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Add normal browser arguments
        options.add_argument(f'--user-data-dir={self._temp_dir}')
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        
        try:
            logger.info("Initializing Chrome driver...")
            logger.info(f"Using temporary profile directory: {self._temp_dir}")
            
            service = Service()
            self._driver = webdriver.Chrome(service=service, options=options)
            
            # Remove webdriver marks
            stealth_js = """
                // Overwrite the 'navigator.webdriver' property
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                
                // Remove 'webdriver' from navigator prototype chain
                delete Object.getPrototypeOf(navigator).webdriver;
                
                // Add missing chrome properties
                window.chrome = {
                    runtime: {},
                    loadTimes: function(){},
                    csi: function(){},
                    app: {}
                };
                
                // Add language property
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });
            """
            self._driver.execute_script(stealth_js)
            
            if self._driver is None:
                raise Exception("Failed to initialize Chrome driver - driver is None")
                
            self._driver.implicitly_wait(10)
            logger.info("Successfully initialized Chrome driver")
            
        except Exception as e:
            logger.error(f"Error setting up Chrome driver: {str(e)}")
            raise
            
    def _random_sleep(self, min_seconds=1, max_seconds=3):
        """Sleep for a random amount of time to appear more human-like."""
        import random
        time.sleep(random.uniform(min_seconds, max_seconds))
            
    def _extract_conversations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Extract conversations from the chat history."""
        try:
            if self._driver is None:
                raise Exception("Chrome driver not initialized")
                
            # Navigate to ChatGPT
            logger.info("Navigating to ChatGPT...")
            self._driver.get('https://chat.openai.com')
            
            # Add human-like behavior
            self._random_sleep(2, 4)
            
            # Simulate natural scrolling
            self._driver.execute_script("""
                function naturalScroll() {
                    let scrollHeight = document.documentElement.scrollHeight;
                    let currentScroll = 0;
                    let scrollStep = Math.floor(Math.random() * 100) + 100;
                    
                    function smoothScroll() {
                        if (currentScroll < scrollHeight) {
                            currentScroll = Math.min(currentScroll + scrollStep, scrollHeight);
                            window.scrollTo(0, currentScroll);
                            setTimeout(smoothScroll, Math.random() * 500 + 200);
                        }
                    }
                    
                    smoothScroll();
                }
                naturalScroll();
            """)
            
            # Wait for manual login
            logger.info("Please log in manually. Waiting 90 seconds...")
            time.sleep(90)  # Wait for 90 seconds for manual login
            
            # Check if we're logged in by looking for the nav element
            try:
                WebDriverWait(self._driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "nav"))
                )
                logger.info("Successfully logged in!")
            except TimeoutException:
                logger.warning("Nav element not found after login wait. Proceeding anyway...")
            
            # Random sleep to appear more human-like
            self._random_sleep(2, 4)
            
            # Log the current URL
            current_url = self._driver.current_url
            logger.info(f"Current URL: {current_url}")
            
            # Try to find conversation links
            try:
                # Wait for conversation links to be visible
                WebDriverWait(self._driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/c/')]"))
                )
                
                conv_links = self._driver.find_elements(By.XPATH, "//a[contains(@href, '/c/')]")[:limit]
                logger.info(f"Found {len(conv_links)} conversation links")
                
                conversations = []
                for link in conv_links:
                    try:
                        href = link.get_attribute('href')
                        if not href:
                            continue
                            
                        conv_id = href.split('/')[-1]
                        title = link.text or "Untitled Conversation"
                        logger.info(f"Processing conversation: {title}")
                        
                        # Random sleep between processing conversations
                        self._random_sleep()
                        
                        conversations.append({
                            "id": conv_id,
                            "title": title,
                            "messages": [],  # We'll fill this later if needed
                            "created_at": datetime.now().isoformat()
                        })
                        
                    except Exception as e:
                        logger.error(f"Error processing conversation link: {str(e)}")
                        continue
                
                return conversations
                
            except Exception as e:
                logger.error(f"Error finding conversation links: {str(e)}")
                return []
            
        except Exception as e:
            logger.error(f"Error accessing ChatGPT: {str(e)}")
            raise
    
    def _calculate_divine_attributes(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate divine attributes for a conversation.
        
        Args:
            conversation: Raw conversation data
            
        Returns:
            Divine attributes including resonance and sacred level
        """
        messages = conversation.get("messages", [])
        message_count = len(messages)
        total_length = sum(len(m.get("content", "")) for m in messages)
        
        # Calculate resonance based on interaction depth
        resonance = min(10, message_count / 2)  # Scale 0-10
        
        # Calculate sacred level based on content length and depth
        sacred_level = min(100, (total_length / 1000) * (message_count / 5))  # Scale 0-100
        
        return {
            "resonance": resonance,
            "sacred_level": sacred_level,
            "timestamp_cosmic": int(datetime.now().timestamp()),
            "divine_signature": "OMEGA_BROWSER"
        }
    
    async def download_conversations(
        self,
        start_date: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Download and process conversations using browser automation.
        
        Args:
            start_date: Start date in ISO format (YYYY-MM-DD)
            limit: Maximum number of conversations to download
            
        Returns:
            List of processed conversations with divine attributes
        """
        try:
            self._setup_driver()
            
            raw_conversations = self._extract_conversations(limit=limit)
            
            processed_conversations = []
            for conv in raw_conversations:
                # Filter by start date if specified
                if start_date:
                    conv_date = datetime.fromisoformat(conv["created_at"])
                    start = datetime.fromisoformat(start_date)
                    if conv_date < start:
                        continue
                
                # Add divine attributes
                conv["divine_attributes"] = self._calculate_divine_attributes(conv)
                processed_conversations.append(conv)
            
            self._conversations = processed_conversations
            return processed_conversations
            
        except Exception as e:
            logger.error(f"Error downloading conversations: {str(e)}")
            return []
            
        finally:
            if self._driver:
                self._driver.quit()
            
            # Clean up the temporary directory
            if hasattr(self, '_temp_dir') and os.path.exists(self._temp_dir):
                import shutil
                try:
                    shutil.rmtree(self._temp_dir, ignore_errors=True)
                    logger.info("Cleaned up temporary profile directory")
                except Exception as e:
                    logger.warning(f"Failed to clean up temporary profile: {str(e)}")
    
    async def export_conversations(self, output_file: str) -> None:
        """Export conversations to a JSON file.
        
        Args:
            output_file: Path to output JSON file
        """
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(self._conversations, f, indent=2) 