from pydantic import BaseModel, Field
from typing import Optional, List


# ==============================
# BASE STATION SCHEMA
# ==============================

class ChargingStationBase(BaseModel):

    station_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None

    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

    operator: Optional[str] = None
    charger_type: Optional[str] = None
    connector_type: Optional[str] = None

    power_kw: Optional[float] = Field(None, ge=0)

    access_type: Optional[str] = None
    opening_hours: Optional[str] = None
    contact_phone: Optional[str] = None

    source: Optional[str] = None


# ==============================
# FULL RESPONSE SCHEMA
# ==============================

class ChargingStation(ChargingStationBase):
    id: int

    model_config = {
        "from_attributes": True
    }


# ==============================
# SEARCH REQUEST SCHEMA
# ==============================

class ChargingStationSearch(BaseModel):

    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    radius_km: float = Field(10, ge=0.1, le=100)
    limit: int = Field(100, ge=1, le=500)

    state: Optional[str] = None
    operator: Optional[str] = None
    connector_type: Optional[str] = None

    min_power_kw: Optional[float] = Field(None, ge=0)


# ==============================
# STATISTICS RESPONSE SCHEMA
# ==============================

class StationStats(BaseModel):

    total_stations: int
    states: List[str]
    operators: List[str]
    connector_types: List[str]

    avg_power_kw: Optional[float] = None