"""
LUCAS SILVEIRA PORTAL - CRYPTO WALLET MODULE
============================================

Cryptocurrency wallet implementation for the Senegal SK8 donation system.
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

class CryptoWallet:
    """Quantum-inspired cryptocurrency wallet for Senegal SK8 donation system."""
    
    # Donation wallet addresses
    DONATION_WALLET = {
        "ethereum": "0x40993f26A65E8a09eEA605DE59D4C18826E30fE2",
        "bitcoin": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
        "solana": "9oN4SgJ9Qz6CX54kundR2wZkMbzo7xVK7PH5fgyBXANM"
    }
    
    # Virgil Abloh memorial addresses
    VIRGIL_MEMORIAL = {
        "ethereum": "0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE",
        "bitcoin": "bc1q9d8u7hsjn45h8vqsnzeptz9lz3plc08hu8j4nq",
        "solana": "7iRcDLQJgqK2FEimzJYQQJXHUZQKhYsHPURFkYjWjbGV"
    }
    
    # Default donation split (80/20)
    DEFAULT_SPLIT = {
        "senegal_sk8": 0.8,   # 80% to Senegal Sk8 organization
        "memorial": 0.2       # 20% to Virgil Abloh memorial fund
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the crypto wallet handler.
        
        Args:
            config_path: Path to configuration file (optional)
        """
        self.donation_history: List[Dict[str, Any]] = []
        self.config = self.DEFAULT_SPLIT.copy()
        
        # Load configuration if provided
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                try:
                    loaded_config = json.load(f)
                    if isinstance(loaded_config, dict):
                        self.config.update(loaded_config)
                except json.JSONDecodeError:
                    pass
    
    def get_donation_addresses(self) -> Dict[str, Dict[str, str]]:
        """Get donation addresses for all supported cryptocurrencies.
        
        Returns:
            Dictionary with organization names and their wallet addresses
        """
        return {
            "senegal_sk8": self.DONATION_WALLET,
            "virgil_memorial": self.VIRGIL_MEMORIAL
        }
    
    def calculate_donation_split(self, amount: float) -> Dict[str, float]:
        """Calculate how a donation will be split based on the 80/20 rule.
        
        Args:
            amount: Total donation amount
            
        Returns:
            Dictionary with the split amounts
        """
        return {
            "senegal_sk8": amount * self.config["senegal_sk8"],
            "memorial": amount * self.config["memorial"]
        }
    
    def format_donation_info(self, amount: float, currency: str) -> str:
        """Format donation information for display to user.
        
        Args:
            amount: Donation amount
            currency: Cryptocurrency being used
            
        Returns:
            Formatted string with donation information
        """
        split = self.calculate_donation_split(amount)
        
        # Format the output with Virgil Abloh inspired design
        output = [
            "╔══════════════════════════ \"DONATION DETAILS\" ══════════════════════════╗",
            f"║  \"TOTAL DONATION\":  {amount:.4f} {currency.upper()}                       ║",
            "╠══════════════════════════ \"QUANTUM SPLIT\" ═══════════════════════════╣",
            f"║  \"SENEGAL SK8 ORG\":  {split['senegal_sk8']:.4f} {currency.upper()} ({self.config['senegal_sk8']*100:.0f}%)           ║",
            f"║  \"VIRGIL MEMORIAL\":  {split['memorial']:.4f} {currency.upper()} ({self.config['memorial']*100:.0f}%)           ║",
            "╠═══════════════════════ \"DONATION ADDRESSES\" ═════════════════════════╣"
        ]
        
        # Add the wallet addresses
        if currency.lower() in self.DONATION_WALLET:
            output.append(f"║  \"SENEGAL SK8 ORG\":  {self.DONATION_WALLET[currency.lower()][:12]}...  ║")
            output.append(f"║  \"VIRGIL MEMORIAL\":  {self.VIRGIL_MEMORIAL[currency.lower()][:12]}...  ║")
        else:
            output.append("║  \"CRYPTOCURRENCY NOT SUPPORTED\"                                      ║")
        
        output.append("╚════════════════════════════════════════════════════════════════════════╝")
        return "\n".join(output)
    
    def record_donation(self, amount: float, currency: str, donor_name: Optional[str] = None) -> Dict[str, Any]:
        """Record a donation for tracking purposes.
        
        Args:
            amount: Donation amount
            currency: Cryptocurrency used
            donor_name: Name of donor (optional)
            
        Returns:
            Donation record
        """
        split = self.calculate_donation_split(amount)
        timestamp = datetime.now().isoformat()
        
        donation = {
            "id": f"donate_{int(time.time())}",
            "timestamp": timestamp,
            "donor": donor_name or "Anonymous",
            "amount": amount,
            "currency": currency,
            "split": split,
            "status": "confirmed"
        }
        
        self.donation_history.append(donation)
        return donation
    
    def get_donation_history(self) -> List[Dict[str, Any]]:
        """Get the complete donation history.
        
        Returns:
            List of donation records
        """
        return self.donation_history
    
    def get_totals(self) -> Dict[str, Dict[str, float]]:
        """Calculate total donations by currency and organization.
        
        Returns:
            Nested dictionary with totals
        """
        totals: Dict[str, Dict[str, float]] = {}
        
        for donation in self.donation_history:
            currency = donation["currency"]
            if currency not in totals:
                totals[currency] = {
                    "senegal_sk8": 0.0,
                    "memorial": 0.0,
                    "total": 0.0
                }
            
            totals[currency]["senegal_sk8"] += donation["split"]["senegal_sk8"]
            totals[currency]["memorial"] += donation["split"]["memorial"]
            totals[currency]["total"] += donation["amount"]
        
        return totals

    def generate_donation_qr(self, currency: str) -> str:
        """Generate QR code for donation (ASCII representation).
        
        Args:
            currency: Cryptocurrency to use
            
        Returns:
            ASCII representation of QR code
        """
        # Simple ASCII QR code representation
        address = self.DONATION_WALLET.get(currency.lower(), "")
        if not address:
            return "Currency not supported"
        
        qr = [
            "▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄",
            "█ ▄▄▄▄▄ █▀█▄▀▀█ ▄▄▄▄▄ █",
            "█ █   █ █▄▀ ▀▄█ █   █ █",
            "█ █▄▄▄█ █▄▀█▀▄█ █▄▄▄█ █",
            "█▄▄▄▄▄▄▄█▄█ █▄█▄▄▄▄▄▄▄█",
            "█ ▄█▀▄▄▀▄█▄█ ▀█▄█ ▀▄▀ █",
            "██▄█▄▄▄█▄▄ ▄▄█▀▄▀▀█ ▄▄█",
            "█ ▄▄▄▄▄ █▄▀▄▄█▄█▄▀ ▀▀▄█",
            "█ █   █ █ ▄█▀▄▄▀█▀▀▀▄▄█",
            "█ █▄▄▄█ █▀▄▄▀▄▄█▄█▄█▀▄█",
            "▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀"
        ]
        
        return "\n".join(qr) + f"\n\n{currency.upper()}: {address[:12]}...\n"

if __name__ == "__main__":
    # Test the wallet functionality
    wallet = CryptoWallet()
    print(wallet.format_donation_info(0.5, "ethereum"))
    print(wallet.generate_donation_qr("bitcoin")) 