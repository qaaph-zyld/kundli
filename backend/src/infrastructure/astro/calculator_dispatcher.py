"""
Calculator Dispatcher
This module provides a dispatcher for multiple astrological calculator implementations.
"""
import time
import logging
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional, Type

from .calculator_protocol import (
    AstronomicalCalculator,
    Coordinates,
    PlanetaryData,
    HouseData,
    AspectData
)
from .swiss_ephemeris_calculator import SwissEphemerisCalculator
from .vedicastro_calculator import VedicastroCalculator

# Configure logging
logger = logging.getLogger(__name__)


class CalculatorDispatcher:
    """
    Dispatcher for multiple astrological calculator implementations.
    Provides fallback, validation, and performance profiling capabilities.
    """
    
    def __init__(self):
        """Initialize the calculator dispatcher."""
        # Register available calculators
        self.calculators: List[AstronomicalCalculator] = []
        self._register_calculators()
        
        # Performance profile configuration
        self.performance_profile = "balanced"  # Options: "speed_optimized", "precision_optimized", "balanced"
        
        # Performance metrics
        self.metrics = {
            "calls": 0,
            "failures": 0,
            "fallbacks": 0,
            "validations": 0,
            "calculator_usage": {},
            "average_calculation_time": {}
        }
    
    def _register_calculators(self):
        """Register available calculator implementations."""
        # Create calculator instances
        calculators = [
            SwissEphemerisCalculator(),
            VedicastroCalculator()
        ]
        
        # Filter available calculators
        self.calculators = [calc for calc in calculators if calc.is_available()]
        
        # Log available calculators
        for calc in self.calculators:
            logger.info(f"Registered calculator: {calc.name}")
            self.metrics["calculator_usage"][calc.name] = 0
            self.metrics["average_calculation_time"][calc.name] = 0.0
        
        if not self.calculators:
            logger.warning("No calculators available")
    
    def set_performance_profile(self, profile: str) -> bool:
        """
        Set the performance profile for the dispatcher.
        
        Args:
            profile: One of "speed_optimized", "precision_optimized", or "balanced"
            
        Returns:
            bool: True if profile was set successfully, False otherwise
        """
        valid_profiles = ["speed_optimized", "precision_optimized", "balanced"]
        if profile not in valid_profiles:
            logger.warning(f"Invalid performance profile: {profile}")
            return False
        
        self.performance_profile = profile
        logger.info(f"Set performance profile to: {profile}")
        return True
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for the dispatcher."""
        return self.metrics
    
    def get_preferred_calculator(self) -> Optional[AstronomicalCalculator]:
        """
        Get the preferred calculator based on the current performance profile.
        
        Returns:
            AstronomicalCalculator or None: The preferred calculator, or None if no calculators are available
        """
        if not self.calculators:
            return None
        
        if self.performance_profile == "speed_optimized":
            # Sort by calculation speed (lowest average calculation time first)
            sorted_calcs = sorted(
                self.calculators,
                key=lambda c: self.metrics["average_calculation_time"].get(c.name, float('inf'))
            )
            return sorted_calcs[0] if sorted_calcs else None
        
        elif self.performance_profile == "precision_optimized":
            # Prefer Swiss Ephemeris for precision
            for calc in self.calculators:
                if calc.name == "swiss_ephemeris":
                    return calc
            # Fall back to any available calculator
            return self.calculators[0]
        
        else:  # balanced profile
            # Use the first available calculator
            return self.calculators[0]
    
    def calculate_planetary_positions(
        self, dt: datetime, coordinates: Coordinates
    ) -> PlanetaryData:
        """
        Calculate planetary positions using the preferred calculator with fallback.
        
        Args:
            dt: The date and time for calculation
            coordinates: The geographical coordinates
            
        Returns:
            PlanetaryData: The calculated planetary positions
            
        Raises:
            RuntimeError: If all calculators fail
        """
        self.metrics["calls"] += 1
        
        # Try calculators in order of preference
        errors = []
        for calculator in self._get_calculator_priority():
            try:
                result = calculator.calculate_planetary_positions(dt, coordinates)
                
                # Update metrics
                self.metrics["calculator_usage"][calculator.name] = self.metrics["calculator_usage"].get(calculator.name, 0) + 1
                self._update_calculation_time(calculator.name, result.calculation_time)
                
                return result
                
            except Exception as e:
                logger.warning(f"Calculator {calculator.name} failed: {str(e)}")
                errors.append(f"{calculator.name}: {str(e)}")
                self.metrics["failures"] += 1
        
        # If all calculators failed
        self.metrics["failures"] += 1
        error_msg = "; ".join(errors)
        logger.error(f"All calculators failed to calculate planetary positions: {error_msg}")
        raise RuntimeError(f"All calculators failed to calculate planetary positions: {error_msg}")
    
    def calculate_house_cusps(
        self, dt: datetime, coordinates: Coordinates, house_system: str = "Placidus"
    ) -> HouseData:
        """
        Calculate house cusps using the preferred calculator with fallback.
        
        Args:
            dt: The date and time for calculation
            coordinates: The geographical coordinates
            house_system: The house system to use
            
        Returns:
            HouseData: The calculated house cusps
            
        Raises:
            RuntimeError: If all calculators fail
        """
        self.metrics["calls"] += 1
        
        # Try calculators in order of preference
        errors = []
        for calculator in self._get_calculator_priority():
            try:
                result = calculator.calculate_house_cusps(dt, coordinates, house_system)
                
                # Update metrics
                self.metrics["calculator_usage"][calculator.name] = self.metrics["calculator_usage"].get(calculator.name, 0) + 1
                self._update_calculation_time(calculator.name, result.calculation_time)
                
                return result
                
            except Exception as e:
                logger.warning(f"Calculator {calculator.name} failed: {str(e)}")
                errors.append(f"{calculator.name}: {str(e)}")
                self.metrics["failures"] += 1
        
        # If all calculators failed
        self.metrics["failures"] += 1
        error_msg = "; ".join(errors)
        logger.error(f"All calculators failed to calculate house cusps: {error_msg}")
        raise RuntimeError(f"All calculators failed to calculate house cusps: {error_msg}")
    
    def calculate_aspects(
        self, 
        dt: datetime, 
        coordinates: Coordinates,
        planets: Optional[List[str]] = None,
        aspect_types: Optional[Dict[str, float]] = None
    ) -> List[AspectData]:
        """
        Calculate aspects using the preferred calculator with fallback.
        
        Args:
            dt: The date and time for calculation
            coordinates: The geographical coordinates
            planets: Optional list of planets to consider
            aspect_types: Optional dictionary of aspect types and their angles
            
        Returns:
            List[AspectData]: The calculated aspects
            
        Raises:
            RuntimeError: If all calculators fail
        """
        self.metrics["calls"] += 1
        
        # Try calculators in order of preference
        errors = []
        for calculator in self._get_calculator_priority():
            try:
                start_time = time.time()
                result = calculator.calculate_aspects(dt, coordinates, planets, aspect_types)
                calc_time = time.time() - start_time
                
                # Update metrics
                self.metrics["calculator_usage"][calculator.name] = self.metrics["calculator_usage"].get(calculator.name, 0) + 1
                self._update_calculation_time(calculator.name, calc_time)
                
                return result
                
            except Exception as e:
                logger.warning(f"Calculator {calculator.name} failed: {str(e)}")
                errors.append(f"{calculator.name}: {str(e)}")
                self.metrics["failures"] += 1
        
        # If all calculators failed
        self.metrics["failures"] += 1
        error_msg = "; ".join(errors)
        logger.error(f"All calculators failed to calculate aspects: {error_msg}")
        raise RuntimeError(f"All calculators failed to calculate aspects: {error_msg}")
    
    def cross_validate(
        self, dt: datetime, coordinates: Coordinates
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Cross-validate results from multiple calculators.
        
        Args:
            dt: The date and time for calculation
            coordinates: The geographical coordinates
            
        Returns:
            Tuple[bool, Dict[str, Any]]: A tuple containing:
                - Boolean indicating if validation passed
                - Dictionary with validation statistics
        """
        if len(self.calculators) < 2:
            return True, {"status": "skipped", "reason": "Not enough calculators for validation"}
        
        self.metrics["validations"] += 1
        
        # Calculate planetary positions with all available calculators
        results = {}
        for calculator in self.calculators:
            try:
                results[calculator.name] = calculator.calculate_planetary_positions(dt, coordinates)
            except Exception as e:
                logger.warning(f"Validation: Calculator {calculator.name} failed: {str(e)}")
        
        if len(results) < 2:
            return True, {"status": "skipped", "reason": "Not enough successful calculations for validation"}
        
        # Compare results
        validation_stats = {
            "status": "passed",
            "calculators": list(results.keys()),
            "differences": {}
        }
        
        # Use the first calculator as reference
        reference_name = list(results.keys())[0]
        reference_data = results[reference_name]
        
        # Compare each planet's position across calculators
        max_diff = 0.0
        for planet in reference_data:
            if planet in ["calculation_system", "calculation_time"]:
                continue
                
            validation_stats["differences"][planet] = {}
            
            for calc_name, calc_data in results.items():
                if calc_name == reference_name or planet not in calc_data:
                    continue
                
                # Calculate difference in longitude
                ref_lon = reference_data[planet].longitude
                calc_lon = calc_data[planet].longitude
                
                # Handle 0/360 degree boundary
                diff = min(
                    abs(ref_lon - calc_lon),
                    abs(ref_lon - calc_lon + 360),
                    abs(ref_lon - calc_lon - 360)
                )
                
                validation_stats["differences"][planet][calc_name] = diff
                max_diff = max(max_diff, diff)
        
        # Validation passes if maximum difference is less than threshold
        threshold = 1.0  # 1 degree threshold
        validation_passed = max_diff < threshold
        
        if not validation_passed:
            validation_stats["status"] = "failed"
            validation_stats["max_difference"] = max_diff
            validation_stats["threshold"] = threshold
            logger.warning(f"Cross-validation failed: Maximum difference {max_diff} exceeds threshold {threshold}")
        
        return validation_passed, validation_stats
    
    def _get_calculator_priority(self) -> List[AstronomicalCalculator]:
        """
        Get calculators in priority order based on the performance profile.
        
        Returns:
            List[AstronomicalCalculator]: Calculators in priority order
        """
        if not self.calculators:
            return []
        
        preferred = self.get_preferred_calculator()
        if preferred:
            # Put preferred calculator first, followed by others
            return [preferred] + [c for c in self.calculators if c != preferred]
        else:
            return self.calculators
    
    def _update_calculation_time(self, calculator_name: str, calculation_time: float):
        """Update the average calculation time for a calculator."""
        current_avg = self.metrics["average_calculation_time"].get(calculator_name, 0.0)
        current_count = self.metrics["calculator_usage"].get(calculator_name, 0)
        
        if current_count <= 1:
            # First calculation, just use the time
            self.metrics["average_calculation_time"][calculator_name] = calculation_time
        else:
            # Update running average
            new_avg = current_avg + (calculation_time - current_avg) / current_count
            self.metrics["average_calculation_time"][calculator_name] = new_avg


# Create a singleton instance
calculator_dispatcher = CalculatorDispatcher()
