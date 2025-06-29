"""
Transit Database Model
This module defines the SQLAlchemy model for transit data.
"""
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship

from .base import Base


def generate_transit_id() -> str:
    """Generate a unique ID for a transit calculation."""
    return f"transit-{str(uuid.uuid4())}"


class TransitModel(Base):
    """SQLAlchemy model for transit calculations."""
    __tablename__ = "transits"
    
    id = Column(String(50), primary_key=True, default=generate_transit_id)
    birth_chart_id = Column(String(50), ForeignKey("birth_charts.id"), nullable=False)
    calculation_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    calculation_system = Column(String(50), nullable=False)
    execution_time = Column(Float, default=0.0)
    
    # Transit data
    transit_date = Column(DateTime, nullable=False)
    planets = Column(JSON, nullable=False, default=dict)
    aspects = Column(JSON, nullable=False, default=list)
    active_effects = Column(JSON, nullable=False, default=list)
    
    # Timeline data (optional)
    timeline = Column(JSON, nullable=True)
    
    # Relationships
    birth_chart = relationship("BirthChartModel", back_populates="transits")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary."""
        return {
            "id": self.id,
            "birth_chart_id": self.birth_chart_id,
            "calculation_time": self.calculation_time.isoformat() if self.calculation_time else None,
            "calculation_system": self.calculation_system,
            "execution_time": self.execution_time,
            "transit_date": self.transit_date.isoformat() if self.transit_date else None,
            "planets": self.planets,
            "aspects": self.aspects,
            "active_effects": self.active_effects,
            "timeline": self.timeline
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TransitModel":
        """Create a model from a dictionary."""
        model = cls()
        
        # Set simple attributes
        model.id = data.get("id")
        model.birth_chart_id = data.get("birth_chart_id")
        model.calculation_system = data.get("calculation_system")
        model.execution_time = data.get("execution_time", 0.0)
        
        # Set datetime attributes
        if "calculation_time" in data:
            if isinstance(data["calculation_time"], str):
                model.calculation_time = datetime.fromisoformat(data["calculation_time"].replace("Z", "+00:00"))
            elif isinstance(data["calculation_time"], datetime):
                model.calculation_time = data["calculation_time"]
        
        if "transit_date" in data:
            if isinstance(data["transit_date"], str):
                model.transit_date = datetime.fromisoformat(data["transit_date"].replace("Z", "+00:00"))
            elif isinstance(data["transit_date"], datetime):
                model.transit_date = data["transit_date"]
        
        # Set JSON attributes
        model.planets = data.get("planets", {})
        model.aspects = data.get("aspects", [])
        model.active_effects = data.get("active_effects", [])
        model.timeline = data.get("timeline")
        
        return model
