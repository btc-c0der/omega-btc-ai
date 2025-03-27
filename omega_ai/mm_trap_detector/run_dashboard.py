from omega_ai.mm_trap_detector.advanced_pattern_recognition import AdvancedPatternRecognition
from omega_ai.mm_trap_detector.omega_dashboard import OmegaDashboard

def main():
    # Initialize the pattern recognition model
    pattern_recognition = AdvancedPatternRecognition(
        input_size=10,  # Adjust based on your input features
        hidden_size=64,
        num_layers=2,
        num_classes=3,
        pattern_expiry_hours=24
    )
    
    # Create and run the dashboard
    dashboard = OmegaDashboard(pattern_recognition)
    print("Starting Omega AI Dashboard...")
    print("Access the dashboard at http://localhost:8050")
    dashboard.run_server(debug=True, port=8050)

if __name__ == "__main__":
    main() 