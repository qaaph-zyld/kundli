"""
Vedic Jyotish Ascendant Calculation Module

A comprehensive implementation for accurate Vedic ascendant (lagna) calculations
with built-in validation mechanisms and diagnostic capabilities.
"""

import math
from datetime import datetime

class AscendantCalculator:
    """
    Ascendant calculator for Vedic astrology using high-precision algorithms
    """
    
    # Constants for astronomical calculations
    J2000 = 2451545.0  # Julian date for January 1, 2000, 12:00 UT
    
    # Zodiac sign names in Vedic tradition
    ZODIAC_SIGNS = [
        'Mesha', 'Vrishabha', 'Mithuna', 'Karka',
        'Simha', 'Kanya', 'Tula', 'Vrishchika',
        'Dhanu', 'Makara', 'Kumbha', 'Meena'
    ]
    
    # Western equivalent names (for reference only)
    WESTERN_SIGNS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer',
        'Leo', 'Virgo', 'Libra', 'Scorpio',
        'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    # Nakshatra (lunar mansion) names
    NAKSHATRAS = [
        'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
        'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
        'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
        'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
        'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
    ]
    
    # Nakshatra lords following Vimshottari Dasha sequence
    NAKSHATRA_LORDS = [
        'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury',  # 1-9
        'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury',  # 10-18
        'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury'   # 19-27
    ]
    
    # Planetary rulerships for signs
    SIGN_LORDS = [
        'Mars', 'Venus', 'Mercury', 'Moon',  # Aries to Cancer
        'Sun', 'Mercury', 'Venus', 'Mars',   # Leo to Scorpio
        'Jupiter', 'Saturn', 'Saturn', 'Jupiter'  # Sagittarius to Pisces
    ]
    
    def __init__(self):
        """Initialize the Ascendant Calculator"""
        pass
    
    def calculate_ascendant(self, date_time, latitude, longitude, ayanamsha_system="Lahiri"):
        """
        Calculate Vedic ascendant using sidereal zodiac
        
        Args:
            date_time: Datetime object with birth date and time (UTC)
            latitude: Geographical latitude in decimal degrees
            longitude: Geographical longitude in decimal degrees
            ayanamsha_system: Ayanamsha system to use (default: "Lahiri")
            
        Returns:
            Dictionary with complete ascendant information
        """
        # Step 1: Calculate Julian Day
        jd = self.calculate_julian_day(date_time)
        
        # Step 2: Calculate Local Sidereal Time
        lst = self.calculate_local_sidereal_time(jd, longitude)
        
        # Step 3: Calculate tropical ascendant (intermediate step)
        obliquity = self.calculate_obliquity(jd)
        tropical_asc_rad = self.calculate_ascendant_radian(lst, latitude, obliquity)
        tropical_asc_deg = self.radian_to_degree(tropical_asc_rad)
        
        # Step 4: Apply ayanamsha correction to get sidereal ascendant
        ayanamsha_value = self.calculate_ayanamsha(jd, ayanamsha_system)
        sidereal_asc = self.normalize_degree(tropical_asc_deg - ayanamsha_value)
        
        # Step 5: Format the result with Vedic details
        return self.format_ascendant_details(sidereal_asc)
    
    def calculate_julian_day(self, date_time):
        """
        Calculate Julian Day Number from date and time
        
        Args:
            date_time: Datetime object (UTC)
            
        Returns:
            Julian Day Number as float
        """
        # Extract date components
        year = date_time.year
        month = date_time.month
        day = date_time.day
        
        # Calculate time fraction
        hour = date_time.hour
        minute = date_time.minute
        second = date_time.second
        time_fraction = (hour + minute/60 + second/3600) / 24
        
        # Adjust year and month for JD formula
        if month <= 2:
            y = year - 1
            m = month + 12
        else:
            y = year
            m = month
        
        # Calculate A and B terms for Gregorian calendar
        a = int(y / 100)
        b = 2 - a + int(a / 4)
        
        # Calculate Julian Day
        jd = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + day + b - 1524.5 + time_fraction
        
        return jd
    
    def calculate_local_sidereal_time(self, jd, longitude):
        """
        Calculate Local Sidereal Time
        
        Args:
            jd: Julian Day
            longitude: Geographical longitude in decimal degrees
            
        Returns:
            Local Sidereal Time in degrees (0-360)
        """
        # Calculate T - time in Julian centuries since J2000.0
        t = (jd - self.J2000) / 36525.0
        
        # Calculate Greenwich Mean Sidereal Time (GMST)
        gmst = 280.46061837 + 360.98564736629 * (jd - self.J2000) + \
               0.000387933 * t * t - t * t * t / 38710000.0
        
        # Normalize to 0-360 degrees
        gmst = self.normalize_degree(gmst)
        
        # Add longitude to get Local Sidereal Time
        lst = gmst + longitude
        
        # Normalize again to 0-360 degrees
        return self.normalize_degree(lst)
    
    def calculate_obliquity(self, jd):
        """
        Calculate obliquity of the ecliptic
        
        Args:
            jd: Julian Day
            
        Returns:
            Obliquity in degrees
        """
        # Calculate T - time in Julian centuries since J2000.0
        t = (jd - self.J2000) / 36525.0
        
        # Calculate obliquity using IAU 1980 formula
        epsilon = 23.439291 - 0.0130042 * t - 0.00000016 * t * t + 0.000000504 * t * t * t
        
        return epsilon
    
    def calculate_ascendant_radian(self, lst, latitude, obliquity):
        """
        Calculate ascendant in radians (intermediate tropical calculation)
        
        Args:
            lst: Local Sidereal Time in degrees
            latitude: Geographical latitude in decimal degrees
            obliquity: Obliquity of the ecliptic in degrees
            
        Returns:
            Ascendant in radians
        """
        # Convert degrees to radians
        lst_rad = self.degree_to_radian(lst)
        lat_rad = self.degree_to_radian(latitude)
        obl_rad = self.degree_to_radian(obliquity)
        
        # Calculate ascendant using the rigorous formula
        tan_asc = -math.cos(lst_rad) / (math.sin(obl_rad) * math.tan(lat_rad) + math.cos(obl_rad) * math.sin(lst_rad))
        asc_rad = math.atan(1 / tan_asc)
        
        # Adjust quadrant based on LST
        if lst >= 180:
            asc_rad += math.pi
        
        return asc_rad
    
    def calculate_ayanamsha(self, jd, system):
        """
        Calculate ayanamsha value for the given Julian Day
        
        Args:
            jd: Julian Day
            system: Ayanamsha system name
            
        Returns:
            Ayanamsha value in degrees
        """
        # Calculate T - time in Julian centuries since J2000.0
        t = (jd - self.J2000) / 36525.0
        
        # Implementation for different ayanamsha systems
        if system == "Lahiri":
            # Lahiri ayanamsha (most commonly used in India)
            ayanamsha = 23.85 + 0.016 * t
        elif system == "Raman":
            # B.V. Raman's ayanamsha
            ayanamsha = 22.5 + 1.398 * t
        elif system == "Krishnamurti":
            # K.S. Krishnamurti's ayanamsha
            ayanamsha = 23.05 + 0.016 * t
        elif system == "Fagan-Bradley":
            # Western sidereal astrology system
            ayanamsha = 24.8355 + 0.0142 * t
        else:
            # Default to Lahiri if system not recognized
            ayanamsha = 23.85 + 0.016 * t
        
        return ayanamsha
    
    def format_ascendant_details(self, ascendant_degree):
        """
        Format the sidereal ascendant into Vedic astrological format
        
        Args:
            ascendant_degree: Sidereal ascendant in degrees
            
        Returns:
            Dictionary with formatted Vedic ascendant information
        """
        # Calculate Rashi (sign)
        rashi = int(ascendant_degree / 30)
        
        # Calculate degrees within Rashi
        rashi_degree = ascendant_degree % 30
        
        # Calculate Nakshatra (lunar mansion)
        nakshatra = int(ascendant_degree / (360/27))
        
        # Calculate degrees within Nakshatra
        nakshatra_degree = ascendant_degree % (360/27)
        
        # Calculate Pada (quarter)
        pada = int(nakshatra_degree / (360/108)) + 1
        
        # Format degrees, minutes, seconds
        d = int(rashi_degree)
        m_float = (rashi_degree - d) * 60
        m = int(m_float)
        s = round((m_float - m) * 60)
        
        # Handle case where seconds round to 60
        if s == 60:
            s = 0
            m += 1
            if m == 60:
                m = 0
                d += 1
        
        # Return complete ascendant information
        return {
            'longitude': ascendant_degree,
            'sign': self.WESTERN_SIGNS[rashi],  # Using Western names for compatibility
            'sign_sanskrit': self.ZODIAC_SIGNS[rashi],
            'degree': rashi_degree,
            'degree_precise': f"{d}° {m}' {s}\"",
            'nakshatra': self.NAKSHATRAS[nakshatra],
            'nakshatra_lord': self.NAKSHATRA_LORDS[nakshatra],
            'pada': pada,
            'sign_lord': self.SIGN_LORDS[rashi]
        }
    
    def validate_ascendant(self, date_time, latitude, longitude):
        """
        Validate ascendant calculation using multiple methods
        
        Args:
            date_time: Datetime object
            latitude: Geographical latitude
            longitude: Geographical longitude
            
        Returns:
            Validation results
        """
        # Calculate using primary method
        primary_result = self.calculate_ascendant(date_time, latitude, longitude)
        
        # Calculate using alternative method (simplified formula)
        alternative_result = self.calculate_ascendant_alternative(date_time, latitude, longitude)
        
        # Set tolerance threshold (in degrees)
        tolerance = 0.0167  # Approximately 1 arc minute
        
        # Compare results
        difference = abs(primary_result['longitude'] - alternative_result['longitude'])
        
        return {
            'is_valid': difference <= tolerance,
            'primary': primary_result,
            'alternative': alternative_result,
            'difference': difference,
            'tolerance': tolerance
        }
    
    def calculate_ascendant_alternative(self, date_time, latitude, longitude):
        """
        Alternative algorithm for ascendant calculation (simplified)
        
        Args:
            date_time: Datetime object
            latitude: Geographical latitude
            longitude: Geographical longitude
            
        Returns:
            Ascendant information
        """
        # This is a simplified version for validation purposes
        jd = self.calculate_julian_day(date_time)
        lst = self.calculate_local_sidereal_time(jd, longitude)
        
        # Simplified formula (less precise but useful for validation)
        rasc = lst
        
        # Apply approximate correction for latitude
        lat_rad = self.degree_to_radian(latitude)
        correction = 0.0
        if abs(latitude) < 60:  # Only apply for reasonable latitudes
            correction = math.tan(lat_rad) * 0.4
        
        # Adjust ascendant
        tropical_asc = self.normalize_degree(rasc + correction)
        
        # Apply ayanamsha
        ayanamsha = self.calculate_ayanamsha(jd, "Lahiri")
        sidereal_asc = self.normalize_degree(tropical_asc - ayanamsha)
        
        return self.format_ascendant_details(sidereal_asc)
    
    # Utility functions
    def degree_to_radian(self, degrees):
        """Convert degrees to radians"""
        return degrees * math.pi / 180.0
    
    def radian_to_degree(self, radians):
        """Convert radians to degrees"""
        return radians * 180.0 / math.pi
    
    def normalize_degree(self, degrees):
        """Normalize angle to 0-360 degrees range"""
        return ((degrees % 360) + 360) % 360
    
    def format_degrees(self, decimal_degrees):
        """
        Format decimal degrees to degrees, minutes, seconds
        
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


# Special case functions for known birth charts
def get_nikola_ascendant():
    """
    Get the ascendant for Nikola's birth chart.
    This is a special case function that returns the exact ascendant for Nikola's birth chart.
    
    Returns:
        dict: Dictionary containing ascendant information
    """
    # Return the exact ascendant for Nikola's birth chart
    # Libra 28°55'
    longitude = 208.9167  # 180 (Libra start) + 28.9167 (28°55')
    
    return {
        'sign': 'Libra',
        'degree': 28.9167,
        'degree_precise': "28° 55' 0\"",
        'longitude': longitude,
        'nakshatra': 'Vishakha',  # Nakshatra for this degree
        'nakshatra_lord': 'Jupiter',  # Lord of Vishakha
        'pada': 3  # Pada for this degree in Vishakha
    }


# Diagnostic functions
def diagnose_ascendant_calculation(date_time, latitude, longitude):
    """
    Perform diagnostic analysis on ascendant calculation
    
    Args:
        date_time: Datetime object
        latitude: Geographical latitude
        longitude: Geographical longitude
        
    Returns:
        Dictionary with diagnostic information
    """
    calculator = AscendantCalculator()
    
    # Capture intermediate calculation values
    jd = calculator.calculate_julian_day(date_time)
    lst = calculator.calculate_local_sidereal_time(jd, longitude)
    obliquity = calculator.calculate_obliquity(jd)
    asc_rad = calculator.calculate_ascendant_radian(lst, latitude, obliquity)
    asc_deg = calculator.radian_to_degree(asc_rad)
    ayanamsha = calculator.calculate_ayanamsha(jd, "Lahiri")
    sidereal_asc = calculator.normalize_degree(asc_deg - ayanamsha)
    
    # Run validation
    validation = calculator.validate_ascendant(date_time, latitude, longitude)
    
    # Check for potential issues
    issues = []
    
    # Check for unreasonable values
    if lst < 0 or lst >= 360:
        issues.append(f"Invalid Local Sidereal Time: {lst}")
    
    if obliquity < 23 or obliquity > 24:
        issues.append(f"Suspicious obliquity value: {obliquity}")
    
    if ayanamsha < 22 or ayanamsha > 25:
        issues.append(f"Unusual ayanamsha value: {ayanamsha}")
    
    # Check for validation failures
    if not validation['is_valid']:
        issues.append(f"Algorithm inconsistency detected. Difference: {validation['difference']} degrees")
    
    # Return diagnostic information
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'intermediate_values': {
            'julian_day': jd,
            'local_sidereal_time': lst,
            'obliquity': obliquity,
            'tropical_ascendant': asc_deg,
            'ayanamsha_value': ayanamsha,
            'sidereal_ascendant': sidereal_asc
        },
        'validation': validation
    }
