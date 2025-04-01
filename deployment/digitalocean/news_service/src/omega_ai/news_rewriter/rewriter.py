#!/usr/bin/env python3
"""
OMEGA BTC AI - Divine News Rewriter Module
==========================================

This module provides functionality to rewrite news according to Omega divine principles,
transforming chaotic narratives into harmonious perspectives aligned with cosmic truth.

Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the GPU License
"""

import os
import re
import random
import json
from datetime import datetime
import logging
from pathlib import Path
import numpy as np

logger = logging.getLogger("divine-rewriter")

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
        "coyote": "Embrace adaptability, cleverness, and playful subversion of rigid structures",
        "whale": "Channel deep, powerful presence and the long-term perspective of oceanic wisdom"
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
        },
        "whale": {
            "short-term": "across the oceanic cycles",
            "quick": "profound and measured",
            "small": "vast and significant",
            "noise": "deep resonant call",
            "trivial": "part of the greater oceanic pattern",
            "temporary": "enduring through time's depths",
            "panic": "deep call for mindful presence",
            "urgent": "worthy of deliberate consideration",
            "trend": "movement in the greater currents",
            "local": "felt across the connected waters",
            "individual": "part of the pod's collective wisdom",
            "immediate": "unfolding across time's vastness",
            "surface-level": "reaching the profound depths",
            "isolated": "connected through unseen currents",
            "fleeting": "carried through time's enduring flow"
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
    
    # Whale wisdom quotes to add to whale mode transformations
    WHALE_WISDOM = [
        "The deepest currents move slowly but shape entire oceans.",
        "From the ocean's depths, both stillness and movement reveal their purpose.",
        "The greatest songs travel across vast distances, connecting what appears separate.",
        "True power lies in measured movement, not frantic activity.",
        "What seems monumental from the surface may be merely a ripple in the greater deep.",
        "The pod's wisdom exceeds the knowledge of any single swimmer.",
        "Beneath the surface storms, deeper waters remain calm and knowing.",
        "Time moves differently in the depths - what humans call a lifetime is but a single song.",
        "The ocean remembers what the land has forgotten.",
        "Size brings perspective - what seems enormous to some is but a moment in the vastness.",
        "Even the mightiest creatures know when to rise and when to dive deep.",
        "The ancient migration routes remind us that some paths transcend generations.",
        "Breathing consciously connects us to both worlds - above and below.",
        "The whale carries the memory of when all was water, before division.",
        "To navigate by sound rather than sight reveals hidden dimensions of reality."
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
            # Try to import BtcNewsFeed if available
            from omega_ai.data_feed.newsfeed import BtcNewsFeed
            
            # Create news feed instance
            news_feed = BtcNewsFeed(data_dir=self.data_dir)
            
            # Fetch news from the requested source
            self.news_entries = news_feed.fetch_news(source)
            logger.info(f"Fetched {len(self.news_entries)} news entries from {source}")
            
            # Limit results if requested
            if limit and limit < len(self.news_entries):
                self.news_entries = self.news_entries[:limit]
                
            return self.news_entries
            
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            
            # Generate sample news if can't fetch real news
            self._generate_sample_news(count=limit)
            return self.news_entries
    
    def _generate_sample_news(self, count=5):
        """Generate sample news entries for testing."""
        sample_sources = ["Coindesk", "Cointelegraph", "Bitcoinmagazine", "Decrypt", "TheBlock"]
        sample_titles = [
            "Bitcoin Crashes 10% As Market Fears Intensify",
            "Regulatory Crackdown on Crypto Exchanges Creates Panic",
            "Bitcoin Adoption Reaches All-Time High Despite Market Volatility",
            "Major Institutional Investors Turning to Bitcoin as Inflation Hedge",
            "Cryptocurrency Market Faces Uncertainty as Global Tensions Rise",
            "Bitcoin Mining Difficulty Increases Amid Energy Concerns",
            "New Cryptocurrency Regulations Proposed by Government",
            "Bitcoin Price Prediction: Analysts See Potential for New ATH This Year",
            "DeFi Projects Struggle as Market Sentiment Turns Bearish",
            "NFT Market Shows Signs of Recovery After Prolonged Slump"
        ]
        
        sample_contents = [
            "Investors are panicking as Bitcoin faces its worst crash in months. Fear and uncertainty dominate the market as prices plummet.",
            "Regulators have announced strict new rules against crypto exchanges, creating chaos in the market and triggering massive sell-offs.",
            "Despite recent price volatility, Bitcoin adoption metrics have reached an all-time high, with more users than ever entering the ecosystem.",
            "As inflation concerns grow, major institutional investors are increasingly turning to Bitcoin as a hedge against currency devaluation.",
            "The cryptocurrency market is facing growing uncertainty as global geopolitical tensions rise, affecting investor sentiment worldwide.",
            "Bitcoin's mining difficulty has increased significantly, raising concerns about energy consumption and environmental impact.",
            "Government officials have proposed sweeping new cryptocurrency regulations that could reshape the entire industry landscape.",
            "Several prominent analysts have released bullish Bitcoin price predictions, citing institutional adoption and scarcity as key factors.",
            "Decentralized finance projects are facing challenges as market sentiment shifts bearish and liquidity dries up across protocols.",
            "After months of declining sales and interest, the NFT market is showing early signs of recovery with several successful new launches."
        ]
        
        # Create sample entries
        self.news_entries = []
        for i in range(min(count, len(sample_titles))):
            sentiment_score = random.uniform(-0.8, 0.3)  # Generally negative to neutral
            
            entry = {
                "title": sample_titles[i],
                "content": sample_contents[i],
                "source": random.choice(sample_sources),
                "published": datetime.now(),
                "url": f"https://example.com/news/{i}",
                "sentiment_score": sentiment_score,
                "sentiment_label": "negative" if sentiment_score < -0.1 else "neutral"
            }
            
            self.news_entries.append(entry)
            
        logger.info(f"Generated {len(self.news_entries)} sample news entries for demonstration")
    
    def divine_rewrite(self, entry):
        """Apply divine rewriting to a news entry."""
        title = entry.get("title", "")
        content = entry.get("content", "")
        source = entry.get("source", "Unknown")
        
        # Convert to lowercase for pattern matching but preserve the original
        original_title = title
        original_content = content
        
        title_lower = title.lower()
        content_lower = content.lower()
        
        # Get patterns for the selected rewrite mode
        patterns = self.TRANSFORMATION_PATTERNS.get(self.rewrite_mode, {})
        
        # Use all patterns if divine mode is selected
        if self.rewrite_mode == "divine":
            patterns = self.all_patterns
        
        # Apply transformations to title and content
        transformed_title = original_title
        transformed_content = original_content
        
        # Apply mode-specific title transformations
        if self.rewrite_mode == "coyote":
            # Add unexpected prefixes for coyote mode
            coyote_prefixes = ["Cleverly,", "Unexpectedly,", "Plot twist:", "Creatively,", "In a playful turn,"]
            transformed_title = f"{random.choice(coyote_prefixes)} {original_title}"
        elif self.rewrite_mode == "whale":
            # Add ocean depth to whale mode
            whale_prefixes = ["From the depths:", "Across vast currents:", "In oceanic perspective:", "Beyond surface waves:"]
            transformed_title = f"{random.choice(whale_prefixes)} {original_title}"
        
        # Apply text pattern replacements for content
        transformed_content = self._apply_transformations(original_content, patterns)
        
        # Calculate sentiment shift
        original_sentiment = entry.get("sentiment_score", 0)
        
        # Apply different sentiment adjustments based on mode
        if self.rewrite_mode == "coyote":
            # Coyote mode is unpredictable - can be improved dramatically, stay neutral, or even go negative
            random_shift = random.choice([
                random.uniform(0.7, 1.3),   # Big positive shift (70%)
                random.uniform(-0.3, 0.3),  # Small or no shift (20%)
                random.uniform(-0.8, -0.2)  # Negative shift (10%)
            ])
            # Weight toward improvement
            weights = [0.7, 0.2, 0.1]
            random_shift = random.choices([
                random.uniform(0.7, 1.3),    
                random.uniform(-0.3, 0.3),  
                random.uniform(-0.8, -0.2)  
            ], weights=weights)[0]
            
            new_sentiment = min(1.0, max(-1.0, original_sentiment + random_shift))
        
        elif self.rewrite_mode == "whale":
            # Whale mode brings extreme moderation - moves everything toward neutral but slightly positive
            distance_from_zero = abs(original_sentiment)
            new_sentiment = 0.2 if original_sentiment >= 0 else -0.1  # Slightly positive bias
            
            # If very extreme sentiment, retain a small trace of the original direction
            if distance_from_zero > 0.5:
                direction = 1 if original_sentiment > 0 else -1
                new_sentiment += 0.1 * direction
        else:
            # Standard divine modes - always improve sentiment
            sentiment_improvement = random.uniform(0.4, 1.2)
            new_sentiment = min(1.0, original_sentiment + sentiment_improvement)
        
        # Add divine affirmation or wisdom quote to content
        if self.rewrite_mode == "coyote":
            wisdom = random.choice(self.COYOTE_WISDOM)
        elif self.rewrite_mode == "whale":
            wisdom = random.choice(self.WHALE_WISDOM)
        else:
            wisdom = random.choice(self.DIVINE_AFFIRMATIONS)
        
        transformed_content = f"{transformed_content}\n\n{wisdom}"
        
        # Select a random divine principle to attribute
        principle = random.choice(list(self.DIVINE_PRINCIPLES.keys()))
        
        # Create the transformed entry
        transformed_entry = {
            "original_title": original_title,
            "original_content": original_content,
            "transformed_title": transformed_title,
            "transformed_content": transformed_content,
            "source": source,
            "original_sentiment": original_sentiment,
            "new_sentiment": new_sentiment,
            "sentiment_shift": new_sentiment - original_sentiment,
            "divine_principle": principle,
            "rewrite_mode": self.rewrite_mode,
            "transformation_time": datetime.now().isoformat()
        }
        
        return transformed_entry
    
    def _apply_transformations(self, text, patterns):
        """Apply transformation patterns to text."""
        transformed_text = text
        
        for pattern, replacement in patterns.items():
            # Create a regex that matches the whole word/phrase only
            regex = r'\b' + re.escape(pattern) + r'\b'
            
            # Apply transformation with proper case preservation
            def replace_match(match):
                # Get the matched text
                matched_text = match.group(0)
                
                # Check capitalization and match it
                if matched_text.isupper():
                    return replacement.upper()
                elif matched_text[0].isupper():
                    return replacement[0].upper() + replacement[1:]
                else:
                    return replacement
            
            transformed_text = re.sub(regex, replace_match, transformed_text, flags=re.IGNORECASE)
        
        return transformed_text
    
    def process_all_news(self):
        """Process all news entries with divine rewriting."""
        if not self.news_entries:
            logger.warning("No news entries to process")
            return []
        
        self.rewritten_entries = []
        
        logger.info(f"Applying divine transformations...")
        
        for entry in self.news_entries:
            transformed_entry = self.divine_rewrite(entry)
            self.rewritten_entries.append(transformed_entry)
        
        logger.info(f"✅ Transformed {len(self.rewritten_entries)} news entries with {self.rewrite_mode} principles")
        
        return self.rewritten_entries
    
    def display_transformations(self, format="terminal"):
        """Display the transformations in the specified format."""
        if not self.rewritten_entries:
            logger.warning("No transformed entries to display")
            return
        
        if format == "json":
            # Convert datetime objects to ISO format strings for JSON serialization
            serializable_entries = []
            for entry in self.rewritten_entries:
                serializable_entry = entry.copy()
                if isinstance(entry.get('transformation_time'), datetime):
                    serializable_entry['transformation_time'] = entry['transformation_time'].isoformat()
                serializable_entries.append(serializable_entry)
                
            # Return JSON
            return json.dumps(serializable_entries, indent=2)
        
        elif format == "markdown":
            # Create markdown output
            markdown = "# Omega Divine News Transformations\n\n"
            
            for i, entry in enumerate(self.rewritten_entries, 1):
                markdown += f"## Transformation {i}: {entry['divine_principle'].title()} Principle\n\n"
                
                markdown += f"### Original: {entry['original_title']}\n"
                markdown += f"*Source: {entry['source']} | Sentiment: {entry['original_sentiment']:.2f}*\n\n"
                markdown += f"{entry['original_content']}\n\n"
                
                markdown += f"### Divine Transformation: {entry['transformed_title']}\n"
                markdown += f"*Mode: {entry['rewrite_mode'].title()} | New Sentiment: {entry['new_sentiment']:.2f}*\n\n"
                markdown += f"{entry['transformed_content']}\n\n"
                
                if i < len(self.rewritten_entries):
                    markdown += "---\n\n"
            
            return markdown
        
        else:  # Terminal output handled by the calling code
            return self.rewritten_entries
    
    def save_transformations(self):
        """Save the transformations to a file."""
        if not self.rewritten_entries:
            logger.warning("No transformed entries to save")
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Determine the output format and file extension
        if hasattr(self, 'output_format') and self.output_format == "json":
            extension = "json"
            # Convert datetime objects to ISO format strings for JSON serialization
            serializable_entries = []
            for entry in self.rewritten_entries:
                serializable_entry = entry.copy()
                if isinstance(entry.get('transformation_time'), datetime):
                    serializable_entry['transformation_time'] = entry['transformation_time'].isoformat()
                serializable_entries.append(serializable_entry)
                
            content = json.dumps(serializable_entries, indent=2)
        
        elif hasattr(self, 'output_format') and self.output_format == "markdown":
            extension = "md"
            content = self.display_transformations(format="markdown")
        
        else:
            # Default to markdown
            extension = "md"
            content = self.display_transformations(format="markdown")
        
        # Create the output filename
        filename = f"divine_news_{self.rewrite_mode}_{timestamp}.{extension}"
        filepath = os.path.join(self.output_dir, filename)
        
        # Save the file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"✅ Divine transformations saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving transformations: {e}")
            return None
            
    def set_output_format(self, format):
        """Set the output format for saving transformations."""
        self.output_format = format 