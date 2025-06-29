"""
Transit SQLAlchemy Repository Implementation
This module implements the repository interface for transit data using SQLAlchemy.
"""
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy import and_, desc

from ...core.entities.transit import Transit
from ...core.repositories.transit_repository import TransitRepository
from ..database.models.transit_model import TransitModel
from ..database.session import get_session

# Configure logging
logger = logging.getLogger(__name__)


class SQLAlchemyTransitRepository(TransitRepository):
    """SQLAlchemy implementation of the transit repository."""
    
    def __init__(self, session: Optional[Session] = None):
        """
        Initialize the repository.
        
        Args:
            session: Optional SQLAlchemy session
        """
        self.session_factory = session if session else get_session
        logger.info("Initialized SQLAlchemy transit repository")
    
    async def save(self, transit: Transit) -> str:
        """
        Save a transit calculation to the repository.
        
        Args:
            transit: The transit calculation to save
            
        Returns:
            str: The ID of the saved transit calculation
        """
        with self.session_factory() as session:
            # Convert to model
            transit_dict = transit.dict()
            transit_model = TransitModel.from_dict(transit_dict)
            
            # Add to session
            session.add(transit_model)
            session.commit()
            
            # Update ID in entity
            transit.id = transit_model.id
            
            logger.info(f"Saved transit with ID: {transit.id}")
            return transit.id
    
    async def get_by_id(self, transit_id: str) -> Optional[Transit]:
        """
        Get a transit calculation by its ID.
        
        Args:
            transit_id: The ID of the transit calculation to retrieve
            
        Returns:
            Optional[Transit]: The transit calculation if found, None otherwise
        """
        with self.session_factory() as session:
            transit_model = session.query(TransitModel).filter(TransitModel.id == transit_id).first()
            
            if not transit_model:
                logger.warning(f"Transit with ID {transit_id} not found")
                return None
            
            # Convert to entity
            transit_dict = transit_model.to_dict()
            transit = Transit(**transit_dict)
            
            return transit
    
    async def get_by_birth_chart_id(self, birth_chart_id: str, limit: int = 10, offset: int = 0) -> List[Transit]:
        """
        Get transit calculations for a specific birth chart.
        
        Args:
            birth_chart_id: The ID of the birth chart
            limit: Maximum number of transit calculations to return
            offset: Number of transit calculations to skip
            
        Returns:
            List[Transit]: List of transit calculations
        """
        with self.session_factory() as session:
            # Query transits
            transit_models = (
                session.query(TransitModel)
                .filter(TransitModel.birth_chart_id == birth_chart_id)
                .order_by(desc(TransitModel.transit_date))
                .offset(offset)
                .limit(limit)
                .all()
            )
            
            # Convert to entities
            transits = [Transit(**model.to_dict()) for model in transit_models]
            
            return transits
    
    async def get_by_date_range(self, birth_chart_id: str, start_date: datetime, end_date: datetime) -> List[Transit]:
        """
        Get transit calculations for a specific birth chart within a date range.
        
        Args:
            birth_chart_id: The ID of the birth chart
            start_date: The start date of the range
            end_date: The end date of the range
            
        Returns:
            List[Transit]: List of transit calculations
        """
        with self.session_factory() as session:
            # Query transits
            transit_models = (
                session.query(TransitModel)
                .filter(
                    and_(
                        TransitModel.birth_chart_id == birth_chart_id,
                        TransitModel.transit_date >= start_date,
                        TransitModel.transit_date <= end_date
                    )
                )
                .order_by(TransitModel.transit_date)
                .all()
            )
            
            # Convert to entities
            transits = [Transit(**model.to_dict()) for model in transit_models]
            
            return transits
    
    async def delete(self, transit_id: str) -> bool:
        """
        Delete a transit calculation by its ID.
        
        Args:
            transit_id: The ID of the transit calculation to delete
            
        Returns:
            bool: True if the transit calculation was deleted, False otherwise
        """
        with self.session_factory() as session:
            # Query transit
            transit_model = session.query(TransitModel).filter(TransitModel.id == transit_id).first()
            
            if not transit_model:
                logger.warning(f"Cannot delete: Transit with ID {transit_id} not found")
                return False
            
            # Delete transit
            session.delete(transit_model)
            session.commit()
            
            logger.info(f"Deleted transit with ID: {transit_id}")
            return True
    
    async def update(self, transit_id: str, data: Dict[str, Any]) -> Optional[Transit]:
        """
        Update a transit calculation with new data.
        
        Args:
            transit_id: The ID of the transit calculation to update
            data: The data to update
            
        Returns:
            Optional[Transit]: The updated transit calculation if found, None otherwise
        """
        with self.session_factory() as session:
            # Query transit
            transit_model = session.query(TransitModel).filter(TransitModel.id == transit_id).first()
            
            if not transit_model:
                logger.warning(f"Cannot update: Transit with ID {transit_id} not found")
                return None
            
            # Update transit
            for key, value in data.items():
                if hasattr(transit_model, key):
                    setattr(transit_model, key, value)
            
            session.commit()
            
            # Convert to entity
            transit_dict = transit_model.to_dict()
            transit = Transit(**transit_dict)
            
            logger.info(f"Updated transit with ID: {transit_id}")
            return transit
    
    async def search(self, query: Dict[str, Any], limit: int = 10, offset: int = 0) -> List[Transit]:
        """
        Search for transit calculations matching query criteria.
        
        Args:
            query: The search criteria
            limit: Maximum number of transit calculations to return
            offset: Number of transit calculations to skip
            
        Returns:
            List[Transit]: List of matching transit calculations
        """
        with self.session_factory() as session:
            # Build query
            db_query = session.query(TransitModel)
            
            # Apply filters
            for key, value in query.items():
                if hasattr(TransitModel, key):
                    db_query = db_query.filter(getattr(TransitModel, key) == value)
            
            # Apply pagination
            transit_models = (
                db_query
                .order_by(desc(TransitModel.transit_date))
                .offset(offset)
                .limit(limit)
                .all()
            )
            
            # Convert to entities
            transits = [Transit(**model.to_dict()) for model in transit_models]
            
            return transits
