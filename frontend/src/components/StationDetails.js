import React from 'react';
import './StationDetails.css';

const StationDetails = ({ station, onClose }) => {
  if (!station) return null;

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

  const openInMaps = () => {
    const url = `https://www.google.com/maps/search/?api=1&query=${station.latitude},${station.longitude}`;
    window.open(url, '_blank');
  };

  return (
    <div className="station-details">
      <div className="details-header">
        <h3>{station.name}</h3>
        <button className="close-btn" onClick={onClose}>×</button>
      </div>
      
      <div className="details-content">
        <div className="detail-item">
          <span className="label">📍 Address:</span>
          <span className="value">{station.address || 'N/A'}</span>
        </div>
        
        <div className="detail-item">
          <span className="label">🏙️ City:</span>
          <span className="value">{station.city || 'N/A'}</span>
        </div>
        
        <div className="detail-item">
          <span className="label">🌍 Country:</span>
          <span className="value">{station.country || 'N/A'}</span>
        </div>
        
        <div className="detail-item">
          <span className="label">🏢 Operator:</span>
          <span className="value">{station.operator_name || 'N/A'}</span>
        </div>
        
        <div className="detail-item">
          <span className="label">🔌 Connection:</span>
          <span className="value">{station.connection_type || 'N/A'}</span>
        </div>
        
        {station.power_kw && (
          <div className="detail-item">
            <span className="label">⚡ Power:</span>
            <span className="value">{station.power_kw} kW</span>
          </div>
        )}
        
        <div className="detail-item">
          <span className="label">📊 Status:</span>
          <span 
            className="value status"
            style={{ color: getStatusColor(station.status) }}
          >
            {station.status || 'Unknown'}
          </span>
        </div>
        
        <div className="detail-item">
          <span className="label">🚪 Access:</span>
          <span className="value">{station.access_type || 'N/A'}</span>
        </div>
        
        <div className="detail-item">
          <span className="label">📍 Coordinates:</span>
          <span className="value">
            {station.latitude?.toFixed(6)}, {station.longitude?.toFixed(6)}
          </span>
        </div>
        
        {station.cost_description && (
          <div className="detail-item">
            <span className="label">💰 Cost:</span>
            <span className="value">{station.cost_description}</span>
          </div>
        )}
        
        <div className="detail-item">
          <span className="label">🕒 Last Updated:</span>
          <span className="value">
            {new Date(station.updated_at).toLocaleDateString()}
          </span>
        </div>
      </div>
      
      <div className="details-actions">
        <button className="action-btn primary" onClick={openInMaps}>
          🗺️ Open in Maps
        </button>
        <button className="action-btn secondary" onClick={onClose}>
          Close
        </button>
      </div>
    </div>
  );
};

export default StationDetails;