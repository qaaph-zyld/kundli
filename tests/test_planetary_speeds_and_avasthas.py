import unittest
from datetime import datetime
import pytz
from vedic_calculator.core import VedicCalculator

class TestPlanetarySpeedsAndAvasthas(unittest.TestCase):
    """Test cases for planetary speeds and avasthas calculations"""
    
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
    
    def test_planetary_speed_categories(self):
        """Test that all planets have speed categories assigned"""
        planets = self.calculator.planets
        
        # Verify all planets have speed categories
        for planet_name, planet_data in planets.items():
            self.assertIn('speed_category', planet_data['state'])
            
            # Verify the speed category is one of the expected values
            valid_categories = ['ati_sheeghra', 'sheeghra', 'madhya', 
                               'manda', 'ati_manda', 'vakra', 'medium']
            self.assertIn(planet_data['state']['speed_category'], valid_categories)
            
            # Print speed and category for debugging
            print(f"{planet_name}: Speed = {planet_data['speed']:.4f}, "
                  f"Category = {planet_data['state']['speed_category']}")
            
            # Test specific cases based on retrograde status
            if planet_data['state']['retrograde']:
                if planet_name not in ['Rahu', 'Ketu']:
                    self.assertEqual(planet_data['state']['speed_category'], 'vakra')
            
            # Nodes should always be 'medium'
            if planet_name in ['Rahu', 'Ketu']:
                self.assertEqual(planet_data['state']['speed_category'], 'medium')
    
    def test_baladi_avasthas(self):
        """Test Baladi Avastha calculations"""
        planets = self.calculator.planets
        
        # Verify all planets have Baladi Avasthas assigned
        for planet_name, planet_data in planets.items():
            self.assertIn('avasthas', planet_data)
            self.assertIn('baladi', planet_data['avasthas'])
            
            # Verify the Baladi Avastha is one of the expected values
            valid_avasthas = ['bala', 'kumara', 'yuva', 'vriddha', 'mrita']
            self.assertIn(planet_data['avasthas']['baladi'], valid_avasthas)
            
            # Print longitude in sign and Baladi Avastha for debugging
            print(f"{planet_name}: Longitude in sign = {planet_data['longitude_in_sign']:.2f}, "
                  f"Baladi Avastha = {planet_data['avasthas']['baladi']}")
            
            # Test specific cases based on longitude in sign
            longitude = planet_data['longitude_in_sign']
            if longitude < 6:
                self.assertEqual(planet_data['avasthas']['baladi'], 'bala')
            elif longitude < 12:
                self.assertEqual(planet_data['avasthas']['baladi'], 'kumara')
            elif longitude < 18:
                self.assertEqual(planet_data['avasthas']['baladi'], 'yuva')
            elif longitude < 24:
                self.assertEqual(planet_data['avasthas']['baladi'], 'vriddha')
            else:
                self.assertEqual(planet_data['avasthas']['baladi'], 'mrita')
    
    def test_jagradadi_avasthas(self):
        """Test Jagradadi Avastha calculations"""
        planets = self.calculator.planets
        sun_longitude = planets['Sun']['longitude']
        
        # Verify all planets have Jagradadi Avasthas assigned
        for planet_name, planet_data in planets.items():
            self.assertIn('avasthas', planet_data)
            self.assertIn('jagradadi', planet_data['avasthas'])
            
            # Verify the Jagradadi Avastha is one of the expected values
            valid_avasthas = ['jagrad', 'swapna', 'sushupti']
            self.assertIn(planet_data['avasthas']['jagradadi'], valid_avasthas)
            
            # Print angular distance from Sun and Jagradadi Avastha for debugging
            if planet_name != 'Sun':
                angular_distance = (planet_data['longitude'] - sun_longitude) % 360
                print(f"{planet_name}: Angular distance from Sun = {angular_distance:.2f}, "
                      f"Jagradadi Avastha = {planet_data['avasthas']['jagradadi']}")
            
            # Sun should always be in Jagrad state
            if planet_name == 'Sun':
                self.assertEqual(planet_data['avasthas']['jagradadi'], 'jagrad')
            else:
                # Test specific cases based on angular distance from Sun
                angular_distance = (planet_data['longitude'] - sun_longitude) % 360
                if angular_distance < 120:
                    self.assertEqual(planet_data['avasthas']['jagradadi'], 'jagrad')
                elif angular_distance < 240:
                    self.assertEqual(planet_data['avasthas']['jagradadi'], 'swapna')
                else:
                    self.assertEqual(planet_data['avasthas']['jagradadi'], 'sushupti')
    
    def test_lajjitadi_avasthas(self):
        """Test Lajjitadi Avastha calculations"""
        planets = self.calculator.planets
        
        # Verify all planets except nodes have Lajjitadi Avasthas assigned
        for planet_name, planet_data in planets.items():
            if planet_name in ['Rahu', 'Ketu']:
                continue  # Nodes don't have Lajjitadi Avasthas
                
            self.assertIn('avasthas', planet_data)
            self.assertIn('lajjitadi', planet_data['avasthas'])
            
            # Verify the Lajjitadi Avastha is one of the expected values
            valid_avasthas = ['lajjita', 'garvita', 'kshudita', 'trushita', 'mudita', 'kshobhita']
            self.assertIn(planet_data['avasthas']['lajjitadi'], valid_avasthas)
            
            # Print dignity, house, and Lajjitadi Avastha for debugging
            print(f"{planet_name}: Dignity = {planet_data['dignity']}, "
                  f"House = {planet_data['house']}, "
                  f"Combustion = {planet_data['state'].get('combustion', False)}, "
                  f"Lajjitadi Avastha = {planet_data['avasthas']['lajjitadi']}")
            
            # Test specific cases based on dignity and house
            dignity = planet_data['dignity']
            house = planet_data['house']
            
            if dignity == 'debilitated':
                self.assertEqual(planet_data['avasthas']['lajjitadi'], 'lajjita')
            elif dignity == 'exalted':
                self.assertEqual(planet_data['avasthas']['lajjitadi'], 'garvita')
            elif house in [6, 8, 12]:
                self.assertEqual(planet_data['avasthas']['lajjitadi'], 'kshudita')
            elif house in [1, 5, 9]:
                self.assertEqual(planet_data['avasthas']['lajjitadi'], 'trushita')
            elif planet_data['state'].get('combustion', False):
                self.assertEqual(planet_data['avasthas']['lajjitadi'], 'mudita')
            else:
                self.assertEqual(planet_data['avasthas']['lajjitadi'], 'kshobhita')

if __name__ == '__main__':
    unittest.main()
