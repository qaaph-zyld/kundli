"""
Error checking utility for the Vedic Kundli Calculator.
This module provides functions to validate calculations and detect errors.
"""

import os
import json
import datetime
from .logger import app_logger, calc_logger, create_error_report

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

def validate_planet_positions(planet_data):
    """
    Validate planetary positions for basic correctness.
    
    Args:
        planet_data: Dictionary containing planetary position data
    
    Returns:
        bool: True if validation passes, False otherwise
    """
    try:
        # Check if all required planets are present
        required_planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
        for planet in required_planets:
            if planet not in planet_data:
                raise ValidationError(f"Missing required planet: {planet}")
        
        # Check if positions are within valid ranges
        for planet, data in planet_data.items():
            if 'longitude' not in data:
                raise ValidationError(f"Missing longitude for planet: {planet}")
            
            longitude = data['longitude']
            if not (0 <= longitude < 360):
                raise ValidationError(f"Invalid longitude for {planet}: {longitude}")
            
            if 'house' in data:
                house = data['house']
                if not (1 <= house <= 12):
                    raise ValidationError(f"Invalid house number for {planet}: {house}")
        
        # Check for logical consistency
        if abs(planet_data['Rahu']['longitude'] - planet_data['Ketu']['longitude']) != 180:
            difference = abs(planet_data['Rahu']['longitude'] - planet_data['Ketu']['longitude'])
            app_logger.warning(f"Rahu-Ketu axis not exactly 180 degrees apart: {difference}")
        
        app_logger.info("Planet position validation passed")
        return True
    
    except ValidationError as e:
        app_logger.error(f"Planet position validation failed: {str(e)}")
        return False
    except Exception as e:
        app_logger.error(f"Unexpected error in planet position validation: {str(e)}")
        return False

def validate_chart_data(chart_data):
    """
    Validate chart data for completeness and correctness.
    
    Args:
        chart_data: Dictionary containing chart data
    
    Returns:
        bool: True if validation passes, False otherwise
    """
    try:
        # Check if all required components are present
        required_components = ['planets', 'houses', 'ascendant']
        for component in required_components:
            if component not in chart_data:
                raise ValidationError(f"Missing required chart component: {component}")
        
        # Check ascendant
        if not (0 <= chart_data['ascendant'] < 360):
            raise ValidationError(f"Invalid ascendant longitude: {chart_data['ascendant']}")
        
        # Check houses
        if len(chart_data['houses']) != 12:
            raise ValidationError(f"Invalid number of houses: {len(chart_data['houses'])}, expected 12")
        
        # Validate planet positions
        validate_planet_positions(chart_data['planets'])
        
        app_logger.info("Chart data validation passed")
        return True
    
    except ValidationError as e:
        app_logger.error(f"Chart data validation failed: {str(e)}")
        return False
    except Exception as e:
        app_logger.error(f"Unexpected error in chart data validation: {str(e)}")
        return False

def validate_dasha_calculations(dasha_data):
    """
    Validate dasha calculations for completeness and correctness.
    
    Args:
        dasha_data: Dictionary containing dasha data
    
    Returns:
        bool: True if validation passes, False otherwise
    """
    try:
        # Check if main dasha data is present
        if 'main' not in dasha_data:
            raise ValidationError("Missing main dasha data")
        
        # Check if at least one level of sub-dasha is present
        if 'sub' not in dasha_data:
            raise ValidationError("Missing sub-dasha data")
        
        # Check for date consistency in main dasha periods
        main_dashas = dasha_data['main']
        for i in range(len(main_dashas) - 1):
            current_end = datetime.datetime.fromisoformat(main_dashas[i]['end_date'])
            next_start = datetime.datetime.fromisoformat(main_dashas[i+1]['start_date'])
            
            # Check if end of one period matches start of next
            if current_end != next_start:
                app_logger.warning(f"Gap in dasha periods: {current_end} to {next_start}")
        
        app_logger.info("Dasha calculation validation passed")
        return True
    
    except ValidationError as e:
        app_logger.error(f"Dasha calculation validation failed: {str(e)}")
        return False
    except Exception as e:
        app_logger.error(f"Unexpected error in dasha calculation validation: {str(e)}")
        return False

def validate_transit_data(transit_data, birth_data):
    """
    Validate transit data against birth data.
    
    Args:
        transit_data: Dictionary containing transit planetary data
        birth_data: Dictionary containing birth chart data
    
    Returns:
        bool: True if validation passes, False otherwise
    """
    try:
        # Check if all required planets are present in transit data
        required_planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
        for planet in required_planets:
            if planet not in transit_data:
                raise ValidationError(f"Missing required planet in transit data: {planet}")
        
        # Validate planet positions in transit data
        validate_planet_positions(transit_data)
        
        # Check that transit data is different from birth data
        if transit_data == birth_data['planets']:
            app_logger.warning("Transit data is identical to birth data")
        
        app_logger.info("Transit data validation passed")
        return True
    
    except ValidationError as e:
        app_logger.error(f"Transit data validation failed: {str(e)}")
        return False
    except Exception as e:
        app_logger.error(f"Unexpected error in transit data validation: {str(e)}")
        return False

def run_comprehensive_validation(chart_data):
    """
    Run comprehensive validation on all chart data.
    
    Args:
        chart_data: Complete chart data dictionary
    
    Returns:
        dict: Validation results with details of any errors found
    """
    validation_results = {
        'timestamp': datetime.datetime.now().isoformat(),
        'overall_result': True,
        'details': {}
    }
    
    # Validate chart data
    chart_valid = validate_chart_data(chart_data)
    validation_results['details']['chart_data'] = {
        'valid': chart_valid,
        'message': "Chart data validation passed" if chart_valid else "Chart data validation failed"
    }
    
    # Validate dasha calculations if present
    if 'dasha' in chart_data:
        dasha_valid = validate_dasha_calculations(chart_data['dasha'])
        validation_results['details']['dasha'] = {
            'valid': dasha_valid,
            'message': "Dasha validation passed" if dasha_valid else "Dasha validation failed"
        }
    
    # Validate transit data if present
    if 'transit' in chart_data:
        transit_valid = validate_transit_data(chart_data['transit'], chart_data)
        validation_results['details']['transit'] = {
            'valid': transit_valid,
            'message': "Transit validation passed" if transit_valid else "Transit validation failed"
        }
    
    # Check overall validation result
    validation_results['overall_result'] = all(detail['valid'] for detail in validation_results['details'].values())
    
    # Create error report if validation failed
    if not validation_results['overall_result']:
        error_data = {
            'validation_results': validation_results,
            'chart_data': chart_data
        }
        error_report_path = create_error_report(error_data)
        validation_results['error_report'] = error_report_path
    
    return validation_results
