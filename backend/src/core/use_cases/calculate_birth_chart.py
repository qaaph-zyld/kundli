"""
Calculate Birth Chart Use Case
This module defines the use case for calculating a birth chart.
"""
from datetime import datetime
from typing import Dict, Any, Optional

from ..entities.birth_chart import BirthChart
from ..repositories.birth_chart_repository import BirthChartRepository


class CalculateBirthChartUseCase:
    """Use case for calculating a birth chart."""
    
    def __init__(
        self, 
        birth_chart_repository: BirthChartRepository,
        calculator_service
    ):
        """
        Initialize the use case.
        
        Args:
            birth_chart_repository: Repository for birth chart data
            calculator_service: Service for astrological calculations
        """
        self.birth_chart_repository = birth_chart_repository
        self.calculator_service = calculator_service
    
    async def execute(
        self,
        date_time: datetime,
        latitude: float,
        longitude: float,
        timezone: str,
        ayanamsa: str = "Lahiri",
        house_system: str = "Placidus",
        user_id: Optional[str] = None,
        calculation_options: Optional[Dict[str, Any]] = None
    ) -> BirthChart:
        """
        Execute the use case to calculate a birth chart.
        
        Args:
            date_time: Date and time of birth
            latitude: Latitude of birth location
            longitude: Longitude of birth location
            timezone: Timezone of birth location
            ayanamsa: Ayanamsa system to use
            house_system: House system to use
            user_id: Optional user ID to associate with the chart
            calculation_options: Optional additional calculation options
            
        Returns:
            BirthChart: The calculated birth chart
        """
        # Set default calculation options if not provided
        if calculation_options is None:
            calculation_options = {}
        
        # Calculate the basic chart data
        chart_data = await self.calculator_service.calculate_chart(
            date_time=date_time,
            latitude=latitude,
            longitude=longitude,
            ayanamsa=ayanamsa,
            house_system=house_system,
            options=calculation_options
        )
        
        # Create the birth chart entity
        birth_chart = BirthChart(
            date_time=date_time,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone,
            ayanamsa=ayanamsa,
            house_system=house_system,
            planets=chart_data.get("planets", {}),
            houses=chart_data.get("houses", {}),
            aspects=chart_data.get("aspects", []),
            ascendant=chart_data.get("ascendant"),
            calculation_system=chart_data.get("calculation_system", ""),
            calculation_time=chart_data.get("calculation_time", 0.0)
        )
        
        # Calculate additional Vedic features if requested
        if calculation_options.get("include_divisional_charts", True):
            divisional_charts = await self.calculator_service.calculate_divisional_charts(
                date_time=date_time,
                latitude=latitude,
                longitude=longitude,
                ayanamsa=ayanamsa
            )
            birth_chart.divisional_charts = divisional_charts
        
        if calculation_options.get("include_dashas", True):
            dashas = await self.calculator_service.calculate_dashas(
                date_time=date_time,
                latitude=latitude,
                longitude=longitude,
                ayanamsa=ayanamsa
            )
            birth_chart.dashas = dashas
        
        if calculation_options.get("include_yogas", True):
            yogas = await self.calculator_service.calculate_yogas(
                chart_data=chart_data
            )
            birth_chart.yogas = yogas
        
        # Save the chart if user_id is provided
        if user_id:
            await self.birth_chart_repository.save(birth_chart)
        
        return birth_chart
