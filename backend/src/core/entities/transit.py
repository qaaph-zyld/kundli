"""
Transit Entity
This module defines the transit entity for the Vedic Kundli Calculator.
"""
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field


class TransitPlanet(BaseModel):
    """Model for a transiting planet."""
    planet: str
    longitude: float
    latitude: float = 0.0
    speed: float = 0.0
    is_retrograde: bool = False
    nakshatra: Optional[str] = None
    nakshatra_pada: Optional[int] = None
    rasi: Optional[str] = None
    house: Optional[int] = None
    degree_in_rasi: Optional[float] = None
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "planet": "Jupiter",
                "longitude": 123.45,
                "latitude": 0.5,
                "speed": 0.1,
                "is_retrograde": False,
                "nakshatra": "Pushya",
                "nakshatra_pada": 2,
                "rasi": "Cancer",
                "house": 10,
                "degree_in_rasi": 3.45
            }
        }


class TransitAspect(BaseModel):
    """Model for a transit aspect."""
    transit_planet: str
    natal_planet: str
    aspect_type: str
    orb: float
    is_applying: bool
    is_exact: bool = False
    is_separating: bool = False
    strength: float = 0.0
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "transit_planet": "Jupiter",
                "natal_planet": "Sun",
                "aspect_type": "Trine",
                "orb": 1.2,
                "is_applying": True,
                "is_exact": False,
                "is_separating": False,
                "strength": 0.8
            }
        }


class TransitHouseIngress(BaseModel):
    """Model for a planet's ingress into a house."""
    planet: str
    from_house: int
    to_house: int
    ingress_time: datetime
    exit_time: Optional[datetime] = None
    duration_days: Optional[float] = None
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "planet": "Mars",
                "from_house": 11,
                "to_house": 12,
                "ingress_time": "2025-07-15T14:30:00Z",
                "exit_time": "2025-09-01T08:15:00Z",
                "duration_days": 47.5
            }
        }


class TransitRasiIngress(BaseModel):
    """Model for a planet's ingress into a rasi (sign)."""
    planet: str
    from_rasi: str
    to_rasi: str
    ingress_time: datetime
    exit_time: Optional[datetime] = None
    duration_days: Optional[float] = None
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "planet": "Saturn",
                "from_rasi": "Capricorn",
                "to_rasi": "Aquarius",
                "ingress_time": "2025-01-17T21:45:00Z",
                "exit_time": "2027-03-29T11:20:00Z",
                "duration_days": 801.5
            }
        }


class TransitNakshatraIngress(BaseModel):
    """Model for a planet's ingress into a nakshatra."""
    planet: str
    from_nakshatra: str
    from_pada: int
    to_nakshatra: str
    to_pada: int
    ingress_time: datetime
    exit_time: Optional[datetime] = None
    duration_days: Optional[float] = None
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "planet": "Moon",
                "from_nakshatra": "Ashwini",
                "from_pada": 4,
                "to_nakshatra": "Bharani",
                "to_pada": 1,
                "ingress_time": "2025-06-30T03:15:00Z",
                "exit_time": "2025-06-30T15:45:00Z",
                "duration_days": 0.52
            }
        }


class TransitEffect(BaseModel):
    """Model for a transit effect."""
    title: str
    description: str
    intensity: float = Field(..., ge=0.0, le=1.0)
    area_of_life: List[str]
    start_time: datetime
    peak_time: Optional[datetime] = None
    end_time: datetime
    is_favorable: bool
    transit_planets: List[str]
    natal_factors: List[str]
    vedic_references: Optional[List[str]] = None
    remedial_measures: Optional[List[str]] = None
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "title": "Jupiter Transit Over Natal Moon",
                "description": "A period of emotional growth, optimism, and spiritual development.",
                "intensity": 0.8,
                "area_of_life": ["Mind", "Emotions", "Spirituality"],
                "start_time": "2025-07-01T00:00:00Z",
                "peak_time": "2025-07-15T12:30:00Z",
                "end_time": "2025-07-30T00:00:00Z",
                "is_favorable": True,
                "transit_planets": ["Jupiter"],
                "natal_factors": ["Moon"],
                "vedic_references": ["Brihat Parashara Hora Shastra 46.12"],
                "remedial_measures": ["Chant Jupiter mantras", "Wear yellow"]
            }
        }


class TransitPeriod(BaseModel):
    """Model for a transit period with multiple effects."""
    start_date: datetime
    end_date: datetime
    duration_days: float
    planets: List[str]
    overall_intensity: float = Field(..., ge=0.0, le=1.0)
    overall_favorability: float = Field(..., ge=-1.0, le=1.0)
    effects: List[TransitEffect]
    concurrent_dasha: Optional[str] = None
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "start_date": "2025-07-01T00:00:00Z",
                "end_date": "2025-09-30T00:00:00Z",
                "duration_days": 91.0,
                "planets": ["Jupiter", "Saturn", "Mars"],
                "overall_intensity": 0.75,
                "overall_favorability": 0.3,
                "effects": [],
                "concurrent_dasha": "Venus-Moon"
            }
        }


class TransitTimeline(BaseModel):
    """Model for a transit timeline."""
    birth_chart_id: str
    start_date: datetime
    end_date: datetime
    duration_days: float
    transit_periods: List[TransitPeriod]
    significant_dates: Dict[str, List[datetime]]
    planet_ingresses: Dict[str, List[Union[TransitRasiIngress, TransitHouseIngress, TransitNakshatraIngress]]]
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "birth_chart_id": "12345",
                "start_date": "2025-07-01T00:00:00Z",
                "end_date": "2026-06-30T00:00:00Z",
                "duration_days": 365.0,
                "transit_periods": [],
                "significant_dates": {
                    "Saturn Retrograde": ["2025-08-15T14:30:00Z"],
                    "Jupiter Direct": ["2025-11-23T09:15:00Z"]
                },
                "planet_ingresses": {}
            }
        }


class Transit(BaseModel):
    """Model for transit calculations."""
    id: Optional[str] = None
    birth_chart_id: str
    calculation_time: datetime = Field(default_factory=datetime.utcnow)
    calculation_system: str
    execution_time: float = 0.0
    
    # Transit data
    transit_date: datetime
    planets: Dict[str, TransitPlanet]
    aspects: List[TransitAspect]
    active_effects: List[TransitEffect]
    
    # Timeline data (optional)
    timeline: Optional[TransitTimeline] = None
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "id": "transit-12345",
                "birth_chart_id": "12345",
                "calculation_time": "2025-06-29T19:20:00Z",
                "calculation_system": "Swiss Ephemeris",
                "execution_time": 0.45,
                "transit_date": "2025-07-01T00:00:00Z",
                "planets": {},
                "aspects": [],
                "active_effects": []
            }
        }
