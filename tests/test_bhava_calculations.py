import unittest
from datetime import datetime
import pytz
from vedic_calculator.core import VedicCalculator

class TestBhavaCalculations(unittest.TestCase):
    """Test cases for bhava-oriented calculations with precise bhava madhya points"""
    
    def setUp(self):
        """Set up test case with a sample birth chart"""
        # Sample birth data - May 15, 1984, 10:30 AM, New Delhi
        birth_datetime = datetime(1984, 5, 15, 10, 30, 0)
        birth_timezone = pytz.timezone('Asia/Kolkata')
        birth_datetime = birth_timezone.localize(birth_datetime)
        
        # New Delhi coordinates
        lat = 28.6139
        lon = 77.2090
        
        # Create calculator instance
        self.calculator = VedicCalculator(birth_datetime, lat, lon)
        
        # Force calculation of the chart
        self.calculator.calculate_all()
    
    def test_bhava_madhya_points(self):
        """Test that bhava madhya points are calculated correctly"""
        # Check that each house has bhava madhya information
        for house_num, house_data in self.calculator.houses.items():
            # Verify bhava madhya data exists
            self.assertIn('bhava_madhya', house_data)
            self.assertIn('bhava_madhya_formatted', house_data)
            self.assertIn('bhava_madhya_sign', house_data)
            self.assertIn('bhava_madhya_in_sign', house_data)
            self.assertIn('bhava_madhya_in_sign_formatted', house_data)
            
            # Verify bhava madhya is a valid longitude
            bhava_madhya = house_data['bhava_madhya']
            self.assertGreaterEqual(bhava_madhya, 0)
            self.assertLess(bhava_madhya, 360)
            
            # Print bhava madhya details for debugging
            print(f"House {house_num} ({house_data['sign']}) bhava madhya: {house_data['bhava_madhya_formatted']} in {house_data['bhava_madhya_sign']}")
    
    def test_house_cusps(self):
        """Test that house cusps are calculated correctly"""
        # Check that each house has cusp information
        for house_num, house_data in self.calculator.houses.items():
            # Verify cusp data exists
            self.assertIn('cusp', house_data)
            self.assertIn('cusp_formatted', house_data)
            
            # Verify cusp is a valid longitude
            cusp = house_data['cusp']
            self.assertGreaterEqual(cusp, 0)
            self.assertLess(cusp, 360)
            
            # Print cusp details for debugging
            print(f"House {house_num} cusp: {house_data['cusp_formatted']}")
    
    def test_bhava_bala(self):
        """Test that bhava bala (house strength) is calculated correctly"""
        # Check bhava bala for each house
        for house_num, bala in self.calculator.bhava_bala.items():
            # Verify house number is valid
            self.assertGreaterEqual(house_num, 1)
            self.assertLessEqual(house_num, 12)
            
            # Verify bhava bala is a dictionary with the expected structure
            self.assertIsInstance(bala, dict)
            self.assertIn('total', bala)
            self.assertIsInstance(bala['total'], (int, float))
            
            # Verify components are present
            self.assertIn('components', bala)
            self.assertIsInstance(bala['components'], dict)
            
            # Check that all expected components are present
            expected_components = [
                'occupant_strength', 
                'lord_placement_strength', 
                'lord_dignity_strength', 
                'aspect_strength', 
                'bhava_madhya_strength'
            ]
            for component in expected_components:
                self.assertIn(component, bala['components'])
                self.assertIsInstance(bala['components'][component], (int, float))
            
            # Print bhava bala for debugging
            print(f"House {house_num} bhava bala: {bala['total']} (components: {bala['components']})")
    
    def test_planets_relative_to_bhava_madhya(self):
        """Test planet positions relative to bhava madhya points"""
        # For each planet, check its position relative to the bhava madhya of its house
        for planet_name, planet_data in self.calculator.planets.items():
            house_num = planet_data['house']
            
            # Skip if house data is not available
            if house_num not in self.calculator.houses:
                continue
                
            house_data = self.calculator.houses[house_num]
            
            # Calculate distance from planet to bhava madhya
            planet_longitude = planet_data['longitude']
            bhava_madhya = house_data['bhava_madhya']
            
            # Calculate the shorter arc distance
            distance = min(
                (planet_longitude - bhava_madhya) % 360,
                (bhava_madhya - planet_longitude) % 360
            )
            
            # Print planet position relative to bhava madhya
            print(f"Planet {planet_name} in house {house_num} is {distance:.2f}° from bhava madhya")
            
            # Verify distance is within reasonable range (should be less than 30°)
            self.assertLessEqual(distance, 30)

if __name__ == '__main__':
    unittest.main()
