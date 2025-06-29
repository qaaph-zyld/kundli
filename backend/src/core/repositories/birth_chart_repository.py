"""
Birth Chart Repository Interface
This module defines the repository interface for birth chart data.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Dict, Any

from ..entities.birth_chart import BirthChart


class BirthChartRepository(ABC):
    """Repository interface for birth chart data."""
    
    @abstractmethod
    async def save(self, chart: BirthChart) -> str:
        """
        Save a birth chart to the repository.
        
        Args:
            chart: The birth chart to save
            
        Returns:
            str: The ID of the saved chart
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, chart_id: str) -> Optional[BirthChart]:
        """
        Get a birth chart by its ID.
        
        Args:
            chart_id: The ID of the chart to retrieve
            
        Returns:
            Optional[BirthChart]: The birth chart if found, None otherwise
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    async def delete(self, chart_id: str) -> bool:
        """
        Delete a birth chart by its ID.
        
        Args:
            chart_id: The ID of the chart to delete
            
        Returns:
            bool: True if the chart was deleted, False otherwise
        """
        pass
    
    @abstractmethod
    async def update(self, chart_id: str, data: Dict[str, Any]) -> Optional[BirthChart]:
        """
        Update a birth chart with new data.
        
        Args:
            chart_id: The ID of the chart to update
            data: The data to update
            
        Returns:
            Optional[BirthChart]: The updated birth chart if found, None otherwise
        """
        pass
    
    @abstractmethod
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
        pass
