from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import json
import pytz
from vedic_calculator.core import VedicCalculator
import logging

app = Flask(__name__)
CORS(app)

# Set up logging
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
def calculate():
    """Endpoint for the frontend to calculate a chart"""
    try:
        print("Received request to /calculate endpoint")
        data = request.json
        print(f"Request data: {data}")
        
        # Format the data for our calculate_chart function
        chart_data = {
            'date': data.get('date'),
            'time': data.get('time'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'timezone': data.get('timezone')
            # Using only Lahiri ayanamsa and Whole Sign house system as required
        }
        
        print(f"Formatted chart data: {chart_data}")
        
        # Call our existing calculate_chart function
        result = calculate_chart_internal(chart_data)
        
        # Log Shadbala data for debugging
        if 'shadbala' in result:
            app.logger.info(f"Shadbala data: {result['shadbala']}")
        else:
            app.logger.warning("Shadbala data not found in calculation result")
        
        return result
    
    except Exception as e:
        app.logger.error(f"Error in calculate endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/calculate_chart', methods=['POST'])
def calculate_chart():
    """Original API endpoint for calculating a chart"""
    try:
        data = request.json
        return calculate_chart_internal(data)
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

def calculate_chart_internal(data):
    """Internal function to calculate a chart from the provided data"""
    print(f"Received data: {data}")
    
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
        print(f"Error initializing calculator: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error initializing calculator: {str(e)}'}), 500
    
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
        
        print("All calculations completed successfully")
    except Exception as e:
        print(f"Error in calculations: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error in calculations: {str(e)}'}), 500
    
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
        'yogas': yogas,
        'ashtakavarga': ashtakavarga
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
        chart_data = json.loads(result.data)['chart_data']
        
        return jsonify(chart_data)
    except Exception as e:
        print(f"Error getting chart data: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/test_profiles', methods=['GET'])
def get_test_profiles():
    return jsonify(test_profiles)

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
def get_yogas():
    """
    Calculate yogas (astrological combinations)
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
        
        # Return only the yogas
        return jsonify(result['yogas'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@app.route('/test', methods=['GET'])
def test():
    """Simple test endpoint to verify the server is working"""
    return jsonify({'status': 'ok', 'message': 'Server is working correctly'})

if __name__ == '__main__':
    app.run(debug=True)
