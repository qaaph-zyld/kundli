"""
Yoga Identification System for Vedic Kundli Calculator.
This module implements various Yoga detection and analysis functions.
"""

from .core import VedicCalculator
import math
from collections import defaultdict

class YogaSystem:
    """
    Class for identifying and analyzing various Vedic astrological Yogas (combinations).
    """
    
    def __init__(self, chart_data):
        """
        Initialize the YogaSystem with chart data.
        
        Args:
            chart_data: Dictionary containing chart data including planets, houses, etc.
        """
        self.chart_data = chart_data
        self.planets = chart_data.get('planets', {})
        self.houses = chart_data.get('houses', {})
        self.ascendant = chart_data.get('ascendant', 0)
        self.yogas = {
            'raja_yogas': [],
            'dhana_yogas': [],
            'pancha_mahapurusha_yogas': [],
            'nabhasa_yogas': [],
            'other_yogas': []
        }
    
    def identify_all_yogas(self):
        """
        Identify all yogas in the chart.
        
        Returns:
            Dictionary containing all identified yogas.
        """
        # Identify Raja Yogas
        self.identify_raja_yogas()
        
        # Identify Dhana Yogas
        self.identify_dhana_yogas()
        
        # Identify Pancha Mahapurusha Yogas
        self.identify_pancha_mahapurusha_yogas()
        
        # Identify Nabhasa Yogas
        self.identify_nabhasa_yogas()
        
        # Identify other yogas
        self.identify_other_yogas()
        
        return self.yogas
    
    def identify_raja_yogas(self):
        """
        Identify Raja Yogas (combinations for power and authority).
        """
        # Get lords of houses
        house_lords = self._get_house_lords()
        
        # Check for Raja Yogas formed by house lords
        # Raja Yoga occurs when lord of a kendra (1, 4, 7, 10) and lord of a trikona (1, 5, 9) conjoin or aspect each other
        kendras = [1, 4, 7, 10]
        trikonas = [1, 5, 9]
        
        # Find lords of kendras and trikonas
        kendra_lords = [planet for planet, lordships in house_lords.items() if any(house in kendras for house in lordships)]
        trikona_lords = [planet for planet, lordships in house_lords.items() if any(house in trikonas for house in lordships)]
        
        # Check for conjunctions between kendra and trikona lords
        for kendra_lord in kendra_lords:
            for trikona_lord in trikona_lords:
                if kendra_lord != trikona_lord:  # Ensure they are different planets
                    if self._are_planets_conjunct(kendra_lord, trikona_lord):
                        # Raja Yoga by conjunction
                        yoga_details = {
                            'type': 'Raja Yoga by conjunction',
                            'planets': [kendra_lord, trikona_lord],
                            'description': f"Raja Yoga formed by conjunction of {kendra_lord} (lord of kendra) and {trikona_lord} (lord of trikona).",
                            'strength': self._calculate_yoga_strength(kendra_lord, trikona_lord)
                        }
                        self.yogas['raja_yogas'].append(yoga_details)
                    elif self._are_planets_aspecting(kendra_lord, trikona_lord):
                        # Raja Yoga by aspect
                        yoga_details = {
                            'type': 'Raja Yoga by aspect',
                            'planets': [kendra_lord, trikona_lord],
                            'description': f"Raja Yoga formed by aspect between {kendra_lord} (lord of kendra) and {trikona_lord} (lord of trikona).",
                            'strength': self._calculate_yoga_strength(kendra_lord, trikona_lord) * 0.8  # Aspect is slightly weaker than conjunction
                        }
                        self.yogas['raja_yogas'].append(yoga_details)
        
        # Check for Gaja Kesari Yoga (Jupiter in kendra from Moon)
        if 'Moon' in self.planets and 'Jupiter' in self.planets:
            moon_house = self.planets['Moon']['house']
            jupiter_house = self.planets['Jupiter']['house']
            
            if (jupiter_house - moon_house) % 12 + 1 in [1, 4, 7, 10]:
                yoga_details = {
                    'type': 'Gaja Kesari Yoga',
                    'planets': ['Moon', 'Jupiter'],
                    'description': "Gaja Kesari Yoga formed by Jupiter in kendra from Moon. This yoga gives wisdom, authority, and success.",
                    'strength': self._calculate_yoga_strength('Moon', 'Jupiter')
                }
                self.yogas['raja_yogas'].append(yoga_details)
    
    def identify_dhana_yogas(self):
        """
        Identify Dhana Yogas (combinations for wealth).
        """
        # Get lords of houses
        house_lords = self._get_house_lords()
        
        # Check for Dhana Yogas
        # Dhana Yoga occurs when lord of 2nd or 11th house (wealth houses) associates with lord of 5th or 9th house (fortune houses)
        wealth_houses = [2, 11]
        fortune_houses = [5, 9]
        
        # Find lords of wealth and fortune houses
        wealth_lords = [planet for planet, lordships in house_lords.items() if any(house in wealth_houses for house in lordships)]
        fortune_lords = [planet for planet, lordships in house_lords.items() if any(house in fortune_houses for house in lordships)]
        
        # Check for conjunctions between wealth and fortune lords
        for wealth_lord in wealth_lords:
            for fortune_lord in fortune_lords:
                if wealth_lord != fortune_lord:  # Ensure they are different planets
                    if self._are_planets_conjunct(wealth_lord, fortune_lord):
                        # Dhana Yoga by conjunction
                        yoga_details = {
                            'type': 'Dhana Yoga by conjunction',
                            'planets': [wealth_lord, fortune_lord],
                            'description': f"Dhana Yoga formed by conjunction of {wealth_lord} (lord of wealth house) and {fortune_lord} (lord of fortune house).",
                            'strength': self._calculate_yoga_strength(wealth_lord, fortune_lord)
                        }
                        self.yogas['dhana_yogas'].append(yoga_details)
                    elif self._are_planets_aspecting(wealth_lord, fortune_lord):
                        # Dhana Yoga by aspect
                        yoga_details = {
                            'type': 'Dhana Yoga by aspect',
                            'planets': [wealth_lord, fortune_lord],
                            'description': f"Dhana Yoga formed by aspect between {wealth_lord} (lord of wealth house) and {fortune_lord} (lord of fortune house).",
                            'strength': self._calculate_yoga_strength(wealth_lord, fortune_lord) * 0.8  # Aspect is slightly weaker than conjunction
                        }
                        self.yogas['dhana_yogas'].append(yoga_details)
        
        # Check for Lakshmi Yoga (Venus and Jupiter in kendras)
        if 'Venus' in self.planets and 'Jupiter' in self.planets:
            venus_house = self.planets['Venus']['house']
            jupiter_house = self.planets['Jupiter']['house']
            
            if venus_house in [1, 4, 7, 10] and jupiter_house in [1, 4, 7, 10]:
                yoga_details = {
                    'type': 'Lakshmi Yoga',
                    'planets': ['Venus', 'Jupiter'],
                    'description': "Lakshmi Yoga formed by Venus and Jupiter in kendras. This yoga gives wealth, prosperity, and good fortune.",
                    'strength': self._calculate_yoga_strength('Venus', 'Jupiter')
                }
                self.yogas['dhana_yogas'].append(yoga_details)
    
    def identify_pancha_mahapurusha_yogas(self):
        """
        Identify Pancha Mahapurusha Yogas (five great person yogas).
        """
        # Pancha Mahapurusha Yogas occur when Mars, Mercury, Jupiter, Venus, or Saturn are in their own sign or exaltation sign and in a kendra (1, 4, 7, 10)
        mahapurusha_planets = {
            'Mars': {'yoga_name': 'Ruchaka Yoga', 'own_signs': [1, 8], 'exaltation': 10},
            'Mercury': {'yoga_name': 'Bhadra Yoga', 'own_signs': [3, 6], 'exaltation': 6},
            'Jupiter': {'yoga_name': 'Hamsa Yoga', 'own_signs': [9, 12], 'exaltation': 4},
            'Venus': {'yoga_name': 'Malavya Yoga', 'own_signs': [2, 7], 'exaltation': 12},
            'Saturn': {'yoga_name': 'Sasa Yoga', 'own_signs': [10, 11], 'exaltation': 7}
        }
        
        kendras = [1, 4, 7, 10]
        
        for planet, yoga_info in mahapurusha_planets.items():
            if planet in self.planets:
                planet_sign = self.planets[planet]['sign_num']
                planet_house = self.planets[planet]['house']
                
                # Check if planet is in own sign or exaltation
                in_own_sign = planet_sign in yoga_info['own_signs']
                in_exaltation = planet_sign == yoga_info['exaltation']
                
                # Check if planet is in kendra
                in_kendra = planet_house in kendras
                
                if (in_own_sign or in_exaltation) and in_kendra:
                    strength_factor = 1.0 if in_exaltation else 0.8  # Exaltation gives stronger yoga
                    
                    yoga_details = {
                        'type': yoga_info['yoga_name'],
                        'planet': planet,
                        'position': 'exaltation' if in_exaltation else 'own sign',
                        'house': planet_house,
                        'description': f"{yoga_info['yoga_name']} formed by {planet} in {'exaltation' if in_exaltation else 'own sign'} and in kendra (house {planet_house}).",
                        'strength': self._calculate_single_planet_yoga_strength(planet) * strength_factor
                    }
                    self.yogas['pancha_mahapurusha_yogas'].append(yoga_details)
    
    def identify_nabhasa_yogas(self):
        """
        Identify Nabhasa Yogas (special planetary formations).
        """
        # Get planet positions by house
        planets_by_house = defaultdict(list)
        for planet, data in self.planets.items():
            if planet not in ['Rahu', 'Ketu']:  # Exclude nodes for some calculations
                planets_by_house[data['house']].append(planet)
        
        # Check for Yuga Yoga (all planets in kendras)
        kendras = [1, 4, 7, 10]
        all_planets_in_kendras = all(self.planets[planet]['house'] in kendras for planet, data in self.planets.items() if planet not in ['Rahu', 'Ketu'])
        
        if all_planets_in_kendras:
            yoga_details = {
                'type': 'Yuga Yoga',
                'description': "Yuga Yoga formed by all planets in kendras. This yoga gives exceptional power and authority.",
                'strength': 1.0  # Maximum strength
            }
            self.yogas['nabhasa_yogas'].append(yoga_details)
        
        # Check for Vajra Yoga (planets in 1st and 7th houses)
        planets_in_1_and_7 = len(planets_by_house[1]) > 0 and len(planets_by_house[7]) > 0 and sum(len(planets) for house, planets in planets_by_house.items() if house not in [1, 7]) == 0
        
        if planets_in_1_and_7:
            yoga_details = {
                'type': 'Vajra Yoga',
                'description': "Vajra Yoga formed by planets in 1st and 7th houses only. This yoga gives strength and resilience.",
                'strength': 0.9
            }
            self.yogas['nabhasa_yogas'].append(yoga_details)
        
        # Check for Vihaga Yoga (planets in 4th and 10th houses)
        planets_in_4_and_10 = len(planets_by_house[4]) > 0 and len(planets_by_house[10]) > 0 and sum(len(planets) for house, planets in planets_by_house.items() if house not in [4, 10]) == 0
        
        if planets_in_4_and_10:
            yoga_details = {
                'type': 'Vihaga Yoga',
                'description': "Vihaga Yoga formed by planets in 4th and 10th houses only. This yoga gives career success and good fortune.",
                'strength': 0.9
            }
            self.yogas['nabhasa_yogas'].append(yoga_details)
    
    def identify_other_yogas(self):
        """
        Identify other important yogas.
        """
        # Check for Budhaditya Yoga (Sun and Mercury in same house)
        if 'Sun' in self.planets and 'Mercury' in self.planets:
            if self.planets['Sun']['house'] == self.planets['Mercury']['house']:
                yoga_details = {
                    'type': 'Budhaditya Yoga',
                    'planets': ['Sun', 'Mercury'],
                    'house': self.planets['Sun']['house'],
                    'description': "Budhaditya Yoga formed by Sun and Mercury in same house. This yoga gives intelligence, education, and communication skills.",
                    'strength': self._calculate_yoga_strength('Sun', 'Mercury')
                }
                self.yogas['other_yogas'].append(yoga_details)
        
        # Check for Chandramangala Yoga (Moon and Mars in same house)
        if 'Moon' in self.planets and 'Mars' in self.planets:
            if self.planets['Moon']['house'] == self.planets['Mars']['house']:
                yoga_details = {
                    'type': 'Chandramangala Yoga',
                    'planets': ['Moon', 'Mars'],
                    'house': self.planets['Moon']['house'],
                    'description': "Chandramangala Yoga formed by Moon and Mars in same house. This yoga gives courage, leadership, and emotional strength.",
                    'strength': self._calculate_yoga_strength('Moon', 'Mars')
                }
                self.yogas['other_yogas'].append(yoga_details)
        
        # Check for Neechabhanga Raja Yoga (planet in debilitation but lord of debilitation sign is in kendra)
        for planet, data in self.planets.items():
            if planet not in ['Rahu', 'Ketu']:  # Exclude nodes
                debilitation_signs = {
                    'Sun': 7,    # Libra
                    'Moon': 8,   # Scorpio
                    'Mars': 4,   # Cancer
                    'Mercury': 12, # Pisces
                    'Jupiter': 6,  # Virgo
                    'Venus': 6,    # Virgo
                    'Saturn': 1    # Aries
                }
                
                if planet in debilitation_signs and data['sign_num'] == debilitation_signs[planet]:
                    # Planet is in debilitation
                    # Find lord of the debilitation sign
                    sign_lords = {
                        1: 'Mars',     # Aries
                        2: 'Venus',    # Taurus
                        3: 'Mercury',  # Gemini
                        4: 'Moon',     # Cancer
                        5: 'Sun',      # Leo
                        6: 'Mercury',  # Virgo
                        7: 'Venus',    # Libra
                        8: 'Mars',     # Scorpio
                        9: 'Jupiter',  # Sagittarius
                        10: 'Saturn',  # Capricorn
                        11: 'Saturn',  # Aquarius
                        12: 'Jupiter'  # Pisces
                    }
                    
                    debilitation_lord = sign_lords[debilitation_signs[planet]]
                    
                    if debilitation_lord in self.planets and self.planets[debilitation_lord]['house'] in [1, 4, 7, 10]:
                        yoga_details = {
                            'type': 'Neechabhanga Raja Yoga',
                            'planet': planet,
                            'debilitation_lord': debilitation_lord,
                            'description': f"Neechabhanga Raja Yoga formed by {planet} in debilitation and {debilitation_lord} (lord of debilitation sign) in kendra.",
                            'strength': 0.7  # Moderate strength
                        }
                        self.yogas['raja_yogas'].append(yoga_details)
    
    def _get_house_lords(self):
        """
        Get the lords of each house.
        
        Returns:
            Dictionary mapping planets to the houses they lord.
        """
        # Sign lords according to Vedic astrology
        sign_lords = {
            'Aries': 'Mars',
            'Taurus': 'Venus',
            'Gemini': 'Mercury',
            'Cancer': 'Moon',
            'Leo': 'Sun',
            'Virgo': 'Mercury',
            'Libra': 'Venus',
            'Scorpio': 'Mars',
            'Sagittarius': 'Jupiter',
            'Capricorn': 'Saturn',
            'Aquarius': 'Saturn',
            'Pisces': 'Jupiter'
        }
        
        # Map houses to signs
        house_signs = {}
        for i in range(1, 13):
            house_data = self.houses.get(str(i), {})
            house_signs[i] = house_data.get('sign', '')
        
        # Map planets to the houses they lord
        house_lords = defaultdict(list)
        for house, sign in house_signs.items():
            lord = sign_lords.get(sign)
            if lord:
                house_lords[lord].append(house)
        
        return dict(house_lords)
    
    def _are_planets_conjunct(self, planet1, planet2):
        """
        Check if two planets are conjunct (in the same house).
        
        Args:
            planet1: First planet name
            planet2: Second planet name
        
        Returns:
            bool: True if planets are conjunct, False otherwise
        """
        if planet1 in self.planets and planet2 in self.planets:
            return self.planets[planet1]['house'] == self.planets[planet2]['house']
        return False
    
    def _are_planets_aspecting(self, planet1, planet2):
        """
        Check if two planets are aspecting each other.
        
        Args:
            planet1: First planet name
            planet2: Second planet name
        
        Returns:
            bool: True if planets are aspecting each other, False otherwise
        """
        if planet1 in self.planets and planet2 in self.planets:
            # Get houses of planets
            house1 = self.planets[planet1]['house']
            house2 = self.planets[planet2]['house']
            
            # In Vedic astrology, planets aspect the 7th house from their position
            # Additionally, Mars aspects the 4th and 8th houses, Jupiter aspects the 5th and 9th houses,
            # and Saturn aspects the 3rd and 10th houses from their position
            
            # Check for 7th aspect (all planets)
            if (house1 - house2) % 12 == 6 or (house2 - house1) % 12 == 6:
                return True
            
            # Check for special aspects
            if planet1 == 'Mars':
                if (house1 - house2) % 12 in [3, 7]:  # 4th and 8th houses
                    return True
            elif planet1 == 'Jupiter':
                if (house1 - house2) % 12 in [4, 8]:  # 5th and 9th houses
                    return True
            elif planet1 == 'Saturn':
                if (house1 - house2) % 12 in [2, 9]:  # 3rd and 10th houses
                    return True
            
            if planet2 == 'Mars':
                if (house2 - house1) % 12 in [3, 7]:  # 4th and 8th houses
                    return True
            elif planet2 == 'Jupiter':
                if (house2 - house1) % 12 in [4, 8]:  # 5th and 9th houses
                    return True
            elif planet2 == 'Saturn':
                if (house2 - house1) % 12 in [2, 9]:  # 3rd and 10th houses
                    return True
        
        return False
    
    def _calculate_yoga_strength(self, planet1, planet2):
        """
        Calculate the strength of a yoga formed by two planets.
        
        Args:
            planet1: First planet name
            planet2: Second planet name
        
        Returns:
            float: Strength value between 0 and 1
        """
        if planet1 not in self.planets or planet2 not in self.planets:
            return 0
        
        # Get planet data
        planet1_data = self.planets[planet1]
        planet2_data = self.planets[planet2]
        
        # Check if planets are in good dignity
        planet1_dignity = self._get_planet_dignity(planet1)
        planet2_dignity = self._get_planet_dignity(planet2)
        
        # Calculate base strength based on dignity
        dignity_values = {
            'exalted': 1.0,
            'own sign': 0.9,
            'friendly sign': 0.7,
            'neutral sign': 0.5,
            'enemy sign': 0.3,
            'debilitated': 0.1
        }
        
        base_strength = (dignity_values.get(planet1_dignity, 0.5) + dignity_values.get(planet2_dignity, 0.5)) / 2
        
        # Adjust for retrograde motion
        if planet1_data.get('retrograde', False) or planet2_data.get('retrograde', False):
            base_strength *= 0.8
        
        # Adjust for house placement
        house1 = planet1_data['house']
        house2 = planet2_data['house']
        
        # Kendras and trikonas are powerful houses
        powerful_houses = [1, 4, 5, 7, 9, 10]
        if house1 in powerful_houses:
            base_strength *= 1.2
        if house2 in powerful_houses:
            base_strength *= 1.2
        
        # Dusthanas (6, 8, 12) are weak houses
        weak_houses = [6, 8, 12]
        if house1 in weak_houses:
            base_strength *= 0.8
        if house2 in weak_houses:
            base_strength *= 0.8
        
        # Cap the strength at 1.0
        return min(base_strength, 1.0)
    
    def _calculate_single_planet_yoga_strength(self, planet):
        """
        Calculate the strength of a yoga formed by a single planet.
        
        Args:
            planet: Planet name
        
        Returns:
            float: Strength value between 0 and 1
        """
        if planet not in self.planets:
            return 0
        
        # Get planet data
        planet_data = self.planets[planet]
        
        # Check if planet is in good dignity
        planet_dignity = self._get_planet_dignity(planet)
        
        # Calculate base strength based on dignity
        dignity_values = {
            'exalted': 1.0,
            'own sign': 0.9,
            'friendly sign': 0.7,
            'neutral sign': 0.5,
            'enemy sign': 0.3,
            'debilitated': 0.1
        }
        
        base_strength = dignity_values.get(planet_dignity, 0.5)
        
        # Adjust for retrograde motion
        if planet_data.get('retrograde', False):
            base_strength *= 0.8
        
        # Adjust for house placement
        house = planet_data['house']
        
        # Kendras and trikonas are powerful houses
        powerful_houses = [1, 4, 5, 7, 9, 10]
        if house in powerful_houses:
            base_strength *= 1.2
        
        # Dusthanas (6, 8, 12) are weak houses
        weak_houses = [6, 8, 12]
        if house in weak_houses:
            base_strength *= 0.8
        
        # Cap the strength at 1.0
        return min(base_strength, 1.0)
    
    def _get_planet_dignity(self, planet):
        """
        Get the dignity of a planet based on its sign placement.
        
        Args:
            planet: Planet name
        
        Returns:
            str: Dignity status ('exalted', 'own sign', 'friendly sign', 'neutral sign', 'enemy sign', 'debilitated')
        """
        if planet not in self.planets:
            return 'unknown'
        
        sign_num = self.planets[planet]['sign_num']
        
        # Exaltation and debilitation signs
        exaltation_signs = {
            'Sun': 1,      # Aries
            'Moon': 2,     # Taurus
            'Mars': 10,    # Capricorn
            'Mercury': 6,  # Virgo
            'Jupiter': 4,  # Cancer
            'Venus': 12,   # Pisces
            'Saturn': 7    # Libra
        }
        
        debilitation_signs = {
            'Sun': 7,      # Libra
            'Moon': 8,     # Scorpio
            'Mars': 4,     # Cancer
            'Mercury': 12, # Pisces
            'Jupiter': 6,  # Virgo
            'Venus': 6,    # Virgo
            'Saturn': 1    # Aries
        }
        
        # Own signs
        own_signs = {
            'Sun': [5],           # Leo
            'Moon': [4],          # Cancer
            'Mars': [1, 8],       # Aries, Scorpio
            'Mercury': [3, 6],    # Gemini, Virgo
            'Jupiter': [9, 12],   # Sagittarius, Pisces
            'Venus': [2, 7],      # Taurus, Libra
            'Saturn': [10, 11]    # Capricorn, Aquarius
        }
        
        # Friendly signs (simplified)
        friendly_signs = {
            'Sun': [1, 9, 10, 11],    # Aries, Sagittarius, Capricorn, Aquarius
            'Moon': [2, 5, 7],        # Taurus, Leo, Libra
            'Mars': [5, 9, 10, 11],   # Leo, Sagittarius, Capricorn, Aquarius
            'Mercury': [2, 5, 7],     # Taurus, Leo, Libra
            'Jupiter': [1, 5, 8],     # Aries, Leo, Scorpio
            'Venus': [3, 4, 6, 12],   # Gemini, Cancer, Virgo, Pisces
            'Saturn': [3, 6, 7, 12]   # Gemini, Virgo, Libra, Pisces
        }
        
        # Check dignity
        if planet in exaltation_signs and sign_num == exaltation_signs[planet]:
            return 'exalted'
        elif planet in debilitation_signs and sign_num == debilitation_signs[planet]:
            return 'debilitated'
        elif planet in own_signs and sign_num in own_signs[planet]:
            return 'own sign'
        elif planet in friendly_signs and sign_num in friendly_signs[planet]:
            return 'friendly sign'
        elif planet in ['Rahu', 'Ketu']:
            return 'neutral sign'  # Nodes don't have traditional dignities
        else:
            # If not in any of the above, check if it's in enemy sign
            # For simplicity, we'll consider any sign not friendly or owned as enemy
            return 'enemy sign'
