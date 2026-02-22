from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from dotenv import load_dotenv
from backend.models import ChargingStation, ChargingStationSearch, StationStats, ChargingStationBase

from backend.database import get_db, ChargingStation as DBChargingStation
from backend.models import ChargingStation, ChargingStationSearch, StationStats

from fastapi.responses import StreamingResponse
import csv
import io
# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="EV Charging Station API",
    description="API for EV charging station data with PostGIS spatial support",
    version="1.0.0"
)

# Enable CORS (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROOT ENDPOINT
@app.get("/")
async def root():
    return {
        "message": "EV Charging Station API running",
        "version": "1.0.0"
    }


# HEALTH CHECK
@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }


# NEARBY STATIONS (Must come before /stations/{station_id})
@app.get("/stations/nearby", response_model=List[ChargingStation])
async def get_nearby_stations(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    radius: float = Query(10, description="Radius in kilometers"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    point = func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326)

    stations = (
        db.query(DBChargingStation)
        .filter(func.ST_DWithin(DBChargingStation.location, point, radius * 1000))
        .order_by(func.ST_Distance(DBChargingStation.location, point))
        .limit(limit)
        .all()
    )

    return stations


# GET ALL STATIONS
@app.get("/stations", response_model=List[ChargingStation])
async def get_stations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    state: Optional[str] = Query(None),
    operator: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(DBChargingStation)

    if state:
        query = query.filter(DBChargingStation.state.ilike(f"%{state}%"))

    if operator:
        query = query.filter(DBChargingStation.operator.ilike(f"%{operator}%"))

    stations = query.offset(skip).limit(limit).all()

    return stations


@app.get("/stations/export")
def export_stations_csv(db: Session = Depends(get_db)):

    stations = db.query(DBChargingStation).all()

    output = io.StringIO()
    writer = csv.writer(output)

    # CSV Header
    writer.writerow([
        "id",
        "station_name",
        "address",
        "city",
        "state",
        "latitude",
        "longitude",
        "operator",
        "connector_type",
        "power_kw",
        "access_type",
        "opening_hours",
        "contact_phone",
        "source"
    ])

    # CSV Rows
    for s in stations:
        writer.writerow([
            s.id,
            s.station_name,
            s.address,
            s.city,
            s.state,
            s.latitude,
            s.longitude,
            s.operator,
            s.connector_type,
            s.power_kw,
            s.access_type,
            s.opening_hours,
            s.contact_phone,
            s.source
        ])

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=ev_stations.csv"
        }
    )

# GET SINGLE STATION BY ID
@app.get("/stations/{station_id}", response_model=ChargingStation)
async def get_station(
    station_id: int,
    db: Session = Depends(get_db)
):
    station = (
        db.query(DBChargingStation)
        .filter(DBChargingStation.id == station_id)
        .first()
    )

    if not station:
        raise HTTPException(
            status_code=404,
            detail="Charging station not found"
        )

    return station


# ADVANCED SEARCH
@app.post("/stations/search", response_model=List[ChargingStation])
async def search_stations(
    search: ChargingStationSearch,
    db: Session = Depends(get_db)
):
    point = func.ST_SetSRID(
        func.ST_MakePoint(search.longitude, search.latitude),
        4326
    )

    query = db.query(DBChargingStation).filter(
        func.ST_DWithin(DBChargingStation.location, point, search.radius_km * 1000)
    )

    if search.state:
        query = query.filter(
            DBChargingStation.state.ilike(f"%{search.state}%")
        )

    if search.operator:
        query = query.filter(
            DBChargingStation.operator.ilike(f"%{search.operator}%")
        )

    if search.connector_type:
        query = query.filter(
            DBChargingStation.connector_type.ilike(
                f"%{search.connector_type}%"
            )
        )

    if search.min_power_kw:
        query = query.filter(
            DBChargingStation.power_kw >= search.min_power_kw
        )

    stations = (
        query.order_by(func.ST_Distance(DBChargingStation.location, point))
        .limit(search.limit)
        .all()
    )

    return stations


# STATISTICS ENDPOINT
@app.get("/stats", response_model=StationStats)
async def get_stats(db: Session = Depends(get_db)):

    total = db.query(func.count(DBChargingStation.id)).scalar()

    avg_power = db.query(
        func.avg(DBChargingStation.power_kw)
    ).scalar()

    states = [
        s[0] for s in db.query(DBChargingStation.state)
        .distinct()
        .filter(DBChargingStation.state.isnot(None))
        .all()
        if s[0]
    ]

    operators = [
        o[0] for o in db.query(DBChargingStation.operator)
        .distinct()
        .filter(DBChargingStation.operator.isnot(None))
        .all()
        if o[0]
    ]

    connector_types = [
        c[0] for c in db.query(DBChargingStation.connector_type)
        .distinct()
        .filter(DBChargingStation.connector_type.isnot(None))
        .all()
        if c[0]
    ]

    return StationStats(
        total_stations=total,
        avg_power_kw=float(avg_power) if avg_power else None,
        states=states[:20],
        operators=operators[:20],
        connector_types=connector_types[:20]
    )

# CREATE NEW STATION
@app.post("/stations", response_model=ChargingStation)
async def create_station(
    station: ChargingStationBase,
    db: Session = Depends(get_db)
):

    db_station = DBChargingStation(

        station_name=station.station_name,
        address=station.address,
        city=station.city,
        state=station.state,

        latitude=station.latitude,
        longitude=station.longitude,

        operator=station.operator,
        charger_type=station.charger_type,
        connector_type=station.connector_type,

        power_kw=station.power_kw,

        access_type=station.access_type,
        opening_hours=station.opening_hours,
        contact_phone=station.contact_phone,

        source=station.source,

        location=func.ST_SetSRID(
            func.ST_MakePoint(
                station.longitude,
                station.latitude
            ),
            4326
        )
    )

    db.add(db_station)

    db.commit()

    db.refresh(db_station)

    return db_station


#Update Endpoint 
@app.put("/stations/{station_id}", response_model=ChargingStation)
async def update_station(
    station_id: int,
    station: ChargingStationBase,
    db: Session = Depends(get_db)
):
    db_station = db.query(DBChargingStation).filter(
        DBChargingStation.id == station_id
    ).first()

    if not db_station:
        raise HTTPException(404, "Station not found")

    for key, value in station.dict().items():
        setattr(db_station, key, value)

    db.commit()
    db.refresh(db_station)

    return db_station
#delet Endpoint 
@app.delete("/stations/{station_id}")
async def delete_station(
    station_id: int,
    db: Session = Depends(get_db)
):
    db_station = db.query(DBChargingStation).filter(
        DBChargingStation.id == station_id
    ).first()

    if not db_station:
        raise HTTPException(404, "Station not found")

    db.delete(db_station)
    db.commit()

    return {"message": "Station deleted successfully"}

@app.get("/debug/db-status")
def db_status(db: Session = Depends(get_db)):

    total = db.query(func.count(DBChargingStation.id)).scalar()

    sample = db.query(
        DBChargingStation.id,
        DBChargingStation.station_name,
        DBChargingStation.city
    ).limit(5).all()

    return {
        "database_connected": True,
        "total_stations": total,
        "sample_data": [
            {
                "id": s.id,
                "station_name": s.station_name,
                "city": s.city
            }
            for s in sample
        ]
    }



# LOCAL RUN SUPPORT
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=True
    )
