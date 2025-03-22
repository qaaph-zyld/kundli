"""
Test suite for planetary relationship calculations
"""

import sys
import os
import unittest
from datetime import datetime

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vedic_calculator.core import VedicCalculator


class TestPlanetaryRelationships(unittest.TestCase):
    """Test cases for planetary relationship calculations"""
    
    def test_natural_relationships(self):
        """Test natural relationship calculations"""
        # Create a calculator with any date
        calculator = VedicCalculator(
            date=datetime(2023, 1, 1, 12, 0),
            lat=28.6139,  # New Delhi
            lon=77.2090
        )
        
        # Test Sun's natural relationships
        self.assertEqual(calculator.planets['Sun']['relationships']['Moon']['natural'], 'friend')
        self.assertEqual(calculator.planets['Sun']['relationships']['Mars']['natural'], 'friend')
        self.assertEqual(calculator.planets['Sun']['relationships']['Jupiter']['natural'], 'friend')
        self.assertEqual(calculator.planets['Sun']['relationships']['Venus']['natural'], 'enemy')
        self.assertEqual(calculator.planets['Sun']['relationships']['Saturn']['natural'], 'enemy')
        self.assertEqual(calculator.planets['Sun']['relationships']['Mercury']['natural'], 'neutral')
        
        # Test Jupiter's natural relationships
        self.assertEqual(calculator.planets['Jupiter']['relationships']['Sun']['natural'], 'friend')
        self.assertEqual(calculator.planets['Jupiter']['relationships']['Moon']['natural'], 'friend')
        self.assertEqual(calculator.planets['Jupiter']['relationships']['Mars']['natural'], 'friend')
        self.assertEqual(calculator.planets['Jupiter']['relationships']['Mercury']['natural'], 'enemy')
        self.assertEqual(calculator.planets['Jupiter']['relationships']['Venus']['natural'], 'enemy')
        self.assertEqual(calculator.planets['Jupiter']['relationships']['Saturn']['natural'], 'neutral')
        
        # Test Rahu's natural relationships
        self.assertEqual(calculator.planets['Rahu']['relationships']['Venus']['natural'], 'friend')
        self.assertEqual(calculator.planets['Rahu']['relationships']['Saturn']['natural'], 'friend')
        self.assertEqual(calculator.planets['Rahu']['relationships']['Sun']['natural'], 'enemy')
        self.assertEqual(calculator.planets['Rahu']['relationships']['Moon']['natural'], 'enemy')
    
    def setUp_temporary_relationships(self, calculator):
        """Set up planets in specific houses for temporary relationship testing"""
        # Sun in house 1
        calculator.planets['Sun']['house'] = 1
        
        # Moon in house 4 (3 houses away from Sun = friend)
        calculator.planets['Moon']['house'] = 4
        
        # Mars in house 6 (5 houses away from Sun = enemy)
        calculator.planets['Mars']['house'] = 6
        
        # Jupiter in house 3 (2 houses away from Sun = neutral)
        calculator.planets['Jupiter']['house'] = 3
        
        # Venus in house 12 (11 houses away from Sun = friend)
        calculator.planets['Venus']['house'] = 12
        
        # Saturn in house 1 (0 houses away from Sun = enemy, same house)
        calculator.planets['Saturn']['house'] = 1
        
        # Recalculate relationships
        calculator._calculate_planetary_relationships()
    
    def test_temporary_relationships(self):
        """Test temporary relationship calculations based on house positions"""
        # Create a calculator with any date
        calculator = VedicCalculator(
            date=datetime(2023, 1, 1, 12, 0),
            lat=28.6139,  # New Delhi
            lon=77.2090
        )
        
        # Set up test scenario
        self.setUp_temporary_relationships(calculator)
        
        # Print house distances for debugging
        print("\nHouse distances from Sun:")
        for planet in ['Moon', 'Mars', 'Jupiter', 'Venus', 'Saturn']:
            house1 = calculator.planets['Sun']['house']
            house2 = calculator.planets[planet]['house']
            house_distance = (house2 - house1) % 12
            print(f"Sun to {planet}: {house_distance} houses away")
        
        # Test Sun's temporary relationships
        self.assertEqual(calculator.planets['Sun']['relationships']['Moon']['temporary'], 'friend')
        self.assertEqual(calculator.planets['Sun']['relationships']['Mars']['temporary'], 'enemy')
        self.assertEqual(calculator.planets['Sun']['relationships']['Jupiter']['temporary'], 'neutral')
        self.assertEqual(calculator.planets['Sun']['relationships']['Venus']['temporary'], 'friend')
        self.assertEqual(calculator.planets['Sun']['relationships']['Saturn']['temporary'], 'enemy')
        
        # Test Moon's temporary relationships with other planets
        # Moon is in house 4, so:
        # Sun is in house 1: (1-4)%12 = 9 houses away = enemy
        # Mars is in house 6: (6-4)%12 = 2 houses away = neutral
        # Jupiter is in house 3: (3-4)%12 = 11 houses away = friend
        # Venus is in house 12: (12-4)%12 = 8 houses away = enemy
        # Saturn is in house 1: (1-4)%12 = 9 houses away = enemy
        self.assertEqual(calculator.planets['Moon']['relationships']['Sun']['temporary'], 'enemy')
        self.assertEqual(calculator.planets['Moon']['relationships']['Mars']['temporary'], 'neutral')
        self.assertEqual(calculator.planets['Moon']['relationships']['Jupiter']['temporary'], 'friend')
        self.assertEqual(calculator.planets['Moon']['relationships']['Venus']['temporary'], 'enemy')
        self.assertEqual(calculator.planets['Moon']['relationships']['Saturn']['temporary'], 'enemy')
    
    def test_composite_relationships(self):
        """Test composite relationship calculations"""
        # Create a calculator with any date
        calculator = VedicCalculator(
            date=datetime(2023, 1, 1, 12, 0),
            lat=28.6139,  # New Delhi
            lon=77.2090
        )
        
        # Force planets into specific houses and set up test scenarios
        
        # Scenario 1: Natural = friend, Temporary = friend -> Composite = friend
        calculator.planets['Sun']['house'] = 1
        calculator.planets['Mars']['house'] = 4  # 3 houses away = friend
        
        # Scenario 2: Natural = enemy, Temporary = enemy -> Composite = enemy
        calculator.planets['Sun']['house'] = 1
        calculator.planets['Venus']['house'] = 6  # 5 houses away = enemy
        
        # Scenario 3: Natural = friend, Temporary = enemy -> Composite = neutral
        calculator.planets['Sun']['house'] = 1
        calculator.planets['Jupiter']['house'] = 6  # 5 houses away = enemy
        
        # Scenario 4: Natural = enemy, Temporary = friend -> Composite = neutral
        calculator.planets['Sun']['house'] = 1
        calculator.planets['Saturn']['house'] = 4  # 3 houses away = friend
        
        # Scenario 5: Natural = neutral, Temporary = friend -> Composite = friend
        calculator.planets['Sun']['house'] = 1
        calculator.planets['Mercury']['house'] = 4  # 3 houses away = friend
        
        # Recalculate relationships
        calculator._calculate_planetary_relationships()
        
        # Test composite relationships
        # Sun-Mars: Natural friend + Temporary friend = Composite friend
        self.assertEqual(calculator.planets['Sun']['relationships']['Mars']['natural'], 'friend')
        self.assertEqual(calculator.planets['Sun']['relationships']['Mars']['temporary'], 'friend')
        self.assertEqual(calculator.planets['Sun']['relationships']['Mars']['composite'], 'friend')
        
        # Sun-Venus: Natural enemy + Temporary enemy = Composite enemy
        self.assertEqual(calculator.planets['Sun']['relationships']['Venus']['natural'], 'enemy')
        self.assertEqual(calculator.planets['Sun']['relationships']['Venus']['temporary'], 'enemy')
        self.assertEqual(calculator.planets['Sun']['relationships']['Venus']['composite'], 'enemy')
        
        # Sun-Jupiter: Natural friend + Temporary enemy = Composite neutral
        self.assertEqual(calculator.planets['Sun']['relationships']['Jupiter']['natural'], 'friend')
        self.assertEqual(calculator.planets['Sun']['relationships']['Jupiter']['temporary'], 'enemy')
        self.assertEqual(calculator.planets['Sun']['relationships']['Jupiter']['composite'], 'neutral')
        
        # Sun-Saturn: Natural enemy + Temporary friend = Composite neutral
        self.assertEqual(calculator.planets['Sun']['relationships']['Saturn']['natural'], 'enemy')
        self.assertEqual(calculator.planets['Sun']['relationships']['Saturn']['temporary'], 'friend')
        self.assertEqual(calculator.planets['Sun']['relationships']['Saturn']['composite'], 'neutral')
        
        # Sun-Mercury: Natural neutral + Temporary friend = Composite friend
        self.assertEqual(calculator.planets['Sun']['relationships']['Mercury']['natural'], 'neutral')
        self.assertEqual(calculator.planets['Sun']['relationships']['Mercury']['temporary'], 'friend')
        self.assertEqual(calculator.planets['Sun']['relationships']['Mercury']['composite'], 'friend')


if __name__ == '__main__':
    unittest.main()
