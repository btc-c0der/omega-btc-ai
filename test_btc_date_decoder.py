#!/usr/bin/env python3
"""
OMEGA BTC AI - Test BTC Date Decoder
===================================

This module contains tests for the BTC Date Decoder module.

Copyright (C) 2024 OMEGA BTC AI Team
License: GNU General Public License v3.0

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import unittest
import datetime
import pytz
from freezegun import freeze_time
from omega_ai.utils.btc_date_decoder import (
    analyze_date,
    analyze_october_29_2023,
    get_btc_age,
    get_halving_phase,
    calculate_market_cycle_phase,
    calculate_golden_ratio_time_alignment
)

class TestBtcDateDecoder(unittest.TestCase):
    """Test the Bitcoin date decoder functionality."""
    
    def test_get_btc_age(self):
        """Test getting Bitcoin's age at a specific timestamp."""
        # Bitcoin's anniversary
        anniversary_date = datetime.datetime(2019, 1, 3, tzinfo=pytz.UTC)
        age = get_btc_age(anniversary_date)
        
        self.assertEqual(age.years, 9)  # Genesis block was on Jan 3, 2009, so on Jan 3, 2019 it's 9 years old
        self.assertEqual(age.months, 11)  # 9 years and 11 months (dateutil counts months differently)
        
    def test_halving_phase(self):
        """Test getting the halving phase for a specific timestamp."""
        # Date between third and fourth halving
        test_date = datetime.datetime(2022, 6, 15, tzinfo=pytz.UTC)
        phase = get_halving_phase(test_date)
        
        self.assertEqual(phase["cycle_name"], "Third to Fourth Halving")
        self.assertTrue(0 <= phase["percentage_complete"] <= 100)
        
    @freeze_time("2023-10-29 12:00:00", tz_offset=0)
    def test_october_29_2023_analysis(self):
        """Test analysis of October 29, 2023."""
        analysis = analyze_october_29_2023()
        
        # Check basic structure
        self.assertIn("date_str", analysis)
        self.assertIn("btc_age", analysis)
        self.assertIn("halving_phase", analysis)
        self.assertIn("market_cycles", analysis)
        self.assertIn("time_alignment", analysis)
        self.assertIn("divine_date_score", analysis)
        self.assertIn("divine_date_rating", analysis)
        self.assertIn("specific_btc_data", analysis)
        
        # Check specific data values
        self.assertEqual(analysis["specific_btc_data"]["closing_price"], 34535.77)
        self.assertEqual(analysis["specific_btc_data"]["24h_change"], 1.3)
        
    def test_market_cycle_phase(self):
        """Test market cycle phase calculation."""
        # Test with a specific date
        test_date = datetime.datetime(2023, 5, 1, tzinfo=pytz.UTC)
        cycles = calculate_market_cycle_phase(test_date)
        
        # Check all cycle types are present
        self.assertIn("micro", cycles)
        self.assertIn("short", cycles)
        self.assertIn("intermediate", cycles)
        self.assertIn("primary", cycles)
        self.assertIn("major", cycles)
        self.assertIn("grand", cycles)
        
        # Check structure of a cycle entry
        self.assertIn("cycle_length_days", cycles["micro"])
        self.assertIn("days_into_cycle", cycles["micro"])
        self.assertIn("days_remaining", cycles["micro"])
        self.assertIn("phase_percentage", cycles["micro"])
        self.assertIn("phase_description", cycles["micro"])
        
    def test_golden_ratio_time_alignment(self):
        """Test golden ratio time alignment calculation."""
        # Test with a specific date
        test_date = datetime.datetime(2023, 10, 29, 13, 25, 47, tzinfo=pytz.UTC)
        alignment = calculate_golden_ratio_time_alignment(test_date)
        
        # Check structure
        self.assertIn("day_cycle_phase", alignment)
        self.assertIn("week_cycle_phase", alignment)
        self.assertIn("month_phase", alignment)
        self.assertIn("year_phase", alignment)
        self.assertIn("overall_temporal_harmony", alignment)
        self.assertIn("harmony_description", alignment)
        
        # Check value ranges
        self.assertTrue(0 <= alignment["day_cycle_phase"] <= 1)
        self.assertTrue(0 <= alignment["week_cycle_phase"] <= 1)
        self.assertTrue(0 <= alignment["overall_temporal_harmony"] <= 1)
        
    def test_analyze_date_string(self):
        """Test analyzing a date from a string."""
        analysis = analyze_date(date_str="2021-04-14")  # Coinbase IPO day
        
        # Check basic structure
        self.assertIn("date_str", analysis)
        self.assertIn("btc_age", analysis)
        self.assertIn("halving_phase", analysis)
        self.assertIn("market_cycles", analysis)
        self.assertIn("divine_date_score", analysis)
        
        # Check the interpreted date is correct
        self.assertEqual(analysis["date_str"][:10], "2021-04-14")
        
    def test_analyze_date_error_handling(self):
        """Test error handling in analyze_date function."""
        # Invalid date format
        result = analyze_date(date_str="invalid-date")
        self.assertIn("error", result)
        
    def test_divine_date_score_range(self):
        """Test divine date score is always in the correct range."""
        for month in range(1, 13):
            for day in range(1, 28, 7):  # Sample days across the year
                test_date = datetime.datetime(2023, month, day, tzinfo=pytz.UTC)
                analysis = analyze_date(timestamp=test_date)
                
                # Score should always be between 0 and 1
                self.assertTrue(0 <= analysis["divine_date_score"] <= 1)

if __name__ == "__main__":
    unittest.main() 