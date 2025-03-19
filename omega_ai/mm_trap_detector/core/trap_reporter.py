"""
📊 TRAP REPORTER - AI-DRIVEN WEEKLY SUMMARY GENERATOR 📊
=====================================================

Generates insightful weekly summaries of detected traps and pattern evolution.
May your reports reveal the truth of market manipulation! 🔍

JAH BLESS THE TRUTHFUL MARKET VISION! 🙏
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any
from omega_ai.mm_trap_detector.core.mm_trap_detector import TrapDetection

class TrapReporter:
    """AI-driven trap report generator."""
    
    def __init__(self):
        """Initialize the trap reporter."""
        self.report_history: List[Dict[str, Any]] = []
    
    async def generate_weekly_report(self, traps: List[TrapDetection]) -> Dict[str, Any]:
        """Generate a weekly summary of detected traps."""
        report = {
            "timestamp": datetime.now(),
            "total_traps": len(traps),
            "pattern_evolution": self._analyze_pattern_evolution(traps),
            "market_condition": self._analyze_market_condition(traps),
            "confidence_trend": self._analyze_confidence_trend(traps),
            "trap_types": self._analyze_trap_types(traps)
        }
        
        self.report_history.append(report)
        return report
    
    async def analyze_pattern_evolution(self, traps: List[TrapDetection]) -> Dict[str, Any]:
        """Analyze how trap patterns have evolved."""
        if len(traps) < 2:
            return {"evolution": "insufficient_data"}
        
        # Sort traps by timestamp
        sorted_traps = sorted(traps, key=lambda x: x.timestamp)
        
        # Analyze pattern changes
        pattern_changes = []
        for i in range(1, len(sorted_traps)):
            prev_trap = sorted_traps[i-1]
            curr_trap = sorted_traps[i]
            
            change = {
                "time_diff": (curr_trap.timestamp - prev_trap.timestamp).total_seconds(),
                "confidence_change": curr_trap.confidence - prev_trap.confidence,
                "volume_change": curr_trap.volume - prev_trap.volume,
                "price_change": curr_trap.price - prev_trap.price
            }
            pattern_changes.append(change)
        
        return {
            "pattern_changes": pattern_changes,
            "market_adaptation": self._detect_market_adaptation(pattern_changes),
            "confidence_trend": self._calculate_confidence_trend(traps)
        }
    
    def _analyze_pattern_evolution(self, traps: List[TrapDetection]) -> Dict[str, Any]:
        """Analyze how trap patterns have evolved over time."""
        if not traps:
            return {"evolution": "no_data"}
        
        # Group traps by type
        type_groups = {}
        for trap in traps:
            if trap.type not in type_groups:
                type_groups[trap.type] = []
            type_groups[trap.type].append(trap)
        
        # Analyze each type's evolution
        evolution = {}
        for trap_type, type_traps in type_groups.items():
            evolution[trap_type.value] = {
                "count": len(type_traps),
                "avg_confidence": sum(t.confidence for t in type_traps) / len(type_traps),
                "pattern_complexity": self._calculate_pattern_complexity(type_traps)
            }
        
        return evolution
    
    def _analyze_market_condition(self, traps: List[TrapDetection]) -> Dict[str, Any]:
        """Analyze overall market conditions based on traps."""
        if not traps:
            return {"condition": "unknown"}
        
        # Calculate market stress indicators
        avg_confidence = sum(t.confidence for t in traps) / len(traps)
        trap_frequency = len(traps) / 7  # traps per day
        
        return {
            "market_stress": "high" if avg_confidence > 0.8 else "medium" if avg_confidence > 0.6 else "low",
            "trap_frequency": trap_frequency,
            "avg_confidence": avg_confidence
        }
    
    def _analyze_confidence_trend(self, traps: List[TrapDetection]) -> Dict[str, Any]:
        """Analyze confidence trends in trap detection."""
        if not traps:
            return {"trend": "no_data"}
        
        # Sort traps by timestamp
        sorted_traps = sorted(traps, key=lambda x: x.timestamp)
        
        # Calculate confidence trend
        confidences = [t.confidence for t in sorted_traps]
        trend = "increasing" if confidences[-1] > confidences[0] else "decreasing"
        
        return {
            "trend": trend,
            "start_confidence": confidences[0],
            "end_confidence": confidences[-1],
            "avg_confidence": sum(confidences) / len(confidences)
        }
    
    def _analyze_trap_types(self, traps: List[TrapDetection]) -> Dict[str, Any]:
        """Analyze distribution of trap types."""
        type_counts = {}
        for trap in traps:
            if trap.type not in type_counts:
                type_counts[trap.type] = 0
            type_counts[trap.type] += 1
        
        return {
            "distribution": {t.value: c for t, c in type_counts.items()},
            "most_common": max(type_counts.items(), key=lambda x: x[1])[0].value if type_counts else None
        }
    
    def _detect_market_adaptation(self, pattern_changes: List[Dict[str, Any]]) -> str:
        """Detect if market makers are adapting their techniques."""
        if not pattern_changes:
            return "no_adaptation"
        
        # Analyze changes in trap characteristics
        confidence_changes = [c["confidence_change"] for c in pattern_changes]
        volume_changes = [c["volume_change"] for c in pattern_changes]
        
        # Detect significant changes
        if any(abs(c) > 0.1 for c in confidence_changes):
            return "high_adaptation"
        elif any(abs(v) > 50 for v in volume_changes):
            return "medium_adaptation"
        else:
            return "low_adaptation"
    
    def _calculate_pattern_complexity(self, traps: List[TrapDetection]) -> float:
        """Calculate the complexity of trap patterns."""
        if not traps:
            return 0.0
        
        # Consider multiple factors for complexity
        avg_confidence = sum(t.confidence for t in traps) / len(traps)
        volume_variance = self._calculate_variance([t.volume for t in traps])
        price_variance = self._calculate_variance([t.price for t in traps])
        
        # Combine factors into complexity score
        complexity = (avg_confidence * 0.4 + 
                     min(volume_variance / 1000, 1) * 0.3 + 
                     min(price_variance / 1000, 1) * 0.3)
        
        return round(complexity * 100, 2)  # Convert to percentage
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of a list of values."""
        if not values:
            return 0.0
        
        mean = sum(values) / len(values)
        squared_diff_sum = sum((x - mean) ** 2 for x in values)
        return squared_diff_sum / len(values)
    
    def _calculate_confidence_trend(self, traps: List[TrapDetection]) -> Dict[str, Any]:
        """Calculate detailed confidence trend analysis."""
        if not traps:
            return {"trend": "no_data"}
        
        sorted_traps = sorted(traps, key=lambda x: x.timestamp)
        confidences = [t.confidence for t in sorted_traps]
        
        return {
            "trend": "increasing" if confidences[-1] > confidences[0] else "decreasing",
            "start_confidence": confidences[0],
            "end_confidence": confidences[-1],
            "avg_confidence": sum(confidences) / len(confidences),
            "variance": self._calculate_variance(confidences)
        } 