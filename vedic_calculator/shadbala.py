"""
Shadbala Module for Vedic Astrology Calculations

This module implements the Shadbala system, a comprehensive method for calculating
planetary strengths in Vedic astrology. The Shadbala consists of six types of strengths:

1. Sthana Bala (Positional Strength)
2. Dig Bala (Directional Strength)
3. Kala Bala (Temporal Strength)
4. Chesta Bala (Motional Strength)
5. Naisargika Bala (Natural Strength)
6. Drik Bala (Aspectual Strength)

Each type of strength is calculated according to classical Parashari rules.
"""

import math
from datetime import datetime, timedelta

class ShadbalaCalculator:
    """
    Calculator for Shadbala (six-fold strength) in Vedic astrology.
    
    This class implements the traditional Parashari rules for calculating
    the six types of planetary strengths in the Shadbala system.
    """
    
    # Constants for Shadbala calculations
    
    # Maximum values for each type of strength
    MAX_STHANA_BALA = 60
    MAX_DIG_BALA = 60
    MAX_KALA_BALA = 60
    MAX_CHESTA_BALA = 60
    MAX_NAISARGIKA_BALA = 60
    MAX_DRIK_BALA = 60
    
    # Exaltation and debilitation points for planets (in degrees)
    EXALTATION_POINTS = {
        'Sun': 10,      # Aries 10°
        'Moon': 33,     # Taurus 3°
        'Mars': 298,    # Capricorn 28°
        'Mercury': 165, # Virgo 15°
        'Jupiter': 95,  # Cancer 5°
        'Venus': 357,   # Pisces 27°
        'Saturn': 200   # Libra 20°
    }
    
    DEBILITATION_POINTS = {
        'Sun': 190,     # Libra 10°
        'Moon': 213,    # Scorpio 3°
        'Mars': 118,    # Cancer 28°
        'Mercury': 345, # Pisces 15°
        'Jupiter': 275, # Capricorn 5°
        'Venus': 177,   # Virgo 27°
        'Saturn': 20    # Aries 20°
    }
    
    # Moolatrikona signs for planets
    MOOLATRIKONA_SIGNS = {
        'Sun': 0,       # Aries
        'Moon': 1,      # Taurus
        'Mars': 0,      # Aries
        'Mercury': 5,   # Virgo
        'Jupiter': 8,   # Sagittarius
        'Venus': 5,     # Virgo
        'Saturn': 10    # Aquarius
    }
    
    # Own signs for planets
    OWN_SIGNS = {
        'Sun': [4],                 # Leo
        'Moon': [3],                # Cancer
        'Mars': [0, 7],             # Aries, Scorpio
        'Mercury': [2, 5],          # Gemini, Virgo
        'Jupiter': [8, 11],         # Sagittarius, Pisces
        'Venus': [1, 6],            # Taurus, Libra
        'Saturn': [9, 10]           # Capricorn, Aquarius
    }
    
    # Friendly signs for planets (signs ruled by friends)
    FRIENDLY_SIGNS = {
        'Sun': [0, 4, 8],           # Aries, Leo, Sagittarius
        'Moon': [1, 3, 5],          # Taurus, Cancer, Virgo
        'Mars': [0, 4, 8, 9, 10],   # Aries, Leo, Sagittarius, Capricorn, Aquarius
        'Mercury': [1, 2, 5, 6],    # Taurus, Gemini, Virgo, Libra
        'Jupiter': [0, 3, 4, 8, 11],# Aries, Cancer, Leo, Sagittarius, Pisces
        'Venus': [1, 2, 5, 6, 11],  # Taurus, Gemini, Virgo, Libra, Pisces
        'Saturn': [9, 10, 6, 7]     # Capricorn, Aquarius, Libra, Scorpio
    }
    
    # Directional strengths - planets are strong in specific directions
    # North = 0°, East = 90°, South = 180°, West = 270°
    DIRECTIONAL_STRENGTHS = {
        'Jupiter': 0,    # North
        'Mars': 90,      # East
        'Saturn': 180,   # South
        'Mercury': 270,  # West
        'Venus': 0,      # North
        'Moon': 90,      # East
        'Sun': 180       # South
    }
    
    # Natural strengths of planets (Naisargika Bala)
    NATURAL_STRENGTHS = {
        'Saturn': 1.0,
        'Mars': 0.85,
        'Mercury': 0.7,
        'Jupiter': 0.6,
        'Venus': 0.5,
        'Moon': 0.3,
        'Sun': 0.4
    }
    
    PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    
    def __init__(self, vedic_calculator):
        """
        Initialize the ShadbalaCalculator with a VedicCalculator instance.
        
        Args:
            vedic_calculator: An instance of VedicCalculator containing planetary positions
        """
        self.vedic_calculator = vedic_calculator
        self.planets = vedic_calculator.planets
        self.houses = vedic_calculator.houses
        self.ascendant = vedic_calculator.ascendant
        self.date = vedic_calculator.date
        
    def calculate_shadbala(self):
        """
        Calculate the complete Shadbala for all planets.
        
        Returns:
            Dictionary with Shadbala results for all planets
        """
        results = {}
        
        for planet in self.planets:
            # Skip Rahu and Ketu as they have different strength calculations
            if planet in ['Rahu', 'Ketu']:
                continue
                
            planet_data = self.planets[planet]
            
            # Calculate each type of strength
            sthana_bala = self.calculate_sthana_bala(planet)
            dig_bala = self.calculate_dig_bala(planet)
            kala_bala = self.calculate_kala_bala(planet)
            chesta_bala = self.calculate_chesta_bala(planet)
            naisargika_bala = self.calculate_naisargika_bala(planet)
            drik_bala = self.calculate_drik_bala(planet)
            
            # Calculate total Shadbala
            total_shadbala = (
                sthana_bala['total'] +
                dig_bala['total'] +
                kala_bala['total'] +
                chesta_bala['total'] +
                naisargika_bala['total'] +
                drik_bala['total']
            )
            
            # Calculate Shadbala Pinda (total strength in Rupas)
            shadbala_pinda = total_shadbala / 60.0
            
            # Calculate relative strength
            required_strength = self._get_required_strength(planet)
            relative_strength = shadbala_pinda / required_strength
            
            # Determine if planet is strong enough
            is_strong = relative_strength >= 1.0
            
            results[planet] = {
                'sthana_bala': sthana_bala,
                'dig_bala': dig_bala,
                'kala_bala': kala_bala,
                'chesta_bala': chesta_bala,
                'naisargika_bala': naisargika_bala,
                'drik_bala': drik_bala,
                'total_shadbala': total_shadbala,
                'shadbala_pinda': shadbala_pinda,
                'required_strength': required_strength,
                'relative_strength': relative_strength,
                'is_strong': is_strong
            }
            
        return results
    
    def calculate_sthana_bala(self, planet):
        """
        Calculate Sthana Bala (Positional Strength) for a planet.
        
        Sthana Bala consists of:
        1. Uchcha Bala (Exaltation Strength)
        2. Saptavargaja Bala (Strength in Divisional Charts)
        3. Ojayugmarasyamsa Bala (Odd-Even Sign-Navamsa Strength)
        4. Kendradi Bala (Quadrant Strength)
        5. Drekkana Bala (Decanate Strength)
        
        Args:
            planet: Name of the planet
            
        Returns:
            Dictionary with Sthana Bala components and total
        """
        planet_data = self.planets[planet]
        longitude = planet_data['longitude']
        house = planet_data['house']
        sign_num = int(longitude / 30)
        
        # 1. Uchcha Bala (Exaltation Strength)
        uchcha_bala = self._calculate_uchcha_bala(planet, longitude)
        
        # 2. Saptavargaja Bala (Strength in Divisional Charts)
        # For MVP, we'll implement a simplified version
        saptavargaja_bala = self._calculate_saptavargaja_bala(planet, sign_num)
        
        # 3. Ojayugmarasyamsa Bala (Odd-Even Sign-Navamsa Strength)
        ojayugmarasyamsa_bala = self._calculate_ojayugmarasyamsa_bala(planet, longitude)
        
        # 4. Kendradi Bala (Quadrant Strength)
        kendradi_bala = self._calculate_kendradi_bala(planet, house)
        
        # 5. Drekkana Bala (Decanate Strength)
        drekkana_bala = self._calculate_drekkana_bala(planet, longitude)
        
        # Calculate total Sthana Bala
        total_sthana_bala = (
            uchcha_bala +
            saptavargaja_bala +
            ojayugmarasyamsa_bala +
            kendradi_bala +
            drekkana_bala
        )
        
        return {
            'uchcha_bala': uchcha_bala,
            'saptavargaja_bala': saptavargaja_bala,
            'ojayugmarasyamsa_bala': ojayugmarasyamsa_bala,
            'kendradi_bala': kendradi_bala,
            'drekkana_bala': drekkana_bala,
            'total': total_sthana_bala
        }
    
    def _calculate_uchcha_bala(self, planet, longitude):
        """
        Calculate Uchcha Bala (Exaltation Strength).
        
        A planet gets maximum strength at its exaltation point and
        minimum strength at its debilitation point.
        
        Args:
            planet: Name of the planet
            longitude: Longitude of the planet in degrees
            
        Returns:
            Uchcha Bala value (0-30)
        """
        if planet not in self.EXALTATION_POINTS:
            return 0
            
        exaltation_point = self.EXALTATION_POINTS[planet]
        debilitation_point = self.DEBILITATION_POINTS[planet]
        
        # Calculate distance from exaltation point
        distance_from_exaltation = min(
            abs(longitude - exaltation_point),
            360 - abs(longitude - exaltation_point)
        )
        
        # Calculate distance from debilitation point
        distance_from_debilitation = min(
            abs(longitude - debilitation_point),
            360 - abs(longitude - debilitation_point)
        )
        
        # If planet is closer to exaltation point
        if distance_from_exaltation <= distance_from_debilitation:
            # Maximum strength at exaltation point, decreasing as it moves away
            strength = 30 * (1 - distance_from_exaltation / 180)
        else:
            # Minimum strength at debilitation point, increasing as it moves away
            strength = 30 * (distance_from_debilitation / 180)
            
        return strength
    
    def _calculate_saptavargaja_bala(self, planet, sign_num):
        """
        Calculate Saptavargaja Bala (Strength in Divisional Charts).
        
        For MVP, we'll implement a simplified version based on:
        - Moolatrikona sign: 45 points
        - Own sign: 30 points
        - Friendly sign: 15 points
        - Neutral sign: 7.5 points
        - Enemy sign: 0 points
        
        Args:
            planet: Name of the planet
            sign_num: Sign number (0-11) where the planet is located
            
        Returns:
            Saptavargaja Bala value (0-45)
        """
        # Check if planet is in its Moolatrikona sign
        if self.MOOLATRIKONA_SIGNS.get(planet) == sign_num:
            return 45
            
        # Check if planet is in its own sign
        if sign_num in self.OWN_SIGNS.get(planet, []):
            return 30
            
        # Check if planet is in a friendly sign
        if sign_num in self.FRIENDLY_SIGNS.get(planet, []):
            return 15
            
        # For neutral and enemy signs, we would need planet relationships
        # For MVP, we'll return a default value for other signs
        return 7.5
    
    def _calculate_ojayugmarasyamsa_bala(self, planet, longitude):
        """
        Calculate Ojayugmarasyamsa Bala (Odd-Even Sign-Navamsa Strength).
        
        Male planets (Sun, Mars, Jupiter) get strength in odd signs and odd navamsas.
        Female planets (Moon, Venus) get strength in even signs and even navamsas.
        Dual planets (Mercury, Saturn) get strength in appropriate combinations.
        
        Args:
            planet: Name of the planet
            longitude: Longitude of the planet in degrees
            
        Returns:
            Ojayugmarasyamsa Bala value (0-15)
        """
        sign_num = int(longitude / 30)
        is_odd_sign = sign_num % 2 == 0  # 0-based, so even indices are odd signs
        
        # Calculate navamsa (0-8)
        position_in_sign = longitude % 30
        navamsa_span = 3 + (1/3)  # 3°20' in decimal
        navamsa_num = int(position_in_sign / navamsa_span)
        is_odd_navamsa = navamsa_num % 2 == 0  # 0-based, so even indices are odd navamsas
        
        # Define planet genders
        male_planets = ['Sun', 'Mars', 'Jupiter']
        female_planets = ['Moon', 'Venus']
        dual_planets = ['Mercury', 'Saturn']
        
        strength = 0
        
        if planet in male_planets:
            # Male planets get strength in odd signs and odd navamsas
            if is_odd_sign:
                strength += 7.5
            if is_odd_navamsa:
                strength += 7.5
        elif planet in female_planets:
            # Female planets get strength in even signs and even navamsas
            if not is_odd_sign:
                strength += 7.5
            if not is_odd_navamsa:
                strength += 7.5
        elif planet in dual_planets:
            # Dual planets get strength in appropriate combinations
            if (planet == 'Mercury' and ((is_odd_sign and is_odd_navamsa) or (not is_odd_sign and not is_odd_navamsa))) or \
               (planet == 'Saturn' and ((is_odd_sign and not is_odd_navamsa) or (not is_odd_sign and is_odd_navamsa))):
                strength = 15
                
        return strength
    
    def _calculate_kendradi_bala(self, planet, house):
        """
        Calculate Kendradi Bala (Quadrant Strength).
        
        Planets get strength based on their house position:
        - Kendras (1, 4, 7, 10): 60 points
        - Panapharas (2, 5, 8, 11): 30 points
        - Apoklimas (3, 6, 9, 12): 15 points
        
        Args:
            planet: Name of the planet
            house: House number (1-12) where the planet is located
            
        Returns:
            Kendradi Bala value (15-60)
        """
        # Kendras (angular houses)
        if house in [1, 4, 7, 10]:
            return 60
            
        # Panapharas (succedent houses)
        if house in [2, 5, 8, 11]:
            return 30
            
        # Apoklimas (cadent houses)
        return 15
    
    def _calculate_drekkana_bala(self, planet, longitude):
        """
        Calculate Drekkana Bala (Decanate Strength).
        
        Planets get strength based on their decanate position.
        
        Args:
            planet: Name of the planet
            longitude: Longitude of the planet in degrees
            
        Returns:
            Drekkana Bala value (0-15)
        """
        # Calculate position within sign (0-30 degrees)
        position_in_sign = longitude % 30
        
        # Determine decanate (0, 1, or 2)
        decanate = int(position_in_sign / 10)
        
        # For MVP, we'll use a simplified rule
        # First decanate: 15 points
        # Second decanate: 7.5 points
        # Third decanate: 0 points
        if decanate == 0:
            return 15
        elif decanate == 1:
            return 7.5
        else:
            return 0
    
    def calculate_dig_bala(self, planet):
        """
        Calculate Dig Bala (Directional Strength) for a planet.
        
        Planets get maximum strength in specific directions:
        - Jupiter, Venus: North (Ascendant)
        - Mercury: West (Descendant)
        - Saturn: South (IC)
        - Mars, Moon: East (MC)
        - Sun: South (IC)
        
        Args:
            planet: Name of the planet
            
        Returns:
            Dictionary with Dig Bala value
        """
        if planet not in self.DIRECTIONAL_STRENGTHS:
            return {'total': 0}
            
        planet_data = self.planets[planet]
        house = planet_data['house']
        
        # Get optimal direction for the planet
        optimal_direction = self.DIRECTIONAL_STRENGTHS[planet]
        
        # Map houses to directions (approximate)
        # Ascendant (house 1) = North = 0°
        # MC (house 10) = East = 90°
        # Descendant (house 7) = South = 180°
        # IC (house 4) = West = 270°
        house_directions = {
            1: 0,    # North
            2: 45,   # North-East
            3: 90,   # East
            4: 135,  # South-East
            5: 180,  # South
            6: 225,  # South-West
            7: 270,  # West
            8: 315,  # North-West
            9: 0,    # North
            10: 45,  # North-East
            11: 90,  # East
            12: 135  # South-East
        }
        
        # Get direction of the house where the planet is located
        house_direction = house_directions.get(house, 0)
        
        # Calculate angular distance between optimal direction and actual direction
        angular_distance = min(
            abs(house_direction - optimal_direction),
            360 - abs(house_direction - optimal_direction)
        )
        
        # Maximum strength when angular distance is 0, minimum when it's 180
        strength = 60 * (1 - angular_distance / 180)
        
        return {'total': strength}
    
    def calculate_kala_bala(self, planet):
        """
        Calculate Kala Bala (Temporal Strength) for a planet.
        
        Kala Bala consists of:
        1. Natonnata Bala (Diurnal/Nocturnal Strength)
        2. Paksha Bala (Lunar Phase Strength)
        3. Tribhaga Bala (Division of Day Strength)
        4. Abda Bala (Yearly Strength)
        5. Masa Bala (Monthly Strength)
        6. Vara Bala (Weekday Strength)
        7. Hora Bala (Hourly Strength)
        8. Ayana Bala (Solstice Strength)
        9. Yuddha Bala (Planetary War Strength)
        
        Args:
            planet: Name of the planet
            
        Returns:
            Dictionary with Kala Bala components and total
        """
        # For MVP, we'll implement a simplified version of Kala Bala
        
        # 1. Natonnata Bala (Diurnal/Nocturnal Strength)
        natonnata_bala = self._calculate_natonnata_bala(planet)
        
        # 2. Paksha Bala (Lunar Phase Strength)
        paksha_bala = self._calculate_paksha_bala(planet)
        
        # 3. Tribhaga Bala (Division of Day Strength) - simplified
        tribhaga_bala = 15  # Default value for MVP
        
        # 4-7. Other temporal strengths - simplified for MVP
        other_temporal_strength = 30  # Default value for MVP
        
        # 8. Ayana Bala (Solstice Strength)
        ayana_bala = self._calculate_ayana_bala(planet)
        
        # 9. Yuddha Bala (Planetary War Strength)
        yuddha_bala = self._calculate_yuddha_bala(planet)
        
        # Calculate total Kala Bala
        total_kala_bala = (
            natonnata_bala +
            paksha_bala +
            tribhaga_bala +
            other_temporal_strength +
            ayana_bala +
            yuddha_bala
        )
        
        return {
            'natonnata_bala': natonnata_bala,
            'paksha_bala': paksha_bala,
            'tribhaga_bala': tribhaga_bala,
            'other_temporal_strength': other_temporal_strength,
            'ayana_bala': ayana_bala,
            'yuddha_bala': yuddha_bala,
            'total': total_kala_bala
        }
    
    def _calculate_natonnata_bala(self, planet):
        """
        Calculate Natonnata Bala (Diurnal/Nocturnal Strength).
        
        Diurnal planets (Sun, Jupiter) get strength during day.
        Nocturnal planets (Moon, Venus, Saturn) get strength during night.
        Dual planets (Mercury, Mars) get strength during dawn/dusk.
        
        Args:
            planet: Name of the planet
            
        Returns:
            Natonnata Bala value (0-60)
        """
        # Define planet types
        diurnal_planets = ['Sun', 'Jupiter']
        nocturnal_planets = ['Moon', 'Venus', 'Saturn']
        dual_planets = ['Mercury', 'Mars']
        
        # For MVP, we'll use a simplified approach
        # Determine if it's day or night based on Sun's position
        sun_longitude = self.planets['Sun']['longitude']
        ascendant_longitude = self.ascendant
        
        # If Sun is above horizon (houses 7-12), it's day
        sun_house = self.planets['Sun']['house']
        is_day = sun_house >= 7
        
        strength = 0
        
        if planet in diurnal_planets:
            strength = 60 if is_day else 0
        elif planet in nocturnal_planets:
            strength = 0 if is_day else 60
        elif planet in dual_planets:
            # Dual planets get half strength regardless
            strength = 30
            
        return strength
    
    def _calculate_paksha_bala(self, planet):
        """
        Calculate Paksha Bala (Lunar Phase Strength).
        
        Moon gets strength during Shukla Paksha (waxing phase).
        Other planets get strength based on their relationship with the Moon.
        
        Args:
            planet: Name of the planet
            
        Returns:
            Paksha Bala value (0-60)
        """
        # Calculate Moon phase
        sun_longitude = self.planets['Sun']['longitude']
        moon_longitude = self.planets['Moon']['longitude']
        
        # Calculate difference between Moon and Sun longitudes
        moon_sun_diff = (moon_longitude - sun_longitude) % 360
        
        # If difference is less than 180, it's Shukla Paksha (waxing)
        is_shukla_paksha = moon_sun_diff < 180
        
        # Calculate phase percentage (0-1)
        phase_percentage = moon_sun_diff / 180 if is_shukla_paksha else (360 - moon_sun_diff) / 180
        
        if planet == 'Moon':
            # Moon gets strength during Shukla Paksha
            return 60 * phase_percentage if is_shukla_paksha else 60 * (1 - phase_percentage)
        else:
            # For MVP, other planets get a default value
            return 30
    
    def _calculate_ayana_bala(self, planet):
        """
        Calculate Ayana Bala (Solstice Strength).
        
        Benefic planets (Jupiter, Venus, Mercury, Moon) get strength during Uttarayana.
        Malefic planets (Sun, Mars, Saturn) get strength during Dakshinayana.
        
        Args:
            planet: Name of the planet
            
        Returns:
            Ayana Bala value (0-30)
        """
        # Define planet types
        benefic_planets = ['Jupiter', 'Venus', 'Mercury', 'Moon']
        malefic_planets = ['Sun', 'Mars', 'Saturn']
        
        # For MVP, we'll use a simplified approach based on Sun's position
        sun_longitude = self.planets['Sun']['longitude']
        
        # If Sun is in Capricorn to Gemini (270-90 degrees), it's Uttarayana
        is_uttarayana = 270 <= sun_longitude or sun_longitude < 90
        
        if planet in benefic_planets:
            return 30 if is_uttarayana else 0
        elif planet in malefic_planets:
            return 0 if is_uttarayana else 30
        else:
            return 15  # Default for other planets
    
    def _calculate_yuddha_bala(self, planet):
        """
        Calculate Yuddha Bala (Planetary War Strength).
        
        When planets are within 1 degree of each other, they are in war.
        The winner gets additional strength.
        
        Args:
            planet: Name of the planet
            
        Returns:
            Yuddha Bala value (0-15)
        """
        # For MVP, we'll use a simplified approach
        planet_longitude = self.planets[planet]['longitude']
        
        # Check if planet is in war with any other planet
        for other_planet, other_data in self.planets.items():
            if other_planet == planet or other_planet in ['Rahu', 'Ketu']:
                continue
                
            other_longitude = other_data['longitude']
            
            # Calculate distance between planets
            distance = min(
                abs(planet_longitude - other_longitude),
                360 - abs(planet_longitude - other_longitude)
            )
            
            # If planets are within 1 degree, they are in war
            if distance <= 1:
                # For MVP, we'll assume the planet with higher longitude wins
                if planet_longitude > other_longitude:
                    return 15
                else:
                    return 0
                    
        # If not in war, return default value
        return 7.5
    
    def calculate_chesta_bala(self, planet):
        """
        Calculate Chesta Bala (Motional Strength) for a planet.
        
        Chesta Bala is based on the planet's motion:
        - Direct motion: Maximum strength
        - Retrograde: Medium strength
        - Combust: Minimum strength
        
        Args:
            planet: Name of the planet
            
        Returns:
            Dictionary with Chesta Bala value
        """
        # Skip Sun and Moon as they don't have retrograde motion
        if planet in ['Sun', 'Moon', 'Rahu', 'Ketu']:
            return {'total': 30}  # Default value
            
        planet_data = self.planets[planet]
        
        # Check if planet is retrograde
        is_retrograde = planet_data.get('is_retrograde', False)
        
        # Check if planet is combust
        is_combust = planet_data.get('is_combust', False)
        
        # Calculate strength based on motion
        if is_combust:
            strength = 15  # Minimum strength when combust
        elif is_retrograde:
            strength = 45  # Medium strength when retrograde
        else:
            strength = 60  # Maximum strength when direct
            
        return {'total': strength}
    
    def calculate_naisargika_bala(self, planet):
        """
        Calculate Naisargika Bala (Natural Strength) for a planet.
        
        Each planet has an inherent natural strength:
        - Saturn: 1.0 rupa
        - Mars: 0.85 rupa
        - Mercury: 0.7 rupa
        - Jupiter: 0.6 rupa
        - Venus: 0.5 rupa
        - Moon: 0.3 rupa
        - Sun: 0.4 rupa
        
        Args:
            planet: Name of the planet
            
        Returns:
            Dictionary with Naisargika Bala value
        """
        # Get natural strength of the planet
        natural_strength = self.NATURAL_STRENGTHS.get(planet, 0.5)
        
        # Convert to virupas (1 rupa = 60 virupas)
        strength = natural_strength * 60
        
        return {'total': strength}
    
    def calculate_drik_bala(self, planet):
        """
        Calculate Drik Bala (Aspectual Strength) for a planet.
        
        Drik Bala is based on the aspects between planets.
        Benefic aspects increase strength, malefic aspects decrease it.
        
        Args:
            planet: Name of the planet
            
        Returns:
            Dictionary with Drik Bala value
        """
        # Define benefic and malefic planets
        benefic_planets = ['Jupiter', 'Venus', 'Mercury', 'Moon']
        malefic_planets = ['Sun', 'Mars', 'Saturn', 'Rahu', 'Ketu']
        
        planet_longitude = self.planets[planet]['longitude']
        total_aspect_strength = 0
        
        # Check aspects from other planets
        for other_planet, other_data in self.planets.items():
            if other_planet == planet or other_planet in ['Rahu', 'Ketu']:
                continue
                
            other_longitude = other_data['longitude']
            
            # Calculate aspect angle
            aspect_angle = (other_longitude - planet_longitude) % 360
            
            # Define aspect strengths based on angle
            # Full aspect: 0°, 180° (opposition)
            # 3/4 aspect: 90°, 270° (square)
            # 1/2 aspect: 120°, 240° (trine)
            # 1/4 aspect: 60°, 300° (sextile)
            
            aspect_strength = 0
            
            # Check for full aspect (conjunction or opposition)
            if aspect_angle < 10 or abs(aspect_angle - 180) < 10:
                aspect_strength = 1.0
            # Check for square aspect
            elif abs(aspect_angle - 90) < 10 or abs(aspect_angle - 270) < 10:
                aspect_strength = 0.75
            # Check for trine aspect
            elif abs(aspect_angle - 120) < 10 or abs(aspect_angle - 240) < 10:
                aspect_strength = 0.5
            # Check for sextile aspect
            elif abs(aspect_angle - 60) < 10 or abs(aspect_angle - 300) < 10:
                aspect_strength = 0.25
                
            # Adjust strength based on whether the aspecting planet is benefic or malefic
            if other_planet in benefic_planets:
                total_aspect_strength += aspect_strength
            elif other_planet in malefic_planets:
                total_aspect_strength -= aspect_strength
                
        # Scale to virupas (0-60)
        # Maximum possible strength is when all 6 other planets give full benefic aspect
        # Minimum possible strength is when all 6 other planets give full malefic aspect
        scaled_strength = 30 + (total_aspect_strength * 5)
        
        # Ensure strength is within bounds
        strength = max(0, min(60, scaled_strength))
        
        return {'total': strength}
    
    def _get_required_strength(self, planet):
        """
        Get the required strength for a planet to be considered strong.
        
        Args:
            planet: Name of the planet
            
        Returns:
            Required strength in Rupas
        """
        required_strengths = {
            'Sun': 5,
            'Moon': 6,
            'Mars': 5,
            'Mercury': 7,
            'Jupiter': 6.5,
            'Venus': 5.5,
            'Saturn': 5
        }
        
        return required_strengths.get(planet, 5)
    
    def calculate_total_shadbala(self, planet):
        """
        Calculate the total Shadbala for a planet by combining all six types of strengths.
        
        Args:
            planet: Name of the planet
            
        Returns:
            Dictionary with all Shadbala components and total
        """
        # Calculate all six types of strengths
        sthana_bala = self.calculate_sthana_bala(planet)
        dig_bala = self.calculate_dig_bala(planet)
        kala_bala = self.calculate_kala_bala(planet)
        chesta_bala = self.calculate_chesta_bala(planet)
        naisargika_bala = self.calculate_naisargika_bala(planet)
        drik_bala = self.calculate_drik_bala(planet)
        
        # Calculate total Shadbala in virupas
        total_shadbala_virupas = (
            sthana_bala['total'] +
            dig_bala['total'] +
            kala_bala['total'] +
            chesta_bala['total'] +
            naisargika_bala['total'] +
            drik_bala['total']
        )
        
        # Convert to rupas (1 rupa = 60 virupas)
        total_shadbala_rupas = total_shadbala_virupas / 60
        
        # Get required strength for the planet
        required_strength = self._get_required_strength(planet)
        
        # Calculate Shadbala Pinda (relative strength)
        shadbala_pinda = total_shadbala_rupas / required_strength
        
        # Determine if the planet is strong or weak
        is_strong = shadbala_pinda >= 1
        
        return {
            'sthana_bala': sthana_bala,
            'dig_bala': dig_bala,
            'kala_bala': kala_bala,
            'chesta_bala': chesta_bala,
            'naisargika_bala': naisargika_bala,
            'drik_bala': drik_bala,
            'total_virupas': total_shadbala_virupas,
            'total_rupas': total_shadbala_rupas,
            'required_strength': required_strength,
            'shadbala_pinda': shadbala_pinda,
            'is_strong': is_strong
        }
    
    def calculate_all_shadbalas(self):
        """
        Calculate Shadbala for all planets.
        
        Returns:
            Dictionary with Shadbala results for all planets
        """
        results = {}
        
        # Calculate Shadbala for each planet
        for planet in self.PLANETS:
            if planet not in ['Rahu', 'Ketu']:  # Skip nodes for now
                results[planet] = self.calculate_total_shadbala(planet)
                
        return results
