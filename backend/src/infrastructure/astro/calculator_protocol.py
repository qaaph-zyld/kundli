"""
Calculator Protocol Interface for Astrological Calculations
This module defines the protocol interface for all astrological calculators in the system.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional

from pydantic import BaseModel


class Coordinates(BaseModel):
    """Coordinates model for latitude and longitude."""
    latitude: float
    longitude: float


class PlanetaryPosition(BaseModel):
    """Model for planetary position data."""
    longitude: float
    latitude: Optional[float] = None
    speed: Optional[float] = None
    house: Optional[int] = None
    sign: Optional[int] = None
    sign_longitude: Optional[float] = None
    nakshatra: Optional[int] = None
    nakshatra_longitude: Optional[float] = None
    is_retrograde: Optional[bool] = None


class PlanetaryData(Dict[str, PlanetaryPosition]):
    """Dictionary mapping planet names to their positions."""
    calculation_system: str = ""
    calculation_time: float = 0.0


class HouseCusp(BaseModel):
    """Model for house cusp data."""
    longitude: float
    sign: Optional[int] = None
    sign_longitude: Optional[float] = None


class HouseData(Dict[int, HouseCusp]):
    """Dictionary mapping house numbers to their cusps."""
    calculation_system: str = ""
    calculation_time: float = 0.0


class AspectData(BaseModel):
    """Model for aspect data between planets."""
    planet1: str
    planet2: str
    aspect_type: str
    orb: float
    is_applying: bool
    exact_time: Optional[datetime] = None


class AstronomicalCalculator(ABC):
    """Protocol interface for astronomical calculators."""
    
    @abstractmethod
    def calculate_planetary_positions(
        self, dt: datetime, coordinates: Coordinates
    ) -> PlanetaryData:
        """Calculate planetary positions for a given date and location."""
        pass
    
    @abstractmethod
    def calculate_house_cusps(
        self, dt: datetime, coordinates: Coordinates, house_system: str = "Placidus"
    ) -> HouseData:
        """Calculate house cusps for a given date, location and house system."""
        pass
    
    @abstractmethod
    def calculate_aspects(
        self, 
        dt: datetime, 
        coordinates: Coordinates,
        planets: Optional[List[str]] = None,
        aspect_types: Optional[Dict[str, float]] = None
    ) -> List[AspectData]:
        """Calculate aspects between planets."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if this calculator implementation is available in the current environment."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of this calculator implementation."""
        pass
