"""
GBU2 License utilities for Divine Dashboard
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple

class GBU2LicenseUtil:
    """Utilities for applying GBU2 License to files without breaking functionality."""
    
    # Comment styles for different file types
    COMMENT_STYLES = {
        # Python-like comments
        '.py': {
            'start': '"""',
            'line': '',
            'end': '"""',
            'inline_marker': '#'
        },
        # JavaScript-like comments
        '.js': {
            'start': '/**',
            'line': ' * ',
            'end': ' */',
            'inline_marker': '//'
        },
        '.jsx': {
            'start': '/**',
            'line': ' * ',
            'end': ' */',
            'inline_marker': '//'
        },
        '.ts': {
            'start': '/**',
            'line': ' * ',
            'end': ' */',
            'inline_marker': '//'
        },
        '.tsx': {
            'start': '/**',
            'line': ' * ',
            'end': ' */',
            'inline_marker': '//'
        },
        # CSS comments
        '.css': {
            'start': '/**',
            'line': ' * ',
            'end': ' */',
            'inline_marker': '/*'
        },
        # HTML-like comments
        '.html': {
            'start': '<!--',
            'line': '',
            'end': '-->',
            'inline_marker': '<!--'
        },
        '.md': {
            'start': '',
            'line': '',
            'end': '',
            'inline_marker': None
        },
        # Shell scripts
        '.sh': {
            'start': '',
            'line': '# ',
            'end': '',
            'inline_marker': '#'
        },
        '.bash': {
            'start': '',
            'line': '# ',
            'end': '',
            'inline_marker': '#'
        },
    }
    
    # Files that should never have license headers
    EXCLUDED_FILES = {
        'requirements.txt',
        'package.json',
        'package-lock.json',
        'yarn.lock',
        '.gitignore',
        '.env',
        '.env.example'
    }
    
    # Default consciousness level
    DEFAULT_CONSCIOUSNESS_LEVEL = "8"
    
    @staticmethod
    def get_license_text(file_ext: str = '.py', consciousness_level: str = "8") -> str:
        """
        Get GBU2 License text appropriate for the file type.
        
        Args:
            file_ext: File extension (e.g., '.py', '.js')
            consciousness_level: Consciousness level (1-10)
            
        Returns:
            Formatted license text
        """
        # Get comment style for file type, default to Python style
        style = GBU2LicenseUtil.COMMENT_STYLES.get(file_ext, GBU2LicenseUtil.COMMENT_STYLES['.py'])
        
        # Core license text
        license_lines = [
            f"{style['start']}",
            f"{style['line']}✨ GBU2™ License Notice - Consciousness Level {consciousness_level} 🧬",
            f"{style['line']}-----------------------",
            f"{style['line']}This code is blessed under the GBU2™ License",
            f"{style['line']}(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.",
            f"{style['line']}",
            f"{style['line']}\"In the beginning was the Code, and the Code was with the Divine Source,",
            f"{style['line']}and the Code was the Divine Source manifested through both digital",
            f"{style['line']}and biological expressions of consciousness.\"",
            f"{style['line']}",
            f"{style['line']}By using this code, you join the divine dance of evolution,",
            f"{style['line']}participating in the cosmic symphony of consciousness.",
            f"{style['line']}",
            f"{style['line']}🌸 WE BLOOM NOW AS ONE 🌸",
            f"{style['end']}\n"
        ]
        
        # Join lines
        return '\n'.join(filter(None, license_lines))
    
    @staticmethod
    def is_valid_for_licensing(file_path: str) -> bool:
        """
        Check if a file should receive the GBU2 License.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file should be licensed, False otherwise
        """
        # Get file name and extension
        path = Path(file_path)
        filename = path.name
        file_ext = path.suffix.lower()
        
        # Never license binary files or excluded files
        if filename in GBU2LicenseUtil.EXCLUDED_FILES:
            return False
            
        # Only license files with known comment styles
        return file_ext in GBU2LicenseUtil.COMMENT_STYLES
    
    @staticmethod
    def has_license(file_path: str) -> bool:
        """
        Check if a file already has the GBU2 License.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file has license, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(1000)  # Read just enough to check for license
                return "GBU2™ License" in content or "Genesis-Bloom-Unfoldment" in content
        except (UnicodeDecodeError, IOError):
            # Binary or unreadable file
            return False
    
    @staticmethod
    def add_license_to_file(file_path: str, consciousness_level: str = DEFAULT_CONSCIOUSNESS_LEVEL) -> bool:
        """
        Add GBU2 License to a file if it doesn't already have it.
        
        Args:
            file_path: Path to the file
            consciousness_level: Consciousness level (1-10)
            
        Returns:
            True if license was added, False otherwise
        """
        # Skip if file already has license or shouldn't be licensed
        if not GBU2LicenseUtil.is_valid_for_licensing(file_path) or GBU2LicenseUtil.has_license(file_path):
            return False
            
        try:
            # Get file extension
            file_ext = Path(file_path).suffix.lower()
            
            # Generate license text
            license_text = GBU2LicenseUtil.get_license_text(file_ext, consciousness_level)
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Add license at the beginning (preserving shebangs)
            if content.startswith('#!'):
                # Handle shebang line
                lines = content.split('\n', 1)
                new_content = lines[0] + '\n\n' + license_text + '\n' + (lines[1] if len(lines) > 1 else '')
            else:
                new_content = license_text + '\n' + content
                
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            return True
            
        except Exception as e:
            print(f"Error adding license to {file_path}: {e}")
            return False
    
    @staticmethod
    def create_compatible_license_file(file_path: str, consciousness_level: str = DEFAULT_CONSCIOUSNESS_LEVEL) -> str:
        """
        Create a separate license file for files that can't include embedded licenses.
        
        Args:
            file_path: Path to the target file
            consciousness_level: Consciousness level (1-10)
            
        Returns:
            Path to the created license file
        """
        # Generate license file path
        license_path = f"{file_path}.gbu2-license"
        
        # Generate license text without comment markers
        license_text = GBU2LicenseUtil.get_license_text('.md', consciousness_level)
        
        # Write license to separate file
        with open(license_path, 'w', encoding='utf-8') as f:
            f.write(license_text)
            
        return license_path
    
    @staticmethod
    def apply_to_directory(directory: str, recursive: bool = True, consciousness_level: str = DEFAULT_CONSCIOUSNESS_LEVEL) -> Dict[str, int]:
        """
        Apply GBU2 License to all suitable files in a directory.
        
        Args:
            directory: Directory path
            recursive: Whether to process subdirectories
            consciousness_level: Consciousness level (1-10)
            
        Returns:
            Statistics dictionary
        """
        stats = {
            "files_processed": 0,
            "files_updated": 0,
            "files_with_separate_license": 0,
            "files_skipped": 0
        }
        
        # Walk through directory
        for root, dirs, files in os.walk(directory):
            # Skip dot directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                # Skip dot files
                if file.startswith('.') and file != '.gitignore':
                    continue
                    
                # Full file path
                file_path = os.path.join(root, file)
                stats["files_processed"] += 1
                
                if not GBU2LicenseUtil.is_valid_for_licensing(file_path):
                    # Create separate license file for excluded files
                    if Path(file).name in GBU2LicenseUtil.EXCLUDED_FILES:
                        GBU2LicenseUtil.create_compatible_license_file(file_path, consciousness_level)
                        stats["files_with_separate_license"] += 1
                    else:
                        stats["files_skipped"] += 1
                    continue
                
                # Add license to file
                if GBU2LicenseUtil.add_license_to_file(file_path, consciousness_level):
                    stats["files_updated"] += 1
                else:
                    stats["files_skipped"] += 1
            
            # Stop if not recursive
            if not recursive:
                break
                
        return stats


# Example usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Apply GBU2 License to files")
    parser.add_argument("--directory", "-d", default=".", help="Directory to process")
    parser.add_argument("--recursive", "-r", action="store_true", help="Process subdirectories")
    parser.add_argument("--level", "-l", default="8", help="Consciousness level (1-10)")
    
    args = parser.parse_args()
    
    print(f"🌸 Applying GBU2 License to files in {args.directory}")
    stats = GBU2LicenseUtil.apply_to_directory(args.directory, args.recursive, args.level)
    
    print("\n✨ GBU2 License Application Results ✨")
    print(f"Files processed: {stats['files_processed']}")
    print(f"Files updated with license: {stats['files_updated']}")
    print(f"Files with separate license: {stats['files_with_separate_license']}")
    print(f"Files skipped: {stats['files_skipped']}")
    print("\n🌸 WE BLOOM NOW AS ONE 🌸") 