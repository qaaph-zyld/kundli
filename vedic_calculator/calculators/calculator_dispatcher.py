"""
Calculator dispatcher for the multi-provider architecture.
This module provides a unified interface to multiple calculator implementations
with fallback, validation, and optimization capabilities.
"""
import logging
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

from ..calculators.protocol import (
    AstronomicalCalculator, PlanetaryData, HouseData, AspectData, Coordinates
)
from ..calculators.vedicastro_calculator import VedicastroCalculator
from ..calculators.swiss_ephemeris_calculator import SwissEphemerisCalculator

# Setup logging
logger = logging.getLogger(__name__)

class CalculatorDispatcher:
    """
    Dispatcher for multiple calculator implementations.
    Provides fallback, validation, and optimization capabilities.
    """
    
    def __init__(self):
        """Initialize the dispatcher with available calculators."""
        self.calculators = {}
        self._initialize_calculators()
        self.performance_profiles = {
            'speed_optimized': ['vedicastro', 'swiss_ephemeris'],
            'precision_optimized': ['swiss_ephemeris', 'vedicastro'],
            'balanced': ['vedicastro', 'swiss_ephemeris'],
        }
        self.current_profile = 'balanced'
        self.performance_metrics = {}
        
    def _initialize_calculators(self):
        """Initialize all available calculator implementations."""
        # Try to initialize each calculator
        calculators_to_init = [
            ('vedicastro', VedicastroCalculator),
            ('swiss_ephemeris', SwissEphemerisCalculator),
            # Add more calculators here as they are implemented
        ]
        
        for name, calculator_class in calculators_to_init:
            try:
                calculator = calculator_class()
                if calculator.available:
                    self.calculators[name] = calculator
                    logger.info(f"Successfully initialized calculator: {name}")
                else:
                    logger.warning(f"Calculator {name} is not available")
            except Exception as e:
                logger.error(f"Error initializing calculator {name}: {str(e)}")
        
        if not self.calculators:
            logger.error("No calculators available. System will not function correctly.")
    
    def set_performance_profile(self, profile: str):
        """Set the performance profile for calculator selection."""
        if profile in self.performance_profiles:
            self.current_profile = profile
            logger.info(f"Set performance profile to {profile}")
        else:
            logger.warning(f"Unknown performance profile: {profile}. Using 'balanced'.")
            self.current_profile = 'balanced'
    
    def _get_calculator_order(self) -> List[str]:
        """Get the order of calculators to try based on current profile."""
        return self.performance_profiles.get(self.current_profile, ['vedicastro', 'swiss_ephemeris'])
    
    def calculate_planetary_positions(self, dt: datetime, coordinates: Coordinates) -> PlanetaryData:
        """
        Calculate planetary positions using available calculators.
        Will try calculators in order based on the current performance profile.
        """
        errors = []
        calculator_order = self._get_calculator_order()
        
        for calculator_name in calculator_order:
            if calculator_name not in self.calculators:
                continue
                
            calculator = self.calculators[calculator_name]
            try:
                start_time = time.time()
                result = calculator.calculate_planetary_positions(dt, coordinates)
                end_time = time.time()
                
                # Record performance metrics
                self._record_performance(calculator_name, 'calculate_planetary_positions', end_time - start_time)
                
                # Validate result
                if self._validate_planetary_data(result):
                    return result
                else:
                    logger.warning(f"Calculator {calculator_name} returned invalid data")
            except Exception as e:
                logger.error(f"Error calculating planetary positions with {calculator_name}: {str(e)}")
                errors.append((calculator_name, str(e)))
        
        # If we get here, all calculators failed
        error_msg = "; ".join([f"{name}: {error}" for name, error in errors])
        raise RuntimeError(f"All calculators failed to calculate planetary positions: {error_msg}")
    
    def calculate_house_cusps(self, dt: datetime, coordinates: Coordinates, system: str = "Placidus") -> HouseData:
        """
        Calculate house cusps using available calculators.
        Will try calculators in order based on the current performance profile.
        """
        errors = []
        calculator_order = self._get_calculator_order()
        
        for calculator_name in calculator_order:
            if calculator_name not in self.calculators:
                continue
                
            calculator = self.calculators[calculator_name]
            try:
                start_time = time.time()
                result = calculator.calculate_house_cusps(dt, coordinates, system)
                end_time = time.time()
                
                # Record performance metrics
                self._record_performance(calculator_name, 'calculate_house_cusps', end_time - start_time)
                
                # Validate result
                if self._validate_house_data(result):
                    return result
                else:
                    logger.warning(f"Calculator {calculator_name} returned invalid house data")
            except Exception as e:
                logger.error(f"Error calculating house cusps with {calculator_name}: {str(e)}")
                errors.append((calculator_name, str(e)))
        
        # If we get here, all calculators failed
        error_msg = "; ".join([f"{name}: {error}" for name, error in errors])
        raise RuntimeError(f"All calculators failed to calculate house cusps: {error_msg}")
    
    def calculate_aspects(self, chart_data: PlanetaryData) -> AspectData:
        """
        Calculate aspects using available calculators.
        Will try calculators in order based on the current performance profile.
        """
        errors = []
        calculator_order = self._get_calculator_order()
        
        for calculator_name in calculator_order:
            if calculator_name not in self.calculators:
                continue
                
            calculator = self.calculators[calculator_name]
            try:
                start_time = time.time()
                result = calculator.calculate_aspects(chart_data)
                end_time = time.time()
                
                # Record performance metrics
                self._record_performance(calculator_name, 'calculate_aspects', end_time - start_time)
                
                return result
            except Exception as e:
                logger.error(f"Error calculating aspects with {calculator_name}: {str(e)}")
                errors.append((calculator_name, str(e)))
        
        # If we get here, all calculators failed
        error_msg = "; ".join([f"{name}: {error}" for name, error in errors])
        raise RuntimeError(f"All calculators failed to calculate aspects: {error_msg}")
    
    def _record_performance(self, calculator_name: str, method_name: str, execution_time: float):
        """Record performance metrics for a calculator method."""
        if calculator_name not in self.performance_metrics:
            self.performance_metrics[calculator_name] = {}
        
        if method_name not in self.performance_metrics[calculator_name]:
            self.performance_metrics[calculator_name][method_name] = {
                'count': 0,
                'total_time': 0,
                'average_time': 0,
                'min_time': float('inf'),
                'max_time': 0
            }
        
        metrics = self.performance_metrics[calculator_name][method_name]
        metrics['count'] += 1
        metrics['total_time'] += execution_time
        metrics['average_time'] = metrics['total_time'] / metrics['count']
        metrics['min_time'] = min(metrics['min_time'], execution_time)
        metrics['max_time'] = max(metrics['max_time'], execution_time)
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get the current performance metrics."""
        return self.performance_metrics
    
    def _validate_planetary_data(self, data: PlanetaryData) -> bool:
        """Validate planetary data for completeness and correctness."""
        required_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        
        # Check that all required planets are present
        for planet in required_planets:
            if planet not in data:
                logger.warning(f"Missing required planet: {planet}")
                return False
        
        # Check that each planet has the required fields
        required_fields = ["longitude", "sign", "house", "degree"]
        for planet in required_planets:
            for field in required_fields:
                if field not in data[planet]:
                    logger.warning(f"Missing required field {field} for planet {planet}")
                    return False
        
        return True
    
    def _validate_house_data(self, data: HouseData) -> bool:
        """Validate house data for completeness and correctness."""
        # Check that the system field is present
        if "system" not in data:
            logger.warning("Missing 'system' field in house data")
            return False
        
        # Check that the cusps field is present and has 12 values
        if "cusps" not in data or len(data["cusps"]) != 12:
            logger.warning("Missing or invalid 'cusps' field in house data")
            return False
        
        return True
    
    def cross_validate(self, dt: datetime, coordinates: Coordinates) -> Tuple[PlanetaryData, Dict[str, Any]]:
        """
        Cross-validate results from multiple calculators.
        Returns the consensus result and validation statistics.
        """
        results = {}
        validation_stats = {
            'calculators_used': [],
            'consensus_level': 0.0,
            'discrepancies': {}
        }
        
        # Get results from all available calculators
        for name, calculator in self.calculators.items():
            try:
                results[name] = calculator.calculate_planetary_positions(dt, coordinates)
                validation_stats['calculators_used'].append(name)
            except Exception as e:
                logger.error(f"Error in cross-validation with {name}: {str(e)}")
        
        if not results:
            raise RuntimeError("No calculators available for cross-validation")
        
        # If only one calculator is available, return its result
        if len(results) == 1:
            calculator_name = next(iter(results))
            validation_stats['consensus_level'] = 1.0
            return results[calculator_name], validation_stats
        
        # Compare results and find consensus
        consensus_result = self._find_consensus(results, validation_stats)
        
        return consensus_result, validation_stats
    
    def _find_consensus(self, results: Dict[str, PlanetaryData], validation_stats: Dict[str, Any]) -> PlanetaryData:
        """Find consensus among multiple calculator results."""
        # For simplicity, we'll use the first calculator's result as the consensus
        # In a real implementation, we would compare the results and find the consensus
        calculator_name = next(iter(results))
        consensus_result = results[calculator_name]
        
        # Calculate consensus level (simplified)
        validation_stats['consensus_level'] = 1.0 / len(results)
        
        # In a real implementation, we would calculate discrepancies between calculators
        
        return consensus_result


# Create a singleton instance
calculator_dispatcher = CalculatorDispatcher()
