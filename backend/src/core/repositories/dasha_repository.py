"""
Dasha Repository Interface
This module defines the repository interface for dasha data.
"""
import abc
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..entities.dasha import DashaAnalysis


class DashaRepository(abc.ABC):
    """Repository interface for dasha data."""
    
    @abc.abstractmethod
    async def save(self, dasha: DashaAnalysis) -> str:
        """
        Save a dasha analysis to the repository.
        
        Args:
            dasha: The dasha analysis to save
            
        Returns:
            str: The ID of the saved dasha analysis
        """
        pass
    
    @abc.abstractmethod
    async def get_by_id(self, dasha_id: str) -> Optional[DashaAnalysis]:
        """
        Get a dasha analysis by its ID.
        
        Args:
            dasha_id: The ID of the dasha analysis to retrieve
            
        Returns:
            Optional[DashaAnalysis]: The dasha analysis if found, None otherwise
        """
        pass
    
    @abc.abstractmethod
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
        pass
    
    @abc.abstractmethod
    async def get_by_dasha_system(self, birth_chart_id: str, dasha_system: str) -> Optional[DashaAnalysis]:
        """
        Get dasha analysis for a specific birth chart and dasha system.
        
        Args:
            birth_chart_id: The ID of the birth chart
            dasha_system: The dasha system name
            
        Returns:
            Optional[DashaAnalysis]: The dasha analysis if found, None otherwise
        """
        pass
    
    @abc.abstractmethod
    async def delete(self, dasha_id: str) -> bool:
        """
        Delete a dasha analysis by its ID.
        
        Args:
            dasha_id: The ID of the dasha analysis to delete
            
        Returns:
            bool: True if the dasha analysis was deleted, False otherwise
        """
        pass
    
    @abc.abstractmethod
    async def update(self, dasha_id: str, data: Dict[str, Any]) -> Optional[DashaAnalysis]:
        """
        Update a dasha analysis with new data.
        
        Args:
            dasha_id: The ID of the dasha analysis to update
            data: The data to update
            
        Returns:
            Optional[DashaAnalysis]: The updated dasha analysis if found, None otherwise
        """
        pass
    
    @abc.abstractmethod
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
        pass
