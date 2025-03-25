import unittest
from datetime import datetime
import pytz
from vedic_calculator.core import VedicCalculator

class TestPlanetaryAspects(unittest.TestCase):
    """Test cases for planetary aspects calculations"""
    
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
    
    def test_house_aspects(self):
        """Test that all planets have house aspects assigned correctly"""
        planets = self.calculator.planets
        
        # Verify all planets have aspects
        for planet_name, planet_data in planets.items():
            self.assertIn('aspects', planet_data)
            self.assertIn('houses', planet_data['aspects'])
            
            # All planets should aspect at least the 7th house from their position
            house = planet_data['house']
            seventh_house = (house + 6) % 12
            if seventh_house == 0:
                seventh_house = 12
            
            self.assertIn(seventh_house, planet_data['aspects']['houses'])
            
            # Print house and aspected houses for debugging
            print(f"{planet_name} in house {house} aspects houses: {planet_data['aspects']['houses']}")
            
            # Test special aspects for specific planets
            if planet_name == 'Mars':
                # Mars should aspect 4th and 8th houses from its position
                fourth_house = (house + 3) % 12
                if fourth_house == 0:
                    fourth_house = 12
                eighth_house = (house + 7) % 12
                if eighth_house == 0:
                    eighth_house = 12
                
                self.assertIn(fourth_house, planet_data['aspects']['houses'])
                self.assertIn(eighth_house, planet_data['aspects']['houses'])
            
            elif planet_name == 'Jupiter':
                # Jupiter should aspect 5th and 9th houses from its position
                fifth_house = (house + 4) % 12
                if fifth_house == 0:
                    fifth_house = 12
                ninth_house = (house + 8) % 12
                if ninth_house == 0:
                    ninth_house = 12
                
                self.assertIn(fifth_house, planet_data['aspects']['houses'])
                self.assertIn(ninth_house, planet_data['aspects']['houses'])
            
            elif planet_name in ['Saturn', 'Rahu', 'Ketu']:
                # Saturn, Rahu, and Ketu should aspect 3rd and 10th houses from their position
                third_house = (house + 2) % 12
                if third_house == 0:
                    third_house = 12
                tenth_house = (house + 9) % 12
                if tenth_house == 0:
                    tenth_house = 12
                
                self.assertIn(third_house, planet_data['aspects']['houses'])
                self.assertIn(tenth_house, planet_data['aspects']['houses'])
    
    def test_planet_aspects(self):
        """Test that planet-to-planet aspects are calculated correctly"""
        planets = self.calculator.planets
        
        # Verify all planets have planet aspects
        for planet_name, planet_data in planets.items():
            self.assertIn('aspects', planet_data)
            self.assertIn('planets', planet_data['aspects'])
            self.assertIn('is_aspected_by', planet_data['aspects'])
            
            # Print planets being aspected for debugging
            print(f"{planet_name} aspects planets: {list(planet_data['aspects']['planets'].keys())}")
            print(f"{planet_name} is aspected by: {list(planet_data['aspects']['is_aspected_by'].keys())}")
            
            # For each planet that planet1 aspects, verify the reciprocal relationship
            for aspected_planet, aspect_data in planet_data['aspects']['planets'].items():
                self.assertIn(planet_name, planets[aspected_planet]['aspects']['is_aspected_by'])
                
                # Verify aspect strength and type match
                self.assertEqual(
                    aspect_data['strength'],
                    planets[aspected_planet]['aspects']['is_aspected_by'][planet_name]['strength']
                )
                self.assertEqual(
                    aspect_data['type'],
                    planets[aspected_planet]['aspects']['is_aspected_by'][planet_name]['type']
                )
    
    def test_aspect_strengths(self):
        """Test that aspect strengths are calculated correctly"""
        planets = self.calculator.planets
        
        # Verify all planets have aspect strengths
        for planet_name, planet_data in planets.items():
            self.assertIn('aspects', planet_data)
            self.assertIn('outgoing_strength', planet_data['aspects'])
            self.assertIn('incoming_strength', planet_data['aspects'])
            
            # Print aspect strengths for debugging
            print(f"{planet_name} outgoing aspect strength: {planet_data['aspects']['outgoing_strength']}")
            print(f"{planet_name} incoming aspect strength: {planet_data['aspects']['incoming_strength']}")
            
            # Verify outgoing strength equals sum of individual aspect strengths
            calculated_outgoing = sum(
                aspect_data['strength'] 
                for aspect_data in planet_data['aspects']['planets'].values()
            )
            self.assertEqual(calculated_outgoing, planet_data['aspects']['outgoing_strength'])
            
            # Verify incoming strength equals sum of individual aspect strengths
            calculated_incoming = sum(
                aspect_data['strength'] 
                for aspect_data in planet_data['aspects']['is_aspected_by'].values()
            )
            self.assertEqual(calculated_incoming, planet_data['aspects']['incoming_strength'])
    
    def test_aspect_types(self):
        """Test that aspect types are assigned correctly"""
        planets = self.calculator.planets
        
        # Check a few specific aspect types
        for planet_name, planet_data in planets.items():
            for aspected_planet, aspect_data in planet_data['aspects']['planets'].items():
                # Get houses
                planet1_house = planet_data['house']
                planet2_house = planets[aspected_planet]['house']
                
                # Calculate house distance
                house_distance = (planet2_house - planet1_house) % 12
                if house_distance == 0:
                    house_distance = 12
                
                # Verify aspect type matches house distance
                expected_type = f"house_{house_distance}"
                self.assertEqual(expected_type, aspect_data['type'])
                
                # Verify aspect strength based on type
                if house_distance == 7:  # 7th house aspect (all planets)
                    self.assertEqual(100, aspect_data['strength'])
                elif house_distance in [3, 10] and planet_name in ['Saturn', 'Rahu', 'Ketu']:
                    self.assertEqual(75, aspect_data['strength'])
                elif house_distance in [4, 8] and planet_name == 'Mars':
                    self.assertEqual(85, aspect_data['strength'])
                elif house_distance in [5, 9] and planet_name == 'Jupiter':
                    self.assertEqual(90, aspect_data['strength'])

if __name__ == '__main__':
    unittest.main()
