"""
Birth Chart Repository Database Implementation
This module implements the repository interface for birth chart data using SQLAlchemy.
"""
import logging
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy import desc

from ....core.entities.birth_chart import BirthChart
from ....core.repositories.birth_chart_repository import BirthChartRepository
from ..models import BirthChartModel

# Configure logging
logger = logging.getLogger(__name__)


class SQLAlchemyBirthChartRepository(BirthChartRepository):
    """SQLAlchemy implementation of the birth chart repository."""
    
    def __init__(self, db_session: Session):
        """
        Initialize the repository.
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db = db_session
    
    async def save(self, chart: BirthChart) -> str:
        """
        Save a birth chart to the repository.
        
        Args:
            chart: The birth chart to save
            
        Returns:
            str: The ID of the saved chart
        """
        # Generate a unique ID
        chart_id = str(uuid.uuid4())
        
        # Create model instance
        chart_model = BirthChartModel(
            id=chart_id,
            user_id=getattr(chart, "user_id", None),
            date_time=chart.date_time,
            latitude=chart.latitude,
            longitude=chart.longitude,
            timezone=chart.timezone,
            ayanamsa=chart.ayanamsa,
            house_system=chart.house_system,
            ascendant=chart.ascendant,
            planets={k: v.dict() for k, v in chart.planets.items()},
            houses={int(k): v.dict() for k, v in chart.houses.items()},
            aspects=[aspect.dict() for aspect in chart.aspects],
            divisional_charts={int(k): v.dict() for k, v in chart.divisional_charts.items()},
            dashas={k: [period.dict() for period in v] for k, v in chart.dashas.items()},
            yogas=[yoga.dict() for yoga in chart.yogas],
            calculation_system=chart.calculation_system,
            calculation_time=chart.calculation_time,
            created_at=datetime.utcnow()
        )
        
        # Add to database
        self.db.add(chart_model)
        self.db.commit()
        self.db.refresh(chart_model)
        
        logger.info(f"Saved birth chart with ID: {chart_id}")
        return chart_id
    
    async def get_by_id(self, chart_id: str) -> Optional[BirthChart]:
        """
        Get a birth chart by its ID.
        
        Args:
            chart_id: The ID of the chart to retrieve
            
        Returns:
            Optional[BirthChart]: The birth chart if found, None otherwise
        """
        # Query the database
        chart_model = self.db.query(BirthChartModel).filter(BirthChartModel.id == chart_id).first()
        
        if not chart_model:
            logger.warning(f"Birth chart with ID {chart_id} not found")
            return None
        
        # Convert to domain entity
        return self._model_to_entity(chart_model)
    
    async def get_by_user_id(self, user_id: str, limit: int = 10, offset: int = 0) -> List[BirthChart]:
        """
        Get birth charts for a specific user.
        
        Args:
            user_id: The ID of the user
            limit: Maximum number of charts to return
            offset: Number of charts to skip
            
        Returns:
            List[BirthChart]: List of birth charts
        """
        # Query the database
        chart_models = (
            self.db.query(BirthChartModel)
            .filter(BirthChartModel.user_id == user_id)
            .order_by(desc(BirthChartModel.created_at))
            .offset(offset)
            .limit(limit)
            .all()
        )
        
        # Convert to domain entities
        return [self._model_to_entity(chart_model) for chart_model in chart_models]
    
    async def delete(self, chart_id: str) -> bool:
        """
        Delete a birth chart by its ID.
        
        Args:
            chart_id: The ID of the chart to delete
            
        Returns:
            bool: True if the chart was deleted, False otherwise
        """
        # Query the database
        chart_model = self.db.query(BirthChartModel).filter(BirthChartModel.id == chart_id).first()
        
        if not chart_model:
            logger.warning(f"Cannot delete: Birth chart with ID {chart_id} not found")
            return False
        
        # Delete from database
        self.db.delete(chart_model)
        self.db.commit()
        
        logger.info(f"Deleted birth chart with ID: {chart_id}")
        return True
    
    async def update(self, chart_id: str, data: Dict[str, Any]) -> Optional[BirthChart]:
        """
        Update a birth chart with new data.
        
        Args:
            chart_id: The ID of the chart to update
            data: The data to update
            
        Returns:
            Optional[BirthChart]: The updated birth chart if found, None otherwise
        """
        # Query the database
        chart_model = self.db.query(BirthChartModel).filter(BirthChartModel.id == chart_id).first()
        
        if not chart_model:
            logger.warning(f"Cannot update: Birth chart with ID {chart_id} not found")
            return None
        
        # Update the model with new data
        for key, value in data.items():
            if hasattr(chart_model, key):
                # Handle special cases for JSON fields
                if key == "planets" and isinstance(value, dict):
                    chart_model.planets = {k: v.dict() for k, v in value.items()}
                elif key == "houses" and isinstance(value, dict):
                    chart_model.houses = {int(k): v.dict() for k, v in value.items()}
                elif key == "aspects" and isinstance(value, list):
                    chart_model.aspects = [aspect.dict() for aspect in value]
                elif key == "divisional_charts" and isinstance(value, dict):
                    chart_model.divisional_charts = {int(k): v.dict() for k, v in value.items()}
                elif key == "dashas" and isinstance(value, dict):
                    chart_model.dashas = {k: [period.dict() for period in v] for k, v in value.items()}
                elif key == "yogas" and isinstance(value, list):
                    chart_model.yogas = [yoga.dict() for yoga in value]
                else:
                    setattr(chart_model, key, value)
        
        # Commit changes
        self.db.commit()
        self.db.refresh(chart_model)
        
        logger.info(f"Updated birth chart with ID: {chart_id}")
        
        # Convert to domain entity
        return self._model_to_entity(chart_model)
    
    async def search(self, query: Dict[str, Any], limit: int = 10, offset: int = 0) -> List[BirthChart]:
        """
        Search for birth charts matching query criteria.
        
        Args:
            query: The search criteria
            limit: Maximum number of charts to return
            offset: Number of charts to skip
            
        Returns:
            List[BirthChart]: List of matching birth charts
        """
        # Start with a base query
        db_query = self.db.query(BirthChartModel)
        
        # Apply filters based on query criteria
        for key, value in query.items():
            if hasattr(BirthChartModel, key):
                # Handle date range queries
                if key == "date_time" and isinstance(value, dict):
                    if "from" in value:
                        db_query = db_query.filter(BirthChartModel.date_time >= value["from"])
                    if "to" in value:
                        db_query = db_query.filter(BirthChartModel.date_time <= value["to"])
                # Handle exact matches
                else:
                    db_query = db_query.filter(getattr(BirthChartModel, key) == value)
        
        # Apply pagination
        chart_models = db_query.order_by(desc(BirthChartModel.created_at)).offset(offset).limit(limit).all()
        
        # Convert to domain entities
        return [self._model_to_entity(chart_model) for chart_model in chart_models]
    
    def _model_to_entity(self, model: BirthChartModel) -> BirthChart:
        """
        Convert a database model to a domain entity.
        
        Args:
            model: The database model
            
        Returns:
            BirthChart: The domain entity
        """
        # Create a birth chart entity
        chart = BirthChart(
            date_time=model.date_time,
            latitude=model.latitude,
            longitude=model.longitude,
            timezone=model.timezone,
            ayanamsa=model.ayanamsa,
            house_system=model.house_system,
            ascendant=model.ascendant,
            calculation_system=model.calculation_system,
            calculation_time=model.calculation_time
        )
        
        # Add planets, houses, aspects, etc.
        # Note: In a real implementation, we would convert the JSON data to proper domain entities
        
        return chart
