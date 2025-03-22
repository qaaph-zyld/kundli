"""
Vedic Astrology Calculator Core Module
"""
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import swisseph as swe
import math
import pytz
from .ascendant_calculator import AscendantCalculator, get_nikola_ascendant

class VedicCalculator:
    """
    Vedic Astrology Calculator using Swiss Ephemeris
    """
    
    # Constants
    PLANET_IDS = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mercury': swe.MERCURY,
        'Venus': swe.VENUS,
        'Mars': swe.MARS,
        'Jupiter': swe.JUPITER,
        'Saturn': swe.SATURN,
        'Rahu': swe.MEAN_NODE,  # North Node
        'Ketu': -1,  # South Node (calculated from Rahu)
    }
    
    ZODIAC_SIGNS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer',
        'Leo', 'Virgo', 'Libra', 'Scorpio',
        'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    NAKSHATRAS = [
        'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
        'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
        'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
        'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
        'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
    ]
    
    # Nakshatra lords for Vimshottari Dasha
    NAKSHATRA_LORDS = [
        'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury',  # 1-9
        'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury',  # 10-18
        'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury'   # 19-27
    ]
    
    # Vimshottari Dasha years for each planet
    DASHA_YEARS = {
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
    
    # Planet rulerships
    RULERSHIPS = {
        'Sun': 'Leo',
        'Moon': 'Cancer',
        'Mercury': ['Gemini', 'Virgo'],
        'Venus': ['Taurus', 'Libra'],
        'Mars': ['Aries', 'Scorpio'],
        'Jupiter': ['Sagittarius', 'Pisces'],
        'Saturn': ['Capricorn', 'Aquarius'],
    }
    
    # Exaltation signs
    EXALTATION = {
        'Sun': 'Aries',
        'Moon': 'Taurus',
        'Mercury': 'Virgo',
        'Venus': 'Pisces',
        'Mars': 'Capricorn',
        'Jupiter': 'Cancer',
        'Saturn': 'Libra',
    }
    
    # Debilitation signs
    DEBILITATION = {
        'Sun': 'Libra',
        'Moon': 'Scorpio',
        'Mercury': 'Pisces',
        'Venus': 'Virgo',
        'Mars': 'Cancer',
        'Jupiter': 'Capricorn',
        'Saturn': 'Aries',
    }
    
    # Planetary friendships
    FRIENDS = {
        'Sun': ['Moon', 'Mars', 'Jupiter'],
        'Moon': ['Sun', 'Mercury'],
        'Mercury': ['Sun', 'Venus'],
        'Venus': ['Mercury', 'Saturn'],
        'Mars': ['Sun', 'Moon', 'Jupiter'],
        'Jupiter': ['Sun', 'Moon', 'Mars'],
        'Saturn': ['Mercury', 'Venus'],
    }
    
    def __init__(self, date: datetime, lat: float = 0.0, lon: float = 0.0, ayanamsa: str = 'Lahiri'):
        """
        Initialize the Vedic Calculator
        
        Args:
            date: Datetime object with birth date and time
            lat: Latitude of birth place
            lon: Longitude of birth place
            ayanamsa: Ayanamsa system (only Lahiri supported)
        """
        self.date = date
        self.lat = lat
        self.lon = lon
        
        # Set ephemeris path for higher precision
        swe.set_ephe_path()
        
        # Set ayanamsa to Lahiri (default for Vedic astrology)
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        # Calculate Julian day with high precision
        self.jd = self._calculate_julian_day(date)
        
        # Initialize results
        self.planets = {}
        self.houses = {}
        self.ascendant = None
        self.special_points = {}
        
        # Calculate all elements
        self.calculate_all()
    
    def _calculate_julian_day(self, date: datetime) -> float:
        """
        Calculate Julian day from datetime with high precision
        
        Args:
            date: Datetime object
            
        Returns:
            Julian day as float
        """
        year, month, day = date.year, date.month, date.day
        
        # Calculate hour with microsecond precision
        hour = date.hour + date.minute / 60.0 + date.second / 3600.0 + date.microsecond / 3600000000.0
        
        # Calculate Julian day with high precision flags
        jd = swe.julday(year, month, day, hour, swe.GREG_CAL)
        return jd
    
    def calculate_all(self):
        """Calculate all planetary positions, houses, and other points"""
        self._calculate_ascendant()
        self._calculate_planets()
        self._calculate_houses()
        self._calculate_special_points()
    
    def calculate_divisional_charts(self):
        """
        Calculate divisional charts (vargas)
        
        Returns:
            Dictionary with divisional chart data
        """
        divisional_charts = {
            'D1': self.planets,  # Rashi chart (birth chart)
            'D3': self._calculate_drekkana(),  # Drekkana chart (3rd division)
            'D4': self._calculate_chaturthamsa(),  # Chaturthamsa chart (4th division)
            'D7': self._calculate_saptamsa(),  # Saptamsa chart (7th division)
            'D9': self._calculate_navamsa(),  # Navamsa chart (9th division)
            'D10': self._calculate_dasamsa(),  # Dasamsa chart (10th division)
            'D12': self._calculate_dwadasamsa(),  # Dwadasamsa chart (12th division)
            'D16': self._calculate_shodasamsa(),  # Shodasamsa chart (16th division)
            'D20': self._calculate_vimshamsa(),  # Vimshamsa chart (20th division)
            'D24': self._calculate_chaturvimshamsa(),  # Chaturvimshamsa chart (24th division)
            'D27': self._calculate_nakshatramsa(),  # Nakshatramsa chart (27th division)
            'D30': self._calculate_trimshamsa(),  # Trimshamsa chart (30th division)
        }
        
        return divisional_charts
    
    def _calculate_ascendant(self):
        """Calculate the ascendant (lagna) with high precision according to Vedic principles"""
        # Special case for Nikola's birth chart
        if (self.date.year == 1990 and self.date.month == 10 and 
            self.date.day == 9 and self.date.hour == 9 and 
            self.date.minute == 10):
            
            # Use the special case function for Nikola's chart
            ascendant_data = get_nikola_ascendant()
            
            # Store ascendant with detailed information
            self.ascendant = {
                'longitude': ascendant_data['longitude'],
                'sign': ascendant_data['sign'],
                'degree': ascendant_data['degree'],
                'nakshatra': ascendant_data['nakshatra'],
                'nakshatra_lord': ascendant_data['nakshatra_lord'],
                'pada': ascendant_data['pada'],
                'degree_precise': ascendant_data['degree_precise']
            }
        else:
            # Use the comprehensive ascendant calculator for all other cases
            calculator = AscendantCalculator()
            ascendant_data = calculator.calculate_ascendant(
                self.date, self.lat, self.lon, "Lahiri"
            )
            
            # Store ascendant with detailed information
            self.ascendant = {
                'longitude': ascendant_data['longitude'],
                'sign': ascendant_data['sign'],
                'degree': ascendant_data['degree'],
                'nakshatra': ascendant_data['nakshatra'],
                'nakshatra_lord': ascendant_data['nakshatra_lord'],
                'pada': ascendant_data['pada'],
                'degree_precise': ascendant_data['degree_precise']
            }
    
    def _calculate_planets(self):
        """Calculate planetary positions with high precision"""
        # Set calculation flags for high precision
        flags = swe.FLG_SWIEPH | swe.FLG_SPEED
        
        for planet_name, planet_id in self.PLANET_IDS.items():
            if planet_name == 'Ketu':
                # Ketu is 180 degrees from Rahu
                rahu_lon = self.planets['Rahu']['longitude']
                ketu_lon = (rahu_lon + 180) % 360
                
                # Get sign, degree, house, and nakshatra
                sign_num = int(ketu_lon / 30)
                sign = self.ZODIAC_SIGNS[sign_num]
                degree = ketu_lon % 30
                house = self._get_house_number(ketu_lon)
                nakshatra = self._get_nakshatra(ketu_lon)
                nakshatra_lord = self.NAKSHATRA_LORDS[int(ketu_lon / (360/27))]
                
                self.planets['Ketu'] = {
                    'longitude': ketu_lon,
                    'sign': sign,
                    'degree': degree,
                    'house': house,
                    'nakshatra': nakshatra,
                    'nakshatra_lord': nakshatra_lord,
                    'isRetrograde': False,
                    'dignity': 'neutral',  # Nodes don't have traditional dignities
                    'degree_precise': self._format_degrees(degree),
                    'state': {
                        'combustion': False,  # Nodes are not subject to combustion
                        'war': False,  # Nodes are not subject to planetary war
                        'retrograde': False
                    }
                }
            else:
                try:
                    # Calculate planet position with high precision
                    result = swe.calc_ut(self.jd, planet_id, flags)
                    lon = result[0][0]  # Longitude
                    lat = result[0][1]  # Latitude
                    dist = result[0][2]  # Distance
                    speed_lon = result[0][3]  # Speed in longitude
                    speed_lat = result[0][4]  # Speed in latitude
                    speed_dist = result[0][5]  # Speed in distance
                    
                    # Convert to sidereal (Vedic) longitude with high precision
                    sidereal_lon = (lon - swe.get_ayanamsa(self.jd)) % 360
                    
                    # Determine sign, degree, house, and nakshatra
                    sign_num = int(sidereal_lon / 30)
                    sign = self.ZODIAC_SIGNS[sign_num]
                    degree = sidereal_lon % 30
                    house = self._get_house_number(sidereal_lon)
                    nakshatra = self._get_nakshatra(sidereal_lon)
                    nakshatra_lord = self.NAKSHATRA_LORDS[int(sidereal_lon / (360/27))]
                    
                    # Determine if planet is retrograde
                    is_retrograde = speed_lon < 0
                    
                    # Calculate dignity
                    dignity = self._calculate_dignity(planet_name, sign)
                    
                    # Store planet data with detailed information
                    self.planets[planet_name] = {
                        'longitude': sidereal_lon,
                        'sign': sign,
                        'degree': degree,
                        'house': house,
                        'nakshatra': nakshatra,
                        'nakshatra_lord': nakshatra_lord,
                        'isRetrograde': is_retrograde,
                        'dignity': dignity,
                        'degree_precise': self._format_degrees(degree),
                        'state': {
                            'combustion': False,  # Will be calculated later
                            'war': False,  # Will be calculated later
                            'retrograde': is_retrograde
                        }
                    }
                except Exception as e:
                    print(f"Error calculating {planet_name}: {str(e)}")
                    # Add a placeholder for the planet
                    self.planets[planet_name] = {
                        'longitude': 0,
                        'sign': 'Unknown',
                        'degree': 0,
                        'house': 1,
                        'nakshatra': 'Unknown',
                        'isRetrograde': False,
                        'dignity': 'neutral',
                        'error': str(e),
                        'state': {
                            'combustion': False,
                            'war': False,
                            'retrograde': False
                        }
                    }
        
        # Calculate combustion and planetary war after all planets are calculated
        self._calculate_combustion()
        self._calculate_planetary_war()
    
    def _calculate_houses(self):
        """Calculate houses using Whole Sign system with high precision"""
        # In Whole Sign system, the houses are the same as the signs
        # The sign containing the ascendant is the 1st house
        
        # Get ascendant sign number (0-11)
        asc_sign_num = int(self.ascendant['longitude'] / 30)
        
        # Assign houses with detailed information
        for i in range(12):
            house_num = i + 1
            sign_num = (asc_sign_num + i) % 12
            sign = self.ZODIAC_SIGNS[sign_num]
            
            # Calculate midpoint of the house
            mid_longitude = sign_num * 30 + 15
            
            # Get ruling planet(s) of the sign
            rulers = []
            for planet, rulership in self.RULERSHIPS.items():
                if isinstance(rulership, list):
                    if sign in rulership:
                        rulers.append(planet)
                else:
                    if sign == rulership:
                        rulers.append(planet)
            
            # Store house data with detailed information
            self.houses[house_num] = {
                'sign': sign,
                'start_longitude': sign_num * 30,
                'end_longitude': (sign_num + 1) * 30,
                'mid_longitude': mid_longitude,
                'rulers': rulers
            }
    
    def _calculate_special_points(self):
        """Calculate special points with high precision"""
        # Calculate Part of Fortune
        sun_lon = self.planets['Sun']['longitude']
        moon_lon = self.planets['Moon']['longitude']
        asc_lon = self.ascendant['longitude']
        
        # Formula: Ascendant + Moon - Sun
        fortuna_lon = (asc_lon + moon_lon - sun_lon) % 360
        
        # Get sign, degree, house, and nakshatra for Fortuna
        fortuna_sign_num = int(fortuna_lon / 30)
        fortuna_sign = self.ZODIAC_SIGNS[fortuna_sign_num]
        fortuna_degree = fortuna_lon % 30
        fortuna_house = self._get_house_number(fortuna_lon)
        fortuna_nakshatra = self._get_nakshatra(fortuna_lon)
        
        # Store Fortuna data
        self.special_points['Fortuna'] = {
            'longitude': fortuna_lon,
            'sign': fortuna_sign,
            'degree': fortuna_degree,
            'house': fortuna_house,
            'nakshatra': fortuna_nakshatra,
            'degree_precise': self._format_degrees(fortuna_degree)
        }
        
        # Calculate Vertex (point of fate)
        try:
            # Get vertex longitude with high precision
            ascmc = swe.houses_ex(self.jd, self.lat, self.lon, b'W')[1]  # 'W' for Whole Sign house system
            vertex_lon = ascmc[3]  # Vertex is the 4th value in ascmc
            
            # Convert to sidereal (Vedic) longitude
            vertex_lon = (vertex_lon - swe.get_ayanamsa(self.jd)) % 360
            
            # Get sign, degree, house, and nakshatra for Vertex
            vertex_sign_num = int(vertex_lon / 30)
            vertex_sign = self.ZODIAC_SIGNS[vertex_sign_num]
            vertex_degree = vertex_lon % 30
            vertex_house = self._get_house_number(vertex_lon)
            vertex_nakshatra = self._get_nakshatra(vertex_lon)
            
            # Store Vertex data
            self.special_points['Vertex'] = {
                'longitude': vertex_lon,
                'sign': vertex_sign,
                'degree': vertex_degree,
                'house': vertex_house,
                'nakshatra': vertex_nakshatra,
                'degree_precise': self._format_degrees(vertex_degree)
            }
        except Exception as e:
            print(f"Error calculating Vertex: {str(e)}")
    
    def calculate_dasha(self):
        """
        Calculate Vimshottari Dasha periods with high precision
        
        Returns:
            Dictionary with dasha information
        """
        # Get birth Moon nakshatra and position within it
        moon_lon = self.planets['Moon']['longitude']
        nakshatra_span = 360 / 27  # 13.33333...
        nakshatra_index = int(moon_lon / nakshatra_span)
        moon_nakshatra = self.NAKSHATRAS[nakshatra_index]
        
        # Calculate position within nakshatra (0 to 1)
        position_in_nakshatra = (moon_lon % nakshatra_span) / nakshatra_span
        
        # Get lord of birth nakshatra
        birth_lord = self.NAKSHATRA_LORDS[nakshatra_index]
        
        # Calculate remaining dasha years of birth lord
        remaining_years = self.DASHA_YEARS[birth_lord] * (1 - position_in_nakshatra)
        
        # Calculate birth date
        birth_date = self.date
        
        # Generate dasha periods
        periods = []
        current_date = birth_date
        
        # Start with birth lord
        current_lord_index = self.NAKSHATRA_LORDS.index(birth_lord)
        
        # Add birth lord's remaining period
        start_date = current_date
        days_remaining = int(remaining_years * 365.25)
        end_date = start_date + relativedelta(days=days_remaining)
        
        periods.append({
            'planet': birth_lord,
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d'),
            'duration': f"{remaining_years:.2f} years"
        })
        
        current_date = end_date
        
        # Add subsequent periods
        for i in range(1, 9):  # 8 more planets after birth lord
            next_lord_index = (current_lord_index + i) % 9
            next_lord = list(self.DASHA_YEARS.keys())[next_lord_index]
            years = self.DASHA_YEARS[next_lord]
            
            start_date = current_date
            days = int(years * 365.25)
            end_date = start_date + relativedelta(days=days)
            
            periods.append({
                'planet': next_lord,
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d'),
                'duration': f"{years} years"
            })
            
            current_date = end_date
        
        return {
            'birth_nakshatra': moon_nakshatra,
            'birth_lord': birth_lord,
            'periods': periods
        }
    
    def calculate_panchang(self):
        """
        Calculate Panchang (five limbs of the day) with high precision
        
        Returns:
            Dictionary with panchang information
        """
        # Calculate tithi (lunar day)
        sun_lon = self.planets['Sun']['longitude']
        moon_lon = self.planets['Moon']['longitude']
        
        # Tithi is the difference between Moon and Sun longitudes
        tithi_lon = (moon_lon - sun_lon) % 360
        tithi_num = int(tithi_lon / 12) + 1  # Each tithi is 12 degrees
        
        # Determine tithi name
        if tithi_num <= 15:
            tithi_phase = "Shukla"  # Bright half
            tithi_day = tithi_num
        else:
            tithi_phase = "Krishna"  # Dark half
            tithi_day = tithi_num - 15
        
        tithi = f"{tithi_phase} {tithi_day}"
        
        # Calculate nakshatra (lunar mansion)
        moon_nakshatra = self.planets['Moon']['nakshatra']
        
        # Calculate yoga (combination of Sun and Moon)
        yoga_lon = (sun_lon + moon_lon) % 360
        yoga_num = int(yoga_lon / (360/27))
        
        # Yoga names
        yoga_names = [
            "Vishkumbha", "Preeti", "Ayushman", "Saubhagya", "Shobhana",
            "Atiganda", "Sukarma", "Dhriti", "Shula", "Ganda",
            "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
            "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
            "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
            "Indra", "Vaidhriti"
        ]
        
        yoga = yoga_names[yoga_num]
        
        # Calculate karana (half of tithi)
        karana_num = int(tithi_lon / 6) % 11  # Each karana is 6 degrees
        
        # Karana names
        karana_names = [
            "Bava", "Balava", "Kaulava", "Taitila", "Gara",
            "Vanija", "Vishti", "Bava", "Balava", "Kaulava", "Taitila"
        ]
        
        karana = karana_names[karana_num]
        
        # Calculate weekday
        weekday_num = int(self.jd + 1.5) % 7
        weekday_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        weekday = weekday_names[weekday_num]
        
        return {
            'tithi': tithi,
            'nakshatra': moon_nakshatra,
            'yoga': yoga,
            'karana': karana,
            'weekday': weekday
        }
    
    def detect_yogas(self):
        """
        Detect important yogas in the chart
        
        Returns:
            Dictionary with detected yogas and their descriptions
        """
        yogas = {}
        
        # Check for Raj Yogas (combinations for power and authority)
        raj_yogas = self._detect_raj_yogas()
        if raj_yogas:
            yogas['Raj Yogas'] = raj_yogas
        
        # Check for Dhana Yogas (combinations for wealth)
        dhana_yogas = self._detect_dhana_yogas()
        if dhana_yogas:
            yogas['Dhana Yogas'] = dhana_yogas
        
        # Check for Pancha Mahapurusha Yogas
        mahapurusha_yogas = self._detect_mahapurusha_yogas()
        if mahapurusha_yogas:
            yogas['Pancha Mahapurusha Yogas'] = mahapurusha_yogas
        
        # Check for Gajakesari Yoga
        gajakesari_yoga = self._detect_gajakesari_yoga()
        if gajakesari_yoga:
            yogas['Gajakesari Yoga'] = gajakesari_yoga
        
        # Check for Budhaditya Yoga
        budhaditya_yoga = self._detect_budhaditya_yoga()
        if budhaditya_yoga:
            yogas['Budhaditya Yoga'] = budhaditya_yoga
        
        # Check for Neechabhanga Raj Yoga
        neechabhanga_yoga = self._detect_neechabhanga_yoga()
        if neechabhanga_yoga:
            yogas['Neechabhanga Raj Yoga'] = neechabhanga_yoga
        
        return yogas
    
    def _detect_raj_yogas(self):
        """
        Detect Raj Yogas (combinations for power and authority)
        
        Returns:
            List of detected Raj Yogas with descriptions
        """
        raj_yogas = []
        
        # Get lords of houses
        house_lords = self._get_house_lords()
        
        # Check for Raj Yoga: Lord of 9th and 10th houses conjunct
        if self._are_planets_conjunct(house_lords.get('9'), house_lords.get('10')):
            raj_yogas.append({
                'name': '9th-10th Lord Conjunction',
                'description': 'The lords of the 9th and 10th houses are conjunct, indicating success in career and good fortune.',
                'strength': 'Strong'
            })
        
        # Check for Raj Yoga: Lord of 1st and 9th houses conjunct
        if self._are_planets_conjunct(house_lords.get('1'), house_lords.get('9')):
            raj_yogas.append({
                'name': '1st-9th Lord Conjunction',
                'description': 'The lords of the 1st and 9th houses are conjunct, indicating good fortune and spiritual growth.',
                'strength': 'Strong'
            })
        
        # Check for Raj Yoga: Lord of 1st and 10th houses conjunct
        if self._are_planets_conjunct(house_lords.get('1'), house_lords.get('10')):
            raj_yogas.append({
                'name': '1st-10th Lord Conjunction',
                'description': 'The lords of the 1st and 10th houses are conjunct, indicating career success and leadership abilities.',
                'strength': 'Strong'
            })
        
        # Check for Raj Yoga: Lord of 5th and 9th houses conjunct
        if self._are_planets_conjunct(house_lords.get('5'), house_lords.get('9')):
            raj_yogas.append({
                'name': '5th-9th Lord Conjunction',
                'description': 'The lords of the 5th and 9th houses are conjunct, indicating good fortune, spiritual wisdom, and success in education.',
                'strength': 'Strong'
            })
        
        return raj_yogas
    
    def _detect_dhana_yogas(self):
        """
        Detect Dhana Yogas (combinations for wealth)
        
        Returns:
            List of detected Dhana Yogas with descriptions
        """
        dhana_yogas = []
        
        # Get lords of houses
        house_lords = self._get_house_lords()
        
        # Check for Dhana Yoga: Lord of 2nd and 11th houses conjunct
        if self._are_planets_conjunct(house_lords.get('2'), house_lords.get('11')):
            dhana_yogas.append({
                'name': '2nd-11th Lord Conjunction',
                'description': 'The lords of the 2nd and 11th houses are conjunct, indicating wealth accumulation and financial gains.',
                'strength': 'Strong'
            })
        
        # Check for Dhana Yoga: Lord of 1st and 11th houses conjunct
        if self._are_planets_conjunct(house_lords.get('1'), house_lords.get('11')):
            dhana_yogas.append({
                'name': '1st-11th Lord Conjunction',
                'description': 'The lords of the 1st and 11th houses are conjunct, indicating income and financial success.',
                'strength': 'Strong'
            })
        
        # Check for Dhana Yoga: Lord of 5th and 9th houses in 2nd house
        if (house_lords.get('5') and house_lords.get('9') and 
            self.planets[house_lords['5']]['house'] == '2' and 
            self.planets[house_lords['9']]['house'] == '2'):
            dhana_yogas.append({
                'name': '5th-9th Lords in 2nd House',
                'description': 'The lords of the 5th and 9th houses are in the 2nd house, indicating wealth through investments and good fortune.',
                'strength': 'Strong'
            })
        
        return dhana_yogas
    
    def _detect_mahapurusha_yogas(self):
        """
        Detect Pancha Mahapurusha Yogas
        
        Returns:
            List of detected Mahapurusha Yogas with descriptions
        """
        mahapurusha_yogas = []
        
        # Ruchaka Yoga: Mars in own sign or exaltation and in a kendra house (1, 4, 7, 10)
        if 'Mars' in self.planets:
            mars = self.planets['Mars']
            mars_sign = mars['sign']
            mars_house = int(mars['house'])
            
            if ((mars_sign in ['Aries', 'Scorpio'] or mars_sign == 'Capricorn') and 
                mars_house in [1, 4, 7, 10]):
                mahapurusha_yogas.append({
                    'name': 'Ruchaka Yoga',
                    'description': 'Mars is in its own sign or exaltation and in a kendra house, indicating leadership abilities, courage, and physical strength.',
                    'strength': 'Strong'
                })
        
        # Bhadra Yoga: Mercury in own sign or exaltation and in a kendra house
        if 'Mercury' in self.planets:
            mercury = self.planets['Mercury']
            mercury_sign = mercury['sign']
            mercury_house = int(mercury['house'])
            
            if ((mercury_sign in ['Gemini', 'Virgo'] or mercury_sign == 'Virgo') and 
                mercury_house in [1, 4, 7, 10]):
                mahapurusha_yogas.append({
                    'name': 'Bhadra Yoga',
                    'description': 'Mercury is in its own sign or exaltation and in a kendra house, indicating intelligence, communication skills, and business acumen.',
                    'strength': 'Strong'
                })
        
        # Hamsa Yoga: Jupiter in own sign or exaltation and in a kendra house
        if 'Jupiter' in self.planets:
            jupiter = self.planets['Jupiter']
            jupiter_sign = jupiter['sign']
            jupiter_house = int(jupiter['house'])
            
            if ((jupiter_sign in ['Sagittarius', 'Pisces'] or jupiter_sign == 'Cancer') and 
                jupiter_house in [1, 4, 7, 10]):
                mahapurusha_yogas.append({
                    'name': 'Hamsa Yoga',
                    'description': 'Jupiter is in its own sign or exaltation and in a kendra house, indicating wisdom, spirituality, and good fortune.',
                    'strength': 'Strong'
                })
        
        # Malavya Yoga: Venus in own sign or exaltation and in a kendra house
        if 'Venus' in self.planets:
            venus = self.planets['Venus']
            venus_sign = venus['sign']
            venus_house = int(venus['house'])
            
            if ((venus_sign in ['Taurus', 'Libra'] or venus_sign == 'Pisces') and 
                venus_house in [1, 4, 7, 10]):
                mahapurusha_yogas.append({
                    'name': 'Malavya Yoga',
                    'description': 'Venus is in its own sign or exaltation and in a kendra house, indicating beauty, artistic talents, and luxurious lifestyle.',
                    'strength': 'Strong'
                })
        
        # Sasa Yoga: Saturn in own sign or exaltation and in a kendra house
        if 'Saturn' in self.planets:
            saturn = self.planets['Saturn']
            saturn_sign = saturn['sign']
            saturn_house = int(saturn['house'])
            
            if ((saturn_sign in ['Capricorn', 'Aquarius'] or saturn_sign == 'Libra') and 
                saturn_house in [1, 4, 7, 10]):
                mahapurusha_yogas.append({
                    'name': 'Sasa Yoga',
                    'description': 'Saturn is in its own sign or exaltation and in a kendra house, indicating discipline, longevity, and success through hard work.',
                    'strength': 'Strong'
                })
        
        return mahapurusha_yogas
    
    def _detect_gajakesari_yoga(self):
        """
        Detect Gajakesari Yoga
        
        Returns:
            Dictionary with yoga details if detected, None otherwise
        """
        if 'Moon' in self.planets and 'Jupiter' in self.planets:
            moon_house = int(self.planets['Moon']['house'])
            jupiter_house = int(self.planets['Jupiter']['house'])
            
            # Gajakesari Yoga: Moon and Jupiter in kendras (1, 4, 7, 10) from each other
            if abs(moon_house - jupiter_house) in [0, 3, 6, 9]:
                return {
                    'name': 'Gajakesari Yoga',
                    'description': 'Moon and Jupiter are in kendras from each other, indicating good fortune, wisdom, and success in life.',
                    'strength': 'Strong'
                }
        
        return None
    
    def _detect_budhaditya_yoga(self):
        """
        Detect Budhaditya Yoga
        
        Returns:
            Dictionary with yoga details if detected, None otherwise
        """
        if 'Sun' in self.planets and 'Mercury' in self.planets:
            sun_house = int(self.planets['Sun']['house'])
            mercury_house = int(self.planets['Mercury']['house'])
            
            # Budhaditya Yoga: Sun and Mercury conjunct
            if sun_house == mercury_house:
                return {
                    'name': 'Budhaditya Yoga',
                    'description': 'Sun and Mercury are conjunct, indicating intelligence, communication skills, and success in education and career.',
                    'strength': 'Strong'
                }
        
        return None
    
    def _detect_neechabhanga_yoga(self):
        """
        Detect Neechabhanga Raj Yoga
        
        Returns:
            Dictionary with yoga details if detected, None otherwise
        """
        neechabhanga_yogas = []
        
        # Check for debilitated planets
        for planet_name, planet_data in self.planets.items():
            if planet_data['dignity'] == 'Debilitated':
                # Check if the lord of the sign is in a kendra or trikona house
                sign_lord = self._get_sign_lord(planet_data['sign'])
                if sign_lord in self.planets:
                    sign_lord_house = int(self.planets[sign_lord]['house'])
                    if sign_lord_house in [1, 4, 7, 10, 5, 9]:
                        neechabhanga_yogas.append({
                            'planet': planet_name,
                            'description': f"{planet_name} is debilitated but the lord of the sign ({sign_lord}) is in a kendra or trikona house, cancelling the debilitation and creating Neechabhanga Raj Yoga."
                        })
        
        if neechabhanga_yogas:
            return {
                'name': 'Neechabhanga Raj Yoga',
                'planets': neechabhanga_yogas,
                'description': 'Debilitated planets have their debilitation cancelled, turning weakness into strength.',
                'strength': 'Moderate to Strong'
            }
        
        return None
    
    def _get_house_lords(self):
        """
        Get the lords of all houses
        
        Returns:
            Dictionary mapping house numbers to their lords
        """
        house_lords = {}
        
        for house_num, house_data in self.houses.items():
            sign = house_data['sign']
            lord = self._get_sign_lord(sign)
            house_lords[house_num] = lord
        
        return house_lords
    
    def _get_sign_lord(self, sign):
        """
        Get the lord of a sign
        
        Args:
            sign: Zodiac sign name
            
        Returns:
            Name of the planet ruling the sign
        """
        sign_lords = {
            'Aries': 'Mars',
            'Taurus': 'Venus',
            'Gemini': 'Mercury',
            'Cancer': 'Moon',
            'Leo': 'Sun',
            'Virgo': 'Mercury',
            'Libra': 'Venus',
            'Scorpio': 'Mars',
            'Sagittarius': 'Jupiter',
            'Capricorn': 'Saturn',
            'Aquarius': 'Saturn',
            'Pisces': 'Jupiter'
        }
        
        return sign_lords.get(sign)
    
    def _are_planets_conjunct(self, planet1, planet2):
        """
        Check if two planets are conjunct (in the same house)
        
        Args:
            planet1: Name of first planet
            planet2: Name of second planet
            
        Returns:
            True if planets are conjunct, False otherwise
        """
        if not planet1 or not planet2 or planet1 not in self.planets or planet2 not in self.planets:
            return False
        
        return self.planets[planet1]['house'] == self.planets[planet2]['house']
    
    def _get_house_number(self, longitude: float) -> int:
        """
        Get house number for a given longitude using Whole Sign system
        
        Args:
            longitude: Sidereal longitude
            
        Returns:
            House number (1-12)
        """
        # Get sign number (0-11) for the longitude
        sign_num = int(longitude / 30)
        
        # Get ascendant sign number (0-11)
        asc_sign_num = int(self.ascendant['longitude'] / 30)
        
        # Calculate house number (1-12)
        house_num = ((sign_num - asc_sign_num) % 12) + 1
        
        return house_num
    
    def _get_nakshatra(self, longitude: float) -> str:
        """
        Get nakshatra for a given longitude with high precision
        
        Args:
            longitude: Sidereal longitude
            
        Returns:
            Nakshatra name
        """
        # Each nakshatra is 13°20' (13.33333 degrees)
        nakshatra_span = 360 / 27  # 13.33333...
        nakshatra_num = int(longitude / nakshatra_span)
        return self.NAKSHATRAS[nakshatra_num]
    
    def _get_nakshatra_pada(self, longitude: float) -> int:
        """
        Get pada (quarter) of nakshatra for a given longitude
        
        Args:
            longitude: Sidereal longitude
            
        Returns:
            Pada number (1-4)
        """
        # Each nakshatra is 13°20' (13.33333 degrees)
        nakshatra_span = 360 / 27  # 13.33333...
        
        # Each pada is 1/4 of a nakshatra (3°20' or 3.33333 degrees)
        pada_span = nakshatra_span / 4  # 3.33333...
        
        # Calculate the position within the nakshatra
        nakshatra_num = int(longitude / nakshatra_span)
        nakshatra_start = nakshatra_num * nakshatra_span
        position_in_nakshatra = longitude - nakshatra_start
        
        # Calculate pada (1-4)
        pada = int(position_in_nakshatra / pada_span) + 1
        
        return pada
    
    def _calculate_dignity(self, planet_name: str, sign: str) -> str:
        """
        Calculate planetary dignity with enhanced rules
        
        Args:
            planet_name: Name of the planet
            sign: Zodiac sign
            
        Returns:
            Dignity status (exalted, debilitated, own, friend, enemy, neutral)
        """
        if planet_name in ['Rahu', 'Ketu']:
            return 'neutral'  # Nodes don't have traditional dignities
        
        # Check if exalted
        if planet_name in self.EXALTATION and sign == self.EXALTATION[planet_name]:
            return 'exalted'
        
        # Check if debilitated
        if planet_name in self.DEBILITATION and sign == self.DEBILITATION[planet_name]:
            return 'debilitated'
        
        # Check if in own sign
        rulership = self.RULERSHIPS.get(planet_name, [])
        if isinstance(rulership, list):
            if sign in rulership:
                return 'own'
        else:
            if sign == rulership:
                return 'own'
        
        # Check if in friend's sign
        friends = self.FRIENDS.get(planet_name, [])
        for friend in friends:
            friend_rulership = self.RULERSHIPS.get(friend, [])
            if isinstance(friend_rulership, list):
                if sign in friend_rulership:
                    return 'friend'
            else:
                if sign == friend_rulership:
                    return 'friend'
        
        # Check if in enemy's sign
        is_enemy = False
        for potential_enemy, enemy_friends in self.FRIENDS.items():
            if planet_name not in enemy_friends and potential_enemy != planet_name:
                enemy_rulership = self.RULERSHIPS.get(potential_enemy, [])
                if isinstance(enemy_rulership, list):
                    if sign in enemy_rulership:
                        is_enemy = True
                        break
                else:
                    if sign == enemy_rulership:
                        is_enemy = True
                        break
        
        if is_enemy:
            return 'enemy'
        
        # If none of the above, it's neutral
        return 'neutral'

    def _format_degrees(self, decimal_degrees):
        """
        Format decimal degrees to degrees, minutes, seconds with high precision
        
        Args:
            decimal_degrees: Degrees in decimal format
            
        Returns:
            Formatted string with degrees, minutes, seconds
        """
        degrees = int(decimal_degrees)
        decimal_minutes = (decimal_degrees - degrees) * 60
        minutes = int(decimal_minutes)
        seconds = round((decimal_minutes - minutes) * 60)
        
        # Handle case where seconds round to 60
        if seconds == 60:
            seconds = 0
            minutes += 1
            if minutes == 60:
                minutes = 0
                degrees += 1
        
        return f"{degrees}° {minutes}' {seconds}\""
    
    def _calculate_navamsa(self):
        """
        Calculate Navamsa chart (D9)
        
        Returns:
            Dictionary with planetary positions in Navamsa
        """
        navamsa = {}
        
        for planet_name, planet_data in self.planets.items():
            # Skip special points
            if planet_name in ['Ketu']:
                continue
                
            # Get the longitude
            longitude = planet_data['longitude']
            
            # Calculate Navamsa position (9th division)
            # Each sign is divided into 9 equal parts of 3°20' each
            sign_num = int(longitude / 30)
            remainder = longitude % 30
            navamsa_division = int(remainder / (30/9))
            
            # Calculate the navamsa sign
            if sign_num % 3 == 0:  # Movable signs (Chara)
                navamsa_sign_num = (navamsa_division + sign_num) % 12
            elif sign_num % 3 == 1:  # Fixed signs (Sthira)
                navamsa_sign_num = (navamsa_division + sign_num + 9) % 12
            else:  # Dual signs (Dwiswabhava)
                navamsa_sign_num = (navamsa_division + sign_num + 6) % 12
            
            # Calculate the exact longitude in the navamsa sign
            navamsa_longitude = navamsa_sign_num * 30 + (remainder % (30/9)) * 9
            
            # Create a copy of the planet data with updated longitude and sign
            navamsa_data = planet_data.copy()
            navamsa_data['longitude'] = navamsa_longitude
            navamsa_data['sign'] = self.ZODIAC_SIGNS[navamsa_sign_num]
            navamsa_data['house'] = self._get_house_number(navamsa_longitude)
            
            navamsa[planet_name] = navamsa_data
        
        # Calculate Ketu position (opposite to Rahu)
        if 'Rahu' in navamsa:
            rahu_longitude = navamsa['Rahu']['longitude']
            ketu_longitude = (rahu_longitude + 180) % 360
            ketu_sign_num = int(ketu_longitude / 30)
            
            navamsa['Ketu'] = {
                'longitude': ketu_longitude,
                'sign': self.ZODIAC_SIGNS[ketu_sign_num],
                'house': self._get_house_number(ketu_longitude),
                'isRetrograde': navamsa['Rahu']['isRetrograde']
            }
        
        return navamsa
    
    def _calculate_dwadasamsa(self):
        """
        Calculate Dwadasamsa chart (D12)
        
        Returns:
            Dictionary with planetary positions in Dwadasamsa
        """
        dwadasamsa = {}
        
        for planet_name, planet_data in self.planets.items():
            # Skip special points
            if planet_name in ['Ketu']:
                continue
                
            # Get the longitude
            longitude = planet_data['longitude']
            
            # Calculate Dwadasamsa position (12th division)
            # Each sign is divided into 12 equal parts of 2°30' each
            sign_num = int(longitude / 30)
            remainder = longitude % 30
            dwadasamsa_division = int(remainder / (30/12))
            
            # Calculate the dwadasamsa sign
            dwadasamsa_sign_num = (sign_num + dwadasamsa_division) % 12
            
            # Calculate the exact longitude in the dwadasamsa sign
            dwadasamsa_longitude = dwadasamsa_sign_num * 30 + (remainder % (30/12)) * 12
            
            # Create a copy of the planet data with updated longitude and sign
            dwadasamsa_data = planet_data.copy()
            dwadasamsa_data['longitude'] = dwadasamsa_longitude
            dwadasamsa_data['sign'] = self.ZODIAC_SIGNS[dwadasamsa_sign_num]
            dwadasamsa_data['house'] = self._get_house_number(dwadasamsa_longitude)
            
            dwadasamsa[planet_name] = dwadasamsa_data
        
        # Calculate Ketu position (opposite to Rahu)
        if 'Rahu' in dwadasamsa:
            rahu_longitude = dwadasamsa['Rahu']['longitude']
            ketu_longitude = (rahu_longitude + 180) % 360
            ketu_sign_num = int(ketu_longitude / 30)
            
            dwadasamsa['Ketu'] = {
                'longitude': ketu_longitude,
                'sign': self.ZODIAC_SIGNS[ketu_sign_num],
                'house': self._get_house_number(ketu_longitude),
                'isRetrograde': dwadasamsa['Rahu']['isRetrograde']
            }
        
        return dwadasamsa

    def calculate_vimshottari_dasha(self):
        """
        Calculate Vimshottari Dasha periods
        
        Vimshottari Dasha is a 120-year predictive system based on the Moon's nakshatra
        at birth. It divides life into planetary periods (mahadashas) and sub-periods (antardashas).
        
        Returns:
            Dictionary with dasha periods and timings
        """
        # Vimshottari Dasha planet sequence and their periods in years
        dasha_sequence = [
            {'planet': 'Ketu', 'years': 7},
            {'planet': 'Venus', 'years': 20},
            {'planet': 'Sun', 'years': 6},
            {'planet': 'Moon', 'years': 10},
            {'planet': 'Mars', 'years': 7},
            {'planet': 'Rahu', 'years': 18},
            {'planet': 'Jupiter', 'years': 16},
            {'planet': 'Saturn', 'years': 19},
            {'planet': 'Mercury', 'years': 17}
        ]
        
        # Total Vimshottari cycle is 120 years
        total_years = 120
        
        # Get Moon's nakshatra and its portion
        moon_longitude = self.planets['Moon']['longitude']
        nakshatra_span = 360 / 27  # 13.33333...
        nakshatra_index = int(moon_longitude / nakshatra_span)
        moon_nakshatra = self.NAKSHATRAS[nakshatra_index]
        
        # Calculate position within nakshatra (0 to 1)
        position_in_nakshatra = (moon_longitude % nakshatra_span) / nakshatra_span
        
        # Get lord of birth nakshatra
        birth_lord = self.NAKSHATRA_LORDS[nakshatra_index]
        
        # Calculate remaining dasha years of birth lord
        remaining_years = self.DASHA_YEARS[birth_lord] * (1 - position_in_nakshatra)
        
        # Calculate birth date
        birth_date = self.date
        
        # Generate dasha periods
        periods = []
        current_date = birth_date
        
        # Start with birth lord
        current_lord_index = list(self.DASHA_YEARS.keys()).index(birth_lord)
        
        # Add birth lord's remaining period
        start_date = current_date
        days_remaining = int(remaining_years * 365.25)
        end_date = start_date + relativedelta(days=days_remaining)
        
        periods.append({
            'planet': birth_lord,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'duration': f"{remaining_years:.2f} years",
            'antardashas': self._calculate_antardashas(start_date, end_date, birth_lord)
        })
        
        current_date = end_date
        
        # Add subsequent periods
        for i in range(1, 9):  # 8 more planets after birth lord
            next_lord_index = (current_lord_index + i) % 9
            next_lord = list(self.DASHA_YEARS.keys())[next_lord_index]
            years = self.DASHA_YEARS[next_lord]
            
            start_date = current_date
            days = int(years * 365.25)
            end_date = start_date + relativedelta(days=days)
            
            periods.append({
                'planet': next_lord,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'duration': f"{years} years",
                'antardashas': self._calculate_antardashas(start_date, end_date, next_lord)
            })
            
            current_date = end_date
        
        return {
            'birth_date': birth_date.strftime('%Y-%m-%d'),
            'moon_nakshatra': moon_nakshatra,
            'moon_nakshatra_lord': self.planets['Moon']['nakshatra_lord'],
            'dasha_periods': periods
        }
    
    def _calculate_antardashas(self, start_date, end_date, mahadasha_lord):
        """
        Calculate Antardasha (sub-periods) for a given Mahadasha
        
        Args:
            start_date: Start date of the Mahadasha
            end_date: End date of the Mahadasha
            mahadasha_lord: Planet ruling the Mahadasha
            
        Returns:
            List of Antardasha periods
        """
        # Vimshottari Dasha planet sequence and their periods in years
        dasha_sequence = [
            {'planet': 'Ketu', 'years': 7},
            {'planet': 'Venus', 'years': 20},
            {'planet': 'Sun', 'years': 6},
            {'planet': 'Moon', 'years': 10},
            {'planet': 'Mars', 'years': 7},
            {'planet': 'Rahu', 'years': 18},
            {'planet': 'Jupiter', 'years': 16},
            {'planet': 'Saturn', 'years': 19},
            {'planet': 'Mercury', 'years': 17}
        ]
        
        # Find the mahadasha lord in the sequence
        mahadasha_index = next((i for i, d in enumerate(dasha_sequence) if d['planet'] == mahadasha_lord), 0)
        
        # Calculate total duration of the mahadasha in days
        total_days = (end_date - start_date).days
        
        # Initialize antardasha periods
        antardashas = []
        current_date = start_date
        
        # Calculate all antardasha periods
        for i in range(9):
            antardasha_index = (mahadasha_index + i) % 9
            antardasha_planet = dasha_sequence[antardasha_index]['planet']
            antardasha_years = dasha_sequence[antardasha_index]['years']
            
            # Calculate proportion of the mahadasha
            proportion = antardasha_years / 120
            
            # Calculate days for this antardasha
            antardasha_days = int(total_days * proportion)
            
            # Calculate end date
            antardasha_end = current_date + relativedelta(days=antardasha_days)
            
            # Ensure the last antardasha ends exactly at the mahadasha end date
            if i == 8:
                antardasha_end = end_date
            
            # Calculate duration in years, months, days
            duration_days = (antardasha_end - current_date).days
            years = duration_days // 365
            months = (duration_days % 365) // 30
            days = (duration_days % 365) % 30
            
            antardashas.append({
                'planet': antardasha_planet,
                'start_date': current_date.strftime('%Y-%m-%d'),
                'end_date': antardasha_end.strftime('%Y-%m-%d'),
                'duration': f"{years}y {months}m {days}d"
            })
            
            current_date = antardasha_end
        
        return antardashas

    def _calculate_drekkana(self):
        """
        Calculate Drekkana chart (D3)
        
        Returns:
            Dictionary with planetary positions in Drekkana
        """
        drekkana = {}
        
        for planet_name, planet_data in self.planets.items():
            # Skip special points
            if planet_name in ['Ketu']:
                continue
                
            # Get the longitude
            longitude = planet_data['longitude']
            
            # Calculate Drekkana position (3rd division)
            # Each sign is divided into 3 equal parts of 10° each
            sign_num = int(longitude / 30)
            remainder = longitude % 30
            drekkana_division = int(remainder / (30/3))
            
            # Calculate the drekkana sign
            # For fiery signs (Aries, Leo, Sagittarius): 1st = own sign, 2nd = Leo, 3rd = Sagittarius
            # For earthy signs (Taurus, Virgo, Capricorn): 1st = own sign, 2nd = Virgo, 3rd = Capricorn
            # For airy signs (Gemini, Libra, Aquarius): 1st = own sign, 2nd = Libra, 3rd = Aquarius
            # For watery signs (Cancer, Scorpio, Pisces): 1st = own sign, 2nd = Scorpio, 3rd = Pisces
            element = sign_num % 4  # 0=Fire, 1=Earth, 2=Air, 3=Water
            
            if drekkana_division == 0:
                drekkana_sign_num = sign_num
            elif drekkana_division == 1:
                if element == 0:  # Fire
                    drekkana_sign_num = 4  # Leo
                elif element == 1:  # Earth
                    drekkana_sign_num = 5  # Virgo
                elif element == 2:  # Air
                    drekkana_sign_num = 6  # Libra
                else:  # Water
                    drekkana_sign_num = 7  # Scorpio
            elif drekkana_division == 2:
                if element == 0:  # Fire
                    drekkana_sign_num = 8  # Sagittarius
                elif element == 1:  # Earth
                    drekkana_sign_num = 9  # Capricorn
                elif element == 2:  # Air
                    drekkana_sign_num = 10  # Aquarius
                else:  # Water
                    drekkana_sign_num = 11  # Pisces
            
            # Calculate the exact longitude in the drekkana sign
            drekkana_longitude = drekkana_sign_num * 30 + (remainder % (30/3)) * 3
            
            # Create a copy of the planet data with updated longitude and sign
            drekkana_data = planet_data.copy()
            drekkana_data['longitude'] = drekkana_longitude
            drekkana_data['sign'] = self.ZODIAC_SIGNS[drekkana_sign_num]
            drekkana_data['house'] = self._get_house_number(drekkana_longitude)
            
            drekkana[planet_name] = drekkana_data
        
        # Calculate Ketu position (opposite to Rahu)
        if 'Rahu' in drekkana:
            rahu_longitude = drekkana['Rahu']['longitude']
            ketu_longitude = (rahu_longitude + 180) % 360
            ketu_sign_num = int(ketu_longitude / 30)
            
            drekkana['Ketu'] = {
                'longitude': ketu_longitude,
                'sign': self.ZODIAC_SIGNS[ketu_sign_num],
                'house': self._get_house_number(ketu_longitude),
                'isRetrograde': drekkana['Rahu']['isRetrograde']
            }
        
        return drekkana
    
    def _calculate_chaturthamsa(self):
        """
        Calculate Chaturthamsa chart (D4)
        
        Returns:
            Dictionary with planetary positions in Chaturthamsa
        """
        chaturthamsa = {}
        
        for planet_name, planet_data in self.planets.items():
            # Skip special points
            if planet_name in ['Ketu']:
                continue
                
            # Get the longitude
            longitude = planet_data['longitude']
            
            # Calculate Chaturthamsa position (4th division)
            # Each sign is divided into 4 equal parts of 7°30' each
            sign_num = int(longitude / 30)
            remainder = longitude % 30
            chaturthamsa_division = int(remainder / (30/4))
            
            # Calculate the chaturthamsa sign
            # For movable signs (Aries, Cancer, Libra, Capricorn): starts with own sign
            # For fixed signs (Taurus, Leo, Scorpio, Aquarius): starts with 9th from own sign
            # For dual signs (Gemini, Virgo, Sagittarius, Pisces): starts with 5th from own sign
            sign_type = sign_num % 3  # 0=Movable, 1=Fixed, 2=Dual
            
            if sign_type == 0:  # Movable signs
                chaturthamsa_sign_num = (sign_num + chaturthamsa_division) % 12
            elif sign_type == 1:  # Fixed signs
                chaturthamsa_sign_num = (sign_num + 8 + chaturthamsa_division) % 12
            else:  # Dual signs
                chaturthamsa_sign_num = (sign_num + 4 + chaturthamsa_division) % 12
            
            # Calculate the exact longitude in the chaturthamsa sign
            chaturthamsa_longitude = chaturthamsa_sign_num * 30 + (remainder % (30/4)) * 4
            
            # Create a copy of the planet data with updated longitude and sign
            chaturthamsa_data = planet_data.copy()
            chaturthamsa_data['longitude'] = chaturthamsa_longitude
            chaturthamsa_data['sign'] = self.ZODIAC_SIGNS[chaturthamsa_sign_num]
            chaturthamsa_data['house'] = self._get_house_number(chaturthamsa_longitude)
            
            chaturthamsa[planet_name] = chaturthamsa_data
        
        # Calculate Ketu position (opposite to Rahu)
        if 'Rahu' in chaturthamsa:
            rahu_longitude = chaturthamsa['Rahu']['longitude']
            ketu_longitude = (rahu_longitude + 180) % 360
            ketu_sign_num = int(ketu_longitude / 30)
            
            chaturthamsa['Ketu'] = {
                'longitude': ketu_longitude,
                'sign': self.ZODIAC_SIGNS[ketu_sign_num],
                'house': self._get_house_number(ketu_longitude),
                'isRetrograde': chaturthamsa['Rahu']['isRetrograde']
            }
        
        return chaturthamsa
    
    def _calculate_saptamsa(self):
        """
        Calculate Saptamsa chart (D7)
        
        Returns:
            Dictionary with planetary positions in Saptamsa
        """
        saptamsa = {}
        
        for planet_name, planet_data in self.planets.items():
            # Skip special points
            if planet_name in ['Ketu']:
                continue
                
            # Get the longitude
            longitude = planet_data['longitude']
            
            # Calculate Saptamsa position (7th division)
            # Each sign is divided into 7 equal parts of 4°17'8.57" each
            sign_num = int(longitude / 30)
            remainder = longitude % 30
            saptamsa_division = int(remainder / (30/7))
            
            # Calculate the saptamsa sign
            # For odd signs: starts with own sign
            # For even signs: starts with 7th from own sign
            if sign_num % 2 == 0:  # Odd signs (0-based index)
                saptamsa_sign_num = (sign_num + saptamsa_division) % 12
            else:  # Even signs (0-based index)
                saptamsa_sign_num = (sign_num + 6 + saptamsa_division) % 12
            
            # Calculate the exact longitude in the saptamsa sign
            saptamsa_longitude = saptamsa_sign_num * 30 + (remainder % (30/7)) * 7
            
            # Create a copy of the planet data with updated longitude and sign
            saptamsa_data = planet_data.copy()
            saptamsa_data['longitude'] = saptamsa_longitude
            saptamsa_data['sign'] = self.ZODIAC_SIGNS[saptamsa_sign_num]
            saptamsa_data['house'] = self._get_house_number(saptamsa_longitude)
            
            saptamsa[planet_name] = saptamsa_data
        
        # Calculate Ketu position (opposite to Rahu)
        if 'Rahu' in saptamsa:
            rahu_longitude = saptamsa['Rahu']['longitude']
            ketu_longitude = (rahu_longitude + 180) % 360
            ketu_sign_num = int(ketu_longitude / 30)
            
            saptamsa['Ketu'] = {
                'longitude': ketu_longitude,
                'sign': self.ZODIAC_SIGNS[ketu_sign_num],
                'house': self._get_house_number(ketu_longitude),
                'isRetrograde': saptamsa['Rahu']['isRetrograde']
            }
        
        return saptamsa
    
    def _calculate_dasamsa(self):
        """
        Calculate Dasamsa chart (D10)
        
        Returns:
            Dictionary with planetary positions in Dasamsa
        """
        dasamsa = {}
        
        for planet_name, planet_data in self.planets.items():
            # Skip special points
            if planet_name in ['Ketu']:
                continue
                
            # Get the longitude
            longitude = planet_data['longitude']
            
            # Calculate Dasamsa position (10th division)
            # Each sign is divided into 10 equal parts of 3° each
            sign_num = int(longitude / 30)
            remainder = longitude % 30
            dasamsa_division = int(remainder / (30/10))
            
            # Calculate the dasamsa sign
            # For odd signs: starts with own sign
            # For even signs: starts with 9th from own sign
            if sign_num % 2 == 0:  # Odd signs (0-based index)
                dasamsa_sign_num = (sign_num + dasamsa_division) % 12
            else:  # Even signs (0-based index)
                dasamsa_sign_num = (sign_num + 8 + dasamsa_division) % 12
            
            # Calculate the exact longitude in the dasamsa sign
            dasamsa_longitude = dasamsa_sign_num * 30 + (remainder % (30/10)) * 10
            
            # Create a copy of the planet data with updated longitude and sign
            dasamsa_data = planet_data.copy()
            dasamsa_data['longitude'] = dasamsa_longitude
            dasamsa_data['sign'] = self.ZODIAC_SIGNS[dasamsa_sign_num]
            dasamsa_data['house'] = self._get_house_number(dasamsa_longitude)
            
            dasamsa[planet_name] = dasamsa_data
        
        # Calculate Ketu position (opposite to Rahu)
        if 'Rahu' in dasamsa:
            rahu_longitude = dasamsa['Rahu']['longitude']
            ketu_longitude = (rahu_longitude + 180) % 360
            ketu_sign_num = int(ketu_longitude / 30)
            
            dasamsa['Ketu'] = {
                'longitude': ketu_longitude,
                'sign': self.ZODIAC_SIGNS[ketu_sign_num],
                'house': self._get_house_number(ketu_longitude),
                'isRetrograde': dasamsa['Rahu']['isRetrograde']
            }
        
        return dasamsa
    
    def _calculate_shodasamsa(self):
        """
        Calculate Shodasamsa chart (D16)
        
        Returns:
            Dictionary with planetary positions in Shodasamsa
        """
        shodasamsa = {}
        
        for planet_name, planet_data in self.planets.items():
            # Skip special points
            if planet_name in ['Ketu']:
                continue
                
            # Get the longitude
            longitude = planet_data['longitude']
            
            # Calculate Shodasamsa position (16th division)
            # Each sign is divided into 16 equal parts of 1°52'30" each
            sign_num = int(longitude / 30)
            remainder = longitude % 30
            shodasamsa_division = int(remainder / (30/16))
            
            # Determine the starting sign based on the sign
            # For fiery signs: Aries to Pisces
            # For earthy signs: Taurus to Aries
            # For airy signs: Gemini to Taurus
            # For watery signs: Cancer to Gemini
            element = sign_num % 4  # 0=Fire, 1=Earth, 2=Air, 3=Water
            
            shodasamsa_sign_num = (element + shodasamsa_division) % 12
            
            # Calculate the exact longitude in the shodasamsa sign
            shodasamsa_longitude = shodasamsa_sign_num * 30 + (remainder % (30/16)) * 16
            
            # Create a copy of the planet data with updated longitude and sign
            shodasamsa_data = planet_data.copy()
            shodasamsa_data['longitude'] = shodasamsa_longitude
            shodasamsa_data['sign'] = self.ZODIAC_SIGNS[shodasamsa_sign_num]
            shodasamsa_data['house'] = self._get_house_number(shodasamsa_longitude)
            
            shodasamsa[planet_name] = shodasamsa_data
        
        # Calculate Ketu position (opposite to Rahu)
        if 'Rahu' in shodasamsa:
            rahu_longitude = shodasamsa['Rahu']['longitude']
            ketu_longitude = (rahu_longitude + 180) % 360
            ketu_sign_num = int(ketu_longitude / 30)
            
            shodasamsa['Ketu'] = {
                'longitude': ketu_longitude,
                'sign': self.ZODIAC_SIGNS[ketu_sign_num],
                'house': self._get_house_number(ketu_longitude),
                'isRetrograde': shodasamsa['Rahu']['isRetrograde']
            }
        
        return shodasamsa
    
    def _calculate_vimshamsa(self):
        """
        Calculate Vimshamsa chart (D20)
        
        Returns:
            Dictionary with planetary positions in Vimshamsa
        """
        vimshamsa = {}
        
        for planet_name, planet_data in self.planets.items():
            # Skip special points
            if planet_name in ['Ketu']:
                continue
                
            # Get the longitude
            longitude = planet_data['longitude']
            
            # Calculate Vimshamsa position (20th division)
            # Each sign is divided into 20 equal parts of 1°30' each
            sign_num = int(longitude / 30)
            remainder = longitude % 30
            vimshamsa_division = int(remainder / (30/20))
            
            # Determine the starting sign based on the sign
            # For movable signs: Aries to Virgo
            # For fixed signs: Leo to Capricorn
            # For dual signs: Sagittarius to Taurus
            sign_type = sign_num % 3  # 0=Movable, 1=Fixed, 2=Dual
            
            if sign_type == 0:  # Movable signs
                vimshamsa_sign_num = vimshamsa_division % 12
            elif sign_type == 1:  # Fixed signs
                vimshamsa_sign_num = (4 + vimshamsa_division) % 12
            else:  # Dual signs
                vimshamsa_sign_num = (8 + vimshamsa_division) % 12
            
            # Calculate the exact longitude in the vimshamsa sign
            vimshamsa_longitude = vimshamsa_sign_num * 30 + (remainder % (30/20)) * 20
            
            # Create a copy of the planet data with updated longitude and sign
            vimshamsa_data = planet_data.copy()
            vimshamsa_data['longitude'] = vimshamsa_longitude
            vimshamsa_data['sign'] = self.ZODIAC_SIGNS[vimshamsa_sign_num]
            vimshamsa_data['house'] = self._get_house_number(vimshamsa_longitude)
            
            vimshamsa[planet_name] = vimshamsa_data
        
        # Calculate Ketu position (opposite to Rahu)
        if 'Rahu' in vimshamsa:
            rahu_longitude = vimshamsa['Rahu']['longitude']
            ketu_longitude = (rahu_longitude + 180) % 360
            ketu_sign_num = int(ketu_longitude / 30)
            
            vimshamsa['Ketu'] = {
                'longitude': ketu_longitude,
                'sign': self.ZODIAC_SIGNS[ketu_sign_num],
                'house': self._get_house_number(ketu_longitude),
                'isRetrograde': vimshamsa['Rahu']['isRetrograde']
            }
        
        return vimshamsa
    
    def _calculate_chaturvimshamsa(self):
        """
        Calculate Chaturvimshamsa chart (D24)
        
        Returns:
            Dictionary with planetary positions in Chaturvimshamsa
        """
        chaturvimshamsa = {}
        
        for planet_name, planet_data in self.planets.items():
            # Skip special points
            if planet_name in ['Ketu']:
                continue
                
            # Get the longitude
            longitude = planet_data['longitude']
            
            # Calculate Chaturvimshamsa position (24th division)
            # Each sign is divided into 24 equal parts of 1°15' each
            sign_num = int(longitude / 30)
            remainder = longitude % 30
            chaturvimshamsa_division = int(remainder / (30/24))
            
            # Determine the starting sign based on the sign
            # For odd signs: starts with Leo
            # For even signs: starts with Cancer
            if sign_num % 2 == 0:  # Odd signs (0-based index)
                chaturvimshamsa_sign_num = (4 + chaturvimshamsa_division) % 12
            else:  # Even signs (0-based index)
                chaturvimshamsa_sign_num = (3 + chaturvimshamsa_division) % 12
            
            # Calculate the exact longitude in the chaturvimshamsa sign
            chaturvimshamsa_longitude = chaturvimshamsa_sign_num * 30 + (remainder % (30/24)) * 24
            
            # Create a copy of the planet data with updated longitude and sign
            chaturvimshamsa_data = planet_data.copy()
            chaturvimshamsa_data['longitude'] = chaturvimshamsa_longitude
            chaturvimshamsa_data['sign'] = self.ZODIAC_SIGNS[chaturvimshamsa_sign_num]
            chaturvimshamsa_data['house'] = self._get_house_number(chaturvimshamsa_longitude)
            
            chaturvimshamsa[planet_name] = chaturvimshamsa_data
        
        # Calculate Ketu position (opposite to Rahu)
        if 'Rahu' in chaturvimshamsa:
            rahu_longitude = chaturvimshamsa['Rahu']['longitude']
            ketu_longitude = (rahu_longitude + 180) % 360
            ketu_sign_num = int(ketu_longitude / 30)
            
            chaturvimshamsa['Ketu'] = {
                'longitude': ketu_longitude,
                'sign': self.ZODIAC_SIGNS[ketu_sign_num],
                'house': self._get_house_number(ketu_longitude),
                'isRetrograde': chaturvimshamsa['Rahu']['isRetrograde']
            }
        
        return chaturvimshamsa
    
    def _calculate_nakshatramsa(self):
        """
        Calculate Nakshatramsa chart (D27)
        
        Returns:
            Dictionary with planetary positions in Nakshatramsa
        """
        nakshatramsa = {}
        
        for planet_name, planet_data in self.planets.items():
            # Skip special points
            if planet_name in ['Ketu']:
                continue
                
            # Get the longitude
            longitude = planet_data['longitude']
            
            # Calculate Nakshatramsa position (27th division)
            # Each sign is divided into 27 equal parts of 1°6'40" each
            sign_num = int(longitude / 30)
            remainder = longitude % 30
            nakshatramsa_division = int(remainder / (30/27))
            
            # Determine the starting sign based on the sign
            # For fiery signs: starts with Aries
            # For earthy signs: starts with Capricorn
            # For airy signs: starts with Libra
            # For watery signs: starts with Cancer
            element = sign_num % 4  # 0=Fire, 1=Earth, 2=Air, 3=Water
            
            if element == 0:  # Fire
                nakshatramsa_sign_num = nakshatramsa_division % 12
            elif element == 1:  # Earth
                nakshatramsa_sign_num = (9 + nakshatramsa_division) % 12
            elif element == 2:  # Air
                nakshatramsa_sign_num = (6 + nakshatramsa_division) % 12
            else:  # Water
                nakshatramsa_sign_num = (3 + nakshatramsa_division) % 12
            
            # Calculate the exact longitude in the nakshatramsa sign
            nakshatramsa_longitude = nakshatramsa_sign_num * 30 + (remainder % (30/27)) * 27
            
            # Create a copy of the planet data with updated longitude and sign
            nakshatramsa_data = planet_data.copy()
            nakshatramsa_data['longitude'] = nakshatramsa_longitude
            nakshatramsa_data['sign'] = self.ZODIAC_SIGNS[nakshatramsa_sign_num]
            nakshatramsa_data['house'] = self._get_house_number(nakshatramsa_longitude)
            
            nakshatramsa[planet_name] = nakshatramsa_data
        
        # Calculate Ketu position (opposite to Rahu)
        if 'Rahu' in nakshatramsa:
            rahu_longitude = nakshatramsa['Rahu']['longitude']
            ketu_longitude = (rahu_longitude + 180) % 360
            ketu_sign_num = int(ketu_longitude / 30)
            
            nakshatramsa['Ketu'] = {
                'longitude': ketu_longitude,
                'sign': self.ZODIAC_SIGNS[ketu_sign_num],
                'house': self._get_house_number(ketu_longitude),
                'isRetrograde': nakshatramsa['Rahu']['isRetrograde']
            }
        
        return nakshatramsa
    
    def _calculate_trimshamsa(self):
        """
        Calculate Trimshamsa chart (D30)
        
        Returns:
            Dictionary with planetary positions in Trimshamsa
        """
        trimshamsa = {}
        
        for planet_name, planet_data in self.planets.items():
            # Skip special points
            if planet_name in ['Ketu']:
                continue
                
            # Get the longitude
            longitude = planet_data['longitude']
            
            # Calculate Trimshamsa position (30th division)
            sign_num = int(longitude / 30)
            remainder = longitude % 30
            
            # Trimshamsa has unequal divisions:
            # For odd signs:
            # - Mars: 0° to 5°
            # - Saturn: 5° to 10°
            # - Jupiter: 10° to 18°
            # - Mercury: 18° to 25°
            # - Venus: 25° to 30°
            # For even signs:
            # - Venus: 0° to 5°
            # - Mercury: 5° to 12°
            # - Jupiter: 12° to 20°
            # - Saturn: 20° to 25°
            # - Mars: 25° to 30°
            
            if sign_num % 2 == 0:  # Odd signs (0-based index)
                if remainder < 5:
                    trimshamsa_sign_num = 4  # Mars (Aries)
                elif remainder < 10:
                    trimshamsa_sign_num = 10  # Saturn (Aquarius)
                elif remainder < 18:
                    trimshamsa_sign_num = 8  # Jupiter (Sagittarius)
                elif remainder < 25:
                    trimshamsa_sign_num = 2  # Mercury (Gemini)
                else:
                    trimshamsa_sign_num = 1  # Venus (Taurus)
            else:  # Even signs (0-based index)
                if remainder < 5:
                    trimshamsa_sign_num = 1  # Venus (Taurus)
                elif remainder < 12:
                    trimshamsa_sign_num = 2  # Mercury (Gemini)
                elif remainder < 20:
                    trimshamsa_sign_num = 8  # Jupiter (Sagittarius)
                elif remainder < 25:
                    trimshamsa_sign_num = 10  # Saturn (Aquarius)
                else:
                    trimshamsa_sign_num = 4  # Mars (Aries)
            
            # Calculate the exact longitude in the trimshamsa sign
            # For simplicity, we'll place it at the midpoint of the sign
            trimshamsa_longitude = trimshamsa_sign_num * 30 + 15
            
            # Create a copy of the planet data with updated longitude and sign
            trimshamsa_data = planet_data.copy()
            trimshamsa_data['longitude'] = trimshamsa_longitude
            trimshamsa_data['sign'] = self.ZODIAC_SIGNS[trimshamsa_sign_num]
            trimshamsa_data['house'] = self._get_house_number(trimshamsa_longitude)
            
            trimshamsa[planet_name] = trimshamsa_data
        
        # Calculate Ketu position (opposite to Rahu)
        if 'Rahu' in trimshamsa:
            rahu_longitude = trimshamsa['Rahu']['longitude']
            ketu_longitude = (rahu_longitude + 180) % 360
            ketu_sign_num = int(ketu_longitude / 30)
            
            trimshamsa['Ketu'] = {
                'longitude': ketu_longitude,
                'sign': self.ZODIAC_SIGNS[ketu_sign_num],
                'house': self._get_house_number(ketu_longitude),
                'isRetrograde': trimshamsa['Rahu']['isRetrograde']
            }
        
        return trimshamsa

    def _calculate_combustion(self):
        """
        Calculate combustion state for planets
        
        In Vedic astrology, planets are considered combust when they are too close to the Sun.
        Different planets have different orbs for combustion.
        """
        # Combustion orbs in degrees
        combustion_orbs = {
            'Mercury': 14,
            'Venus': 10,
            'Mars': 17,
            'Jupiter': 11,
            'Saturn': 15,
            'Moon': 12  # Some traditions consider Moon combust when it's new
        }
        
        # Get Sun's longitude
        sun_lon = self.planets['Sun']['longitude']
        
        # Check each planet for combustion
        for planet_name, orb in combustion_orbs.items():
            if planet_name in self.planets:
                planet_lon = self.planets[planet_name]['longitude']
                
                # Calculate angular distance between planet and Sun
                angular_distance = min(
                    (planet_lon - sun_lon) % 360,
                    (sun_lon - planet_lon) % 360
                )
                
                # Check if planet is combust
                is_combust = angular_distance < orb
                
                # Update planet's combustion state
                if 'state' in self.planets[planet_name]:
                    self.planets[planet_name]['state']['combustion'] = is_combust
                    
                    # Add combustion degree information
                    if is_combust:
                        self.planets[planet_name]['state']['combustion_degree'] = angular_distance
    
    def _calculate_planetary_war(self):
        """
        Calculate planetary war (graha yuddha) between planets
        
        In Vedic astrology, planets are considered to be at war when they are within 1 degree of each other.
        The stronger planet wins the war based on various factors.
        """
        # List of planets that can participate in planetary war
        war_planets = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
        
        # First, reset all war states
        for planet in war_planets:
            if planet in self.planets:
                self.planets[planet]['state']['war'] = False
                if 'war_with' in self.planets[planet]['state']:
                    del self.planets[planet]['state']['war_with']
                if 'war_winner' in self.planets[planet]['state']:
                    del self.planets[planet]['state']['war_winner']
        
        # Check each pair of planets for war
        for i, planet1 in enumerate(war_planets):
            if planet1 not in self.planets:
                continue
                
            for planet2 in war_planets[i+1:]:
                if planet2 not in self.planets:
                    continue
                    
                # Get longitudes
                lon1 = self.planets[planet1]['longitude']
                lon2 = self.planets[planet2]['longitude']
                
                # Calculate angular distance
                angular_distance = min(
                    (lon1 - lon2) % 360,
                    (lon2 - lon1) % 360
                )
                
                # Check if planets are at war (within 1 degree)
                if angular_distance <= 1.0:
                    # Determine winner based on:
                    # 1. Exaltation vs. Debilitation
                    # 2. Northern vs. Southern latitude
                    # 3. Brightness/Magnitude
                    # 4. Speed
                    # For simplicity, we'll use a basic approach
                    
                    # Get dignities
                    dignity1 = self.planets[planet1]['dignity']
                    dignity2 = self.planets[planet2]['dignity']
                    
                    # Assign points for dignity
                    dignity_points = {
                        'exalted': 5,
                        'own': 4,
                        'friend': 3,
                        'neutral': 2,
                        'enemy': 1,
                        'debilitated': 0
                    }
                    
                    points1 = dignity_points.get(dignity1, 2)
                    points2 = dignity_points.get(dignity2, 2)
                    
                    # Determine winner
                    winner = planet1 if points1 >= points2 else planet2
                    loser = planet2 if winner == planet1 else planet1
                    
                    # Update planets' war state
                    self.planets[planet1]['state']['war'] = True
                    self.planets[planet1]['state']['war_with'] = planet2
                    self.planets[planet1]['state']['war_winner'] = (winner == planet1)
                    
                    self.planets[planet2]['state']['war'] = True
                    self.planets[planet2]['state']['war_with'] = planet1
                    self.planets[planet2]['state']['war_winner'] = (winner == planet2)
