\# EV Charging Station Map



!\[Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python\\\&logoColor=white)

!\[FastAPI](https://img.shields.io/badge/FastAPI-0.129.2-009688?logo=fastapi\\\&logoColor=white)

!\[SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy\\\&logoColor=white)

!\[PostgreSQL](https://img.shields.io/badge/PostgreSQL-PostGIS-336791?logo=postgresql\\\&logoColor=white)

!\[React](https://img.shields.io/badge/React-18-61DAFB?logo=react\\\&logoColor=black)

!\[Power BI](https://img.shields.io/badge/PowerBI-Dashboard-F2C811?logo=powerbi\\\&logoColor=black)

!\[Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker\\\&logoColor=white)

!\[License](https://img.shields.io/badge/License-MIT-yellow)



A \*\*full-stack geospatial application\*\* for collecting, storing, and visualizing electric vehicle charging stations.

The platform integrates multiple open datasets, processes them through a Python pipeline, stores them in a spatial database, and exposes them through a modern API and interactive map.



---



\# 🎯 Project Highlights



\* 10,000+ EV charging stations processed

\* Geospatial queries powered by PostGIS

\* Automated data pipeline

\* RESTful API with FastAPI

\* Interactive map using React + Leaflet

\* Power BI analytics dashboard

\* Production-ready architecture



---



\# 🏗️ Architecture



```

OpenChargeMap / OpenStreetMap

&nbsp;         ↓

&nbsp;  Data Pipeline (Python)

&nbsp;         ↓

&nbsp;PostgreSQL + PostGIS

&nbsp;         ↓

&nbsp;FastAPI Backend API

&nbsp;         ↓

&nbsp;React Frontend + Leaflet

&nbsp;         ↓

&nbsp;Power BI Analytics

```



---



\# 🛠️ Tech Stack



\## Backend



\* Python 3.10+

\* FastAPI

\* SQLAlchemy ORM

\* PostgreSQL

\* PostGIS (geospatial queries)

\* Uvicorn

\* Requests

\* Pandas



\## Frontend



\* React 18

\* Leaflet.js

\* Axios

\* CSS3



\## Data Pipeline



\* Python scripts

\* OpenChargeMap API

\* OpenStreetMap data

\* Scheduled jobs



\## Analytics



\* Power BI Desktop



\## Deployment



\* GitHub Pages (frontend)

\* GitHub Actions CI/CD

\* Docker support



---



\# 📦 Installation



\## Prerequisites



Install the following:



\* Python 3.10+

\* Node.js 16+

\* PostgreSQL 12+

\* PostGIS extension

\* Power BI Desktop (optional)



---



\# 🚀 Quick Start



\## 1. Clone the Repository



```bash

git clone https://github.com/sharadk11/ev\_charging\_stations.git

cd ev\_charging\_stations

```



---



\# 🗄️ Database Setup



This project uses \*\*PostgreSQL + PostGIS\*\* for spatial queries.



\## Create Database



```bash

createdb ev\_india

```



or inside PostgreSQL:



```sql

CREATE DATABASE ev\_india;

```



Connect to the database:



```bash

psql -U postgres -d ev\_india

```



---



\## Enable PostGIS Extension



```sql

CREATE EXTENSION IF NOT EXISTS postgis;

```



---



\## Initialize Database Schema



Run the schema initialization script:



```bash

psql -U postgres -d ev\_india -f database/init.sql

```



---



\# 📍 Database Schema



The main table used by the system:



```sql

CREATE TABLE ev\_stations (

&nbsp;   id SERIAL PRIMARY KEY,

&nbsp;   station\_name TEXT,

&nbsp;   address TEXT,

&nbsp;   city TEXT,

&nbsp;   state TEXT,

&nbsp;   latitude DOUBLE PRECISION,

&nbsp;   longitude DOUBLE PRECISION,

&nbsp;   location GEOGRAPHY(Point,4326),

&nbsp;   operator TEXT,

&nbsp;   charger\_type TEXT,

&nbsp;   connector\_type TEXT,

&nbsp;   power\_kw NUMERIC,

&nbsp;   access\_type TEXT,

&nbsp;   opening\_hours TEXT,

&nbsp;   contact\_phone TEXT,

&nbsp;   source TEXT,

&nbsp;   created\_at TIMESTAMP DEFAULT CURRENT\_TIMESTAMP

);

```



Spatial index for fast geolocation queries:



```sql

CREATE INDEX idx\_ev\_location

ON ev\_stations USING GIST(location);

```



---



\# ⚙️ Backend Setup



Create virtual environment:



```bash

python -m venv .venv

```



Activate environment:



Linux / Mac



```bash

source .venv/bin/activate

```



Windows



```bash

.venv\\Scripts\\activate

```



Install dependencies:



```bash

pip install -r requirements.txt

```



Create environment variables:



Linux / Mac



```bash

cp .env.example .env

```



Windows



```bash

copy .env.example .env

```



Edit `.env` with database credentials.



---



\# 🔄 Run Data Pipeline



Fetch EV charging station data and populate the database:



```bash

cd data-pipeline

python data\_collector.py

```



The pipeline will:



1\. Fetch charging stations from APIs

2\. Clean and normalize records

3\. Remove duplicates

4\. Upsert data into PostgreSQL

5\. Update spatial location column



---



\# 🚀 Start Backend API



```bash

uvicorn backend.main:app --reload

```



Backend will run at:



```

http://localhost:8000

```



Interactive API docs:



```

http://localhost:8000/docs

```



---



\# 🌍 Start Frontend



```bash

cd frontend

npm install

npm start

```



Frontend runs at:



```

http://localhost:3000

```



---



\# 📊 API Endpoints



\## Stations



| Endpoint           | Description          |

| ------------------ | -------------------- |

| `/stations`        | List stations        |

| `/stations/{id}`   | Get station details  |

| `/stations/search` | Advanced search      |

| `/stations/nearby` | Find nearby stations |



Example:



```

GET /stations/nearby?lat=18.6106\&lng=73.7850\&radius=10\&limit=50

```



This query uses \*\*PostGIS spatial functions\*\* internally:



```

ST\_DWithin()

ST\_Distance()

```



---



\# 🗺️ Map Features



\* Interactive Leaflet map

\* Marker clustering

\* Station popups

\* Status indicators

\* GPS location search

\* Radius-based discovery



---



\# 📈 Analytics Dashboard



Power BI dashboard can visualize:



\* Station density by region

\* Operator distribution

\* Charging power statistics

\* Connector types



Steps:



1\. Open Power BI Desktop

2\. Connect to PostgreSQL database

3\. Import `ev\_stations` table

4\. Create visualizations



---



\# 🔄 Data Pipeline Automation



The pipeline can run automatically using:



Linux



```

cron jobs

```



Windows



```

Windows Task Scheduler

```



or using Python scheduler:



```bash

python scheduler.py

```



---



\# 🧪 Testing



Backend tests:



```bash

pytest

```



API health check:



```bash

curl http://localhost:8000/health

```



---



\# 📱 Mobile Support



The frontend is responsive and supports:



\* Desktop browsers

\* Mobile phones

\* Tablets



Future plans include a \*\*React Native mobile application\*\*.



---



\# 🚀 Deployment



Recommended production stack:



```

React Frontend → CDN

&nbsp;       ↓

FastAPI Backend (Uvicorn / Gunicorn)

&nbsp;       ↓

PostgreSQL + PostGIS

```



Possible cloud platforms:



\* AWS

\* Azure

\* Google Cloud

\* Railway

\* Render



---



\# 📂 Project Structure



```

ev\_charging\_stations

│

├── backend

│   ├── main.py

│   ├── database.py

│   └── models.py

│

├── data-pipeline

│   ├── data\_collector.py

│   ├── scheduler.py

│   └── config.py

│

├── frontend

│

├── dashboard

│

├── database

│   └── init.sql

│

├── requirements.txt

└── README.md

```



---



\# 🤝 Contributing



1\. Fork repository

2\. Create feature branch



```

git checkout -b feature/new-feature

```



3\. Commit changes



```

git commit -m "Add new feature"

```



4\. Push branch



```

git push origin feature/new-feature

```



5\. Open Pull Request



---



\# 📄 License



This project is licensed under the \*\*MIT License\*\*.



---



\# 🙏 Acknowledgements



\* OpenChargeMap for EV charging data

\* OpenStreetMap for global map tiles

\* Leaflet.js for mapping

\* FastAPI for backend framework



---



\# 📞 Support



For questions or support:



Email: \*\*\[sharoar27n@gmail.com](mailto:sharoar27n@gmail.com)\*\*

or open an issue in the repository.



