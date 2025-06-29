"""
Adapter for the VedicCalculator to work with the multi-provider architecture.
This module bridges the existing VedicCalculator with the new calculator protocol.
"""
import logging
from datetime import datetime
from typing import Dict, List, Any

from ..core import VedicCalculator
from ..calculators.protocol import AstronomicalCalculator, PlanetaryData, HouseData, AspectData, Coordinates

# Setup logging
logger = logging.getLogger(__name__)

class VedicCalculatorAdapter:
    """
    Adapter class that bridges the existing VedicCalculator with the new calculator protocol.
    This allows us to gradually migrate to the new architecture while maintaining compatibility.
    """
    
    def __init__(self):
        """Initialize the adapter."""
        # Don't initialize VedicCalculator here as it needs date/lat/lon parameters
        # We'll create instances as needed in the calculate_chart method
        logger.info("VedicCalculatorAdapter initialized successfully")
    
    def calculate_chart(self, dt: datetime, lat: float, lon: float, house_system: str = "Placidus") -> Dict[str, Any]:
        """
        Calculate a complete chart using the VedicCalculator.
        This is the main entry point for chart calculations.
        """
        # Create coordinates object
        coordinates = Coordinates(latitude=lat, longitude=lon)
        
        # Use the calculator dispatcher to get planetary positions
        from ..calculators.calculator_dispatcher import calculator_dispatcher
        
        try:
            # Try to use the multi-provider architecture
            planetary_data = calculator_dispatcher.calculate_planetary_positions(dt, coordinates)
            house_data = calculator_dispatcher.calculate_house_cusps(dt, coordinates, house_system)
            
            # Log which calculator was used
            logger.info(f"Used {planetary_data.get('calculation_system', 'unknown')} for planetary calculations")
            
            # Create a chart result that matches the expected format
            chart_result = self._format_chart_result(dt, lat, lon, planetary_data, house_data)
            
            # Add cross-validation information if available
            try:
                _, validation_stats = calculator_dispatcher.cross_validate(dt, coordinates)
                chart_result['calculation_validation'] = validation_stats
            except Exception as e:
                logger.warning(f"Cross-validation failed: {str(e)}")
            
            return chart_result
            
        except Exception as e:
            # If the multi-provider architecture fails, fall back to the original VedicCalculator
            logger.warning(f"Multi-provider calculation failed, falling back to original VedicCalculator: {str(e)}")
            
            # Create a VedicCalculator instance for fallback
            try:
                vedic_calculator = VedicCalculator(
                    date=dt,
                    lat=lat,
                    lon=lon,
                    ayanamsa='Lahiri'  # Only using Lahiri ayanamsa
                )
                return vedic_calculator.calculate_chart(dt, lat, lon)
            except Exception as fallback_error:
                logger.error(f"Fallback to original VedicCalculator also failed: {str(fallback_error)}")
                raise RuntimeError(f"All calculation methods failed: {str(e)} and fallback error: {str(fallback_error)}")
    
    def _format_chart_result(self, dt: datetime, lat: float, lon: float, 
                            planetary_data: PlanetaryData, house_data: HouseData) -> Dict[str, Any]:
        """
        Format the results from the multi-provider architecture to match the expected format
        of the original VedicCalculator.
        """
        # Start with a basic chart structure
        chart_result = {
            'date': dt.strftime('%Y-%m-%d'),
            'time': dt.strftime('%H:%M:%S'),
            'latitude': lat,
            'longitude': lon,
            'planets': {},
            'houses': [],
            'ascendant': {},
            'calculation_system': planetary_data.get('calculation_system', 'multi-provider')
        }
        
        # Add planetary positions
        for planet_name, planet_data in planetary_data.items():
            if planet_name == 'calculation_system':
                continue
                
            if planet_name == 'Ascendant':
                chart_result['ascendant'] = {
                    'longitude': planet_data['longitude'],
                    'sign': planet_data['sign'],
                    'degree': planet_data['degree'],
                    'formatted_degree': planet_data['formatted_degree'],
                    'nakshatra': planet_data['nakshatra'],
                    'pada': planet_data['pada']
                }
            else:
                chart_result['planets'][planet_name] = {
                    'longitude': planet_data['longitude'],
                    'latitude': planet_data['latitude'],
                    'sign': planet_data['sign'],
                    'house': planet_data['house'],
                    'degree': planet_data['degree'],
                    'formatted_degree': planet_data['formatted_degree'],
                    'nakshatra': planet_data['nakshatra'],
                    'pada': planet_data['pada'],
                    'retrograde': planet_data['retrograde'],
                    'speed': planet_data['speed']
                }
        
        # Add house cusps
        chart_result['houses'] = house_data['cusps']
        chart_result['house_system'] = house_data['system']
        
        # Calculate additional chart features using the original VedicCalculator
        self._add_additional_features(chart_result, dt, lat, lon)
        
        return chart_result
    
    def _add_additional_features(self, chart_result: Dict[str, Any], dt: datetime, lat: float, lon: float):
        """
        Add additional chart features that are not provided by the basic planetary calculations.
        These are calculated using the original VedicCalculator.
        """
        try:
            # Create a VedicCalculator instance for additional calculations
            vedic_calculator = VedicCalculator(
                date=dt,
                lat=lat,
                lon=lon,
                ayanamsa='Lahiri'  # Only using Lahiri ayanamsa
            )
            
            # Calculate divisional charts
            divisional_charts = vedic_calculator.calculate_divisional_charts(chart_result)
            chart_result['divisional_charts'] = divisional_charts
            
            # Calculate Vimshottari Dasha
            vimshottari_dasha = vedic_calculator.calculate_vimshottari_dasha(chart_result, dt)
            chart_result['vimshottari_dasha'] = vimshottari_dasha
            
            # Calculate Yogas
            yogas = vedic_calculator.calculate_yogas(chart_result)
            chart_result['yogas'] = yogas
            
            # Calculate Ashtakavarga
            ashtakavarga = vedic_calculator.calculate_ashtakavarga(chart_result)
            chart_result['ashtakavarga'] = ashtakavarga
            
            # Calculate Shadbala
            shadbala = vedic_calculator.calculate_shadbala(chart_result)
            chart_result['shadbala'] = shadbala
            
            # Calculate Vimsopaka Bala
            vimsopaka_bala = vedic_calculator.calculate_vimsopaka_bala(divisional_charts)
            chart_result['vimsopaka_bala'] = vimsopaka_bala
            
            # Calculate Ishta-Kashta Phala
            ishta_kashta_phala = vedic_calculator.calculate_ishta_kashta_phala(chart_result)
            chart_result['ishta_kashta_phala'] = ishta_kashta_phala
            
        except Exception as e:
            logger.error(f"Error calculating additional chart features: {str(e)}")
            # Don't fail the entire calculation if additional features fail
            chart_result['calculation_errors'] = {
                'message': f"Error calculating some chart features: {str(e)}",
                'type': str(type(e).__name__)
            }


# Create a singleton instance
vedic_calculator_adapter = VedicCalculatorAdapter()
