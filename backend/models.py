from pydantic import BaseModel
from typing import Optional, List


# Base schema matching ev_stations table
class ChargingStationBase(BaseModel):

    station_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    operator: Optional[str] = None
    charger_type: Optional[str] = None
    connector_type: Optional[str] = None

    power_kw: Optional[float] = None

    access_type: Optional[str] = None
    opening_hours: Optional[str] = None
    contact_phone: Optional[str] = None

    source: Optional[str] = None



# Full schema returned by API
class ChargingStation(ChargingStationBase):

    id: int

    class Config:
        from_attributes = True


# Search request schema
class ChargingStationSearch(BaseModel):

    latitude: float
    longitude: float

    radius_km: Optional[float] = 10
    limit: Optional[int] = 100

    state: Optional[str] = None
    operator: Optional[str] = None
    connector_type: Optional[str] = None

    min_power_kw: Optional[float] = None


# Statistics schema
class StationStats(BaseModel):

    total_stations: int

    states: List[str]
    operators: List[str]
    connector_types: List[str]

    avg_power_kw: Optional[float]
