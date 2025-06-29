"""
Birth Chart Repository Implementation
This module implements the repository interface for birth chart data.
"""
import logging
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from ...core.entities.birth_chart import BirthChart
from ...core.repositories.birth_chart_repository import BirthChartRepository

# Configure logging
logger = logging.getLogger(__name__)


class InMemoryBirthChartRepository(BirthChartRepository):
    """In-memory implementation of the birth chart repository."""
    
    def __init__(self):
        """Initialize the repository."""
        self.charts = {}
        self.user_charts = {}
    
    async def save(self, chart: BirthChart) -> str:
        """
        Save a birth chart to the repository.
        
        Args:
            chart: The birth chart to save
            
        Returns:
            str: The ID of the saved chart
        """
        # Generate a unique ID if not present
        chart_id = str(uuid.uuid4())
        
        # Store the chart
        self.charts[chart_id] = chart
        
        # Add to user's charts if user_id is provided
        user_id = getattr(chart, "user_id", None)
        if user_id:
            if user_id not in self.user_charts:
                self.user_charts[user_id] = []
            self.user_charts[user_id].append(chart_id)
        
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
        chart = self.charts.get(chart_id)
        if not chart:
            logger.warning(f"Birth chart with ID {chart_id} not found")
        return chart
    
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
        chart_ids = self.user_charts.get(user_id, [])
        
        # Apply pagination
        paginated_ids = chart_ids[offset:offset + limit]
        
        # Retrieve charts
        charts = []
        for chart_id in paginated_ids:
            chart = self.charts.get(chart_id)
            if chart:
                charts.append(chart)
        
        return charts
    
    async def delete(self, chart_id: str) -> bool:
        """
        Delete a birth chart by its ID.
        
        Args:
            chart_id: The ID of the chart to delete
            
        Returns:
            bool: True if the chart was deleted, False otherwise
        """
        if chart_id not in self.charts:
            logger.warning(f"Cannot delete: Birth chart with ID {chart_id} not found")
            return False
        
        # Remove from charts
        chart = self.charts.pop(chart_id)
        
        # Remove from user's charts
        user_id = getattr(chart, "user_id", None)
        if user_id and user_id in self.user_charts:
            try:
                self.user_charts[user_id].remove(chart_id)
            except ValueError:
                pass
        
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
        if chart_id not in self.charts:
            logger.warning(f"Cannot update: Birth chart with ID {chart_id} not found")
            return None
        
        # Get the existing chart
        chart = self.charts[chart_id]
        
        # Update the chart with new data
        for key, value in data.items():
            if hasattr(chart, key):
                setattr(chart, key, value)
        
        logger.info(f"Updated birth chart with ID: {chart_id}")
        return chart
    
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
        # Simple implementation for now
        results = []
        
        for chart in self.charts.values():
            match = True
            
            # Check each query criterion
            for key, value in query.items():
                if hasattr(chart, key):
                    chart_value = getattr(chart, key)
                    
                    # Handle date range queries
                    if key == "date_time" and isinstance(value, dict):
                        if "from" in value and chart_value < value["from"]:
                            match = False
                            break
                        if "to" in value and chart_value > value["to"]:
                            match = False
                            break
                    # Handle exact matches
                    elif chart_value != value:
                        match = False
                        break
                else:
                    match = False
                    break
            
            if match:
                results.append(chart)
        
        # Apply pagination
        paginated_results = results[offset:offset + limit]
        
        return paginated_results
