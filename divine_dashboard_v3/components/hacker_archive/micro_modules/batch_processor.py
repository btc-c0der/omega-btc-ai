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
Batch Processor Module

Handles batch generation of multiple NFTs with customizable options.
"""

import asyncio
import uuid
import time
import logging
from typing import List, Dict, Any, Optional, Callable, Awaitable, Tuple
import random

# Configure logging
logger = logging.getLogger(__name__)

class BatchProcessor:
    """Handles batch generation of multiple NFTs."""
    
    def __init__(self, 
                generate_function: Callable[..., Awaitable[Dict[str, Any]]],
                max_concurrent: int = 5):
        """
        Initialize the batch processor.
        
        Args:
            generate_function: Async function that generates a single NFT
            max_concurrent: Maximum number of concurrent generation tasks
        """
        self.generate_function = generate_function
        self.max_concurrent = max(1, max_concurrent)
        self.batch_history: List[Dict[str, Any]] = []
        
    async def process_batch(self,
                          count: int,
                          options_list: Optional[List[Dict[str, Any]]] = None,
                          **kwargs) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Process a batch of NFT generation requests.
        
        Args:
            count: Number of NFTs to generate
            options_list: Optional list of specific options for each NFT
            **kwargs: Default options to use if options_list not provided
            
        Returns:
            Tuple of (list_of_results, batch_stats)
        """
        batch_id = str(uuid.uuid4())
        start_time = time.time()
        results: List[Dict[str, Any]] = []
        errors = 0
        
        logger.info(f"Starting batch {batch_id} with {count} NFTs")
        
        # Create a semaphore to limit concurrent tasks
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def wrapped_generate(index: int, options: Dict[str, Any]) -> Dict[str, Any]:
            """Wrapper for generation with semaphore and error handling."""
            async with semaphore:
                try:
                    # Add batch metadata to options
                    options['batch_id'] = batch_id
                    options['batch_index'] = index
                    
                    # Call the generate function
                    result = await self.generate_function(**options)
                    
                    # Ensure batch info is in the result
                    if 'batch_id' not in result:
                        result['batch_id'] = batch_id
                    if 'batch_index' not in result:
                        result['batch_index'] = index
                        
                    return result
                    
                except Exception as e:
                    logger.error(f"Error generating NFT {index} in batch {batch_id}: {str(e)}")
                    return {
                        'status': 'error',
                        'batch_id': batch_id,
                        'batch_index': index,
                        'error': str(e)
                    }
        
        # Create tasks based on either options_list or kwargs
        tasks = []
        
        if options_list and len(options_list) > 0:
            # Use provided options for each NFT
            for i in range(min(count, len(options_list))):
                tasks.append(wrapped_generate(i, options_list[i]))
                
            # If we need more than provided, use the last options as template
            template = options_list[-1] if options_list else kwargs
            for i in range(len(options_list), count):
                tasks.append(wrapped_generate(i, template.copy()))
        else:
            # Use kwargs as default options for all NFTs
            for i in range(count):
                tasks.append(wrapped_generate(i, kwargs.copy()))
        
        # Wait for all tasks to complete
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)
            
            # Track errors
            if result.get('status') == 'error':
                errors += 1
        
        # Calculate stats
        end_time = time.time()
        total_time = end_time - start_time
        success_count = count - errors
        
        # Sort results by batch_index
        results.sort(key=lambda x: x.get('batch_index', 0))
        
        # Calculate average successful generation time
        avg_time = total_time / max(1, count)
        
        # Create batch stats
        batch_stats = {
            'batch_id': batch_id,
            'total_count': count,
            'success_count': success_count,
            'error_count': errors,
            'success_rate': success_count / count if count > 0 else 0,
            'total_time': total_time,
            'avg_time_per_nft': avg_time,
            'start_time': start_time,
            'end_time': end_time,
            'concurrent_limit': self.max_concurrent
        }
        
        # Store in history
        self.batch_history.append(batch_stats)
        
        logger.info(f"Completed batch {batch_id}: {success_count}/{count} successful " +
                   f"in {total_time:.2f}s ({avg_time:.2f}s per NFT)")
        
        return results, batch_stats
        
    def get_batch_history(self) -> List[Dict[str, Any]]:
        """Get the history of processed batches."""
        return self.batch_history
        
    def get_batch_stats(self, batch_id: str) -> Optional[Dict[str, Any]]:
        """Get statistics for a specific batch."""
        for stats in self.batch_history:
            if stats.get('batch_id') == batch_id:
                return stats
        return None 