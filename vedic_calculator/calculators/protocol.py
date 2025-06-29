"""
Protocol definitions for astronomical calculators.
This module defines the interfaces that all calculator implementations must follow.
"""
from typing import Protocol, Dict, List, Any, TypedDict, Optional
from dataclasses import dataclass
from datetime import datetime
from typing_extensions import NotRequired


@dataclass
class Coordinates:
    """Geographic coordinates."""
    latitude: float
    longitude: float


class PlanetaryPosition(TypedDict):
    """Planetary position data."""
    longitude: float  # Zodiacal longitude in degrees
    latitude: float  # Celestial latitude in degrees
    speed: float  # Daily motion in degrees
    sign: str  # Zodiac sign
    nakshatra: str  # Lunar mansion
    pada: int  # Quarter of nakshatra
    house: int  # House number
    retrograde: bool  # Whether planet is retrograde
    degree: float  # Degree within sign
    formatted_degree: str  # Formatted degree (e.g. "15°30'45\"")
    declination: NotRequired[float]  # Declination in degrees
    right_ascension: NotRequired[float]  # Right ascension in degrees


class PlanetaryData(TypedDict):
    """Complete planetary data for a chart."""
    Sun: PlanetaryPosition
    Moon: PlanetaryPosition
    Mars: PlanetaryPosition
    Mercury: PlanetaryPosition
    Jupiter: PlanetaryPosition
    Venus: PlanetaryPosition
    Saturn: PlanetaryPosition
    Rahu: PlanetaryPosition
    Ketu: PlanetaryPosition
    Ascendant: NotRequired[PlanetaryPosition]
    calculation_system: str  # Name of calculation system used


class HouseData(TypedDict):
    """House cusps data."""
    system: str  # House system used (e.g., "Placidus", "Koch", "Whole Sign")
    cusps: List[float]  # List of house cusps in degrees


class AspectData(TypedDict):
    """Aspect data between planets."""
    aspects: List[Dict[str, Any]]  # List of aspects


class AstronomicalCalculator(Protocol):
    """Protocol for astronomical calculators."""
    
    def calculate_planetary_positions(self, dt: datetime, coordinates: Coordinates) -> PlanetaryData:
        """Calculate planetary positions for the given datetime and coordinates."""
        ...
    
    def calculate_house_cusps(self, dt: datetime, coordinates: Coordinates, system: str = "Placidus") -> HouseData:
        """Calculate house cusps for the given datetime, coordinates, and house system."""
        ...
    
    def calculate_aspects(self, chart_data: PlanetaryData) -> AspectData:
        """Calculate aspects between planets in the given chart data."""
        ...


class EphemerisProvider(Protocol):
    """Protocol for ephemeris data providers."""
    
    def get_planet_position(self, planet: str, dt: datetime) -> Dict[str, float]:
        """Get position of a planet at the given datetime."""
        ...
    
    def get_house_cusps(self, dt: datetime, lat: float, lon: float, system: str = "Placidus") -> List[float]:
        """Get house cusps for the given datetime, coordinates, and house system."""
        ...
