"""
Swiss Ephemeris calculator implementation.
This module provides a calculator using the pyswisseph library for maximum precision.
"""
import logging
from datetime import datetime
from typing import Dict, List, Any

from ..calculators.protocol import AstronomicalCalculator, PlanetaryData, HouseData, AspectData, Coordinates

# Setup logging
logger = logging.getLogger(__name__)

class SwissEphemerisCalculator(AstronomicalCalculator):
    """Implementation of the AstronomicalCalculator protocol using pyswisseph."""
    
    def __init__(self):
        """Initialize the calculator with the pyswisseph library."""
        try:
            # Import pyswisseph here to avoid global dependency
            import swisseph as swe
            self.swe = swe
            self.available = True
            
            # Set ephemeris path - this should be configured properly in production
            # swe.set_ephe_path("/path/to/ephemeris/files")
            
            logger.info("SwissEphemerisCalculator initialized successfully")
        except ImportError:
            self.available = False
            logger.warning("pyswisseph library not available")
    
    def calculate_planetary_positions(self, dt: datetime, coordinates: Coordinates) -> PlanetaryData:
        """Calculate planetary positions using pyswisseph."""
        if not self.available:
            raise RuntimeError("pyswisseph library not available")
        
        try:
            # Convert datetime to Julian day
            jd = self._datetime_to_jd(dt)
            
            # Define planet mapping (Swiss Ephemeris constants to our planet names)
            planet_map = {
                self.swe.SUN: "Sun",
                self.swe.MOON: "Moon",
                self.swe.MARS: "Mars",
                self.swe.MERCURY: "Mercury",
                self.swe.JUPITER: "Jupiter",
                self.swe.VENUS: "Venus",
                self.swe.SATURN: "Saturn",
                self.swe.MEAN_NODE: "Rahu"  # Using Mean Node for Rahu
            }
            
            # Calculate Ayanamsa (precession)
            ayanamsa = self.swe.get_ayanamsa(jd)
            
            # Calculate planetary positions
            planets = {}
            for swe_planet, planet_name in planet_map.items():
                # Calculate planet position
                result = self.swe.calc_ut(jd, swe_planet)
                
                # Convert to sidereal (Vedic) longitude
                sidereal_longitude = (result[0] - ayanamsa) % 360
                
                # Calculate sign, nakshatra, etc.
                sign_num = int(sidereal_longitude / 30)
                sign = self._get_sign_name(sign_num)
                degree = sidereal_longitude % 30
                nakshatra, pada = self._calculate_nakshatra(sidereal_longitude)
                
                # Determine house (simplified - in a real implementation, we would use proper house calculation)
                house = self._estimate_house(sidereal_longitude, 0)  # Assuming Ascendant at 0 for simplicity
                
                # Store planet data
                planets[planet_name] = {
                    "longitude": sidereal_longitude,
                    "latitude": result[1],
                    "speed": result[3],
                    "sign": sign,
                    "nakshatra": nakshatra,
                    "pada": pada,
                    "house": house,
                    "retrograde": result[3] < 0,  # Negative speed means retrograde
                    "degree": degree,
                    "formatted_degree": self._format_degree(degree),
                }
            
            # Calculate Ketu (opposite to Rahu)
            rahu_longitude = planets["Rahu"]["longitude"]
            ketu_longitude = (rahu_longitude + 180) % 360
            
            # Calculate Ketu's sign, nakshatra, etc.
            sign_num = int(ketu_longitude / 30)
            sign = self._get_sign_name(sign_num)
            degree = ketu_longitude % 30
            nakshatra, pada = self._calculate_nakshatra(ketu_longitude)
            house = self._estimate_house(ketu_longitude, 0)  # Simplified
            
            # Store Ketu data
            planets["Ketu"] = {
                "longitude": ketu_longitude,
                "latitude": -planets["Rahu"]["latitude"],  # Opposite latitude to Rahu
                "speed": planets["Rahu"]["speed"],  # Same speed as Rahu
                "sign": sign,
                "nakshatra": nakshatra,
                "pada": pada,
                "house": house,
                "retrograde": planets["Rahu"]["retrograde"],  # Same as Rahu
                "degree": degree,
                "formatted_degree": self._format_degree(degree),
            }
            
            # Calculate Ascendant
            ascendant = self.swe.houses(jd, coordinates.latitude, coordinates.longitude)[0]
            sidereal_ascendant = (ascendant - ayanamsa) % 360
            
            # Calculate Ascendant's sign, nakshatra, etc.
            sign_num = int(sidereal_ascendant / 30)
            sign = self._get_sign_name(sign_num)
            degree = sidereal_ascendant % 30
            nakshatra, pada = self._calculate_nakshatra(sidereal_ascendant)
            
            # Store Ascendant data
            planets["Ascendant"] = {
                "longitude": sidereal_ascendant,
                "latitude": 0.0,  # Ascendant doesn't have latitude
                "speed": 0.0,     # Ascendant doesn't have speed
                "sign": sign,
                "nakshatra": nakshatra,
                "pada": pada,
                "house": 1,  # Ascendant is always in the 1st house
                "retrograde": False,  # Ascendant is never retrograde
                "degree": degree,
                "formatted_degree": self._format_degree(degree),
            }
            
            # Add calculation system info
            planets["calculation_system"] = "swiss_ephemeris"
            
            return planets
        
        except Exception as e:
            logger.error(f"Error calculating planetary positions with pyswisseph: {str(e)}")
            raise
    
    def calculate_house_cusps(self, dt: datetime, coordinates: Coordinates, system: str = "Placidus") -> HouseData:
        """Calculate house cusps using pyswisseph."""
        if not self.available:
            raise RuntimeError("pyswisseph library not available")
        
        try:
            # Convert datetime to Julian day
            jd = self._datetime_to_jd(dt)
            
            # Map house system name to Swiss Ephemeris constant
            house_system = self._get_house_system(system)
            
            # Calculate houses
            houses = self.swe.houses(jd, coordinates.latitude, coordinates.longitude, house_system)
            
            # Calculate Ayanamsa (precession)
            ayanamsa = self.swe.get_ayanamsa(jd)
            
            # Convert to sidereal (Vedic) longitudes
            cusps = [(h - ayanamsa) % 360 for h in houses[0]]
            
            return {
                "system": system,
                "cusps": cusps
            }
        
        except Exception as e:
            logger.error(f"Error calculating house cusps with pyswisseph: {str(e)}")
            raise
    
    def calculate_aspects(self, chart_data: PlanetaryData) -> AspectData:
        """Calculate aspects between planets."""
        if not self.available:
            raise RuntimeError("pyswisseph library not available")
        
        try:
            # In a real implementation, we would calculate aspects here
            # For now, we'll return an empty list
            return {"aspects": []}
        
        except Exception as e:
            logger.error(f"Error calculating aspects with pyswisseph: {str(e)}")
            raise
    
    def _datetime_to_jd(self, dt: datetime) -> float:
        """Convert Python datetime to Julian day."""
        return self.swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0 + dt.second/3600.0)
    
    def _get_sign_name(self, sign_num: int) -> str:
        """Get zodiac sign name from sign number (0-11)."""
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                 "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        return signs[sign_num % 12]
    
    def _calculate_nakshatra(self, longitude: float) -> tuple:
        """Calculate nakshatra and pada from longitude."""
        # Each nakshatra is 13°20' (13.33333... degrees)
        nakshatra_size = 13 + 1/3
        
        # Calculate nakshatra number (0-26)
        nakshatra_num = int(longitude / nakshatra_size)
        
        # Calculate pada (1-4)
        pada = int((longitude % nakshatra_size) / (nakshatra_size / 4)) + 1
        
        # Get nakshatra name
        nakshatras = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
            "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", 
            "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", 
            "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]
        nakshatra = nakshatras[nakshatra_num % 27]
        
        return nakshatra, pada
    
    def _estimate_house(self, longitude: float, ascendant_longitude: float) -> int:
        """Estimate house number based on longitude and ascendant (simplified)."""
        # This is a simplified approach - in a real implementation, we would use proper house calculation
        relative_pos = (longitude - ascendant_longitude) % 360
        house = int(relative_pos / 30) + 1
        return house
    
    def _format_degree(self, degree: float) -> str:
        """Format degree as DMS (degrees, minutes, seconds)."""
        d = int(degree)
        m_float = (degree - d) * 60
        m = int(m_float)
        s = int((m_float - m) * 60)
        return f"{d}°{m}'{s}\""
    
    def _get_house_system(self, system: str) -> str:
        """Map house system name to Swiss Ephemeris constant."""
        house_systems = {
            "Placidus": b'P',
            "Koch": b'K',
            "Whole Sign": b'W',
            "Equal": b'E',
            "Campanus": b'C',
            "Regiomontanus": b'R',
            "Porphyry": b'O',
            "Morinus": b'M',
            "Polich-Page": b'T',  # Topocentric
            "Alcabitius": b'B',
            "Krusinski": b'U',
            "APC": b'Y'
        }
        return house_systems.get(system, b'P')  # Default to Placidus
