"""
Birth Chart Entity
This module defines the core domain entity for birth charts in the system.
"""
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


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
    
    # Additional Vedic attributes
    dignity: Optional[str] = None
    shadbala: Optional[float] = None
    vimsopaka_bala: Optional[float] = None
    ishta_phala: Optional[float] = None
    kashta_phala: Optional[float] = None


class HouseCusp(BaseModel):
    """Model for house cusp data."""
    longitude: float
    sign: Optional[int] = None
    sign_longitude: Optional[float] = None


class Aspect(BaseModel):
    """Model for aspect data between planets."""
    planet1: str
    planet2: str
    aspect_type: str
    orb: float
    is_applying: bool
    exact_time: Optional[datetime] = None


class DashaPeriod(BaseModel):
    """Model for dasha period data."""
    planet: str
    start_date: datetime
    end_date: datetime
    sub_periods: Optional[List["DashaPeriod"]] = None


class Yoga(BaseModel):
    """Model for yoga data."""
    name: str
    description: str
    strength: Optional[float] = None
    planets_involved: List[str]


class DivisionalChart(BaseModel):
    """Model for divisional chart (varga) data."""
    name: str
    division: int
    planets: Dict[str, PlanetaryPosition]
    houses: Dict[int, HouseCusp]


class BirthChart(BaseModel):
    """Core domain entity for birth charts."""
    # Birth data
    date_time: datetime
    latitude: float
    longitude: float
    timezone: str
    
    # Chart data
    ayanamsa: str = "Lahiri"
    house_system: str = "Placidus"
    
    # Calculation results
    planets: Dict[str, PlanetaryPosition] = Field(default_factory=dict)
    houses: Dict[int, HouseCusp] = Field(default_factory=dict)
    aspects: List[Aspect] = Field(default_factory=list)
    
    # Vedic specific data
    ascendant: Optional[float] = None
    divisional_charts: Dict[int, DivisionalChart] = Field(default_factory=dict)
    dashas: Dict[str, List[DashaPeriod]] = Field(default_factory=dict)
    yogas: List[Yoga] = Field(default_factory=list)
    
    # Calculation metadata
    calculation_system: str = ""
    calculation_time: float = 0.0
    
    class Config:
        arbitrary_types_allowed = True
        
    def get_planet_in_house(self, planet_name: str) -> Optional[int]:
        """Get the house number that a planet is in."""
        if planet_name not in self.planets:
            return None
        return self.planets[planet_name].house
    
    def get_planets_in_house(self, house_number: int) -> List[str]:
        """Get all planets in a specific house."""
        return [
            planet_name for planet_name, position in self.planets.items()
            if position.house == house_number
        ]
    
    def get_planets_in_sign(self, sign_number: int) -> List[str]:
        """Get all planets in a specific zodiac sign."""
        return [
            planet_name for planet_name, position in self.planets.items()
            if position.sign == sign_number
        ]
    
    def get_current_dasha(self, reference_date: Optional[datetime] = None) -> Optional[DashaPeriod]:
        """Get the current dasha period at the reference date."""
        if not reference_date:
            reference_date = datetime.now()
            
        # Check Vimshottari dasha first
        if "vimshottari" in self.dashas:
            for period in self.dashas["vimshottari"]:
                if period.start_date <= reference_date <= period.end_date:
                    return period
        
        # Check other dasha systems if needed
        for dasha_type, periods in self.dashas.items():
            for period in periods:
                if period.start_date <= reference_date <= period.end_date:
                    return period
                    
        return None
    
    def get_divisional_chart(self, division: int) -> Optional[DivisionalChart]:
        """Get a specific divisional chart."""
        return self.divisional_charts.get(division)
    
    def get_applicable_yogas(self) -> List[Yoga]:
        """Get all applicable yogas in the chart."""
        return self.yogas
