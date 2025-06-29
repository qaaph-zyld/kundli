"""
Transit Calculator
This module implements transit calculations for the Vedic Kundli Calculator.
"""
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

from ...core.entities.birth_chart import BirthChart
from ...core.entities.transit import (
    Transit, TransitPlanet, TransitAspect, TransitEffect,
    TransitTimeline, TransitPeriod, TransitHouseIngress, TransitRasiIngress
)

# Configure logging
logger = logging.getLogger(__name__)


class TransitCalculator:
    """Transit calculator for Vedic astrology."""
    
    def __init__(self, calculator_service: Any):
        """
        Initialize the transit calculator.
        
        Args:
            calculator_service: Service for astronomical calculations
        """
        self.calculator_service = calculator_service
        logger.info("Initialized transit calculator")
    
    async def calculate_transit(self, birth_chart: BirthChart, transit_date: datetime) -> Dict[str, Any]:
        """
        Calculate transit for a specific date.
        
        Args:
            birth_chart: Birth chart
            transit_date: Date for transit calculation
            
        Returns:
            Dict[str, Any]: Transit calculation data
        """
        start_time = time.time()
        logger.info(f"Calculating transit for {transit_date}")
        
        # Calculate planet positions at transit date
        planets = await self._calculate_transit_planets(birth_chart, transit_date)
        
        # Calculate aspects between transit and natal planets
        aspects = await self._calculate_transit_aspects(birth_chart, planets)
        
        # Calculate active effects
        active_effects = await self._calculate_transit_effects(birth_chart, planets, aspects)
        
        execution_time = time.time() - start_time
        
        return {
            "calculation_system": self.calculator_service.get_calculator_name(),
            "calculation_time": datetime.utcnow(),
            "execution_time": execution_time,
            "planets": planets,
            "aspects": aspects,
            "active_effects": active_effects
        }
    
    async def calculate_transit_timeline(
        self,
        birth_chart: BirthChart,
        start_date: datetime,
        end_date: datetime,
        step_days: int = 1
    ) -> Dict[str, Any]:
        """
        Calculate transit timeline for a date range.
        
        Args:
            birth_chart: Birth chart
            start_date: Start date for timeline
            end_date: End date for timeline
            step_days: Number of days between transit calculations
            
        Returns:
            Dict[str, Any]: Transit timeline data
        """
        start_time = time.time()
        logger.info(f"Calculating transit timeline from {start_date} to {end_date}")
        
        # Calculate significant dates (retrogrades, stations, etc.)
        significant_dates = await self._calculate_significant_dates(birth_chart, start_date, end_date)
        
        # Calculate planet ingresses
        planet_ingresses = await self._calculate_planet_ingresses(birth_chart, start_date, end_date)
        
        # Calculate transit periods
        transit_periods = await self._calculate_transit_periods(birth_chart, start_date, end_date, step_days)
        
        # Calculate duration in days
        duration_days = (end_date - start_date).total_seconds() / 86400
        
        execution_time = time.time() - start_time
        
        return {
            "birth_chart_id": birth_chart.id,
            "start_date": start_date,
            "end_date": end_date,
            "duration_days": duration_days,
            "transit_periods": transit_periods,
            "significant_dates": significant_dates,
            "planet_ingresses": planet_ingresses,
            "execution_time": execution_time
        }
    
    async def _calculate_transit_planets(self, birth_chart: BirthChart, transit_date: datetime) -> Dict[str, TransitPlanet]:
        """
        Calculate planet positions at transit date.
        
        Args:
            birth_chart: Birth chart
            transit_date: Date for transit calculation
            
        Returns:
            Dict[str, TransitPlanet]: Transit planet positions
        """
        # Get planet positions from calculator service
        planet_positions = await self.calculator_service.calculate_planet_positions(
            date_time=transit_date,
            latitude=birth_chart.latitude,
            longitude=birth_chart.longitude,
            ayanamsa=birth_chart.ayanamsa
        )
        
        # Convert to transit planets
        transit_planets = {}
        for planet_name, position in planet_positions.items():
            transit_planets[planet_name] = TransitPlanet(
                planet=planet_name,
                longitude=position["longitude"],
                latitude=position.get("latitude", 0.0),
                speed=position.get("speed", 0.0),
                is_retrograde=position.get("is_retrograde", False),
                nakshatra=position.get("nakshatra"),
                nakshatra_pada=position.get("nakshatra_pada"),
                rasi=position.get("rasi"),
                house=position.get("house"),
                degree_in_rasi=position.get("degree_in_rasi")
            )
        
        return transit_planets
    
    async def _calculate_transit_aspects(
        self,
        birth_chart: BirthChart,
        transit_planets: Dict[str, TransitPlanet]
    ) -> List[TransitAspect]:
        """
        Calculate aspects between transit and natal planets.
        
        Args:
            birth_chart: Birth chart
            transit_planets: Transit planet positions
            
        Returns:
            List[TransitAspect]: Transit aspects
        """
        aspects = []
        
        # Define aspect types and orbs
        aspect_types = {
            "Conjunction": 0,
            "Opposition": 180,
            "Trine": 120,
            "Square": 90,
            "Sextile": 60
        }
        
        # Define orbs for each aspect type
        orbs = {
            "Conjunction": 8,
            "Opposition": 8,
            "Trine": 6,
            "Square": 6,
            "Sextile": 4
        }
        
        # Calculate aspects
        for transit_planet_name, transit_planet in transit_planets.items():
            # Skip Rahu/Ketu for certain aspects
            if transit_planet_name in ["Rahu", "Ketu"] and aspect_type != "Conjunction":
                continue
                
            for natal_planet_name, natal_planet in birth_chart.planets.items():
                # Calculate aspects for each aspect type
                for aspect_type, aspect_angle in aspect_types.items():
                    # Calculate angle between planets
                    angle_diff = (transit_planet.longitude - natal_planet["longitude"]) % 360
                    if angle_diff > 180:
                        angle_diff = 360 - angle_diff
                    
                    # Check if within orb
                    orb_value = abs(angle_diff - aspect_angle)
                    if orb_value <= orbs[aspect_type]:
                        # Determine if applying or separating
                        is_applying = False
                        if transit_planet.speed < 0:  # Retrograde
                            is_applying = (angle_diff > aspect_angle)
                        else:
                            is_applying = (angle_diff < aspect_angle)
                        
                        # Calculate aspect strength (1.0 = exact, 0.0 = at maximum orb)
                        strength = 1.0 - (orb_value / orbs[aspect_type])
                        
                        # Create aspect
                        aspect = TransitAspect(
                            transit_planet=transit_planet_name,
                            natal_planet=natal_planet_name,
                            aspect_type=aspect_type,
                            orb=orb_value,
                            is_applying=is_applying,
                            is_exact=(orb_value < 1.0),
                            is_separating=(not is_applying),
                            strength=strength
                        )
                        
                        aspects.append(aspect)
        
        return aspects
    
    async def _calculate_transit_effects(
        self,
        birth_chart: BirthChart,
        transit_planets: Dict[str, TransitPlanet],
        transit_aspects: List[TransitAspect]
    ) -> List[TransitEffect]:
        """
        Calculate active transit effects.
        
        Args:
            birth_chart: Birth chart
            transit_planets: Transit planet positions
            transit_aspects: Transit aspects
            
        Returns:
            List[TransitEffect]: Active transit effects
        """
        effects = []
        
        # Process aspects to generate effects
        for aspect in transit_aspects:
            # Skip weak aspects
            if aspect.strength < 0.4:
                continue
                
            # Get effect data based on aspect
            effect_data = self._get_effect_data(aspect, birth_chart)
            
            if effect_data:
                # Create effect
                effect = TransitEffect(
                    title=effect_data["title"],
                    description=effect_data["description"],
                    intensity=aspect.strength,
                    area_of_life=effect_data["area_of_life"],
                    start_time=datetime.utcnow() - timedelta(days=7),  # Approximate
                    peak_time=datetime.utcnow() if aspect.is_exact else None,
                    end_time=datetime.utcnow() + timedelta(days=7),  # Approximate
                    is_favorable=effect_data["is_favorable"],
                    transit_planets=[aspect.transit_planet],
                    natal_factors=[aspect.natal_planet],
                    vedic_references=effect_data.get("vedic_references"),
                    remedial_measures=effect_data.get("remedial_measures")
                )
                
                effects.append(effect)
        
        return effects
    
    def _get_effect_data(self, aspect: TransitAspect, birth_chart: BirthChart) -> Optional[Dict[str, Any]]:
        """
        Get effect data for an aspect.
        
        Args:
            aspect: Transit aspect
            birth_chart: Birth chart
            
        Returns:
            Optional[Dict[str, Any]]: Effect data if available
        """
        # This is a simplified implementation
        # In a real implementation, this would use a database of transit effects
        
        # Example effect for Jupiter transit over natal Moon
        if aspect.transit_planet == "Jupiter" and aspect.natal_planet == "Moon" and aspect.aspect_type == "Conjunction":
            return {
                "title": "Jupiter Transit Over Natal Moon",
                "description": "A period of emotional growth, optimism, and spiritual development.",
                "area_of_life": ["Mind", "Emotions", "Spirituality"],
                "is_favorable": True,
                "vedic_references": ["Brihat Parashara Hora Shastra 46.12"],
                "remedial_measures": ["Chant Jupiter mantras", "Wear yellow"]
            }
        
        # Example effect for Saturn transit square natal Sun
        if aspect.transit_planet == "Saturn" and aspect.natal_planet == "Sun" and aspect.aspect_type == "Square":
            return {
                "title": "Saturn Square Natal Sun",
                "description": "A period of challenges to ego and identity, requiring patience and discipline.",
                "area_of_life": ["Career", "Authority", "Self-expression"],
                "is_favorable": False,
                "vedic_references": ["Brihat Parashara Hora Shastra 47.8"],
                "remedial_measures": ["Chant Saturn mantras", "Donate black items"]
            }
        
        # Add more effect data as needed
        
        return None
    
    async def _calculate_significant_dates(
        self,
        birth_chart: BirthChart,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, List[datetime]]:
        """
        Calculate significant dates in the transit period.
        
        Args:
            birth_chart: Birth chart
            start_date: Start date for timeline
            end_date: End date for timeline
            
        Returns:
            Dict[str, List[datetime]]: Significant dates by type
        """
        # This is a simplified implementation
        # In a real implementation, this would calculate actual retrograde dates, etc.
        
        return {
            "Saturn Retrograde": [datetime(2025, 8, 15, 14, 30)],
            "Jupiter Direct": [datetime(2025, 11, 23, 9, 15)],
            "Mars-Saturn Conjunction": [datetime(2025, 9, 5, 12, 0)]
        }
    
    async def _calculate_planet_ingresses(
        self,
        birth_chart: BirthChart,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, List[Any]]:
        """
        Calculate planet ingresses in the transit period.
        
        Args:
            birth_chart: Birth chart
            start_date: Start date for timeline
            end_date: End date for timeline
            
        Returns:
            Dict[str, List[Any]]: Planet ingresses by planet
        """
        # This is a simplified implementation
        # In a real implementation, this would calculate actual ingress dates
        
        return {
            "Jupiter": [
                TransitRasiIngress(
                    planet="Jupiter",
                    from_rasi="Pisces",
                    to_rasi="Aries",
                    ingress_time=datetime(2025, 7, 15, 8, 30),
                    exit_time=datetime(2025, 8, 15, 10, 45),
                    duration_days=31.1
                )
            ],
            "Saturn": [
                TransitRasiIngress(
                    planet="Saturn",
                    from_rasi="Capricorn",
                    to_rasi="Aquarius",
                    ingress_time=datetime(2025, 1, 17, 21, 45),
                    exit_time=datetime(2027, 3, 29, 11, 20),
                    duration_days=801.5
                )
            ]
        }
    
    async def _calculate_transit_periods(
        self,
        birth_chart: BirthChart,
        start_date: datetime,
        end_date: datetime,
        step_days: int
    ) -> List[TransitPeriod]:
        """
        Calculate transit periods in the timeline.
        
        Args:
            birth_chart: Birth chart
            start_date: Start date for timeline
            end_date: End date for timeline
            step_days: Number of days between transit calculations
            
        Returns:
            List[TransitPeriod]: Transit periods
        """
        # This is a simplified implementation
        # In a real implementation, this would calculate actual transit periods
        
        # Example transit period
        return [
            TransitPeriod(
                start_date=start_date,
                end_date=start_date + timedelta(days=30),
                duration_days=30.0,
                planets=["Jupiter", "Saturn", "Mars"],
                overall_intensity=0.75,
                overall_favorability=0.3,
                effects=[],
                concurrent_dasha="Venus-Moon"
            ),
            TransitPeriod(
                start_date=start_date + timedelta(days=30),
                end_date=start_date + timedelta(days=60),
                duration_days=30.0,
                planets=["Jupiter", "Saturn", "Mars"],
                overall_intensity=0.65,
                overall_favorability=0.5,
                effects=[],
                concurrent_dasha="Venus-Mars"
            )
        ]
