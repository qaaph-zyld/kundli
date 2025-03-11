from flask import Flask, request, jsonify
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
        with open('data/custom_cities.json', 'r', encoding='utf-8') as f:
            print("Loading cities database from:", f.name)
            cities = json.load(f)
            print(f"Loaded {len(cities)} cities")
            return cities
    except Exception as e:
        print(f"Error loading cities: {e}")
        return []

cities_db = load_cities()

@app.route('/calculate_chart', methods=['POST'])
def calculate_chart():
    try:
        data = request.json
        
        # Get date and time components
        date_str = data.get('date')
        time_str = data.get('time')
        timezone = data.get('timezone', 'UTC')
        
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
        
        # Set the timezone
        local_tz = pytz.timezone(timezone)
        local_time = local_tz.localize(local_time)
        
        # Get coordinates
        latitude = float(data.get('latitude', 0))
        longitude = float(data.get('longitude', 0))
        
        # Get ayanamsa and house system
        ayanamsa = data.get('ayanamsa', 'Lahiri')
        house_system = data.get('houseSystem', 'W')
        
        # Initialize calculator
        try:
            calculator = VedicCalculator(local_time, latitude, longitude, ayanamsa)
            
            # Calculate houses
            try:
                houses = calculator.calculate_houses(house_system)
                print("Houses calculated successfully")
            except Exception as e:
                print(f"Error calculating houses: {str(e)}")
                import traceback
                traceback.print_exc()
                houses = {}
            
            # Calculate planets
            try:
                planets = {}
                for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']:
                    planets[planet] = calculator.get_planet_position(planet)
                print("Planets calculated successfully")
            except Exception as e:
                print(f"Error calculating planets: {str(e)}")
                import traceback
                traceback.print_exc()
                planets = {}
            
            # Calculate Panchang
            try:
                panchang = calculator.calculate_panchang()
                print("Panchang calculated successfully")
            except Exception as e:
                print(f"Error calculating panchang: {str(e)}")
                import traceback
                traceback.print_exc()
                panchang = {}
            
            # Calculate Upagrahas
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
                print(f"Error calculating vimshottari dasha: {str(e)}")
                import traceback
                traceback.print_exc()
                dasha = []
            
            # Prepare response
            result = {
                'date': local_time.strftime('%Y-%m-%d'),
                'time': local_time.strftime('%H:%M:%S'),
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
            
            return jsonify(result)
        except Exception as e:
            print(f"Error calculating chart: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return "Welcome to the Jyotish API"

@app.route('/search_place', methods=['GET'])
def search_place():
    query = request.args.get('q', '').lower()
    print(f"Searching for: {query}")
    if len(query) < 2:
        return jsonify([])
    
    matches = []
    try:
        for city in cities_db:
            if query in city['name'].lower():
                matches.append({
                    'name': city['display'],
                    'lat': city['lat'],
                    'lon': city['lon'],
                    'timezone': city['timezone']
                })
        print(f"Found {len(matches)} matches")
        return jsonify(matches)
    except Exception as e:
        print(f"Error during search: {e}")
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
