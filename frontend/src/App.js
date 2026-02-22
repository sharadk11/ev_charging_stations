import React, { useState, useEffect } from 'react';
import MapComponent from './components/MapComponent';
import SearchPanel from './components/SearchPanel';
import StationDetails from './components/StationDetails';
import StatsPanel from './components/StatsPanel';
import { getStats } from './services/api';
import './App.css';

function App() {
  const [selectedStation, setSelectedStation] = useState(null);
  const [searchResults, setSearchResults] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Load initial stats
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const statsData = await getStats();
      setStats(statsData);
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  };

  const handleStationSelect = (station) => {
    setSelectedStation(station);
  };

  const handleSearchResults = (results) => {
    setSearchResults(results);
    setSelectedStation(null);
  };

  const handleCloseDetails = () => {
    setSelectedStation(null);
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🔌 EV Charging Station Map</h1>
        <p>Find electric vehicle charging stations near you</p>
      </header>

      <div className="app-content">
        <div className="sidebar">
          <SearchPanel 
            onSearchResults={handleSearchResults}
            onLoading={setLoading}
          />
          
          {stats && <StatsPanel stats={stats} />}
          
          {selectedStation && (
            <StationDetails 
              station={selectedStation}
              onClose={handleCloseDetails}
            />
          )}
        </div>

        <div className="map-container">
          <MapComponent
            stations={searchResults}
            selectedStation={selectedStation}
            onStationSelect={handleStationSelect}
            loading={loading}
          />
        </div>
      </div>
    </div>
  );
}

export default App;