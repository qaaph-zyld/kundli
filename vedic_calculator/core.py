"""
Core astronomical calculations for Vedic astrology
"""
from datetime import datetime
import math
from functools import lru_cache
from typing import Dict, Tuple, List
from skyfield.api import load, wgs84
from skyfield.positionlib import Geocentric

class VedicCalculator:
    """
    Core calculator class for Vedic astrology calculations using Lahiri ayanamsa
    """
    # Zodiac signs in order
    ZODIAC_SIGNS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    # Planet dignities
    EXALTATION = {
        'Sun': 'Aries',
        'Moon': 'Taurus',
        'Mars': 'Capricorn',
        'Mercury': 'Virgo',
        'Jupiter': 'Cancer',
        'Venus': 'Pisces',
        'Saturn': 'Libra'
    }
    
    DEBILITATION = {
        'Sun': 'Libra',
        'Moon': 'Scorpio',
        'Mars': 'Cancer',
        'Mercury': 'Pisces',
        'Jupiter': 'Capricorn',
        'Venus': 'Virgo',
        'Saturn': 'Aries'
    }

    # Load ephemeris data
    EPHEMERIS = load('de421.bsp')
    EARTH = EPHEMERIS['earth']
    SUN = EPHEMERIS['sun']
    MOON = EPHEMERIS['moon']
    MARS = EPHEMERIS['mars']
    JUPITER = EPHEMERIS['jupiter barycenter']
    SATURN = EPHEMERIS['saturn barycenter']
    VENUS = EPHEMERIS['venus']
    MERCURY = EPHEMERIS['mercury']
    
    def __init__(self, date: datetime, lat: float = 0.0, lon: float = 0.0):
        """
        Initialize calculator with date, time and location
        
        Args:
            date: Datetime object in UTC
            lat: Latitude in degrees (North positive)
            lon: Longitude in degrees (East positive)
        """
        self.date = date
        self.lat = float(lat)
        self.lon = float(lon)
        
        # Create location object
        self.location = wgs84.latlon(self.lat, self.lon)
        self.observer = self.EARTH + self.location
        
        # Convert datetime to Time object
        self.ts = load.timescale()
        self.time = self.ts.from_datetime(date)
        
        # Calculate ayanamsa
        self.ayanamsa = self._calculate_lahiri_ayanamsa()

    def _calculate_lahiri_ayanamsa(self) -> float:
        """
        Calculate Lahiri ayanamsa for the given date
        
        Returns:
            float: Ayanamsa value in degrees
        """
        jd = self.time.tt - 2451545.0  # Days since J2000
        t = jd / 36525  # Julian centuries since J2000
        
        # Lahiri ayanamsa formula
        ayanamsa = 23.636953 + 0.017314 * t
        
        return ayanamsa

    def _normalize_longitude(self, longitude: float) -> float:
        """Normalize longitude to 0-360 range"""
        longitude = longitude % 360
        if longitude < 0:
            longitude += 360
        return longitude

    @lru_cache(maxsize=128)
    def get_planet_position(self, planet_name: str) -> Tuple[float, str]:
        """
        Calculate tropical position of a planet and convert to sidereal
        
        Args:
            planet_name: Name of the planet (Sun, Moon, Mars, etc.)
            
        Returns:
            Tuple[float, str]: (longitude in degrees, zodiac sign name)
        """
        # Get planet object
        planet = getattr(self, planet_name.upper())
        
        # Calculate planet position
        planet_at_date = planet.at(self.time)
        earth_at_date = self.EARTH.at(self.time)
        
        # Get ecliptic longitude
        _, lat, lon = planet_at_date.observe(self.EARTH).ecliptic_latlon()
        long_deg = float(lon.degrees)
        
        # Convert to sidereal by subtracting ayanamsa
        long_deg = self._normalize_longitude(long_deg - self.ayanamsa)
        
        # Calculate zodiac sign
        sign_num = int(long_deg / 30)
        sign = self.ZODIAC_SIGNS[sign_num]
        
        return (long_deg, sign)

    def get_house_cusps(self) -> List[float]:
        """
        Calculate house cusps using equal house system
        
        Returns:
            List[float]: List of 12 house cusp longitudes
        """
        # Calculate ascendant (Lagna)
        sun = self.SUN.at(self.time)
        earth = self.EARTH.at(self.time)
        
        # Get local sidereal time
        lst = earth.lst_hours_at(self.lon) * 15  # Convert hours to degrees
        
        # Convert to sidereal
        ascendant = self._normalize_longitude(lst - self.ayanamsa)
        
        # In equal house system, houses are exactly 30° apart
        cusps = [(ascendant + (i * 30)) % 360 for i in range(12)]
        return cusps

    def get_planet_dignity(self, planet_name: str) -> str:
        """
        Determine dignity state of a planet
        
        Args:
            planet_name: Name of the planet
            
        Returns:
            str: Dignity state (exalted, debilitated, neutral)
        """
        _, sign = self.get_planet_position(planet_name)
        
        if planet_name in self.EXALTATION and sign == self.EXALTATION[planet_name]:
            return 'exalted'
        elif planet_name in self.DEBILITATION and sign == self.DEBILITATION[planet_name]:
            return 'debilitated'
        return 'neutral'

    def calculate_all_planets(self) -> Dict[str, Dict[str, str]]:
        """
        Calculate positions for all major planets
        
        Returns:
            Dict with planet positions and dignities
        """
        planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
        result = {}
        
        for planet in planets:
            long_deg, sign = self.get_planet_position(planet)
            dignity = self.get_planet_dignity(planet)
            
            result[planet] = {
                'longitude': f"{long_deg:.2f}",
                'sign': sign,
                'dignity': dignity,
                'degree': f"{long_deg % 30:.2f}"
            }
            
        return result
