from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import json
import pytz
from vedic_calculator.core import VedicCalculator

app = Flask(__name__)
CORS(app)

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

@app.route('/calculate', methods=['POST'])
def calculate():
    """Endpoint for the frontend to calculate a chart"""
    try:
        data = request.json
        
        # Format the data for our calculate_chart function
        chart_data = {
            'date': data.get('date'),
            'time': data.get('time'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'timezone': data.get('timezone'),
            'ayanamsa': 'Lahiri',  # Default to Lahiri ayanamsa
            'houseSystem': 'W'     # Default to Whole Sign house system
        }
        
        # Call our existing calculate_chart function
        return calculate_chart_internal(chart_data)
    
    except Exception as e:
        print(f"Error in calculate endpoint: {str(e)}")
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
    
    # Get ayanamsa and house system
    ayanamsa = data.get('ayanamsa', 'Lahiri')
    house_system = data.get('houseSystem', 'W')
    
    print(f"Ayanamsa: {ayanamsa}, House System: {house_system}")
    
    # Initialize calculator
    try:
        calculator = VedicCalculator(
            date=local_time,
            lat=latitude,
            lon=longitude,
            ayanamsa=ayanamsa
        )
        print("VedicCalculator initialized successfully")
    except Exception as e:
        print(f"Error initializing calculator: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error initializing calculator: {str(e)}'}), 500
    
    # Calculate houses
    try:
        houses = calculator.calculate_houses()
        print("Houses calculated successfully")
    except Exception as e:
        print(f"Error calculating houses: {str(e)}")
        houses = {}
    
    # Calculate planets
    planets = {}
    try:
        for planet in calculator.PLANET_IDS.keys():
            print(f"Calculating position for {planet}")
            planets[planet] = calculator.get_planet_position(planet)
        print("Planets calculated successfully")
    except Exception as e:
        print(f"Error calculating planets: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Calculate panchang
    try:
        panchang = calculator.calculate_panchang()
        print("Panchang calculated successfully")
    except Exception as e:
        print(f"Error calculating panchang: {str(e)}")
        import traceback
        traceback.print_exc()
        panchang = {}
    
    # Calculate upagrahas
    try:
        upagrahas = calculator.calculate_upagrahas()
        print("Upagrahas calculated successfully")
    except Exception as e:
        print(f"Error calculating upagrahas: {str(e)}")
        import traceback
        traceback.print_exc()
        upagrahas = {}
    
    # Calculate Vimshottari Dasha
    try:
        dasha = calculator.calculate_vimshottari_dasha()
        print("Vimshottari Dasha calculated successfully")
    except Exception as e:
        print(f"Error in calculate_vimshottari_dasha: {str(e)}")
        import traceback
        traceback.print_exc()
        dasha = []
    
    # Prepare response
    response = {
        'date': date_str,
        'time': time_str,
        'timezone': timezone,
        'latitude': latitude,
        'longitude': longitude,
        'ayanamsa': ayanamsa,
        'houses': houses,
        'planets': planets,
        'panchang': panchang,
        'upagrahas': upagrahas,
        'dasha': dasha
    }
    
    return jsonify(response)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_place', methods=['GET'])
def search_place():
    query = request.args.get('q', '').lower().strip()
    print(f"Searching for: {query}")
    if len(query) < 2:
        return jsonify([])
    
    matches = []
    try:
        # Check if cities_db is a list or a dictionary
        if isinstance(cities_db, list):
            # Handle list format (custom_cities.json)
            for city in cities_db:
                city_name = city.get('name', '').lower()
                city_display = city.get('display', '').lower()
                
                if query in city_name or query in city_display:
                    matches.append({
                        'name': city.get('display', city.get('name', '')),
                        'lat': city.get('lat'),
                        'lon': city.get('lon'),
                        'timezone': city.get('timezone')
                    })
        else:
            # Handle dictionary format (cities.json)
            for city_id, city_data in cities_db.items():
                city_name = city_data.get('name', '').lower()
                country = city_data.get('country', '').lower()
                
                # Search in both city name and country
                if query in city_name or query in country:
                    display_name = f"{city_data.get('name')}, {city_data.get('country')}"
                    
                    # Handle different longitude field names (lon vs lng)
                    longitude = city_data.get('lon')
                    if longitude is None:
                        longitude = city_data.get('lng')
                    
                    matches.append({
                        'name': display_name,
                        'lat': city_data.get('lat'),
                        'lon': longitude,
                        'timezone': city_data.get('timezone')
                    })
                
                # Limit results to prevent overwhelming the UI
                if len(matches) >= 20:
                    break
        
        print(f"Found {len(matches)} matches for '{query}'")
        return jsonify(matches)
    except Exception as e:
        print(f"Error during search: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/validate_coordinates', methods=['POST'])
def validate_coordinates():
    data = request.get_json()
    
    try:
        latitude = float(data.get('latitude', 0))
        longitude = float(data.get('longitude', 0))
        
        # Validate coordinate ranges
        if not (-90 <= latitude <= 90):
            return jsonify({'valid': False, 'error': 'Latitude must be between -90° and 90°'}), 400
        
        if not (-180 <= longitude <= 180):
            return jsonify({'valid': False, 'error': 'Longitude must be between -180° and 180°'}), 400
        
        # Try to get timezone for these coordinates
        from timezonefinder import TimezoneFinder
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lat=latitude, lng=longitude)
        
        if not timezone:
            return jsonify({'valid': True, 'warning': 'Could not determine timezone for these coordinates'}), 200
        
        return jsonify({'valid': True, 'timezone': timezone}), 200
        
    except ValueError:
        return jsonify({'valid': False, 'error': 'Invalid coordinate format'}), 400
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 500

@app.route('/ayanamsa_options', methods=['GET'])
def get_ayanamsa_options():
    # Return available ayanamsa options
    options = list(VedicCalculator.AYANAMSA_OPTIONS.keys())
    return jsonify(options)

@app.route('/house_system_options', methods=['GET'])
def get_house_system_options():
    # Return available house system options
    options = {
        'P': 'Placidus',
        'K': 'Koch',
        'O': 'Porphyrius',
        'R': 'Regiomontanus',
        'C': 'Campanus',
        'E': 'Equal',
        'W': 'Whole sign',
        'B': 'Alcabitus',
        'M': 'Morinus'
    }
    return jsonify(options)

if __name__ == '__main__':
    app.run(debug=True)
