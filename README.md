# Vedic Kundli Calculator

A simple web application for calculating Vedic (Indian) astrological birth charts using sidereal calculations.

## Features

- Calculate birth chart based on date, time, and location
- Display planetary positions in Vedic zodiac signs
- User-friendly interface
- Timezone support

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Enter birth details:
   - Date
   - Time
   - Place
   - Latitude
   - Longitude
   - Timezone

4. Click "Calculate Kundli" to see the planetary positions

## Technical Details

- Built with Flask
- Uses vedicastro library for Vedic astronomical calculations
- Frontend built with Bootstrap and vanilla JavaScript
- Timezone handling with moment.js

## Note

This is an MVP version focusing on basic birth chart calculations. Future versions will include:
- House calculations
- Nakshatra positions
- Dasha calculations
- Yoga identification
- PDF report generation
