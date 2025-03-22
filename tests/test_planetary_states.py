"""
Test suite for planetary state calculations (combustion, war, etc.)
"""

import sys
import os
import unittest
from datetime import datetime
import math

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vedic_calculator.core import VedicCalculator


class TestPlanetaryStates(unittest.TestCase):
    """Test cases for planetary state calculations"""
    
    def test_combustion_implementation(self):
        """Test the combustion calculation implementation directly"""
        # Create a calculator with any date
        calculator = VedicCalculator(
            date=datetime(2023, 1, 1, 12, 0),
            lat=28.6139,  # New Delhi
            lon=77.2090
        )
        
        # Force Sun and Mercury to be close to each other
        calculator.planets['Sun']['longitude'] = 100.0
        calculator.planets['Mercury']['longitude'] = 105.0  # 5 degrees from Sun, should be combust
        
        # Recalculate combustion
        calculator._calculate_combustion()
        
        # Verify Mercury is combust (should be within 14 degrees)
        self.assertTrue(calculator.planets['Mercury']['state']['combustion'])
        self.assertTrue('combustion_degree' in calculator.planets['Mercury']['state'])
        self.assertAlmostEqual(calculator.planets['Mercury']['state']['combustion_degree'], 5.0)
        
        # Move Mercury further away
        calculator.planets['Mercury']['longitude'] = 115.0  # 15 degrees from Sun, should not be combust
        
        # Recalculate combustion
        calculator._calculate_combustion()
        
        # Verify Mercury is not combust
        self.assertFalse(calculator.planets['Mercury']['state']['combustion'])
        
        # Verify nodes are never combust
        self.assertFalse(calculator.planets['Rahu']['state']['combustion'])
        self.assertFalse(calculator.planets['Ketu']['state']['combustion'])
    
    def test_retrograde_implementation(self):
        """Test the retrograde detection implementation"""
        # Create a calculator with any date
        calculator = VedicCalculator(
            date=datetime(2023, 1, 1, 12, 0),
            lat=28.6139,  # New Delhi
            lon=77.2090
        )
        
        # Force Jupiter to be retrograde
        calculator.planets['Jupiter']['isRetrograde'] = True
        calculator.planets['Jupiter']['state']['retrograde'] = True
        
        # Verify Jupiter is retrograde
        self.assertTrue(calculator.planets['Jupiter']['isRetrograde'])
        self.assertTrue(calculator.planets['Jupiter']['state']['retrograde'])
        
        # Force Saturn to not be retrograde
        calculator.planets['Saturn']['isRetrograde'] = False
        calculator.planets['Saturn']['state']['retrograde'] = False
        
        # Verify Saturn is not retrograde
        self.assertFalse(calculator.planets['Saturn']['isRetrograde'])
        self.assertFalse(calculator.planets['Saturn']['state']['retrograde'])
        
        # Verify Sun and Moon are never retrograde
        self.assertFalse(calculator.planets['Sun']['isRetrograde'])
        self.assertFalse(calculator.planets['Sun']['state']['retrograde'])
        self.assertFalse(calculator.planets['Moon']['isRetrograde'])
        self.assertFalse(calculator.planets['Moon']['state']['retrograde'])
    
    def test_planetary_war_implementation(self):
        """Test the planetary war detection implementation directly"""
        # Create a calculator with any date
        calculator = VedicCalculator(
            date=datetime(2023, 1, 1, 12, 0),
            lat=28.6139,  # New Delhi
            lon=77.2090
        )
        
        # Force Venus and Mars to be close to each other
        calculator.planets['Venus']['longitude'] = 120.0
        calculator.planets['Mars']['longitude'] = 120.8  # 0.8 degrees from Venus, should be at war
        
        # Set dignities to determine winner
        calculator.planets['Venus']['dignity'] = 'exalted'
        calculator.planets['Mars']['dignity'] = 'debilitated'
        
        # Recalculate planetary war
        calculator._calculate_planetary_war()
        
        # Verify Venus and Mars are at war
        self.assertTrue(calculator.planets['Venus']['state']['war'])
        self.assertTrue(calculator.planets['Mars']['state']['war'])
        
        # Verify war details
        self.assertEqual(calculator.planets['Venus']['state']['war_with'], 'Mars')
        self.assertEqual(calculator.planets['Mars']['state']['war_with'], 'Venus')
        
        # Venus should win due to higher dignity
        self.assertTrue(calculator.planets['Venus']['state']['war_winner'])
        self.assertFalse(calculator.planets['Mars']['state']['war_winner'])
        
        # Move Mars further away
        calculator.planets['Mars']['longitude'] = 122.0  # 2 degrees from Venus, should not be at war
        
        # Recalculate planetary war
        calculator._calculate_planetary_war()
        
        # Verify Venus and Mars are not at war
        self.assertFalse(calculator.planets['Venus']['state']['war'])
        self.assertFalse(calculator.planets['Mars']['state']['war'])


if __name__ == '__main__':
    unittest.main()
