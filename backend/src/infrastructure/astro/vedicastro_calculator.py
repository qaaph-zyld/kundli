"""
Vedicastro Calculator Implementation
This module provides a calculator implementation using the Vedicastro library.
"""
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple

from .calculator_protocol import (
    AstronomicalCalculator,
    Coordinates,
    PlanetaryData,
    PlanetaryPosition,
    HouseData,
    HouseCusp,
    AspectData
)

# Dictionary mapping planet names to their Vedicastro names
PLANET_MAPPING = {
    "Sun": "Sun",
    "Moon": "Moon",
    "Mercury": "Mercury",
    "Venus": "Venus",
    "Mars": "Mars",
    "Jupiter": "Jupiter",
    "Saturn": "Saturn",
    "Uranus": "Uranus",
    "Neptune": "Neptune",
    "Pluto": "Pluto",
    "Rahu": "Rahu",
    "Ketu": "Ketu",
}

# Dictionary mapping aspect types to their angles
DEFAULT_ASPECTS = {
    "Conjunction": 0.0,
    "Opposition": 180.0,
    "Trine": 120.0,
    "Square": 90.0,
    "Sextile": 60.0,
}

# Default orb for aspects
DEFAULT_ORB = 8.0


class VedicastroCalculator(AstronomicalCalculator):
    """Calculator implementation using the Vedicastro library."""
    
    def __init__(self):
        """Initialize the Vedicastro calculator."""
        try:
            import vedicastro
            self.vedicastro = vedicastro
            self.available = True
        except ImportError:
            self.vedicastro = None
            self.available = False
            print("vedicastro library not available")
    
    def is_available(self) -> bool:
        """Check if Vedicastro is available."""
        return self.available
    
    @property
    def name(self) -> str:
        """Get the name of this calculator."""
        return "vedicastro"
    
    def calculate_planetary_positions(
        self, dt: datetime, coordinates: Coordinates
    ) -> PlanetaryData:
        """Calculate planetary positions using Vedicastro."""
        if not self.is_available():
            raise ImportError("Vedicastro library is not available")
        
        start_time = time.time()
        
        # Create Vedicastro chart
        chart = self.vedicastro.Chart(
            dt,
            coordinates.latitude,
            coordinates.longitude,
            "Lahiri"  # Default ayanamsa
        )
        
        # Initialize result dictionary
        result = PlanetaryData()
        
        # Get planetary positions
        for planet_name, vedicastro_name in PLANET_MAPPING.items():
            try:
                # Get planet object
                planet = getattr(chart, vedicastro_name.lower())
                
                # Create position object
                position = PlanetaryPosition(
                    longitude=planet.longitude,
                    latitude=planet.latitude if hasattr(planet, 'latitude') else 0.0,
                    speed=planet.daily_motion if hasattr(planet, 'daily_motion') else 0.0,
                    sign=planet.sign,
                    sign_longitude=planet.sign_longitude,
                    is_retrograde=planet.is_retrograde if hasattr(planet, 'is_retrograde') else False,
                    nakshatra=planet.nakshatra if hasattr(planet, 'nakshatra') else None,
                    nakshatra_longitude=planet.nakshatra_longitude if hasattr(planet, 'nakshatra_longitude') else None,
                )
                
                # Add to result
                result[planet_name] = position
            except (AttributeError, Exception) as e:
                # Skip planets that are not available
                continue
        
        # Add calculation metadata
        result.calculation_system = self.name
        result.calculation_time = time.time() - start_time
        
        return result
    
    def calculate_house_cusps(
        self, dt: datetime, coordinates: Coordinates, house_system: str = "Placidus"
    ) -> HouseData:
        """Calculate house cusps using Vedicastro."""
        if not self.is_available():
            raise ImportError("Vedicastro library is not available")
        
        start_time = time.time()
        
        # Create Vedicastro chart
        chart = self.vedicastro.Chart(
            dt,
            coordinates.latitude,
            coordinates.longitude,
            "Lahiri"  # Default ayanamsa
        )
        
        # Initialize result dictionary
        result = HouseData()
        
        # Get house cusps
        for i in range(1, 13):
            try:
                # Get house object
                house = chart.houses[i-1]
                
                # Create cusp object
                cusp = HouseCusp(
                    longitude=house.longitude,
                    sign=house.sign,
                    sign_longitude=house.sign_longitude
                )
                
                # Add to result
                result[i] = cusp
            except (IndexError, AttributeError, Exception) as e:
                # Use placeholder for missing houses
                result[i] = HouseCusp(
                    longitude=(i-1) * 30.0,
                    sign=i,
                    sign_longitude=0.0
                )
        
        # Add calculation metadata
        result.calculation_system = self.name
        result.calculation_time = time.time() - start_time
        
        return result
    
    def calculate_aspects(
        self, 
        dt: datetime, 
        coordinates: Coordinates,
        planets: Optional[List[str]] = None,
        aspect_types: Optional[Dict[str, float]] = None
    ) -> List[AspectData]:
        """Calculate aspects between planets."""
        if not self.is_available():
            raise ImportError("Vedicastro library is not available")
        
        # Use default planets if none specified
        if planets is None:
            planets = list(PLANET_MAPPING.keys())
        
        # Use default aspects if none specified
        if aspect_types is None:
            aspect_types = DEFAULT_ASPECTS
        
        # Calculate planetary positions
        positions = self.calculate_planetary_positions(dt, coordinates)
        
        # Initialize results list
        aspects = []
        
        # Check aspects between each pair of planets
        for i, planet1 in enumerate(planets):
            for j, planet2 in enumerate(planets):
                # Skip same planet and avoid duplicate pairs
                if i >= j:
                    continue
                
                # Get longitudes
                if planet1 not in positions or planet2 not in positions:
                    continue
                
                lon1 = positions[planet1].longitude
                lon2 = positions[planet2].longitude
                
                # Calculate angle between planets
                angle = abs((lon1 - lon2 + 180) % 360 - 180)
                
                # Check each aspect type
                for aspect_name, aspect_angle in aspect_types.items():
                    # Calculate orb
                    orb = abs(angle - aspect_angle)
                    if orb <= DEFAULT_ORB:
                        # Determine if aspect is applying or separating
                        speed1 = positions[planet1].speed or 0
                        speed2 = positions[planet2].speed or 0
                        relative_speed = speed1 - speed2
                        
                        is_applying = False
                        if relative_speed != 0:
                            # If planets are moving toward the exact aspect
                            if angle < aspect_angle and relative_speed < 0:
                                is_applying = True
                            elif angle > aspect_angle and relative_speed > 0:
                                is_applying = True
                        
                        # Create aspect data
                        aspect = AspectData(
                            planet1=planet1,
                            planet2=planet2,
                            aspect_type=aspect_name,
                            orb=orb,
                            is_applying=is_applying
                        )
                        aspects.append(aspect)
        
        return aspects
