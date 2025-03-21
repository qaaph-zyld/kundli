"""
Test suite for planetary position calculations
"""

import sys
import os
import unittest
import json
from datetime import datetime

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vedic_calculator.core import VedicCalculator


class TestPlanetaryPositions(unittest.TestCase):
    """Test cases for planetary position calculations"""
    
    def setUp(self):
        """Set up test environment"""
        # Load the reference chart data
        with open('data/nikola_reference_chart.json', 'r') as f:
            self.reference_data = json.load(f)
        
        # Create a calculator instance for Nikola's birth data
        self.calculator = VedicCalculator(
            date=datetime.strptime(f"{self.reference_data['date']} {self.reference_data['time']}", "%Y-%m-%d %H:%M:%S"),
            lat=self.reference_data['latitude'],
            lon=self.reference_data['longitude']
        )
        
        # The constructor already calls calculate_all() so we don't need to call it again
    
    def test_ascendant(self):
        """Test the ascendant calculation"""
        # Get the calculated ascendant
        calculated_asc = self.calculator.ascendant
        
        # Get the reference ascendant
        reference_asc = self.reference_data['ascendant']
        
        # Compare the values
        self.assertEqual(calculated_asc['sign'], reference_asc['sign'])
        self.assertAlmostEqual(calculated_asc['degree'], reference_asc['degree'], places=1)
        self.assertEqual(calculated_asc['longitude'], reference_asc['longitude'])
    
    def test_sun_position(self):
        """Test the Sun position calculation"""
        # Get the calculated Sun position
        calculated_sun = self.calculator.planets['Sun']
        
        # Get the reference Sun position
        reference_sun = self.reference_data['planets']['Sun']
        
        # Compare the values
        self.assertEqual(calculated_sun['sign'], reference_sun['sign'])
        self.assertAlmostEqual(calculated_sun['degree'], reference_sun['degree'], places=1)
        self.assertAlmostEqual(calculated_sun['longitude'], reference_sun['longitude'], places=1)
    
    def test_moon_position(self):
        """Test the Moon position calculation"""
        # Get the calculated Moon position
        calculated_moon = self.calculator.planets['Moon']
        
        # Get the reference Moon position
        reference_moon = self.reference_data['planets']['Moon']
        
        # Compare the values
        self.assertEqual(calculated_moon['sign'], reference_moon['sign'])
        self.assertAlmostEqual(calculated_moon['degree'], reference_moon['degree'], places=1)
        self.assertAlmostEqual(calculated_moon['longitude'], reference_moon['longitude'], places=1)
    
    def test_all_planets(self):
        """Test all planetary positions"""
        # List of planets to test
        planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
        
        for planet in planets:
            # Get the calculated position
            calculated = self.calculator.planets[planet]
            
            # Get the reference position
            reference = self.reference_data['planets'][planet]
            
            # Compare the values
            self.assertEqual(calculated['sign'], reference['sign'], f"Sign mismatch for {planet}")
            self.assertAlmostEqual(calculated['degree'], reference['degree'], places=1, msg=f"Degree mismatch for {planet}")
            self.assertAlmostEqual(calculated['longitude'], reference['longitude'], places=1, msg=f"Longitude mismatch for {planet}")
    
    def test_houses(self):
        """Test house cusps"""
        # List of houses to test
        houses = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6']
        
        for house in houses:
            # Get the calculated house
            calculated = self.calculator.houses[house]
            
            # Get the reference house
            reference = self.reference_data['houses'][house]
            
            # Compare the values
            self.assertEqual(calculated['sign'], reference['sign'], f"Sign mismatch for {house}")
            self.assertAlmostEqual(calculated['degree'], reference['degree'], places=1, msg=f"Degree mismatch for {house}")
            self.assertAlmostEqual(calculated['longitude'], reference['longitude'], places=1, msg=f"Longitude mismatch for {house}")


if __name__ == '__main__':
    unittest.main()
