# Power BI Dashboard Setup

This directory contains Power BI files for creating dashboards from the Databse ev_india and table ev_stations data.

## Files

- `ev-charging-dashboard.pbix` - Main Power BI dashboard file
- `data-connection.txt` - Database connection instructions

## Setup Instructions

### 1. Database Connection

1. Open Power BI Desktop
2. Click "Get Data" → "More" → "Database" → "PostgreSQL database"
3. Enter your database connection details:
   - Server: `localhost` (or your PostgreSQL server)
   - Database: `ev_india`
   - Data Connectivity mode: Import

### 2. Import Tables

Import the following table:
- `ev_stations` - Main stations data

### 3. Create Visualizations

#### Recommended Visualizations:

1. **Map Visualization**
   - Use latitude/longitude for location
   - Size by power_kw
   - Color by status

2. **Station Count by Country**
   - Bar chart showing stations per country

3. **Operator Analysis**
   - Pie chart of stations by operator
   - Bar chart of average power by operator

4. **Connection Type Distribution**
   - Donut chart showing connection types

5. **Power Distribution**
   - Histogram of power ratings

6. **Status Overview**
   - Card visuals showing operational vs non-operational

### 4. Key Metrics Cards

Create cards for:
- Total Stations
- Average Power (kW)
- Countries Covered
- Unique Operators

### 5. Filters

Add slicers for:
- Country
- Operator
- Connection Type
- Power Range
- Status

## Data Refresh

To keep your dashboard updated:

1. Set up scheduled refresh in Power BI Service
2. Or manually refresh data in Power BI Desktop
3. Republish to Power BI Service

## Sample DAX Measures

```dax
Total Stations = COUNT(ev_stations[id])

Average Power = AVERAGE(ev_stations[power_kw])

Operational Stations = 
CALCULATE(
    COUNT(ev_stations[id]),
    ev_stations[status] IN {"Operational", "Available"}
)

Operational Percentage = 
DIVIDE([Operational Stations], [Total Stations], 0) * 100
```

## Publishing

1. Save your .pbix file in this directory
2. Publish to Power BI Service
3. Share with your team or embed in websites