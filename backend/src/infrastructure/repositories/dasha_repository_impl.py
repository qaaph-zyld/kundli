"""
Dasha Repository Implementation
This module implements the repository interface for dasha data.
"""
import logging
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from ...core.entities.dasha import DashaAnalysis
from ...core.repositories.dasha_repository import DashaRepository

# Configure logging
logger = logging.getLogger(__name__)


class InMemoryDashaRepository(DashaRepository):
    """In-memory implementation of the dasha repository."""
    
    def __init__(self):
        """Initialize the repository."""
        self.dashas = {}
        self.birth_chart_index = {}
        self.dasha_system_index = {}
        logger.info("Initialized in-memory dasha repository")
    
    async def save(self, dasha: DashaAnalysis) -> str:
        """
        Save a dasha analysis to the repository.
        
        Args:
            dasha: The dasha analysis to save
            
        Returns:
            str: The ID of the saved dasha analysis
        """
        # Generate a unique ID if not provided
        if not dasha.id:
            dasha.id = f"dasha-{str(uuid.uuid4())}"
        
        # Store the dasha analysis
        self.dashas[dasha.id] = dasha
        
        # Update the birth chart index
        if dasha.birth_chart_id not in self.birth_chart_index:
            self.birth_chart_index[dasha.birth_chart_id] = []
        
        self.birth_chart_index[dasha.birth_chart_id].append(dasha.id)
        
        # Update the dasha system index
        key = f"{dasha.birth_chart_id}:{dasha.dasha_system}"
        self.dasha_system_index[key] = dasha.id
        
        logger.info(f"Saved dasha analysis with ID: {dasha.id}")
        return dasha.id
    
    async def get_by_id(self, dasha_id: str) -> Optional[DashaAnalysis]:
        """
        Get a dasha analysis by its ID.
        
        Args:
            dasha_id: The ID of the dasha analysis to retrieve
            
        Returns:
            Optional[DashaAnalysis]: The dasha analysis if found, None otherwise
        """
        dasha = self.dashas.get(dasha_id)
        
        if not dasha:
            logger.warning(f"Dasha analysis with ID {dasha_id} not found")
            return None
        
        return dasha
    
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
        # Get dasha IDs for the birth chart
        dasha_ids = self.birth_chart_index.get(birth_chart_id, [])
        
        # Apply pagination
        paginated_ids = dasha_ids[offset:offset + limit]
        
        # Get dashas
        dashas = [self.dashas[dasha_id] for dasha_id in paginated_ids if dasha_id in self.dashas]
        
        return dashas
    
    async def get_by_dasha_system(self, birth_chart_id: str, dasha_system: str) -> Optional[DashaAnalysis]:
        """
        Get dasha analysis for a specific birth chart and dasha system.
        
        Args:
            birth_chart_id: The ID of the birth chart
            dasha_system: The dasha system name
            
        Returns:
            Optional[DashaAnalysis]: The dasha analysis if found, None otherwise
        """
        key = f"{birth_chart_id}:{dasha_system}"
        dasha_id = self.dasha_system_index.get(key)
        
        if not dasha_id:
            logger.warning(f"Dasha analysis for birth chart {birth_chart_id} and system {dasha_system} not found")
            return None
        
        return self.dashas.get(dasha_id)
    
    async def delete(self, dasha_id: str) -> bool:
        """
        Delete a dasha analysis by its ID.
        
        Args:
            dasha_id: The ID of the dasha analysis to delete
            
        Returns:
            bool: True if the dasha analysis was deleted, False otherwise
        """
        if dasha_id not in self.dashas:
            logger.warning(f"Cannot delete: Dasha analysis with ID {dasha_id} not found")
            return False
        
        # Get the dasha analysis
        dasha = self.dashas[dasha_id]
        
        # Remove from birth chart index
        if dasha.birth_chart_id in self.birth_chart_index:
            if dasha_id in self.birth_chart_index[dasha.birth_chart_id]:
                self.birth_chart_index[dasha.birth_chart_id].remove(dasha_id)
        
        # Remove from dasha system index
        key = f"{dasha.birth_chart_id}:{dasha.dasha_system}"
        if key in self.dasha_system_index:
            del self.dasha_system_index[key]
        
        # Remove the dasha analysis
        del self.dashas[dasha_id]
        
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
        if dasha_id not in self.dashas:
            logger.warning(f"Cannot update: Dasha analysis with ID {dasha_id} not found")
            return None
        
        # Get the dasha analysis
        dasha = self.dashas[dasha_id]
        
        # Update the dasha analysis
        for key, value in data.items():
            if hasattr(dasha, key):
                setattr(dasha, key, value)
        
        logger.info(f"Updated dasha analysis with ID: {dasha_id}")
        return dasha
    
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
        # Filter dashas based on query criteria
        filtered_dashas = []
        for dasha in self.dashas.values():
            match = True
            for key, value in query.items():
                if hasattr(dasha, key):
                    attr_value = getattr(dasha, key)
                    if attr_value != value:
                        match = False
                        break
                else:
                    match = False
                    break
            
            if match:
                filtered_dashas.append(dasha)
        
        # Sort by calculation time (newest first)
        filtered_dashas.sort(key=lambda d: d.calculation_time, reverse=True)
        
        # Apply pagination
        paginated_dashas = filtered_dashas[offset:offset + limit]
        
        return paginated_dashas
