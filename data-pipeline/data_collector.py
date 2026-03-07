import requests
import pandas as pd
import psycopg2
import logging
from typing import List, Dict
from config import (
    DATABASE_URL,
    OPENCHARGE_API_KEY,
    OPENCHARGE_BASE_URL,
    MAX_RESULTS,
    COUNTRY_CODES,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class EVChargingDataCollector:
    def __init__(self):
        self.db_connection = None
        self.connect_to_database()

    def connect_to_database(self):
        try:
            self.db_connection = psycopg2.connect(DATABASE_URL)
            logger.info("Connected to database successfully")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def fetch_opencharge_data(self, country_code: str) -> List[Dict]:
        params = {
            "output": "json",
            "countrycode": country_code,
            "maxresults": MAX_RESULTS,
            "compact": "true",
            "verbose": "false",
        }

        if OPENCHARGE_API_KEY:
            params["key"] = OPENCHARGE_API_KEY

        try:
            response = requests.get(
                OPENCHARGE_BASE_URL,
                params=params,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            logger.info(f"Fetched {len(data)} stations for {country_code}")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"API fetch failed for {country_code}: {e}")
            return []

    def process_station_data(self, raw_data: List[Dict]) -> pd.DataFrame:
        processed = []

        for station in raw_data:
            try:
                address = station.get("AddressInfo", {})
                connections = station.get("Connections", [])

                latitude = address.get("Latitude")
                longitude = address.get("Longitude")

                if latitude is None or longitude is None:
                    continue

                connector_type = None
                power_kw = None
                charger_type = None

                if connections:
                    first = connections[0]
                    connector_type = (
                        first.get("ConnectionType", {}).get("Title")
                    )
                    power_kw = first.get("PowerKW")
                    charger_type = first.get("Level", {}).get("Title")

                processed.append(
                    {
                        "station_name": address.get("Title"),
                        "address": address.get("AddressLine1"),
                        "city": address.get("Town"),
                        "state": address.get("StateOrProvince"),
                        "latitude": latitude,
                        "longitude": longitude,
                        "operator": (
                            station.get("OperatorInfo", {}).get("Title")
                            if station.get("OperatorInfo")
                            else None
                        ),
                        "charger_type": charger_type,
                        "connector_type": connector_type,
                        "power_kw": power_kw,
                        "access_type": (
                            station.get("UsageType", {}).get("Title")
                            if station.get("UsageType")
                            else None
                        ),
                        "opening_hours": None,
                        "contact_phone": None,
                        "source": "OpenChargeMap",
                    }
                )

            except Exception as e:
                logger.warning(
                    f"Failed to process station {station.get('ID')}: {e}"
                )
                continue

        return pd.DataFrame(processed)

    def upsert_stations(self, df: pd.DataFrame):
        if df.empty:
            logger.warning("No stations to insert/update")
            return

        cursor = self.db_connection.cursor()

        upsert_query = """
        INSERT INTO ev_stations (
            station_name,
            address,
            city,
            state,
            latitude,
            longitude,
            operator,
            charger_type,
            connector_type,
            power_kw,
            access_type,
            opening_hours,
            contact_phone,
            source
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (station_name, latitude, longitude)
        DO UPDATE SET
            address = EXCLUDED.address,
            city = EXCLUDED.city,
            state = EXCLUDED.state,
            operator = EXCLUDED.operator,
            charger_type = EXCLUDED.charger_type,
            connector_type = EXCLUDED.connector_type,
            power_kw = EXCLUDED.power_kw,
            access_type = EXCLUDED.access_type,
            opening_hours = EXCLUDED.opening_hours,
            contact_phone = EXCLUDED.contact_phone,
            source = EXCLUDED.source
        """

        try:
            for _, row in df.iterrows():
                cursor.execute(
                    upsert_query,
                    (
                        row["station_name"],
                        row["address"],
                        row["city"],
                        row["state"],
                        row["latitude"],
                        row["longitude"],
                        row["operator"],
                        row["charger_type"],
                        row["connector_type"],
                        row["power_kw"],
                        row["access_type"],
                        row["opening_hours"],
                        row["contact_phone"],
                        row["source"],
                    ),
                )

            self.db_connection.commit()
            logger.info(f"Upserted {len(df)} stations successfully")

        except Exception as e:
            self.db_connection.rollback()
            logger.error(f"Upsert failed: {e}")
            raise
        finally:
            cursor.close()

    def run_data_collection(self):
        logger.info("Starting data collection")

        all_data = []

        for country in COUNTRY_CODES:
            raw = self.fetch_opencharge_data(country)
            if raw:
                df = self.process_station_data(raw)
                all_data.append(df)

        if all_data:
            combined = pd.concat(all_data, ignore_index=True)
            logger.info(f"Total processed stations: {len(combined)}")
            self.upsert_stations(combined)
        else:
            logger.warning("No data collected")

        logger.info("Data collection completed")

    def close_connection(self):
        if self.db_connection:
            self.db_connection.close()
            logger.info("Database connection closed")


if __name__ == "__main__":
    collector = EVChargingDataCollector()
    try:
        collector.run_data_collection()
    finally:
        collector.close_connection()