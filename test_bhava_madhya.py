from datetime import datetime
from vedic_calculator.core import VedicCalculator

def test_bhava_madhya():
    """Test script to verify bhava madhya calculations"""
    # Create a test birth chart
    birth_datetime = datetime(1990, 1, 1, 12, 0, 0)
    lat = 28.6139  # Delhi latitude
    lon = 77.2090  # Delhi longitude
    
    # Initialize calculator
    calculator = VedicCalculator(birth_datetime, lat, lon)
    
    # Print ascendant
    asc_deg = calculator.ascendant['longitude']
    asc_sign = calculator.ascendant['sign']
    print(f"Ascendant: {asc_deg:.2f}° ({asc_sign})")
    
    # Print house cusps and bhava madhya points
    print("\nHouse Cusps and Bhava Madhya Points:")
    print("-" * 50)
    print(f"{'House':<6} {'Sign':<12} {'Cusp':<15} {'Bhava Madhya':<15}")
    print("-" * 50)
    
    for house_num, house_data in calculator.houses.items():
        cusp = house_data['cusp']
        bhava_madhya = house_data['bhava_madhya']
        
        # Get sign names
        cusp_sign_num = int(cusp / 30)
        cusp_sign = calculator.ZODIAC_SIGNS[cusp_sign_num]
        
        bhava_madhya_sign_num = int(bhava_madhya / 30)
        bhava_madhya_sign = calculator.ZODIAC_SIGNS[bhava_madhya_sign_num]
        
        # Format degrees
        cusp_formatted = calculator._format_degrees(cusp)
        bhava_madhya_formatted = calculator._format_degrees(bhava_madhya)
        
        print(f"{house_num:<6} {cusp_sign:<12} {cusp_formatted:<15} {bhava_madhya_formatted:<15} in {bhava_madhya_sign}")
    
    # Print planets with their distances from bhava madhya
    print("\nPlanets and Their Distances from Bhava Madhya:")
    print("-" * 60)
    print(f"{'Planet':<10} {'House':<6} {'Distance from Bhava Madhya':<30}")
    print("-" * 60)
    
    for planet_name, planet_data in calculator.planets.items():
        house_num = planet_data['house']
        longitude = planet_data['longitude']
        
        # Get bhava madhya of the house
        if house_num in calculator.houses:
            bhava_madhya = calculator.houses[house_num]['bhava_madhya']
            
            # Calculate distance from bhava madhya
            distance = min(
                (longitude - bhava_madhya) % 360,
                (bhava_madhya - longitude) % 360
            )
            
            print(f"{planet_name:<10} {house_num:<6} {distance:.2f}°")
    
    # Print bhava bala (house strength)
    print("\nBhava Bala (House Strength):")
    print("-" * 80)
    print(f"{'House':<6} {'Total':<8} {'Occupants':<10} {'Lord Place':<10} {'Lord Dignity':<12} {'Aspects':<8} {'Bhava Madhya':<12}")
    print("-" * 80)
    
    for house_num, bala in calculator.bhava_bala.items():
        total = bala['total']
        components = bala['components']
        
        print(f"{house_num:<6} {total:<8} {components['occupant_strength']:<10} {components['lord_placement_strength']:<10} {components['lord_dignity_strength']:<12} {components['aspect_strength']:<8} {components['bhava_madhya_strength']:<12}")

if __name__ == "__main__":
    test_bhava_madhya()
