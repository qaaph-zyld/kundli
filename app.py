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
        
        # Convert to UTC
        utc_time = local_time.astimezone(pytz.UTC)
        
        # Get coordinates
        try:
            latitude = float(data.get('latitude', 0))
            longitude = float(data.get('longitude', 0))
        except ValueError:
            return jsonify({'error': 'Invalid coordinate format'}), 400
        
        # Get ayanamsa and house system if provided
        ayanamsa = data.get('ayanamsa', 'Lahiri')
        house_system = data.get('houseSystem', 'W')  # Default to Whole Sign houses
        
        # Calculate chart data
        calculator = VedicCalculator(utc_time, latitude, longitude, ayanamsa)
        
        # Get house cusps
        house_cusps = calculator.get_house_cusps(house_system)
        ascendant_deg = house_cusps[0]
        
        # Calculate all planet positions
        planet_positions = {}
        for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']:
            planet_positions[planet] = calculator.get_planet_position(planet)
        
        # Calculate Panchang details
        panchang = calculator.calculate_panchang()
        
        # Calculate Upagrahas
        upagrahas = calculator.calculate_upagrahas()
        
        # Calculate Vimshottari Dasha
        dashas = calculator.calculate_vimshottari_dasha()
        
        # Calculate traditional time units
        local_hour = local_time.hour + local_time.minute/60.0 + local_time.second/3600.0
        ghati, vighati, pal = calculator.convert_to_ghati_pal(local_hour)
        
        # Format response
        chart_data = {
            'ascendant': {
                'longitude': float(ascendant_deg),
                'sign': calculator.ZODIAC_SIGNS[int(ascendant_deg / 30)],
                'degree': float(ascendant_deg % 30),
                'nakshatra': calculator.get_nakshatra(ascendant_deg)[0],
                'pada': calculator.get_nakshatra(ascendant_deg)[1]
            },
            'planets': [],
            'houses': [],
            'panchang': panchang,
            'upagrahas': upagrahas,
            'dashas': dashas,
            'timeInfo': {
                'local': local_time.strftime('%Y-%m-%d %H:%M:%S %Z'),
                'utc': utc_time.strftime('%Y-%m-%d %H:%M:%S %Z'),
                'ghati': ghati,
                'vighati': vighati,
                'pal': pal,
                'ayanamsa': calculator._calculate_ayanamsa()
            }
        }
        
        # Add planet data
        for planet_name, planet_data in planet_positions.items():
            chart_data['planets'].append({
                'name': planet_name,
                'sign': planet_data['sign'],
                'degree': planet_data['degree'],
                'longitude': planet_data['longitude'],
                'dignity': planet_data['dignity'],
                'nakshatra': planet_data['nakshatra'],
                'pada': planet_data['pada'],
                'isRetrograde': planet_data.get('is_retrograde', False)
            })
        
        # Add house data
        for i, cusp in enumerate(house_cusps, 1):
            sign_num = int(cusp / 30)
            chart_data['houses'].append({
                'number': i,
                'longitude': float(cusp),
                'sign': calculator.ZODIAC_SIGNS[sign_num],
                'degree': float(cusp % 30)
            })
        
        return jsonify(chart_data)
        
    except Exception as e:
        print(f"Error calculating chart: {e}")
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
