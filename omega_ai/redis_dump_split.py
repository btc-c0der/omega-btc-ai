"""
Redis Dump Splitter
==================

This script reads the most recent Redis dump JSON file from the redis-dumps folder
and splits it into smaller, AI-uploadable chunks while preserving data integrity.

Features:
- Finds most recent dump file in redis-dumps folder
- Splits data into manageable chunks (default 512MB)
- Preserves JSON structure and Unicode characters
- Adds metadata for chunk tracking
- Supports compression for large entries
"""

import os
import json
import glob
import gzip
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import sys

# ANSI colors for output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

def find_latest_dump() -> Optional[str]:
    """Find the most recent Redis dump JSON file."""
    try:
        # Look for JSON files in redis-dumps folder
        dump_pattern = os.path.join("redis-dumps", "*.json")
        dump_files = glob.glob(dump_pattern)
        
        if not dump_files:
            print(f"{YELLOW}⚠️ No JSON files found in redis-dumps folder{RESET}")
            return None
            
        # Get the most recent file by modification time
        latest_file = max(dump_files, key=os.path.getmtime)
        print(f"{GREEN}✓ Found latest dump: {latest_file}{RESET}")
        return latest_file
    except Exception as e:
        print(f"{RED}✗ Error finding latest dump: {e}{RESET}")
        return None

