"""
Dasha Entity
This module defines the dasha entity for the Vedic Kundli Calculator.
"""
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field


class DashaLevel(BaseModel):
    """Model for a dasha level (e.g., Mahadasha, Antardasha, Pratyantardasha)."""
    planet: str
    start_date: datetime
    end_date: datetime
    duration_years: float
    level: int
    parent_planet: Optional[str] = None
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "planet": "Venus",
                "start_date": "2020-01-01T00:00:00Z",
                "end_date": "2040-01-01T00:00:00Z",
                "duration_years": 20.0,
                "level": 1,
                "parent_planet": None
            }
        }


class DashaPhala(BaseModel):
    """Model for dasha phala (results/effects)."""
    title: str
    description: str
    areas_of_life: List[str]
    intensity: float = Field(..., ge=0.0, le=1.0)
    is_favorable: bool
    classical_references: Optional[List[Dict[str, str]]] = None
    remedial_measures: Optional[List[str]] = None
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "title": "Venus Mahadasha Effects",
                "description": "A period of comfort, luxury, and artistic pursuits.",
                "areas_of_life": ["Relationships", "Wealth", "Arts"],
                "intensity": 0.8,
                "is_favorable": True,
                "classical_references": [
                    {"text": "The native enjoys comforts, conveyances, ornaments...", "source": "BPHS 46.22-23"}
                ],
                "remedial_measures": ["Worship Goddess Lakshmi", "Wear white clothes on Fridays"]
            }
        }


class DashaNode(BaseModel):
    """Model for a dasha node in the dasha tree."""
    planet: str
    start_date: datetime
    end_date: datetime
    duration_years: float
    level: int
    phala: Optional[DashaPhala] = None
    children: Optional[List["DashaNode"]] = None
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "planet": "Venus",
                "start_date": "2020-01-01T00:00:00Z",
                "end_date": "2040-01-01T00:00:00Z",
                "duration_years": 20.0,
                "level": 1,
                "phala": {},
                "children": []
            }
        }


# Update forward reference for DashaNode
DashaNode.update_forward_refs()


class DashaSystem(BaseModel):
    """Model for a dasha system."""
    name: str
    description: str
    levels: int
    total_years: float
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "name": "Vimshottari",
                "description": "The most commonly used dasha system in Vedic astrology.",
                "levels": 3,
                "total_years": 120.0
            }
        }


class DashaTimeline(BaseModel):
    """Model for a dasha timeline."""
    birth_chart_id: str
    dasha_system: str
    start_date: datetime
    end_date: datetime
    levels: List[int]
    timeline_entries: List[Dict[str, Any]]
    significant_transitions: List[Dict[str, Any]]
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "birth_chart_id": "12345",
                "dasha_system": "Vimshottari",
                "start_date": "2020-01-01T00:00:00Z",
                "end_date": "2080-01-01T00:00:00Z",
                "levels": [1, 2, 3],
                "timeline_entries": [],
                "significant_transitions": []
            }
        }


class DashaAnalysis(BaseModel):
    """Model for dasha analysis."""
    id: Optional[str] = None
    birth_chart_id: str
    calculation_time: datetime = Field(default_factory=datetime.utcnow)
    calculation_system: str
    execution_time: float = 0.0
    
    # Dasha data
    dasha_system: str
    current_mahadasha: DashaLevel
    current_antardasha: Optional[DashaLevel] = None
    current_pratyantardasha: Optional[DashaLevel] = None
    
    # Dasha tree (hierarchical structure)
    dasha_tree: List[DashaNode]
    
    # Dasha timeline
    timeline: Optional[DashaTimeline] = None
    
    # Analysis and interpretations
    current_dasha_phala: Optional[DashaPhala] = None
    upcoming_significant_periods: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "id": "dasha-12345",
                "birth_chart_id": "12345",
                "calculation_time": "2025-06-29T19:20:00Z",
                "calculation_system": "Vedicastro",
                "execution_time": 0.45,
                "dasha_system": "Vimshottari",
                "current_mahadasha": {},
                "current_antardasha": {},
                "current_pratyantardasha": {},
                "dasha_tree": [],
                "timeline": None,
                "current_dasha_phala": {},
                "upcoming_significant_periods": []
            }
        }
