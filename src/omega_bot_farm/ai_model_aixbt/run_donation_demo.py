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

"""
AIXBT Quantum Donation Integration Demo
=======================================

Demonstrates the integration between the Mock Quantum Divergence Predictor
and the AIXBT Donation system, showcasing how 80% of proceeds from quantum
predictions can be automatically allocated to Omega NGO.

Usage:
    python -m src.omega_bot_farm.ai_model_aixbt.run_donation_demo
"""

import os
import sys
import logging
import json
from datetime import datetime, timezone

# Add the project root to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("aixbt-donation-demo")

# Import from local modules
try:
    from src.omega_bot_farm.ai_model_aixbt.quantum_donation_bridge import QuantumDonationBridge
    from src.omega_bot_farm.ai_model_aixbt.donation_integration import DonationManager, SmartContractIntegration
    MODULES_AVAILABLE = True
except ImportError:
    logger.error("Failed to import required modules. Make sure you're running from project root.")
    MODULES_AVAILABLE = False

def print_banner():
    """Print demo banner."""
    print("\n" + "=" * 78)
    print(f"{'AIXBT QUANTUM DONATION INTEGRATION DEMO':^78}")
    print("=" * 78)
    print(f"{'80% of AIXBT Proceeds Donated to Omega NGO':^78}")
    print(f"{'Powered by Mock Quantum Divergence Prediction':^78}")
    print("-" * 78)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"{'Started at: ' + timestamp:^78}")
    print("=" * 78 + "\n")

def print_section(title):
    """Print section header."""
    print("\n" + "-" * 78)
    print(f"{title:^78}")
    print("-" * 78)

