"""
Vimsopaka Bala Calculator Module

This module calculates the Vimsopaka Bala (20-point strength) of planets based on their
positions in various divisional charts (Varga charts). Vimsopaka Bala is an important
strength parameter in Vedic astrology that evaluates a planet's cumulative strength
across multiple divisional charts.

The calculation assigns different weights to different divisional charts and computes
a total strength out of 20 points.
"""

class VimsopakaCalculator:
    """
    VimsopakaCalculator class for calculating Vimsopaka Bala (20-point strength)
    based on planetary positions in divisional charts.
    """
    
    # Weights for different divisional charts in Vimsopaka Bala calculation
    # As per classical texts, different charts have different importance
    VARGA_WEIGHTS = {
        'D1': 3.5,  # Rashi (birth chart)
        'D2': 0.5,  # Hora (wealth)
        'D3': 1.0,  # Drekkana (siblings)
        'D4': 0.5,  # Chaturthamsha (fortune)
        'D7': 0.5,  # Saptamsha (children)
        'D9': 3.0,  # Navamsha (spouse)
        'D10': 2.5, # Dashamsha (career)
        'D12': 0.5, # Dwadashamsha (parents)
        'D16': 2.0, # Shodashamsha (vehicles)
        'D20': 1.5, # Vimshamsha (spiritual life)
        'D24': 1.0, # Chaturvimshamsha (education)
        'D27': 1.0, # Saptavimshamsha (strength)
        'D30': 1.0, # Trimshamsha (misfortune)
        'D40': 0.5, # Khavedamsha (auspicious/inauspicious effects)
        'D45': 0.5, # Akshavedamsha (general indications)
        'D60': 1.0, # Shashtiamsha (overall life)
    }
    
    # Total possible points in Vimsopaka Bala
    TOTAL_POINTS = 20.0
    
    def __init__(self, divisional_charts):
        """
        Initialize the Vimsopaka Bala calculator with divisional charts.
        
        Args:
            divisional_charts (dict): Dictionary containing divisional charts data
                                     with keys like 'D1', 'D9', etc.
        """
        self.divisional_charts = divisional_charts
        print(f"VimsopakaCalculator initialized with divisional charts: {list(divisional_charts.keys())}")
        
        # Debug: Print the structure of the first divisional chart
        if divisional_charts and len(divisional_charts) > 0:
            first_chart_key = list(divisional_charts.keys())[0]
            print(f"First chart ({first_chart_key}) structure: {list(divisional_charts[first_chart_key].keys())}")
            
            # Check if planets are in the expected format
            if 'planets' in divisional_charts[first_chart_key]:
                print(f"Planets in {first_chart_key}: {list(divisional_charts[first_chart_key]['planets'].keys())}")
                if 'Sun' in divisional_charts[first_chart_key]['planets']:
                    sun_data = divisional_charts[first_chart_key]['planets']['Sun']
                    print(f"Sun data in {first_chart_key}: {sun_data}")
                    print(f"Sun data keys: {list(sun_data.keys())}")
    
    def get_dignity_points(self, planet, sign_num):
        """
        Calculate dignity points for a planet in a specific sign.
        
        Args:
            planet (str): Planet name
            sign_num (int): Sign number (0-11)
            
        Returns:
            float: Points based on planetary dignity (0-1)
        """
        # Determine dignity based on sign placement
        # Exaltation: 1.0, Own sign: 0.75, Friend's sign: 0.5, Neutral sign: 0.25, Debilitation: 0
        if self.is_exalted(planet, sign_num):
            return 1.0
        elif self.is_own_sign(planet, sign_num):
            return 0.75
        elif self.is_friend_sign(planet, sign_num):
            return 0.5
        elif self.is_neutral_sign(planet, sign_num):
            return 0.25
        else:  # Debilitation or enemy sign
            return 0.0
    
    def is_exalted(self, planet, sign_num):
        """
        Check if a planet is exalted in a given sign.
        
        Args:
            planet (str): Planet name
            sign_num (int): Sign number (0-11)
            
        Returns:
            bool: True if the planet is exalted, False otherwise
        """
        # Exaltation signs for planets
        exaltation = {
            'Sun': 0,      # Aries
            'Moon': 1,     # Taurus
            'Mars': 9,     # Capricorn
            'Mercury': 5,  # Virgo
            'Jupiter': 3,  # Cancer
            'Venus': 11,   # Pisces
            'Saturn': 6,   # Libra
            'Rahu': 2,     # Gemini
            'Ketu': 8      # Sagittarius
        }
        
        return planet in exaltation and sign_num == exaltation[planet]
    
    def is_own_sign(self, planet, sign_num):
        """
        Check if a planet is in its own sign.
        
        Args:
            planet (str): Planet name
            sign_num (int): Sign number (0-11)
            
        Returns:
            bool: True if the planet is in its own sign, False otherwise
        """
        # Own signs for planets (some planets rule two signs)
        own_signs = {
            'Sun': [4],                # Leo
            'Moon': [3],               # Cancer
            'Mars': [0, 7],            # Aries, Scorpio
            'Mercury': [2, 5],         # Gemini, Virgo
            'Jupiter': [8, 11],        # Sagittarius, Pisces
            'Venus': [1, 6],           # Taurus, Libra
            'Saturn': [9, 10],         # Capricorn, Aquarius
            'Rahu': [],                # No rulership
            'Ketu': []                 # No rulership
        }
        
        return planet in own_signs and sign_num in own_signs[planet]
    
    def is_friend_sign(self, planet, sign_num):
        """
        Check if a planet is in a friend's sign.
        
        Args:
            planet (str): Planet name
            sign_num (int): Sign number (0-11)
            
        Returns:
            bool: True if the planet is in a friend's sign, False otherwise
        """
        # Friendship relationships between planets
        friends = {
            'Sun': ['Moon', 'Mars', 'Jupiter'],
            'Moon': ['Sun', 'Mercury'],
            'Mars': ['Sun', 'Moon', 'Jupiter'],
            'Mercury': ['Sun', 'Venus'],
            'Jupiter': ['Sun', 'Moon', 'Mars'],
            'Venus': ['Mercury', 'Saturn'],
            'Saturn': ['Mercury', 'Venus'],
            'Rahu': ['Venus', 'Saturn'],
            'Ketu': ['Venus', 'Saturn']
        }
        
        # Rulerships of signs
        sign_rulers = {
            0: 'Mars',      # Aries
            1: 'Venus',     # Taurus
            2: 'Mercury',   # Gemini
            3: 'Moon',      # Cancer
            4: 'Sun',       # Leo
            5: 'Mercury',   # Virgo
            6: 'Venus',     # Libra
            7: 'Mars',      # Scorpio
            8: 'Jupiter',   # Sagittarius
            9: 'Saturn',    # Capricorn
            10: 'Saturn',   # Aquarius
            11: 'Jupiter'   # Pisces
        }
        
        # Check if the sign's ruler is a friend of the planet
        sign_ruler = sign_rulers.get(sign_num)
        return sign_ruler in friends.get(planet, [])
    
    def is_neutral_sign(self, planet, sign_num):
        """
        Check if a planet is in a neutral sign.
        
        Args:
            planet (str): Planet name
            sign_num (int): Sign number (0-11)
            
        Returns:
            bool: True if the planet is in a neutral sign, False otherwise
        """
        # If it's not own sign, friend's sign, or enemy's sign, it's neutral
        return not (self.is_own_sign(planet, sign_num) or 
                   self.is_friend_sign(planet, sign_num) or 
                   self.is_enemy_sign(planet, sign_num))
    
    def is_enemy_sign(self, planet, sign_num):
        """
        Check if a planet is in an enemy's sign.
        
        Args:
            planet (str): Planet name
            sign_num (int): Sign number (0-11)
            
        Returns:
            bool: True if the planet is in an enemy's sign, False otherwise
        """
        # Enemy relationships between planets
        enemies = {
            'Sun': ['Saturn', 'Venus'],
            'Moon': ['Saturn'],
            'Mars': ['Mercury', 'Venus'],
            'Mercury': ['Moon'],
            'Jupiter': ['Mercury', 'Venus'],
            'Venus': ['Sun', 'Moon', 'Jupiter'],
            'Saturn': ['Sun', 'Moon', 'Mars', 'Jupiter'],
            'Rahu': ['Sun', 'Moon', 'Mars'],
            'Ketu': ['Sun', 'Moon', 'Mars']
        }
        
        # Rulerships of signs
        sign_rulers = {
            0: 'Mars',      # Aries
            1: 'Venus',     # Taurus
            2: 'Mercury',   # Gemini
            3: 'Moon',      # Cancer
            4: 'Sun',       # Leo
            5: 'Mercury',   # Virgo
            6: 'Venus',     # Libra
            7: 'Mars',      # Scorpio
            8: 'Jupiter',   # Sagittarius
            9: 'Saturn',    # Capricorn
            10: 'Saturn',   # Aquarius
            11: 'Jupiter'   # Pisces
        }
        
        # Check if the sign's ruler is an enemy of the planet
        sign_ruler = sign_rulers.get(sign_num)
        return sign_ruler in enemies.get(planet, [])
    
    def calculate_vimsopaka_bala(self, planet):
        """
        Calculate Vimsopaka Bala for a given planet.
        
        Args:
            planet (str): Name of the planet (e.g., 'Sun', 'Moon', etc.)
            
        Returns:
            dict: Dictionary containing Vimsopaka Bala details
        """
        # Define weights for each divisional chart
        chart_weights = {
            'D1': 3.5,  # Rashi (Birth chart)
            'D9': 1.5,  # Navamsha
            'D12': 1.0,  # Dwadashamsha
        }
        
        # Initialize chart points
        chart_points = {}
        total_points = 0
        max_points = 0
        
        # Calculate points for each divisional chart
        for chart_name, weight in chart_weights.items():
            print(f"Processing {chart_name} for {planet}...")
            
            if chart_name not in self.divisional_charts:
                print(f"Chart {chart_name} not found in divisional charts")
                continue
                
            chart = self.divisional_charts[chart_name]
            
            if 'planets' not in chart:
                print(f"No planets key found in {chart_name}")
                continue
                
            if planet not in chart['planets']:
                print(f"Planet {planet} not found in {chart_name}")
                continue
            
            # Get planet data from the chart
            planet_data = chart['planets'][planet]
            
            # Get sign number from sign name if sign_num is not available
            if 'sign_num' in planet_data:
                sign_num = planet_data['sign_num']
            elif 'sign' in planet_data:
                # Convert sign name to number
                sign_map = {
                    'Aries': 0, 'Taurus': 1, 'Gemini': 2, 'Cancer': 3,
                    'Leo': 4, 'Virgo': 5, 'Libra': 6, 'Scorpio': 7,
                    'Sagittarius': 8, 'Capricorn': 9, 'Aquarius': 10, 'Pisces': 11
                }
                sign_num = sign_map.get(planet_data['sign'], 0)
                print(f"Converted sign {planet_data['sign']} to number {sign_num}")
            else:
                # Try to get sign number from longitude
                if 'longitude' in planet_data:
                    sign_num = int(planet_data['longitude'] / 30)
                    print(f"Calculated sign_num {sign_num} from longitude {planet_data['longitude']}")
                else:
                    print(f"No sign_num, sign, or longitude found for {planet} in {chart_name}")
                    continue
            
            # Calculate dignity points
            dignity_factor = self.get_dignity_points(planet, sign_num)
            points = dignity_factor * weight
            
            # Store points for this chart
            chart_points[chart_name] = {
                "dignity_factor": dignity_factor,
                "weight": weight,
                "points": points
            }
            
            # Add to total points
            total_points += points
            
            # Add to max possible points
            max_points += 5 * weight  # 5 is the maximum points a planet can get in a chart
        
        # Calculate percentage
        percentage = (total_points / max_points) * 100 if max_points > 0 else 0
        
        # Determine if the planet is strong based on percentage
        is_strong = percentage >= 50
        
        # Determine strength category
        strength_category = self.get_strength_category(percentage)
        
        # Return Vimsopaka Bala details
        return {
            'planet': planet,
            'chart_points': chart_points,
            'total_points': round(total_points, 2),
            'percentage': round(percentage, 2),
            'is_strong': is_strong,
            'strength_category': strength_category
        }
    
    def get_strength_category(self, percentage):
        """
        Get the strength category based on Vimsopaka Bala percentage.
        
        Args:
            percentage (float): Vimsopaka Bala percentage (0-100)
            
        Returns:
            str: Strength category
        """
        if percentage >= 80:
            return "Excellent"
        elif percentage >= 60:
            return "Good"
        elif percentage >= 40:
            return "Moderate"
        elif percentage >= 20:
            return "Weak"
        else:
            return "Very Weak"
    
    def calculate_all_vimsopaka_bala(self):
        """
        Calculate Vimsopaka Bala for all planets.
        
        Returns:
            dict: Dictionary containing Vimsopaka Bala results for all planets
        """
        planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
        results = {}
        
        print(f"Starting Vimsopaka Bala calculation for all planets: {planets}")
        
        try:
            for planet in planets:
                print(f"Calculating Vimsopaka Bala for {planet}...")
                try:
                    results[planet] = self.calculate_vimsopaka_bala(planet)
                    print(f"Vimsopaka Bala for {planet} calculated successfully: {results[planet]['total_points']} points")
                except Exception as e:
                    print(f"Error calculating Vimsopaka Bala for {planet}: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    results[planet] = {
                        'planet': planet,
                        'error': str(e),
                        'total_points': 0,
                        'percentage': 0,
                        'is_strong': False,
                        'strength_category': 'Error',
                        'chart_points': {}
                    }
            
            print(f"Vimsopaka Bala calculation completed for all planets")
            return results
        except Exception as e:
            print(f"Error in calculate_all_vimsopaka_bala: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'error': str(e)}
