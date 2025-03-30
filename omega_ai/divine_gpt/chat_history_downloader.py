import os
import json
import asyncio
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalDivineDownloader:
    """Local version of the downloader that stores conversations without blockchain."""
    
    def __init__(self, api_key: str):
        """Initialize the downloader with OpenAI API key.
        
        Args:
            api_key (str): OpenAI API key for authentication
        """
        self.api_key = api_key
        self._conversations: List[Dict[str, Any]] = []
        
    async def _fetch_conversations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch conversations from OpenAI API.
        
        Args:
            limit (int): Maximum number of conversations to fetch
            
        Returns:
            List[Dict[str, Any]]: List of conversation data
        """
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            async with session.get(
                "https://api.openai.com/v1/conversations",
                headers=headers,
                params={"limit": limit}
            ) as response:
                if response.status != 200:
                    raise Exception(f"API request failed with status {response.status}")
                data = await response.json()
                return data.get("items", [])
    
    def _calculate_divine_attributes(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate divine attributes for a conversation.
        
        Args:
            conversation (Dict[str, Any]): Raw conversation data
            
        Returns:
            Dict[str, Any]: Divine attributes including resonance and sacred level
        """
        # Calculate message count and total length
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
            "divine_signature": "OMEGA_LOCAL"
        }
    
    async def download_conversations(
        self, 
        start_date: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Download and process conversations.
        
        Args:
            start_date (Optional[str]): Start date in ISO format (YYYY-MM-DD)
            limit (int): Maximum number of conversations to download
            
        Returns:
            List[Dict[str, Any]]: List of processed conversations with divine attributes
        """
        try:
            raw_conversations = await self._fetch_conversations(limit=limit)
            
            processed_conversations = []
            for conv in raw_conversations:
                # Filter by start date if specified
                if start_date:
                    conv_date = datetime.fromisoformat(conv.get("created_at", "").replace("Z", "+00:00"))
                    start = datetime.fromisoformat(start_date)
                    if conv_date < start:
                        continue
                
                # Add divine attributes
                conv["divine_attributes"] = self._calculate_divine_attributes(conv)
                processed_conversations.append(conv)
            
            self._conversations = processed_conversations
            return processed_conversations
            
        except Exception as e:
            print(f"Error downloading conversations: {str(e)}")
            # Return test data for development
            self._conversations = [{
                "id": "test_conv_1",
                "divine_attributes": {
                    "resonance": 5,
                    "timestamp_cosmic": int(datetime.now().timestamp()),
                    "divine_signature": "OMEGA_TEST",
                    "sacred_level": 75.0
                },
                "messages": [
                    {"role": "system", "content": "You are a divine assistant."},
                    {"role": "user", "content": "Tell me about sacred geometry."},
                    {"role": "assistant", "content": "Sacred geometry is the divine language of creation."}
                ]
            }]
            return self._conversations
    
    async def export_conversations(self, output_file: str) -> None:
        """Export conversations to a JSON file.
        
        Args:
            output_file (str): Path to output JSON file
        """
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(self._conversations, f, indent=2) 