def save_output(result, output_path="outputs/donation_demo_result.json"):
    """Save the demo result to a JSON file."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            # Convert non-serializable objects to strings
            def json_serializable(obj):
                if isinstance(obj, (datetime, )):
                    return obj.isoformat()
                try:
                    return float(obj)
                except:
                    return str(obj)
            
            json.dump(result, f, indent=2, default=json_serializable)
        print(f"Results saved to {output_path}")
    except Exception as e:
        logger.error(f"Error saving output: {e}")

def run_single_prediction_demo():
    """Run a demo with a single prediction."""
    print_section("Single Prediction Demo")
    
    # Create quantum donation bridge
    print("Initializing Quantum Donation Bridge...")
    bridge = QuantumDonationBridge()
    
    # Run a prediction with donation
    print("Running quantum prediction with donation processing...")
    result = bridge.run_quantum_prediction_with_donation(revenue_estimate=1000.0)
    
    # Display prediction result
    print("\nPrediction Result:")
    if "predicted_divergence" in result:
        print(f"  Predicted AIXBT-BTC Divergence: {float(result['predicted_divergence']):.6f}")
        print(f"  Prediction Confidence: {float(result['confidence']):.4f}")
        if "entanglement_info" in result:
            ent = result["entanglement_info"]
            print(f"  Overall Entanglement: {float(ent.get('overall_entanglement', 0)):.4f}")
    else:
        print("  No prediction data available")
    
    # Display donation info
    if "donation" in result:
        donation = result["donation"]
        print("\nDonation Details:")
        print(f"  Revenue Amount: ${float(donation.get('revenue_amount', 0)):.2f}")
        print(f"  Donation Amount: ${float(donation.get('amount', 0)):.2f} " +
              f"({float(donation.get('percentage', 0)):.1f}%)")
        print(f"  Recipient: {donation.get('recipient', 'Unknown')}")
        print(f"  Donation ID: {donation.get('donation_id', 'N/A')}")
        print(f"  Status: {donation.get('status', 'Unknown')}")
    
    # Display donation processing info
    if "donation_processing" in result:
        processing = result["donation_processing"]
        print("\nDonation Processing Status:")
        print(f"  Status: {processing.get('status', 'Unknown')}")
        
        tx_hash = None
        if "transaction_hash" in processing:
            tx_hash = processing.get("transaction_hash")
        elif "transaction" in processing:
            tx_hash = processing.get("transaction", {}).get("transaction_hash")
        
        if tx_hash:
            print(f"  Transaction Hash: {tx_hash}")
    
    return result

def run_impact_assessment_demo(bridge):
    """Run a demo of impact assessment."""
    print_section("Impact Assessment Demo")
    
    if not bridge or not bridge.donation_manager:
        print("Donation manager not available for impact assessment")
        return {}
    
    # Generate impact report
    print("Generating donation impact report...")
    impact = bridge.donation_manager.generate_impact_report()
    
    # Display impact metrics
    print("\nDonation Impact Metrics:")
    print(f"  Total Donated: ${impact.get('total_donated', 0):.2f}")
    print(f"  Donation Count: {impact.get('donation_count', 0)}")
    print(f"  Average Donation: ${impact.get('average_donation', 0):.2f}")
    
    if "estimated_impact" in impact:
        est = impact["estimated_impact"]
        print("\nEstimated Real-World Impact:")
        print(f"  Lives Impacted: {est.get('lives_impacted', 0)}")
        print(f"  Community Projects: {est.get('community_projects', 0)}")
        print(f"  Sustainability Score: {est.get('sustainability_score', 0):.1f}/10")
    
    # Display timeline
    print("\nDonation Timeline:")
    print(f"  First Donation: {impact.get('first_donation', 'N/A')}")
    print(f"  Latest Donation: {impact.get('latest_donation', 'N/A')}")
    print(f"  Report Generated: {impact.get('generated_at', 'N/A')}")
    
    return impact

def run_multiple_predictions_demo():
    """Run a demo with multiple predictions to show cumulative effect."""
    print_section("Multiple Predictions Demo")
    
    # Create quantum donation bridge
    bridge = QuantumDonationBridge()
    
    # Run multiple predictions
    print("Running 5 sequential predictions with varying revenue...")
    revenues = [500.0, 750.0, 1200.0, 900.0, 1500.0]
    results = []
    
    for i, revenue in enumerate(revenues):
        print(f"\nPrediction {i+1} (Revenue: ${revenue:.2f}):")
        result = bridge.run_quantum_prediction_with_donation(revenue_estimate=revenue)
        
        # Display minimal info
        if "donation" in result:
            donation = result["donation"]
            print(f"  Donation Amount: ${float(donation.get('amount', 0)):.2f}")
            print(f"  Status: {donation.get('status', 'Unknown')}")
        
        results.append(result)
    
    # Get cumulative metrics
    metrics = bridge.get_performance_metrics()
    
    print("\nCumulative Metrics:")
    print(f"  Predictions Processed: {metrics.get('predictions_processed', 0)}")
    print(f"  Donations Initiated: {metrics.get('donations_initiated', 0)}")
    print(f"  Total Revenue: ${metrics.get('total_predicted_value', 0):.2f}")
    print(f"  Total Donations: ${metrics.get('total_donation_value', 0):.2f}")
    
    if "donation_summary" in metrics:
        summary = metrics["donation_summary"]
        print(f"  Completed Donations: {summary.get('completed_donations', 0)}")
        print(f"  Pending Donations: {summary.get('pending_donations', 0)}")
    
    return {"results": results, "metrics": metrics}

def main():
    """Run the donation integration demo."""
    print_banner()
    
    if not MODULES_AVAILABLE:
        print("Required modules not available. Cannot run demonstration.")
        return
    
    try:
        # Make sure config directory exists
        config_dir = os.path.join(current_dir, "config")
        os.makedirs(config_dir, exist_ok=True)
        
        # Run single prediction demo
        single_result = run_single_prediction_demo()
        
        # Create bridge for impact assessment
        bridge = QuantumDonationBridge()
        
        # Run impact assessment demo
        impact_result = run_impact_assessment_demo(bridge)
        
        # Run multiple predictions demo
        multi_result = run_multiple_predictions_demo()
        
        # Combine all results
        complete_result = {
            "single_prediction": single_result,
            "impact_assessment": impact_result,
            "multiple_predictions": multi_result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Save output
        save_output(complete_result)
        
        print_section("Demo Completed Successfully")
        print(f"{'Thank you for supporting Omega NGO through AIXBT':^78}")
        print(f"{'80% of all proceeds are automatically donated':^78}")
        print(f"\n{'🌸 WE BLOOM NOW AS ONE 🌸':^78}\n")
        
    except Exception as e:
        logger.error(f"Error in donation demo: {e}")
        import traceback
        logger.error(traceback.format_exc())
        print("\nAn error occurred during the demo. See logs for details.")

if __name__ == "__main__":
    main() 