from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import pytz
import math
import json
import os

app = Flask(__name__)

# Load cities database
with open(os.path.join(os.path.dirname(__file__), 'data', 'cities.json'), 'r', encoding='utf-8') as f:
    CITIES_DB = json.load(f)

# Path to stored kundlis
KUNDLIS_FILE = os.path.join(os.path.dirname(__file__), 'data', 'stored_kundlis.json')

def load_stored_kundlis():
    if os.path.exists(KUNDLIS_FILE):
        with open(KUNDLIS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"kundlis": []}

def save_kundli(kundli_data):
    stored = load_stored_kundlis()
    
    # Check if kundli with same name exists
    for idx, k in enumerate(stored['kundlis']):
        if k['name'] == kundli_data['name']:
            stored['kundlis'][idx] = kundli_data
            break
    else:
        stored['kundlis'].append(kundli_data)
    
    with open(KUNDLIS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stored, f, indent=4)

def search_cities(query):
    """Search cities in our database"""
    query = query.lower()
    matches = []
    for city in CITIES_DB['cities']:
        if query in city['name'].lower():
            matches.append({
                'name': city['display'],
                'lat': city['lat'],
                'lon': city['lon'],
                'timezone': city['timezone']
            })
    return matches[:10]  # Limit to 10 results for better performance

class VedicCalculator:
    def __init__(self, date, lat=0, lon=0):
        self.date = date
        self.lat = float(lat) if lat else 0
        self.lon = float(lon) if lon else 0
        
        # J2000 epoch
        self.j2000 = datetime(2000, 1, 1, 12, 0, tzinfo=pytz.UTC)
        
    def get_julian_date(self):
        """Convert datetime to Julian Date"""
        time_diff = self.date - self.j2000
        return 2451545.0 + time_diff.days + time_diff.seconds / 86400.0
    
    def calculate_ayanamsa(self):
        """Calculate Lahiri ayanamsa"""
        jd = self.get_julian_date()
        t = (jd - 2451545.0) / 36525  # Julian centuries since J2000
        return 23.636953 + 0.017314 * t  # Lahiri ayanamsa formula

    def get_sun_position(self):
        """Simplified Sun position calculation"""
        jd = self.get_julian_date()
        n = jd - 2451545.0
        
        # Mean elements
        L = 280.460 + 0.9856474 * n  # Mean longitude
        g = 357.528 + 0.9856003 * n  # Mean anomaly
        
        # Convert to radians
        g_rad = math.radians(g)
        
        # Ecliptic longitude
        lambda_sun = L + 1.915 * math.sin(g_rad) + 0.020 * math.sin(2 * g_rad)
        
        # Convert to sidereal (subtract ayanamsa)
        lambda_sun -= self.calculate_ayanamsa()
        
        # Normalize to 0-360 range
        lambda_sun = lambda_sun % 360
        if lambda_sun < 0:
            lambda_sun += 360
            
        return lambda_sun
    
    def get_moon_position(self):
        """Simplified Moon position calculation"""
        jd = self.get_julian_date()
        n = jd - 2451545.0
        
        # Mean elements
        L = 218.316 + 13.176396 * n  # Mean longitude
        M = 134.963 + 13.064993 * n  # Mean anomaly
        F = 93.272 + 13.229350 * n   # Argument of latitude
        
        # Convert to radians
        L_rad = math.radians(L)
        M_rad = math.radians(M)
        F_rad = math.radians(F)
        
        # Simplified perturbations
        lambda_moon = L + 6.289 * math.sin(M_rad)
        
        # Convert to sidereal
        lambda_moon -= self.calculate_ayanamsa()
        
        # Normalize to 0-360 range
        lambda_moon = lambda_moon % 360
        if lambda_moon < 0:
            lambda_moon += 360
            
        return lambda_moon

def get_zodiac_sign(degrees):
    zodiac_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    sign_num = int(degrees / 30)
    return zodiac_signs[sign_num]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_place', methods=['GET'])
def search_place():
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify([])
    locations = search_cities(query)
    return jsonify(locations)

@app.route('/get_saved_kundlis', methods=['GET'])
def get_saved_kundlis():
    stored = load_stored_kundlis()
    return jsonify(stored)

@app.route('/calculate', methods=['POST'])
def calculate_kundli():
    try:
        data = request.json
        birth_date = datetime.strptime(data['date'], '%Y-%m-%d')
        birth_time = datetime.strptime(data['time'], '%H:%M').time()
        birth_datetime = datetime.combine(birth_date, birth_time)
        
        # Convert to UTC
        local_tz = pytz.timezone(data.get('timezone', 'UTC'))
        local_dt = local_tz.localize(birth_datetime)
        utc_dt = local_dt.astimezone(pytz.UTC)
        
        # Create calculator
        calc = VedicCalculator(
            utc_dt,
            data.get('latitude', 0),
            data.get('longitude', 0)
        )
        
        # Calculate positions
        sun_long = calc.get_sun_position()
        moon_long = calc.get_moon_position()
        
        # Basic planetary positions (simplified)
        result = {
            'Sun': {
                'sign': get_zodiac_sign(sun_long),
                'degree': round(sun_long % 30, 2)
            },
            'Moon': {
                'sign': get_zodiac_sign(moon_long),
                'degree': round(moon_long % 30, 2)
            }
        }
        
        # Add placeholder positions for other planets
        other_planets = ['Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
        base_degrees = {
            'Mars': 45,
            'Mercury': 90,
            'Jupiter': 135,
            'Venus': 180,
            'Saturn': 225,
            'Rahu': 270,
            'Ketu': 90
        }
        
        for planet in other_planets:
            base_deg = (base_degrees[planet] + sun_long) % 360
            result[planet] = {
                'sign': get_zodiac_sign(base_deg),
                'degree': round(base_deg % 30, 2)
            }
        
        # Save the kundli data
        kundli_data = {
            'name': data['name'],
            'date': data['date'],
            'time': data['time'],
            'place': data['place'],
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'timezone': data.get('timezone', 'UTC'),
            'planets': result
        }
        save_kundli(kundli_data)
            
        return jsonify({
            'success': True,
            'planets': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
