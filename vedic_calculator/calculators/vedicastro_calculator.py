"""
VedicAstro calculator implementation.
This module provides the primary calculator using the vedicastro library.
"""
import logging
from datetime import datetime
from typing import Dict, List, Any

from ..calculators.protocol import AstronomicalCalculator, PlanetaryData, HouseData, AspectData, Coordinates

# Setup logging
logger = logging.getLogger(__name__)

class VedicastroCalculator(AstronomicalCalculator):
    """Implementation of the AstronomicalCalculator protocol using vedicastro."""
    
    def __init__(self):
        """Initialize the calculator with the vedicastro library."""
        try:
            # Import vedicastro here to avoid global dependency
            # This allows the system to work even if vedicastro is not available
            from vedicastro import Chart
            self.Chart = Chart
            self.available = True
            logger.info("VedicastroCalculator initialized successfully")
        except ImportError:
            self.available = False
            logger.warning("vedicastro library not available")
    
    def calculate_planetary_positions(self, dt: datetime, coordinates: Coordinates) -> PlanetaryData:
        """Calculate planetary positions using vedicastro."""
        if not self.available:
            raise RuntimeError("vedicastro library not available")
        
        try:
            # Create a chart using vedicastro
            chart = self.Chart(dt, coordinates.latitude, coordinates.longitude)
            
            # Extract planetary positions
            planets = {}
            for planet_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
                planet = getattr(chart, planet_name.lower())
                planets[planet_name] = {
                    "longitude": planet.longitude,
                    "latitude": planet.latitude if hasattr(planet, "latitude") else 0.0,
                    "speed": planet.daily_motion if hasattr(planet, "daily_motion") else 0.0,
                    "sign": planet.sign,
                    "nakshatra": planet.nakshatra,
                    "pada": planet.pada,
                    "house": planet.house,
                    "retrograde": planet.is_retrograde if hasattr(planet, "is_retrograde") else False,
                    "degree": planet.longitude % 30,
                    "formatted_degree": planet.formatted_degree if hasattr(planet, "formatted_degree") else "",
                }
            
            # Add Ascendant
            ascendant = chart.ascendant
            planets["Ascendant"] = {
                "longitude": ascendant.longitude,
                "latitude": 0.0,  # Ascendant doesn't have latitude
                "speed": 0.0,     # Ascendant doesn't have speed
                "sign": ascendant.sign,
                "nakshatra": ascendant.nakshatra if hasattr(ascendant, "nakshatra") else "",
                "pada": ascendant.pada if hasattr(ascendant, "pada") else 0,
                "house": 1,  # Ascendant is always in the 1st house
                "retrograde": False,  # Ascendant is never retrograde
                "degree": ascendant.longitude % 30,
                "formatted_degree": ascendant.formatted_degree if hasattr(ascendant, "formatted_degree") else "",
            }
            
            # Add calculation system info
            planets["calculation_system"] = "vedicastro"
            
            return planets
        
        except Exception as e:
            logger.error(f"Error calculating planetary positions with vedicastro: {str(e)}")
            raise
    
    def calculate_house_cusps(self, dt: datetime, coordinates: Coordinates, system: str = "Placidus") -> HouseData:
        """Calculate house cusps using vedicastro."""
        if not self.available:
            raise RuntimeError("vedicastro library not available")
        
        try:
            # Create a chart using vedicastro
            chart = self.Chart(dt, coordinates.latitude, coordinates.longitude)
            
            # Extract house cusps
            cusps = [house.longitude for house in chart.houses]
            
            return {
                "system": system,
                "cusps": cusps
            }
        
        except Exception as e:
            logger.error(f"Error calculating house cusps with vedicastro: {str(e)}")
            raise
    
    def calculate_aspects(self, chart_data: PlanetaryData) -> AspectData:
        """Calculate aspects between planets."""
        if not self.available:
            raise RuntimeError("vedicastro library not available")
        
        try:
            # In a real implementation, we would calculate aspects here
            # For now, we'll return an empty list
            return {"aspects": []}
        
        except Exception as e:
            logger.error(f"Error calculating aspects with vedicastro: {str(e)}")
            raise
