from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import json
import pytz
import os
import shutil
from vedic_calculator.core import VedicCalculator
from vedic_calculator.yoga_system import YogaSystem
import logging
from utils.logger import app_logger, calc_logger, log_function_call, log_api_call
from utils.error_checker import validate_chart_data, validate_planet_positions, run_comprehensive_validation

app = Flask(__name__)
CORS(app)

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Set up Flask logger to use our custom logger
app.logger.handlers = []
for handler in app_logger.handlers:
    app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Load cities database
def load_cities():
    try:
        # First try to load the comprehensive cities database
        try:
            with open('data/cities.json', 'r', encoding='utf-8') as f:
                print("Loading cities database from:", f.name)
                cities_data = json.load(f)
                print(f"Loaded {len(cities_data)} cities")
                return cities_data
        except Exception as e:
            print(f"Error loading main cities database: {e}")
            
            # Fallback to custom cities database
            with open('data/custom_cities.json', 'r', encoding='utf-8') as f:
                print("Loading custom cities database from:", f.name)
                cities_data = json.load(f)
                cities = cities_data.get('cities', [])
                print(f"Loaded {len(cities)} cities")
                return cities
    except Exception as e:
        print(f"Error loading cities: {e}")
        return []

cities_db = load_cities()

# Load test profiles
def load_test_profiles():
    try:
        with open('data/test_profiles.json', 'r', encoding='utf-8') as f:
            print("Loading test profiles from:", f.name)
            profiles = json.load(f)
            print(f"Loaded {len(profiles)} test profiles")
            return profiles
    except Exception as e:
        print(f"Error loading test profiles: {e}")
        # Return some default test profiles if file doesn't exist
        return [
            {
                "name": "Albert Einstein",
                "date": "1879-03-14",
                "time": "11:30:00",
                "latitude": 48.4010822,
                "longitude": 9.987607599999999,
                "timezone": "Europe/Berlin"
            },
            {
                "name": "Mahatma Gandhi",
                "date": "1869-10-02",
                "time": "07:12:00",
                "latitude": 21.6458,
                "longitude": 69.9323,
                "timezone": "Asia/Kolkata"
            }
        ]

test_profiles = load_test_profiles()

