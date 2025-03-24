"""
Demonstration script for Ashtakavarga system
"""
from datetime import datetime
from vedic_calculator.core import VedicCalculator

def display_ashtakavarga_demo():
    """Display Ashtakavarga system demonstration"""
    # Create a test birth chart
    birth_datetime = datetime(1990, 1, 1, 12, 0, 0)
    lat = 28.6139  # Delhi latitude
    lon = 77.2090  # Delhi longitude
    
    print("Calculating Ashtakavarga for birth chart:")
    print(f"Date/Time: {birth_datetime}")
    print(f"Location: Delhi (Lat: {lat}, Lon: {lon})")
    print("-" * 60)
    
    # Initialize calculator
    calculator = VedicCalculator(birth_datetime, lat, lon)
    
    # Display Prastarashtakavarga (individual planet Ashtakavarga)
    print("\nPRASTARASHTAKAVARGA (Individual Planet Ashtakavarga):")
    print("=" * 60)
    
    for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
        planet_ashtakavarga = calculator.get_prastarashtakavarga(planet)
        total_bindus = calculator.get_planet_bindu_total(planet)
        
        print(f"\n{planet} Ashtakavarga (Total Bindus: {total_bindus}):")
        print("-" * 60)
        print("House: ", end="")
        for house in range(1, 13):
            print(f"{house:4}", end="")
        print("\nBindu: ", end="")
        for house in range(1, 13):
            print(f"{planet_ashtakavarga[house]:4}", end="")
        print()
    
    # Display Sarvashtakavarga (combined Ashtakavarga)
    print("\n\nSARVASHTAKAVARGA (Combined Ashtakavarga):")
    print("=" * 60)
    sarvashtakavarga = calculator.get_sarvashtakavarga()
    
    print("House: ", end="")
    for house in range(1, 13):
        print(f"{house:4}", end="")
    print("\nBindu: ", end="")
    for house in range(1, 13):
        print(f"{sarvashtakavarga[house]:4}", end="")
    print()
    
    # Display Ashtakavarga strength assessment
    print("\n\nASHTAKAVARGA STRENGTH ASSESSMENT:")
    print("=" * 60)
    strength = calculator.get_ashtakavarga_strength()
    
    print("\nPlanet Strengths:")
    print("-" * 60)
    print(f"{'Planet':<10} {'Total Bindus':<15} {'Strength':<10}")
    print("-" * 60)
    for planet, data in strength['planet_strengths'].items():
        print(f"{planet:<10} {data['total_bindus']:<15} {data['strength']:<10}")
    
    print("\nHouse Strengths:")
    print("-" * 60)
    print(f"{'House':<10} {'Total Bindus':<15} {'Strength':<10}")
    print("-" * 60)
    for house in range(1, 13):
        data = strength['house_strengths'][house]
        print(f"{house:<10} {data['total_bindus']:<15} {data['strength']:<10}")

if __name__ == "__main__":
    display_ashtakavarga_demo()
