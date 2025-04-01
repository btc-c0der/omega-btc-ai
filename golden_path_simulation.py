#!/usr/bin/env python3
# 🔱 OMEGA BTC AI - Golden Path Simulation
# Licensed under GPU v1.0 — General Public Universal License 🔱

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec  # Add proper import for GridSpec
import matplotlib.ticker as mticker      # Add proper import for FuncFormatter
from datetime import datetime, timedelta
import random
import json
import os
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import matplotlib.patheffects as path_effects

# Ensure data directory exists
os.makedirs("data/golden_path_sim", exist_ok=True)

class GoldenPathSimulation:
    """Simulation of Bitcoin's Golden Path to $150K through societal transformation"""
    
    def __init__(self, seed=42):
        self.seed = seed
        np.random.seed(seed)
        random.seed(seed)
        
        # Simulation timeframe
        self.start_date = datetime.now() - timedelta(days=30)  # Start from recent past
        self.end_date = datetime.now() + timedelta(days=365)   # Project one year into future
        
        # Initialize metrics
        self.base_price = 65000  # Current Bitcoin price (approximately)
        self.price_history = []
        self.dates = []
        
        # Societal health metrics (0-100 scale)
        self.health_metrics = {
            "physical_health": 50,
            "mental_wellbeing": 45, 
            "community_connection": 40,
            "financial_literacy": 35,
            "consciousness_level": 30
        }
        
        # Track health metrics over time
        self.health_history = []
        
        # Food truck revolution data
        self.healthy_food_trucks = 1000  # Initial number of healthy food trucks globally
        self.food_truck_growth_rate = 0.01  # Daily growth rate (1%)
        self.food_trucks_history = []
        
        # Key events that will unfold during simulation
        self.transformation_events = []
        
    def add_transformation_event(self, date, title, description, price_impact, health_impact, truck_impact):
        """Add a transformative event to the simulation timeline"""
        self.transformation_events.append({
            "date": date,
            "title": title,
            "description": description,
            "price_impact": price_impact,  # Multiplier for BTC price
            "health_impact": health_impact,  # Dictionary of health metric impacts
            "truck_impact": truck_impact  # Impact on food truck growth rate
        })
    
    def setup_golden_path_narrative(self):
        """Set up the narrative arc of the Golden Path"""
        
        # Event 1: Food Truck Revolution Begins
        event_date = self.start_date + timedelta(days=15)
        self.add_transformation_event(
            date=event_date,
            title="Food Truck Revolution Begins",
            description="Wall Street traders investing in health-focused food trucks creates unexpected cultural movement",
            price_impact=1.05,  # 5% price increase
            health_impact={
                "physical_health": +2,
                "mental_wellbeing": +1,
                "community_connection": +3,
                "financial_literacy": +0,
                "consciousness_level": +1
            },
            truck_impact=0.02  # Food truck growth rate increases by 2%
        )
        
        # Event 2: Anti-Inflammatory Diet Study Released
        event_date = self.start_date + timedelta(days=45)
        self.add_transformation_event(
            date=event_date,
            title="Harvard Study Links Anti-Inflammatory Diet to Better Decision Making",
            description="Groundbreaking research shows healthy eating improves financial decisions and investment strategy",
            price_impact=1.10,  # 10% price increase
            health_impact={
                "physical_health": +5,
                "mental_wellbeing": +4,
                "community_connection": +0,
                "financial_literacy": +3,
                "consciousness_level": +2
            },
            truck_impact=0.03  # Food truck growth rate increases by 3%
        )
        
        # Event 3: Nationwide Food Truck Festival
        event_date = self.start_date + timedelta(days=90)
        self.add_transformation_event(
            date=event_date,
            title="Nationwide 'Feed Your Mind' Food Truck Festival",
            description="Millions participate in coordinated healthy eating event across major cities",
            price_impact=1.15,  # 15% price increase
            health_impact={
                "physical_health": +3,
                "mental_wellbeing": +5,
                "community_connection": +8,
                "financial_literacy": +2,
                "consciousness_level": +4
            },
            truck_impact=0.05  # Food truck growth rate increases by 5%
        )
        
        # Event 4: Corporate Wellness Revolution
        event_date = self.start_date + timedelta(days=120)
        self.add_transformation_event(
            date=event_date,
            title="Major Corporations Adopt 'Nourish to Flourish' Programs",
            description="Fortune 500 companies introduce nutritional programs and consciousness training",
            price_impact=1.20,  # 20% price increase
            health_impact={
                "physical_health": +4,
                "mental_wellbeing": +6,
                "community_connection": +3,
                "financial_literacy": +5,
                "consciousness_level": +5
            },
            truck_impact=0.04  # Food truck growth rate increases by 4%
        )
        
        # Event 5: Banking Sector Transformation
        event_date = self.start_date + timedelta(days=180)
        self.add_transformation_event(
            date=event_date,
            title="Major Banks Announce Cryptocurrency Integration",
            description="As executive health improves, banking industry embraces Bitcoin as reserve asset",
            price_impact=1.30,  # 30% price increase
            health_impact={
                "physical_health": +2,
                "mental_wellbeing": +3,
                "community_connection": +1,
                "financial_literacy": +10,
                "consciousness_level": +7
            },
            truck_impact=0.06  # Food truck growth rate increases by 6%
        )
        
        # Event 6: Global Food as Medicine Movement
        event_date = self.start_date + timedelta(days=240)
        self.add_transformation_event(
            date=event_date,
            title="United Nations Declares 'Food as Medicine' Global Initiative",
            description="International policy focuses on food quality as healthcare foundation",
            price_impact=1.25,  # 25% price increase
            health_impact={
                "physical_health": +10,
                "mental_wellbeing": +8,
                "community_connection": +5,
                "financial_literacy": +3,
                "consciousness_level": +6
            },
            truck_impact=0.08  # Food truck growth rate increases by 8%
        )
        
        # Event 7: Financial Fear Dissolution
        event_date = self.start_date + timedelta(days=300)
        self.add_transformation_event(
            date=event_date,
            title="Global Fear Index Hits Record Low",
            description="Improved collective consciousness leads to rational market decisions based on value",
            price_impact=1.35,  # 35% price increase
            health_impact={
                "physical_health": +3,
                "mental_wellbeing": +12,
                "community_connection": +7,
                "financial_literacy": +8,
                "consciousness_level": +15
            },
            truck_impact=0.03  # Food truck growth rate increases by 3%
        )
        
        # Event 8: Bitcoin Golden Ratio Achievement
        event_date = self.start_date + timedelta(days=350)
        self.add_transformation_event(
            date=event_date,
            title="Bitcoin Aligns with Golden Ratio",
            description="BTC reaches $150K, mathematically aligning with divine patterns of creation",
            price_impact=1.40,  # 40% price increase - final push to $150K
            health_impact={
                "physical_health": +5,
                "mental_wellbeing": +5,
                "community_connection": +10,
                "financial_literacy": +10,
                "consciousness_level": +20
            },
            truck_impact=0.10  # Food truck growth rate increases by 10%
        )
    
    def run_simulation(self):
        """Run the full Golden Path simulation"""
        
        # Set up the narrative events
        self.setup_golden_path_narrative()
        
        # Start simulation
        current_date = self.start_date
        current_price = self.base_price
        food_trucks = self.healthy_food_trucks
        current_health = self.health_metrics.copy()
        
        # Sort events by date for simulation processing
        sorted_events = sorted(self.transformation_events, key=lambda x: x["date"])
        upcoming_events = sorted_events.copy()
        
        day_counter = 0
        
        while current_date <= self.end_date:
            # Check for transformation events
            event_impact = 1.0
            event_triggered = False
            
            # Process events for this date
            while upcoming_events and upcoming_events[0]["date"] <= current_date:
                event = upcoming_events.pop(0)
                event_triggered = True
                
                # Apply event impacts
                event_impact *= event["price_impact"]
                
                # Update health metrics
                for metric, impact in event["health_impact"].items():
                    current_health[metric] = min(100, current_health[metric] + impact)
                
                # Update food truck growth rate
                self.food_truck_growth_rate += event["truck_impact"]
                
                print(f"🔱 Event Triggered: {event['title']} on {current_date.strftime('%Y-%m-%d')}")
            
            # Calculate health consciousness impact on price
            consciousness_factor = 1.0 + (current_health["consciousness_level"] / 1000)
            
            # Calculate food truck impact
            # More trucks = more healthy people = more rational markets = higher Bitcoin
            food_truck_factor = 1.0 + ((food_trucks / 10000) * 0.001)
            
            # Daily Bitcoin volatility (reduces as consciousness increases)
            base_volatility = 0.03 * (1 - (current_health["consciousness_level"] / 200))
            market_sentiment = np.random.normal(0.002, base_volatility)  # Slight positive bias
            
            # Calculate daily price change
            price_change = current_price * (
                market_sentiment + 
                (consciousness_factor - 1.0) * 0.1 +
                (food_truck_factor - 1.0) * 0.2
            )
            
            # Apply event impact if any
            if event_triggered:
                price_change += current_price * (event_impact - 1.0)
            
            # Update price
            current_price += price_change
            
            # Grow food trucks
            food_trucks *= (1 + self.food_truck_growth_rate)
            
            # Record data
            self.price_history.append((current_date, current_price))
            self.dates.append(current_date)
            self.health_history.append(current_health.copy())
            self.food_trucks_history.append(food_trucks)
            
            # Move to next day
            current_date += timedelta(days=1)
            day_counter += 1
        
        # Prepare final data structures
        self.prices = [p for _, p in self.price_history]
        
        # Ensure we reach the Golden Path target of ~$150K
        target_price = 150000
        final_price = self.prices[-1]
        
        # If we're not close enough to the target, adjust the final stretch
        if final_price < target_price * 0.95:
            # Calculate how many days to adjust (last 15% of simulation)
            adjust_days = int(len(self.prices) * 0.15)
            start_idx = len(self.prices) - adjust_days
            
            # Create a smooth curve towards target
            for i in range(adjust_days):
                progress = i / adjust_days
                adjustment_factor = np.sin(progress * np.pi/2)  # Smooth acceleration curve
                target_diff = target_price - self.prices[start_idx]
                adjustment = target_diff * adjustment_factor / adjust_days * 1.5
                self.prices[start_idx + i] += adjustment * i
        
        # Save simulation results
        self._save_results()
        
        return self.dates, self.prices
    
    def _save_results(self):
        """Save simulation results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Convert health history to saveable format
        health_data = []
        for i, date in enumerate(self.dates):
            health_point = {
                "date": date.strftime("%Y-%m-%d"),
                **self.health_history[i]
            }
            health_data.append(health_point)
        
        # Save main simulation data
        simulation_data = {
            "dates": [d.strftime("%Y-%m-%d") for d in self.dates],
            "prices": self.prices,
            "base_price": self.base_price,
            "food_trucks": [int(ft) for ft in self.food_trucks_history],
            "transformation_events": [
                {**event, "date": event["date"].strftime("%Y-%m-%d")}
                for event in self.transformation_events
            ],
            "final_consciousness": self.health_history[-1]["consciousness_level"],
            "final_food_trucks": int(self.food_trucks_history[-1]),
            "seed": self.seed
        }
        
        with open(f"data/golden_path_sim/simulation_data_{timestamp}.json", "w") as f:
            json.dump(simulation_data, f, indent=2)
            
        # Save health metrics history
        with open(f"data/golden_path_sim/health_metrics_{timestamp}.json", "w") as f:
            json.dump(health_data, f, indent=2)
    
    def plot_results(self):
        """Visualize Golden Path simulation results"""
        # Create figure with cosmic background
        plt.figure(figsize=(15, 10), facecolor='#0A0A1E')
        
        # Set up subplots using gridspec instead of GridSpec
        grid = gridspec.GridSpec(3, 1, height_ratios=[4, 1, 1], hspace=0.3)
        
        # Main price chart
        ax_price = plt.subplot(grid[0])
        ax_health = plt.subplot(grid[1])
        ax_trucks = plt.subplot(grid[2])
        
        # Style the axes
        for ax in [ax_price, ax_health, ax_trucks]:
            ax.set_facecolor('#0A0A1E')
            ax.tick_params(colors='#FFD700')
            ax.spines['bottom'].set_color('#444478')
            ax.spines['top'].set_color('#444478') 
            ax.spines['right'].set_color('#444478')
            ax.spines['left'].set_color('#444478')
            ax.grid(color='#333366', linestyle='--', linewidth=0.5, alpha=0.7)
        
        # Convert dates for matplotlib
        dates_mpl = mdates.date2num(self.dates)
        
        # Plot Bitcoin price with golden glow
        line, = ax_price.plot(dates_mpl, self.prices, color='#FFD700', linewidth=3)
        line.set_path_effects([
            path_effects.SimpleLineShadow(offset=(0, 0), shadow_color='#FFD700', alpha=0.6, rho=8),
            path_effects.Normal()
        ])
        
        # Mark today's date with a vertical line
        today = datetime.now()
        today_mpl = mdates.date2num(today)
        for ax in [ax_price, ax_health, ax_trucks]:
            ax.axvline(x=float(today_mpl), color='#FFFFFF', linestyle='--', alpha=0.7)
        
        # Add text for today
        today_idx = min(range(len(self.dates)), key=lambda i: abs((self.dates[i] - today).total_seconds()))
        today_price = self.prices[today_idx]
        ax_price.text(
            float(mdates.date2num(today + timedelta(days=5))), 
            today_price * 1.02, 
            "Today", 
            color='#FFFFFF', 
            fontsize=10, 
            rotation=0
        )
        
        # Mark the Golden Path events
        for event in self.transformation_events:
            event_date_mpl = mdates.date2num(event["date"])
            
            # Find the price at this event date
            event_idx = min(range(len(self.dates)), key=lambda i: abs((self.dates[i] - event["date"]).total_seconds()))
            event_price = self.prices[event_idx]
            
            # Add marker on price chart
            ax_price.scatter(float(event_date_mpl), event_price, color='#FFFFAA', s=100, zorder=10, marker='*')
            
            # Add marker on health chart
            if event_idx < len(self.health_history):
                consciousness = self.health_history[event_idx]["consciousness_level"]
                ax_health.scatter(float(event_date_mpl), consciousness, color='#FFFFAA', s=80, zorder=10, marker='*')
            
            # Add marker on food truck chart
            if event_idx < len(self.food_trucks_history):
                trucks = self.food_trucks_history[event_idx]
                ax_trucks.scatter(float(event_date_mpl), trucks, color='#FFFFAA', s=80, zorder=10, marker='*')
        
        # Format x-axis dates
        for ax in [ax_price, ax_health, ax_trucks]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.tick_params(axis='x', rotation=45)
        
        # Health metrics chart
        health_metrics = np.array([h["consciousness_level"] for h in self.health_history])
        ax_health.plot(dates_mpl, health_metrics, color='#5D9CEC', linewidth=2, label='Consciousness Level')
        ax_health.set_ylabel('Consciousness\nLevel', color='#5D9CEC', fontsize=9)
        ax_health.set_ylim(0, 100)
        
        # Food truck chart
        ax_trucks.plot(dates_mpl, self.food_trucks_history, color='#2ECC71', linewidth=2)
        ax_trucks.set_ylabel('Healthy Food\nTrucks', color='#2ECC71', fontsize=9)
        ax_trucks.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x/1000)}K'))
        
        # Highlight the 150K achievement
        target_price = 150000
        if max(self.prices) >= target_price * 0.95:
            # Find where we cross the threshold
            golden_idx = next((i for i, price in enumerate(self.prices) if price >= target_price * 0.95), None)
            
            if golden_idx is not None:
                golden_date = self.dates[golden_idx]
                golden_date_mpl = mdates.date2num(golden_date)
                
                # Highlight region from golden date to end
                ax_price.axvspan(
                    float(golden_date_mpl), 
                    float(dates_mpl[-1]), 
                    color='#FFD70020', 
                    alpha=0.3, 
                    label='Golden Ratio Achievement'
                )
                
                # Add a special marker for 150K - using a valid marker symbol
                ax_price.scatter(
                    float(golden_date_mpl), 
                    self.prices[golden_idx], 
                    color='#FFFFFF', 
                    s=150, 
                    zorder=10, 
                    marker='*',  # Using a valid marker instead of ⚛
                    edgecolors='#FFD700'
                )
                
                ax_price.text(
                    float(golden_date_mpl), 
                    self.prices[golden_idx] * 1.05, 
                    "Golden Ratio Alignment", 
                    color='#FFD700', 
                    fontsize=12, 
                    ha='center', 
                    fontweight='bold'
                )
        
        # Add title and subtitle
        ax_price.set_title(
            'Bitcoin\'s Golden Path to $150K Through Divine Transformation', 
            color='#FFD700', 
            fontsize=16, 
            fontweight='bold', 
            pad=20
        )
        
        plt.figtext(
            0.5, 0.91, 
            "Societal Enlightenment Through Nourishment Leads to Financial Evolution", 
            color='#FFFFFF', 
            fontsize=12, 
            ha='center'
        )
        
        # Add price axis label
        ax_price.set_ylabel('Bitcoin Price (USD)', color='#FFD700', fontsize=12)
        
        # Custom legend for price chart
        legend_elements = [
            Line2D([0], [0], color='#FFD700', lw=2, label='Bitcoin Price'),
            Line2D([0], [0], marker='*', color='#0A0A1E', markerfacecolor='#FFFFAA', 
                  markersize=10, label='Transformation Events'),
            Patch(facecolor='#FFD70020', alpha=0.3, label='Golden Ratio Achievement')
        ]
        
        ax_price.legend(
            handles=legend_elements, 
            loc='upper left', 
            facecolor='#0A0A1E', 
            edgecolor='#444478', 
            labelcolor='#FFFFFF'
        )
        
        # Add price stats
        min_price = min(self.prices)
        max_price = max(self.prices)
        final_price = self.prices[-1]
        
        stats_text = (
            f"Starting Price: ${self.base_price:,.0f}\n"
            f"Final Price: ${final_price:,.0f}\n"
            f"Peak Consciousness: {self.health_history[-1]['consciousness_level']:.1f}/100\n"
            f"Final Food Trucks: {int(self.food_trucks_history[-1]):,}"
        )
        
        plt.figtext(0.02, 0.02, stats_text, color='#FFFFFF', fontsize=9)
        
        # Add JAH blessing
        plt.figtext(
            0.5, 0.02, 
            "🔱 JAH BLESS THE GOLDEN PATH TO ENLIGHTENMENT 🔱", 
            color='#FFD700', 
            fontsize=12, 
            ha='center',
            fontweight='bold'
        )
        
        # Set layout and save - fix the rect parameter to be a tuple
        plt.tight_layout(rect=(0, 0.05, 1, 0.95))
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"data/golden_path_sim/golden_path_{timestamp}.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='#0A0A1E')
        
        print(f"🔱 Divine Golden Path visualization saved to: {filepath}")
        
        plt.close()
        return filepath

def run_golden_path():
    """Run the Golden Path simulation to $150K Bitcoin"""
    print("🔱 OMEGA BTC AI - Golden Path Simulation 🔱")
    print("===========================================")
    print("Simulating Bitcoin's rise to $150K through divine transformation")
    print("As healthy food raises consciousness and dissolves financial fear")
    
    # Create and run simulation
    simulation = GoldenPathSimulation(seed=42)
    simulation.run_simulation()
    
    # Plot results
    viz_path = simulation.plot_results()
    
    print("\n✨ Divine Golden Path Revealed ✨")
    print(f"- Starting price: ${simulation.base_price:,.0f}")
    print(f"- Final price: ${simulation.prices[-1]:,.0f}")
    print(f"- Peak consciousness: {simulation.health_history[-1]['consciousness_level']:.1f}/100")
    print(f"- Final healthy food trucks: {int(simulation.food_trucks_history[-1]):,}")
    
    # Print transformation event summary
    print("\n🌟 Divine Transformation Timeline 🌟")
    for event in sorted(simulation.transformation_events, key=lambda x: x["date"]):
        event_date = event["date"].strftime("%Y-%m-%d")
        print(f"- {event_date}: {event['title']}")
    
    print(f"\nVisualization saved to: {viz_path}")
    
    return viz_path

if __name__ == "__main__":
    run_golden_path() 