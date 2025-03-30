"""Real-time GPT interaction module.

This module provides real-time interaction capabilities with OpenAI's GPT models,
including streaming responses and handling continuous conversations.
"""

import os
import json
import asyncio
import logging
from typing import AsyncGenerator, Dict, List, Optional, Any
from datetime import datetime

import openai
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

class RealTimeGPT:
    """Handles real-time interactions with GPT models."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4-turbo-preview"):
        """Initialize the real-time GPT handler.
        
        Args:
            api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY env var
            model: GPT model to use for interactions
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided or set in OPENAI_API_KEY environment variable")
        
        self.model = model
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.conversation_history: List[Dict[str, str]] = []
        
    async def stream_completion(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream_callback = None
    ) -> AsyncGenerator[str, None]:
        """Stream a completion from GPT.
        
        Args:
            prompt: The user's input prompt
            system_message: Optional system message to set context
            temperature: Controls randomness (0-1)
            max_tokens: Maximum tokens to generate
            stream_callback: Optional callback function for each chunk
            
        Yields:
            Generated text chunks as they arrive
        """
        messages = []
        
        # Add system message if provided
        if system_message:
            messages.append({"role": "system", "content": system_message})
            
        # Add conversation history
        messages.extend(self.conversation_history)
        
        # Add current prompt
        messages.append({"role": "user", "content": prompt})
        
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            collected_chunks = []
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    collected_chunks.append(content)
                    
                    if stream_callback:
                        await stream_callback(content)
                        
                    yield content
                    
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history.append({
                "role": "assistant",
                "content": "".join(collected_chunks)
            })
            
        except Exception as e:
            logger.error(f"Error in stream_completion: {str(e)}")
            raise
            
    async def stream_with_functions(
        self,
        prompt: str,
        functions: List[Dict[str, Any]],
        stream_callback = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream a completion with function calling capabilities.
        
        Args:
            prompt: The user's input prompt
            functions: List of function definitions
            stream_callback: Optional callback for streaming updates
            
        Yields:
            Chunks of the response, including function calls
        """
        messages = [{"role": "user", "content": prompt}]
        
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                functions=functions,
                stream=True
            )
            
            current_function_call = None
            collected_chunks = []
            
            async for chunk in stream:
                delta = chunk.choices[0].delta
                
                # Handle function calls
                if delta.function_call:
                    if current_function_call is None:
                        current_function_call = {
                            "name": delta.function_call.name,
                            "arguments": ""
                        }
                    
                    if delta.function_call.arguments:
                        current_function_call["arguments"] += delta.function_call.arguments
                        
                    if stream_callback:
                        await stream_callback({
                            "type": "function_call",
                            "data": current_function_call
                        })
                        
                    yield {
                        "type": "function_call",
                        "data": current_function_call
                    }
                    
                # Handle regular content
                elif delta.content:
                    collected_chunks.append(delta.content)
                    
                    if stream_callback:
                        await stream_callback({
                            "type": "content",
                            "data": delta.content
                        })
                        
                    yield {
                        "type": "content",
                        "data": delta.content
                    }
                    
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": prompt})
            
            if current_function_call:
                self.conversation_history.append({
                    "role": "assistant",
                    "function_call": current_function_call
                })
            else:
                self.conversation_history.append({
                    "role": "assistant",
                    "content": "".join(collected_chunks)
                })
                
        except Exception as e:
            logger.error(f"Error in stream_with_functions: {str(e)}")
            raise
            
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        
    async def save_history(self, filepath: str):
        """Save the conversation history to a file.
        
        Args:
            filepath: Path to save the conversation history
        """
        try:
            with open(filepath, 'w') as f:
                json.dump({
                    "model": self.model,
                    "timestamp": datetime.now().isoformat(),
                    "history": self.conversation_history
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving conversation history: {str(e)}")
            raise 