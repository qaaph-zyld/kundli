"""
Ashtakavarga Module for Vedic Astrology Calculations

This module implements the Ashtakavarga system, a key Vedic astrology technique
for evaluating planetary and house strengths through bindu (beneficial point) calculations.

Key components:
1. Prastarashtakavarga: Individual ashtakavarga tables for each of the 7 planets
2. Sarvashtakavarga: Combined table showing total bindus from all planets
3. Bindu calculations: Each planet contributes a bindu (1) or not (0) to each house
   based on specific rules from classical Parashari texts
"""

class AshtakavargaCalculator:
    """
    Calculator for Ashtakavarga system in Vedic astrology.
    
    This class implements the traditional Parashari rules for calculating
    bindus (beneficial points) in the Ashtakavarga system.
    """
    
    # Classical benefic positions for each planet when viewed from different houses
    # Format: planet: [list of benefic houses when viewed from 1st house, 2nd house, ..., 12th house]
    # These are the traditional Parashari rules for bindu contributions
    BENEFIC_POSITIONS = {
        'Sun': [1, 2, 4, 7, 8, 9, 10, 11],
        'Moon': [3, 6, 10, 11],
        'Mars': [1, 2, 4, 7, 8, 9, 10, 11],
        'Mercury': [1, 3, 5, 6, 9, 10, 11, 12],
        'Jupiter': [2, 5, 6, 7, 9, 10, 11],
        'Venus': [1, 2, 3, 4, 5, 8, 9, 11, 12],
        'Saturn': [3, 5, 6, 10, 11, 12],
        'Ascendant': [1, 3, 4, 7, 10, 11]
    }
    
    # Benefic positions for each planet from different planets
    # Format: contributing_planet: {viewed_from_planet: [list of benefic houses]}
    PLANETARY_BENEFIC_POSITIONS = {
        'Sun': {
            'Sun': [3, 6, 10, 11],
            'Moon': [3, 6, 10, 11],
            'Mars': [3, 6, 10, 11],
            'Mercury': [5, 6, 9, 11, 12],
            'Jupiter': [5, 7, 9, 11],
            'Venus': [6, 7, 12],
            'Saturn': [1, 2, 4, 7, 8, 10, 11],
            'Ascendant': [3, 6, 10, 11]
        },
        'Moon': {
            'Sun': [3, 6, 10, 11],
            'Moon': [1, 3, 6, 7, 10, 11],
            'Mars': [2, 3, 5, 6, 9, 10, 11],
            'Mercury': [1, 3, 4, 5, 7, 8, 10, 11],
            'Jupiter': [1, 4, 7, 8, 10, 11],
            'Venus': [3, 4, 5, 7, 9, 10, 11],
            'Saturn': [3, 5, 6, 11],
            'Ascendant': [3, 6, 10, 11]
        },
        'Mars': {
            'Sun': [3, 5, 6, 10, 11],
            'Moon': [3, 6, 11],
            'Mars': [1, 3, 6, 10, 11],
            'Mercury': [3, 5, 6, 11],
            'Jupiter': [6, 10, 11, 12],
            'Venus': [6, 8, 11, 12],
            'Saturn': [1, 4, 7, 8, 9, 10, 11],
            'Ascendant': [1, 3, 6, 10, 11]
        },
        'Mercury': {
            'Sun': [5, 6, 9, 11, 12],
            'Moon': [2, 4, 6, 8, 10, 11],
            'Mars': [1, 2, 4, 7, 8, 9, 10, 11],
            'Mercury': [1, 3, 5, 6, 9, 10, 11, 12],
            'Jupiter': [6, 8, 11, 12],
            'Venus': [1, 2, 3, 4, 5, 8, 9, 11],
            'Saturn': [1, 2, 4, 7, 8, 9, 10, 11],
            'Ascendant': [1, 2, 4, 7, 8, 9, 10, 11]
        },
        'Jupiter': {
            'Sun': [1, 2, 3, 4, 7, 8, 9, 10, 11],
            'Moon': [2, 5, 7, 9, 11],
            'Mars': [1, 2, 4, 7, 8, 10, 11],
            'Mercury': [1, 2, 4, 5, 6, 9, 10, 11],
            'Jupiter': [1, 2, 3, 4, 7, 8, 10, 11],
            'Venus': [2, 5, 6, 9, 10, 11],
            'Saturn': [3, 5, 6, 12],
            'Ascendant': [1, 2, 4, 5, 6, 7, 9, 10, 11]
        },
        'Venus': {
            'Sun': [8, 11, 12],
            'Moon': [1, 2, 3, 4, 5, 8, 9, 11, 12],
            'Mars': [1, 2, 3, 4, 5, 8, 9, 11, 12],
            'Mercury': [1, 2, 3, 4, 5, 8, 9, 10, 11],
            'Jupiter': [5, 8, 9, 10, 11],
            'Venus': [1, 2, 3, 4, 5, 8, 9, 11, 12],
            'Saturn': [3, 4, 5, 8, 9, 10, 11],
            'Ascendant': [1, 2, 3, 4, 5, 8, 9, 11]
        },
        'Saturn': {
            'Sun': [1, 2, 4, 7, 8, 10, 11],
            'Moon': [3, 6, 11],
            'Mars': [3, 5, 6, 10, 11, 12],
            'Mercury': [6, 8, 9, 10, 11, 12],
            'Jupiter': [5, 6, 11, 12],
            'Venus': [6, 11, 12],
            'Saturn': [3, 5, 6, 11],
            'Ascendant': [3, 5, 6, 11]
        }
    }
    
    def __init__(self, chart):
        """
        Initialize AshtakavargaCalculator with a VedicCalculator chart
        
        Args:
            chart: An instance of VedicCalculator containing the birth chart data
        """
        self.chart = chart
        self.prastarashtakavarga = {}  # Individual ashtakavarga tables
        self.sarvashtakavarga = {}     # Combined ashtakavarga table
        
        # Initialize data structures
        self._initialize_ashtakavarga()
    
    def _initialize_ashtakavarga(self):
        """Initialize the ashtakavarga data structures"""
        # Initialize individual ashtakavarga tables for each planet
        for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
            self.prastarashtakavarga[planet] = {house: 0 for house in range(1, 13)}
        
        # Initialize sarvashtakavarga (combined table)
        self.sarvashtakavarga = {house: 0 for house in range(1, 13)}
    
    def calculate_ashtakavarga(self):
        """
        Calculate the complete Ashtakavarga system
        
        This calculates both the individual planet ashtakavarga (prastarashtakavarga)
        and the combined ashtakavarga (sarvashtakavarga)
        
        Returns:
            Dict containing prastarashtakavarga and sarvashtakavarga
        """
        # Calculate individual ashtakavarga for each planet
        for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
            self._calculate_planet_ashtakavarga(planet)
        
        # Calculate sarvashtakavarga (sum of all individual ashtakavargas)
        for house in range(1, 13):
            for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
                self.sarvashtakavarga[house] += self.prastarashtakavarga[planet][house]
        
        return {
            'prastarashtakavarga': self.prastarashtakavarga,
            'sarvashtakavarga': self.sarvashtakavarga
        }
    
    def _calculate_planet_ashtakavarga(self, planet):
        """
        Calculate the ashtakavarga for a specific planet
        
        Args:
            planet: The planet to calculate ashtakavarga for
        """
        # Get the house position of the planet
        if planet not in self.chart.planets:
            return
        
        planet_house = self.chart.planets[planet]['house']
        
        # Calculate bindu contributions from each planet and the ascendant
        for contributor in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Ascendant']:
            # For ascendant, we use a special case
            if contributor == 'Ascendant':
                contributor_house = 1  # Ascendant is always in the 1st house
            else:
                # Skip if contributor planet is not in the chart
                if contributor not in self.chart.planets:
                    continue
                contributor_house = self.chart.planets[contributor]['house']
            
            # Calculate bindu for each house from this contributor
            for house in range(1, 13):
                # Calculate the relative house position from the contributor
                relative_house = ((house - contributor_house) % 12) + 1
                
                # Check if this relative house position gets a bindu
                if contributor == 'Ascendant':
                    # Use the ascendant's benefic positions
                    if relative_house in self.BENEFIC_POSITIONS['Ascendant']:
                        self.prastarashtakavarga[planet][house] += 1
                else:
                    # Use the planetary benefic positions
                    if relative_house in self.PLANETARY_BENEFIC_POSITIONS[planet].get(contributor, []):
                        self.prastarashtakavarga[planet][house] += 1
    
    def get_planet_ashtakavarga(self, planet):
        """
        Get the ashtakavarga for a specific planet
        
        Args:
            planet: The planet to get ashtakavarga for
            
        Returns:
            Dict with house numbers as keys and bindu counts as values
        """
        if planet not in self.prastarashtakavarga:
            return {}
        return self.prastarashtakavarga[planet]
    
    def get_sarvashtakavarga(self):
        """
        Get the sarvashtakavarga (combined ashtakavarga)
        
        Returns:
            Dict with house numbers as keys and total bindu counts as values
        """
        return self.sarvashtakavarga
    
    def get_planet_bindu_score(self, planet):
        """
        Get the total bindu score for a planet across all houses
        
        Args:
            planet: The planet to get the bindu score for
            
        Returns:
            Total bindu score (int)
        """
        if planet not in self.prastarashtakavarga:
            return 0
        return sum(self.prastarashtakavarga[planet].values())
    
    def get_house_bindu_score(self, house):
        """
        Get the total bindu score for a house from all planets
        
        Args:
            house: The house number to get the bindu score for
            
        Returns:
            Total bindu score (int)
        """
        if house not in self.sarvashtakavarga:
            return 0
        return self.sarvashtakavarga[house]
    
    def get_transit_effectiveness(self, planet, house):
        """
        Calculate the effectiveness of a planet transiting through a house
        
        Args:
            planet: The transiting planet
            house: The house being transited
            
        Returns:
            Effectiveness score (int) - higher is better
        """
        if planet not in self.prastarashtakavarga or house not in self.prastarashtakavarga[planet]:
            return 0
        return self.prastarashtakavarga[planet][house]
    
    def get_kakshya_position(self, planet, house):
        """
        Get the kakshya (sub-division) position of a planet in a house
        
        In Ashtakavarga, each house is divided into 8 kakshyas (sub-divisions),
        each ruled by a planet or the ascendant.
        
        Args:
            planet: The planet to check
            house: The house number
            
        Returns:
            Dict with kakshya information
        """
        if planet not in self.chart.planets:
            return {}
        
        # Get the longitude of the planet within the house
        planet_longitude = self.chart.planets[planet]['longitude']
        house_start = (house - 1) * 30  # Each house is 30 degrees
        position_in_house = (planet_longitude - house_start) % 30
        
        # Each kakshya is 3.75 degrees (30/8)
        kakshya_size = 30 / 8
        kakshya_num = int(position_in_house / kakshya_size) + 1
        
        # Kakshya rulers in traditional order
        kakshya_rulers = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Ascendant']
        kakshya_ruler = kakshya_rulers[kakshya_num - 1]
        
        return {
            'kakshya_number': kakshya_num,
            'kakshya_ruler': kakshya_ruler,
            'position_in_kakshya': position_in_house % kakshya_size,
            'kakshya_size': kakshya_size
        }