def load_dump_file(file_path: str) -> Dict[str, Any]:
    """Load and parse the Redis dump JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"{GREEN}✓ Successfully loaded dump file{RESET}")
        return data
    except Exception as e:
        print(f"{RED}✗ Error loading dump file: {e}{RESET}")
        return {}

def analyze_data(data: Dict[str, Any]) -> Tuple[Dict[str, int], List[Tuple[str, int]]]:
    """Analyze Redis data structure and sizes."""
    key_sizes = {}
    total_size = 0
    
    print(f"\n{MAGENTA}📊 Data Analysis:{RESET}")
    
    # Calculate sizes and collect statistics
    for key, value in data.items():
        entry = {key: value}
        entry_json = json.dumps(entry)
        size = len(entry_json.encode('utf-8'))
        key_sizes[key] = size
        total_size += size
        
    # Sort keys by size
    sorted_keys = sorted(key_sizes.items(), key=lambda x: x[1], reverse=True)
    
    # Print size distribution
    print(f"{MAGENTA}Top 5 largest entries:{RESET}")
    for key, size in sorted_keys[:5]:
        size_mb = size / (1024 * 1024)
        print(f"• {key}: {size_mb:.1f}MB")
    
    print(f"\n{MAGENTA}Total entries: {len(data)}{RESET}")
    print(f"{MAGENTA}Total size: {total_size / (1024*1024):.1f}MB{RESET}")
    
    return key_sizes, sorted_keys

def compress_entry(entry: Dict[str, Any]) -> bytes:
    """Compress a dictionary entry using gzip."""
    json_str = json.dumps(entry, ensure_ascii=False)
    return gzip.compress(json_str.encode('utf-8'))

def save_compressed_chunk(chunk: Dict[str, Any], filename: str) -> float:
    """Save chunk with compression for large entries."""
    # Compress entries larger than 100MB
    compressed_chunk = {}
    for key, value in chunk.items():
        if key == "_metadata":
            compressed_chunk[key] = value
            continue
            
        entry = {key: value}
        entry_size = len(json.dumps(entry, ensure_ascii=False).encode('utf-8'))
        
        if entry_size > 100 * 1024 * 1024:  # 100MB
            compressed_chunk[f"{key}.gz"] = compress_entry(entry)
        else:
            compressed_chunk[key] = value
    
    # Save to file
    with open(filename, 'wb') as f:
        f.write(json.dumps(compressed_chunk, ensure_ascii=False, default=lambda x: x.hex() if isinstance(x, bytes) else x).encode('utf-8'))
    
    size_mb = os.path.getsize(filename) / (1024 * 1024)
    return size_mb

def split_data(data: Dict[str, Any], chunk_size: int = 512 * 1024 * 1024) -> List[Dict[str, Any]]:
    """Split Redis data into manageable chunks of approximately 512MB each."""
    chunks = []
    current_chunk = {}
    current_size = 0
    
    # Analyze data first
    key_sizes, sorted_keys = analyze_data(data)
    total_size = sum(key_sizes.values())
    
    # Estimate number of chunks needed
    estimated_chunks = max(1, total_size // chunk_size + (1 if total_size % chunk_size else 0))
    target_chunk_size = total_size // estimated_chunks
    
    print(f"\n{CYAN}ℹ Target chunk size: {target_chunk_size / (1024*1024):.1f}MB{RESET}")
    
    # Add metadata template
    metadata = {
        "timestamp": datetime.now().isoformat(),
        "total_keys": len(data),
        "total_size_bytes": total_size,
        "chunk_number": 0,
        "total_chunks": 0,  # Will be updated later
        "compression_info": {
            "enabled": True,
            "threshold_mb": 100,
            "format": "gzip"
        }
    }
    
    # Process entries by size
    for key, size in sorted_keys:
        # If this entry alone is larger than target size, it gets its own chunk
        if size > target_chunk_size:
            if current_chunk:
                current_chunk["_metadata"] = metadata.copy()
                chunks.append(current_chunk)
                current_chunk = {}
                current_size = 0
            
            # Create a dedicated chunk for this large entry
            chunk = {key: data[key]}
            chunk["_metadata"] = metadata.copy()
            chunks.append(chunk)
            continue
        
        # If adding this entry would exceed target size, start new chunk
        if current_size + size > target_chunk_size and current_chunk:
            current_chunk["_metadata"] = metadata.copy()
            chunks.append(current_chunk)
            current_chunk = {}
            current_size = 0
        
        # Add entry to current chunk
        current_chunk[key] = data[key]
        current_size += size
    
    # Add remaining data as final chunk
    if current_chunk:
        current_chunk["_metadata"] = metadata.copy()
        chunks.append(current_chunk)
    
    # Update metadata with total chunks and chunk numbers
    total_chunks = len(chunks)
    for i, chunk in enumerate(chunks, 1):
        chunk["_metadata"].update({
            "chunk_number": i,
            "total_chunks": total_chunks,
            "chunk_size_bytes": len(json.dumps(chunk, ensure_ascii=False).encode('utf-8'))
        })
    
    return chunks

def save_chunks(chunks: List[Dict[str, Any]], base_name: str = "redis_chunk") -> None:
    """Save data chunks to files with compression for large entries."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("redis-chunks", exist_ok=True)
    
    print(f"\n{CYAN}Saving chunks with compression:{RESET}")
    for i, chunk in enumerate(chunks, 1):
        output_file = os.path.join("redis-chunks", f"{base_name}_{timestamp}_{i:03d}.json")
        try:
            size_mb = save_compressed_chunk(chunk, output_file)
            keys_count = len(chunk) - 1  # Subtract 1 for metadata
            print(f"{GREEN}✓ Chunk {i}/{len(chunks)} ({size_mb:.1f}MB, {keys_count} keys): {output_file}{RESET}")
        except Exception as e:
            print(f"{RED}✗ Error saving chunk {i}: {e}{RESET}")

def main():
    """Main execution function."""
    print(f"\n{CYAN}🔍 Redis Dump Splitter{RESET}")
    
    # Find latest dump file
    dump_file = find_latest_dump()
    if not dump_file:
        print(f"{RED}✗ No dump file found to process{RESET}")
        return
    
    # Load the dump file
    data = load_dump_file(dump_file)
    if not data:
        print(f"{RED}✗ No data loaded from dump file{RESET}")
        return
    
    # Split into chunks
    chunks = split_data(data)
    if not chunks:
        print(f"{RED}✗ No chunks created{RESET}")
        return
    
    # Save chunks with compression
    save_chunks(chunks)
    print(f"\n{GREEN}✨ Processing complete! Check the redis-chunks folder for split files{RESET}")

if __name__ == "__main__":
    main()
