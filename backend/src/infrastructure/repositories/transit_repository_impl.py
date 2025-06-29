"""
Transit Repository Implementation
This module implements the repository interface for transit data.
"""
import logging
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from ...core.entities.transit import Transit
from ...core.repositories.transit_repository import TransitRepository

# Configure logging
logger = logging.getLogger(__name__)


class InMemoryTransitRepository(TransitRepository):
    """In-memory implementation of the transit repository."""
    
    def __init__(self):
        """Initialize the repository."""
        self.transits = {}
        self.birth_chart_index = {}
        logger.info("Initialized in-memory transit repository")
    
    async def save(self, transit: Transit) -> str:
        """
        Save a transit calculation to the repository.
        
        Args:
            transit: The transit calculation to save
            
        Returns:
            str: The ID of the saved transit calculation
        """
        # Generate a unique ID if not provided
        if not transit.id:
            transit.id = f"transit-{str(uuid.uuid4())}"
        
        # Store the transit
        self.transits[transit.id] = transit
        
        # Update the birth chart index
        if transit.birth_chart_id not in self.birth_chart_index:
            self.birth_chart_index[transit.birth_chart_id] = []
        
        self.birth_chart_index[transit.birth_chart_id].append(transit.id)
        
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
        transit = self.transits.get(transit_id)
        
        if not transit:
            logger.warning(f"Transit with ID {transit_id} not found")
            return None
        
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
        # Get transit IDs for the birth chart
        transit_ids = self.birth_chart_index.get(birth_chart_id, [])
        
        # Apply pagination
        paginated_ids = transit_ids[offset:offset + limit]
        
        # Get transits
        transits = [self.transits[transit_id] for transit_id in paginated_ids if transit_id in self.transits]
        
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
        # Get transit IDs for the birth chart
        transit_ids = self.birth_chart_index.get(birth_chart_id, [])
        
        # Filter by date range
        filtered_transits = []
        for transit_id in transit_ids:
            transit = self.transits.get(transit_id)
            if transit and start_date <= transit.transit_date <= end_date:
                filtered_transits.append(transit)
        
        return filtered_transits
    
    async def delete(self, transit_id: str) -> bool:
        """
        Delete a transit calculation by its ID.
        
        Args:
            transit_id: The ID of the transit calculation to delete
            
        Returns:
            bool: True if the transit calculation was deleted, False otherwise
        """
        if transit_id not in self.transits:
            logger.warning(f"Cannot delete: Transit with ID {transit_id} not found")
            return False
        
        # Get the birth chart ID
        birth_chart_id = self.transits[transit_id].birth_chart_id
        
        # Remove from birth chart index
        if birth_chart_id in self.birth_chart_index:
            if transit_id in self.birth_chart_index[birth_chart_id]:
                self.birth_chart_index[birth_chart_id].remove(transit_id)
        
        # Remove the transit
        del self.transits[transit_id]
        
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
        if transit_id not in self.transits:
            logger.warning(f"Cannot update: Transit with ID {transit_id} not found")
            return None
        
        # Get the transit
        transit = self.transits[transit_id]
        
        # Update the transit
        for key, value in data.items():
            if hasattr(transit, key):
                setattr(transit, key, value)
        
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
        # Filter transits based on query criteria
        filtered_transits = []
        for transit in self.transits.values():
            match = True
            for key, value in query.items():
                if hasattr(transit, key):
                    attr_value = getattr(transit, key)
                    if attr_value != value:
                        match = False
                        break
                else:
                    match = False
                    break
            
            if match:
                filtered_transits.append(transit)
        
        # Sort by transit date (newest first)
        filtered_transits.sort(key=lambda t: t.transit_date, reverse=True)
        
        # Apply pagination
        paginated_transits = filtered_transits[offset:offset + limit]
        
        return paginated_transits
