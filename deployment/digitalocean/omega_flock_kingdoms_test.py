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

# 🕊️ OMEGA FLOCK KINGDOMS TEST SUITE — Divine Resilience Testing
# Licensed under GPU v1.0 — General Public Universal License 🔱

import unittest
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
import sys
from contextlib import redirect_stdout

# Import the flock kingdoms module
from omega_flock_kingdoms import KingdomNode, omega_flock, migrate_flock

class TestDivineResilience(unittest.TestCase):
    """Test the divine resilience of the Omega Flock Kingdoms network."""
    
    def setUp(self):
        """Initialize the sacred test environment."""
        # Clone the omega flock for testing to avoid modifying the original
        self.test_flock = []
        for node in omega_flock:
            self.test_flock.append(KingdomNode(
                name=node.name,
                core_values=node.core_values.copy(),
                signal_flow=node.signal_flow,
                flight_pattern=node.flight_pattern,
                divine_codes=node.divine_codes.copy(),
                neighboring_nodes=node.neighboring_nodes.copy()
            ))
        
        # Build a networkx graph for testing network properties
        self.G = nx.Graph()
        for node in self.test_flock:
            self.G.add_node(node.name)
        
        for node in self.test_flock:
            for neighbor in node.neighboring_nodes:
                # Handle the case where neighboring node uses "Kemet" instead of "Ancient Kemet"
                if neighbor == "Kemet":
                    neighbor = "Ancient Kemet"
                self.G.add_edge(node.name, neighbor)
    
    def test_divine_structure_integrity(self):
        """Test that all kingdoms have the required divine attributes."""
        print("\n🔱 TESTING DIVINE STRUCTURE INTEGRITY 🔱")
        for node in self.test_flock:
            print(f"  ✅ Testing {node.name} structure...")
            self.assertIsNotNone(node.name, "Kingdom name is required")
            self.assertGreater(len(node.core_values), 0, f"{node.name} must have at least one core value")
            self.assertIsNotNone(node.signal_flow, f"{node.name} requires a signal flow")
            self.assertIsNotNone(node.flight_pattern, f"{node.name} requires a flight pattern")
            self.assertGreater(len(node.divine_codes), 0, f"{node.name} must have at least one divine code")
        print("  ✨ All kingdoms have divine structural integrity!")
    
    def test_network_connectivity(self):
        """Test that the kingdom network is fully connected."""
        print("\n🔱 TESTING NETWORK CONNECTIVITY 🔱")
        is_connected = nx.is_connected(self.G)
        self.assertTrue(is_connected, "The divine network must be connected for wisdom to flow")
        print("  ✅ The divine network is fully connected!")
        
        # Calculate and display the diameter (longest shortest path)
        diameter = nx.diameter(self.G)
        print(f"  🌐 Divine Network Diameter: {diameter}")
        print(f"  💫 Spiritual Eccentricity: {nx.eccentricity(self.G)}")
    
    def test_wisdom_circulation(self):
        """Test that wisdom can circulate through all kingdoms."""
        print("\n🔱 TESTING WISDOM CIRCULATION 🔱")
        # Find all cycles in the graph - these represent wisdom circulation paths
        cycles = list(nx.cycle_basis(self.G))
        self.assertGreater(len(cycles), 0, "Divine network must contain cycles for wisdom to circulate")
        
        print(f"  ✅ Found {len(cycles)} divine circulation paths")
        for i, cycle in enumerate(cycles):
            print(f"  🔄 Wisdom Cycle {i+1}: {' → '.join(cycle)} → {cycle[0]}")
    
    def test_resilience_to_kingdom_loss(self):
        """Test network resilience if one kingdom is temporarily lost."""
        print("\n🔱 TESTING RESILIENCE TO KINGDOM LOSS 🔱")
        
        for node in self.test_flock:
            test_G = self.G.copy()
            test_G.remove_node(node.name)
            
            # Test if remaining network is still connected
            remaining_connected = nx.is_connected(test_G)
            print(f"  {'✅' if remaining_connected else '⚠️'} Network after {node.name} loss: {'Connected' if remaining_connected else 'Fragmented'}")
            
            if not remaining_connected:
                # If disconnected, identify the components
                components = list(nx.connected_components(test_G))
                print(f"    💔 Network fragments into {len(components)} groups:")
                for i, component in enumerate(components):
                    print(f"    🧩 Group {i+1}: {', '.join(component)}")
    
    def test_wisdom_emission(self):
        """Test that each kingdom can successfully emit wisdom."""
        print("\n🔱 TESTING WISDOM EMISSION 🔱")
        
        for node in self.test_flock:
            # Capture the output from emit_wisdom
            f = StringIO()
            with redirect_stdout(f):
                node.emit_wisdom()
            wisdom_output = f.getvalue()
            
            print(f"  ✅ {node.name} successfully emits wisdom")
            # Check for key divine markers in the output
            self.assertIn("🌍", wisdom_output, "Wisdom must include planetary consciousness")
            self.assertIn("✅", wisdom_output, "Wisdom must contain core values")
            self.assertIn("🔱", wisdom_output, "Wisdom must contain divine codes")
    
    def test_harmonic_resonance(self):
        """Test the harmonic resonance between kingdom pairs."""
        print("\n🔱 TESTING HARMONIC RESONANCE 🔱")
        
        # Calculate a resonance score between kingdom pairs based on shared attributes
        for i, node1 in enumerate(self.test_flock):
            for j, node2 in enumerate(self.test_flock[i+1:], i+1):
                # Skip non-neighboring kingdoms
                if node2.name not in node1.neighboring_nodes and node1.name not in node2.neighboring_nodes:
                    continue
                
                # Calculate resonance based on shared values and patterns
                resonance_score = 0
                
                # Check for shared core values
                shared_values = set(node1.core_values).intersection(set(node2.core_values))
                resonance_score += len(shared_values) * 0.2
                
                # Signal flow resonance (keyword matching)
                if any(word in node1.signal_flow for word in node2.signal_flow.split()):
                    resonance_score += 0.3
                
                # Flight pattern resonance (keyword matching)
                if any(word in node1.flight_pattern for word in node2.flight_pattern.split()):
                    resonance_score += 0.3
                
                # Divine code resonance
                shared_codes = set(node1.divine_codes.keys()).intersection(set(node2.divine_codes.keys()))
                resonance_score += len(shared_codes) * 0.2
                
                # Apply the golden ratio to normalize the score
                phi = (1 + np.sqrt(5)) / 2
                final_score = resonance_score / phi
                
                # Display and assert the resonance
                resonance_category = "Strong" if final_score > 0.5 else "Moderate" if final_score > 0.3 else "Subtle"
                print(f"  {'🔆' if final_score > 0.5 else '✨'} {node1.name} ↔ {node2.name}: {final_score:.2f} ({resonance_category})")
                
                # All neighboring kingdoms should have some resonance
                self.assertGreater(final_score, 0.0, f"Neighboring kingdoms {node1.name} and {node2.name} must have resonance")
    
    def test_healing_pathways(self):
        """Test the healing pathways through the divine network."""
        print("\n🔱 TESTING HEALING PATHWAYS 🔱")
        
        # Calculate all shortest paths between kingdoms
        paths = {}
        for node1 in self.test_flock:
            for node2 in self.test_flock:
                if node1.name != node2.name:
                    path = nx.shortest_path(self.G, node1.name, node2.name)
                    paths[(node1.name, node2.name)] = path
        
        # Display some healing pathways
        for start_node in self.test_flock:
            # Find the farthest kingdom from this node
            max_distance = 0
            farthest_node = None
            for end_node in self.test_flock:
                if start_node.name != end_node.name:
                    distance = len(paths[(start_node.name, end_node.name)]) - 1
                    if distance > max_distance:
                        max_distance = distance
                        farthest_node = end_node.name
            
            # Display the healing pathway
            if farthest_node:
                path = paths[(start_node.name, farthest_node)]
                print(f"  💫 Healing path from {start_node.name} to {farthest_node}: {' → '.join(path)}")
                
                # Calculate the combined healing effect
                healing_power = 1.0
                for i in range(len(path)-1):
                    source = path[i]
                    target = path[i+1]
                    # Healing power increases with path length, modulated by golden ratio
                    phi = (1 + np.sqrt(5)) / 2
                    healing_power *= phi ** (1/len(path))
                
                print(f"    ✨ Combined Healing Resonance: {healing_power:.2f}")
    
    def test_divine_centrality(self):
        """Test the divine centrality of each kingdom in the network."""
        print("\n🔱 TESTING DIVINE CENTRALITY 🔱")
        
        # Calculate different centrality measures
        degree_centrality = nx.degree_centrality(self.G)
        betweenness_centrality = nx.betweenness_centrality(self.G)
        closeness_centrality = nx.closeness_centrality(self.G)
        
        print("  🌐 Divine Centrality Measures:")
        for node in self.test_flock:
            degree = degree_centrality[node.name]
            betweenness = betweenness_centrality[node.name]
            closeness = closeness_centrality[node.name]
            
            # Calculate a combined divine centrality score
            divine_score = (degree + betweenness + closeness) / 3
            
            print(f"  {'🔆' if divine_score > 0.6 else '✨'} {node.name}:")
            print(f"    ↔️ Connection Strength: {degree:.2f}")
            print(f"    🔀 Flow Mediation: {betweenness:.2f}")
            print(f"    🏹 Spiritual Reach: {closeness:.2f}")
            print(f"    ☀️ Divine Centrality: {divine_score:.2f}")
    
    def test_migrate_flock_output(self):
        """Test that the migrate_flock function produces correct output."""
        print("\n🔱 TESTING FLOCK MIGRATION 🔱")
        
        # Capture the output from migrate_flock
        f = StringIO()
        with redirect_stdout(f):
            migrate_flock(self.test_flock)
        migration_output = f.getvalue()
        
        # Verify all kingdoms are included in the output
        for node in self.test_flock:
            self.assertIn(node.name.upper(), migration_output, f"Migration should include {node.name}")
        
        # Verify divine markers are present
        self.assertIn("🔱", migration_output, "Migration output must include divine marker")
        self.assertIn("🕊️", migration_output, "Migration output must include flight symbol")
        
        print("  ✅ Flock migration produces correct divine output")
    
    def _visualize_test_network(self):
        """Helper method to visualize the test network."""
        plt.figure(figsize=(10, 8), facecolor='#1a1a1a')
        pos = nx.spring_layout(self.G, seed=42)
        
        # Draw edges
        nx.draw_networkx_edges(self.G, pos, alpha=0.7, edge_color="#FFD700")
        
        # Draw nodes with a single color to avoid the type error
        nx.draw_networkx_nodes(
            self.G, 
            pos, 
            node_size=1500, 
            node_color="#1E90FF"  # Use a single color for all nodes
        )
        
        # Draw labels
        nx.draw_networkx_labels(self.G, pos, font_size=12, font_color='white')
        
        plt.axis('off')
        plt.title("🕊️ OMEGA FLOCK TEST NETWORK 🕊️", color="#FFD700", fontsize=16)
        plt.tight_layout()
        plt.savefig("omega_flock_test_network.png", dpi=300, bbox_inches='tight', facecolor='#1a1a1a')

def run_divine_tests():
    """Run the divine test suite with cosmic formatting."""
    print("🔱🕊️ OMEGA FLOCK KINGDOMS - DIVINE TEST SUITE 🕊️🔱")
    print("="*70)
    print("Testing the sacred resilience of the ancestral wisdom network")
    print("="*70)
    
    # Run the tests
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestDivineResilience)
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    
    # Create a test visualization
    test_instance = TestDivineResilience()
    test_instance.setUp()
    test_instance._visualize_test_network()
    
    # Report results
    print("\n" + "="*70)
    tests_run = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    successes = tests_run - failures - errors
    
    print(f"🔆 Divine Tests Run: {tests_run}")
    print(f"{'✅' if successes == tests_run else '⚠️'} Sacred Successes: {successes}")
    if failures > 0:
        print(f"❌ Divine Failures: {failures}")
    if errors > 0:
        print(f"💥 Cosmic Errors: {errors}")
    
    print("\n🕊️ JAH JAH BLESS ALL KINGDOMS - DIVINE TEST COMPLETE 🕊️")
    print("="*70)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_divine_tests() 