"""
SwissEphemeris Calculator Implementation
This module provides a calculator implementation using the Swiss Ephemeris library.
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

# Dictionary mapping planet names to their Swiss Ephemeris indices
PLANET_INDICES = {
    "Sun": 0,
    "Moon": 1,
    "Mercury": 2,
    "Venus": 3,
    "Mars": 4,
    "Jupiter": 5,
    "Saturn": 6,
    "Uranus": 7,
    "Neptune": 8,
    "Pluto": 9,
    "Rahu": 10,  # North Node
    "Ketu": 11,  # South Node
}

# Dictionary mapping house systems to their Swiss Ephemeris codes
HOUSE_SYSTEMS = {
    "Placidus": b"P",
    "Koch": b"K",
    "Whole Sign": b"W",
    "Equal": b"E",
    "Campanus": b"C",
    "Regiomontanus": b"R",
    "Porphyry": b"O",
}

# Dictionary mapping aspect types to their orbs
DEFAULT_ASPECTS = {
    "Conjunction": 0.0,
    "Opposition": 180.0,
    "Trine": 120.0,
    "Square": 90.0,
    "Sextile": 60.0,
}

# Default orb for aspects
DEFAULT_ORB = 8.0


class SwissEphemerisCalculator(AstronomicalCalculator):
    """Calculator implementation using the Swiss Ephemeris library."""
    
    def __init__(self):
        """Initialize the Swiss Ephemeris calculator."""
        try:
            import swisseph as swe
            self.swe = swe
            # Set ephemeris path if needed
            # swe.set_ephe_path("path/to/ephemeris/files")
        except ImportError:
            self.swe = None
    
    def is_available(self) -> bool:
        """Check if Swiss Ephemeris is available."""
        return self.swe is not None
    
    @property
    def name(self) -> str:
        """Get the name of this calculator."""
        return "swiss_ephemeris"
    
    def calculate_planetary_positions(
        self, dt: datetime, coordinates: Coordinates
    ) -> PlanetaryData:
        """Calculate planetary positions using Swiss Ephemeris."""
        if not self.is_available():
            raise ImportError("Swiss Ephemeris library is not available")
        
        start_time = time.time()
        
        # Convert datetime to Julian day
        jd = self._datetime_to_jd(dt)
        
        # Initialize result dictionary
        result = PlanetaryData()
        
        # Calculate positions for each planet
        for planet_name, planet_index in PLANET_INDICES.items():
            # Special handling for Rahu and Ketu (North and South Nodes)
            if planet_name == "Rahu":
                # Calculate North Node (Mean Node)
                position = self._calculate_node(jd)
                result[planet_name] = position
            elif planet_name == "Ketu":
                # Calculate South Node (opposite to North Node)
                position = self._calculate_node(jd)
                # Adjust longitude by 180 degrees for South Node
                position.longitude = (position.longitude + 180.0) % 360.0
                result[planet_name] = position
            else:
                # Calculate regular planet position
                position = self._calculate_planet(jd, planet_index)
                result[planet_name] = position
        
        # Add calculation metadata
        result.calculation_system = self.name
        result.calculation_time = time.time() - start_time
        
        return result
    
    def calculate_house_cusps(
        self, dt: datetime, coordinates: Coordinates, house_system: str = "Placidus"
    ) -> HouseData:
        """Calculate house cusps using Swiss Ephemeris."""
        if not self.is_available():
            raise ImportError("Swiss Ephemeris library is not available")
        
        start_time = time.time()
        
        # Convert datetime to Julian day
        jd = self._datetime_to_jd(dt)
        
        # Get house system code
        hsys = HOUSE_SYSTEMS.get(house_system, b"P")  # Default to Placidus
        
        # Calculate houses
        houses, ascmc = self.swe.houses(
            jd, 
            coordinates.latitude, 
            coordinates.longitude, 
            hsys
        )
        
        # Initialize result dictionary
        result = HouseData()
        
        # Process house cusps
        for i, longitude in enumerate(houses, start=1):
            cusp = HouseCusp(
                longitude=longitude,
                sign=int(longitude / 30) + 1,
                sign_longitude=longitude % 30
            )
            result[i] = cusp
        
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
            raise ImportError("Swiss Ephemeris library is not available")
        
        # Use default planets if none specified
        if planets is None:
            planets = list(PLANET_INDICES.keys())
        
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
    
    def _datetime_to_jd(self, dt: datetime) -> float:
        """Convert datetime to Julian day."""
        return self.swe.julday(
            dt.year,
            dt.month,
            dt.day,
            dt.hour + dt.minute/60.0 + dt.second/3600.0
        )
    
    def _calculate_planet(self, jd: float, planet_index: int) -> PlanetaryPosition:
        """Calculate position for a regular planet."""
        # Calculate planet position
        res = self.swe.calc_ut(jd, planet_index)
        
        # Extract data
        longitude = res[0]
        latitude = res[1]
        speed = res[3]  # Daily motion in longitude
        
        # Create position object
        position = PlanetaryPosition(
            longitude=longitude,
            latitude=latitude,
            speed=speed,
            sign=int(longitude / 30) + 1,
            sign_longitude=longitude % 30,
            is_retrograde=speed < 0
        )
        
        return position
    
    def _calculate_node(self, jd: float) -> PlanetaryPosition:
        """Calculate position for the North Node (Rahu)."""
        # Calculate mean node
        res = self.swe.calc_ut(jd, self.swe.MEAN_NODE)
        
        # Extract data
        longitude = res[0]
        latitude = res[1]
        speed = res[3]
        
        # Create position object
        position = PlanetaryPosition(
            longitude=longitude,
            latitude=latitude,
            speed=speed,
            sign=int(longitude / 30) + 1,
            sign_longitude=longitude % 30,
            is_retrograde=speed < 0
        )
        
        return position
