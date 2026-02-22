import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom charging station icon
const chargingIcon = new L.Icon({
  iconUrl: 'data:image/svg+xml;base64,' + btoa(`
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#4CAF50" width="24" height="24">
      <path d="M14.5 11l-3 6v-4h-2l3-6v4h2zm3.5 6V9.5C18 8.1 16.9 7 15.5 7S13 8.1 13 9.5V11h-1V9.5C12 7.6 13.6 6 15.5 6S19 7.6 19 9.5V17h-1zm2-7h1v7h-1v-7zm-16 0h1v7H4v-7z"/>
    </svg>
  `),
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

// Component to handle map updates
function MapUpdater({ stations, selectedStation }) {
  const map = useMap();

  useEffect(() => {
    if (stations.length > 0) {
      const group = new L.featureGroup(
        stations.map(station => 
          L.marker([station.latitude, station.longitude])
        )
      );
      map.fitBounds(group.getBounds().pad(0.1));
    }
  }, [stations, map]);

  useEffect(() => {
    if (selectedStation) {
      map.setView([selectedStation.latitude, selectedStation.longitude], 15);
    }
  }, [selectedStation, map]);

  return null;
}

const MapComponent = ({ stations, selectedStation, onStationSelect, loading }) => {
  const [mapCenter, setMapCenter] = useState([39.8283, -98.5795]); // Center of US
  const [mapZoom, setMapZoom] = useState(4);

  const handleMarkerClick = (station) => {
    onStationSelect(station);
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'operational':
      case 'available':
        return '#4CAF50';
      case 'out of service':
      case 'unavailable':
        return '#f44336';
      case 'maintenance':
        return '#ff9800';
      default:
        return '#9e9e9e';
    }
  };

  const createCustomIcon = (station) => {
    const color = getStatusColor(station.status);
    return new L.Icon({
      iconUrl: 'data:image/svg+xml;base64,' + btoa(`
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="${color}" width="24" height="24">
          <path d="M14.5 11l-3 6v-4h-2l3-6v4h2zm3.5 6V9.5C18 8.1 16.9 7 15.5 7S13 8.1 13 9.5V11h-1V9.5C12 7.6 13.6 6 15.5 6S19 7.6 19 9.5V17h-1zm2-7h1v7h-1v-7zm-16 0h1v7H4v-7z"/>
        </svg>
      `),
      iconSize: [28, 28],
      iconAnchor: [14, 28],
      popupAnchor: [0, -28],
    });
  };

  return (
    <div style={{ height: '100%', width: '100%', position: 'relative' }}>
      {loading && (
        <div style={{
          position: 'absolute',
          top: '10px',
          right: '10px',
          background: 'rgba(255, 255, 255, 0.9)',
          padding: '10px',
          borderRadius: '5px',
          zIndex: 1000,
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          <div className="loading-spinner"></div>
          Loading stations...
        </div>
      )}
      
      <MapContainer
        center={mapCenter}
        zoom={mapZoom}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        <MapUpdater stations={stations} selectedStation={selectedStation} />
        
        {stations.map((station) => (
          <Marker
            key={station.id}
            position={[station.latitude, station.longitude]}
            icon={createCustomIcon(station)}
            eventHandlers={{
              click: () => handleMarkerClick(station),
            }}
          >
            <Popup>
              <div style={{ minWidth: '200px' }}>
                <h3 style={{ margin: '0 0 10px 0', fontSize: '16px' }}>
                  {station.name}
                </h3>
                <p style={{ margin: '5px 0', fontSize: '14px' }}>
                  <strong>Address:</strong> {station.address || 'N/A'}
                </p>
                <p style={{ margin: '5px 0', fontSize: '14px' }}>
                  <strong>City:</strong> {station.city || 'N/A'}
                </p>
                <p style={{ margin: '5px 0', fontSize: '14px' }}>
                  <strong>Operator:</strong> {station.operator_name || 'N/A'}
                </p>
                <p style={{ margin: '5px 0', fontSize: '14px' }}>
                  <strong>Status:</strong> 
                  <span style={{ 
                    color: getStatusColor(station.status),
                    fontWeight: 'bold',
                    marginLeft: '5px'
                  }}>
                    {station.status || 'Unknown'}
                  </span>
                </p>
                {station.power_kw && (
                  <p style={{ margin: '5px 0', fontSize: '14px' }}>
                    <strong>Power:</strong> {station.power_kw} kW
                  </p>
                )}
                <button
                  onClick={() => handleMarkerClick(station)}
                  style={{
                    marginTop: '10px',
                    padding: '5px 10px',
                    background: '#007bff',
                    color: 'white',
                    border: 'none',
                    borderRadius: '3px',
                    cursor: 'pointer',
                    fontSize: '12px'
                  }}
                >
                  View Details
                </button>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default MapComponent;