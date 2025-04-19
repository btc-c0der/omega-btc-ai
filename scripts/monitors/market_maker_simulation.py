#!/usr/bin/env python3

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
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

# 🔱 OMEGA BTC AI - Market Maker Simulation
# Licensed under GPU v1.0 — General Public Universal License 🔱

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import random
import json
import os
from matplotlib.patches import Patch

# Ensure data directory exists
os.makedirs("data/market_maker_sim", exist_ok=True)

class MarketMakerSimulation:
    """Simulation of Bitcoin market makers and their impact on prices"""
    
    def __init__(self, num_market_makers=13, seed=42):
        self.seed = seed
        np.random.seed(seed)
        random.seed(seed)
        
        self.num_market_makers = num_market_makers
        self.start_date = datetime.now() - timedelta(days=90)  # 3 months history
        self.end_date = datetime.now() + timedelta(days=14)    # 2 weeks projection
        
        # Create market makers with different characteristics
        self.market_makers = self._create_market_makers()
        
        # News and reaction events
        self.news_events = []
        self.market_reactions = []
        
        # Initialize price data
        self.base_price = 40000  # Starting Bitcoin price
        self.price_history = []
        self.dates = []
        self.agreement_failures = []
        
    def _create_market_makers(self):
        """Create market maker profiles with different characteristics"""
        makers = []
        
        # Names of fictional trading entities
        maker_names = [
            "Quantum Capital", "Nexus Trading", "Zion Markets", 
            "Alpha Zenith", "Crown Exchange", "Divine Arbitrage",
            "Oracle Liquidity", "Phoenix Trading", "Unity Markets",
            "Stellar Flow", "Cosmic Ventures", "Lion's Gate Capital",
            "Omega Prime"
        ]
        
        for i in range(self.num_market_makers):
            # Each market maker has different characteristics
            maker = {
                "id": i + 1,
                "name": maker_names[i],
                "capital": np.random.uniform(100e6, 5e9),  # $100M to $5B
                "aggression": np.random.uniform(0.1, 0.9),  # How aggressively they trade
                "manipulation_tendency": np.random.uniform(0.01, 0.4),  # Tendency to manipulate
                "cooperation": np.random.uniform(0.3, 0.9),  # Tendency to cooperate with others
                "btc_holdings": np.random.uniform(1000, 50000),  # BTC holdings
                "trust_score": np.random.uniform(0.5, 0.95),  # Trust from other makers
                "technical_capability": np.random.uniform(0.6, 0.98),  # Trading tech quality
                "reaction_time": np.random.uniform(0.001, 0.1),  # Seconds to react to market
                "primary_exchange": random.choice(["Binance", "Coinbase", "OKX", "Bitfinex", "Kraken"])
            }
            makers.append(maker)
            
        return makers
    
    def run_simulation(self):
        """Run the full market simulation"""
        # Generate daily price data spanning 3-month history plus 2-week projection
        current_date = self.start_date
        current_price = self.base_price
        day_counter = 0
        agreement_failures = 0
        
        # Track if Saturday push happened
        saturday_push_happened = False
        
        while current_date <= self.end_date:
            is_weekend = current_date.weekday() >= 5  # 5=Saturday, 6=Sunday
            is_saturday = current_date.weekday() == 5
            
            # Daily price change factors
            market_sentiment = np.random.normal(0, 0.01)  # General market sentiment
            
            # Simulate the 29 agreement failures over 3 months (90 days)
            if day_counter < 90 and random.random() < (29/90):
                agreement_failures += 1
                failure_impact = -0.02 * random.random()  # Each failure hurts trust and price
                
                # Record the failure
                self.agreement_failures.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "count": agreement_failures,
                    "impact": failure_impact,
                    "price_before": current_price
                })
                
                # Market makers lose cooperation after failures
                for maker in self.market_makers:
                    maker["cooperation"] *= 0.98
                    maker["trust_score"] *= 0.97
            
            # The big Saturday price push to $50K on the first Saturday after today
            if is_saturday and current_date > datetime.now() and not saturday_push_happened:
                saturday_push_happened = True
                print(f"🚀 Simulating the Saturday price push to $50K on {current_date.strftime('%Y-%m-%d')}")
                
                # Coordinated push by market makers
                push_power = sum([m["capital"] * m["manipulation_tendency"] for m in self.market_makers]) / 1e11
                
                # Force price to trend toward $50K
                target = 50000
                price_gap = target - current_price
                push_effect = price_gap * 0.8  # Move 80% of the way there
                
                current_price += push_effect
                
                # Add news event
                self.news_events.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "source": "New York Times",
                    "headline": "Bitcoin Surges to $50K as Market Makers Coordinate Unprecedented Push",
                    "impact_factor": 0.85,
                    "sentiment": "extremely bullish"
                })
                
                # Wall Street reaction the next day
                self.market_reactions.append({
                    "date": (current_date + timedelta(days=1)).strftime("%Y-%m-%d"),
                    "entity": "Wall Street Traders",
                    "reaction": "Food truck investments surge as traders cash out crypto gains for real-world assets",
                    "impact_factor": 0.3,
                    "sentiment": "mixed"
                })
            else:
                # Normal daily price fluctuation
                maker_influence = sum([
                    (m["capital"] / 1e9) * m["aggression"] * (1 - m["cooperation"]) 
                    for m in self.market_makers
                ]) / self.num_market_makers
                
                # Higher volatility on weekends
                volatility = 0.03 if is_weekend else 0.02
                
                # Calculate price change
                price_change = current_price * (
                    market_sentiment + 
                    np.random.normal(0, volatility) +
                    maker_influence * np.random.normal(0, 0.01)
                )
                
                current_price += price_change
            
            # Ensure price doesn't go below reasonable floor
            current_price = max(current_price, self.base_price * 0.5)
            
            # Record price
            self.price_history.append((current_date, current_price))
            self.dates.append(current_date)
            
            # Move to next day
            current_date += timedelta(days=1)
            day_counter += 1
            
        # Convert price history to usable formats
        self.dates = [d for d, _ in self.price_history]
        self.prices = [p for _, p in self.price_history]
        
        # Save simulation results
        self._save_results()
        
        return self.dates, self.prices
    
    def _save_results(self):
        """Save simulation results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save price data
        price_data = {
            "dates": [d.strftime("%Y-%m-%d") for d in self.dates],
            "prices": self.prices,
            "base_price": self.base_price,
            "market_makers": self.num_market_makers,
            "agreement_failures": len(self.agreement_failures),
            "news_events": self.news_events,
            "market_reactions": self.market_reactions
        }
        
        with open(f"data/market_maker_sim/price_data_{timestamp}.json", "w") as f:
            json.dump(price_data, f, indent=2)
            
        # Save market maker profiles
        with open(f"data/market_maker_sim/market_makers_{timestamp}.json", "w") as f:
            json.dump(self.market_makers, f, indent=2)
            
        # Save agreement failures
        if self.agreement_failures:
            with open(f"data/market_maker_sim/agreement_failures_{timestamp}.json", "w") as f:
                json.dump(self.agreement_failures, f, indent=2)
    
    def plot_results(self):
        """Visualize simulation results"""
        plt.figure(figsize=(14, 10), facecolor='#1A1A1A')
        ax = plt.gca()
        ax.set_facecolor('#1A1A1A')
        
        # Convert datetime objects to matplotlib format
        dates_mpl = mdates.date2num(self.dates)
        
        # Plot the prices
        plt.plot(dates_mpl, self.prices, color='#FFD700', linewidth=2)
        
        # Mark today's date with a vertical line
        today = datetime.now()
        today_mpl = mdates.date2num(today)
        plt.axvline(x=today_mpl, color='#FFFFFF', linestyle='--', alpha=0.7)
        plt.text(mdates.date2num(today + timedelta(days=1)), max(self.prices) * 0.95, "Today", 
                 color='#FFFFFF', fontsize=10, rotation=90)
        
        # Mark the agreement failures
        failure_dates = [datetime.strptime(f["date"], "%Y-%m-%d") for f in self.agreement_failures]
        failure_dates_mpl = mdates.date2num(failure_dates)
        failure_prices = []
        
        # Only include failures that match dates in our simulation
        for fail_date in failure_dates:
            if fail_date in self.dates:
                idx = self.dates.index(fail_date)
                failure_prices.append(self.prices[idx])
        
        if failure_dates and failure_prices:
            plt.scatter(failure_dates_mpl[:len(failure_prices)], failure_prices, color='#FF4500', s=100, zorder=5, 
                       marker='x', label=f'Agreement Failures ({len(self.agreement_failures)})')
        
        # Mark news events
        for event in self.news_events:
            event_date = datetime.strptime(event["date"], "%Y-%m-%d")
            if event_date in self.dates:
                event_date_mpl = mdates.date2num(event_date)
                event_price = self.prices[self.dates.index(event_date)]
                plt.scatter(event_date_mpl, event_price, color='#00BFFF', s=150, zorder=5, marker='*')
                plt.text(event_date_mpl, event_price * 1.02, event["source"], 
                         color='#00BFFF', fontsize=10, ha='center')
        
        # Mark market reactions
        for reaction in self.market_reactions:
            reaction_date = datetime.strptime(reaction["date"], "%Y-%m-%d")
            if reaction_date in self.dates:
                reaction_date_mpl = mdates.date2num(reaction_date)
                reaction_price = self.prices[self.dates.index(reaction_date)]
                plt.scatter(reaction_date_mpl, reaction_price, color='#32CD32', s=120, zorder=5, marker='o')
                plt.text(reaction_date_mpl, reaction_price * 0.98, reaction["entity"], 
                         color='#32CD32', fontsize=10, ha='center')
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        
        # Add grid
        plt.grid(color='#333333', linestyle='--', linewidth=0.5, alpha=0.7)
        
        # Find the Saturday push event date
        saturday_push_date = None
        for event in self.news_events:
            event_date = datetime.strptime(event["date"], "%Y-%m-%d")
            if event_date.weekday() == 5 and event_date > today:  # 5 = Saturday
                saturday_push_date = event_date
                break
        
        # Highlight the Saturday push to $50K
        if saturday_push_date and saturday_push_date in self.dates:
            idx = self.dates.index(saturday_push_date)
            push_price = self.prices[idx]
            
            start_span = mdates.date2num(saturday_push_date)
            end_span = mdates.date2num(saturday_push_date + timedelta(days=1))
            
            plt.axvspan(start_span, end_span, 
                       color='#B22222', alpha=0.3, label='Saturday $50K Push')
            
            plt.text(mdates.date2num(saturday_push_date + timedelta(hours=12)), push_price * 1.05, 
                    f"$50K Push\n{saturday_push_date.strftime('%Y-%m-%d')}", 
                    color='#FFFFFF', fontsize=12, ha='center', weight='bold')
        
        # Add labels and title
        plt.xlabel('Date', color='#FFFFFF', fontsize=12)
        plt.ylabel('Bitcoin Price (USD)', color='#FFFFFF', fontsize=12)
        plt.title(f'13 Market Makers Simulation with 29 Agreement Failures\n'
                 f'and Coordinated Push to $50K', color='#FFD700', fontsize=16)
        
        # Add subtitle about market makers and food trucks
        if self.market_reactions:
            plt.figtext(0.5, 0.915, 
                      "Wall Street Traders Exit Crypto to Invest in Food Trucks", 
                      color='#32CD32', fontsize=12, ha='center', 
                      bbox=dict(facecolor='#000000', alpha=0.5, edgecolor='none', pad=5))
        
        # Create custom legend
        legend_elements = [
            Patch(facecolor='#B22222', alpha=0.3, label='Saturday $50K Push'),
            Patch(facecolor='#FF4500', label=f'Agreement Failures ({len(self.agreement_failures)})'),
            Patch(facecolor='#00BFFF', label='News Events'),
            Patch(facecolor='#32CD32', label='Wall Street Reactions')
        ]
        
        plt.legend(handles=legend_elements, loc='upper left', facecolor='#1A1A1A', 
                  edgecolor='#FFFFFF', labelcolor='#FFFFFF')
        
        # Set text color for ticks
        plt.tick_params(colors='#FFFFFF')
        
        # Add price stats
        min_price = min(self.prices)
        max_price = max(self.prices)
        final_price = self.prices[-1]
        
        stats_text = f"Min: ${min_price:.2f}\nMax: ${max_price:.2f}\nFinal: ${final_price:.2f}"
        plt.figtext(0.02, 0.02, stats_text, color='#FFFFFF', fontsize=10)
        
        # Add simulation info
        sim_info = (f"Simulation of {self.num_market_makers} Market Makers\n"
                   f"Over {len(self.dates)} days with 3-month history\n"
                   f"Seed: {self.seed}")
        plt.figtext(0.98, 0.02, sim_info, color='#CCCCCC', fontsize=8, ha='right')
        
        # Save figure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.tight_layout()
        plt.savefig(f"data/market_maker_sim/market_maker_simulation_{timestamp}.png", 
                   dpi=300, bbox_inches='tight', facecolor='#1A1A1A')
        
        print(f"🔱 Saved market maker simulation visualization to: "
              f"data/market_maker_sim/market_maker_simulation_{timestamp}.png")
        
        plt.close()
        return f"data/market_maker_sim/market_maker_simulation_{timestamp}.png"

def run_market_maker_scenario():
    """Run the market maker scenario simulation"""
    print("🔱 OMEGA BTC AI - Market Maker Simulation 🔱")
    print("===========================================")
    print("Simulating 13 market makers with 29 agreement failures over 3 months")
    print("Includes Saturday price push to $50K and Wall Street reactions")
    
    # Create and run simulation
    simulation = MarketMakerSimulation(num_market_makers=13, seed=42)
    simulation.run_simulation()
    
    # Plot results
    viz_path = simulation.plot_results()
    
    print("\n✨ Simulation Results ✨")
    print(f"- Initial price: ${simulation.base_price}")
    print(f"- Final price: ${simulation.prices[-1]:.2f}")
    print(f"- Agreement failures: {len(simulation.agreement_failures)}")
    print(f"- News events: {len(simulation.news_events)}")
    print(f"- Wall Street reactions: {len(simulation.market_reactions)}")
    print(f"\nVisualization saved to: {viz_path}")
    
    return viz_path

if __name__ == "__main__":
    run_market_maker_scenario() 