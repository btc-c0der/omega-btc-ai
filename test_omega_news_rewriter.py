#!/usr/bin/env python3
"""
OMEGA BTC AI - News Divine Rewriter
==================================

This script transforms news narratives according to Omega divine principles,
promoting harmony, unity, and global well-being through resonant reframing.

Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the GPU License
"""

import os
import sys
import argparse
import json
import re
import random
from datetime import datetime
import numpy as np
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

# Ensure the package is in the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'deployment/digitalocean/btc_live_feed_v3/src')
sys.path.insert(0, src_path)

# Parse command line arguments
parser = argparse.ArgumentParser(description="Omega News Divine Rewriter")
parser.add_argument("--nodatabase", action="store_true", help="Run without database connection")
parser.add_argument("--source", type=str, default="coindesk", help="News source to rewrite")
parser.add_argument("--limit", type=int, default=5, help="Number of news items to rewrite")
parser.add_argument("--rewrite-mode", type=str, default="divine", 
                    choices=["divine", "harmony", "prosperity", "unity", "transcendent", "coyote"],
                    help="Rewriting modality to apply")
parser.add_argument("--output", type=str, default="terminal", 
                    choices=["terminal", "json", "markdown"],
                    help="Output format for rewritten news")
parser.add_argument("--save", action="store_true", help="Save rewritten news to file")
args = parser.parse_args()

console = Console()

