"""
Ishta-Kashta Phala Calculator Module

This module calculates the Ishta-Kashta Phala (benefic and malefic effects) of planets
based on their positions in the birth chart. Ishta-Kashta Phala is an important
parameter in Vedic astrology that evaluates the benefic (Ishta) and malefic (Kashta)
effects of planets on different areas of life.

The calculation considers planetary positions, dignities, aspects, and relationships
to determine the net benefic or malefic influence of each planet.
"""

class IshtaKashtaCalculator:
    """
    IshtaKashtaCalculator class for calculating Ishta (benefic) and Kashta (malefic)
    effects of planets in a Vedic birth chart.
    """
    
    # Natural benefic and malefic planets
    NATURAL_BENEFICS = ['Moon', 'Mercury', 'Jupiter', 'Venus']
    NATURAL_MALEFICS = ['Sun', 'Mars', 'Saturn', 'Rahu', 'Ketu']
    
    # Weightage for different factors in Ishta-Kashta calculation
    FACTOR_WEIGHTS = {
        'natural_nature': 2.0,    # Natural benefic/malefic nature
        'dignity': 3.0,           # Dignity status (exaltation, own sign, etc.)
        'house_position': 2.5,    # Position in houses (benefic/malefic houses)
        'aspects': 1.5,           # Aspects received from other planets
        'associations': 1.0       # Conjunctions with other planets
    }
    
    # Maximum possible points for Ishta and Kashta
    MAX_POINTS = 60.0
    
    def __init__(self, birth_chart, shadbala_results=None, vimsopaka_results=None):
        """
        Initialize the Ishta-Kashta Phala calculator with birth chart data.
        
        Args:
            birth_chart (dict): Dictionary containing birth chart data
            shadbala_results (dict, optional): Shadbala calculation results
            vimsopaka_results (dict, optional): Vimsopaka Bala calculation results
        """
        self.birth_chart = birth_chart
        self.shadbala_results = shadbala_results
        self.vimsopaka_results = vimsopaka_results
        
        # Debug information
        print(f"IshtaKashtaCalculator initialized with birth chart data")
        if shadbala_results:
            print(f"Shadbala results provided for planets: {list(shadbala_results.keys())}")
        if vimsopaka_results:
            print(f"Vimsopaka Bala results provided for planets: {list(vimsopaka_results.keys())}")
    
    def is_natural_benefic(self, planet):
        """
        Check if a planet is naturally benefic.
        
        Args:
            planet (str): Planet name
            
        Returns:
            bool: True if the planet is naturally benefic, False otherwise
        """
        return planet in self.NATURAL_BENEFICS
    
    def is_natural_malefic(self, planet):
        """
        Check if a planet is naturally malefic.
        
        Args:
            planet (str): Planet name
            
        Returns:
            bool: True if the planet is naturally malefic, False otherwise
        """
        return planet in self.NATURAL_MALEFICS
    
    def get_dignity_factor(self, planet, sign_num):
        """
        Calculate the dignity factor for Ishta-Kashta calculation.
        
        Args:
            planet (str): Planet name
            sign_num (int): Sign number (0-11)
            
        Returns:
            tuple: (ishta_points, kashta_points) based on dignity
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
        
        # Debilitation signs for planets (opposite to exaltation)
        debilitation = {
            'Sun': 6,      # Libra
            'Moon': 7,     # Scorpio
            'Mars': 3,     # Cancer
            'Mercury': 11, # Pisces
            'Jupiter': 9,  # Capricorn
            'Venus': 5,    # Virgo
            'Saturn': 0,   # Aries
            'Rahu': 8,     # Sagittarius
            'Ketu': 2      # Gemini
        }
        
        # Own signs for planets
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
        
        # Initialize ishta and kashta points
        ishta_points = 0.0
        kashta_points = 0.0
        
        # Exaltation gives maximum ishta points
        if planet in exaltation and sign_num == exaltation[planet]:
            ishta_points += 5.0
            return (ishta_points, kashta_points)
        
        # Debilitation gives maximum kashta points
        if planet in debilitation and sign_num == debilitation[planet]:
            kashta_points += 5.0
            return (ishta_points, kashta_points)
        
        # Own sign gives high ishta points
        if planet in own_signs and sign_num in own_signs[planet]:
            ishta_points += 4.0
            return (ishta_points, kashta_points)
        
        # Friend's sign gives moderate ishta points
        sign_ruler = sign_rulers.get(sign_num)
        if sign_ruler in friends.get(planet, []):
            ishta_points += 3.0
            return (ishta_points, kashta_points)
        
        # Enemy's sign gives moderate kashta points
        enemies = []
        for p, friends_list in friends.items():
            if planet not in friends_list and p != planet:
                enemies.append(p)
        
        if sign_ruler in enemies:
            kashta_points += 3.0
            return (ishta_points, kashta_points)
        
        # Neutral sign gives low ishta points
        ishta_points += 1.0
        return (ishta_points, kashta_points)
    
    def get_house_position_factor(self, planet, house_num):
        """
        Calculate the house position factor for Ishta-Kashta calculation.
        
        Args:
            planet (str): Planet name
            house_num (int): House number (1-12)
            
        Returns:
            tuple: (ishta_points, kashta_points) based on house position
        """
        # Initialize ishta and kashta points
        ishta_points = 0.0
        kashta_points = 0.0
        
        # Benefic houses for all planets
        benefic_houses = [1, 4, 5, 7, 9, 10]  # 1st, 4th, 5th, 7th, 9th, 10th houses
        
        # Malefic houses for all planets
        malefic_houses = [6, 8, 12]  # 6th, 8th, 12th houses
        
        # Neutral houses
        neutral_houses = [2, 3, 11]  # 2nd, 3rd, 11th houses
        
        # Special considerations for specific planets
        if planet == 'Saturn':
            # Saturn does well in 3rd, 6th, 11th houses
            if house_num in [3, 6, 11]:
                ishta_points += 3.0
                return (ishta_points, kashta_points)
        
        if planet == 'Mars':
            # Mars does well in 3rd, 6th houses
            if house_num in [3, 6]:
                ishta_points += 3.0
                return (ishta_points, kashta_points)
        
        if planet == 'Rahu' or planet == 'Ketu':
            # Rahu and Ketu do well in 3rd, 6th, 11th houses
            if house_num in [3, 6, 11]:
                ishta_points += 2.5
                return (ishta_points, kashta_points)
        
        # General house position evaluation
        if house_num in benefic_houses:
            ishta_points += 2.0
        elif house_num in malefic_houses:
            kashta_points += 2.0
        else:  # Neutral houses
            ishta_points += 1.0
        
        return (ishta_points, kashta_points)
    
    def get_aspect_factor(self, planet, aspects):
        """
        Calculate the aspect factor for Ishta-Kashta calculation.
        
        Args:
            planet (str): Planet name
            aspects (list): List of planets aspecting this planet
            
        Returns:
            tuple: (ishta_points, kashta_points) based on aspects
        """
        # Initialize ishta and kashta points
        ishta_points = 0.0
        kashta_points = 0.0
        
        # Evaluate aspects from each planet
        for aspecting_planet in aspects:
            if aspecting_planet in self.NATURAL_BENEFICS:
                ishta_points += 1.0
            elif aspecting_planet in self.NATURAL_MALEFICS:
                kashta_points += 1.0
        
        return (ishta_points, kashta_points)
    
    def get_association_factor(self, planet, conjunctions):
        """
        Calculate the association (conjunction) factor for Ishta-Kashta calculation.
        
        Args:
            planet (str): Planet name
            conjunctions (list): List of planets in conjunction with this planet
            
        Returns:
            tuple: (ishta_points, kashta_points) based on conjunctions
        """
        # Initialize ishta and kashta points
        ishta_points = 0.0
        kashta_points = 0.0
        
        # Evaluate conjunctions with each planet
        for conj_planet in conjunctions:
            if conj_planet in self.NATURAL_BENEFICS:
                ishta_points += 1.5
            elif conj_planet in self.NATURAL_MALEFICS:
                kashta_points += 1.5
        
        return (ishta_points, kashta_points)
    
    def calculate_ishta_kashta(self, planet):
        """
        Calculate Ishta-Kashta Phala for a given planet.
        
        Args:
            planet (str): Name of the planet (e.g., 'Sun', 'Moon', etc.)
            
        Returns:
            dict: Dictionary containing Ishta-Kashta Phala details
        """
        # Initialize factors dictionary
        factors = {
            'natural_nature': {'ishta': 0.0, 'kashta': 0.0},
            'dignity': {'ishta': 0.0, 'kashta': 0.0},
            'house_position': {'ishta': 0.0, 'kashta': 0.0},
            'aspects': {'ishta': 0.0, 'kashta': 0.0},
            'associations': {'ishta': 0.0, 'kashta': 0.0}
        }
        
        # Get planet data from birth chart
        if 'planets' not in self.birth_chart:
            raise ValueError(f"No planets data found in birth chart")
        
        if planet not in self.birth_chart['planets']:
            raise ValueError(f"Planet {planet} not found in birth chart")
        
        planet_data = self.birth_chart['planets'][planet]
        
        # 1. Natural nature factor
        if self.is_natural_benefic(planet):
            factors['natural_nature']['ishta'] = 5.0
        elif self.is_natural_malefic(planet):
            factors['natural_nature']['kashta'] = 5.0
        
        # 2. Dignity factor
        sign_num = planet_data.get('sign_num')
        if sign_num is None:
            # Try to get sign number from sign name
            sign_map = {
                'Aries': 0, 'Taurus': 1, 'Gemini': 2, 'Cancer': 3,
                'Leo': 4, 'Virgo': 5, 'Libra': 6, 'Scorpio': 7,
                'Sagittarius': 8, 'Capricorn': 9, 'Aquarius': 10, 'Pisces': 11
            }
            sign = planet_data.get('sign')
            if sign:
                sign_num = sign_map.get(sign)
            else:
                # Try to get sign number from longitude
                longitude = planet_data.get('longitude')
                if longitude is not None:
                    sign_num = int(longitude / 30)
                else:
                    raise ValueError(f"Cannot determine sign for planet {planet}")
        
        ishta, kashta = self.get_dignity_factor(planet, sign_num)
        factors['dignity']['ishta'] = ishta
        factors['dignity']['kashta'] = kashta
        
        # 3. House position factor
        house_num = planet_data.get('house')
        if house_num is None:
            # Try to determine house from other data
            # For simplicity, we'll use sign_num + 1 as house_num (whole sign houses)
            # This is a simplification and should be replaced with actual house calculation
            house_num = sign_num + 1
        
        ishta, kashta = self.get_house_position_factor(planet, house_num)
        factors['house_position']['ishta'] = ishta
        factors['house_position']['kashta'] = kashta
        
        # 4. Aspect factor
        # Get aspects from birth chart data
        aspects = []
        if 'aspects' in planet_data:
            aspects = planet_data['aspects']
        elif 'aspected_by' in planet_data:
            aspects = planet_data['aspected_by']
        
        ishta, kashta = self.get_aspect_factor(planet, aspects)
        factors['aspects']['ishta'] = ishta
        factors['aspects']['kashta'] = kashta
        
        # 5. Association (conjunction) factor
        conjunctions = []
        if 'conjunctions' in planet_data:
            conjunctions = planet_data['conjunctions']
        
        ishta, kashta = self.get_association_factor(planet, conjunctions)
        factors['associations']['ishta'] = ishta
        factors['associations']['kashta'] = kashta
        
        # Calculate weighted total
        total_ishta = 0.0
        total_kashta = 0.0
        
        for factor, weight in self.FACTOR_WEIGHTS.items():
            total_ishta += factors[factor]['ishta'] * weight
            total_kashta += factors[factor]['kashta'] * weight
        
        # Calculate percentages
        ishta_percentage = (total_ishta / self.MAX_POINTS) * 100
        kashta_percentage = (total_kashta / self.MAX_POINTS) * 100
        
        # Determine net effect
        net_effect = total_ishta - total_kashta
        is_benefic = net_effect > 0
        
        # Determine effect category
        effect_category = self.get_effect_category(ishta_percentage, kashta_percentage)
        
        # Return Ishta-Kashta Phala details
        return {
            'planet': planet,
            'factors': factors,
            'total_ishta': round(total_ishta, 2),
            'total_kashta': round(total_kashta, 2),
            'ishta_percentage': round(ishta_percentage, 2),
            'kashta_percentage': round(kashta_percentage, 2),
            'net_effect': round(net_effect, 2),
            'is_benefic': is_benefic,
            'effect_category': effect_category
        }
    
    def get_effect_category(self, ishta_percentage, kashta_percentage):
        """
        Get the effect category based on Ishta and Kashta percentages.
        
        Args:
            ishta_percentage (float): Ishta percentage (0-100)
            kashta_percentage (float): Kashta percentage (0-100)
            
        Returns:
            str: Effect category
        """
        diff = ishta_percentage - kashta_percentage
        
        if diff > 40:
            return "Highly Benefic"
        elif diff > 20:
            return "Moderately Benefic"
        elif diff > 5:
            return "Slightly Benefic"
        elif diff < -40:
            return "Highly Malefic"
        elif diff < -20:
            return "Moderately Malefic"
        elif diff < -5:
            return "Slightly Malefic"
        else:
            return "Neutral"
    
    def calculate_all_ishta_kashta(self):
        """
        Calculate Ishta-Kashta Phala for all planets.
        
        Returns:
            dict: Dictionary containing Ishta-Kashta Phala results for all planets
        """
        planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
        results = {}
        
        print(f"Starting Ishta-Kashta Phala calculation for all planets")
        
        try:
            for planet in planets:
                print(f"Calculating Ishta-Kashta Phala for {planet}...")
                try:
                    results[planet] = self.calculate_ishta_kashta(planet)
                    print(f"Ishta-Kashta Phala for {planet} calculated successfully")
                except Exception as e:
                    print(f"Error calculating Ishta-Kashta Phala for {planet}: {str(e)}")
                    results[planet] = {
                        'planet': planet,
                        'error': str(e),
                        'total_ishta': 0,
                        'total_kashta': 0,
                        'ishta_percentage': 0,
                        'kashta_percentage': 0,
                        'net_effect': 0,
                        'is_benefic': False,
                        'effect_category': 'Error',
                        'factors': {}
                    }
            
            print(f"Ishta-Kashta Phala calculation completed for all planets")
            
            # Calculate overall chart Ishta-Kashta balance
            total_ishta = sum(results[p]['total_ishta'] for p in planets if 'error' not in results[p])
            total_kashta = sum(results[p]['total_kashta'] for p in planets if 'error' not in results[p])
            
            # Add overall results
            results['overall'] = {
                'total_ishta': round(total_ishta, 2),
                'total_kashta': round(total_kashta, 2),
                'net_effect': round(total_ishta - total_kashta, 2),
                'is_benefic': total_ishta > total_kashta,
                'effect_category': self.get_effect_category(
                    (total_ishta / (self.MAX_POINTS * len(planets))) * 100,
                    (total_kashta / (self.MAX_POINTS * len(planets))) * 100
                )
            }
            
            return results
        except Exception as e:
            print(f"Error in calculate_all_ishta_kashta: {str(e)}")
            return {'error': str(e)}
