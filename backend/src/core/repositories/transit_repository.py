"""
Transit Repository Interface
This module defines the repository interface for transit data.
"""
import abc
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..entities.transit import Transit


class TransitRepository(abc.ABC):
    """Repository interface for transit data."""
    
    @abc.abstractmethod
    async def save(self, transit: Transit) -> str:
        """
        Save a transit calculation to the repository.
        
        Args:
            transit: The transit calculation to save
            
        Returns:
            str: The ID of the saved transit calculation
        """
        pass
    
    @abc.abstractmethod
    async def get_by_id(self, transit_id: str) -> Optional[Transit]:
        """
        Get a transit calculation by its ID.
        
        Args:
            transit_id: The ID of the transit calculation to retrieve
            
        Returns:
            Optional[Transit]: The transit calculation if found, None otherwise
        """
        pass
    
    @abc.abstractmethod
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
        pass
    
    @abc.abstractmethod
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
        pass
    
    @abc.abstractmethod
    async def delete(self, transit_id: str) -> bool:
        """
        Delete a transit calculation by its ID.
        
        Args:
            transit_id: The ID of the transit calculation to delete
            
        Returns:
            bool: True if the transit calculation was deleted, False otherwise
        """
        pass
    
    @abc.abstractmethod
    async def update(self, transit_id: str, data: Dict[str, Any]) -> Optional[Transit]:
        """
        Update a transit calculation with new data.
        
        Args:
            transit_id: The ID of the transit calculation to update
            data: The data to update
            
        Returns:
            Optional[Transit]: The updated transit calculation if found, None otherwise
        """
        pass
    
    @abc.abstractmethod
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
        pass
