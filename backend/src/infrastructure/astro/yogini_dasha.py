"""
Yogini Dasha Calculator
This module provides functionality for calculating Yogini dashas in Vedic astrology.
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple

from ...core.entities.dasha import DashaLevel, DashaNode
from ...core.entities.birth_chart import BirthChart

# Configure logging
logger = logging.getLogger(__name__)


class YoginiDasha:
    """Class for calculating Yogini dasha."""
    
    # Yogini dasha constants
    TOTAL_YEARS = 36.0
    
    # Planet order and years (8-year cycle)
    PLANET_ORDER = ["Ma", "Me", "Sa", "Mo", "Ve", "Su", "Ra", "Ju"]
    PLANET_YEARS = {"Ma": 1, "Me": 2, "Sa": 3, "Mo": 4, "Ve": 5, "Su": 6, "Ra": 7, "Ju": 8}
    
    # Yogini names corresponding to planets
    YOGINI_NAMES = {
        "Ma": "Mangala",
        "Me": "Pingala",
        "Sa": "Dhanya",
        "Mo": "Bhramari",
        "Ve": "Bhadrika",
        "Su": "Ulka",
        "Ra": "Siddha",
        "Ju": "Sankata"
    }
    
    # Moon's nakshatra determines starting Yogini
    # Mapping of nakshatra to starting planet
    NAKSHATRA_TO_PLANET = {
        0: "Ma",   # Ashwini -> Mars
        1: "Me",   # Bharani -> Mercury
        2: "Sa",   # Krittika -> Saturn
        3: "Mo",   # Rohini -> Moon
        4: "Ve",   # Mrigashira -> Venus
        5: "Su",   # Ardra -> Sun
        6: "Ra",   # Punarvasu -> Rahu
        7: "Ju",   # Pushya -> Jupiter
        8: "Ma",   # Ashlesha -> Mars
        9: "Me",   # Magha -> Mercury
        10: "Sa",  # Purva Phalguni -> Saturn
        11: "Mo",  # Uttara Phalguni -> Moon
        12: "Ve",  # Hasta -> Venus
        13: "Su",  # Chitra -> Sun
        14: "Ra",  # Swati -> Rahu
        15: "Ju",  # Vishakha -> Jupiter
        16: "Ma",  # Anuradha -> Mars
        17: "Me",  # Jyeshtha -> Mercury
        18: "Sa",  # Mula -> Saturn
        19: "Mo",  # Purva Ashadha -> Moon
        20: "Ve",  # Uttara Ashadha -> Venus
        21: "Su",  # Shravana -> Sun
        22: "Ra",  # Dhanishta -> Rahu
        23: "Ju",  # Shatabhisha -> Jupiter
        24: "Ma",  # Purva Bhadrapada -> Mars
        25: "Me",  # Uttara Bhadrapada -> Mercury
        26: "Sa"   # Revati -> Saturn
    }
    
    def __init__(self):
        """Initialize the Yogini dasha calculator."""
        logger.info("Initialized Yogini dasha calculator")
    
    def calculate(self, birth_chart: BirthChart) -> Tuple[List[DashaNode], Dict[str, DashaLevel]]:
        """
        Calculate Yogini dasha for a birth chart.
        
        Args:
            birth_chart: The birth chart
            
        Returns:
            Tuple[List[DashaNode], Dict[str, DashaLevel]]: The dasha tree and current levels
        """
        logger.info(f"Calculating Yogini dasha for birth chart {birth_chart.id}")
        
        # Get Moon's longitude
        moon_longitude = birth_chart.planets.get("Mo", {}).get("longitude", 0.0)
        
        # Calculate nakshatra index (0-26)
        nakshatra_span = 13 + (1/3)  # 13°20' per nakshatra
        nakshatra_index = int(moon_longitude / nakshatra_span)
        
        # Get starting planet based on nakshatra
        starting_planet = self.NAKSHATRA_TO_PLANET[nakshatra_index]
        
        # Calculate birth date
        birth_date = datetime.fromisoformat(birth_chart.date_time.replace('Z', '+00:00'))
        
        # Calculate mahadasha periods
        mahadasha_periods = self._calculate_mahadasha_periods(birth_date, starting_planet)
        
        # Build dasha tree
        dasha_tree = self._build_dasha_tree(mahadasha_periods, birth_date)
        
        # Get current dasha levels
        current_levels = self._get_current_dasha_levels(dasha_tree, datetime.utcnow())
        
        return dasha_tree, current_levels
    
    def _calculate_mahadasha_periods(self, birth_date: datetime, first_lord: str) -> List[Dict[str, Any]]:
        """
        Calculate mahadasha periods.
        
        Args:
            birth_date: Birth date
            first_lord: First dasha lord
            
        Returns:
            List[Dict[str, Any]]: Mahadasha periods
        """
        # Find index of first lord
        first_index = self.PLANET_ORDER.index(first_lord)
        
        # Initialize periods
        periods = []
        current_date = birth_date
        
        # Calculate periods for all planets in order (4 cycles = 36 years)
        for cycle in range(4):
            for i in range(8):
                # Get planet index (circular)
                planet_index = (first_index + i) % 8
                planet = self.PLANET_ORDER[planet_index]
                
                # Get years for planet
                years = self.PLANET_YEARS[planet]
                
                # Calculate end date
                end_date = current_date + timedelta(days=years * 365.25)
                
                # Add period
                periods.append({
                    "planet": planet,
                    "start_date": current_date,
                    "end_date": end_date,
                    "duration_years": years,
                    "yogini": self.YOGINI_NAMES[planet]
                })
                
                # Update current date
                current_date = end_date
        
        return periods
    
    def _build_dasha_tree(self, mahadasha_periods: List[Dict[str, Any]], birth_date: datetime) -> List[DashaNode]:
        """
        Build dasha tree.
        
        Args:
            mahadasha_periods: Mahadasha periods
            birth_date: Birth date
            
        Returns:
            List[DashaNode]: Dasha tree
        """
        # Initialize tree
        tree = []
        
        # Build tree for each mahadasha
        for mahadasha in mahadasha_periods:
            # Skip mahadashas that ended before birth
            if mahadasha["end_date"] < birth_date:
                continue
            
            # Create mahadasha node
            mahadasha_node = DashaNode(
                planet=mahadasha["planet"],
                start_date=mahadasha["start_date"],
                end_date=mahadasha["end_date"],
                duration_years=mahadasha["duration_years"],
                level=1,
                children=[]
            )
            
            # Calculate antardashas for this mahadasha
            antardashas = self._calculate_antardashas(
                mahadasha["planet"],
                mahadasha["start_date"],
                mahadasha["duration_years"]
            )
            
            # Add antardashas to mahadasha
            for antardasha in antardashas:
                # Skip antardashas that ended before birth
                if antardasha["end_date"] < birth_date:
                    continue
                
                # Create antardasha node
                antardasha_node = DashaNode(
                    planet=antardasha["planet"],
                    start_date=antardasha["start_date"],
                    end_date=antardasha["end_date"],
                    duration_years=antardasha["duration_years"],
                    level=2,
                    children=[]
                )
                
                # Calculate pratyantardashas for this antardasha
                pratyantardashas = self._calculate_pratyantardashas(
                    mahadasha["planet"],
                    antardasha["planet"],
                    antardasha["start_date"],
                    antardasha["duration_years"]
                )
                
                # Add pratyantardashas to antardasha
                for pratyantardasha in pratyantardashas:
                    # Skip pratyantardashas that ended before birth
                    if pratyantardasha["end_date"] < birth_date:
                        continue
                    
                    # Create pratyantardasha node
                    pratyantardasha_node = DashaNode(
                        planet=pratyantardasha["planet"],
                        start_date=pratyantardasha["start_date"],
                        end_date=pratyantardasha["end_date"],
                        duration_years=pratyantardasha["duration_years"],
                        level=3,
                        children=[]
                    )
                    
                    # Add pratyantardasha to antardasha
                    antardasha_node.children.append(pratyantardasha_node)
                
                # Add antardasha to mahadasha
                mahadasha_node.children.append(antardasha_node)
            
            # Add mahadasha to tree
            tree.append(mahadasha_node)
        
        return tree
    
    def _calculate_antardashas(self, mahadasha_lord: str, start_date: datetime, mahadasha_years: float) -> List[Dict[str, Any]]:
        """
        Calculate antardashas for a mahadasha.
        
        Args:
            mahadasha_lord: Mahadasha lord
            start_date: Start date
            mahadasha_years: Mahadasha years
            
        Returns:
            List[Dict[str, Any]]: Antardasha periods
        """
        # Find index of mahadasha lord
        lord_index = self.PLANET_ORDER.index(mahadasha_lord)
        
        # Initialize periods
        periods = []
        current_date = start_date
        
        # Calculate periods for all planets in order
        for i in range(8):
            # Get planet index (circular)
            planet_index = (lord_index + i) % 8
            planet = self.PLANET_ORDER[planet_index]
            
            # Calculate years for antardasha
            years = (self.PLANET_YEARS[planet] / self.TOTAL_YEARS) * mahadasha_years
            
            # Calculate end date
            end_date = current_date + timedelta(days=years * 365.25)
            
            # Add period
            periods.append({
                "planet": planet,
                "start_date": current_date,
                "end_date": end_date,
                "duration_years": years
            })
            
            # Update current date
            current_date = end_date
        
        return periods
    
    def _calculate_pratyantardashas(
        self, 
        mahadasha_lord: str, 
        antardasha_lord: str, 
        start_date: datetime, 
        antardasha_years: float
    ) -> List[Dict[str, Any]]:
        """
        Calculate pratyantardashas for an antardasha.
        
        Args:
            mahadasha_lord: Mahadasha lord
            antardasha_lord: Antardasha lord
            start_date: Start date
            antardasha_years: Antardasha years
            
        Returns:
            List[Dict[str, Any]]: Pratyantardasha periods
        """
        # Find index of antardasha lord
        lord_index = self.PLANET_ORDER.index(antardasha_lord)
        
        # Initialize periods
        periods = []
        current_date = start_date
        
        # Calculate periods for all planets in order
        for i in range(8):
            # Get planet index (circular)
            planet_index = (lord_index + i) % 8
            planet = self.PLANET_ORDER[planet_index]
            
            # Calculate years for pratyantardasha
            years = (self.PLANET_YEARS[planet] / self.TOTAL_YEARS) * antardasha_years
            
            # Calculate end date
            end_date = current_date + timedelta(days=years * 365.25)
            
            # Add period
            periods.append({
                "planet": planet,
                "start_date": current_date,
                "end_date": end_date,
                "duration_years": years
            })
            
            # Update current date
            current_date = end_date
        
        return periods
    
    def _get_current_dasha_levels(self, dasha_tree: List[DashaNode], current_date: datetime) -> Dict[str, DashaLevel]:
        """
        Get current dasha levels.
        
        Args:
            dasha_tree: Dasha tree
            current_date: Current date
            
        Returns:
            Dict[str, DashaLevel]: Current dasha levels
        """
        # Initialize result
        result = {}
        
        # Find current mahadasha
        current_mahadasha = None
        for mahadasha in dasha_tree:
            if mahadasha.start_date <= current_date <= mahadasha.end_date:
                current_mahadasha = mahadasha
                break
        
        # If no current mahadasha found, return empty result
        if not current_mahadasha:
            return result
        
        # Add current mahadasha to result
        result["mahadasha"] = DashaLevel(
            planet=current_mahadasha.planet,
            start_date=current_mahadasha.start_date,
            end_date=current_mahadasha.end_date,
            duration_years=current_mahadasha.duration_years,
            level=1
        )
        
        # Find current antardasha
        current_antardasha = None
        for antardasha in current_mahadasha.children:
            if antardasha.start_date <= current_date <= antardasha.end_date:
                current_antardasha = antardasha
                break
        
        # If no current antardasha found, return result with just mahadasha
        if not current_antardasha:
            return result
        
        # Add current antardasha to result
        result["antardasha"] = DashaLevel(
            planet=current_antardasha.planet,
            start_date=current_antardasha.start_date,
            end_date=current_antardasha.end_date,
            duration_years=current_antardasha.duration_years,
            level=2,
            parent_planet=current_mahadasha.planet
        )
        
        # Find current pratyantardasha
        current_pratyantardasha = None
        for pratyantardasha in current_antardasha.children:
            if pratyantardasha.start_date <= current_date <= pratyantardasha.end_date:
                current_pratyantardasha = pratyantardasha
                break
        
        # If no current pratyantardasha found, return result with mahadasha and antardasha
        if not current_pratyantardasha:
            return result
        
        # Add current pratyantardasha to result
        result["pratyantardasha"] = DashaLevel(
            planet=current_pratyantardasha.planet,
            start_date=current_pratyantardasha.start_date,
            end_date=current_pratyantardasha.end_date,
            duration_years=current_pratyantardasha.duration_years,
            level=3,
            parent_planet=current_antardasha.planet
        )
        
        return result
