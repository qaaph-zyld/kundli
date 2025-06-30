"""
SQLAlchemy Dasha Repository
This module implements the repository interface for dasha data using SQLAlchemy.
"""
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import desc

from ...core.entities.dasha import DashaAnalysis, DashaLevel, DashaNode, DashaPhala, DashaTimeline
from ...core.repositories.dasha_repository import DashaRepository
from ..database.models.dasha_model import DashaModel
from ..database.session import get_db_session

# Configure logging
logger = logging.getLogger(__name__)


class SQLAlchemyDashaRepository(DashaRepository):
    """SQLAlchemy implementation of the dasha repository."""
    
    def __init__(self, session_factory=get_db_session):
        """
        Initialize the repository.
        
        Args:
            session_factory: Factory function to get a database session
        """
        self.session_factory = session_factory
        logger.info("Initialized SQLAlchemy dasha repository")
    
    async def save(self, dasha: DashaAnalysis) -> str:
        """
        Save a dasha analysis to the repository.
        
        Args:
            dasha: The dasha analysis to save
            
        Returns:
            str: The ID of the saved dasha analysis
        """
        with self.session_factory() as session:
            # Convert entity to model
            dasha_model = DashaModel.from_entity(dasha)
            
            # Add to session
            session.add(dasha_model)
            session.commit()
            
            logger.info(f"Saved dasha analysis with ID: {dasha_model.id}")
            return dasha_model.id
    
    async def get_by_id(self, dasha_id: str) -> Optional[DashaAnalysis]:
        """
        Get a dasha analysis by its ID.
        
        Args:
            dasha_id: The ID of the dasha analysis to retrieve
            
        Returns:
            Optional[DashaAnalysis]: The dasha analysis if found, None otherwise
        """
        with self.session_factory() as session:
            dasha_model = session.query(DashaModel).filter(DashaModel.id == dasha_id).first()
            
            if not dasha_model:
                logger.warning(f"Dasha analysis with ID {dasha_id} not found")
                return None
            
            return self._convert_to_entity(dasha_model)
    
    async def get_by_birth_chart_id(self, birth_chart_id: str, limit: int = 10, offset: int = 0) -> List[DashaAnalysis]:
        """
        Get dasha analyses for a specific birth chart.
        
        Args:
            birth_chart_id: The ID of the birth chart
            limit: Maximum number of dasha analyses to return
            offset: Number of dasha analyses to skip
            
        Returns:
            List[DashaAnalysis]: List of dasha analyses
        """
        with self.session_factory() as session:
            dasha_models = (
                session.query(DashaModel)
                .filter(DashaModel.birth_chart_id == birth_chart_id)
                .order_by(desc(DashaModel.calculation_time))
                .limit(limit)
                .offset(offset)
                .all()
            )
            
            return [self._convert_to_entity(model) for model in dasha_models]
    
    async def get_by_dasha_system(self, birth_chart_id: str, dasha_system: str) -> Optional[DashaAnalysis]:
        """
        Get dasha analysis for a specific birth chart and dasha system.
        
        Args:
            birth_chart_id: The ID of the birth chart
            dasha_system: The dasha system name
            
        Returns:
            Optional[DashaAnalysis]: The dasha analysis if found, None otherwise
        """
        with self.session_factory() as session:
            dasha_model = (
                session.query(DashaModel)
                .filter(DashaModel.birth_chart_id == birth_chart_id, DashaModel.dasha_system == dasha_system)
                .order_by(desc(DashaModel.calculation_time))
                .first()
            )
            
            if not dasha_model:
                logger.warning(f"Dasha analysis for birth chart {birth_chart_id} and system {dasha_system} not found")
                return None
            
            return self._convert_to_entity(dasha_model)
    
    async def delete(self, dasha_id: str) -> bool:
        """
        Delete a dasha analysis by its ID.
        
        Args:
            dasha_id: The ID of the dasha analysis to delete
            
        Returns:
            bool: True if the dasha analysis was deleted, False otherwise
        """
        with self.session_factory() as session:
            dasha_model = session.query(DashaModel).filter(DashaModel.id == dasha_id).first()
            
            if not dasha_model:
                logger.warning(f"Cannot delete: Dasha analysis with ID {dasha_id} not found")
                return False
            
            session.delete(dasha_model)
            session.commit()
            
            logger.info(f"Deleted dasha analysis with ID: {dasha_id}")
            return True
    
    async def update(self, dasha_id: str, data: Dict[str, Any]) -> Optional[DashaAnalysis]:
        """
        Update a dasha analysis with new data.
        
        Args:
            dasha_id: The ID of the dasha analysis to update
            data: The data to update
            
        Returns:
            Optional[DashaAnalysis]: The updated dasha analysis if found, None otherwise
        """
        with self.session_factory() as session:
            dasha_model = session.query(DashaModel).filter(DashaModel.id == dasha_id).first()
            
            if not dasha_model:
                logger.warning(f"Cannot update: Dasha analysis with ID {dasha_id} not found")
                return None
            
            # Update the model
            for key, value in data.items():
                if hasattr(dasha_model, key):
                    setattr(dasha_model, key, value)
            
            session.commit()
            
            logger.info(f"Updated dasha analysis with ID: {dasha_id}")
            return self._convert_to_entity(dasha_model)
    
    async def search(self, query: Dict[str, Any], limit: int = 10, offset: int = 0) -> List[DashaAnalysis]:
        """
        Search for dasha analyses matching query criteria.
        
        Args:
            query: The search criteria
            limit: Maximum number of dasha analyses to return
            offset: Number of dasha analyses to skip
            
        Returns:
            List[DashaAnalysis]: List of matching dasha analyses
        """
        with self.session_factory() as session:
            # Build query
            db_query = session.query(DashaModel)
            
            # Apply filters
            for key, value in query.items():
                if hasattr(DashaModel, key):
                    db_query = db_query.filter(getattr(DashaModel, key) == value)
            
            # Apply pagination
            db_query = db_query.order_by(desc(DashaModel.calculation_time)).limit(limit).offset(offset)
            
            # Execute query
            dasha_models = db_query.all()
            
            return [self._convert_to_entity(model) for model in dasha_models]
    
    def _convert_to_entity(self, model: DashaModel) -> DashaAnalysis:
        """
        Convert a dasha model to a dasha entity.
        
        Args:
            model: The dasha model
            
        Returns:
            DashaAnalysis: The dasha entity
        """
        # Convert current dasha levels
        current_mahadasha = DashaLevel(**model.current_mahadasha) if model.current_mahadasha else None
        current_antardasha = DashaLevel(**model.current_antardasha) if model.current_antardasha else None
        current_pratyantardasha = DashaLevel(**model.current_pratyantardasha) if model.current_pratyantardasha else None
        
        # Convert dasha tree
        dasha_tree = []
        if model.dasha_tree:
            for node_data in model.dasha_tree:
                # Recursively convert nested nodes
                node = self._convert_to_dasha_node(node_data)
                dasha_tree.append(node)
        
        # Convert timeline
        timeline = None
        if model.timeline:
            timeline = DashaTimeline(**model.timeline)
        
        # Convert dasha phala
        current_dasha_phala = None
        if model.current_dasha_phala:
            current_dasha_phala = DashaPhala(**model.current_dasha_phala)
        
        # Create dasha analysis entity
        return DashaAnalysis(
            id=model.id,
            birth_chart_id=model.birth_chart_id,
            calculation_time=model.calculation_time,
            calculation_system=model.calculation_system,
            execution_time=model.execution_time,
            dasha_system=model.dasha_system,
            current_mahadasha=current_mahadasha,
            current_antardasha=current_antardasha,
            current_pratyantardasha=current_pratyantardasha,
            dasha_tree=dasha_tree,
            timeline=timeline,
            current_dasha_phala=current_dasha_phala,
            upcoming_significant_periods=model.upcoming_significant_periods
        )
    
    def _convert_to_dasha_node(self, node_data: Dict[str, Any]) -> DashaNode:
        """
        Recursively convert a dasha node dictionary to a DashaNode entity.
        
        Args:
            node_data: The dasha node data
            
        Returns:
            DashaNode: The dasha node entity
        """
        # Extract children data
        children_data = node_data.pop("children", None)
        phala_data = node_data.pop("phala", None)
        
        # Convert phala
        phala = None
        if phala_data:
            phala = DashaPhala(**phala_data)
        
        # Create node
        node = DashaNode(
            **node_data,
            phala=phala,
            children=[]
        )
        
        # Convert children recursively
        if children_data:
            for child_data in children_data:
                child_node = self._convert_to_dasha_node(child_data)
                node.children.append(child_node)
        
        return node
