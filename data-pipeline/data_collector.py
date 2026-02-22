import requests
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from typing import List, Dict, Optional
from config import DATABASE_URL, OPENCHARGE_API_KEY, OPENCHARGE_BASE_URL, MAX_RESULTS, COUNTRY_CODES

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EVChargingDataCollector:
    def __init__(self):
        self.db_connection = None
        self.connect_to_database()
    
    def connect_to_database(self):
        """Establish database connection"""
        try:
            self.db_connection = psycopg2.connect(DATABASE_URL)
            logger.info("Connected to database successfully")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def fetch_opencharge_data(self, country_code: str) -> List[Dict]:
        """Fetch charging station data from OpenChargeMap API"""
        params = {
            'output': 'json',
            'countrycode': country_code,
            'maxresults': MAX_RESULTS,
            'compact': 'true',
            'verbose': 'false'
        }
        
        if OPENCHARGE_API_KEY:
            params['key'] = OPENCHARGE_API_KEY
        
        try:
            response = requests.get(OPENCHARGE_BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Fetched {len(data)} charging stations for {country_code}")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch data for {country_code}: {e}")
            return []
    
    def process_station_data(self, raw_data: List[Dict]) -> pd.DataFrame:
        """Process raw API data into structured format"""
        processed_stations = []
        
        for station in raw_data:
            try:
                # Extract basic information
                processed_station = {
                    'external_id': str(station.get('ID', '')),
                    'name': station.get('AddressInfo', {}).get('Title', 'Unknown'),
                    'address': station.get('AddressInfo', {}).get('AddressLine1', ''),
                    'city': station.get('AddressInfo', {}).get('Town', ''),
                    'country': station.get('AddressInfo', {}).get('Country', {}).get('Title', ''),
                    'latitude': station.get('AddressInfo', {}).get('Latitude'),
                    'longitude': station.get('AddressInfo', {}).get('Longitude'),
                    'operator_name': station.get('OperatorInfo', {}).get('Title', '') if station.get('OperatorInfo') else '',
                    'status': station.get('StatusType', {}).get('Title', 'Unknown') if station.get('StatusType') else 'Unknown',
                    'access_type': station.get('UsageType', {}).get('Title', '') if station.get('UsageType') else ''
                }
                
                # Extract connection information (first connection if available)
                connections = station.get('Connections', [])
                if connections:
                    first_connection = connections[0]
                    processed_station['connection_type'] = first_connection.get('ConnectionType', {}).get('Title', '')
                    processed_station['power_kw'] = first_connection.get('PowerKW')
                else:
                    processed_station['connection_type'] = ''
                    processed_station['power_kw'] = None
                
                # Only add stations with valid coordinates
                if processed_station['latitude'] and processed_station['longitude']:
                    processed_stations.append(processed_station)
                    
            except Exception as e:
                logger.warning(f"Failed to process station {station.get('ID', 'unknown')}: {e}")
                continue
        
        return pd.DataFrame(processed_stations)
    
    def upsert_stations(self, df: pd.DataFrame):
        """Insert or update charging stations in database"""
        if df.empty:
            logger.warning("No data to insert")
            return
        
        cursor = self.db_connection.cursor()
        
        try:
            for _, row in df.iterrows():
                upsert_query = """
                INSERT INTO charging_stations 
                (external_id, name, address, city, country, latitude, longitude, 
                 operator_name, connection_type, power_kw, status, access_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (external_id) 
                DO UPDATE SET
                    name = EXCLUDED.name,
                    address = EXCLUDED.address,
                    city = EXCLUDED.city,
                    country = EXCLUDED.country,
                    latitude = EXCLUDED.latitude,
                    longitude = EXCLUDED.longitude,
                    operator_name = EXCLUDED.operator_name,
                    connection_type = EXCLUDED.connection_type,
                    power_kw = EXCLUDED.power_kw,
                    status = EXCLUDED.status,
                    access_type = EXCLUDED.access_type,
                    updated_at = CURRENT_TIMESTAMP
                """
                
                cursor.execute(upsert_query, (
                    row['external_id'], row['name'], row['address'], row['city'],
                    row['country'], row['latitude'], row['longitude'],
                    row['operator_name'], row['connection_type'], row['power_kw'],
                    row['status'], row['access_type']
                ))
            
            self.db_connection.commit()
            logger.info(f"Successfully upserted {len(df)} charging stations")
            
        except Exception as e:
            self.db_connection.rollback()
            logger.error(f"Failed to upsert stations: {e}")
            raise
        finally:
            cursor.close()
    
    def run_data_collection(self):
        """Main method to run the complete data collection process"""
        logger.info("Starting data collection process")
        
        all_stations = []
        
        for country_code in COUNTRY_CODES:
            logger.info(f"Processing country: {country_code}")
            raw_data = self.fetch_opencharge_data(country_code)
            
            if raw_data:
                processed_df = self.process_station_data(raw_data)
                all_stations.append(processed_df)
        
        if all_stations:
            combined_df = pd.concat(all_stations, ignore_index=True)
            logger.info(f"Total stations processed: {len(combined_df)}")
            self.upsert_stations(combined_df)
        else:
            logger.warning("No data collected from any country")
        
        logger.info("Data collection process completed")
    
    def close_connection(self):
        """Close database connection"""
        if self.db_connection:
            self.db_connection.close()
            logger.info("Database connection closed")

if __name__ == "__main__":
    collector = EVChargingDataCollector()
    try:
        collector.run_data_collection()
    finally:
        collector.close_connection()