"""
Calculate Transits Use Case
This module defines the use case for calculating transits.
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from ..entities.transit import Transit, TransitPlanet, TransitAspect, TransitEffect, TransitTimeline
from ..entities.birth_chart import BirthChart
from ..repositories.transit_repository import TransitRepository
from ..repositories.birth_chart_repository import BirthChartRepository

# Configure logging
logger = logging.getLogger(__name__)


class CalculateTransitsUseCase:
    """Use case for calculating transits."""
    
    def __init__(
        self,
        transit_repository: TransitRepository,
        birth_chart_repository: BirthChartRepository,
        calculator_service: Any
    ):
        """
        Initialize the use case.
        
        Args:
            transit_repository: Repository for transit data
            birth_chart_repository: Repository for birth chart data
            calculator_service: Service for astronomical calculations
        """
        self.transit_repository = transit_repository
        self.birth_chart_repository = birth_chart_repository
        self.calculator_service = calculator_service
        logger.info("Initialized calculate transits use case")
    
    async def calculate_transit(self, birth_chart_id: str, transit_date: datetime) -> Transit:
        """
        Calculate transit for a specific date.
        
        Args:
            birth_chart_id: ID of the birth chart
            transit_date: Date for transit calculation
            
        Returns:
            Transit: The calculated transit
        """
        logger.info(f"Calculating transit for birth chart {birth_chart_id} on {transit_date}")
        
        # Get birth chart
        birth_chart = await self.birth_chart_repository.get_by_id(birth_chart_id)
        if not birth_chart:
            logger.error(f"Birth chart with ID {birth_chart_id} not found")
            raise ValueError(f"Birth chart with ID {birth_chart_id} not found")
        
        # Calculate transit using calculator service
        start_time = datetime.utcnow()
        transit_data = await self.calculator_service.calculate_transit(
            birth_chart=birth_chart,
            transit_date=transit_date
        )
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Create transit entity
        transit = Transit(
            birth_chart_id=birth_chart_id,
            calculation_time=datetime.utcnow(),
            calculation_system=transit_data["calculation_system"],
            execution_time=execution_time,
            transit_date=transit_date,
            planets=transit_data["planets"],
            aspects=transit_data["aspects"],
            active_effects=transit_data["active_effects"]
        )
        
        # Save transit
        transit_id = await self.transit_repository.save(transit)
        
        logger.info(f"Transit calculated and saved with ID {transit_id}")
        return transit
    
    async def calculate_transit_timeline(
        self,
        birth_chart_id: str,
        start_date: datetime,
        end_date: datetime,
        step_days: int = 1
    ) -> Transit:
        """
        Calculate transit timeline for a date range.
        
        Args:
            birth_chart_id: ID of the birth chart
            start_date: Start date for timeline
            end_date: End date for timeline
            step_days: Number of days between transit calculations
            
        Returns:
            Transit: Transit with timeline data
        """
        logger.info(f"Calculating transit timeline for birth chart {birth_chart_id} from {start_date} to {end_date}")
        
        # Get birth chart
        birth_chart = await self.birth_chart_repository.get_by_id(birth_chart_id)
        if not birth_chart:
            logger.error(f"Birth chart with ID {birth_chart_id} not found")
            raise ValueError(f"Birth chart with ID {birth_chart_id} not found")
        
        # Calculate transit timeline using calculator service
        start_time = datetime.utcnow()
        timeline_data = await self.calculator_service.calculate_transit_timeline(
            birth_chart=birth_chart,
            start_date=start_date,
            end_date=end_date,
            step_days=step_days
        )
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Get current transit data (for the start date)
        transit_data = await self.calculator_service.calculate_transit(
            birth_chart=birth_chart,
            transit_date=start_date
        )
        
        # Create transit entity with timeline
        transit = Transit(
            birth_chart_id=birth_chart_id,
            calculation_time=datetime.utcnow(),
            calculation_system=transit_data["calculation_system"],
            execution_time=execution_time,
            transit_date=start_date,
            planets=transit_data["planets"],
            aspects=transit_data["aspects"],
            active_effects=transit_data["active_effects"],
            timeline=timeline_data
        )
        
        # Save transit
        transit_id = await self.transit_repository.save(transit)
        
        logger.info(f"Transit timeline calculated and saved with ID {transit_id}")
        return transit
    
    async def get_transit(self, transit_id: str) -> Optional[Transit]:
        """
        Get a transit by ID.
        
        Args:
            transit_id: ID of the transit
            
        Returns:
            Optional[Transit]: The transit if found, None otherwise
        """
        return await self.transit_repository.get_by_id(transit_id)
    
    async def get_transits_for_birth_chart(
        self,
        birth_chart_id: str,
        limit: int = 10,
        offset: int = 0
    ) -> List[Transit]:
        """
        Get transits for a birth chart.
        
        Args:
            birth_chart_id: ID of the birth chart
            limit: Maximum number of transits to return
            offset: Number of transits to skip
            
        Returns:
            List[Transit]: List of transits
        """
        return await self.transit_repository.get_by_birth_chart_id(birth_chart_id, limit, offset)
    
    async def get_transits_by_date_range(
        self,
        birth_chart_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Transit]:
        """
        Get transits for a birth chart within a date range.
        
        Args:
            birth_chart_id: ID of the birth chart
            start_date: Start date of the range
            end_date: End date of the range
            
        Returns:
            List[Transit]: List of transits
        """
        return await self.transit_repository.get_by_date_range(birth_chart_id, start_date, end_date)
    
    async def delete_transit(self, transit_id: str) -> bool:
        """
        Delete a transit.
        
        Args:
            transit_id: ID of the transit to delete
            
        Returns:
            bool: True if the transit was deleted, False otherwise
        """
        return await self.transit_repository.delete(transit_id)
