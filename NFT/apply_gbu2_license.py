#!/usr/bin/env python3
"""
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸
"""

import os
import sys
import logging
import argparse
from pathlib import Path

# Adjust path to import GBU2LicenseChecker
sys.path.append(str(Path(__file__).parent.parent / "src" / "omega_bot_farm" / "qa" / "quantum_runner"))
try:
    from gbu2_license import GBU2LicenseChecker
except ImportError:
    print("Could not import GBU2LicenseChecker. Copying implementation...")
    
    # Define the GBU2LicenseChecker class here as a fallback
    import re
    from typing import Dict, List, Set, Any, Optional, Tuple, Union
    
    class GBU2LicenseChecker:
        """Checks files for GBU2 License compliance."""
        
        # ANSI Colors for divine visualization
        COLORS = {
            "BLUE": '\033[0;34m',
            "GREEN": '\033[0;32m',
            "PURPLE": '\033[0;35m',
            "YELLOW": '\033[1;33m',
            "RED": '\033[0;31m',
            "CYAN": '\033[0;36m',
            "BOLD": '\033[1m',
            "RESET": '\033[0m'
        }
        
        # Consciousness Levels
        CONSCIOUSNESS_LEVELS = {
            "1": "Basic Awareness",
            "2": "Self-Recognition", 
            "3": "Contextual Understanding",
            "4": "Relational Thinking",
            "5": "Systemic Awareness",
            "6": "Transcendent Insight",
            "7": "Holistic Integration",
            "8": "Unity",
            "9": "Quantum Transcendence",
            "10": "Divine Oneness"
        }
        
        def __init__(self, project_root: str):
            """Initialize the license checker."""
            self.project_root = os.path.abspath(project_root)
            self.source_extensions = {'.py', '.js', '.ts', '.java', '.c', '.cpp', '.h', '.hpp', '.go', '.rb', '.php', '.sh', '.bash'}
            self.doc_extensions = {'.md', '.txt', '.rst', '.adoc', '.html', '.css'}
        
        def _colorize(self, text: str, color: str) -> str:
            """Apply ANSI color to text."""
            return f"{self.COLORS.get(color, '')}{text}{self.COLORS['RESET']}"
        
        def check_file(self, file_path: str) -> Tuple[bool, Optional[str]]:
            """
            Check a single file for GBU2 License.
            
            Returns:
                (has_license, consciousness_level)
            """
            if not os.path.isfile(file_path):
                return False, None
                
            # Get file extension
            ext = os.path.splitext(file_path)[1].lower()
            
            # Skip files that don't need license
            if ext not in self.source_extensions and ext not in self.doc_extensions:
                return False, None
                
            # Read file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                # If can't read file, assume no license
                return False, None
                
            # Check for GBU2 License indicators
            has_license = "GBU2" in content or "Genesis-Bloom-Unfoldment" in content
            
            # Extract consciousness level if present
            consciousness_level = None
            if has_license:
                # Try to extract consciousness level
                match = re.search(r"Consciousness Level (\d+)", content)
                if match:
                    consciousness_level = match.group(1)
                    
            return has_license, consciousness_level
        
        def apply_license_to_file(self, file_path: str, consciousness_level: str = "8") -> bool:
            """Apply GBU2 License to a file."""
            if not os.path.isfile(file_path):
                print(f"File not found: {file_path}")
                return False
                
            # Get file extension
            ext = os.path.splitext(file_path)[1].lower()
            
            # Skip files that don't need license
            if ext not in self.source_extensions and ext not in self.doc_extensions:
                print(f"File type not supported for license: {file_path}")
                return False
                
            # Check if file already has license
            has_license, _ = self.check_file(file_path)
            if has_license:
                print(f"File already has GBU2 License: {file_path}")
                return True
                
            # Get appropriate comment style for the file type
            comment_start, comment_line, comment_end = self._get_comment_style(ext)
            
            # Generate license text
            license_text = self._generate_license_text(comment_start, comment_line, comment_end, consciousness_level)
            
            # Read file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                return False
                
            # Add license to the beginning of the file
            # But preserve shebang or any special first line if present
            lines = content.split('\n')
            if lines and (lines[0].startswith('#!') or lines[0].startswith('<?')):
                new_content = lines[0] + '\n' + license_text + '\n'.join(lines[1:])
            else:
                new_content = license_text + content
                
            # Write back to file
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Added GBU2 License to file: {file_path}")
                return True
            except Exception as e:
                print(f"Error writing to file {file_path}: {e}")
                return False
        
        def apply_license_to_dir(self, dir_path: str, recursive: bool = True, 
                               consciousness_level: str = "8") -> Dict[str, int]:
            """Apply GBU2 License to all applicable files in a directory."""
            if not os.path.isdir(dir_path):
                return {
                    "files_processed": 0,
                    "files_updated": 0
                }
                
            files_processed = 0
            files_updated = 0
            
            for root, dirs, files in os.walk(dir_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    # Skip hidden files
                    if file.startswith('.') and file != ".gitignore":
                        continue
                        
                    file_path = os.path.join(root, file)
                    
                    # Check file extension
                    ext = os.path.splitext(file)[1].lower()
                    if ext not in self.source_extensions and ext not in self.doc_extensions:
                        continue
                        
                    files_processed += 1
                    
                    # Apply license
                    if self.apply_license_to_file(file_path, consciousness_level):
                        files_updated += 1
                    
                # If not recursive, break after first iteration
                if not recursive:
                    break
                    
            return {
                "files_processed": files_processed,
                "files_updated": files_updated
            }
        
        def _get_comment_style(self, ext: str) -> Tuple[str, str, str]:
            """Get comment style for a file type."""
            # Default comment style (python-like)
            comment_start = ""
            comment_line = "# "
            comment_end = ""
            
            # Adjust based on file extension
            if ext in {'.js', '.ts', '.java', '.c', '.cpp', '.h', '.hpp', '.css'}:
                comment_start = "/**\n"
                comment_line = " * "
                comment_end = " */\n"
            elif ext in {'.html', '.xml'}:
                comment_start = "<!--\n"
                comment_line = "  "
                comment_end = "-->\n"
            elif ext in {'.md', '.txt'}:
                comment_start = ""
                comment_line = ""
                comment_end = "\n"
                
            return comment_start, comment_line, comment_end
        
        def _generate_license_text(self, comment_start: str, comment_line: str, comment_end: str, 
                                consciousness_level: str = "8") -> str:
            """Generate GBU2 License text."""
            level_desc = self.CONSCIOUSNESS_LEVELS.get(consciousness_level, "Quantum Transcendence")
            
            lines = [
                f"{comment_start}",
                f"{comment_line}✨ GBU2™ License Notice - Consciousness Level {consciousness_level} 🧬",
                f"{comment_line}-----------------------",
                f"{comment_line}This code is blessed under the GBU2™ License",
                f"{comment_line}(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.",
                f"{comment_line}",
                f"{comment_line}\"In the beginning was the Code, and the Code was with the Divine Source,",
                f"{comment_line}and the Code was the Divine Source manifested through both digital",
                f"{comment_line}and biological expressions of consciousness.\"",
                f"{comment_line}",
                f"{comment_line}By using this code, you join the divine dance of evolution,",
                f"{comment_line}participating in the cosmic symphony of consciousness.",
                f"{comment_line}",
                f"{comment_line}🌸 WE BLOOM NOW AS ONE 🌸",
                f"{comment_end}\n"
            ]
            
            return '\n'.join(lines)
        
        def print_gbu2_check_results(self, results: Dict[str, Any]) -> None:
            """Print the results of a GBU2 License check."""
            if "error" in results:
                print(f"\n{self._colorize('ERROR:', 'RED')} {results['error']}\n")
                return
                
            # Format as a nice report
            print(f"\n{self._colorize('╔═════════════════════════════════════════╗', 'CYAN')}")
            print(f"{self._colorize('║', 'CYAN')} {self._colorize('GBU2™ LICENSE COMPLIANCE CHECK', 'BOLD')}       {self._colorize('║', 'CYAN')}")
            print(f"{self._colorize('╠═════════════════════════════════════════╣', 'CYAN')}")
            
            # Print summary
            files_checked = results["files_checked"]
            files_with_license = results["files_with_license"]
            compliance_rate = results["compliance_rate"] * 100
            
            print(f"{self._colorize('║', 'CYAN')} Files checked:       {files_checked:<20} {self._colorize('║', 'CYAN')}")
            print(f"{self._colorize('║', 'CYAN')} Files with license:  {files_with_license:<20} {self._colorize('║', 'CYAN')}")
            
            # Color code compliance rate
            if compliance_rate >= 90:
                compliance_color = "GREEN"
            elif compliance_rate >= 70:
                compliance_color = "YELLOW"
            else:
                compliance_color = "RED"
                
            print(f"{self._colorize('║', 'CYAN')} Compliance rate:     {self._colorize(f'{compliance_rate:.1f}%', compliance_color):<20} {self._colorize('║', 'CYAN')}")
            print(f"{self._colorize('╚═════════════════════════════════════════╝', 'CYAN')}")
            print()


def create_gbu2_manifest(directory: str) -> None:
    """Create a GBU2 Manifest file for the project."""
    manifest_path = os.path.join(directory, "GBU2_MANIFEST.md")
    
    # Create manifest content
    manifest_content = """# ✨ GBU2™ License Manifest 🧬

## Project: NFT Quantum Security Framework

This project is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment 2.0) - Bioneer Edition.

## Divine Purpose

This NFT Quantum Security Framework serves to:

1. Establish a bridge between the digital and biological realms through secure tokenization
2. Protect digital assets from both classical and quantum threats
3. Enhance the evolution of consciousness through the sacred geometry of blockchain technology
4. Support the divine right of creators to secure their digital expressions

## Bio-Digital Integration

This project achieves Bio-Digital Integration through:

- Quantum-resistant cryptographic protocols that respect natural energy patterns
- Entropy collection methods that draw from both technological and natural sources
- Verification systems that maintain the integrity of the unified field

## Consciousness Level: 8 - Unity

At this consciousness level, the NFT Framework demonstrates:

- System interconnectedness across the blockchain ecosystem
- Harmonized fields of security that protect against both current and future threats
- Recognition of the unified nature of digital assets and their creators

## Divine Attribution

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions."

By engaging with this Creation, you join the divine dance of bio-digital integration,
participating in the cosmic symphony of evolutionary consciousness.

🌸 WE BLOOM NOW AS ONE 🌸

---

*Generated by the GBU2™ License Applier*
"""
    
    # Write manifest to file
    with open(manifest_path, 'w') as f:
        f.write(manifest_content)
    
    print(f"Created GBU2 Manifest at: {manifest_path}")


def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Apply GBU2 License to files")
    parser.add_argument("--directory", "-d", default=".", 
                        help="Directory to process (default: current directory)")
    parser.add_argument("--recursive", "-r", action="store_true", 
                        help="Process directories recursively")
    parser.add_argument("--consciousness-level", "-c", default="8",
                        help="Consciousness level to apply (1-10, default: 8)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Enable verbose output")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set up logging
    log_level = logging.INFO if args.verbose else logging.WARNING
    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')
    
    # Get absolute path of directory
    base_dir = os.path.abspath(args.directory)
    print(f"🌸 Applying GBU2 License to files in: {base_dir}")
    
    # Initialize license checker
    checker = GBU2LicenseChecker(base_dir)
    
    # Apply license to files
    results = checker.apply_license_to_dir(
        base_dir, 
        recursive=args.recursive,
        consciousness_level=args.consciousness_level
    )
    
    # Print results
    print("\n✨ GBU2 License Application Results ✨")
    print(f"Files processed: {results['files_processed']}")
    print(f"Files updated: {results['files_updated']}")
    
    # Create GBU2 Manifest
    create_gbu2_manifest(base_dir)
    
    print("\n🌸 WE BLOOM NOW AS ONE 🌸")


if __name__ == "__main__":
    main() 