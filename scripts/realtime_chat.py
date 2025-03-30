#!/usr/bin/env python3
"""Example script demonstrating real-time chat with GPT."""

import os
import sys
import asyncio
import argparse
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from omega_ai.divine_gpt.realtime_gpt import RealTimeGPT

async def print_stream(text: str):
    """Print streaming text with a typewriter effect."""
    print(text, end='', flush=True)

async def main(api_key: Optional[str] = None):
    """Run the real-time chat example."""
    gpt = RealTimeGPT(api_key=api_key)
    
    # Example system message
    system_message = """You are a helpful AI assistant with expertise in cryptocurrency 
    and blockchain technology. You provide clear, concise responses with a focus on 
    accuracy and real-world applications."""
    
    print("\nWelcome to Real-time GPT Chat!")
    print("Type 'exit' to end the conversation\n")
    
    while True:
        try:
            # Get user input
            prompt = input("\nYou: ")
            if prompt.lower() == 'exit':
                break
                
            print("\nAssistant: ", end='', flush=True)
            
            # Stream the response
            async for chunk in gpt.stream_completion(
                prompt=prompt,
                system_message=system_message,
                stream_callback=print_stream
            ):
                pass  # Content is printed by callback
                
            print()  # New line after response
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            break
    
    # Save conversation history
    await gpt.save_history("chat_history.json")
    print("\nChat history saved to chat_history.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real-time chat with GPT")
    parser.add_argument("--api-key", help="OpenAI API key (optional, can use OPENAI_API_KEY env var)")
    args = parser.parse_args()
    
    asyncio.run(main(api_key=args.api_key)) 