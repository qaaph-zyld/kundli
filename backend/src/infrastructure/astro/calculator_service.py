"""
Calculator Service
This module provides a service for astrological calculations using the calculator dispatcher.
"""
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

from .calculator_dispatcher import calculator_dispatcher
from .calculator_protocol import Coordinates
from ...core.entities.birth_chart import (
    PlanetaryPosition, 
    HouseCusp, 
    Aspect, 
    DashaPeriod, 
    Yoga, 
    DivisionalChart
)

# Configure logging
logger = logging.getLogger(__name__)


class CalculatorService:
    """Service for astrological calculations."""
    
    async def calculate_chart(
        self,
        date_time: datetime,
        latitude: float,
        longitude: float,
        ayanamsa: str = "Lahiri",
        house_system: str = "Placidus",
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calculate a complete birth chart.
        
        Args:
            date_time: Date and time for calculation
            latitude: Latitude for calculation
            longitude: Longitude for calculation
            ayanamsa: Ayanamsa system to use
            house_system: House system to use
            options: Optional calculation options
            
        Returns:
            Dict[str, Any]: The calculated chart data
        """
        # Create coordinates object
        coordinates = Coordinates(latitude=latitude, longitude=longitude)
        
        # Set default options if not provided
        if options is None:
            options = {}
        
        try:
            # Calculate planetary positions
            planetary_data = calculator_dispatcher.calculate_planetary_positions(
                date_time, coordinates
            )
            
            # Calculate house cusps
            house_data = calculator_dispatcher.calculate_house_cusps(
                date_time, coordinates, house_system
            )
            
            # Calculate aspects if requested
            aspects = []
            if options.get("include_aspects", True):
                aspect_data = calculator_dispatcher.calculate_aspects(
                    date_time, coordinates
                )
                
                # Convert to domain entities
                for aspect in aspect_data:
                    aspects.append(
                        Aspect(
                            planet1=aspect.planet1,
                            planet2=aspect.planet2,
                            aspect_type=aspect.aspect_type,
                            orb=aspect.orb,
                            is_applying=aspect.is_applying,
                            exact_time=aspect.exact_time
                        )
                    )
            
            # Create result dictionary
            result = {
                "planets": {},
                "houses": {},
                "aspects": aspects,
                "calculation_system": planetary_data.get("calculation_system", ""),
                "calculation_time": planetary_data.get("calculation_time", 0.0)
            }
            
            # Convert planetary positions to domain entities
            for planet_name, position in planetary_data.items():
                if planet_name in ["calculation_system", "calculation_time"]:
                    continue
                    
                result["planets"][planet_name] = PlanetaryPosition(
                    longitude=position.longitude,
                    latitude=position.latitude,
                    speed=position.speed,
                    house=position.house,
                    sign=position.sign,
                    sign_longitude=position.sign_longitude,
                    nakshatra=position.nakshatra,
                    nakshatra_longitude=position.nakshatra_longitude,
                    is_retrograde=position.is_retrograde
                )
            
            # Convert house cusps to domain entities
            for house_num, cusp in house_data.items():
                if house_num in ["calculation_system", "calculation_time"]:
                    continue
                    
                result["houses"][house_num] = HouseCusp(
                    longitude=cusp.longitude,
                    sign=cusp.sign,
                    sign_longitude=cusp.sign_longitude
                )
            
            # Calculate ascendant
            if 1 in result["houses"]:
                result["ascendant"] = result["houses"][1].longitude
            
            # Add validation information if available
            try:
                _, validation_stats = calculator_dispatcher.cross_validate(date_time, coordinates)
                result["calculation_validation"] = validation_stats
            except Exception as e:
                logger.warning(f"Cross-validation failed: {str(e)}")
            
            return result
            
        except Exception as e:
            logger.error(f"Chart calculation failed: {str(e)}")
            raise
    
    async def calculate_divisional_charts(
        self,
        date_time: datetime,
        latitude: float,
        longitude: float,
        ayanamsa: str = "Lahiri"
    ) -> Dict[int, DivisionalChart]:
        """
        Calculate divisional charts (vargas).
        
        Args:
            date_time: Date and time for calculation
            latitude: Latitude for calculation
            longitude: Longitude for calculation
            ayanamsa: Ayanamsa system to use
            
        Returns:
            Dict[int, DivisionalChart]: Dictionary of divisional charts
        """
        # This is a placeholder implementation
        # In a real implementation, we would use a specialized calculator for divisional charts
        
        # Create coordinates object
        coordinates = Coordinates(latitude=latitude, longitude=longitude)
        
        # Standard divisional charts in Vedic astrology
        divisions = {
            1: "Rashi (D-1)",
            2: "Hora (D-2)",
            3: "Drekkana (D-3)",
            4: "Chaturthamsha (D-4)",
            7: "Saptamsha (D-7)",
            9: "Navamsha (D-9)",
            10: "Dashamsha (D-10)",
            12: "Dwadashamsha (D-12)",
            16: "Shodashamsha (D-16)",
            20: "Vimshamsha (D-20)",
            24: "Chaturvimshamsha (D-24)",
            27: "Nakshatramsha (D-27)",
            30: "Trimshamsha (D-30)",
            40: "Khavedamsha (D-40)",
            45: "Akshavedamsha (D-45)",
            60: "Shashtiamsha (D-60)"
        }
        
        # Initialize result dictionary
        result = {}
        
        # For now, just return the D-1 chart (rashi chart)
        # In a real implementation, we would calculate all divisional charts
        try:
            chart_data = await self.calculate_chart(
                date_time=date_time,
                latitude=latitude,
                longitude=longitude,
                ayanamsa=ayanamsa
            )
            
            result[1] = DivisionalChart(
                name=divisions[1],
                division=1,
                planets=chart_data["planets"],
                houses=chart_data["houses"]
            )
            
            # For D-9 (Navamsha), we would calculate it properly
            # This is just a placeholder
            result[9] = DivisionalChart(
                name=divisions[9],
                division=9,
                planets={},  # Would be calculated properly
                houses={}    # Would be calculated properly
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Divisional chart calculation failed: {str(e)}")
            return {}
    
    async def calculate_dashas(
        self,
        date_time: datetime,
        latitude: float,
        longitude: float,
        ayanamsa: str = "Lahiri"
    ) -> Dict[str, List[DashaPeriod]]:
        """
        Calculate dasha periods.
        
        Args:
            date_time: Date and time for calculation
            latitude: Latitude for calculation
            longitude: Longitude for calculation
            ayanamsa: Ayanamsa system to use
            
        Returns:
            Dict[str, List[DashaPeriod]]: Dictionary of dasha systems and their periods
        """
        # This is a placeholder implementation
        # In a real implementation, we would use a specialized calculator for dashas
        
        # Initialize result dictionary
        result = {
            "vimshottari": []
        }
        
        # For now, return empty dasha periods
        # In a real implementation, we would calculate proper dasha periods
        
        return result
    
    async def calculate_yogas(
        self,
        chart_data: Dict[str, Any]
    ) -> List[Yoga]:
        """
        Calculate yogas (planetary combinations).
        
        Args:
            chart_data: Chart data to analyze for yogas
            
        Returns:
            List[Yoga]: List of identified yogas
        """
        # This is a placeholder implementation
        # In a real implementation, we would analyze the chart for yogas
        
        # Initialize result list
        result = []
        
        # For now, return empty yoga list
        # In a real implementation, we would identify yogas in the chart
        
        return result
    
    def set_performance_profile(self, profile: str) -> bool:
        """
        Set the performance profile for calculations.
        
        Args:
            profile: Performance profile to set
            
        Returns:
            bool: True if profile was set successfully, False otherwise
        """
        return calculator_dispatcher.set_performance_profile(profile)
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get performance metrics for calculations.
        
        Returns:
            Dict[str, Any]: Performance metrics
        """
        return calculator_dispatcher.get_metrics()


# Create a singleton instance
calculator_service = CalculatorService()
