import React, { useState, useEffect } from 'react';
import { searchStations, getNearbyStations } from '../services/api';
import './SearchPanel.css';

const SearchPanel = ({ onSearchResults, onLoading }) => {
  const [searchType, setSearchType] = useState('nearby');
  const [location, setLocation] = useState({ lat: '', lng: '' });
  const [radius, setRadius] = useState(10);
  const [filters, setFilters] = useState({
    country: '',
    operator: '',
    connection_type: '',
    min_power_kw: ''
  });
  const [useCurrentLocation, setUseCurrentLocation] = useState(false);

  const handleSearch = async () => {
    if (!location.lat || !location.lng) {
      alert('Please enter valid coordinates or use current location');
      return;
    }

    onLoading(true);
    try {
      let results;
      
      if (searchType === 'nearby') {
        results = await getNearbyStations(
          parseFloat(location.lat),
          parseFloat(location.lng),
          radius,
          100
        );
      } else {
        const searchParams = {
          latitude: parseFloat(location.lat),
          longitude: parseFloat(location.lng),
          radius_km: radius,
          limit: 100,
          ...Object.fromEntries(
            Object.entries(filters).filter(([_, value]) => value !== '')
          )
        };
        
        if (filters.min_power_kw) {
          searchParams.min_power_kw = parseFloat(filters.min_power_kw);
        }
        
        results = await searchStations(searchParams);
      }
      
      onSearchResults(results);
    } catch (error) {
      console.error('Search failed:', error);
      alert('Search failed. Please try again.');
    } finally {
      onLoading(false);
    }
  };

  const getCurrentLocation = () => {
    if (navigator.geolocation) {
      onLoading(true);
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            lat: position.coords.latitude.toFixed(6),
            lng: position.coords.longitude.toFixed(6)
          });
          setUseCurrentLocation(true);
          onLoading(false);
        },
        (error) => {
          console.error('Geolocation error:', error);
          alert('Unable to get current location. Please enter coordinates manually.');
          onLoading(false);
        }
      );
    } else {
      alert('Geolocation is not supported by this browser.');
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const clearFilters = () => {
    setFilters({
      country: '',
      operator: '',
      connection_type: '',
      min_power_kw: ''
    });
  };

  return (
    <div className="search-panel">
      <div className="search-section">
        <h3>🔍 Search Charging Stations</h3>
        
        <div className="search-type">
          <label>
            <input
              type="radio"
              value="nearby"
              checked={searchType === 'nearby'}
              onChange={(e) => setSearchType(e.target.value)}
            />
            Nearby Search
          </label>
          <label>
            <input
              type="radio"
              value="advanced"
              checked={searchType === 'advanced'}
              onChange={(e) => setSearchType(e.target.value)}
            />
            Advanced Search
          </label>
        </div>

        <div className="location-input">
          <h4>📍 Location</h4>
          <div className="coordinate-inputs">
            <input
              type="number"
              placeholder="Latitude"
              value={location.lat}
              onChange={(e) => setLocation(prev => ({ ...prev, lat: e.target.value }))}
              step="any"
            />
            <input
              type="number"
              placeholder="Longitude"
              value={location.lng}
              onChange={(e) => setLocation(prev => ({ ...prev, lng: e.target.value }))}
              step="any"
            />
          </div>
          <button 
            className="location-btn"
            onClick={getCurrentLocation}
          >
            📱 Use Current Location
          </button>
          {useCurrentLocation && (
            <small className="location-status">✅ Using current location</small>
          )}
        </div>

        <div className="radius-input">
          <label>
            🎯 Search Radius: {radius} km
            <input
              type="range"
              min="1"
              max="100"
              value={radius}
              onChange={(e) => setRadius(parseInt(e.target.value))}
            />
          </label>
        </div>

        {searchType === 'advanced' && (
          <div className="filters">
            <h4>🔧 Filters</h4>
            
            <input
              type="text"
              placeholder="Country (e.g., United States)"
              value={filters.country}
              onChange={(e) => handleFilterChange('country', e.target.value)}
            />
            
            <input
              type="text"
              placeholder="Operator (e.g., Tesla)"
              value={filters.operator}
              onChange={(e) => handleFilterChange('operator', e.target.value)}
            />
            
            <input
              type="text"
              placeholder="Connection Type (e.g., CCS)"
              value={filters.connection_type}
              onChange={(e) => handleFilterChange('connection_type', e.target.value)}
            />
            
            <input
              type="number"
              placeholder="Min Power (kW)"
              value={filters.min_power_kw}
              onChange={(e) => handleFilterChange('min_power_kw', e.target.value)}
              min="0"
              step="0.1"
            />
            
            <button 
              className="clear-filters-btn"
              onClick={clearFilters}
            >
              Clear Filters
            </button>
          </div>
        )}

        <button 
          className="search-btn"
          onClick={handleSearch}
          disabled={!location.lat || !location.lng}
        >
          🔍 Search Stations
        </button>
      </div>
    </div>
  );
};

export default SearchPanel;