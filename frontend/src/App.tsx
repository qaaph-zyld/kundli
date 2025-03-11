import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from './store';
import { setDate, setTime, setLocation } from './store/kundliSlice';
import './App.css';

const App: React.FC = () => {
  const dispatch = useDispatch();
  const {
    date,
    time,
    city,
    latitude,
    longitude,
    timezone,
    loading,
    error
  } = useSelector((state: RootState) => state.kundli);

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    dispatch(setDate(e.target.value));
  };

  const handleTimeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    dispatch(setTime(e.target.value));
  };

  const handleCitySearch = async (query: string) => {
    try {
      const response = await fetch(`/api/search_cities?query=${encodeURIComponent(query)}`);
      const data = await response.json();
      if (data.length > 0) {
        const city = data[0];
        dispatch(setLocation({
          lat: city.lat,
          lon: city.lon,
          city: city.name,
          timezone: city.timezone
        }));
      }
    } catch (err) {
      console.error('Error searching cities:', err);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Vedic Astrology Calculator</h1>
      </header>
      <main>
        <div className="input-form">
          <div className="form-group">
            <label htmlFor="date">Date:</label>
            <input
              type="date"
              id="date"
              value={date}
              onChange={handleDateChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="time">Time:</label>
            <input
              type="time"
              id="time"
              value={time}
              onChange={handleTimeChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="city">City:</label>
            <input
              type="text"
              id="city"
              value={city}
              onChange={(e) => handleCitySearch(e.target.value)}
              placeholder="Search for a city..."
            />
          </div>
          {latitude && longitude && (
            <div className="coordinates">
              <p>Latitude: {latitude}°</p>
              <p>Longitude: {longitude}°</p>
              <p>Timezone: {timezone}</p>
            </div>
          )}
          {error && <div className="error">{error}</div>}
        </div>
        <div className="chart-container">
          {loading ? (
            <div className="loading">Loading chart...</div>
          ) : (
            <div className="placeholder-chart">
              {/* Chart visualization will be added here */}
              <p>South Indian Chart will be displayed here</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default App;
