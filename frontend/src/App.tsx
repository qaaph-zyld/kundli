import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from './store';
import axios from 'axios';
import './App.css';
// @ts-ignore
import { v4 as uuidv4 } from 'uuid';
import {
  setDate,
  setTime,
  setSeconds,
  setAmPm,
  setCityInput,
  setLocation,
  setManualCoordinates,
  setLatitude,
  setLongitude,
  setTimezone,
  setAyanamsa,
  setHouseSystem,
  startCalculation,
  setChartData,
  calculationError,
  addSavedKundli,
  removeSavedKundli,
  loadKundli,
  SavedKundli
} from './store/kundliSlice';

// Zodiac sign symbols
const zodiacSymbols = ['♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓'];
const zodiacNames = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];

// Planet symbols
const planetSymbols: Record<string, string> = {
  'Sun': '☉',
  'Moon': '☽',
  'Mercury': '☿',
  'Venus': '♀',
  'Mars': '♂',
  'Jupiter': '♃',
  'Saturn': '♄',
  'Rahu': '☊',
  'Ketu': '☋',
  'Uranus': '♅',
  'Neptune': '♆',
  'Pluto': '♇'
};

// API base URL
const API_BASE_URL = 'http://localhost:5000';

function App() {
  const dispatch = useDispatch();
  const {
    date,
    time,
    seconds,
    amPm,
    cityInput,
    city,
    latitude,
    longitude,
    timezone,
    manualCoordinates,
    ayanamsa,
    houseSystem,
    loading,
    error,
    chartData,
    savedKundlis
  } = useSelector((state: RootState) => state.kundli);

  const [cityResults, setCityResults] = useState<any[]>([]);
  const [showCityDropdown, setShowCityDropdown] = useState(false);
  const [kundliName, setKundliName] = useState('');
  const [coordError, setCoordError] = useState<string | null>(null);
  const [ayanamsaOptions, setAyanamsaOptions] = useState<string[]>([]);
  const [houseSystemOptions, setHouseSystemOptions] = useState<{[key: string]: string}>({});

  useEffect(() => {
    // Fetch available ayanamsa options
    axios.get(`${API_BASE_URL}/ayanamsa_options`)
      .then(response => {
        setAyanamsaOptions(response.data);
      })
      .catch(error => {
        console.error('Error fetching ayanamsa options:', error);
      });
    
    // Fetch available house system options
    axios.get(`${API_BASE_URL}/house_system_options`)
      .then(response => {
        setHouseSystemOptions(response.data);
      })
      .catch(error => {
        console.error('Error fetching house system options:', error);
      });
  }, []);

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    dispatch(setDate(e.target.value));
  };

  const handleTimeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    dispatch(setTime(e.target.value));
  };

  const handleSecondsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    dispatch(setSeconds(e.target.value));
  };

  const handleAmPmChange = (value: 'AM' | 'PM') => {
    dispatch(setAmPm(value));
  };

  const handleCityInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    dispatch(setCityInput(value));
    
    if (value.length >= 2) {
      axios.get(`${API_BASE_URL}/search_place?q=${encodeURIComponent(value)}`)
        .then(response => {
          setCityResults(response.data);
          setShowCityDropdown(true);
        })
        .catch(error => {
          console.error('Error searching for city:', error);
        });
    } else {
      setCityResults([]);
      setShowCityDropdown(false);
    }
  };

  const handleCitySelect = (city: any) => {
    dispatch(setLocation({
      city: city.name,
      latitude: city.lat,
      longitude: city.lon,
      timezone: city.timezone
    }));
    setShowCityDropdown(false);
  };

  const toggleManualCoordinates = () => {
    dispatch(setManualCoordinates(!manualCoordinates));
  };

  const handleLatitudeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    dispatch(setLatitude(parseFloat(e.target.value)));
    validateCoordinates();
  };

  const handleLongitudeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    dispatch(setLongitude(parseFloat(e.target.value)));
    validateCoordinates();
  };
  
  const handleTimezoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    dispatch(setTimezone(e.target.value));
  };

  const handleAyanamsaChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    dispatch(setAyanamsa(e.target.value));
  };

  const handleHouseSystemChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    dispatch(setHouseSystem(e.target.value));
  };

  const validateCoordinates = () => {
    if (latitude === null || longitude === null) return;
    
    setCoordError(null);
    
    // Basic validation
    if (latitude < -90 || latitude > 90) {
      setCoordError('Latitude must be between -90° and 90°');
      return;
    }
    
    if (longitude < -180 || longitude > 180) {
      setCoordError('Longitude must be between -180° and 180°');
      return;
    }
    
    // Get timezone for these coordinates
    axios.post(`${API_BASE_URL}/validate_coordinates`, {
      latitude,
      longitude
    })
    .then(response => {
      if (response.data.valid && response.data.timezone) {
        dispatch(setTimezone(response.data.timezone));
      } else if (response.data.warning) {
        setCoordError(response.data.warning);
      }
    })
    .catch(error => {
      setCoordError(error.response?.data?.error || 'Invalid coordinates');
    });
  };

  const calculateChart = async () => {
    if (!date || !time || latitude === null || longitude === null || !timezone) {
      dispatch(calculationError('Please fill in all required fields'));
      return;
    }
    
    try {
      dispatch(startCalculation());
      
      // Convert 12-hour format to 24-hour if needed
      let hour24Format = time;
      if (amPm) {
        const [hours, minutes] = time.split(':').map(Number);
        const hour24 = amPm === 'PM' && hours < 12 
          ? hours + 12 
          : (amPm === 'AM' && hours === 12 ? 0 : hours);
        hour24Format = `${hour24.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds}`;
      }
      
      const response = await axios.post(`${API_BASE_URL}/calculate_chart`, {
        date,
        time: hour24Format,
        latitude,
        longitude,
        timezone,
        ayanamsa,
        houseSystem
      });
      
      dispatch(setChartData(response.data));
    } catch (error: any) {
      dispatch(calculationError(error.response?.data?.error || 'Failed to calculate chart'));
    }
  };

  const handleSaveKundli = () => {
    if (!chartData || !kundliName) return;
    
    const savedKundli: SavedKundli = {
      id: uuidv4(),
      name: kundliName,
      date,
      time,
      city,
      latitude: latitude || 0,
      longitude: longitude || 0,
      timezone,
      chartData,
      ayanamsa,
      houseSystem
    };
    
    dispatch(addSavedKundli(savedKundli));
    setKundliName('');
  };

  const handleDeleteKundli = (id: string) => {
    dispatch(removeSavedKundli(id));
  };

  const handleLoadKundli = (kundli: SavedKundli) => {
    dispatch(loadKundli(kundli));
  };

  const formatDegree = (deg: number) => {
    const degrees = Math.floor(deg);
    const minutes = Math.floor((deg - degrees) * 60);
    const seconds = Math.floor(((deg - degrees) * 60 - minutes) * 60);
    return `${degrees}° ${minutes}' ${seconds}"`;
  };

  const getDignityColor = (dignity: string) => {
    const dignityColors: {[key: string]: string} = {
      'Exalted': '#4CAF50',
      'Moolatrikona': '#8BC34A',
      'Own sign': '#CDDC39',
      'Friend\'s sign': '#FFC107',
      'Neutral': '#FF9800',
      'Enemy\'s sign': '#FF5722',
      'Debilitated': '#F44336'
    };
    
    return dignityColors[dignity] || '#757575';
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Vedic Astrology Calculator</h1>
      </header>
      
      <main>
        <div className="container">
          <div className="input-section">
            <h2>Birth Details</h2>
            
            <div className="form-group">
              <label>Birth Date:</label>
              <input
                type="date"
                value={date}
                onChange={handleDateChange}
              />
            </div>
            
            <div className="form-group time-group">
              <label>Birth Time:</label>
              <div className="time-inputs">
                <input
                  type="time"
                  value={time}
                  onChange={handleTimeChange}
                />
                <input
                  type="text"
                  placeholder="Seconds"
                  value={seconds}
                  onChange={handleSecondsChange}
                  maxLength={2}
                  className="seconds-input"
                />
                <div className="am-pm-toggle">
                  <button 
                    className={amPm === 'AM' ? 'active' : ''} 
                    onClick={() => handleAmPmChange('AM')}
                  >
                    AM
                  </button>
                  <button 
                    className={amPm === 'PM' ? 'active' : ''} 
                    onClick={() => handleAmPmChange('PM')}
                  >
                    PM
                  </button>
                </div>
              </div>
            </div>
            
            <div className="form-group">
              <label>Birth Place:</label>
              <input
                type="text"
                value={cityInput}
                onChange={handleCityInputChange}
                placeholder="Enter city name"
              />
              {showCityDropdown && cityResults.length > 0 && (
                <ul className="city-dropdown">
                  {cityResults.map((city, index) => (
                    <li key={index} onClick={() => handleCitySelect(city)}>
                      {city.name}
                    </li>
                  ))}
                </ul>
              )}
            </div>

            <div className="form-group manual-coords-toggle">
              <label>
                <input
                  type="checkbox"
                  checked={manualCoordinates}
                  onChange={toggleManualCoordinates}
                />
                Enter coordinates manually
              </label>
            </div>
            
            {manualCoordinates && (
              <div className="manual-coordinates">
                <div className="form-group">
                  <label>Latitude:</label>
                  <input
                    type="number"
                    value={latitude || ''}
                    onChange={handleLatitudeChange}
                    step="0.000001"
                    placeholder="e.g. 28.6139"
                  />
                </div>
                
                <div className="form-group">
                  <label>Longitude:</label>
                  <input
                    type="number"
                    value={longitude || ''}
                    onChange={handleLongitudeChange}
                    step="0.000001"
                    placeholder="e.g. 77.2090"
                  />
                </div>
                
                <div className="form-group">
                  <label>Timezone:</label>
                  <input
                    type="text"
                    value={timezone}
                    onChange={handleTimezoneChange}
                    placeholder="e.g. Asia/Kolkata"
                  />
                </div>
                
                {coordError && <div className="error-message">{coordError}</div>}
              </div>
            )}
            
            <div className="calculation-options">
              <div className="form-group">
                <label>Ayanamsa:</label>
                <select value={ayanamsa} onChange={handleAyanamsaChange}>
                  {ayanamsaOptions.map(option => (
                    <option key={option} value={option}>{option}</option>
                  ))}
                </select>
              </div>
              
              <div className="form-group">
                <label>House System:</label>
                <select value={houseSystem} onChange={handleHouseSystemChange}>
                  {Object.entries(houseSystemOptions).map(([key, value]) => (
                    <option key={key} value={key}>{value}</option>
                  ))}
                </select>
              </div>
            </div>
            
            <button 
              className="calculate-btn" 
              onClick={calculateChart}
              disabled={loading}
            >
              {loading ? 'Calculating...' : 'Calculate Chart'}
            </button>
            
            {error && <div className="error-message">{error}</div>}
          </div>
          
          {chartData && (
            <div className="chart-section">
              <h2>Birth Chart</h2>
              
              <div className="chart-info">
                <div className="ascendant-info">
                  <h3>Ascendant (Lagna)</h3>
                  <p>
                    <span className="zodiac-symbol">{zodiacSymbols[zodiacNames.indexOf(chartData.ascendant.sign)]}</span>
                    {chartData.ascendant.sign} {formatDegree(chartData.ascendant.degree)}
                  </p>
                  {chartData.ascendant.nakshatra && (
                    <p>Nakshatra: {chartData.ascendant.nakshatra} (Pada {chartData.ascendant.pada})</p>
                  )}
                </div>
                
                <div className="time-info">
                  <h3>Time Information</h3>
                  <p>Local: {chartData.timeInfo.local}</p>
                  <p>UTC: {chartData.timeInfo.utc}</p>
                  <p>Ayanamsa: {formatDegree(chartData.timeInfo.ayanamsa)}</p>
                  <p>Ghati: {chartData.timeInfo.ghati.toFixed(2)}</p>
                  <p>Vighati: {chartData.timeInfo.vighati.toFixed(2)}</p>
                  <p>Pal: {chartData.timeInfo.pal.toFixed(2)}</p>
                </div>
              </div>
              
              <div className="planet-table">
                <h3>Planetary Positions</h3>
                <table>
                  <thead>
                    <tr>
                      <th>Planet</th>
                      <th>Sign</th>
                      <th>Degree</th>
                      <th>Nakshatra</th>
                      <th>Pada</th>
                      <th>Dignity</th>
                    </tr>
                  </thead>
                  <tbody>
                    {chartData.planets.map((planet, index) => (
                      <tr key={index}>
                        <td>
                          <span className="planet-symbol">{planetSymbols[planet.name]}</span>
                          {planet.name}
                        </td>
                        <td>
                          <span className="zodiac-symbol">{zodiacSymbols[planet.sign - 1]}</span>
                          {zodiacNames[planet.sign - 1]}
                        </td>
                        <td>{formatDegree(planet.degree)}</td>
                        <td>{planet.nakshatra}</td>
                        <td>{planet.pada}</td>
                        <td style={{ color: getDignityColor(planet.dignity || '') }}>
                          {planet.dignity}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              
              <div className="house-table">
                <h3>House Cusps</h3>
                <table>
                  <thead>
                    <tr>
                      <th>House</th>
                      <th>Sign</th>
                      <th>Degree</th>
                    </tr>
                  </thead>
                  <tbody>
                    {chartData.houses.map((house) => (
                      <tr key={house.number}>
                        <td>{house.number}</td>
                        <td>
                          <span className="zodiac-symbol">{zodiacSymbols[parseInt(house.sign.toString()) - 1]}</span>
                          {house.sign}
                        </td>
                        <td>{formatDegree(house.degree)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              
              <div className="save-kundli">
                <input
                  type="text"
                  value={kundliName}
                  onChange={(e) => setKundliName(e.target.value)}
                  placeholder="Enter name to save chart"
                />
                <button onClick={handleSaveKundli} disabled={!kundliName}>Save Chart</button>
              </div>
            </div>
          )}
          
          {savedKundlis.length > 0 && (
            <div className="saved-kundlis">
              <h2>Saved Charts</h2>
              <div className="kundli-list">
                {savedKundlis.map((kundli) => (
                  <div key={kundli.id} className="saved-kundli-item">
                    <div className="kundli-details">
                      <strong>{kundli.name}</strong>
                      <span>{kundli.date} {kundli.time}</span>
                      <span>{kundli.city}</span>
                    </div>
                    <div className="kundli-actions">
                      <button onClick={() => handleLoadKundli(kundli)}>Load</button>
                      <button onClick={() => handleDeleteKundli(kundli.id)}>Delete</button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
