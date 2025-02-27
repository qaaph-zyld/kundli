"""
Tests for core Vedic astrology calculations
"""
import unittest
from datetime import datetime
import pytz
from ..core import VedicCalculator

class TestVedicCalculator(unittest.TestCase):
    def setUp(self):
        # Test data: January 1, 2000, 12:00 UTC
        # Location: Greenwich Observatory (51.4769° N, 0.0005° W)
        self.test_date = datetime(2000, 1, 1, 12, 0, tzinfo=pytz.UTC)
        self.test_lat = 51.4769
        self.test_lon = -0.0005
        self.calc = VedicCalculator(self.test_date, self.test_lat, self.test_lon)

    def test_ayanamsa_calculation(self):
        """Test Lahiri ayanamsa calculation"""
        # Expected value for Jan 1, 2000 (approximately)
        expected_ayanamsa = 23.85
        calculated = self.calc._calculate_lahiri_ayanamsa()
        self.assertAlmostEqual(calculated, expected_ayanamsa, places=1)

    def test_sun_position(self):
        """Test Sun position calculation"""
        longitude, sign = self.calc.get_planet_position('Sun')
        
        # Sun should be in Sagittarius around Jan 1 (sidereal)
        self.assertEqual(sign, 'Sagittarius')
        # Longitude should be between 240° and 270° (Sagittarius)
        self.assertTrue(240 <= longitude <= 270)

    def test_moon_position(self):
        """Test Moon position calculation"""
        longitude, sign = self.calc.get_planet_position('Moon')
        
        # Verify longitude is in valid range
        self.assertTrue(0 <= longitude <= 360)
        # Verify sign is in zodiac list
        self.assertIn(sign, VedicCalculator.ZODIAC_SIGNS)

    def test_house_cusps(self):
        """Test house cusp calculations"""
        cusps = self.calc.get_house_cusps()
        
        # Should have 12 houses
        self.assertEqual(len(cusps), 12)
        
        # All cusps should be 30° apart in equal house system
        for i in range(11):
            diff = (cusps[i+1] - cusps[i]) % 360
            self.assertAlmostEqual(diff, 30.0, places=1)

    def test_planet_dignity(self):
        """Test planet dignity calculations"""
        # Test Sun's dignity
        sun_dignity = self.calc.get_planet_dignity('Sun')
        self.assertIn(sun_dignity, ['exalted', 'debilitated', 'neutral'])

        # Test Moon's dignity
        moon_dignity = self.calc.get_planet_dignity('Moon')
        self.assertIn(moon_dignity, ['exalted', 'debilitated', 'neutral'])

    def test_all_planets_calculation(self):
        """Test calculation of all planets"""
        result = self.calc.calculate_all_planets()
        
        # Check all major planets are included
        expected_planets = {'Sun', 'Moon', 'Mars', 'Jupiter', 'Venus', 'Saturn'}
        self.assertEqual(set(result.keys()), expected_planets)
        
        # Check structure of each planet's data
        for planet_data in result.values():
            self.assertIn('longitude', planet_data)
            self.assertIn('sign', planet_data)
            self.assertIn('dignity', planet_data)
            self.assertIn('degree', planet_data)

if __name__ == '__main__':
    unittest.main()
