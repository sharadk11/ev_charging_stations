import React from 'react';
import './StatsPanel.css';

const StatsPanel = ({ stats }) => {
  if (!stats) return null;

  return (
    <div className="stats-panel">
      <h3>📊 Database Statistics</h3>
      
      <div className="stat-item">
        <span className="stat-label">🔌 Total Stations:</span>
        <span className="stat-value">{stats.total_stations?.toLocaleString() || 0}</span>
      </div>
      
      {stats.avg_power_kw && (
        <div className="stat-item">
          <span className="stat-label">⚡ Avg Power:</span>
          <span className="stat-value">{stats.avg_power_kw.toFixed(1)} kW</span>
        </div>
      )}
      
      <div className="stat-section">
        <h4>🌍 Countries ({stats.countries?.length || 0})</h4>
        <div className="stat-list">
          {stats.countries?.slice(0, 5).map((country, index) => (
            <span key={index} className="stat-tag">{country}</span>
          ))}
          {stats.countries?.length > 5 && (
            <span className="stat-more">+{stats.countries.length - 5} more</span>
          )}
        </div>
      </div>
      
      <div className="stat-section">
        <h4>🏢 Top Operators ({stats.operators?.length || 0})</h4>
        <div className="stat-list">
          {stats.operators?.slice(0, 3).map((operator, index) => (
            <span key={index} className="stat-tag">{operator}</span>
          ))}
          {stats.operators?.length > 3 && (
            <span className="stat-more">+{stats.operators.length - 3} more</span>
          )}
        </div>
      </div>
      
      <div className="stat-section">
        <h4>🔌 Connection Types ({stats.connection_types?.length || 0})</h4>
        <div className="stat-list">
          {stats.connection_types?.slice(0, 4).map((type, index) => (
            <span key={index} className="stat-tag">{type}</span>
          ))}
          {stats.connection_types?.length > 4 && (
            <span className="stat-more">+{stats.connection_types.length - 4} more</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default StatsPanel;