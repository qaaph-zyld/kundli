"""
Dasha SQLAlchemy Model
This module defines the SQLAlchemy model for dasha analysis.
"""
import json
from datetime import datetime
from typing import Dict, Any, Optional

from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship

from ..base import Base
from ...utils.json_encoder import CustomJSONEncoder


class DashaModel(Base):
    """SQLAlchemy model for dasha analysis."""
    __tablename__ = "dasha_analyses"
    
    id = Column(String(50), primary_key=True)
    birth_chart_id = Column(String(50), ForeignKey("birth_charts.id"), nullable=False)
    calculation_time = Column(DateTime, default=datetime.utcnow)
    calculation_system = Column(String(50), nullable=False)
    execution_time = Column(Float, default=0.0)
    
    # Dasha system information
    dasha_system = Column(String(50), nullable=False)
    
    # Current dasha levels (stored as JSON)
    current_mahadasha = Column(JSON, nullable=False)
    current_antardasha = Column(JSON, nullable=True)
    current_pratyantardasha = Column(JSON, nullable=True)
    current_sookshma = Column(JSON, nullable=True)
    current_prana = Column(JSON, nullable=True)
    
    # Dasha tree and timeline (stored as JSON)
    dasha_tree = Column(JSON, nullable=False)
    timeline = Column(JSON, nullable=True)
    
    # Analysis and interpretations
    current_dasha_phala = Column(JSON, nullable=True)
    upcoming_significant_periods = Column(JSON, nullable=True)
    
    # Relationships
    birth_chart = relationship("BirthChartModel", back_populates="dasha_analyses")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the model to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the model
        """
        return {
            "id": self.id,
            "birth_chart_id": self.birth_chart_id,
            "calculation_time": self.calculation_time.isoformat() if self.calculation_time else None,
            "calculation_system": self.calculation_system,
            "execution_time": self.execution_time,
            "dasha_system": self.dasha_system,
            "current_mahadasha": self.current_mahadasha,
            "current_antardasha": self.current_antardasha,
            "current_pratyantardasha": self.current_pratyantardasha,
            "current_sookshma": self.current_sookshma,
            "current_prana": self.current_prana,
            "dasha_tree": self.dasha_tree,
            "timeline": self.timeline,
            "current_dasha_phala": self.current_dasha_phala,
            "upcoming_significant_periods": self.upcoming_significant_periods
        }
    
    @classmethod
    def from_entity(cls, dasha_analysis):
        """
        Create a model from a dasha analysis entity.
        
        Args:
            dasha_analysis: The dasha analysis entity
            
        Returns:
            DashaModel: The dasha model
        """
        # Convert Pydantic models to dictionaries for JSON storage
        current_mahadasha = dasha_analysis.current_mahadasha.dict() if dasha_analysis.current_mahadasha else None
        current_antardasha = dasha_analysis.current_antardasha.dict() if dasha_analysis.current_antardasha else None
        current_pratyantardasha = dasha_analysis.current_pratyantardasha.dict() if dasha_analysis.current_pratyantardasha else None
        
        # Convert dasha tree to JSON-compatible format
        dasha_tree = []
        if dasha_analysis.dasha_tree:
            for node in dasha_analysis.dasha_tree:
                dasha_tree.append(json.loads(json.dumps(node.dict(), cls=CustomJSONEncoder)))
        
        # Convert timeline to JSON-compatible format
        timeline = None
        if dasha_analysis.timeline:
            timeline = json.loads(json.dumps(dasha_analysis.timeline.dict(), cls=CustomJSONEncoder))
        
        # Convert dasha phala to JSON-compatible format
        current_dasha_phala = None
        if dasha_analysis.current_dasha_phala:
            current_dasha_phala = json.loads(json.dumps(dasha_analysis.current_dasha_phala.dict(), cls=CustomJSONEncoder))
        
        # Convert upcoming significant periods to JSON-compatible format
        upcoming_significant_periods = None
        if dasha_analysis.upcoming_significant_periods:
            upcoming_significant_periods = json.loads(json.dumps(dasha_analysis.upcoming_significant_periods, cls=CustomJSONEncoder))
        
        return cls(
            id=dasha_analysis.id,
            birth_chart_id=dasha_analysis.birth_chart_id,
            calculation_time=dasha_analysis.calculation_time,
            calculation_system=dasha_analysis.calculation_system,
            execution_time=dasha_analysis.execution_time,
            dasha_system=dasha_analysis.dasha_system,
            current_mahadasha=current_mahadasha,
            current_antardasha=current_antardasha,
            current_pratyantardasha=current_pratyantardasha,
            dasha_tree=dasha_tree,
            timeline=timeline,
            current_dasha_phala=current_dasha_phala,
            upcoming_significant_periods=upcoming_significant_periods
        )
