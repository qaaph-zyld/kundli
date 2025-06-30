"""
Dasha Phala Generator
This module provides functionality for generating dasha phala (effects) in Vedic astrology.
"""
import logging
from typing import Dict, List, Optional, Any

from ...core.entities.dasha import DashaNode, DashaPhala
from ...core.entities.birth_chart import BirthChart
from .dasha_phala_data import (
    MAHADASHA_EFFECTS, 
    ANTARDASHA_EFFECTS, 
    HOUSE_BASED_EFFECTS,
    NAKSHATRA_EFFECTS
)

# Configure logging
logger = logging.getLogger(__name__)


class DashaPhalagenerator:
    """Class for generating dasha phala (effects) based on classical references."""
    
    def __init__(self):
        """Initialize the dasha phala generator."""
        logger.info("Initialized dasha phala generator")
    
    def generate_phala(self, dasha_node: DashaNode, birth_chart: BirthChart) -> DashaPhala:
        """
        Generate dasha phala (effects) for a dasha node.
        
        Args:
            dasha_node: The dasha node
            birth_chart: The birth chart
            
        Returns:
            DashaPhala: The dasha phala (effects)
        """
        planet = dasha_node.planet
        level = dasha_node.level
        
        # Generate effects based on level
        if level == 1:  # Mahadasha
            return self._generate_mahadasha_phala(planet, birth_chart)
        elif level == 2:  # Antardasha
            parent_planet = dasha_node.parent_planet if hasattr(dasha_node, 'parent_planet') else None
            return self._generate_antardasha_phala(planet, parent_planet, birth_chart)
        elif level == 3:  # Pratyantardasha
            # For simplicity, we'll use the same logic as antardasha for now
            parent_planet = dasha_node.parent_planet if hasattr(dasha_node, 'parent_planet') else None
            return self._generate_pratyantardasha_phala(planet, parent_planet, birth_chart)
        else:
            # Default case
            return DashaPhala(
                general="No specific effects available for this dasha level.",
                areas_of_influence=[],
                favorable_outcomes=[],
                challenging_outcomes=[],
                classical_references=[],
                remedial_measures=[]
            )
    
    def _generate_mahadasha_phala(self, planet: str, birth_chart: BirthChart) -> DashaPhala:
        """
        Generate mahadasha phala (effects).
        
        Args:
            planet: The planet
            birth_chart: The birth chart
            
        Returns:
            DashaPhala: The dasha phala (effects)
        """
        logger.info(f"Generating mahadasha phala for planet {planet}")
        
        # Get planet effects from reference data
        planet_effects = MAHADASHA_EFFECTS.get(planet, {})
        
        # Get planet house position
        house_position = self._get_planet_house(planet, birth_chart)
        house_effects = HOUSE_BASED_EFFECTS.get(house_position, "")
        
        # Get planet nakshatra
        nakshatra = self._get_planet_nakshatra(planet, birth_chart)
        nakshatra_effects = NAKSHATRA_EFFECTS.get(nakshatra, "")
        
        # Generate areas of influence
        areas_of_influence = self._generate_areas_of_influence(planet, house_position)
        
        # Generate favorable outcomes
        favorable_outcomes = self._generate_favorable_outcomes(planet, house_position, birth_chart)
        
        # Generate challenging outcomes
        challenging_outcomes = self._generate_challenging_outcomes(planet, house_position, birth_chart)
        
        # Generate classical references
        classical_references = [planet_effects.get("classical_reference", "")]
        
        # Generate remedial measures
        remedial_measures = [planet_effects.get("remedial_measures", "")]
        
        # Combine all effects
        general = f"{planet_effects.get('general', '')} {house_effects} {nakshatra_effects}"
        
        return DashaPhala(
            general=general,
            areas_of_influence=areas_of_influence,
            favorable_outcomes=favorable_outcomes,
            challenging_outcomes=challenging_outcomes,
            classical_references=classical_references,
            remedial_measures=remedial_measures
        )
    
    def _generate_antardasha_phala(self, planet: str, parent_planet: Optional[str], birth_chart: BirthChart) -> DashaPhala:
        """
        Generate antardasha phala (effects).
        
        Args:
            planet: The planet
            parent_planet: The parent planet (mahadasha lord)
            birth_chart: The birth chart
            
        Returns:
            DashaPhala: The dasha phala (effects)
        """
        logger.info(f"Generating antardasha phala for planet {planet} under {parent_planet}")
        
        # If parent_planet is None, use a default approach
        if parent_planet is None:
            return self._generate_mahadasha_phala(planet, birth_chart)
        
        # Get combination effects from reference data
        combination_effects = ANTARDASHA_EFFECTS.get(parent_planet, {}).get(planet, "")
        
        # Get planet house position
        house_position = self._get_planet_house(planet, birth_chart)
        house_effects = HOUSE_BASED_EFFECTS.get(house_position, "")
        
        # Generate areas of influence
        areas_of_influence = self._generate_areas_of_influence(planet, house_position)
        
        # Generate favorable outcomes
        favorable_outcomes = self._generate_favorable_outcomes(planet, house_position, birth_chart)
        
        # Generate challenging outcomes
        challenging_outcomes = self._generate_challenging_outcomes(planet, house_position, birth_chart)
        
        # Generate classical references
        classical_references = [f"Effects of {planet} antardasha in {parent_planet} mahadasha: {combination_effects}"]
        
        # Generate remedial measures
        remedial_measures = [MAHADASHA_EFFECTS.get(planet, {}).get("remedial_measures", "")]
        
        # Combine all effects
        general = f"This is the {planet} antardasha in {parent_planet} mahadasha. {combination_effects} {house_effects}"
        
        return DashaPhala(
            general=general,
            areas_of_influence=areas_of_influence,
            favorable_outcomes=favorable_outcomes,
            challenging_outcomes=challenging_outcomes,
            classical_references=classical_references,
            remedial_measures=remedial_measures
        )
    
    def _generate_pratyantardasha_phala(self, planet: str, parent_planet: Optional[str], birth_chart: BirthChart) -> DashaPhala:
        """
        Generate pratyantardasha phala (effects).
        
        Args:
            planet: The planet
            parent_planet: The parent planet (antardasha lord)
            birth_chart: The birth chart
            
        Returns:
            DashaPhala: The dasha phala (effects)
        """
        logger.info(f"Generating pratyantardasha phala for planet {planet} under {parent_planet}")
        
        # For simplicity, we'll use a similar approach to antardasha for now
        # In a full implementation, this would be more detailed and specific
        
        # If parent_planet is None, use a default approach
        if parent_planet is None:
            return self._generate_mahadasha_phala(planet, birth_chart)
        
        # Get planet house position
        house_position = self._get_planet_house(planet, birth_chart)
        house_effects = HOUSE_BASED_EFFECTS.get(house_position, "")
        
        # Generate areas of influence
        areas_of_influence = self._generate_areas_of_influence(planet, house_position)
        
        # Generate favorable outcomes
        favorable_outcomes = self._generate_favorable_outcomes(planet, house_position, birth_chart)
        
        # Generate challenging outcomes
        challenging_outcomes = self._generate_challenging_outcomes(planet, house_position, birth_chart)
        
        # Generate classical references
        classical_references = [f"Effects of {planet} pratyantardasha under {parent_planet} antardasha."]
        
        # Generate remedial measures
        remedial_measures = [MAHADASHA_EFFECTS.get(planet, {}).get("remedial_measures", "")]
        
        # Combine all effects
        general = f"This is the {planet} pratyantardasha under {parent_planet} antardasha. {house_effects}"
        
        return DashaPhala(
            general=general,
            areas_of_influence=areas_of_influence,
            favorable_outcomes=favorable_outcomes,
            challenging_outcomes=challenging_outcomes,
            classical_references=classical_references,
            remedial_measures=remedial_measures
        )
    
    def _get_planet_house(self, planet: str, birth_chart: BirthChart) -> int:
        """
        Get the house position of a planet.
        
        Args:
            planet: The planet
            birth_chart: The birth chart
            
        Returns:
            int: The house position (1-12)
        """
        # Default to 1st house if not found
        default_house = 1
        
        # Get planet data from birth chart
        planet_data = birth_chart.planets.get(planet, {})
        
        # Get house position
        house = planet_data.get("house", default_house)
        
        return house
    
    def _get_planet_nakshatra(self, planet: str, birth_chart: BirthChart) -> str:
        """
        Get the nakshatra of a planet.
        
        Args:
            planet: The planet
            birth_chart: The birth chart
            
        Returns:
            str: The nakshatra name
        """
        # Default nakshatra
        default_nakshatra = "Ashwini"
        
        # Get planet data from birth chart
        planet_data = birth_chart.planets.get(planet, {})
        
        # Get nakshatra
        nakshatra = planet_data.get("nakshatra", default_nakshatra)
        
        return nakshatra
    
    def _generate_areas_of_influence(self, planet: str, house_position: int) -> List[str]:
        """
        Generate areas of influence based on planet and house position.
        
        Args:
            planet: The planet
            house_position: The house position
            
        Returns:
            List[str]: Areas of influence
        """
        # Planet significations
        planet_areas = {
            "Su": ["Authority", "Father", "Government", "Health", "Self-confidence"],
            "Mo": ["Mind", "Mother", "Public", "Emotions", "Comfort"],
            "Ma": ["Energy", "Siblings", "Property", "Courage", "Technical skills"],
            "Me": ["Communication", "Business", "Education", "Intelligence", "Analytical skills"],
            "Ju": ["Wisdom", "Children", "Higher education", "Spirituality", "Wealth"],
            "Ve": ["Relationships", "Marriage", "Luxury", "Arts", "Comforts"],
            "Sa": ["Longevity", "Career", "Discipline", "Hard work", "Delays"],
            "Ra": ["Foreign matters", "Unconventional success", "Ambition", "Obsession", "Technology"],
            "Ke": ["Spirituality", "Mysticism", "Detachment", "Liberation", "Past life karma"]
        }
        
        # House significations
        house_areas = {
            1: ["Self", "Personality", "Health", "Life direction"],
            2: ["Wealth", "Family", "Speech", "Early education"],
            3: ["Courage", "Siblings", "Short journeys", "Communication"],
            4: ["Mother", "Home", "Property", "Education", "Happiness"],
            5: ["Children", "Creativity", "Intelligence", "Speculative gains"],
            6: ["Enemies", "Debts", "Diseases", "Service"],
            7: ["Spouse", "Business partnerships", "Foreign travel", "Public relations"],
            8: ["Longevity", "Obstacles", "Occult knowledge", "Sudden events"],
            9: ["Fortune", "Higher education", "Spirituality", "Long journeys"],
            10: ["Career", "Authority", "Father", "Social status"],
            11: ["Gains", "Elder siblings", "Friends", "Fulfillment of desires"],
            12: ["Expenses", "Losses", "Foreign residence", "Spiritual liberation"]
        }
        
        # Combine planet and house areas
        planet_significations = planet_areas.get(planet, [])
        house_significations = house_areas.get(house_position, [])
        
        # Return combined areas of influence
        return planet_significations + house_significations
    
    def _generate_favorable_outcomes(self, planet: str, house_position: int, birth_chart: BirthChart) -> List[str]:
        """
        Generate favorable outcomes based on planet and house position.
        
        Args:
            planet: The planet
            house_position: The house position
            birth_chart: The birth chart
            
        Returns:
            List[str]: Favorable outcomes
        """
        # Get planet effects from reference data
        planet_effects = MAHADASHA_EFFECTS.get(planet, {})
        favorable = planet_effects.get("favorable", "")
        
        # Split into list items
        favorable_list = favorable.split(", ")
        
        # Add house-specific favorable outcomes
        if house_position in [1, 5, 9]:  # Trine houses
            favorable_list.append("Success in personal endeavors")
            favorable_list.append("Spiritual growth")
            favorable_list.append("Good fortune")
        elif house_position in [2, 6, 10]:  # Success houses
            favorable_list.append("Financial gains")
            favorable_list.append("Career advancement")
            favorable_list.append("Professional recognition")
        elif house_position in [3, 7, 11]:  # Upachaya houses
            favorable_list.append("Growth through effort")
            favorable_list.append("Successful partnerships")
            favorable_list.append("Fulfillment of desires")
        
        return favorable_list
    
    def _generate_challenging_outcomes(self, planet: str, house_position: int, birth_chart: BirthChart) -> List[str]:
        """
        Generate challenging outcomes based on planet and house position.
        
        Args:
            planet: The planet
            house_position: The house position
            birth_chart: The birth chart
            
        Returns:
            List[str]: Challenging outcomes
        """
        # Get planet effects from reference data
        planet_effects = MAHADASHA_EFFECTS.get(planet, {})
        challenging = planet_effects.get("challenging", "")
        
        # Split into list items
        challenging_list = challenging.split(", ")
        
        # Add house-specific challenging outcomes
        if house_position in [6, 8, 12]:  # Dusthana houses
            challenging_list.append("Obstacles and delays")
            challenging_list.append("Health issues")
            challenging_list.append("Unexpected expenses")
        elif house_position in [4, 7, 10]:  # Kendra houses with potential challenges
            challenging_list.append("Pressure and responsibilities")
            challenging_list.append("Relationship tensions")
            challenging_list.append("Work-related stress")
        
        return challenging_list
