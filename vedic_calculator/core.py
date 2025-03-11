from datetime import datetime
from typing import List, Dict, Tuple, Any, Optional
import math
import swisseph as swe
import pytz
from datetime import timedelta

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
    """Core class for Vedic astrology calculations."""
    
    # Constants
    ZODIAC_SIGNS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
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

    NAKSHATRA_LORDS = [
        'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter',
        'Saturn', 'Mercury', 'Ketu', 'Venus', 'Sun', 'Moon', 'Mars',
        'Rahu', 'Jupiter', 'Saturn', 'Mercury', 'Ketu', 'Venus', 'Sun',
        'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury'
    ]
    
    PLANET_IDS = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mars': swe.MARS,
        'Mercury': swe.MERCURY,
        'Jupiter': swe.JUPITER,
        'Venus': swe.VENUS,
        'Saturn': swe.SATURN,
        'Rahu': swe.MEAN_NODE,  # North Node (Rahu)
        'Ketu': None  # South Node (Ketu) - calculated from Rahu
    }
    
    # Vimshottari Dasha periods in years
    DASHA_PERIODS = {
        'Ketu': 7,
        'Venus': 20,
        'Sun': 6,
        'Moon': 10,
        'Mars': 7,
        'Rahu': 18,
        'Jupiter': 16,
        'Saturn': 19,
        'Mercury': 17
    }
    
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
        """Calculate Vimshottari Dasha periods based on Moon's Nakshatra."""
        try:
            # Get Moon position
            moon_pos = self.get_planet_position('Moon')
            
            # Get nakshatra details
            nakshatra_name = moon_pos['nakshatra']
            
            # Find nakshatra index
            if isinstance(self.NAKSHATRAS[0], tuple):
                nakshatra_names = [nak[0] for nak in self.NAKSHATRAS]
                nakshatra_index = nakshatra_names.index(nakshatra_name)
            else:
                nakshatra_index = self.NAKSHATRAS.index(nakshatra_name)
            
            # Find the lord of the nakshatra
            nakshatra_lord = self.NAKSHATRA_LORDS[nakshatra_index]
            
            # Calculate progression of dashas
            dasha_sequence = self._get_dasha_sequence(nakshatra_lord)
            
            # Calculate start time of mahadasha
            birth_time = self.date
            
            # Calculate elapsed portion of nakshatra
            nakshatra_start_deg = nakshatra_index * (360 / 27)
            nakshatra_end_deg = (nakshatra_index + 1) * (360 / 27)
            moon_longitude = moon_pos['longitude']
            
            # Calculate elapsed portion as a percentage
            elapsed_portion = (moon_longitude - nakshatra_start_deg) / (nakshatra_end_deg - nakshatra_start_deg)
            
            # Calculate remaining portion of the first dasha
            first_lord = dasha_sequence[0]
            first_period_years = self.DASHA_PERIODS[first_lord]
            remaining_years = first_period_years * (1 - elapsed_portion)
            
            # Generate dasha periods
            dasha_periods = []
            current_time = birth_time
            
            for lord in dasha_sequence:
                period_years = self.DASHA_PERIODS[lord]
                
                if lord == first_lord:
                    # First dasha has already started
                    period_years = remaining_years
                
                end_time = current_time + timedelta(days=period_years * 365.25)
                
                dasha_periods.append({
                    'planet': lord,
                    'start_date': current_time.strftime('%Y-%m-%d'),
                    'end_date': end_time.strftime('%Y-%m-%d'),
                    'duration_years': period_years
                })
                
                current_time = end_time
            
            return dasha_periods
        except Exception as e:
            print(f"Error in calculate_vimshottari_dasha: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def _get_dasha_sequence(self, start_lord: str) -> List[str]:
        """Get the sequence of dashas starting from a specific lord."""
        # Order of lords in Vimshottari Dasha
        lord_order = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
        
        # Find the starting index
        start_index = lord_order.index(start_lord)
        
        # Create the sequence starting from the given lord
        sequence = lord_order[start_index:] + lord_order[:start_index]
        
        return sequence

    def get_planet_position(self, planet_name: str) -> Dict[str, Any]:
        """Get detailed planetary position including retrograde status."""
        if planet_name == 'Ketu':
            rahu_result = self.get_planet_position('Rahu')
            longitude = (rahu_result['longitude'] + 180) % 360
            is_retrograde = rahu_result.get('is_retrograde', False)
        else:
            planet_id = self.PLANET_IDS[planet_name]
            flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
            result = swe.calc_ut(self.jd, planet_id, flags)
            
            # Check if result has enough elements before accessing
            longitude = result[0] if len(result) > 0 else 0
            
            # Check if speed is available in the result
            is_retrograde = False
            if len(result) > 3:
                speed = result[3]  # Daily motion in longitude
                is_retrograde = speed < 0
            
        # Ensure longitude is a float
        if isinstance(longitude, tuple):
            longitude = longitude[0] if len(longitude) > 0 else 0
        
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
        # Each nakshatra is 13°20' (or 13.33333... degrees)
        nakshatra_span = 360 / 27
        
        # Calculate nakshatra index (0-26)
        nakshatra_index = int(longitude / nakshatra_span)
        
        # Get nakshatra name
        if isinstance(self.NAKSHATRAS[0], tuple):
            nakshatra_name = self.NAKSHATRAS[nakshatra_index][0]
        else:
            nakshatra_name = self.NAKSHATRAS[nakshatra_index]
        
        # Calculate pada (1-4)
        pada_span = nakshatra_span / 4
        pada = int((longitude % nakshatra_span) / pada_span) + 1
        
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
        for planet in self.PLANET_IDS.keys():
            all_planets[planet] = self.get_planet_position(planet)
        return all_planets

    def calculate_houses(self, house_system: str = 'W') -> Dict[int, Dict[str, Any]]:
        """Calculate house cusps using specified house system."""
        houses = {}
        
        if house_system == 'W':  # Whole Sign house system
            # Get ascendant longitude
            ascendant = self._calculate_ascendant()
            asc_sign = int(ascendant / 30)
            
            # For Whole Sign houses, each house starts at 0° of a sign
            for i in range(1, 13):
                house_num = i
                sign_num = (asc_sign + i - 1) % 12
                sign_name = self.ZODIAC_SIGNS[sign_num]
                
                houses[house_num] = {
                    'longitude': sign_num * 30,
                    'sign': sign_name,
                    'degree': 0
                }
        else:
            # Default to Placidus or other house systems if implemented
            # This is a placeholder for other house systems
            for i in range(1, 13):
                houses[i] = {
                    'longitude': 0,
                    'sign': 'Unknown',
                    'degree': 0
                }
        
        return houses
    
    def _calculate_ascendant(self) -> float:
        """Calculate the ascendant (rising sign)."""
        # Use Swiss Ephemeris to calculate ascendant
        cusps, ascmc = swe.houses(self.jd, self.lat, self.lon, b'P')
        ascendant = ascmc[0]  # Ascendant is the first element of ascmc
        
        return ascendant
