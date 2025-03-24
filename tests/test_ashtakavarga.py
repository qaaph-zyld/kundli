"""
Test module for Ashtakavarga calculations
"""
import unittest
from datetime import datetime
from vedic_calculator.core import VedicCalculator
from vedic_calculator.ashtakavarga import AshtakavargaCalculator

class TestAshtakavarga(unittest.TestCase):
    """Test cases for Ashtakavarga calculations"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a test birth chart
        self.birth_datetime = datetime(1990, 1, 1, 12, 0, 0)
        self.lat = 28.6139  # Delhi latitude
        self.lon = 77.2090  # Delhi longitude
        
        # Initialize calculator
        self.calculator = VedicCalculator(self.birth_datetime, self.lat, self.lon)
    
    def test_ashtakavarga_initialization(self):
        """Test that Ashtakavarga is properly initialized"""
        # Ensure Ashtakavarga data is calculated
        self.calculator._calculate_ashtakavarga()
        
        # Check that Ashtakavarga data exists
        self.assertIsNotNone(self.calculator.ashtakavarga)
        self.assertIn('prastarashtakavarga', self.calculator.ashtakavarga)
        self.assertIn('sarvashtakavarga', self.calculator.ashtakavarga)
    
    def test_prastarashtakavarga(self):
        """Test individual planet Ashtakavarga calculations"""
        # Get Prastarashtakavarga for Sun
        sun_ashtakavarga = self.calculator.get_prastarashtakavarga('Sun')
        
        # Check structure
        self.assertIsInstance(sun_ashtakavarga, dict)
        
        # Check that all 12 houses have bindu values
        for house in range(1, 13):
            self.assertIn(house, sun_ashtakavarga)
            self.assertIsInstance(sun_ashtakavarga[house], int)
            # Bindu values should be between 0 and 8 (8 contributors max)
            self.assertGreaterEqual(sun_ashtakavarga[house], 0)
            self.assertLessEqual(sun_ashtakavarga[house], 8)
    
    def test_sarvashtakavarga(self):
        """Test combined Ashtakavarga calculations"""
        # Get Sarvashtakavarga
        sarvashtakavarga = self.calculator.get_sarvashtakavarga()
        
        # Check structure
        self.assertIsInstance(sarvashtakavarga, dict)
        
        # Check that all 12 houses have bindu values
        for house in range(1, 13):
            self.assertIn(house, sarvashtakavarga)
            self.assertIsInstance(sarvashtakavarga[house], int)
            # Sarvashtakavarga values should be between 0 and 56 (7 planets * 8 contributors max)
            self.assertGreaterEqual(sarvashtakavarga[house], 0)
            self.assertLessEqual(sarvashtakavarga[house], 56)
    
    def test_planet_bindu_total(self):
        """Test planet bindu total calculations"""
        # Get bindu total for Jupiter
        jupiter_total = self.calculator.get_planet_bindu_total('Jupiter')
        
        # Check that it's a valid number
        self.assertIsInstance(jupiter_total, int)
        # Total should be between 0 and 96 (8 max per house * 12 houses)
        self.assertGreaterEqual(jupiter_total, 0)
        self.assertLessEqual(jupiter_total, 96)
    
    def test_house_bindu_total(self):
        """Test house bindu total calculations"""
        # Get bindu total for 1st house
        house_total = self.calculator.get_house_bindu_total(1)
        
        # Check that it's a valid number
        self.assertIsInstance(house_total, int)
        # Total should be between 0 and 56 (7 planets * 8 contributors max)
        self.assertGreaterEqual(house_total, 0)
        self.assertLessEqual(house_total, 56)
    
    def test_ashtakavarga_strength(self):
        """Test Ashtakavarga strength assessment"""
        # Get strength assessment
        strength = self.calculator.get_ashtakavarga_strength()
        
        # Check structure
        self.assertIsInstance(strength, dict)
        self.assertIn('planet_strengths', strength)
        self.assertIn('house_strengths', strength)
        
        # Check planet strengths
        for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
            self.assertIn(planet, strength['planet_strengths'])
            planet_data = strength['planet_strengths'][planet]
            self.assertIn('total_bindus', planet_data)
            self.assertIn('strength', planet_data)
            self.assertIn(planet_data['strength'], ['strong', 'medium', 'weak'])
        
        # Check house strengths
        for house in range(1, 13):
            self.assertIn(house, strength['house_strengths'])
            house_data = strength['house_strengths'][house]
            self.assertIn('total_bindus', house_data)
            self.assertIn('strength', house_data)
            self.assertIn(house_data['strength'], ['strong', 'medium', 'weak'])

if __name__ == '__main__':
    unittest.main()
