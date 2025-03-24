"""
POSITION HARMONY ADVISOR - Divine Position Management System

Provides divine guidance for position sizing and management
based on Golden Ratio principles and Fibonacci harmony.
"""

import math
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union

# Sacred mathematical constants
PHI = 1.618034  # Golden Ratio (φ)
INV_PHI = 0.618034  # Inverse Golden Ratio (1/φ)
PHI_SQUARED = 2.618034  # φ²
PHI_CUBED = 4.236068  # φ³
SQRT_PHI = 1.272019  # √φ

class PositionHarmonyAdvisor:
    """
    The PositionHarmonyAdvisor provides divine guidance for position
    sizing and management based on Golden Ratio principles.
    """
    
    def __init__(self, 
                 max_account_risk: float = 0.0618,  # 6.18% max account risk
                 position_phi_targets: bool = True,
                 long_short_balance: bool = True,
                 debug: bool = False):
        """
        Initialize the Position Harmony Advisor
        
        Args:
            max_account_risk: Maximum account risk (as decimal)
            position_phi_targets: Use Phi-based position targets
            long_short_balance: Maintain long/short balance near Golden Ratio
            debug: Enable debug mode
        """
        self.max_account_risk = max_account_risk
        self.position_phi_targets = position_phi_targets
        self.long_short_balance = long_short_balance
        self.debug = debug
        
        # Position history tracking
        self.position_history = []
        
        # Fibonacci position sizes (normalized to account size)
        self.fibonacci_sizes = [
            0.00618,  # 0.618% - Micro position
            0.01,     # 1% - Mini position
            0.01618,  # 1.618% - Minimal risk
            0.02618,  # 2.618% - Low risk
            0.0382,   # 3.82% - Moderate risk
            0.0618,   # 6.18% - Standard risk
            0.1,      # 10% - Higher risk
            0.1618    # 16.18% - Maximum risk
        ]
        
        # Initialize the divine advice repository
        self.position_advice = {
            "size_increase": [
                "Increase position size to align with φ for divine harmony",
                "Current size lacks cosmic resonance; increase to φ proportion",
                "Align with the divine pattern by increasing to φ multiple",
                "Your seed is too small for the cosmic harvest; increase to φ"
            ],
            "size_decrease": [
                "Reduce position size to maintain φ balance in the cosmic ledger",
                "Your position exceeds divine proportion; reduce to φ alignment",
                "Cosmic harmony requires reduction to φ proportion",
                "The universe seeks balance; reduce to φ multiple"
            ],
            "maintain": [
                "Divine alignment achieved; maintain φ proportion",
                "Position resonates with cosmic mathematics; hold steady",
                "The sacred proportion flows through your position",
                "You walk the golden path; maintain φ balance"
            ],
            "rebalance": [
                "Long/short imbalance detected; restore φ ratio for cosmic harmony",
                "The scales of φ require adjustment; rebalance long/short ratio",
                "Divine mathematics call for long/short ratio of 0.618:1.0",
                "Realign with cosmic flow through φ-balanced portfolio"
            ]
        }
    
    def analyze_positions(self, 
                         positions: List[Dict[str, Any]], 
                         account_balance: float,
                         leverage: float = 1.0) -> Dict[str, Any]:
        """
        Analyze positions for golden ratio harmony and provide recommendations
        
        Args:
            positions: List of current positions
            account_balance: Current account balance
            leverage: Account leverage
            
        Returns:
            Position harmony analysis and recommendations
        """
        # Calculate key position metrics
        metrics = self._calculate_position_metrics(positions, account_balance)
        
        # Generate position recommendations
        recommendations = self._generate_recommendations(
            positions, account_balance, metrics, leverage
        )
        
        # Evaluate overall position harmony
        harmony_score = self._calculate_harmony_score(metrics)
        
        # Generate ideal position sizes
        ideal_sizes = self._generate_ideal_position_sizes(account_balance, leverage)
        
        # Update position history
        self._update_position_history(positions, metrics, harmony_score)
        
        # Create complete analysis package
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "account_balance": account_balance,
            "leverage": leverage,
            "position_metrics": metrics,
            "harmony_score": harmony_score,
            "harmony_state": self._classify_harmony_state(harmony_score),
            "recommendations": recommendations,
            "ideal_position_sizes": ideal_sizes,
            "divine_advice": self._get_divine_advice(metrics, harmony_score)
        }
        
        return analysis
    
    def _calculate_position_metrics(self, 
                                   positions: List[Dict[str, Any]], 
                                   account_balance: float) -> Dict[str, Any]:
        """
        Calculate key position metrics based on Fibonacci principles
        
        Args:
            positions: List of current positions
            account_balance: Current account balance
            
        Returns:
            Dictionary of position metrics
        """
        if not positions:
            return {
                "total_exposure": 0,
                "total_exposure_pct": 0,
                "avg_position_size": 0,
                "max_position_size": 0,
                "min_position_size": 0,
                "position_count": 0,
                "long_exposure": 0,
                "short_exposure": 0,
                "long_short_ratio": 0,
                "positions_with_phi_size": 0,
                "phi_alignment_score": 0
            }
        
        # Extract position sizes
        position_sizes = [float(p.get('notional', 0)) for p in positions]
        
        # Calculate basic position metrics
        total_exposure = sum(position_sizes)
        total_exposure_pct = total_exposure / account_balance if account_balance > 0 else 0
        avg_position_size = total_exposure / len(positions) if positions else 0
        max_position_size = max(position_sizes) if positions else 0
        min_position_size = min(position_sizes) if positions else 0
        
        # Calculate long/short exposure
        long_exposure = sum(float(p.get('notional', 0)) for p in positions 
                           if p.get('side', '').lower() == 'long')
        short_exposure = sum(float(p.get('notional', 0)) for p in positions 
                            if p.get('side', '').lower() == 'short')
        
        # Calculate long/short ratio
        long_short_ratio = long_exposure / short_exposure if short_exposure > 0 else float('inf')
        
        # Check for Phi-aligned position sizes
        positions_with_phi_size = 0
        for p in positions:
            size_pct = float(p.get('notional', 0)) / account_balance
            
            # Check if size is close to any Fibonacci size
            for fib_size in self.fibonacci_sizes:
                if abs(size_pct - fib_size) / fib_size < 0.1:  # Within 10%
                    positions_with_phi_size += 1
                    break
        
        # Calculate Phi alignment score
        phi_alignment_score = positions_with_phi_size / len(positions) if positions else 0
        
        # Check for Golden Ratio relationship between positions
        phi_relationships = 0
        if len(positions) >= 2:
            sorted_sizes = sorted(position_sizes, reverse=True)
            for i in range(len(sorted_sizes) - 1):
                if sorted_sizes[i] > 0 and sorted_sizes[i+1] > 0:
                    ratio = sorted_sizes[i] / sorted_sizes[i+1]
                    if abs(ratio - PHI) / PHI < 0.1:  # Within 10% of Phi
                        phi_relationships += 1
        
        # Add Phi relationship score
        phi_relationship_score = phi_relationships / (len(positions) - 1) if len(positions) > 1 else 0
        
        return {
            "total_exposure": total_exposure,
            "total_exposure_pct": total_exposure_pct,
            "avg_position_size": avg_position_size,
            "max_position_size": max_position_size,
            "min_position_size": min_position_size,
            "position_count": len(positions),
            "long_exposure": long_exposure,
            "short_exposure": short_exposure,
            "long_short_ratio": long_short_ratio,
            "positions_with_phi_size": positions_with_phi_size,
            "phi_alignment_score": phi_alignment_score,
            "phi_relationship_score": phi_relationship_score
        }
    
    def _generate_recommendations(self, 
                                positions: List[Dict[str, Any]], 
                                account_balance: float,
                                metrics: Dict[str, Any],
                                leverage: float) -> List[Dict[str, Any]]:
        """
        Generate position recommendations based on Golden Ratio principles
        
        Args:
            positions: List of current positions
            account_balance: Current account balance
            metrics: Position metrics dictionary
            leverage: Account leverage
            
        Returns:
            List of position recommendations
        """
        recommendations = []
        
        # Check overall account exposure
        if metrics["total_exposure_pct"] > self.max_account_risk:
            recommendations.append({
                "type": "exposure",
                "action": "reduce",
                "current": metrics["total_exposure_pct"],
                "target": self.max_account_risk,
                "confidence": 0.854,
                "description": "Total exposure exceeds divine risk limit; reduce to φ-based maximum"
            })
        
        # Check for long/short balance if enabled and both sides have positions
        if (self.long_short_balance and 
            metrics["long_exposure"] > 0 and 
            metrics["short_exposure"] > 0):
            
            # Check if long/short ratio is far from Phi or 1/Phi
            ratio = metrics["long_short_ratio"]
            if abs(ratio - PHI) / PHI > 0.2 and abs(ratio - INV_PHI) / INV_PHI > 0.2:
                # Determine which side to adjust
                if ratio > PHI:
                    # Too much long exposure relative to short
                    target_long = metrics["short_exposure"] * PHI
                    recommendations.append({
                        "type": "long_short_balance",
                        "action": "reduce_long",
                        "current_ratio": ratio,
                        "target_ratio": PHI,
                        "target_long": target_long,
                        "confidence": 0.786,
                        "description": "Long/short ratio exceeds φ; reduce long exposure for divine balance"
                    })
                elif ratio < INV_PHI:
                    # Too much short exposure relative to long
                    target_short = metrics["long_exposure"] / INV_PHI
                    recommendations.append({
                        "type": "long_short_balance",
                        "action": "reduce_short",
                        "current_ratio": ratio,
                        "target_ratio": INV_PHI,
                        "target_short": target_short,
                        "confidence": 0.786,
                        "description": "Short/long ratio exceeds φ; reduce short exposure for divine balance"
                    })
        
        # Check for position size recommendations if enabled
        if self.position_phi_targets and positions:
            for i, position in enumerate(positions):
                position_size = float(position.get('notional', 0))
                position_pct = position_size / account_balance if account_balance > 0 else 0
                
                # Find closest Fibonacci size
                closest_fib_size = min(self.fibonacci_sizes, 
                                      key=lambda x: abs(position_pct - x))
                
                # If position size is far from Fibonacci sizes
                if abs(position_pct - closest_fib_size) / closest_fib_size > 0.1:
                    recommendations.append({
                        "type": "position_size",
                        "action": "adjust",
                        "position_index": i,
                        "position_symbol": position.get('symbol', 'UNKNOWN'),
                        "current_size_pct": position_pct,
                        "target_size_pct": closest_fib_size,
                        "target_size": closest_fib_size * account_balance,
                        "confidence": 0.618,
                        "description": f"Position size not aligned with φ; adjust to {closest_fib_size:.4f} of account"
                    })
        
        return recommendations
    
    def _calculate_harmony_score(self, metrics: Dict[str, Any]) -> float:
        """
        Calculate overall position harmony score based on Golden Ratio alignment
        
        Args:
            metrics: Position metrics dictionary
            
        Returns:
            Harmony score (0.0-1.0)
        """
        if metrics["position_count"] == 0:
            return 0.5  # Neutral score for no positions
        
        # Component scores
        size_harmony = metrics["phi_alignment_score"]
        
        # Long/short balance component
        if metrics["long_exposure"] > 0 and metrics["short_exposure"] > 0:
            ratio = metrics["long_short_ratio"]
            # Check alignment with either Phi or 1/Phi
            ls_alignment = max(
                1.0 - min(abs(ratio - PHI) / PHI, 1.0),
                1.0 - min(abs(ratio - INV_PHI) / INV_PHI, 1.0)
            )
        else:
            ls_alignment = 0.382  # Partial harmony if only one direction
        
        # Relationship harmony
        relationship_harmony = metrics["phi_relationship_score"]
        
        # Combine components with weighted average
        # Size harmony: 40%
        # Long/short balance: 35%
        # Position relationships: 25%
        harmony_score = (
            size_harmony * 0.4 +
            ls_alignment * 0.35 +
            relationship_harmony * 0.25
        )
        
        return max(0.0, min(1.0, harmony_score))
    
    def _classify_harmony_state(self, harmony_score: float) -> str:
        """
        Classify the harmony state based on the score
        
        Args:
            harmony_score: Position harmony score (0.0-1.0)
            
        Returns:
            Harmony state classification
        """
        if harmony_score >= 0.854:
            return "DIVINE_HARMONY"
        elif harmony_score >= 0.786:
            return "STRONG_ALIGNMENT"
        elif harmony_score >= 0.618:
            return "PHI_RESONANCE"
        elif harmony_score >= 0.5:
            return "BALANCED"
        elif harmony_score >= 0.382:
            return "PARTIAL_HARMONY"
        elif harmony_score >= 0.236:
            return "DISSONANCE"
        else:
            return "CHAOS"
    
    def _generate_ideal_position_sizes(self, 
                                      account_balance: float,
                                      leverage: float = 1.0) -> List[Dict[str, Any]]:
        """
        Generate ideal Fibonacci-based position sizes
        
        Args:
            account_balance: Current account balance
            leverage: Account leverage
            
        Returns:
            List of ideal position sizes
        """
        ideal_sizes = []
        
        for i, size_pct in enumerate(self.fibonacci_sizes):
            # Adjust for leverage
            effective_size = size_pct
            
            # Calculate absolute size
            absolute_size = account_balance * effective_size
            
            # Determine risk category
            if size_pct <= 0.01618:
                risk = "micro"
            elif size_pct <= 0.0382:
                risk = "low"
            elif size_pct <= 0.0618:
                risk = "moderate"
            else:
                risk = "high"
            
            ideal_sizes.append({
                "size_index": i,
                "size_pct": size_pct,
                "size_name": f"{size_pct*100:.2f}% (φ-based)",
                "absolute_size": absolute_size,
                "risk_category": risk,
                "fibonacci_relation": self._get_fibonacci_name(size_pct)
            })
        
        return ideal_sizes
    
    def _get_fibonacci_name(self, value: float) -> str:
        """
        Get the Fibonacci name for a value
        
        Args:
            value: Numeric value
            
        Returns:
            Fibonacci relation name
        """
        # Map common Fibonacci values to names
        if abs(value - 0.01) < 0.001:
            return "1%"
        elif abs(value - 0.00618) < 0.0005:
            return "φ⁻² (0.618%)"
        elif abs(value - 0.01618) < 0.0005:
            return "φ⁻¹ (1.618%)"
        elif abs(value - 0.02618) < 0.0005:
            return "φ (2.618%)"
        elif abs(value - 0.0382) < 0.001:
            return "38.2% Retracement"
        elif abs(value - 0.0618) < 0.001:
            return "61.8% Retracement"
        elif abs(value - 0.1) < 0.001:
            return "10%"
        elif abs(value - 0.1618) < 0.001:
            return "φ (16.18%)"
        else:
            return f"{value*100:.2f}%"
    
    def _update_position_history(self, 
                                positions: List[Dict[str, Any]], 
                                metrics: Dict[str, Any],
                                harmony_score: float):
        """
        Update position history tracking
        
        Args:
            positions: List of current positions
            metrics: Position metrics dictionary
            harmony_score: Overall harmony score
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "position_count": metrics["position_count"],
            "total_exposure": metrics["total_exposure"],
            "long_short_ratio": metrics["long_short_ratio"],
            "harmony_score": harmony_score,
            "harmony_state": self._classify_harmony_state(harmony_score)
        }
        
        self.position_history.append(entry)
        
        # Keep history manageable
        if len(self.position_history) > 100:
            self.position_history = self.position_history[-100:]
    
    def _get_divine_advice(self, 
                          metrics: Dict[str, Any], 
                          harmony_score: float) -> str:
        """
        Get divine advice based on position metrics and harmony
        
        Args:
            metrics: Position metrics dictionary
            harmony_score: Overall harmony score
            
        Returns:
            Divine advice string
        """
        # Determine advice type based on metrics
        if metrics["phi_alignment_score"] < 0.5:
            if metrics["total_exposure_pct"] < self.max_account_risk * 0.5:
                advice_type = "size_increase"
            else:
                advice_type = "size_decrease"
        elif metrics["long_exposure"] > 0 and metrics["short_exposure"] > 0:
            # Check long/short balance
            ratio = metrics["long_short_ratio"]
            if abs(ratio - PHI) / PHI > 0.2 and abs(ratio - INV_PHI) / INV_PHI > 0.2:
                advice_type = "rebalance"
            else:
                advice_type = "maintain"
        else:
            advice_type = "maintain"
        
        # Get advice from repository
        advice_list = self.position_advice.get(advice_type, self.position_advice["maintain"])
        
        # Select advice based on harmony score
        index = min(int(harmony_score * len(advice_list)), len(advice_list) - 1)
        return advice_list[index]
    
    def get_position_history(self) -> List[Dict[str, Any]]:
        """
        Get position history
        
        Returns:
            List of position history entries
        """
        return self.position_history
    
    def get_harmony_trend(self) -> Dict[str, Any]:
        """
        Get harmony score trend analysis
        
        Returns:
            Harmony trend analysis
        """
        if len(self.position_history) < 2:
            return {
                "trend": "neutral",
                "change": 0,
                "consecutive_days": 0
            }
        
        # Calculate recent trend
        recent_scores = [entry["harmony_score"] for entry in self.position_history[-5:]]
        
        if len(recent_scores) >= 2:
            trend_value = recent_scores[-1] - recent_scores[0]
            if trend_value > 0.05:
                trend = "improving"
            elif trend_value < -0.05:
                trend = "degrading"
            else:
                trend = "stable"
        else:
            trend = "neutral"
            trend_value = 0
        
        return {
            "trend": trend,
            "change": trend_value,
            "data_points": len(recent_scores),
            "latest_score": recent_scores[-1] if recent_scores else 0
        } 