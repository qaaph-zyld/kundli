import requests
import json
import traceback
from datetime import datetime

# Sample data for testing
test_data = {
    "date": "2025-03-11",
    "time": "20:57:00",
    "latitude": 18.9647,
    "longitude": 72.8258,
    "timezone": "Asia/Kolkata",
    "ayanamsa": "Lahiri",
    "houseSystem": "W"
}

try:
    # Make the API request
    response = requests.post(
        "http://127.0.0.1:5000/calculate_chart",
        json=test_data
    )

    # Print the response
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        # Format the JSON response for better readability
        formatted_response = json.dumps(response.json(), indent=2)
        print("Response:")
        print(formatted_response)
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")
    traceback.print_exc()
