# EV Charging Station Map

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.129.2-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.46-D71F00?logo=sqlalchemy&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-PostGIS-336791?logo=postgresql&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![PowerBI](https://img.shields.io/badge/PowerBI-Dashboard-F2C811?logo=powerbi&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
A comprehensive end-to-end application for mapping and analyzing electric vehicle charging stations using data from OpenChargeMap and OpenStreetMap.

## 🎯 Project Highlights

- 10,000+ EV charging stations processed
- Spatial queries powered by PostGIS
- RESTful API with 15+ endpoints
- Modular data pipeline architecture
- Production-ready backend structure

## 🏗️ Architecture

```
Data Sources (OpenChargeMap, OpenStreetMap)
↓
Data Pipeline (Python scripts)
↓
Database (PostgreSQL)
↓
Backend API (FastAPI)
↓
Frontend App (React + Leaflet)
↓
Dashboard (Power BI)
```
🧪 Backend Quick Start (WSL / Linux)
```
# Clone
git clone git@github.com:sharadk11/ev_charging_stations.git
cd ev_charging_stations

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Start server
uvicorn backend.main:app --reload
```


## 🚀 Features

- **Real-time Data Collection**: Automated data pipeline fetching from OpenChargeMap API
- **Spatial Search**: Find charging stations within specified radius
- **Interactive Map**: Leaflet.js-powered map with OpenStreetMap tiles
- **Advanced Filtering**: Filter by country, operator, connection type, power rating
- **Detailed Station Info**: Complete station details with status indicators
- **Analytics Dashboard**: Power BI dashboard for data insights
- **Responsive Design**: Works on desktop and mobile devices

## 🛠️ Tech Stack

### Backend
- **Python 3.10+** - Core language
- **FastAPI** - REST API framework
- **PostgreSQL + PostGIS** - Database with spatial extensions
- **SQLAlchemy** - ORM
- **Requests** - HTTP client for API calls
- **Pandas** - Data processing

### Frontend
- **React 18** - UI framework
- **Leaflet.js** - Interactive maps
- **Axios** - HTTP client
- **CSS3** - Styling

### Data Pipeline
- **Python Schedule** - Task scheduling
- **Windows Task Scheduler** - Production scheduling

### Analytics
- **Power BI Desktop** - Dashboard creation

### Deployment
- **GitHub Pages** - Frontend hosting
- **GitHub Actions** - CI/CD pipeline

## 📦 Installation

### Prerequisites
- Python 3.10+
- Node.js 16+
- PostgreSQL 12+ with PostGIS extension
- Power BI Desktop (for dashboards)

### 1. Clone Repository
```bash
git clone git@github.com:sharadk11/ev_charging_stations.git
cd ev_charging_stations

```

### 2. Database Setup
```bash
# Create database
createdb ev_india

# Enable PostGIS extension
psql -U postgres -d ev_india -c "CREATE EXTENSION IF NOT EXISTS postgis;"

# Run initialization script
psql -U postgres -d ev_india -f database/init.sql

```

### 3. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Copy environment file and configure
# Linux / Mac
cp .env.example .env

# Windows
copy .env.example .env
# Edit .env with your database credentials and API keys

# Run data collection (first time)
cd data-pipeline
python data_collector.py

# Start API server
uvicorn backend.main:app --reload
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 5. Data Pipeline (Production)
```bash
# For continuous data updates
cd data-pipeline
python scheduler.py

# Or set up Windows Task Scheduler to run data_collector.py daily
```

## 🔧 Configuration

### Environment Variables (.env)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/ev_india
OPENCHARGE_API_KEY=your_api_key_here
API_HOST=localhost
API_PORT=8000
REACT_APP_API_URL=http://localhost:8000
```

### Data Collection Settings (data-pipeline/config.py)
- `COUNTRY_CODES`: Countries to collect data for
- `MAX_RESULTS`: Maximum stations per API call
- `UPDATE_INTERVAL_HOURS`: How often to update data

## 📊 API Endpoints

### Stations
- `GET /stations` - List all stations with pagination
- `GET /stations/{id}` - Get specific station
- `POST /stations/search` - Advanced search with filters
- `GET /stations/nearby` - Find nearby stations

### Analytics
- `GET /stats` - Database statistics
- `GET /health` - Health check

### Example API Usage
```javascript
// Search for stations near coordinates
const response = await fetch('/stations/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    latitude: 40.7128,
    longitude: -74.0060,
    radius_km: 10,
    min_power_kw: 50
  })
});
```

## 🗺️ Map Features

- **Interactive Markers**: Click stations for details
- **Status Colors**: Green (operational), Red (out of service), Orange (maintenance)
- **Popup Information**: Quick station overview
- **Zoom Controls**: Navigate and explore
- **Current Location**: Use GPS to find nearby stations

## 📈 Dashboard Setup

1. Open Power BI Desktop
2. Connect to PostgreSQL database
3. Import `charging_stations` table
4. Create visualizations (see dashboard/README.md)
5. Publish to Power BI Service

## 🚀 Deployment

### Frontend (GitHub Pages)
1. Update `homepage` in frontend/package.json
2. Push to GitHub
3. Enable GitHub Pages in repository settings
4. GitHub Actions will auto-deploy on push to main

### Backend (Production)
- Deploy to cloud provider (AWS, Azure, GCP)
- Set up environment variables
- Configure database connection
- Set up SSL certificate

## 🔄 Data Pipeline

The data pipeline runs automatically and:
1. Fetches latest data from OpenChargeMap API
2. Processes and cleans the data
3. Updates PostgreSQL database
4. Handles duplicates and updates existing records

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test

# API health check
curl http://localhost:8000/health
```

## 📱 Mobile Support

The application is fully responsive and works on:
- Desktop browsers
- Mobile phones
- Tablets

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [OpenChargeMap](https://openchargemap.org/) for charging station data
- [OpenStreetMap](https://www.openstreetmap.org/) for map tiles
- [Leaflet.js](https://leafletjs.com/) for mapping library
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent API framework

## 📞 Support


For support, email sharoar27n@gmail.com or create an issue in the GitHub repository.
