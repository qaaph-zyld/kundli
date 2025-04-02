"""
Logger utility for the Vedic Kundli Calculator.
This module provides logging functionality to track application behavior and errors.
"""

import os
import logging
import datetime
import json
from functools import wraps
import time

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Configure main application logger
app_logger = logging.getLogger('kundli_app')
app_logger.setLevel(logging.DEBUG)

# Create file handler for general logs
log_file = os.path.join(logs_dir, f'kundli_app_{datetime.datetime.now().strftime("%Y%m%d")}.log')
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Create file handler specifically for errors
error_log_file = os.path.join(logs_dir, f'kundli_errors_{datetime.datetime.now().strftime("%Y%m%d")}.log')
error_file_handler = logging.FileHandler(error_log_file)
error_file_handler.setLevel(logging.ERROR)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

# Create formatters and add them to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
error_file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
app_logger.addHandler(file_handler)
app_logger.addHandler(error_file_handler)
app_logger.addHandler(console_handler)

# Create a separate logger for calculation performance
calc_logger = logging.getLogger('kundli_calculations')
calc_logger.setLevel(logging.DEBUG)

# Create file handler for calculation logs
calc_log_file = os.path.join(logs_dir, f'kundli_calculations_{datetime.datetime.now().strftime("%Y%m%d")}.log')
calc_file_handler = logging.FileHandler(calc_log_file)
calc_file_handler.setLevel(logging.DEBUG)
calc_file_handler.setFormatter(formatter)
calc_logger.addHandler(calc_file_handler)

def log_function_call(logger=app_logger):
    """
    Decorator to log function calls, arguments, return values, and execution time.
    
    Args:
        logger: The logger to use (default: app_logger)
    
    Returns:
        Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            start_time = time.time()
            
            # Log function call with arguments
            arg_str = ', '.join([repr(a) for a in args] + [f"{k}={repr(v)}" for k, v in kwargs.items()])
            logger.debug(f"Calling {func_name}({arg_str})")
            
            try:
                # Call the function
                result = func(*args, **kwargs)
                
                # Log execution time
                execution_time = time.time() - start_time
                logger.debug(f"{func_name} completed in {execution_time:.4f} seconds")
                
                # Log return value (truncate if too large)
                result_str = repr(result)
                if len(result_str) > 1000:
                    result_str = result_str[:997] + "..."
                logger.debug(f"{func_name} returned: {result_str}")
                
                return result
            except Exception as e:
                # Log exception
                logger.error(f"Exception in {func_name}: {str(e)}")
                raise
        
        return wrapper
    
    return decorator

def log_api_call(endpoint):
    """
    Decorator to log API calls, request data, response data, and execution time.
    
    Args:
        endpoint: The name of the API endpoint
    
    Returns:
        Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            from flask import request
            
            start_time = time.time()
            
            # Log request
            request_data = {}
            if request.method == 'GET':
                request_data = dict(request.args)
            elif request.method in ['POST', 'PUT']:
                if request.is_json:
                    request_data = request.get_json()
                else:
                    request_data = dict(request.form)
            
            app_logger.info(f"API Call: {endpoint} - {request.method} - {json.dumps(request_data)}")
            
            try:
                # Call the function
                result = func(*args, **kwargs)
                
                # Log execution time
                execution_time = time.time() - start_time
                app_logger.info(f"API {endpoint} completed in {execution_time:.4f} seconds")
                
                return result
            except Exception as e:
                # Log exception
                app_logger.error(f"API Exception in {endpoint}: {str(e)}")
                raise
        
        return wrapper
    
    return decorator

def create_error_report(error_data):
    """
    Create a detailed error report and save it to a JSON file.
    
    Args:
        error_data: Dictionary containing error details
    
    Returns:
        str: Path to the error report file
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(logs_dir, f'error_report_{timestamp}.json')
    
    with open(report_file, 'w') as f:
        json.dump(error_data, f, indent=2)
    
    app_logger.info(f"Error report created: {report_file}")
    return report_file

def check_calculation_accuracy(calculated_value, expected_value, tolerance=0.0001, description=""):
    """
    Check if a calculated value matches an expected value within a tolerance.
    
    Args:
        calculated_value: The value calculated by the application
        expected_value: The expected correct value
        tolerance: Acceptable difference between values (default: 0.0001)
        description: Description of what is being checked
    
    Returns:
        bool: True if the values match within tolerance, False otherwise
    """
    if isinstance(calculated_value, (int, float)) and isinstance(expected_value, (int, float)):
        difference = abs(calculated_value - expected_value)
        result = difference <= tolerance
        
        if result:
            calc_logger.debug(f"ACCURACY CHECK PASSED: {description} - {calculated_value} matches {expected_value} (diff: {difference})")
        else:
            calc_logger.error(f"ACCURACY CHECK FAILED: {description} - {calculated_value} does not match {expected_value} (diff: {difference})")
        
        return result
    else:
        result = calculated_value == expected_value
        
        if result:
            calc_logger.debug(f"ACCURACY CHECK PASSED: {description} - Values match")
        else:
            calc_logger.error(f"ACCURACY CHECK FAILED: {description} - {calculated_value} does not match {expected_value}")
        
        return result
