import random

from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta


class AirQualityData(BaseModel):
    Date: datetime
    NO2: float = 10.5
    PM2_5: float = 12.0
    O3: float = 20.0
    PM10: float = 15.0
    temperature_2m_C: float = 18.5
    relative_humidity_2m: float = 60.0
    dew_point_2m_C: float = 10.0
    apparent_temperature_C: float = 18.0
    precipitation_mm: float = 0.0
    pressure_msl_hPa: float = 1015.0
    surface_pressure_hPa: float = 1010.0

    class Config:
        json_schema_extra = {
            "example": {
                "Date": "2023-01-01T00:00:00",
                "NO2": 10.5,
                "PM2_5": 12.0,
                "O3": 20.0,
                "PM10": 15.0,
                "temperature_2m_C": 18.5,
                "relative_humidity_2m": 60.0,
                "dew_point_2m_C": 10.0,
                "apparent_temperature_C": 18.0,
                "precipitation_mm": 0.0,
                "pressure_msl_hPa": 1015.0,
                "surface_pressure_hPa": 1010.0
            }
        }


class AirQualityDataList(BaseModel):
    data: List[AirQualityData]

    class Config:
        json_schema_extra = {
            "data": [
                {
                    "Date": (datetime(2023, 1, 1) + timedelta(days=i)).isoformat(),
                    "NO2": random.uniform(5, 15),
                    "PM2_5": random.uniform(10, 20),
                    "O3": random.uniform(15, 25),
                    "PM10": random.uniform(10, 20),
                    "temperature_2m_C": random.uniform(15, 25),
                    "relative_humidity_2m": random.uniform(50, 70),
                    "dew_point_2m_C": random.uniform(5, 15),
                    "apparent_temperature_C": random.uniform(15, 25),
                    "precipitation_mm": random.uniform(0, 5),
                    "pressure_msl_hPa": random.uniform(1000, 1020),
                    "surface_pressure_hPa": random.uniform(995, 1015)
                }
                for i in range(21)
            ]
        }
