import unittest
from datetime import datetime
import pytz
from vedic_calculator.core import VedicCalculator

class TestHouseLords(unittest.TestCase):
    """Test cases for house lord relationships and functional nature calculations"""
    
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
    
    def test_house_lords(self):
        """Test that house lords are assigned correctly"""
        # Check that each house has a lord
        for house_num, house_data in self.calculator.houses.items():
            self.assertIn('lord', house_data)
            lord = house_data['lord']
            self.assertIsNotNone(lord)
            
            # Verify the lord is a valid planet
            self.assertIn(lord, self.calculator.planets.keys())
            
            # Print house and lord for debugging
            print(f"House {house_num} ({house_data['sign']}) has lord {lord}")
    
    def test_house_lord_placements(self):
        """Test that house lord placements are calculated correctly"""
        # Check that house_lords dictionary is populated
        self.assertIsNotNone(self.calculator.house_lords)
        
        # Check each house lord's placement
        for house_num, lord_data in self.calculator.house_lords.items():
            self.assertIn('lord', lord_data)
            self.assertIn('placement_house', lord_data)
            
            lord = lord_data['lord']
            placement_house = lord_data['placement_house']
            
            # Verify the placement matches the planet's house
            self.assertEqual(placement_house, self.calculator.planets[lord]['house'])
            
            # Print house lord placement for debugging
            print(f"Lord of house {house_num} ({lord}) is placed in house {placement_house}")
    
    def test_house_relationships(self):
        """Test that house relationships are calculated correctly"""
        # Check that house_relationships dictionary is populated
        self.assertIsNotNone(self.calculator.house_relationships)
        
        # Check relationships for each house
        for house1, relationships in self.calculator.house_relationships.items():
            # Print relationships for debugging
            print(f"House {house1} has relationships with: {list(relationships.keys())}")
            
            # Check each relationship
            for house2, relationship_data in relationships.items():
                self.assertIn('type', relationship_data)
                self.assertIn('description', relationship_data)
                
                # Verify relationship type is valid
                self.assertIn(relationship_data['type'], 
                             ['lord_placement', 'mutual_lordship', 'parivartana', 'lord_aspects'])
                
                # Print relationship details for debugging
                print(f"  - {relationship_data['description']}")
    
    def test_functional_nature(self):
        """Test that functional nature of planets is calculated correctly"""
        # Check that functional_nature dictionary is populated
        self.assertIsNotNone(self.calculator.functional_nature)
        
        # Check functional nature for each planet
        for planet_name, nature in self.calculator.functional_nature.items():
            # Verify the planet is valid
            self.assertIn(planet_name, self.calculator.planets.keys())
            
            # Verify nature is one of the valid types
            self.assertIn(nature, [
                'yogakaraka', 'strong_benefic', 'benefic', 'neutral', 
                'malefic', 'strong_malefic', 'functional_benefic', 
                'functional_malefic', 'natural_benefic', 'natural_malefic'
            ])
            
            # Print functional nature for debugging
            print(f"Planet {planet_name} has functional nature: {nature}")
            
            # For yogakaraka planets, verify they rule both a trine and an angle
            if nature == 'yogakaraka':
                ruled_houses = []
                for house_num, house_data in self.calculator.houses.items():
                    if house_data['lord'] == planet_name:
                        ruled_houses.append(house_num)
                
                # Check if planet rules both a trine and an angle
                rules_trine = any(h in [1, 5, 9] for h in ruled_houses)
                rules_angle = any(h in [1, 4, 7, 10] for h in ruled_houses)
                
                self.assertTrue(rules_trine)
                self.assertTrue(rules_angle)

if __name__ == '__main__':
    unittest.main()
