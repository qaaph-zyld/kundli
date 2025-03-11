from datetime import datetime
from typing import List, Dict, Tuple, Any, Optional
import math
import swisseph as swe
import pytz

# Planet IDs in Swiss Ephemeris
PLANET_IDS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Rahu': swe.MEAN_NODE,  # North Node
    'Ketu': None,  # South Node, calculated from Rahu
    'Uranus': swe.URANUS,
    'Neptune': swe.NEPTUNE,
    'Pluto': swe.PLUTO
}

# Upagraha calculations
UPAGRAHA_LONGITUDES = {
    'Dhuma': 133.0,
    'Vyatipata': 313.0,
    'Parivesha': 133.0,
    'Indrachapa': 313.0,
    'Upaketu': 313.0
}

class VedicCalculator:
    ZODIAC_SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    
    NAKSHATRAS = [
        ('Ashwini', 'Ashwini Kumaras'),
        ('Bharani', 'Yama'),
        ('Krittika', 'Agni'),
        ('Rohini', 'Brahma'),
        ('Mrigashira', 'Chandra'),
        ('Ardra', 'Rudra'),
        ('Punarvasu', 'Aditi'),
        ('Pushya', 'Brihaspati'),
        ('Ashlesha', 'Sarpa'),
        ('Magha', 'Pitris'),
        ('Purva Phalguni', 'Bhaga'),
        ('Uttara Phalguni', 'Aryaman'),
        ('Hasta', 'Savitar'),
        ('Chitra', 'Tvashtar'),
        ('Swati', 'Vayu'),
        ('Vishakha', 'Indra-Agni'),
        ('Anuradha', 'Mitra'),
        ('Jyeshtha', 'Indra'),
        ('Mula', 'Nirrti'),
        ('Purva Ashadha', 'Apas'),
        ('Uttara Ashadha', 'Vishvedevas'),
        ('Shravana', 'Vishnu'),
        ('Dhanishta', 'Vasus'),
        ('Shatabhisha', 'Varuna'),
        ('Purva Bhadrapada', 'Ajaikapada'),
        ('Uttara Bhadrapada', 'Ahirbudhnya'),
        ('Revati', 'Pushan')
    ]

    # Tithi names
    TITHIS = [
        'Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami',
        'Shashthi', 'Saptami', 'Ashtami', 'Navami', 'Dashami',
        'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Purnima/Amavasya'
    ]

    # Karana names
    KARANAS = [
        'Bava', 'Balava', 'Kaulava', 'Taitila', 'Garija',
        'Vanija', 'Vishti', 'Shakuni', 'Chatushpada', 'Naga'
    ]

    # Yoga names
    YOGAS = [
        'Vishkambha', 'Priti', 'Ayushman', 'Saubhagya', 'Shobhana',
        'Atiganda', 'Sukarman', 'Dhriti', 'Shula', 'Ganda',
        'Vriddhi', 'Dhruva', 'Vyaghata', 'Harshana', 'Vajra',
        'Siddhi', 'Vyatipata', 'Variyan', 'Parigha', 'Shiva',
        'Siddha', 'Sadhya', 'Shubha', 'Shukla', 'Brahma',
        'Indra', 'Vaidhriti'
    ]

    # Various Ayanamsa options
    AYANAMSA_OPTIONS = {
        'Lahiri': swe.SIDM_LAHIRI,
        'Raman': swe.SIDM_RAMAN,
        'KP': swe.SIDM_KRISHNAMURTI,
        'Yukteshwar': swe.SIDM_YUKTESHWAR,
        'Fagan/Bradley': swe.SIDM_FAGAN_BRADLEY
    }
    
    # Planet dignities 
    DIGNITIES = {
        'Sun': {'exalted': 'Aries', 'moolatrikona': 'Leo', 'own': ['Leo'], 
               'friend': ['Moon', 'Mars', 'Jupiter'], 'enemy': ['Venus', 'Saturn']},
        'Moon': {'exalted': 'Taurus', 'moolatrikona': 'Taurus', 'own': ['Cancer'], 
                'friend': ['Sun', 'Mercury'], 'enemy': []},
        'Mercury': {'exalted': 'Virgo', 'moolatrikona': 'Virgo', 'own': ['Gemini', 'Virgo'], 
                   'friend': ['Sun', 'Venus'], 'enemy': ['Moon']},
        'Venus': {'exalted': 'Pisces', 'moolatrikona': 'Libra', 'own': ['Taurus', 'Libra'], 
                 'friend': ['Mercury', 'Saturn'], 'enemy': ['Sun', 'Moon']},
        'Mars': {'exalted': 'Capricorn', 'moolatrikona': 'Aries', 'own': ['Aries', 'Scorpio'], 
                'friend': ['Sun', 'Moon', 'Jupiter'], 'enemy': ['Mercury']},
        'Jupiter': {'exalted': 'Cancer', 'moolatrikona': 'Sagittarius', 'own': ['Sagittarius', 'Pisces'], 
                   'friend': ['Sun', 'Moon', 'Mars'], 'enemy': ['Mercury', 'Venus']},
        'Saturn': {'exalted': 'Libra', 'moolatrikona': 'Aquarius', 'own': ['Capricorn', 'Aquarius'], 
                  'friend': ['Mercury', 'Venus'], 'enemy': ['Sun', 'Moon', 'Mars']},
        'Rahu': {'exalted': 'Gemini', 'moolatrikona': None, 'own': [], 
                'friend': ['Venus', 'Saturn'], 'enemy': ['Sun', 'Moon']},
        'Ketu': {'exalted': 'Sagittarius', 'moolatrikona': None, 'own': [], 
                'friend': ['Venus', 'Saturn'], 'enemy': ['Sun', 'Moon']}
    }

    def __init__(self, date: datetime, lat: float = 0.0, lon: float = 0.0, ayanamsa: str = 'Lahiri'):
        # Set ephemeris path (update with correct path if needed)
        swe.set_ephe_path(None)  # Uses internal ephemeris
        
        # Store input parameters
        self.date = date
        self.lat = lat
        self.lon = lon
        
        # Convert date to Julian day
        self.jd = self._datetime_to_jd(date)
        
        # Set ayanamsa
        self.ayanamsa = ayanamsa
        swe.set_sid_mode(self.AYANAMSA_OPTIONS.get(ayanamsa, swe.SIDM_LAHIRI))

    def calculate_panchang(self) -> Dict[str, Any]:
        """Calculate Panchang (Tithi, Nakshatra, Yoga, Karana) details."""
        # Get Sun and Moon positions
        sun_pos = self.get_planet_position('Sun')['longitude']
        moon_pos = self.get_planet_position('Moon')['longitude']

        # Calculate Tithi
        moon_sun_diff = (moon_pos - sun_pos) % 360
        tithi_num = int(moon_sun_diff / 12)
        tithi_name = self.TITHIS[tithi_num % 15]
        
        # Calculate Karana
        karana_num = int(moon_sun_diff / 6) % 60
        karana_name = self.KARANAS[karana_num % 10]
        
        # Calculate Yoga
        yoga_longitude = (sun_pos + moon_pos) % 360
        yoga_num = int(yoga_longitude * 27 / 360)
        yoga_name = self.YOGAS[yoga_num]

        # Get weekday
        weekday = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 
                  'Thursday', 'Friday', 'Saturday'][int(self.jd + 1.5) % 7]

        return {
            'tithi': tithi_name,
            'karana': karana_name,
            'yoga': yoga_name,
            'weekday': weekday,
            'moon_phase': 'Full Moon' if tithi_num == 14 else 'New Moon' if tithi_num == 29 else None
        }

    def calculate_upagrahas(self) -> Dict[str, Dict[str, Any]]:
        """Calculate positions of Upagrahas (sub-planets)."""
        sun_long = self.get_planet_position('Sun')['longitude']
        upagrahas = {}
        
        for name, offset in UPAGRAHA_LONGITUDES.items():
            longitude = (sun_long + offset) % 360
            sign_num = int(longitude / 30)
            sign_name = self.ZODIAC_SIGNS[sign_num]
            degree = longitude % 30
            nakshatra, pada = self.get_nakshatra(longitude)
            
            upagrahas[name] = {
                'longitude': longitude,
                'sign': sign_name,
                'degree': degree,
                'nakshatra': nakshatra,
                'pada': pada
            }
        
        return upagrahas

    def calculate_vimshottari_dasha(self) -> List[Dict[str, Any]]:
        """Calculate Vimshottari Dasha periods."""
        moon_pos = self.get_planet_position('Moon')
        nakshatra_name = moon_pos['nakshatra']
        pada = moon_pos['pada']
        
        # Dasha order and their years
        dasha_order = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 
                      'Rahu', 'Jupiter', 'Saturn', 'Mercury']
        dasha_years = [7, 20, 6, 10, 7, 18, 16, 19, 17]
        
        # Find starting Mahadasha based on Moon's Nakshatra
        nakshatra_lord_index = self.NAKSHATRAS.index((nakshatra_name, self.NAKSHATRAS[0][1]))
        start_dasha_index = nakshatra_lord_index % 9
        
        dashas = []
        current_date = self.date
        
        for i in range(9):
            dasha_index = (start_dasha_index + i) % 9
            planet = dasha_order[dasha_index]
            years = dasha_years[dasha_index]
            
            dashas.append({
                'planet': planet,
                'duration': years,
                'start_date': current_date.strftime('%Y-%m-%d')
            })
            
            # Add years to get next dasha start date
            current_date = current_date.replace(year=current_date.year + years)
        
        return dashas

    def get_planet_position(self, planet_name: str) -> Dict[str, Any]:
        """Get detailed planetary position including retrograde status."""
        if planet_name == 'Ketu':
            rahu_result = self.get_planet_position('Rahu')
            longitude = (rahu_result['longitude'] + 180) % 360
            is_retrograde = rahu_result.get('is_retrograde', False)
        else:
            planet_id = PLANET_IDS[planet_name]
            flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
            result = swe.calc_ut(self.jd, planet_id, flags)
            longitude = result[0]
            speed = result[3]  # Daily motion in longitude
            is_retrograde = speed < 0
            
        sign_num = int(longitude / 30)
        sign_name = self.ZODIAC_SIGNS[sign_num]
        degrees_in_sign = longitude % 30
        
        nakshatra_name, pada = self.get_nakshatra(longitude)
        dignity = self._get_dignity(planet_name, sign_name)
            
        return {
            'longitude': longitude,
            'sign': sign_name,
            'degree': degrees_in_sign,
            'nakshatra': nakshatra_name,
            'pada': pada,
            'dignity': dignity,
            'is_retrograde': is_retrograde
        }

    def get_nakshatra(self, longitude: float) -> Tuple[str, int]:
        """Get nakshatra and pada for a given longitude."""
        nakshatra_span = 360 / 27  # Each nakshatra spans 13°20'
        pada_span = nakshatra_span / 4  # Each pada spans 3°20'
        
        nakshatra_idx = int(longitude / nakshatra_span)
        nakshatra_name = self.NAKSHATRAS[nakshatra_idx][0]
        
        # Calculate pada (1-4)
        pada_progress = (longitude % nakshatra_span) / pada_span
        pada = int(pada_progress) + 1
        
        return nakshatra_name, pada

    def _get_dignity(self, planet_name: str, sign_name: str) -> str:
        """Determine the dignity of a planet in a particular sign."""
        if planet_name not in self.DIGNITIES:
            return 'Unknown'
            
        dignity_data = self.DIGNITIES[planet_name]
        
        if sign_name == dignity_data.get('exalted'):
            return 'Exalted'
        elif sign_name == dignity_data.get('moolatrikona'):
            return 'Moolatrikona'
        elif sign_name in dignity_data.get('own', []):
            return 'Own sign'
        
        sign_rulers = {
            'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon',
            'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars',
            'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
        }
        
        ruler = sign_rulers.get(sign_name)
        if ruler in dignity_data.get('friend', []):
            return "Friend's sign"
        elif ruler in dignity_data.get('enemy', []):
            return "Enemy's sign"
        
        exalted_sign = dignity_data.get('exalted', '')
        if exalted_sign:
            exalted_idx = self.ZODIAC_SIGNS.index(exalted_sign)
            debilitated_idx = (exalted_idx + 6) % 12
            if sign_name == self.ZODIAC_SIGNS[debilitated_idx]:
                return 'Debilitated'
            
        return 'Neutral'

    def _calculate_ayanamsa(self) -> float:
        """Calculate ayanamsa value at the given date."""
        return swe.get_ayanamsa(self.jd)

    def _datetime_to_jd(self, dt: datetime) -> float:
        """Convert datetime to Julian day."""
        dt_utc = dt.replace(tzinfo=None)
        jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, 
                        dt_utc.hour + dt_utc.minute/60.0 + dt_utc.second/3600.0)
        return jd

    def convert_to_ghati_pal(self, hours: float) -> Tuple[float, float, float]:
        """Convert hours to traditional Indian units."""
        total_ghatis = hours * 2.5  # 1 day = 60 ghatis, so 1 hour = 2.5 ghatis
        ghatis = int(total_ghatis)
        
        remaining_vighatis = (total_ghatis - ghatis) * 60
        vighatis = int(remaining_vighatis)
        
        pals = int((remaining_vighatis - vighatis) * 60)
        
        return ghatis, vighatis, pals

    def get_house_cusps(self, system: str = 'W') -> List[float]:
        """
        Calculate house cusps according to the specified house system.
        
        system: House system
            'P' - Placidus
            'K' - Koch
            'O' - Porphyrius
            'R' - Regiomontanus
            'C' - Campanus
            'E' - Equal
            'W' - Whole sign
            'B' - Alcabitus
            'M' - Morinus
        """
        # For whole sign houses, the cusps are at the beginning of each sign
        if system == 'W':
            # First get the ascendant
            ascendant = swe.houses(self.jd, self.lat, self.lon, b'P')[1][0]
            # Find the sign number (0-11) of the ascendant
            asc_sign = int(ascendant / 30)
            # Create cusps starting from the ascendant sign
            cusps = [(asc_sign + i) % 12 * 30 for i in range(12)]
            return cusps
        
        # For other house systems, use Swiss Ephemeris
        hsys = bytes(system, 'utf-8')
        try:
            cusps = swe.houses(self.jd, self.lat, self.lon, hsys)[0]
            return list(cusps)
        except:
            # Fallback to Placidus if the requested system fails
            cusps = swe.houses(self.jd, self.lat, self.lon, b'P')[0]
            return list(cusps)

    def calculate_all_planets(self) -> Dict[str, Dict[str, Any]]:
        """Calculate positions for all planets."""
        all_planets = {}
        for planet in PLANET_IDS.keys():
            all_planets[planet] = self.get_planet_position(planet)
        return all_planets
