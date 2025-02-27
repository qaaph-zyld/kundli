import os
import csv
import json
import urllib.request
import zipfile
import io

def download_and_process_cities():
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Download cities1000.zip from GeoNames
    url = 'https://download.geonames.org/export/dump/cities1000.zip'
    print("Downloading cities1000.zip...")
    
    response = urllib.request.urlopen(url)
    zip_file = zipfile.ZipFile(io.BytesIO(response.read()))
    
    # Process the cities file
    cities = []
    print("Processing cities data...")
    
    with zip_file.open('cities1000.txt') as file:
        for line in io.TextIOWrapper(file, encoding='utf-8'):
            # GeoNames TSV format:
            # 0:geonameid, 1:name, 2:asciiname, 3:alternatenames, 4:latitude, 5:longitude,
            # 6:feature class, 7:feature code, 8:country code, 9:cc2, 10:admin1 code,
            # 11:admin2 code, 12:admin3 code, 13:admin4 code, 14:population, 15:elevation,
            # 16:dem, 17:timezone, 18:modification date
            
            fields = line.strip().split('\t')
            if len(fields) >= 19:
                name = fields[1]
                lat = float(fields[4])
                lon = float(fields[5])
                country = fields[8]
                timezone = fields[17]
                population = int(fields[14])
                
                # Format coordinates in DMS (Degrees, Minutes, Seconds)
                lat_deg = abs(int(lat))
                lat_min = abs(int((abs(lat) - lat_deg) * 60))
                lat_dir = 'N' if lat >= 0 else 'S'
                
                lon_deg = abs(int(lon))
                lon_min = abs(int((abs(lon) - lon_deg) * 60))
                lon_dir = 'E' if lon >= 0 else 'W'
                
                display = f"{name}, {country} ({lat_deg}° {lat_min}' {lat_dir}, {lon_deg}° {lon_min}' {lon_dir})"
                
                cities.append({
                    'name': name,
                    'display': display,
                    'lat': lat,
                    'lon': lon,
                    'country': country,
                    'timezone': timezone,
                    'population': population
                })
    
    # Sort cities by population (descending)
    cities.sort(key=lambda x: x['population'], reverse=True)
    
    # Save to JSON file
    output_file = os.path.join(data_dir, 'cities.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({'cities': cities}, f, indent=2, ensure_ascii=False)
    
    print(f"Processed {len(cities)} cities and saved to {output_file}")

if __name__ == '__main__':
    download_and_process_cities()