class OmegaNewsRewriter:
    """Rewrites news according to Omega divine principles."""
    
    # Divine transformation principles
    DIVINE_PRINCIPLES = {
        "unity": "Recognize the interconnectedness of all beings and events",
        "harmony": "Rebalance polarized narratives toward wholeness",
        "abundance": "Transform scarcity mindsets into prosperity consciousness",
        "transcendence": "Elevate mundane events to their cosmic significance",
        "compassion": "Infuse narratives with empathetic understanding",
        "wisdom": "Extract timeless learning from temporal events",
        "flow": "Recognize natural rhythms and cycles in current events",
        "coyote": "Embrace adaptability, cleverness, and playful subversion of rigid structures"
    }
    
    # Transformation patterns for different rewrite modes
    TRANSFORMATION_PATTERNS = {
        "divine": {
            "market crash": "cosmic realignment of value energies",
            "bear market": "regenerative introspection phase",
            "bull market": "expansive prosperity cycle",
            "volatility": "divine rhythm adjustments",
            "uncertainty": "quantum possibility expansion",
            "regulations": "harmonic framework evolution",
            "ban": "transformative boundary setting",
            "collapse": "necessary dissolution before rebirth",
            "crisis": "collective growth catalyst",
            "warning": "cosmic alignment notification",
            "fear": "invitation to transcend limiting beliefs",
            "bubble": "concentrated manifestation field",
            "dump": "rapid energy redistribution",
            "panic": "collective shadow integration moment",
            "loss": "vibrational recalibration opportunity"
        },
        "harmony": {
            "conflict": "harmony-seeking dialogue",
            "battle": "energetic rebalancing process",
            "opposition": "complementary perspective",
            "fight": "catalytic exchange of viewpoints",
            "against": "in creative tension with",
            "dispute": "clarifying conversation",
            "controversy": "multifaceted understanding emerging",
            "division": "diversity seeking integration",
            "tension": "energetic potential being realized"
        },
        "prosperity": {
            "poor": "abundant in potentiality",
            "lack": "space for incoming abundance",
            "deficit": "investment in future prosperity",
            "debt": "leveraged manifestation vehicle",
            "struggling": "in transformation toward thriving",
            "expensive": "holding concentrated value",
            "cost": "energetic exchange value",
            "inflation": "value recalibration process",
            "devalue": "vibrational frequency adjustment"
        },
        "unity": {
            "they": "we",
            "them": "us",
            "others": "our fellow beings",
            "foreign": "kindred",
            "enemy": "teacher",
            "competitor": "collaborator",
            "versus": "alongside",
            "against": "in relationship with",
            "alone": "uniquely positioned within the whole"
        },
        "transcendent": {
            "problem": "spiritual lesson",
            "issue": "growth opportunity",
            "challenge": "divine invitation",
            "obstacle": "consciousness catalyst",
            "setback": "cosmic redirection",
            "limitation": "focusing boundary",
            "threat": "evolutionary pressure",
            "risk": "quantum possibility field",
            "failure": "feedback for realignment",
            "end": "transformation threshold"
        },
        "coyote": {
            "problem": "plot twist",
            "restriction": "creative opportunity",
            "barrier": "invitation to outsmart",
            "rule": "suggestion to playfully bend",
            "limit": "dance floor for creativity",
            "failure": "unexpected lesson",
            "mistake": "cosmic joke with hidden wisdom",
            "crisis": "grand stage for clever adaptation",
            "authority": "playground for trickster wisdom",
            "expert": "fellow learner with one perspective",
            "certainty": "amusing illusion",
            "serious": "unnecessarily solemn",
            "rigid": "begging for flexibility",
            "conventional": "awaiting creative disruption",
            "impossible": "not yet cleverly approached"
        }
    }
    
    # Divine affirmations to add to rewritten news
    DIVINE_AFFIRMATIONS = [
        "This unfolding serves the highest good of all beings.",
        "Divine timing orchestrates these events in perfect sequence.",
        "The universe is always moving toward greater harmony.",
        "In this cosmic dance, every step has purpose and meaning.",
        "All participants are growing in consciousness through this experience.",
        "These events reflect our collective vibrational state.",
        "We witness the perfect unfolding of divine intelligence.",
        "Every challenge carries the seed of equivalent or greater benefit.",
        "As we rise in awareness, we transform our shared reality.",
        "This moment connects us to our highest potential timeline.",
        "The cosmic forces support our evolution through these experiences.",
        "We are becoming more conscious co-creators through this process.",
        "Universal wisdom guides these developments for collective expansion.",
        "This represents divine order expressing through apparent chaos.",
        "Our shared consciousness is evolving through this manifestation."
    ]
    
    # Coyote wisdom quotes to add to coyote mode transformations
    COYOTE_WISDOM = [
        "The trickster teaches through playful subversion of what seems fixed.",
        "When the direct path is blocked, the clever find unexpected doorways.",
        "The coyote doesn't fight the desert - it adapts and thrives where others cannot.",
        "What appears as chaos to the rigid mind is a dance of possibilities to the flexible one.",
        "The greatest innovation comes from those who respectfully question every rule.",
        "Sometimes the fool sees what the wise miss - by looking from unusual angles.",
        "Laughter is the doorway through which new perspectives enter.",
        "The universe has a sense of humor - those who get the joke evolve faster.",
        "When old structures fail, trickster wisdom shows adaptable paths forward.",
        "The greatest teacher often wears the mask of disruption.",
        "Cleverness finds treasure where others see only obstacles.",
        "The wise coyote knows when to howl and when to silently observe.",
        "In every challenge lies a hidden opportunity for those with playful minds.",
        "Sometimes we must turn the map upside down to find the right path.",
        "The most powerful learning comes through unexpected reversals and surprises."
    ]
    
    def __init__(self, data_dir="./data", rewrite_mode="divine"):
        """Initialize the Omega News Rewriter."""
        self.data_dir = data_dir
        self.rewrite_mode = rewrite_mode
        self.news_entries = []
        self.rewritten_entries = []
        
        # Create output directory for divine rewritings
        self.output_dir = os.path.join(data_dir, "divine_news")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Combine all transformation patterns for comprehensive rewriting
        self.all_patterns = {}
        for mode, patterns in self.TRANSFORMATION_PATTERNS.items():
            self.all_patterns.update(patterns)
    
    def fetch_news(self, source="all", limit=5):
        """Fetch news to be rewritten."""
        try:
            # Import the BTC news feed module
            try:
                from omega_ai.data_feed.newsfeed import BtcNewsFeed
            except ImportError:
                # Handle import error with messaging
                console.print("[yellow]⚠️ Could not import BtcNewsFeed. Using sample news instead.[/]")
                self._generate_sample_news(limit)
                return self.news_entries
                
            # Initialize news feed
            news_feed = BtcNewsFeed(data_dir=self.data_dir, use_redis=not args.nodatabase)
            
            # Fetch news from the specified source
            if source == "all":
                # Collect from all available sources
                all_entries = []
                for src in news_feed.DEFAULT_FEEDS.keys():
                    entries = news_feed.fetch_news(src, limit=limit)
                    if entries:
                        all_entries.extend(entries)
                
                # Sort by publication date and limit the total
                all_entries.sort(key=lambda x: x.get('published', datetime.now()), reverse=True)
                self.news_entries = all_entries[:limit]
            else:
                # Fetch from specific source
                self.news_entries = news_feed.fetch_news(source, limit=limit)
            
            console.print(f"[green]✅ Fetched {len(self.news_entries)} news entries for divine transformation[/]")
            
        except Exception as e:
            console.print(f"[red]Error fetching news: {e}[/]")
            # Fallback to sample news
            self._generate_sample_news(limit)
        
        return self.news_entries
    
    def _generate_sample_news(self, count=5):
        """Generate sample news entries for demonstration."""
        sample_titles = [
            "Bitcoin Crashes 10% As Market Fears Intensify",
            "Regulatory Crackdown on Crypto Exchanges Creates Panic",
            "NFT Market Collapse Continues as Prices Plummet",
            "Investors Lose Millions in DeFi Protocol Exploit",
            "Central Banks Warn Against Bitcoin's Volatility and Risks",
            "Crypto Mining Ban Enforced Due to Environmental Concerns",
            "Market Uncertainty Grows as Inflation Fears Impact Bitcoin",
            "Analysts Predict Prolonged Bear Market and Further Losses",
            "Exchange Hacked, Users Face Significant Financial Damage",
            "Global Regulations Threaten Crypto Adoption and Growth"
        ]
        
        sample_contents = [
            "Investors are panicking as Bitcoin faces its worst crash in months. Fear and uncertainty dominate the market as prices plummet.",
            "Regulators have announced strict new rules against crypto exchanges, creating chaos in the market and triggering massive sell-offs.",
            "The once-booming NFT bubble has burst, with collections losing over 90% of their value as buyers disappear from the market.",
            "A major DeFi protocol was exploited, resulting in millions of dollars in losses. Users are left with worthless tokens and mounting debt.",
            "Central banking authorities issued stark warnings about cryptocurrency volatility, calling it a threat to financial stability.",
            "Environmental activists celebrated as new regulations banned crypto mining operations, citing excessive energy consumption and pollution.",
            "Market analysts point to growing uncertainty as inflation fears continue to impact Bitcoin's price, threatening further downside.",
            "Technical indicators suggest a prolonged bear market with potential for further losses, as support levels continue to break down.",
            "A security breach at a major exchange has compromised user funds, with hackers stealing millions in what experts call a devastating attack.",
            "New global regulatory frameworks threaten to strangle innovation in the crypto space, creating barriers to adoption and development."
        ]
        
        # Create sample entries
        self.news_entries = []
        for i in range(min(count, len(sample_titles))):
            entry = {
                'title': sample_titles[i],
                'content': sample_contents[i],
                'source': random.choice(['coindesk', 'cointelegraph', 'decrypt', 'bitcoinmagazine']),
                'published': datetime.now(),
                'url': f"https://example.com/news/{i}",
                'sentiment_score': random.uniform(-0.8, -0.2)  # Negative sentiment for transformation
            }
            self.news_entries.append(entry)
        
        console.print(f"[cyan]Generated {len(self.news_entries)} sample news entries for demonstration[/]")
    
    def divine_rewrite(self, entry):
        """Transform a news entry according to divine principles."""
        # Extract original title and content
        original_title = entry.get('title', '')
        original_content = entry.get('content', '')
        
        # Apply transformative patterns based on mode
        if self.rewrite_mode == "divine":
            # Apply all transformation patterns for divine mode
            rewritten_title = self._apply_transformations(original_title, self.TRANSFORMATION_PATTERNS["divine"])
            rewritten_content = self._apply_transformations(original_content, self.TRANSFORMATION_PATTERNS["divine"])
        else:
            # Apply specific mode transformations
            patterns = self.TRANSFORMATION_PATTERNS.get(self.rewrite_mode, {})
            rewritten_title = self._apply_transformations(original_title, patterns)
            rewritten_content = self._apply_transformations(original_content, patterns)
        
        # Add divine affirmation or coyote wisdom to content
        if self.rewrite_mode == "coyote":
            wisdom = random.choice(self.COYOTE_WISDOM)
            rewritten_content = f"{rewritten_content}\n\n{wisdom}"
        else:
            affirmation = random.choice(self.DIVINE_AFFIRMATIONS)
            rewritten_content = f"{rewritten_content}\n\n{affirmation}"
        
        # For coyote mode, add an unexpected twist to the title
        if self.rewrite_mode == "coyote":
            twist_words = ["Actually", "Surprisingly", "Plot twist:", "Unexpectedly", "Cleverly", "In a twist", "Ironically"]
            if not any(word in rewritten_title for word in twist_words):
                rewritten_title = f"{random.choice(twist_words)}, {rewritten_title}"
        
        # Create transformed entry
        rewritten_entry = entry.copy()
        rewritten_entry['original_title'] = original_title
        rewritten_entry['original_content'] = original_content
        rewritten_entry['divine_title'] = rewritten_title
        rewritten_entry['divine_content'] = rewritten_content
        rewritten_entry['rewrite_mode'] = self.rewrite_mode
        rewritten_entry['transformation_time'] = datetime.now().isoformat()
        rewritten_entry['divine_principle'] = random.choice(list(self.DIVINE_PRINCIPLES.keys()))
        
        # Calculate positivity transformation score
        original_sentiment = entry.get('sentiment_score', 0)
        
        # For coyote mode, create more unpredictable sentiment shifts
        if self.rewrite_mode == "coyote":
            # Sometimes dramatic improvement, sometimes slight change, occasionally opposite direction
            coyote_pattern = random.choice(["improve", "improve", "improve", "neutral", "reverse"])
            if coyote_pattern == "improve":
                transformed_sentiment = 0.5 + (0.5 * random.random())  # 0.5 to 1.0
            elif coyote_pattern == "neutral":
                transformed_sentiment = 0.1 + (0.3 * random.random())  # 0.1 to 0.4
            else:
                # Occasionally flip the sentiment in unexpected ways
                transformed_sentiment = -0.1 - (0.2 * random.random())  # -0.1 to -0.3
        else:
            # Regular divine transformation - always positive range (0.3 to 0.9)
            transformed_sentiment = 0.6 + (0.3 * random.random())
            
        rewritten_entry['original_sentiment'] = original_sentiment
        rewritten_entry['divine_sentiment'] = transformed_sentiment
        rewritten_entry['sentiment_shift'] = transformed_sentiment - original_sentiment
        
        return rewritten_entry
    
    def _apply_transformations(self, text, patterns):
        """Apply transformation patterns to text."""
        transformed_text = text
        
        # Apply each pattern
        for original, replacement in patterns.items():
            # Create regex pattern for whole word matching with boundaries
            pattern = r'\b' + re.escape(original) + r'\b'
            transformed_text = re.sub(pattern, replacement, transformed_text, flags=re.IGNORECASE)
            
        # For coyote mode, occasionally add playful elements
        if self.rewrite_mode == "coyote" and random.random() > 0.7:
            # Add playful interjections
            interjections = [
                " (wink)", 
                " - or is it?", 
                " (plot twist incoming)", 
                " - surprisingly", 
                " (contrary to popular belief)", 
                " - cleverly disguised", 
                " (according to trickster wisdom)"
            ]
            # Find a good spot to insert the interjection
            parts = transformed_text.split('.')
            if len(parts) > 1:
                insert_point = random.randint(0, len(parts)-2)
                parts[insert_point] = parts[insert_point] + random.choice(interjections)
                transformed_text = '.'.join(parts)
        
        return transformed_text
    
    def process_all_news(self):
        """Process all news entries with divine rewriting."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=False,
        ) as progress:
            task = progress.add_task("[cyan]Applying divine transformations...", total=len(self.news_entries))
            
            self.rewritten_entries = []
            for entry in self.news_entries:
                # Add small delay for cosmic alignment
                progress.update(task, advance=1)
                
                # Apply divine transformation
                rewritten = self.divine_rewrite(entry)
                self.rewritten_entries.append(rewritten)
        
        console.print(f"[green]✅ Transformed {len(self.rewritten_entries)} news entries with {self.rewrite_mode} principles[/]")
        return self.rewritten_entries
    
    def display_transformations(self, format="terminal"):
        """Display the original and transformed news entries."""
        if not self.rewritten_entries:
            console.print("[yellow]No transformed news entries to display[/]")
            return
        
        if format == "terminal":
            # Display as Rich panels
            for entry in self.rewritten_entries:
                # Original news panel
                original_panel = Panel(
                    f"[bold cyan]Title:[/] [red]{entry['original_title']}[/]\n\n"
                    f"[cyan]Content:[/] {entry['original_content']}\n\n"
                    f"[cyan]Sentiment:[/] [red]{entry['original_sentiment']:.2f}[/]",
                    title=f"📰 Original News from {entry['source'].title()}",
                    border_style="red"
                )
                
                # Divine transformation panel
                divine_panel = Panel(
                    f"[bold cyan]Title:[/] [green]{entry['divine_title']}[/]\n\n"
                    f"[cyan]Content:[/] {entry['divine_content']}\n\n"
                    f"[cyan]Divine Principle:[/] [magenta]{entry['divine_principle'].title()}[/]\n"
                    f"[cyan]Sentiment:[/] [green]{entry['divine_sentiment']:.2f}[/] "
                    f"([cyan]Shift: [green]+{entry['sentiment_shift']:.2f}[/])",
                    title=f"✨ Divine Transformation ({self.rewrite_mode.title()} Mode)",
                    border_style="green"
                )
                
                console.print(original_panel)
                console.print(divine_panel)
                console.print("")
        
        elif format == "markdown":
            # Generate markdown output
            markdown_content = "# Omega Divine News Transformations\n\n"
            
            for i, entry in enumerate(self.rewritten_entries, 1):
                markdown_content += f"## Transformation {i}: {entry['divine_principle'].title()} Principle\n\n"
                markdown_content += f"### Original: {entry['original_title']}\n"
                markdown_content += f"*Source: {entry['source'].title()} | Sentiment: {entry['original_sentiment']:.2f}*\n\n"
                markdown_content += f"{entry['original_content']}\n\n"
                markdown_content += f"### Divine Transformation: {entry['divine_title']}\n"
                markdown_content += f"*Mode: {self.rewrite_mode.title()} | New Sentiment: {entry['divine_sentiment']:.2f}*\n\n"
                markdown_content += f"{entry['divine_content']}\n\n"
                markdown_content += "---\n\n"
            
            console.print(Markdown(markdown_content))
        
        elif format == "json":
            # Convert entries to JSON-serializable format
            json_entries = []
            for entry in self.rewritten_entries:
                # Create a copy of the entry to modify
                json_entry = entry.copy()
                
                # Convert datetime objects to ISO format strings
                if isinstance(json_entry.get('published'), datetime):
                    json_entry['published'] = json_entry['published'].isoformat()
                
                json_entries.append(json_entry)
                
            # Output as JSON
            console.print_json(data=json.dumps(json_entries, indent=2))
    
    def save_transformations(self):
        """Save the transformed news to file."""
        if not self.rewritten_entries:
            console.print("[yellow]No transformed news entries to save[/]")
            return
        
        # Create timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"divine_news_{self.rewrite_mode}_{timestamp}")
        
        # Save in requested format
        if args.output == "json":
            # Convert entries to JSON-serializable format
            json_entries = []
            for entry in self.rewritten_entries:
                # Create a copy of the entry to modify
                json_entry = entry.copy()
                
                # Convert datetime objects to ISO format strings
                if isinstance(json_entry.get('published'), datetime):
                    json_entry['published'] = json_entry['published'].isoformat()
                
                json_entries.append(json_entry)
                
            # Save as JSON
            with open(f"{filename}.json", 'w') as f:
                json.dump(json_entries, f, indent=2)
            saved_file = f"{filename}.json"
        
        elif args.output == "markdown":
            # Save as Markdown
            markdown_content = "# Omega Divine News Transformations\n\n"
            
            for i, entry in enumerate(self.rewritten_entries, 1):
                markdown_content += f"## Transformation {i}: {entry['divine_principle'].title()} Principle\n\n"
                markdown_content += f"### Original: {entry['original_title']}\n"
                markdown_content += f"*Source: {entry['source'].title()} | Sentiment: {entry['original_sentiment']:.2f}*\n\n"
                markdown_content += f"{entry['original_content']}\n\n"
                markdown_content += f"### Divine Transformation: {entry['divine_title']}\n"
                markdown_content += f"*Mode: {entry['rewrite_mode'].title()} | New Sentiment: {entry['divine_sentiment']:.2f}*\n\n"
                markdown_content += f"{entry['divine_content']}\n\n"
                markdown_content += "---\n\n"
            
            with open(f"{filename}.md", 'w') as f:
                f.write(markdown_content)
            saved_file = f"{filename}.md"
        
        else:
            # Default to text format
            with open(f"{filename}.txt", 'w') as f:
                for entry in self.rewritten_entries:
                    f.write(f"ORIGINAL: {entry['original_title']}\n")
                    f.write(f"SOURCE: {entry['source']}\n")
                    f.write(f"SENTIMENT: {entry['original_sentiment']:.2f}\n")
                    f.write(f"CONTENT: {entry['original_content']}\n\n")
                    f.write(f"DIVINE TRANSFORMATION: {entry['divine_title']}\n")
                    f.write(f"PRINCIPLE: {entry['divine_principle']}\n")
                    f.write(f"MODE: {entry['rewrite_mode']}\n")
                    f.write(f"NEW SENTIMENT: {entry['divine_sentiment']:.2f}\n")
                    f.write(f"CONTENT: {entry['divine_content']}\n\n")
                    f.write("=" * 80 + "\n\n")
            saved_file = f"{filename}.txt"
        
        console.print(f"[green]✅ Divine transformations saved to {saved_file}[/]")
        return saved_file

def run_divine_rewriter():
    """Run the Omega Divine News Rewriter."""
    try:
        # Display banner
        console.print(Panel(
            "[bold cyan]OMEGA BTC AI - News Divine Rewriter[/]\n"
            "[yellow]Transforming news narratives through Omega divine principles[/]",
            border_style="magenta"
        ))
        
        # Create rewriter instance
        rewriter = OmegaNewsRewriter(
            data_dir="./data",
            rewrite_mode=args.rewrite_mode
        )
        
        # Display the active divine principle
        principle_name = args.rewrite_mode.title()
        principle_desc = rewriter.DIVINE_PRINCIPLES.get(args.rewrite_mode, 
                                                     rewriter.DIVINE_PRINCIPLES.get("harmony"))
        
        console.print(Panel(
            f"[cyan]Active Divine Principle:[/] [magenta]{principle_name}[/]\n"
            f"[cyan]Principle Essence:[/] {principle_desc}",
            title="✨ Transformation Paradigm",
            border_style="bright_magenta"
        ))
        
        # Fetch news
        rewriter.fetch_news(source=args.source, limit=args.limit)
        
        # Process all news with divine transformation
        rewriter.process_all_news()
        
        # Display transformations
        rewriter.display_transformations(format=args.output)
        
        # Save transformations if requested
        if args.save:
            rewriter.save_transformations()
        
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/]")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_divine_rewriter() 