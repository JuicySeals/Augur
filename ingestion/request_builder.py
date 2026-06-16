# ingestion/request_builder.py

import yaml
import os
from config.cities import CITIES

MODEL_API_STRINGS = {
    "GFS": "gfs_seamless",
    "NAM": "ncep_nam_conus",
    "ECMWF": "ecmwf_ifs025",
    "HRRR": "gfs_hrrr",
    "NBM": "ncep_nbm_conus"
}

def build_forecast_request(
    city_code: str,
    models: list[str],
    forecast_days: int = 3,
    temperature_unit: str = "fahrenheit"
) -> str:
    city = CITIES[city_code]

    lat = city["lat"]
    lon = city["lon"]
    timezone = city["timezone"]

    api_models = ",".join([MODEL_API_STRINGS[m] for m in models])

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&temperature_unit={temperature_unit}"
        f"&timezone={timezone}"
        f"&forecast_days={forecast_days}"
        f"&models={api_models}"
    )

    return url