@app.route('/calculate', methods=['POST'])
@log_api_call('calculate')
def calculate():
    """Endpoint for the frontend to calculate a chart"""
    try:
        app_logger.info("Received request to /calculate endpoint")
        data = request.json
        app_logger.debug(f"Request data: {json.dumps(data)}")
        
        # Format the data for our calculate_chart function
        chart_data = {
            'date': data.get('date'),
            'time': data.get('time'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'timezone': data.get('timezone')
            # Using only Lahiri ayanamsa and Whole Sign house system as required
        }
        
        app_logger.debug(f"Formatted chart data: {json.dumps(chart_data)}")
        
        # Call our existing calculate_chart function
        result = calculate_chart_internal(chart_data)
        
        # Validate the calculation results
        validation_results = run_comprehensive_validation(result)
        if not validation_results['overall_result']:
            app_logger.warning(f"Validation failed: {json.dumps(validation_results['details'])}")
            # We still return the result, but log the validation failure
            result['validation_warning'] = "Some validation checks failed. Results may not be accurate."
        
        # Log Shadbala data for debugging
        if 'shadbala' in result:
            calc_logger.info(f"Shadbala data calculated successfully")
            calc_logger.debug(f"Shadbala data: {json.dumps(result['shadbala'])}")
        else:
            app_logger.warning("Shadbala data not found in calculation result")
        
        # Log Vimsopaka Bala data for debugging
        if 'vimsopaka_bala' in result:
            calc_logger.info(f"Vimsopaka Bala data calculated successfully")
            calc_logger.debug(f"Vimsopaka Bala calculation details available: {bool(result.get('vimsopaka_bala_calculation_details'))}")
        else:
            app_logger.warning("Vimsopaka Bala data not found in calculation result")
        
        return result
    
    except Exception as e:
        error_message = str(e)
        app_logger.error(f"Error in calculate endpoint: {error_message}")
        return jsonify({'error': error_message}), 500

@app.route('/calculate_chart', methods=['POST'])
@log_api_call('calculate_chart')
def calculate_chart():
    """Original API endpoint for calculating a chart"""
    try:
        data = request.json
        app_logger.info(f"Received request to /calculate_chart endpoint")
        return calculate_chart_internal(data)
    except Exception as e:
        error_message = str(e)
        app_logger.error(f"Error processing request: {error_message}")
        return jsonify({'error': error_message}), 500

@log_function_call(calc_logger)
def calculate_chart_internal(data):
    """Internal function to calculate a chart from the provided data"""
    app_logger.info(f"Starting chart calculation")
    calc_logger.debug(f"Calculation input data: {json.dumps(data)}")
    
    # Get date and time components
    date_str = data.get('date')
    time_str = data.get('time')
    timezone = data.get('timezone', 'UTC')
    
    print(f"Date: {date_str}, Time: {time_str}, Timezone: {timezone}")
    
    # Combine date and time
    datetime_str = f"{date_str} {time_str}"
    
    # Parse the datetime string
    try:
        # Try parsing with seconds
        local_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            # Try parsing without seconds
            local_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        except ValueError:
            return jsonify({'error': 'Invalid date/time format'}), 400
    
    print(f"Parsed datetime: {local_time}")
    
    # Get timezone
    try:
        tz = pytz.timezone(timezone)
        local_time = tz.localize(local_time)
        print(f"Localized datetime: {local_time}")
    except Exception as e:
        return jsonify({'error': f'Invalid timezone: {str(e)}'}), 400
    
    # Get coordinates
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if latitude is None or longitude is None:
        return jsonify({'error': 'Latitude and longitude are required'}), 400
    
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return jsonify({'error': 'Invalid latitude or longitude'}), 400
    
    print(f"Coordinates: Lat {latitude}, Lon {longitude}")
    
    # Initialize calculator with Lahiri ayanamsa (only option supported)
    try:
        calculator = VedicCalculator(
            date=local_time,
            lat=latitude,
            lon=longitude,
            ayanamsa='Lahiri'  # Only using Lahiri ayanamsa
        )
        print("VedicCalculator initialized successfully")
    except Exception as e:
        error_message = str(e)
        print(f"Error initializing calculator: {error_message}")
        app_logger.error(f"Error initializing calculator: {error_message}")
        return jsonify({'error': f'Error initializing calculator: {error_message}'}), 500
    
    # Get planets, houses, and other data from the calculator
    try:
        # Get planets data
        planets = calculator.planets
        
        # Get houses data (Whole Sign system only)
        houses = calculator.houses
        
        # Get ascendant data
        ascendant = calculator.ascendant
        
        # Get special points
        special_points = calculator.special_points
        
        # Calculate dasha
        dasha = calculator.calculate_dasha()
        
        # Calculate vimshottari dasha
        vimshottari_dasha = calculator.calculate_vimshottari_dasha()
        
        # Calculate panchang
        panchang = calculator.calculate_panchang()
        
        # Calculate divisional charts
        divisional_charts = calculator.calculate_divisional_charts()
        
        # Detect yogas
        yogas = calculator.detect_yogas()
        
        # Get Ashtakavarga data
        ashtakavarga = {
            'prastarashtakavarga': calculator.get_prastarashtakavarga(),
            'sarvashtakavarga': calculator.get_sarvashtakavarga(),
            'strength': calculator.get_ashtakavarga_strength()
        }
        
        # Calculate Shadbala
        shadbala = calculator.calculate_shadbala()
        
        # Calculate Vimsopaka Bala
        vimsopaka_bala_calculation_details = calculator.calculate_vimsopaka_bala_details()
        vimsopaka_bala = calculator.calculate_vimsopaka_bala()
        
        # Debug: Print divisional charts structure
        if 'divisional_charts' in locals():
            print(f"Divisional charts keys: {list(divisional_charts.keys())}")
            if 'D1' in divisional_charts:
                print(f"D1 chart keys: {list(divisional_charts['D1'].keys())}")
                if 'planets' in divisional_charts['D1']:
                    print(f"D1 planets keys: {list(divisional_charts['D1']['planets'].keys())}")
                    if 'Sun' in divisional_charts['D1']['planets']:
                        print(f"D1 Sun data: {divisional_charts['D1']['planets']['Sun']}")
                else:
                    print("No 'planets' key found in D1 chart")
                    print(f"Full D1 chart structure: {divisional_charts['D1']}")
            else:
                print("No 'D1' key found in divisional_charts")
                print(f"Available keys in divisional_charts: {list(divisional_charts.keys())}")
        else:
            print("divisional_charts variable not found in locals()")
        
        print("All calculations completed successfully")
    except Exception as e:
        error_message = str(e)
        print(f"Error in calculations: {error_message}")
        app_logger.error(f"Error in calculations: {error_message}")
        return jsonify({'error': f'Error in calculations: {error_message}'}), 500
    
    # Format degrees for display
    def format_degrees(degree):
        """Format decimal degrees to degrees, minutes, seconds"""
        d = int(degree)
        m_float = (degree - d) * 60
        m = int(m_float)
        s = round((m_float - m) * 60)
        
        # Handle case where seconds round to 60
        if s == 60:
            s = 0
            m += 1
            if m == 60:
                m = 0
                d += 1
                
        return f"{d}° {m}' {s}\""
    
    # Format planets for display
    formatted_planets = {}
    for planet, data in planets.items():
        formatted_planets[planet] = {
            'longitude': data['longitude'],
            'sign': data['sign'],
            'degree': data['degree'],
            'formatted_degree': format_degrees(data['degree']),
            'house': data['house'],
            'nakshatra': data['nakshatra'],
            'isRetrograde': data['isRetrograde'],
            'dignity': data['dignity']
        }
    
    # Prepare chart data for D3.js visualization
    chart_data = {
        'ascendant': {
            'longitude': ascendant['longitude'],
            'sign': ascendant['sign'],
            'degree': ascendant['degree'],
            'formatted_degree': format_degrees(ascendant['degree']),
            'nakshatra': ascendant.get('nakshatra', ''),
            'pada': ascendant.get('pada', '')
        },
        'houses': {},
        'planets': {},
        'special_points': {}
    }
    
    # Format houses for chart
    for house_num, house_data in houses.items():
        chart_data['houses'][house_num] = {
            'sign': house_data['sign'],
            'start_longitude': house_data['start_longitude'],
            'end_longitude': house_data['end_longitude']
        }
    
    # Format planets for chart
    for planet, data in planets.items():
        chart_data['planets'][planet] = {
            'longitude': data['longitude'],
            'sign': data['sign'],
            'degree': data['degree'],
            'house': data['house'],
            'isRetrograde': data['isRetrograde'],
            'dignity': data['dignity']
        }
    
    # Format special points for chart
    for point, data in special_points.items():
        chart_data['special_points'][point] = {
            'longitude': data['longitude'],
            'sign': data['sign'],
            'degree': data['degree'],
            'house': data['house']
        }
    
    # Prepare response
    response = {
        'date': date_str,
        'time': time_str,
        'timezone': timezone,
        'latitude': latitude,
        'longitude': longitude,
        'ascendant': ascendant,
        'planets': formatted_planets,
        'houses': houses,
        'special_points': special_points,
        'dasha': dasha,
        'vimshottari_dasha': vimshottari_dasha,
        'panchang': panchang,
        'chart_data': chart_data,
        'divisional_charts': divisional_charts,
        'ashtakavarga': ashtakavarga,
        'shadbala': shadbala,
        'vimsopaka_bala': vimsopaka_bala,
        'vimsopaka_bala_calculation_details': vimsopaka_bala_calculation_details
    }
    
    # Calculate yogas using the YogaSystem
    try:
        yoga_system = YogaSystem(response)
        yogas = yoga_system.identify_all_yogas()
        response['yogas'] = yogas
        calc_logger.info(f"Identified {sum(len(yoga_list) for yoga_list in yogas.values())} yogas in the chart")
    except Exception as e:
        app_logger.error(f"Error calculating yogas in calculate_chart_internal: {str(e)}")
        # If there's an error, set empty yogas
        response['yogas'] = {
            'raja_yogas': [],
            'dhana_yogas': [],
            'pancha_mahapurusha_yogas': [],
            'nabhasa_yogas': [],
            'other_yogas': []
        }
    
    return response

@app.route('/divisional_charts', methods=['POST'])
def get_divisional_charts():
    """
    Calculate divisional charts (D1, D9, D12)
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['date', 'time', 'latitude', 'longitude']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Calculate chart
        result = calculate_chart_internal(data)
        
        # Check if result is a tuple (error response)
        if isinstance(result, tuple):
            return result
        
        # Return only the divisional charts
        return jsonify(result['divisional_charts'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/search_place', methods=['GET'])
def search_place():
    """Search for a place by name"""
    query = request.args.get('q', '').lower()
    
    if not query or len(query) < 2:
        return jsonify([])
    
    # Search in the cities database
    results = []
    
    if isinstance(cities_db, list):
        # If cities_db is a list of cities
        for city in cities_db:
            if query in city.get('name', '').lower():
                results.append({
                    'name': city.get('name', ''),
                    'country': city.get('country', ''),
                    'state': city.get('state', ''),
                    'latitude': city.get('lat', 0),
                    'longitude': city.get('lng', 0),
                    'timezone': city.get('timezone', 'UTC')
                })
    else:
        # If cities_db is a dictionary with city names as keys
        for city_name, city_data in cities_db.items():
            if query in city_name.lower():
                results.append({
                    'name': city_name,
                    'country': city_data.get('country', ''),
                    'state': city_data.get('state', ''),
                    'latitude': city_data.get('lat', 0),
                    'longitude': city_data.get('lng', 0),
                    'timezone': city_data.get('timezone', 'UTC')
                })
    
    # Limit results to avoid overwhelming the frontend
    return jsonify(results[:10])

@app.route('/validate_coordinates', methods=['POST'])
def validate_coordinates():
    """Validate coordinates and return timezone"""
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if latitude is None or longitude is None:
        return jsonify({'error': 'Latitude and longitude are required'}), 400
    
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return jsonify({'error': 'Invalid latitude or longitude'}), 400
    
    # Validate latitude and longitude ranges
    if latitude < -90 or latitude > 90:
        return jsonify({'error': 'Latitude must be between -90 and 90'}), 400
    
    if longitude < -180 or longitude > 180:
        return jsonify({'error': 'Longitude must be between -180 and 180'}), 400
    
    # For now, just return a default timezone
    # In a real app, you would use a service like Google Time Zone API
    return jsonify({
        'latitude': latitude,
        'longitude': longitude,
        'timezone': 'UTC'
    })

@app.route('/api/chart_data', methods=['POST'])
def get_chart_data():
    """Get chart data for D3.js visualization"""
    try:
        data = request.json
        result = calculate_chart_internal(data)
        
        # Extract just the chart_data from the result
        chart_data = result['chart_data']
        
        return jsonify(chart_data)
    except Exception as e:
        print(f"Error getting chart data: {str(e)}")
        app_logger.error(f"Error getting chart data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/test_profiles', methods=['GET'])
def get_test_profiles():
    """Return list of test profiles"""
    try:
        return jsonify(test_profiles)
    except Exception as e:
        error_message = str(e)
        app_logger.error(f"Error getting test profiles: {error_message}")
        return jsonify({'error': error_message}), 500

@app.route('/load_test_profile/<int:profile_id>', methods=['GET'])
def load_test_profile(profile_id):
    if profile_id < 0 or profile_id >= len(test_profiles):
        return jsonify({"error": "Profile not found"}), 404
    profile = test_profiles[profile_id]
    return jsonify(profile)

@app.route('/edit_test_profile/<int:profile_id>', methods=['POST'])
def edit_test_profile(profile_id):
    global test_profiles
    
    if profile_id < 0 or profile_id >= len(test_profiles):
        return jsonify({"error": "Profile not found"}), 404
    
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Update the profile
    test_profiles[profile_id] = data
    
    # Save to file
    try:
        with open('data/test_profiles.json', 'w', encoding='utf-8') as f:
            json.dump(test_profiles, f, indent=2)
        return jsonify({"success": True, "message": "Profile updated successfully"})
    except Exception as e:
        return jsonify({"error": f"Failed to save profile: {str(e)}"}), 500

@app.route('/add_test_profile', methods=['POST'])
def add_test_profile():
    global test_profiles
    
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Add the new profile
    test_profiles.append(data)
    
    # Save to file
    try:
        with open('data/test_profiles.json', 'w', encoding='utf-8') as f:
            json.dump(test_profiles, f, indent=2)
        return jsonify({"success": True, "message": "Profile added successfully", "profile_id": len(test_profiles) - 1})
    except Exception as e:
        return jsonify({"error": f"Failed to save profile: {str(e)}"}), 500

@app.route('/delete_test_profile/<int:profile_id>', methods=['DELETE'])
def delete_test_profile(profile_id):
    global test_profiles
    
    if profile_id < 0 or profile_id >= len(test_profiles):
        return jsonify({"error": "Profile not found"}), 404
    
    # Remove the profile
    deleted_profile = test_profiles.pop(profile_id)
    
    # Save to file
    try:
        with open('data/test_profiles.json', 'w', encoding='utf-8') as f:
            json.dump(test_profiles, f, indent=2)
        return jsonify({"success": True, "message": f"Profile '{deleted_profile['name']}' deleted successfully"})
    except Exception as e:
        # Restore the profile if saving fails
        test_profiles.insert(profile_id, deleted_profile)
        return jsonify({"error": f"Failed to delete profile: {str(e)}"}), 500

@app.route('/yogas', methods=['POST'])
@log_api_call('get_yogas')
def get_yogas():
    """
    Calculate yogas (astrological combinations)
    """
    try:
        app_logger.info("Calculating yogas (astrological combinations)")
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['date', 'time', 'latitude', 'longitude']
        for field in required_fields:
            if field not in data:
                app_logger.warning(f"Missing required field: {field}")
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Calculate chart
        result = calculate_chart_internal(data)
        
        # Check if result is a tuple (error response)
        if isinstance(result, tuple):
            return result
        
        # Use the new YogaSystem to identify yogas
        yoga_system = YogaSystem(result)
        yogas = yoga_system.identify_all_yogas()
        
        # Add the yogas to the result
        result['yogas'] = yogas
        
        # Log the number of yogas found
        calc_logger.info(f"Found {sum(len(yoga_list) for yoga_list in yogas.values())} yogas in the chart")
        for yoga_type, yoga_list in yogas.items():
            calc_logger.debug(f"{yoga_type}: {len(yoga_list)} yogas found")
        
        # Return only the yogas
        return jsonify(yogas)
    except Exception as e:
        error_message = str(e)
        app_logger.error(f"Error calculating yogas: {error_message}")
        return jsonify({'error': error_message}), 500

@app.route('/vimshottari_dasha', methods=['POST'])
def get_vimshottari_dasha():
    """
    Calculate Vimshottari Dasha
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['date', 'time', 'latitude', 'longitude']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Calculate chart
        result = calculate_chart_internal(data)
        
        # Check if result is a tuple (error response)
        if isinstance(result, tuple):
            return result
        
        # Return only the Vimshottari Dasha
        return jsonify(result['vimshottari_dasha'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_transits', methods=['GET'])
@log_api_call('get_transits')
def get_transits():
    """Calculate current planetary positions for transit overlay"""
    try:
        app_logger.info("Calculating current planetary positions for transit overlay")
        
        # Get current date and time in UTC
        now = datetime.now(pytz.UTC)
        
        # Format the data for calculation
        transit_data = {
            'date': now.strftime('%Y-%m-%d'),
            'time': now.strftime('%H:%M:%S'),
            'latitude': 0.0,  # Using 0,0 as default location for transit calculations
            'longitude': 0.0,
            'timezone': 'UTC'
        }
        
        app_logger.debug(f"Transit calculation input: {json.dumps(transit_data)}")
        
        # Calculate the transit positions
        calculator = VedicCalculator()
        result = calculator.calculate(
            transit_data['date'],
            transit_data['time'],
            transit_data['latitude'],
            transit_data['longitude'],
            transit_data['timezone'],
            ayanamsa='lahiri',
            house_system='whole_sign'
        )
        
        # Validate the transit data
        if not validate_planet_positions(result['planets']):
            app_logger.warning("Transit planet position validation failed")
            # We still continue, but log the warning
        
        # Extract only the planetary positions for transit overlay
        transit_positions = {}
        for planet, data in result['planets'].items():
            transit_positions[planet] = {
                'longitude': data['longitude'],
                'sign': data['sign'],
                'sign_num': data['sign_num'],
                'nakshatra': data['nakshatra'],
                'nakshatra_lord': data['nakshatra_lord'],
                'house': data['house'],
                'retrograde': data['retrograde']
            }
        
        calc_logger.info(f"Transit calculation completed successfully for {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        
        return jsonify({
            'success': True,
            'transits': transit_positions,
            'calculation_time': now.strftime('%Y-%m-%d %H:%M:%S %Z')
        })
    except Exception as e:
        app_logger.error(f"Error calculating transits: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/test', methods=['GET'])
def test():
    """Simple test endpoint to verify the server is working"""
    return jsonify({'status': 'ok', 'message': 'Server is working correctly'})

@app.route('/system/status', methods=['GET'])
@log_api_call('system_status')
def system_status():
    """
    Check the status of the application and return system information
    """
    try:
        # Get system information
        import platform
        import sys
        import psutil
        import os
        
        # Get memory usage
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        # Get disk usage for logs directory
        logs_path = os.path.join(os.path.dirname(__file__), 'logs')
        if os.path.exists(logs_path):
            _, _, free = shutil.disk_usage(logs_path)
            disk_free_gb = free / (1024 ** 3)
        else:
            disk_free_gb = "N/A"
        
        # Check if log files exist and get their sizes
        log_files = {}
        if os.path.exists(logs_path):
            for log_file in os.listdir(logs_path):
                if log_file.endswith('.log'):
                    file_path = os.path.join(logs_path, log_file)
                    log_files[log_file] = {
                        'size': os.path.getsize(file_path) / 1024,  # Size in KB
                        'last_modified': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                    }
        
        # Get recent errors from error log
        recent_errors = []
        error_log_path = os.path.join(logs_path, f'kundli_errors_{datetime.now().strftime("%Y%m%d")}.log')
        if os.path.exists(error_log_path):
            with open(error_log_path, 'r') as f:
                lines = f.readlines()
                # Get the last 10 error lines
                error_lines = [line for line in lines if 'ERROR' in line][-10:]
                recent_errors = error_lines
        
        status_data = {
            'status': 'running',
            'version': '1.0.0',
            'uptime': str(datetime.now() - datetime.fromtimestamp(process.create_time())),
            'system': {
                'python_version': sys.version,
                'platform': platform.platform(),
                'processor': platform.processor()
            },
            'resources': {
                'memory_usage_mb': memory_info.rss / (1024 * 1024),
                'disk_free_gb': disk_free_gb
            },
            'logs': {
                'log_files': log_files,
                'recent_errors': recent_errors
            }
        }
        
        return jsonify(status_data)
    except Exception as e:
        app_logger.error(f"Error in system status endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/system/logs', methods=['GET'])
@log_api_call('system_logs')
def system_logs():
    """
    View application logs
    """
    try:
        log_type = request.args.get('type', 'app')
        lines = int(request.args.get('lines', 100))
        
        # Limit the number of lines to prevent excessive memory usage
        if lines > 1000:
            lines = 1000
        
        logs_path = os.path.join(os.path.dirname(__file__), 'logs')
        
        # Determine which log file to read
        if log_type == 'app':
            log_file = f'kundli_app_{datetime.now().strftime("%Y%m%d")}.log'
        elif log_type == 'error':
            log_file = f'kundli_errors_{datetime.now().strftime("%Y%m%d")}.log'
        elif log_type == 'calc':
            log_file = f'kundli_calculations_{datetime.now().strftime("%Y%m%d")}.log'
        else:
            return jsonify({'error': 'Invalid log type'}), 400
        
        log_path = os.path.join(logs_path, log_file)
        
        # Check if log file exists
        if not os.path.exists(log_path):
            return jsonify({
                'log_type': log_type,
                'log_file': log_file,
                'exists': False,
                'message': 'Log file does not exist'
            })
        
        # Read the log file
        with open(log_path, 'r') as f:
            log_lines = f.readlines()
        
        # Get the last N lines
        last_lines = log_lines[-lines:] if lines < len(log_lines) else log_lines
        
        return jsonify({
            'log_type': log_type,
            'log_file': log_file,
            'exists': True,
            'total_lines': len(log_lines),
            'lines_returned': len(last_lines),
            'content': last_lines
        })
    except Exception as e:
        app_logger.error(f"Error in system logs endpoint: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
