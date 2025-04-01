import json
import graphviz
from collections import defaultdict
import os
from datetime import datetime

def load_simulation_data():
    # Find the most recent simulation file
    sim_dir = 'omega_king_runs'
    json_files = [f for f in os.listdir(sim_dir) if f.endswith('run_summary.json')]
    if not json_files:
        raise FileNotFoundError("No simulation data found")
    
    latest_file = os.path.join(sim_dir, 'run_summary.json')
    with open(latest_file, 'r') as f:
        return json.load(f)

def create_state_visualization(state_counts, total_transitions):
    # Create a new directed graph
    dot = graphviz.Digraph('state_transitions')
    dot.attr(rankdir='LR')
    
    # Color scheme for states
    state_colors = {
        'ANALYZING': '#FFD700',  # Gold
        'TRAP_DETECTION': '#FF6B6B',  # Red
        'LONG_SETUP': '#4CAF50',  # Green
        'SHORT_SETUP': '#2196F3',  # Blue
        'SCALING_UP': '#9C27B0',  # Purple
        'SCALING_DOWN': '#FF9800',  # Orange
        'CLOSING_LONG': '#795548',  # Brown
        'CLOSING_SHORT': '#4CAF50',  # Green
        'WAITING_FOR_REENTRY': '#607D8B',  # Blue Grey
        'REENTRY_SETUP': '#009688',  # Teal
        'IDLE': '#9E9E9E'  # Grey
    }
    
    # Add nodes with state counts
    for state, count in state_counts.items():
        if count > 0:  # Only show states that were visited
            percentage = (count / total_transitions) * 100
            label = f"{state}\n{count} visits\n({percentage:.1f}%)"
            dot.node(state, label, 
                    style='filled', 
                    fillcolor=state_colors.get(state, '#CCCCCC'),
                    fontcolor='black')
    
    # Add edges between states that can transition
    valid_transitions = {
        'IDLE': ['ANALYZING'],
        'ANALYZING': ['TRAP_DETECTION', 'LONG_SETUP', 'SHORT_SETUP'],
        'TRAP_DETECTION': ['ANALYZING', 'LONG_SETUP', 'SHORT_SETUP'],
        'LONG_SETUP': ['SCALING_UP', 'WAITING_FOR_REENTRY'],
        'SHORT_SETUP': ['SCALING_DOWN', 'WAITING_FOR_REENTRY'],
        'SCALING_UP': ['CLOSING_LONG', 'SCALING_UP'],
        'SCALING_DOWN': ['CLOSING_SHORT', 'SCALING_DOWN'],
        'CLOSING_LONG': ['WAITING_FOR_REENTRY', 'REENTRY_SETUP'],
        'CLOSING_SHORT': ['WAITING_FOR_REENTRY', 'REENTRY_SETUP'],
        'WAITING_FOR_REENTRY': ['REENTRY_SETUP', 'ANALYZING'],
        'REENTRY_SETUP': ['LONG_SETUP', 'SHORT_SETUP']
    }
    
    # Add edges with transition probabilities
    for source, targets in valid_transitions.items():
        if state_counts.get(source, 0) > 0:  # Only process states that were visited
            for target in targets:
                if state_counts.get(target, 0) > 0:  # Only connect to states that were visited
                    # Calculate edge thickness based on state counts
                    weight = 1 + (min(state_counts[source], state_counts[target]) / total_transitions) * 5
                    dot.edge(source, target, penwidth=str(weight))
    
    return dot

def main():
    try:
        # Load simulation data
        data = load_simulation_data()
        state_counts = data.get('state_counts', {})
        total_transitions = data.get('total_transitions', 0)
        
        if not state_counts:
            print("❌ No state counts found in simulation data")
            return
        
        # Create visualization
        dot = create_state_visualization(state_counts, total_transitions)
        
        # Save visualization
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'state_transitions_{timestamp}'
        dot.render(output_file, format='png', cleanup=True)
        
        # Print statistics
        print(f"\n✅ Generated visualization of state transitions")
        print(f"📊 Total transitions: {total_transitions}")
        print(f"📝 Saved to: {output_file}.png")
        
        # Print state statistics
        print("\n📊 State Statistics:")
        total_visits = sum(state_counts.values())
        for state, count in sorted(state_counts.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                percentage = (count / total_visits) * 100
                print(f"{state}: {count} visits ({percentage:.1f}%)")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 